#!/usr/bin/env python
from helpers_jira import read_test_cases_table_from_description
from jira_liferay import get_jira_connection
from liferay.helpers_testmap import is_mapped, get_mapped_stories, insert_lines_in_component, remove_underline
from liferay.testmap_jira import get_testmap_connection

ECHO_TESTMAP_ID = '1-7-qJE-J3-jChauzSyCnDvvSbTWeJkSr7u5D_VBOIP0'
ECHO_TESTMAP_SHEET_NAME = 'Test Map'
ECHO_TESTMAP_SHEET_ID = '540408560'
ECHO_TESTMAP_SHEET_LAST_COLUMN = 'Q'
ECHO_TESTMAP_SHEET_COMPONENT_COLUMN = 'I'
ECHO_TESTMAP_SHEET_HEADER_LENGTH = 2
ECHO_TESTMAP_SHEET_FIRST_COLUMN_NUMBER = ECHO_TESTMAP_SHEET_HEADER_LENGTH + 1
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


def add_test_cases_to_test_map(jira):
    print("Adding stories into echo test map")
    sheet = get_testmap_connection()
    stories_to_check = jira.search_issues('filter=55104', fields="key, issuelinks, labels, components, description")
    lps_list = get_mapped_stories(sheet, ECHO_TESTMAP_ID, TESTMAP_MAPPED_RANGE)
    components_testcases_dict = dict([])
    output_message = ''
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
                        else:
                            test_cases_table = read_test_cases_table_from_description(story.fields.description)
                            lines = []
                            for test_case in test_cases_table:
                                test_case_list = test_case.split('|')
                                test_type = 'Manual'
                                test_status = 'Needs Automation'
                                lines.append(
                                    _line_data(story.key, test_case_list[1], test_case_list[2], test_type, test_status,
                                               '', '', '', '', test_case_list[4], test_case_list[5]))
                            _add_lines_to_components_dic(components_testcases_dict, story_component, lines)
                        needs_manual_review = False
                        break
                if needs_manual_review:
                    output_message += str(story.key) + " needs manual review\n"

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

        else:
            print(story.key, 'is already mapped')
    output_message += _insert_lines_in_component(sheet, components_testcases_dict)
    return output_message


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    add_test_cases_to_test_map(jira_connection)
    print(add_test_cases_to_test_map(jira_connection))
