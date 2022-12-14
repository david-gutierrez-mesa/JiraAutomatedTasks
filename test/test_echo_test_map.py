import unittest

from echo_test_map import add_test_cases_to_test_map, check_need_automation_test_cases
from jira_liferay import get_jira_connection
from testmap_jira import get_testmap_connection


class EchoTestMapTests(unittest.TestCase):
    def test_add_test_cases_to_test_map(self):
        try:
            message = ''
            info = ''
            jira_connection = get_jira_connection()
            sheet_connection = get_testmap_connection()
            message, info = add_test_cases_to_test_map(sheet_connection, jira_connection, message, info)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_check_need_automation_test_cases(self):
        try:
            message = ''
            info = ''
            jira_connection = get_jira_connection()
            sheet_connection = get_testmap_connection()
            message, info = check_need_automation_test_cases(sheet_connection, jira_connection, message, info)
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()