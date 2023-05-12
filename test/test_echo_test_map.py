import unittest

from echo_test_map import *
from helpers_jira import get_team_components
from jira_liferay import get_jira_connection
from testmap_jira import get_testmap_connection


class EchoTestMapTests(unittest.TestCase):
    def test_add_test_cases_to_test_map(self):
        try:
            message = ''
            info_test = ''
            jira_connection_test = get_jira_connection()
            sheet_connection_test = get_testmap_connection()
            team_components_test = get_team_components(jira_connection, 'LPS', 'Product Team Echo')
            message, info_test = add_test_cases_to_test_map(sheet_connection_test, jira_connection_test,
                                                            team_components_test,
                                                            message, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_check_bug_threshold(self):
        try:
            message = ''
            info_test = ''
            jira_connection_test = get_jira_connection()
            sheet_connection_test = get_testmap_connection()
            message, info_test = check_bug_threshold(sheet_connection_test, jira_connection_test, message, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_check_control_panel_tab(self):
        try:
            message = ''
            sheet_connection = get_testmap_connection()
            message = check_control_panel_tab(sheet_connection, message)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_check_need_automation_test_cases(self):
        try:
            message = ''
            info_test = ''
            jira_connection_test = get_jira_connection()
            sheet_connection_test = get_testmap_connection()
            team_components_test = get_team_components(jira_connection_test, 'LPS', 'Product Team Echo')
            message, info_test = check_need_automation_test_cases(sheet_connection_test, jira_connection,
                                                                  team_components_test, message, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_echo_update_test_map(self):
        try:
            info_test = ''
            jira_connection_test = get_jira_connection()
            sheet_connection_test = get_testmap_connection()
            info_test = update_echo_test_map(sheet_connection_test, jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()
