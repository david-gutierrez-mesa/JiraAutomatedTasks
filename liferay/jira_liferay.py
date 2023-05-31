from jira import JIRA

from jira_constants import Instance
from manageCredentialsCrypto import get_credentials


def get_jira_connection(instance_url=Instance.Jira_URL, instance_type=Instance.Type):
    login = get_credentials()
    try:
        if instance_type == "Cloud":
            jira = JIRA(instance_url, basic_auth=login)
        elif instance_type == "Server":
            jira = JIRA(instance_url, token_auth=login[1])
        else:
            raise Exception("Sorry, only Cloud and Server are valid values for Instance.Type")
    except Exception as err:
        raise Exception("Error accessing Jira instance. Please check .jira_user folder and jira_constants.py: "
                        "Error message\n" +
                        str(err))

    return jira
