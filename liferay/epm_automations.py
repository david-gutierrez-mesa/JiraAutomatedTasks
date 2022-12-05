#!/usr/bin/env python
from jira_liferay import get_jira_connection
from testmap_jira import get_testmap_connection

SUB_COMPONENTS_JSON_URL = 'https://issues.liferay.com/rest/net.brokenbuild.subcomponents/1.0/subcomponents/LPS.json'

EPM_SPREADSHEET_ID = '1azJIucqKawYB7TMCnUIfmNac9iQEfkPDR5JKM6Nzia0'
EPM_TAB_BY_LEVEL_NAME = 'By Top Level Grouping'
EPM_TAB_BY_LEVEL_ID = '1959442404'
EPM_BY_LEVEL_TABLE_START_INDEX = '4'
EPM_BY_LEVEL_SPREADSHEET_RANGE = EPM_TAB_BY_LEVEL_NAME + '!B' + EPM_BY_LEVEL_TABLE_START_INDEX + ':K'
EPM_BY_LEVEL_FIRST_LEVEL_RANGE = EPM_TAB_BY_LEVEL_NAME + '!B' + EPM_BY_LEVEL_TABLE_START_INDEX + ':B'


def _create_collapse_group_body(local_requests, sheet_id, start, end):
    local_requests.append([{
        "addDimensionGroup": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": start,
                "endIndex": end
            }
        }
    }])


def _delete_all_raw_groups(sheet, spreadsheet_id, sheet_id):
    row_groups = _get_all_row_groups(sheet, spreadsheet_id, sheet_id)
    local_requests = []
    if row_groups is not None:
        for raw_group in row_groups:
            local_requests.append([{
                "deleteDimensionGroup": {
                    "range": {
                        'sheetId': raw_group.get('range').get('sheetId'),
                        'dimension': raw_group.get('range').get('dimension'),
                        'startIndex': raw_group.get('range').get('startIndex'),
                        'endIndex': raw_group.get('range').get('endIndex')
                    }
                }
            }])
        body = {
            'requests': local_requests
        }
        sheet.batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()


def _get_all_row_groups(sheet, spreadsheet_id, range_metadata):
    metadata = sheet.get(spreadsheetId=spreadsheet_id, ranges=range_metadata).execute()
    return metadata.get('sheets')[0].get('rowGroups')


def _line_data(line, components_full_info, deep, children):
    lead = ''
    archived = False
    for component in components_full_info:
        if component.name == line.get('name'):
            if hasattr(component, 'lead'):
                lead = component.lead.displayName
            else:
                print("\"", component.name, "\" has not lead")
            archived = component.archived
            break
    if lead == '':
        lead = line.get('lead')
    if archived:
        status = 'Deprecated'
    else:
        status = 'Active'
    match deep:
        case 0:
            return [line.get('id'), line.get('name'), '', '', '', len(children), line.get('type').capitalize(),
                    status,
                    lead, line.get('description')]
        case 1:
            return ['', '', line.get('name'), '', '', len(children), line.get('type').capitalize(), status,
                    lead, line.get('description')]
        case 2:
            return ['', '', '', line.get('name'), '', len(children), line.get('type').capitalize(), status,
                    lead, line.get('description')]
        case _:
            return ['', '', '', '', line.get('name'), len(children), line.get('type').capitalize(), status,
                    lead, line.get('description')]


def _process_line(body_values, line, components_full_info, deep):
    children = line.get('children', {})
    body_values.append(_line_data(line, components_full_info, deep, children))

    for child in children:
        _process_line(body_values, child, components_full_info, deep + 1)


def update_components_sheet(jira):
    components = jira._get_json("", None, SUB_COMPONENTS_JSON_URL)['subcomponents']
    components_full_info = jira.project_components("LPS")
    sheet = get_testmap_connection()
    sheet.values().clear(
        spreadsheetId=EPM_SPREADSHEET_ID, range=EPM_BY_LEVEL_SPREADSHEET_RANGE).execute()
    _delete_all_raw_groups(sheet, EPM_SPREADSHEET_ID, EPM_BY_LEVEL_SPREADSHEET_RANGE)
    body_values = []
    for component in components:
        _process_line(body_values, component, components_full_info, 0)

    body = {
        'values': body_values
    }
    sheet.values().append(
        spreadsheetId=EPM_SPREADSHEET_ID, range=EPM_BY_LEVEL_SPREADSHEET_RANGE, valueInputOption='USER_ENTERED',
        body=body).execute()

    l1_list = sheet.values().get(spreadsheetId=EPM_SPREADSHEET_ID, range=EPM_BY_LEVEL_FIRST_LEVEL_RANGE).execute() \
        .get('values', [])
    start = -1
    local_requests = []
    for level1 in enumerate(l1_list):
        if len(level1[1]) != 0:
            if level1[1][0] != '':
                if start >= 0:
                    if level1[0] - start > 1:
                        _create_collapse_group_body(local_requests, EPM_TAB_BY_LEVEL_ID,
                                                    start + int(EPM_BY_LEVEL_TABLE_START_INDEX),
                                                    level1[0] + int(EPM_BY_LEVEL_TABLE_START_INDEX) - 1)

                start = level1[0]
    body = {
        'requests': local_requests
    }
    sheet.batchUpdate(
        spreadsheetId=EPM_SPREADSHEET_ID,
        body=body).execute()


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    update_components_sheet(jira_connection)
