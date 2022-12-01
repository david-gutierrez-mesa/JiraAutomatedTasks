from jira_liferay import get_jira_connection
from testmap_jira import get_testmap_connection

SUB_COMPONENTS_JSON_URL = 'https://issues.liferay.com/rest/net.brokenbuild.subcomponents/1.0/subcomponents/LPS.json'

EPM_SPREADSHEET_ID = '1azJIucqKawYB7TMCnUIfmNac9iQEfkPDR5JKM6Nzia0'
EPM_SPREADSHEET_RANGE = 'By Top Level Grouping_Test!B4:K'


def _line_data(line, deep, children):

    match deep:
        case 0:
            return [line.get('id'), line.get('name'), '', '', '', len(children), line.get('type').capitalize(), 'Active',
                    line.get('lead'), line.get('description')]
        case 1:
            return ['', '', line.get('name'), '', '', len(children), line.get('type').capitalize(), 'Active',
                    line.get('lead'), line.get('description')]
        case 2:
            return ['', '', '', line.get('name'), '', len(children), line.get('type').capitalize(), 'Active',
                    line.get('lead'), line.get('description')]
        case _:
            return ['', '', '', '', line.get('name'), len(children), line.get('type').capitalize(), 'Active',
                    line.get('lead'), line.get('description')]


def _process_line(body_values, line, deep):
    print(deep, line.get('name'))
    children = line.get('children', {})
    body_values.append(_line_data(line, deep, children))

    for child in children:
        _process_line(body_values, child, deep + 1)


def update_components_sheet(jira):
    components = jira._get_json("", None, SUB_COMPONENTS_JSON_URL)['subcomponents']
    sheet = get_testmap_connection()
    sheet.values().clear(
        spreadsheetId=EPM_SPREADSHEET_ID, range=EPM_SPREADSHEET_RANGE).execute()
    body_values = []
    for component in components:
        _process_line(body_values, component, 0)

    body = {
        'values': body_values
    }
    sheet.values().append(
        spreadsheetId=EPM_SPREADSHEET_ID, range=EPM_SPREADSHEET_RANGE, valueInputOption='USER_ENTERED',
        body=body).execute()


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    update_components_sheet(jira_connection)
