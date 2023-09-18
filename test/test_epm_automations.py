import unittest

from liferay.teams.epm.epm_automations import update_components_sheet
from liferay.utils.jira.jira_liferay import get_jira_connection


class EpmAutomationTests(unittest.TestCase):
    def test_update_components_sheet(self):
        jira_connection_test = get_jira_connection()
        try:
            update_components_sheet(jira_connection_test, "18k_C77ujQjpmy5ZW-TNCihmYXHGYAelRJ-_MJTqhvHs")
        except Exception:
            self.fail("Test failed unexpectedly!")
        finally:
            jira_connection_test.close()


if __name__ == '__main__':
    unittest.main()
