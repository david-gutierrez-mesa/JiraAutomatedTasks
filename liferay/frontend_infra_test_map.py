#!/usr/bin/env python

from helpers import create_output_files
from jira_liferay import get_jira_connection
from helpers_testmap import *
from testmap_jira import get_testmap_connection

ECHO_TESTMAP_ID = '1_liLRC1XHBydH_mfeeDifgKxBWN3kfRtX7uqbKgJ72k'
JIRA_TEST_MAP_TAB = "JIRA-TestMap"
JIRA_TEST_MAP_TAB_RANGE = JIRA_TEST_MAP_TAB + '!B3:H'
OUTPUT_MESSAGE_FILE_NAME = "output_message.txt"
OUTPUT_INFO_FILE_NAME = "output_info.txt"


def update_frontend_infra_test_map(sheet, jira, output_info):
    output_info = update_test_map(sheet, jira, output_info, 'filter=50189', ECHO_TESTMAP_ID, JIRA_TEST_MAP_TAB,
                                  JIRA_TEST_MAP_TAB_RANGE)
    return output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    jira_connection = get_jira_connection()
    sheet_connection = get_testmap_connection()
    info = update_frontend_infra_test_map(sheet_connection, jira_connection, info)

    create_output_files([warning, OUTPUT_MESSAGE_FILE_NAME],
                        [info, OUTPUT_INFO_FILE_NAME])
