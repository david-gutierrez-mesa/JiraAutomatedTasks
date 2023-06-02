import json
import requests
from requests.auth import HTTPBasicAuth

from manageCredentialsCrypto import get_credentials


def _parse_permission(permissions):
    parsed_permission = []
    for permission in permissions:
        current_permission = {
            "id": permission.id,
            "type": permission.type
        }
        parsed_permission.append(current_permission)
    return parsed_permission


def set_filter_permissions(jira_connection, jira_url, new_filter, permissions, error_message=''):
    filter_id = new_filter.id
    url = jira_url + "/rest/api/2/filter/" + filter_id

    credentials = get_credentials()
    auth = HTTPBasicAuth(credentials[0], credentials[1])

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    for permission in permissions:
        current_filter = jira_connection.filter(filter_id)
        edit_permissions = _parse_permission(current_filter.editPermissions)
        share_permissions = _parse_permission(current_filter.sharePermissions)
        permission_type = permission.type
        current_permission = dict()

        if permission_type == 'group':
            current_permission = {
                "type": "group",
                "group":
                    {
                        "name": permission.group.name
                    }
            }
        elif permission_type == 'project':
            project_id = jira_connection.project(permission.project).id
            current_permission = {
                "type": "project",
                "project":
                    {
                        "id": project_id
                    }
            }
        elif permission_type == 'user':
            list_of_users = jira_connection.search_users(query=permission.user.key)
            if list_of_users:
                account_id = list_of_users[0].accountId
            else:
                error_message += '  User does not exist: ' + permission.user.displayName
                continue
            current_permission = {
                "type": "user",
                "user":
                    {
                        "accountId": account_id
                    }
            }
        elif permission_type == 'loggedin':
            current_permission = {
                "type": "authenticated"
            }

        if permission.edit:
            edit_permissions.append(current_permission)
        elif permission.view:
            share_permissions.append(current_permission)

        payload = json.dumps({
            "editPermissions": edit_permissions,
            "id": filter_id,
            "name": new_filter.name,
            "sharePermissions": share_permissions
        })
        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )

        if not response.ok:
            error_message += '  Permission no created: ' + response.text

    return error_message
