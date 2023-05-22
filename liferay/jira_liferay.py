from jira import JIRA

from jira_constants import Instance
from manageCredentialsCrypto import get_credentials


def get_jira_connection():
    login = get_credentials()
    try:
        if Instance.Type == "Cloud":
            jira = JIRA(Instance.Jira_URL, basic_auth=login)
        elif Instance.Type == "Server":
            jira = JIRA(Instance.Jira_URL, token_auth=login[1])
        else:
            raise Exception("Sorry, only Cloud and Server are valid values for Instance.Type")
    except Exception as err:
        raise Exception("Error accessing Jira instance. Please check .jira_user folder and jira_constants.py: "
                        "Error message\n" +
                        str(err))

    return jira
