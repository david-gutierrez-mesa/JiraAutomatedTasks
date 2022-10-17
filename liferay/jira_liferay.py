from jira import JIRA

from manageCredentialsCrypto import get_credentials


def get_jira_connection():
    login = get_credentials()
    jira = JIRA("https://issues.liferay.com", basic_auth=login)
    return jira
