import unittest

from liferay.echo import create_poshi_automation_task, transition_story_to_ready_for_pm_review, \
    create_poshi_automation_task_for_bugs
from liferay.jira_liferay import get_jira_connection


class EchoJiraTestCase(unittest.TestCase):
    def test_create_poshi_automation_task(self):
        jira_connection = get_jira_connection()
        try:
            create_poshi_automation_task(jira_connection)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_create_poshi_automation_task_for_bugs(self):
        jira_connection = get_jira_connection()
        try:
            create_poshi_automation_task_for_bugs(jira_connection)
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_transition_story_to_ready_for_pm_review(self):
        jira_connection = get_jira_connection()
        try:
            transition_story_to_ready_for_pm_review(jira_connection)
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()
