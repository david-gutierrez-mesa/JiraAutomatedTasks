from jira import JIRA

from manage_credentials import manageCredentialsCrypto


def get_jira_connection():
    login = manageCredentialsCrypto.get_credentials()
    jira = JIRA("https://issues.liferay.com", basic_auth=login)
    return jira
