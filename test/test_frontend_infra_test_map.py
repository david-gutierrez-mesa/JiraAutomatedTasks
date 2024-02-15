import unittest

from liferay.teams.frontend_infra.frontend_infra_test_map import *
from liferay_utils.jira_utils.jira_liferay import get_jira_connection
from liferay_utils.sheets.sheets_liferay import get_testmap_connection


class EchoTestMapTests(unittest.TestCase):

    def test_update_frontend_infra_test_map(self):
        info_test = ''
        jira_connection_test = get_jira_connection()
        sheet_connection_test = get_testmap_connection()
        try:
            info_test = update_frontend_infra_test_map(sheet_connection_test, jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")
        finally:
            jira_connection_test.close()

    def test_update_frontend_infra_bug_threshold(self):
        info_test = ''
        jira_connection_test = get_jira_connection()
        sheet_connection_test = get_testmap_connection()
        try:
            info_test = update_frontend_infra_bug_threshold(sheet_connection_test, jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")
        finally:
            jira_connection_test.close()


if __name__ == '__main__':
    unittest.main()
