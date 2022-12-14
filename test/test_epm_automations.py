import unittest

from epm_automations import update_components_sheet
from jira_liferay import get_jira_connection


class EpmAutomationTests(unittest.TestCase):
    def test_update_components_sheet(self):
        try:
            jira_connection = get_jira_connection()
            update_components_sheet(jira_connection)
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()
