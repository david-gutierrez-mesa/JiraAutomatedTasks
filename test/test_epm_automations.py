import unittest

from liferay.epm_automations import update_components_sheet
from liferay.jira_liferay import get_jira_connection


class EpmAutomationTests(unittest.TestCase):
    def test_update_components_sheet(self):
        try:
            jira_connection = get_jira_connection()
            update_components_sheet(jira_connection, "18k_C77ujQjpmy5ZW-TNCihmYXHGYAelRJ-_MJTqhvHs")
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()
