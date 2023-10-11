#!/usr/bin/env python
import linecache
import os
import pickle
import re

from liferay.teams.echo.echo_test_map import _line_data, _add_lines_to_components_dic, _insert_lines_in_component
from liferay.utils.file_helpers import search_file_inside_dir
from liferay.utils.jira.jira_liferay import get_jira_connection
from liferay.utils.sheets.sheets_liferay import get_testmap_connection

ECHO_LAST_REPORT_ID = '1owKo77sLqtqNkxod8427blIZkMemEseszHDq8f7X_Tg'
ECHO_TESTMAP_SHEET_ID = '15465545'
POSHI_REPORT_TAB = "Poshi-Report"
POSHI_REPORT_TAB_RANGE = POSHI_REPORT_TAB + '!A3:Q'


def update_echo_test_cases_from_monthly_report(sheet, liferay_repo_path):
    teams = ['Echo', 'Tango']
    all_test_cases = sheet.values().get(spreadsheetId=ECHO_LAST_REPORT_ID, range=POSHI_REPORT_TAB_RANGE).execute()\
        .get('values', [])
    test_not_in_test_map = []
    file_paths_dict = dict()
    tesctcases_paths_name = './tesctcases_paths.pkl'
    check_file = os.path.isfile(tesctcases_paths_name)
    for matrix_i in enumerate(all_test_cases):
        if len(matrix_i[1]) != 0:
            team = matrix_i[1][0].strip()
            if any(team in s for s in teams):
                on_the_test_map = matrix_i[1][16].strip()
                if on_the_test_map == 'NOT Tracked':
                    test_not_in_test_map.append(matrix_i)
                    if not check_file:
                        file_name = matrix_i[1][4].strip()
                        if file_name not in file_paths_dict:
                            file_path = search_file_inside_dir(liferay_repo_path, file_name + '.testcase')
                            file_paths_dict[file_name] = file_path
                            print("Adding path" + file_path + "\n")

    if check_file:
        with open(tesctcases_paths_name, 'rb') as inp:
            file_paths_dict = pickle.load(inp)
    else:
        with open(tesctcases_paths_name, 'wb') as f:
            pickle.dump(file_paths_dict, f, pickle.HIGHEST_PROTOCOL)

    components_testcases_dict = dict([])
    lps_missing = 0
    priority_missing = 0
    description_missing = 0
    testcases_to_be_added = 0
    list_missing_priority = []
    list_missing_description = []
    for matrix_i in enumerate(test_not_in_test_map):
        file_name = matrix_i[1][1][4].strip()
        test_name = matrix_i[1][1][5].strip()
        component = matrix_i[1][1][1].strip()
        file_path = file_paths_dict.get(file_name)
        line_no = 0
        description = ''
        lps_number = ''
        priority = ''
        lines = []
        if not file_path:
            print('[WARNING] No path found for ' + file_name + ' when trying to add case ' + test_name )
            continue
        with open(file_path, 'r') as fp:
            for l_no, line in enumerate(fp):
                if 'test ' + test_name in line:
                    line_no = l_no
                    break
        last_property = False
        for annotations_line in range(line_no, line_no-5, -1):
            properties_line = linecache.getline(file_path, annotations_line)
            if '@description' in properties_line:
                description = properties_line.split('=')[1].strip().strip('"')
                lps_number = re.findall(r'\bLPS-\w+', description)
                if last_property:
                    break
                else:
                    last_property = True
            elif '@priority' in properties_line:
                priority = properties_line.split('=')[1].strip()
                if last_property:
                    break
                else:
                    last_property = True
        if not lps_number:
            lps_number = '-'
        if not description:
            description = file_name + '#' + test_name
        if priority:
            testcases_to_be_added += 1
            priority_text = 'low'
            match priority:
                case '3':
                    priority_text = 'medium'
                case '4':
                    priority_text = 'high'
                case '5':
                    priority_text = 'critical'
            lines.append(
                _line_data(', '.join(lps_number), description, priority_text, 'Poshi', 'Automated', file_name,
                           test_name, '', '', 'No', 'No'))
            _add_lines_to_components_dic(components_testcases_dict, component, lines)

        if not lps_number:
            lps_missing += 1
        if not description:
            description_missing += 1
            list_missing_description.append(file_name + ' ' + test_name + ' ' + file_path)
        if not priority:
            priority_missing += 1
            list_missing_priority.append(file_name + ' ' + test_name + ' ' + file_path)

    output_warning = _insert_lines_in_component(sheet, components_testcases_dict)
    print("Total test cases to be added: " + str(testcases_to_be_added))
    print("Missing LPS: " + str(lps_missing))
    print("Missing Description: " + str(description_missing))
    print("   " + "\n   ".join(list_missing_description))
    print("Missing Priority: " + str(priority_missing))
    print("   " + "\n   ".join(list_missing_priority))
    print("-------------------------------------------")
    print("Warning messages:\n" + output_warning)


if __name__ == "__main__":
    warning = ''
    info = ''
    bug_threshold_exceed = ''
    bug_threshold_warning = ''
    jira_connection = get_jira_connection()
    sheet_connection = get_testmap_connection()
    update_echo_test_cases_from_monthly_report(sheet_connection, '/Users/dgutierrez/Liferay/ENG/liferay-portal')
