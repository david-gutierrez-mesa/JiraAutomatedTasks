#!/usr/bin/env python
from liferay.teams.uniform.uniform_constants import FileName, Sheets
from liferay.utils.jira.jira_constants import Filter
from liferay.utils.file_helpers import create_output_files
from liferay.utils.jira.jira_liferay import get_jira_connection
from liferay.utils.sheets.sheets_liferay import get_testmap_connection
from liferay.utils.sheets.testmap_helpers import update_bug_threshold, update_test_map

BUG_THRESHOLD_TAB = 'JIRA-BUGS-7.4'
BUG_THRESHOLD_TAB_RANGE = BUG_THRESHOLD_TAB + '!B3:L'
JIRA_TEST_MAP_TAB = "JIRA-TestMap-7.4"
JIRA_TEST_MAP_TAB_RANGE = JIRA_TEST_MAP_TAB + '!B3:I'


def update_uniform_bug_threshold(sheet, jira, output_info):
    output_info = update_bug_threshold(sheet, jira, output_info, Filter.Uniform_Bugs_Unresolved,
                                       Sheets.UNIFORM_TESTMAP_ID, BUG_THRESHOLD_TAB, BUG_THRESHOLD_TAB_RANGE)
    return output_info


def update_uniform_test_map(sheet, jira, output_info):
    output_info = update_test_map(sheet, jira, output_info, Filter.Uniform_7_4_CE_GA_All,
                                  Sheets.UNIFORM_TESTMAP_ID, JIRA_TEST_MAP_TAB, JIRA_TEST_MAP_TAB_RANGE)
    return output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    jira_connection = get_jira_connection()
    sheet_connection = get_testmap_connection()
    info = update_uniform_test_map(sheet_connection, jira_connection, info)
    info = update_uniform_bug_threshold(sheet_connection, jira_connection, info)
    jira_connection.close()

    create_output_files([warning, FileName.OUTPUT_MESSAGE_FILE_NAME],
                        [info, FileName.OUTPUT_INFO_FILE_NAME])