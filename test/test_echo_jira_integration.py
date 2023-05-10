import unittest

from liferay.echo import *
from liferay.jira_liferay import get_jira_connection


class EchoJiraTestCase(unittest.TestCase):

    def test_assign_qa_engineer(self):
        jira_connection_test = get_jira_connection()
        try:
            assign_qa_engineer(jira_connection_test, '')
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_create_poshi_automation_task(self):
        jira_connection_test = get_jira_connection()
        try:
            create_poshi_automation_task(jira_connection_test, '', '')
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_create_poshi_automation_task_for_bugs(self):
        jira_connection_test = get_jira_connection()
        try:
            create_poshi_automation_task_for_bugs(jira_connection_test, '')
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_create_testing_table_for_stories(self):
        jira_connection_test = get_jira_connection()
        try:
            create_testing_table_for_stories(jira_connection_test, '')
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_fill_round_technical_testing_description(self):
        jira_connection_test = get_jira_connection()
        try:
            fill_round_technical_testing_description(jira_connection_test, '')
        except Exception:
            self.fail("Test failed unexpectedly!")

    def test_transition_story_to_ready_for_pm_review(self):
        jira_connection_test = get_jira_connection()
        try:
            transition_story_to_ready_for_pm_review(jira_connection_test, '', '')
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()
