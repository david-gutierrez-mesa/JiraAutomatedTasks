import unittest

from liferay.teams.echo.echo_bugs_dashboard import update_echo_bug_threshold, check_bug_threshold
from liferay.utils.jira.jira_liferay import get_jira_connection
from liferay.utils.sheets.sheets_liferay import get_testmap_connection


class EchoTestMapTests(unittest.TestCase):

    def test_check_bug_threshold(self):
        sheet_connection_test = get_testmap_connection()
        try:
            message = ''
            info_test = ''
            info_test, message = check_bug_threshold(sheet_connection_test, info_test, message)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_update_echo_bug_threshold(self):
        info_test = ''
        jira_connection_test = get_jira_connection()
        try:
            sheet_connection_test = get_testmap_connection()
            info_test = update_echo_bug_threshold(sheet_connection_test, jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")
        finally:
            jira_connection_test.close()


if __name__ == '__main__':
    unittest.main()
