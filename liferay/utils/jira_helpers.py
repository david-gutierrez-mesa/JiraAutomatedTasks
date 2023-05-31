import json
import requests
from requests.auth import HTTPBasicAuth

from manageCredentialsCrypto import get_credentials


def set_filter_permissions(jira_connection, jira_url, filter_id, permission):
    url = jira_url + "/rest/api/2/filter/" + filter_id

    credentials = get_credentials()
    auth = HTTPBasicAuth(credentials[0], credentials[1])

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = ''
    request_type = ''

    permission_type = permission.type

    if permission.view:
        url += "/permission"
        if permission_type == 'group':
            payload = json.dumps({
                "groupname": permission.group.name,
                "rights": 1,
                "type": "group"
            })
        elif permission_type == 'project':
            payload = json.dumps({
                "projectId": permission.project.name,
                "rights": 1,
                "type": "project"
            })
            request_type = "POST"
    elif permission.edit:
        edit_permissions = ''
        if permission_type == 'group':
            group = json.dumps({
                "name": permission.group.name
            })
            edit_permissions = json.dumps({
                "group": group
            })
        elif permission_type == 'project':
            project_id = jira_connection.project(permission.project)
            project = json.dumps({
                "id": project_id
            })
            edit_permissions = json.dumps({
                "project": project
            })
        elif permission_type == 'user':
            account_id = jira_connection.search_users(user=permission.user)[0].id
            user = json.dumps({
                "accountId": account_id
            })
            edit_permissions = json.dumps({
                "user": user
            })
        payload = json.dumps({
            "editPermissions": edit_permissions
        })
        request_type = "PUT"

    response = requests.request(
        request_type,
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    print(response)
