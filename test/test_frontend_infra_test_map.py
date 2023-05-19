import unittest

from frontend_infra_test_map import *
from jira_liferay import get_jira_connection
from testmap_jira import get_testmap_connection


class EchoTestMapTests(unittest.TestCase):

    def test_update_frontend_infra_test_map(self):
        try:
            info_test = ''
            jira_connection_test = get_jira_connection()
            sheet_connection_test = get_testmap_connection()
            info_test = update_frontend_infra_test_map(sheet_connection_test, jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_update_frontend_infra_bug_threshold(self):
        try:
            info_test = ''
            jira_connection_test = get_jira_connection()
            sheet_connection_test = get_testmap_connection()
            info_test = update_frontend_infra_bug_threshold(sheet_connection_test, jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()
