import unittest

from liferay.teams.frontend_infra.frontend_infrastructure import *
from utils.liferay_utils.jira.jira_liferay import get_jira_connection


class EchoTestMapTests(unittest.TestCase):

    def test_create_technical_sub_task_test_scope_out_of_scope_creation(self):
        info_test = ''
        jira_connection_test = get_jira_connection()
        try:
            info_test = create_technical_sub_task_test_scope_out_of_scope_creation(jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")
        finally:
            jira_connection_test.close()


if __name__ == '__main__':
    unittest.main()
