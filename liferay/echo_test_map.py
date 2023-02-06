#!/usr/bin/env python
from collections import Counter

from helpers import create_output_files
from helpers_google_sheet import expand_group, collapse_group
from helpers_jira import read_test_cases_table_from_description
from jira_liferay import get_jira_connection
from helpers_testmap import is_mapped, get_mapped_stories, insert_lines_in_component, remove_underline, update_line, \
    get_group_start_and_end_position
from testmap_jira import get_testmap_connection

CONTROL_PANEL_SHEET_NAME = 'Control panel'
CONTROL_PANEL_NEEDS_AUTOMATION_RANGE = CONTROL_PANEL_SHEET_NAME + '!B11:B'
CONTROL_PANEL_SUMMARY_RANGE = CONTROL_PANEL_SHEET_NAME + '!I2:I5'
BUG_THRESHOLD_SHEET_NAME = 'Bugs Thresholds'
BUG_THRESHOLD_COMPONENT_GROUPS = BUG_THRESHOLD_SHEET_NAME + '!A22:A31'
BUG_THRESHOLD_JIRA_FILERS_ID = BUG_THRESHOLD_SHEET_NAME + '!I4:I13'
BUG_THRESHOLD_MAX_VALUES = BUG_THRESHOLD_SHEET_NAME + '!C22:G31'
ECHO_TESTMAP_ID = '1-7-qJE-J3-jChauzSyCnDvvSbTWeJkSr7u5D_VBOIP0'
ECHO_TESTMAP_SHEET_NAME = 'Test Map'
ECHO_TESTMAP_SHEET_ID = '540408560'
ECHO_TESTMAP_SHEET_LAST_COLUMN = 'Q'
ECHO_TESTMAP_SHEET_COMPONENT_COLUMN = 'I'
ECHO_TESTMAP_SHEET_HEADER_LENGTH = 2
ECHO_TESTMAP_SHEET_FIRST_COLUMN_NUMBER = ECHO_TESTMAP_SHEET_HEADER_LENGTH + 1
OUTPUT_MESSAGE_FILE_NAME = "output_message.txt"
OUTPUT_INFO_FILE_NAME = "output_info.txt"
OUTPUT_BUG_THRESHOLD_EXCEED_FILE_NAME = "bug_threshold_exceed_message.txt"
OUTPUT_BUG_THRESHOLD_WARNING_FILE_NAME = "bug_threshold_warning_message.txt"
TESTMAP_MAPPED_RANGE = ECHO_TESTMAP_SHEET_NAME + '!G4:G'


def _add_lines_to_components_dic(components_testcases_dict, story_component, lines):
    component_in_dictionary = components_testcases_dict.get(story_component)
    if component_in_dictionary is not None:
        for line in lines:
            component_in_dictionary.append(line)
    else:
        components_testcases_dict[story_component] = lines
    return components_testcases_dict


def _insert_lines_in_component(sheet, components_testcases_dict):
    return insert_lines_in_component(sheet, ECHO_TESTMAP_ID, ECHO_TESTMAP_SHEET_ID, ECHO_TESTMAP_SHEET_NAME,
                                     ECHO_TESTMAP_SHEET_LAST_COLUMN, components_testcases_dict,
                                     ECHO_TESTMAP_SHEET_COMPONENT_COLUMN, ECHO_TESTMAP_SHEET_FIRST_COLUMN_NUMBER,
                                     ECHO_TESTMAP_SHEET_HEADER_LENGTH)


def _line_data(lps, summary, priority, test_type, test_status, test_case, test_name, comments, blocked_reason,
               backend_automated, frontend_automated):
    link_text = '=IF(REGEXMATCH(INDIRECT(ADDRESS(ROW(),COLUMN()-1)), ","), HYPERLINK(CONCATENATE(' \
                '"https://issues.liferay.com/issues/?jql=key%20in%20(", INDIRECT(ADDRESS(ROW(),COLUMN()-1)), ")" ),' \
                '"Here"), HYPERLINK(CONCAT("https://issues.liferay.com/browse/",INDIRECT(ADDRESS(ROW(),COLUMN()-1))),' \
                '"Here")) '
    priority_text = ''
    match remove_underline(priority.casefold()):
        case 'low':
            priority_text = '2 - Low'
        case 'medium':
            priority_text = '3 - Medium'
        case 'high':
            priority_text = '4 - High'
        case 'critical':
            priority_text = '5 - Critical'

    if backend_automated.casefold() == 'Yes'.casefold() or frontend_automated.casefold() == 'Yes'.casefold():
        test_type = 'Automation Low Level'
        test_status = 'Automated'

    line = [['N', 'N', 'N', 'N', 'N', 'Y\n(Original)', remove_underline(lps), remove_underline(link_text),
             remove_underline(summary), priority_text, '', remove_underline(test_type), remove_underline(test_status),
             remove_underline(test_case), remove_underline(test_name), remove_underline(comments),
             remove_underline(blocked_reason)]]
    return line


def add_test_cases_to_test_map(sheet, jira, output_warning, output_info):
    print("Adding stories into echo test map")
    stories_to_check = jira.search_issues('filter=55104', fields="key, issuelinks, labels, components, description")
    lps_list = get_mapped_stories(sheet, ECHO_TESTMAP_ID, TESTMAP_MAPPED_RANGE)
    components_testcases_dict = dict([])
    for story in stories_to_check:
        if not is_mapped(story.key, lps_list):
            print("Processing ", story.key)
            labels = story.get_field("labels")
            story_component = story.get_field("components")[0].name
            if 'poshi_test_not_needed' not in labels:
                needs_manual_review = True
                for link in story.fields.issuelinks:
                    linked_issue_key = ""
                    if hasattr(link, "inwardIssue"):
                        linked_issue_key = link.inwardIssue
                    elif hasattr(link, "outwardIssue"):
                        linked_issue_key = link.outwardIssue
                    if linked_issue_key.fields.summary.endswith(' - Product QA | Test Automation Creation'):
                        if linked_issue_key.fields.status.name == 'Closed':
                            linked_issue = jira.issue(linked_issue_key.key)
                            test_cases_table = read_test_cases_table_from_description(linked_issue.fields.description)
                            lines = []
                            for test_case in test_cases_table:
                                test_case_list = test_case.split('|')
                                lines.append(
                                    _line_data(story.key, test_case_list[1], test_case_list[2], 'Poshi',
                                               'Automated', test_case_list[7], test_case_list[8], '', '',
                                               test_case_list[4], test_case_list[5]))
                            _add_lines_to_components_dic(components_testcases_dict, story_component, lines)
                            output_info += "* Added tests for story " + story.key + \
                                           "(https://issues.liferay.com/browse/" + story.key + "): Poshi finished\n"
                        else:
                            test_cases_table = read_test_cases_table_from_description(story.fields.description)
                            lines = []
                            for test_case in test_cases_table:
                                test_case_list = test_case.split('|')
                                lines.append(
                                    _line_data(story.key, test_case_list[1], test_case_list[2], 'Manual',
                                               'Needs Automation', '', '', '', '', test_case_list[4],
                                               test_case_list[5]))
                            _add_lines_to_components_dic(components_testcases_dict, story_component, lines)
                            output_info += "* Added tests for story " + story.key + \
                                           "(https://issues.liferay.com/browse/" + story.key + "): Poshi in progress\n"
                        needs_manual_review = False
                        break
                if needs_manual_review:
                    output_warning += "* " + str(story.key) + \
                                      " (https://issues.liferay.com/browse/" + story.key + ") needs manual review\n "

            else:
                test_cases_table = read_test_cases_table_from_description(story.fields.description)
                lines = []
                for test_case in test_cases_table:
                    test_case_list = test_case.split('|')
                    test_type = 'Manual'
                    test_status = 'Not Possible to Automate'
                    lines.append(_line_data(story.key, test_case_list[1], test_case_list[2], test_type, test_status, '',
                                            '', '', '', test_case_list[4], test_case_list[5]))
                _add_lines_to_components_dic(components_testcases_dict, story_component, lines)
                output_info += "* Added tests for story " + story.key + "(https://issues.liferay.com/browse/" + \
                               story.key + "): Poshi not needed\n"

        else:
            print(story.key, 'is already mapped')
    output_warning += _insert_lines_in_component(sheet, components_testcases_dict)
    return output_warning, output_info


def check_bug_threshold(sheet, jira, output_exceed, output_warning):
    max_values = sheet.values().get(spreadsheetId=ECHO_TESTMAP_ID, range=BUG_THRESHOLD_MAX_VALUES).execute() \
        .get('values', [])
    components_groups = sheet.values().get(spreadsheetId=ECHO_TESTMAP_ID, range=BUG_THRESHOLD_COMPONENT_GROUPS) \
        .execute().get('values', [])
    jira_filter_ids = sheet.values().get(spreadsheetId=ECHO_TESTMAP_ID, range=BUG_THRESHOLD_JIRA_FILERS_ID) \
        .execute().get('values', [])
    for i, filter_id in enumerate(jira_filter_ids):
        bugs_for_component_group = jira.search_issues('filter=' + filter_id[0], fields="customfield_12523")
        bugs_fix_priority = []
        current_component_group = components_groups[i][0]
        for bug in enumerate(bugs_for_component_group):
            fix_priority = bug[1].fields.customfield_12523.value
            bugs_fix_priority.append(fix_priority)
        count_per_priority = Counter(bugs_fix_priority)
        for fp in range(1, 6):
            max_value = int(max_values[i][5 - fp])
            current_bug_numbers = count_per_priority[str(fp)]
            if current_bug_numbers > max_value:
                output_exceed += '* Bug threshold exceed for <https://issues.liferay.com/issues/?filter=' + \
                                 filter_id[0] + "|" + current_component_group + '> in Fix Priority ' + str(fp) + '\n'
            elif max_value != 0 and current_bug_numbers == max_value:
                output_warning += '* Bug threshold just on the limit for <https://issues.liferay.com/issues/?filter=' +\
                                  filter_id[0] + "|" + current_component_group + '> in Fix Priority ' + str(fp) + '\n'

    return output_exceed, output_warning


def check_control_panel_tab(sheet, output_warning):
    summary_status = sheet.values().get(spreadsheetId=ECHO_TESTMAP_ID, range=CONTROL_PANEL_SUMMARY_RANGE).execute() \
        .get('values', [])
    for status in summary_status:
        if status[0] != "FINE":
            output_warning += '* Please check Control Panel: ' + status[0] + '\n'
    return output_warning


def check_need_automation_test_cases(sheet, jira, output_warning, output_info):
    lps_list = sheet.values().get(spreadsheetId=ECHO_TESTMAP_ID, range=CONTROL_PANEL_NEEDS_AUTOMATION_RANGE).execute() \
        .get('values', [])
    test_map_range = ECHO_TESTMAP_SHEET_NAME + '!' + ECHO_TESTMAP_SHEET_COMPONENT_COLUMN + \
                     str(ECHO_TESTMAP_SHEET_FIRST_COLUMN_NUMBER) + ':' + ECHO_TESTMAP_SHEET_COMPONENT_COLUMN
    current_test_cases_list = sheet.values().get(spreadsheetId=ECHO_TESTMAP_ID, range=test_map_range).execute().get(
        'values', [])
    for lps in lps_list:
        story = jira.issue(lps[0])
        component = story.get_field("components")[0].name
        for link in story.fields.issuelinks:
            linked_issue_key = ""
            if hasattr(link, "inwardIssue"):
                linked_issue_key = link.inwardIssue
            elif hasattr(link, "outwardIssue"):
                linked_issue_key = link.outwardIssue
            if linked_issue_key.fields.summary.endswith(' - Product QA | Test Automation Creation'):
                if linked_issue_key.fields.status.name == 'Closed':
                    linked_issue = jira.issue(linked_issue_key.key)
                    test_cases_table = read_test_cases_table_from_description(linked_issue.fields.description)
                    start, end = get_group_start_and_end_position(component, current_test_cases_list,
                                                                  ECHO_TESTMAP_SHEET_HEADER_LENGTH)
                    expand_group(sheet, ECHO_TESTMAP_ID, ECHO_TESTMAP_SHEET_ID, start, end)
                    for test_case in test_cases_table:
                        test_case_list = test_case.split('|')
                        line = _line_data(story.key, test_case_list[1], test_case_list[2], 'Poshi',
                                          'Automated', test_case_list[7], test_case_list[8], '', '',
                                          test_case_list[4], test_case_list[5])
                        output_warning += update_line(sheet, current_test_cases_list, ECHO_TESTMAP_SHEET_NAME,
                                                      ECHO_TESTMAP_ID, ECHO_TESTMAP_SHEET_FIRST_COLUMN_NUMBER, line,
                                                      ECHO_TESTMAP_SHEET_LAST_COLUMN, start, end)
                    output_info += "* Added tests for story " + story.key + \
                                   "(https://issues.liferay.com/browse/" + story.key + "): Poshi finished\n"
                    collapse_group(sheet, ECHO_TESTMAP_ID, ECHO_TESTMAP_SHEET_ID, start, end)
                else:
                    output_info += "* " + str(story.key) + \
                                   " (https://issues.liferay.com/browse/" + story.key + ") is still not automated\n "

    return output_warning, output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    bug_threshold_exceed = ''
    bug_threshold_warning = ''
    jira_connection = get_jira_connection()
    sheet_connection = get_testmap_connection()
    warning, info = check_need_automation_test_cases(sheet_connection, jira_connection, warning, info)
    warning, info = add_test_cases_to_test_map(sheet_connection, jira_connection, warning, info)
    warning = check_control_panel_tab(sheet_connection, warning)
    bug_threshold_exceed, bug_threshold_warning = check_bug_threshold(sheet_connection, jira_connection,
                                                                      bug_threshold_exceed, bug_threshold_warning)

    create_output_files([warning, OUTPUT_MESSAGE_FILE_NAME],
                        [info, OUTPUT_INFO_FILE_NAME],
                        [bug_threshold_exceed, OUTPUT_BUG_THRESHOLD_EXCEED_FILE_NAME],
                        [bug_threshold_warning, OUTPUT_BUG_THRESHOLD_WARNING_FILE_NAME])
