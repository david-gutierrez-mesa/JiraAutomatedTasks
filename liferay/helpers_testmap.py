from itertools import islice

from helpers_google_sheet import *
from helpers_jira import get_all_issues
from jira_constants import CustomField


def component_row(component, matrix):
    position = -1
    for i, matrix_i in enumerate(matrix):
        if component in matrix_i[0]:
            position = i
            break
    return position


def get_components(story):
    return [component.name for component in story.get_field("components")]


def get_component_in_team_components(story, team_components):
    components = story.get_field("components")
    for component in components:
        if component.name in team_components:
            return component.name
    return ''


def get_group_start_and_end_position(component, matrix, header_length):
    starting = component_row('Component: ' + component, matrix)
    if starting >= 0:
        for i in range(starting + 1, len(matrix)):
            if len(matrix[i]) != 0:
                if 'Component:' in matrix[i][0] or 'Others:' in matrix[i][0]:
                    return starting + header_length + 1, i + header_length
        return 0, 0
    else:
        return -1, -1


def get_line_position_by_test_case_name(lps_list, header_length, test_case_name, start, end):
    for pos, matrix_i in islice(enumerate(lps_list), start, end):
        if len(matrix_i) != 0:
            if len(matrix_i[0]) != 0:
                value = matrix_i[0].strip()
                if value == test_case_name.strip():
                    return pos + header_length
    return -1


def get_mapped_stories(sheet, test_map_id, test_map_range):
    lps_list = sheet.values().get(spreadsheetId=test_map_id, range=test_map_range).execute().get('values', [])
    lps_list_strings = []
    for matrix_i in enumerate(lps_list):
        if len(matrix_i[1]) != 0:
            value = matrix_i[1][0].strip()
            if ',' in value:
                several_lps_covered = value.split(',')
                for lps_covered in several_lps_covered:
                    lps_covered = lps_covered.strip()
                    if lps_covered not in lps_list_strings:
                        lps_list_strings.append(lps_covered)
            else:
                if value not in lps_list_strings:
                    lps_list_strings.append(value)

    return lps_list_strings


def is_mapped(element, lps_list_strings):
    if element in lps_list_strings:
        return True
    else:
        return False


def insert_line_after(sheet, spreadsheet_id, sheet_id, sheet_name, sheet_last_column, index, line):
    insert_one_row_after(sheet, spreadsheet_id, sheet_id, index)
    body = {
        'values': line
    }
    range_name = sheet_name + '!A' + str(index + 1) + ':' + sheet_last_column + str(index)
    sheet.values().append(
        spreadsheetId=spreadsheet_id, range=range_name, valueInputOption='USER_ENTERED', body=body).execute()


def insert_lines_in_component(sheet, spreadsheet_id, sheet_id, sheet_name, sheet_last_column,
                              components_testcases_dict, component_column, first_column_number, header_length):
    test_map_cases_column = sheet_name + '!' + component_column + str(first_column_number) + ':' + component_column
    output_message = ''

    for component, test_cases in components_testcases_dict.items():
        matrix = sheet.values().get(spreadsheetId=spreadsheet_id, range=test_map_cases_column).execute() \
            .get('values', [])
        start, end = get_group_start_and_end_position(component, matrix, header_length)

        if start == -1:
            output_message += '* Component "' + component + '" does not exist on ' + sheet_name +\
                              '. Please consider adding it manually\n'
        else:
            if start != end:
                expand_group(sheet, spreadsheet_id, sheet_id, start, end)

            for test_case in reversed(test_cases):
                insert_line_after(sheet, spreadsheet_id, sheet_id, sheet_name, sheet_last_column, end, test_case)

            if start == end:
                create_collapse_group(sheet, spreadsheet_id, sheet_id, start, end + len(test_cases))
            collapse_group(sheet, spreadsheet_id, sheet_id, start, end + len(test_cases))

    return output_message


def update_line(sheet, lps_list, test_map_sheet_name, spreadsheet_id, header_length, line, sheet_last_column, start,
                end):
    position = get_line_position_by_test_case_name(lps_list, header_length, line[0][8], start, end)
    if position == -1:
        return '* Test with summary "' + line[0][8] + '" not found in story ' + line[0][6] + \
               "(https://issues.liferay.com/browse/" + line[0][6] + ")\n"
    body = {
        'values': line
    }
    range_name = test_map_sheet_name + '!A' + str(position) + ':' + sheet_last_column + str(position)
    sheet.values().update(
        spreadsheetId=spreadsheet_id, range=range_name, valueInputOption="USER_ENTERED", body=body).execute()
    return ''


def update_bug_threshold(sheet, jira, output_info, jira_filter, testmap_id, jira_test_map_tab, jira_test_map_tab_range):
    stories_to_add_to_test_map_bug_threshold = get_all_issues(jira, jira_filter,
                                                ["key", "summary", "issuetype", "status", "labels",
                                                 "components", "customfield_12523"])
    body_values = []
    for story in stories_to_add_to_test_map_bug_threshold:
        components = ', '.join(get_components(story))
        labels = ','.join(story.get_field('labels'))
        body_values.append([story.key,
                            story.get_field('summary'),
                            story.get_field('issuetype').name,
                            story.get_field('status').name,
                            labels,
                            components,
                            story.get_field('customfield_12523').name])

    sheet.values().clear(
        spreadsheetId=testmap_id, range=jira_test_map_tab_range).execute()

    body = {
        'values': body_values
    }
    sheet.values().append(
        spreadsheetId=testmap_id,
        range=jira_test_map_tab_range,
        valueInputOption='USER_ENTERED',
        body=body).execute()

    set_update_time_in_cell(sheet, testmap_id, jira_test_map_tab + '!A1')

    output_info += 'Bug Threshold from Test Map Updated\n'

    return output_info


def update_test_map(sheet, jira, output_info, jira_filter, testmap_id, jira_test_map_tab, jira_test_map_tab_range):
    stories_to_add_to_test_map = get_all_issues(jira, jira_filter,
                                                ["key", "summary", "issuetype", "status", "labels",
                                                 "components", CustomField.Epic_Link])
    body_values = []
    for story in stories_to_add_to_test_map:
        components = ', '.join(get_components(story))
        labels = ','.join(story.get_field('labels'))
        epic_link = story.get_field(CustomField.Epic_Link)
        if epic_link is None:
            epic = 'n/a'
        else:
            epic = jira.issue(epic_link, fields='summary').get_field('summary')
        body_values.append([story.key,
                            story.get_field('summary'),
                            story.get_field('issuetype').name,
                            story.get_field('status').name,
                            labels,
                            components,
                            epic])

    sheet.values().clear(
        spreadsheetId=testmap_id, range=jira_test_map_tab_range).execute()

    body = {
        'values': body_values
    }
    sheet.values().append(
        spreadsheetId=testmap_id,
        range=jira_test_map_tab_range,
        valueInputOption='USER_ENTERED',
        body=body).execute()

    set_update_time_in_cell(sheet, testmap_id, jira_test_map_tab + '!A1')

    output_info += 'Test map updated\n'

    return output_info


def remove_underline(string):
    return string.strip('-')
