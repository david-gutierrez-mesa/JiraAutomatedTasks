import unittest

from liferay.teams.echo.echo_bugs_dashboard import check_bug_threshold
from liferay.teams.echo.echo_test_map import *
from utils.liferay_utils.jira.jira_helpers import get_team_components
from utils.liferay_utils.jira.jira_liferay import get_jira_connection
from utils.liferay_utils.sheets.sheets_liferay import get_testmap_connection


class EchoTestMapTests(unittest.TestCase):
    def test_add_test_cases_to_test_map(self):
        message = ''
        info_test = ''
        jira_connection_test = get_jira_connection()
        sheet_connection_test = get_testmap_connection()
        try:
            team_components_test = get_team_components(jira_connection_test, 'LPS', 'Product Team Echo')
            message, info_test = add_test_cases_to_test_map(sheet_connection_test, jira_connection_test,
                                                            team_components_test,
                                                            message, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")
        finally:
            jira_connection_test.close()

    def test_check_bug_threshold(self):
        message = ''
        info_test = ''
        sheet_connection_test = get_testmap_connection()
        try:
            message, info_test = check_bug_threshold(sheet_connection_test, message, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_check_control_panel_tab(self):
        message = ''
        sheet_connection_test = get_testmap_connection()
        try:
            message = check_control_panel_tab(sheet_connection_test, message)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_check_need_automation_test_cases(self):
        message = ''
        info_test = ''
        jira_connection_test = get_jira_connection()
        sheet_connection_test = get_testmap_connection()
        try:
            team_components_test = get_team_components(jira_connection_test, 'LPS', 'Product Team Echo')
            message, info_test = check_need_automation_test_cases(sheet_connection_test, jira_connection_test,
                                                                  team_components_test, message, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")
        finally:
            jira_connection_test.close()

    def test_echo_update_test_map(self):
        info_test = ''
        jira_connection_test = get_jira_connection()
        sheet_connection_test = get_testmap_connection()
        try:
            info_test = update_echo_test_map(sheet_connection_test, jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")
        finally:
            jira_connection_test.close()


if __name__ == '__main__':
    unittest.main()
