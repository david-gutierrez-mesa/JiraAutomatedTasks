import unittest

from liferay.frontend_infrastructure import *
from liferay.jira_liferay import get_jira_connection


class EchoTestMapTests(unittest.TestCase):

    def test_create_technical_sub_task_test_scope_out_of_scope_creation(self):
        try:
            info_test = ''
            jira_connection_test = get_jira_connection()
            info_test = create_technical_sub_task_test_scope_out_of_scope_creation(jira_connection_test, info_test)
        except Exception:
            self.fail("Test failed unexpectedly!")


if __name__ == '__main__':
    unittest.main()
