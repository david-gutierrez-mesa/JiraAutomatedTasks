import json
import requests
from requests.auth import HTTPBasicAuth

from liferay.utils.jira.jira_constants import CustomField, Status, Instance, Transition, Strings, IssueTypes
from liferay.utils.manageCredentialsCrypto import get_credentials

AUTOMATION_TABLE_HEADER = '||Test Scenarios||Test Strategy||Kind of test||Is it covered by FrontEnd ? (' \
                          'JS-Unit)||Is it covered by BackEnd ? (unit or integration)||Could it be covered by ' \
                          'POSHI?||'
LIFERAY_JIRA_BROWSE_URL = Instance.Jira_URL + "/browse/"
LIFERAY_JIRA_ISSUES_URL = Instance.Jira_URL + "/issues/"


def __initialize_subtask(story, components, summary, issuetype, description=''):
    subtask_test_automation = {
        'project': {'key': 'LPS'},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issuetype},
        'parent': {'id': story.id}
    }
    if components:
        subtask_test_automation.update({'components': components})
    return subtask_test_automation


def __initialize_subtask_design_task(story, summary, description=''):
    return __initialize_subtask(story, [], summary, IssueTypes.Design_Task, description)


def __initialize_subtask_technical_test(story, components, summary, description=''):
    return __initialize_subtask(story, components, summary, IssueTypes.Technical_Testing, description)


def _parse_permission(permissions):
    parsed_permission = []
    for permission in permissions:
        current_permission = {
            "id": permission.id,
            "type": permission.type
        }
        parsed_permission.append(current_permission)
    return parsed_permission


def close_functional_automation_subtask(jira_local, story, poshi_task=''):
    for subtask in story.get_field('subtasks'):
        if subtask.fields.summary == 'Product QA | Functional Automation' or subtask.fields.summary == 'Automation ' \
                                                                                                       'Test Creation':
            testing_subtask = subtask.id
            if not subtask.fields.status.name == Status.Closed:
                jira_local.transition_issue(testing_subtask, transition=Transition.Closed,
                                            resolution={'name': 'Discarded'})
                if poshi_task:
                    jira_local.add_comment(testing_subtask, 'Closing. Poshi automation is going to be done in '
                                           + poshi_task)
                else:
                    jira_local.add_comment(testing_subtask, 'Closing. Poshi automation not needed')
            break


def create_poshi_automation_task_for(jira_local, issue, summary, description):
    new_issue = ''
    if not has_linked_task_with_summary(issue, summary):
        parent_key = issue.key
        epic_link = issue.get_field(CustomField.Epic_Link)
        components = []
        for component in issue.fields.components:
            components.append({'name': component.name})

        labels = []
        if hasattr(issue.fields, CustomField.Epic_Link):
            epic = jira_local.issue(epic_link, fields='labels')
            if hasattr(epic.fields, 'labels'):
                epic_labels = epic.get_field('labels')
                for label in epic_labels:
                    if label.startswith('202') and label.endswith('_DEV'):
                        labels.append(label)

        issue_dict = {
            'project': {'key': 'LPS'},
            'summary': summary,
            'description': description,
            'issuetype': {'name': IssueTypes.Testing},
            'components': components,
            CustomField.Epic_Link: epic_link
        }

        new_issue = jira_local.create_issue(fields=issue_dict)
        jira_local.create_issue_link(
            type="relates",
            inwardIssue=new_issue.key,
            outwardIssue=parent_key,
        )
    return new_issue


def get_all_issues(jira_local, jql_str, fields):
    issues = []
    i = 0
    chunk_size = 50
    while True:
        chunk = jira_local.search_issues(jql_str, startAt=i, maxResults=chunk_size, fields=fields)
        i += chunk_size
        issues += chunk.iterable
        if i >= chunk.total:
            break
    return issues


def create_poshi_automation_task_for_bug(jira_local, bug):
    parent_key = bug.key
    bug_summary = bug.fields.summary
    print("Creating automation task for bug", parent_key)
    summary = 'Poshi Automation for Bug ' + parent_key + ' ' + bug_summary

    description = 'We need to automate bug ' + parent_key + '\'' + bug_summary + '\' since it was a release blocker. ' \
                                                                                 'Feel free to create a new test or ' \
                                                                                 'add new steps to an existing one '
    new_issue = create_poshi_automation_task_for(jira_local, bug, summary, description)
    if new_issue:
        print("Poshi task with summary", summary, " already existed for", parent_key)
    else:
        print("Poshi task ", new_issue.key, " created for", parent_key)
    return new_issue


def get_property(local_case, property_name):
    test_property = 'TBD'
    label_start = local_case.lower().find(property_name.lower())
    string_start = label_start + len(property_name)
    if label_start != -1:
        string_end = local_case.find('\n', string_start)
        test_property = local_case[string_start:string_end].strip()
    return test_property


def get_team_components(jira, project, team_name_in_jira):
    components_full_info = jira.project_components(project)
    team_components = [x.name for x in components_full_info if is_component_lead(x, team_name_in_jira)]
    return team_components


def has_linked_task_with_summary(story, summary):
    if hasattr(story.fields, "issuelinks"):
        for link in story.fields.issuelinks:
            linked_issue_key = ""
            if hasattr(link, "inwardIssue"):
                linked_issue_key = link.inwardIssue
            elif hasattr(link, "outwardIssue"):
                linked_issue_key = link.outwardIssue
            if summary in linked_issue_key.fields.summary:
                return True
    return False


def html_issue_with_link(issue):
    return "<" + LIFERAY_JIRA_BROWSE_URL + issue.key + "|" + issue.key + ">"


def initialize_subtask_check_ux_pm_impedibug(story, components, impedibug):
    impedibug_id = '?'
    impedibug_summary = '?'
    if impedibug:
        impedibug_id = impedibug.key
        impedibug_summary = impedibug.fields.summary
    description = "h1. Bugs found:\n(/) - PASS\n(!) - To Do\n(x) - FAIL\nh2. " \
                  "Impeditive:\n||Ticket||Title||QA Status||\n|?|?|(!)|\n\nh2. Not " \
                  "impeditive:\n||Ticket||Title||QA Status||\n|?|?|(x)|\n\nh2. Assert fix: " \
                  "\n||Ticket||Title||QA Status||\n|" + impedibug_id + "|" + impedibug_summary + "|(!)|\n\nh2. " \
                                                                                                 "Note:\nPlease also " \
                                                                                                 "check if we should " \
                                                                                                 "update already " \
                                                                                                 "defined test cases "
    subtask_check_impedi = __initialize_subtask_technical_test(story, components,
                                                               Strings.subtask_check_ux_pm_impedibug_summary,
                                                               description)
    return subtask_check_impedi


def initialize_subtask_back_end(story, components):
    subtask_backend = __initialize_subtask_technical_test(story, components, Strings.subtask_backend_summary,
                                                          Strings.subtask_backend_description)
    return subtask_backend


def initialize_subtask_front_end(story, components):
    subtask_test_creation = __initialize_subtask_technical_test(story, components, Strings.subtask_frontend_summary,
                                                                Strings.subtask_frontend_description)
    return subtask_test_creation


def initialize_subtask_test_creation(story, components, description):
    subtask_test_creation = __initialize_subtask_technical_test(story, components,
                                                                Strings.subtask_test_creation_summary, description)
    return subtask_test_creation


def initialize_subtask_test_validation(story, components, description):
    subtask_test_validation = __initialize_subtask_technical_test(story, components, Strings.subtask_round_1_summary,
                                                                  description)
    return subtask_test_validation


def initialize_subtask_test_automation(story, components, description):
    subtask_test_automation = __initialize_subtask_technical_test(story, components,
                                                                  Strings.subtask_automation_test_creation_summary,
                                                                  description)
    return subtask_test_automation


def initialize_subtask_ux_validation(story):
    subtask_test_validation = __initialize_subtask_design_task(story, Strings.subtask_ux_summary)
    return subtask_test_validation


def is_component_lead(component, team_name_in_jira):
    if hasattr(component, "lead"):
        return component.lead.displayName == team_name_in_jira
    else:
        return False


def is_sub_task_closed(story, sub_task_title):
    for subtask in story.get_field('subtasks'):
        if subtask.fields.summary == sub_task_title:
            if subtask.fields.status == Status.Closed:
                return True
            else:
                break
    return False


def line_strip(line):
    line = line.replace(' \n', '\n')
    line = line.replace('\n\n', '\n')
    return line


def prepare_test_creation_subtask(story):
    test_creation = True
    for subtask in story.fields.subtasks:
        summary = subtask.fields.summary
        if summary == Strings.subtask_test_creation_summary:
            test_creation = False

    components = []
    for component in story.fields.components:
        components.append({'name': component.name})

    return test_creation, components


def prepare_test_validation_subtask(story):
    test_validation = True
    for subtask in story.fields.subtasks:
        summary = subtask.fields.summary
        if summary == Strings.subtask_round_1_summary:
            test_validation = False

    components = []
    for component in story.fields.components:
        components.append({'name': component.name})

    return test_validation, components


def read_test_cases_table_from_description(description):
    table_starring_string = ''
    if description.find('||*Test Scenarios*||') != -1:
        table_starring_string = '||*Test Scenarios*||'
    elif description.find('||Test Scenarios||') != -1:
        table_starring_string = '||Test Scenarios||'
    table_staring_position = description.find(table_starring_string)

    table_ending_string = ''
    if description.find('h3. Test Cases') != -1:
        table_ending_string = 'h3. Test Cases'
    elif description.find('h3. *Test Cases*') != -1:
        table_ending_string = 'h3. *Test Cases*'
    elif description.find('*Case ') != -1:
        table_ending_string = '*Case '
    table_ending_position = description.find(table_ending_string)

    if table_starring_string:
        if table_ending_position == -1:
            table_ending_position = len(description)
        table = description[table_staring_position:table_ending_position]
        table_rows = table.replace('|\n', '||\n').split('|\n')
        table_rows = [value for value in table_rows if value != '']
        table_rows = [value for value in table_rows if value != '\n']
        return table_rows[1:]
    else:
        return []


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
