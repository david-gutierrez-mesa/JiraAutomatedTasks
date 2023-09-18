from jira import JIRA

from liferay.utils.jira.jira_constants import Instance
from liferay.utils.manageCredentialsCrypto import get_credentials


def get_jira_connection(instance_url=Instance.Jira_URL, instance_type=Instance.Type):
    login = get_credentials()
    try:
        print("Connecting to Jira " + instance_type + " in URL " + instance_url + " with user " + login[0])
        if instance_type == "Cloud":
            jira = JIRA(instance_url, basic_auth=login)
        elif instance_type == "Server":
            jira = JIRA(instance_url, token_auth=login[1])
        else:
            raise Exception("Sorry, only Cloud and Server are valid values for Instance.Type")
        print("Connected to Jira")
    except Exception as err:
        raise Exception("Error accessing Jira instance. Please check .jira_user folder and jira_constants.py: "
                        "Error message\n" +
                        str(err))

    return jira
