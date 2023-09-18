#!/usr/bin/env python
from liferay.teams.frontend_infra.frontend_infra_constants import Sheets, FileName
from liferay.utils.file_helpers import create_output_files
from liferay.utils.jira.jira_constants import Filter
from liferay.utils.jira.jira_liferay import get_jira_connection
from liferay.utils.sheets.testmap_helpers import *
from liferay.utils.sheets.sheets_liferay import get_testmap_connection

BUG_THRESHOLD_TAB = 'JIRA-BUGS'
BUG_THRESHOLD_TAB_RANGE = BUG_THRESHOLD_TAB + '!B3:L'
JIRA_TEST_MAP_TAB = "JIRA-TestMap"
JIRA_TEST_MAP_TAB_RANGE = JIRA_TEST_MAP_TAB + '!B3:H'


def update_frontend_infra_bug_threshold(sheet, jira, output_info):
    output_info = update_bug_threshold(sheet, jira, output_info, Filter.FI_ALL_bugs_unresolved_Manoel,
                                       Sheets.FI_TESTMAP_ID, BUG_THRESHOLD_TAB, BUG_THRESHOLD_TAB_RANGE)
    return output_info


def update_frontend_infra_test_map(sheet, jira, output_info):
    output_info = update_test_map(sheet, jira, output_info, Filter.GSheets_FI_7_4_CE_GA_All, Sheets.FI_TESTMAP_ID,
                                  JIRA_TEST_MAP_TAB, JIRA_TEST_MAP_TAB_RANGE)
    return output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    jira_connection = get_jira_connection()
    sheet_connection = get_testmap_connection()
    info = update_frontend_infra_test_map(sheet_connection, jira_connection, info)
    info = update_frontend_infra_bug_threshold(sheet_connection, jira_connection, info)
    jira_connection.close()

    create_output_files([warning, FileName.OUTPUT_MESSAGE_FILE_NAME],
                        [info, FileName.OUTPUT_INFO_FILE_NAME])
