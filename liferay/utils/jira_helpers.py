import json
import requests
from requests.auth import HTTPBasicAuth

from manageCredentialsCrypto import get_credentials


def set_filter_permissions(jira_connection, jira_url, new_filter, permission):
    filter_id = new_filter.id
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

    if permission.edit:

        if permission_type == 'group':
            payload = json.dumps({
                "editPermissions": [
                    {
                        "type": "group",
                        "group":
                            {
                                "name": permission.group.name
                            }
                    }
                ],
                "id": filter_id,
                "name": new_filter.name
            })
        elif permission_type == 'project':
            project_id = jira_connection.project(permission.project)
            payload = json.dumps({
                "editPermissions": [
                    {
                        "type": "project",
                        "project":
                            {
                                "id": project_id
                            }
                    }
                ],
                "id": filter_id,
                "name": new_filter.name
            })
        elif permission_type == 'user':
            account_id = jira_connection.search_users(query=permission.user.key)[0].accountId
            payload = json.dumps({
                "editPermissions": [
                    {
                        "type": "user",
                        "user":
                            {
                                "accountId": account_id
                            }
                    }
                ],
                "id": filter_id,
                "name": new_filter.name
            })
        request_type = "PUT"
    elif permission.view:
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

    response = requests.request(
        request_type,
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    print(response)
