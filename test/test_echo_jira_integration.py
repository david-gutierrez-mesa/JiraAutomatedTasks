import unittest

from liferay.echo import create_poshi_automation_task
from liferay.jira_liferay import get_jira_connection


class EchoJiraTestCase(unittest.TestCase):
    def test_create_poshi_automation_task(self):
        jira_connection = get_jira_connection()
        try:
            create_poshi_automation_task(jira_connection)
        except Exception:
            self.fail("myFunc() raised ExceptionType unexpectedly!")


if __name__ == '__main__':
    unittest.main()
