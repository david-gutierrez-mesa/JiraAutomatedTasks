#!/usr/bin/env python

from helpers import create_output_files
from jira_constants import Filter
from jira_liferay import get_jira_connection
from helpers_testmap import *
from testmap_jira import get_testmap_connection

BUG_THRESHOLD_TAB = 'JIRA-BUGS'
BUG_THRESHOLD_TAB_RANGE = BUG_THRESHOLD_TAB + '!B2:L'
ECHO_TESTMAP_ID = '1_liLRC1XHBydH_mfeeDifgKxBWN3kfRtX7uqbKgJ72k'
JIRA_TEST_MAP_TAB = "JIRA-TestMap"
JIRA_TEST_MAP_TAB_RANGE = JIRA_TEST_MAP_TAB + '!B3:H'
OUTPUT_MESSAGE_FILE_NAME = "output_message.txt"
OUTPUT_INFO_FILE_NAME = "output_info.txt"
OUTPUT_BUG_THRESHOLD_INFO_FILE_NAME = "bug_threshold_output_info.txt"

def update_frontend_infra_bug_threshold(sheet, jira, bug_threshold_output_info):
    bug_threshold_output_info = update_bug_threshold(sheet, jira, bug_threshold_output_info, 'filter=56141', ECHO_TESTMAP_ID, BUG_THRESHOLD_TAB,
                                  BUG_THRESHOLD_TAB_RANGE)
    return bug_threshold_output_info

def update_frontend_infra_test_map(sheet, jira, output_info):
    output_info = update_test_map(sheet, jira, output_info, Filter.GSheets_FI_7_4_CE_GA_All, ECHO_TESTMAP_ID,
                                  JIRA_TEST_MAP_TAB, JIRA_TEST_MAP_TAB_RANGE)
    return output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    bug_threshold_info = ''
    jira_connection = get_jira_connection()
    sheet_connection = get_testmap_connection()
    info = update_frontend_infra_test_map(sheet_connection, jira_connection, info)
    bug_threshold_info = update_frontend_infra_bug_threshold(sheet_connection, jira_connection, bug_threshold_info)

    create_output_files([warning, OUTPUT_MESSAGE_FILE_NAME],
                        [info, OUTPUT_INFO_FILE_NAME],
                        [bug_threshold_info, OUTPUT_BUG_THRESHOLD_INFO_FILE_NAME])
