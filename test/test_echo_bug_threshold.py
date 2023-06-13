import unittest

from liferay.echo_team.echo_bug_threshold import update_echo_bug_threshold
from liferay.jira_liferay import get_jira_connection
from liferay.testmap_jira import get_testmap_connection


class EchoTestMapTests(unittest.TestCase):

    def test_update_echo_bug_threshold(self):
        try:
            info_test = ''
            jira_connection_test = get_jira_connection()
            sheet_connection_test = get_testmap_connection()
            info_test = update_echo_bug_threshold(sheet_connection_test, jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()
