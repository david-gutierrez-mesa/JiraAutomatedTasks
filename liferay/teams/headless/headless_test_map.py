#!/usr/bin/env python

from helpers import create_output_files
from jira_constants import Filter
from jira_liferay import get_jira_connection
from helpers_testmap import *
from testmap_jira import get_testmap_connection

BUG_THRESHOLD_TAB = 'JIRA-BUGSv2'
BUG_THRESHOLD_TAB_RANGE = BUG_THRESHOLD_TAB + '!B3:L'
HEADLESS_TESTMAP_ID = '19KSqxtKJQ5FHZbHKxDS3_TzptWeD0DrL-mLk0y0WFYY'
JIRA_TEST_MAP_TAB = "JIRA-TestMap"
JIRA_TEST_MAP_TAB_RANGE = JIRA_TEST_MAP_TAB + '!C3:I'
OUTPUT_MESSAGE_FILE_NAME = "output_message.txt"
OUTPUT_INFO_FILE_NAME = "../../output_info.txt"
OUTPUT_BUG_THRESHOLD_INFO_FILE_NAME = "bug_threshold_output_info.txt"


def update_headless_bug_threshold(sheet, jira, output_info):
    output_info = update_bug_threshold(sheet, jira, output_info, Filter.Headless_All_verified_Bugs_in_master,
                                       HEADLESS_TESTMAP_ID, BUG_THRESHOLD_TAB, BUG_THRESHOLD_TAB_RANGE)
    return output_info


def update_headless_test_map(sheet, jira, output_info):
    output_info = update_test_map(sheet, jira, output_info, Filter.GSheets_Headless_All_Stories,
                                  HEADLESS_TESTMAP_ID, JIRA_TEST_MAP_TAB, JIRA_TEST_MAP_TAB_RANGE)
    return output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    jira_connection = get_jira_connection()
    sheet_connection = get_testmap_connection()
    info = update_headless_test_map(sheet_connection, jira_connection, info)
    info = update_headless_bug_threshold(sheet_connection, jira_connection, info)

    create_output_files([warning, OUTPUT_MESSAGE_FILE_NAME],
                        [info, OUTPUT_INFO_FILE_NAME])
