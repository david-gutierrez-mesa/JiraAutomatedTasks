AUTOMATION_TABLE_HEADER = '||Test Scenarios||Test Strategy||Kind of test||Is it covered by FrontEnd ? (' \
                          'JS-Unit)||Is it covered by BackEnd ? (unit or integration)||Could it be covered by ' \
                          'POSHI?||'
LIFERAY_JIRA_URL = "https://issues.liferay.com/"
LIFERAY_JIRA_BROWSE_URL = LIFERAY_JIRA_URL + "browse/"
LIFERAY_JIRA_ISSUES_URL = LIFERAY_JIRA_URL + "issues/"


def __initialize_subtask_technical_test(story, components, summary, description):
    subtask_test_automation = {
        'project': {'key': 'LPS'},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Technical Testing'},
        'components': components,
        'parent': {'id': story.id},
    }
    return subtask_test_automation


def close_functional_automation_subtask(jira_local, story, poshi_task=''):
    for subtask in story.get_field('subtasks'):
        if subtask.fields.summary == 'Product QA | Functional Automation' or subtask.fields.summary == 'Automation ' \
                                                                                                       'Test Creation':
            testing_subtask = subtask.id
            jira_local.transition_issue(testing_subtask, transition='Closed')
            if poshi_task:
                jira_local.add_comment(testing_subtask, 'Closing. Poshi automation is going to be done in '
                                       + poshi_task)
            else:
                jira_local.add_comment(testing_subtask, 'Closing. Poshi automation not needed')
            break


def create_poshi_automation_task_for(jira_local, issue, summary, description):
    parent_key = issue.key
    epic_link = issue.get_field('customfield_12821')
    components = []
    for component in issue.fields.components:
        components.append({'name': component.name})
    issue_dict = {
        'project': {'key': 'LPS'},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Testing'},
        'components': components,
        'customfield_12821': epic_link
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
    print("Poshi task ", new_issue.key, " created for bug", parent_key)
    return new_issue


def get_property(local_case, property_name):
    local_case = local_case.replace(' \r\n', '\r\n')
    test_property = 'TBD'
    string_start = local_case.find(property_name) + len(property_name)
    if string_start != -1:
        string_end = local_case.find('\r\n', string_start)
        test_property = local_case[string_start:string_end].strip()
    return test_property


def get_team_components(jira, project, team_name_in_jira):
    components_full_info = jira.project_components(project)
    team_components = [x.name for x in components_full_info if is_component_lead(x, team_name_in_jira)]
    return team_components


def initialize_subtask_back_end(story, components):
    summary = 'Test Scenarios Coverage | Backend'
    description = '* Fill the Backend coverage on the test scenarios table, created in the parent story.\n' \
                  '* Implement the Backend unit and/or integration tests that are missing, comparing with the test ' \
                  'scenarios table, created in the parent story. '
    subtask_backend = __initialize_subtask_technical_test(story, components, summary, description)
    return subtask_backend


def initialize_subtask_front_end(story, components):
    summary = 'Test Scenarios Coverage | Frontend'
    description = '* Fill the Frontend coverage on the test scenarios table, created in the parent story.\n' \
                  '* Implement the Frontend unit and/or integration tests that are missing, comparing with the test ' \
                  'scenarios table, created in the parent story. '
    subtask_test_creation = __initialize_subtask_technical_test(story, components, summary, description)
    return subtask_test_creation


def initialize_subtask_test_creation(story, components, description):
    summary = 'Test Scenarios Coverage | Test Creation'
    subtask_test_creation = __initialize_subtask_technical_test(story, components, summary, description)
    return subtask_test_creation


def initialize_subtask_test_validation(story, components, description):
    summary = 'Product QA | Test Validation - Round 1'
    subtask_test_validation = __initialize_subtask_technical_test(story, components, summary, description)
    return subtask_test_validation


def initialize_subtask_test_automation(story, components, description):
    summary = 'Product QA | Automation Test Creation'
    subtask_test_automation = __initialize_subtask_technical_test(story, components, summary, description)
    return subtask_test_automation


def is_component_lead(component, team_name_in_jira):
    if hasattr(component, "lead"):
        return component.lead.displayName == team_name_in_jira
    else:
        return False


def prepare_test_creation_subtask(story):
    test_creation = True
    for subtask in story.fields.subtasks:
        summary = subtask.fields.summary
        if summary == 'Test Scenarios Coverage | Test Creation':
            test_creation = False

    components = []
    for component in story.fields.components:
        components.append({'name': component.name})

    return test_creation, components


def prepare_test_validation_subtask(story):
    test_validation = True
    for subtask in story.fields.subtasks:
        summary = subtask.fields.summary
        if summary == 'Product QA | Test Validation - Round 1':
            test_validation = False

    components = []
    for component in story.fields.components:
        components.append({'name': component.name})

    return test_validation, components


def read_test_cases_table_from_description(description):
    table_starring_string = '||Test Scenarios||'
    table_ending_string = 'h3. Test Cases'
    table_alternative_ending_string = '*Case '
    table_staring_position = description.find(table_starring_string)
    table_ending_position = description.find(table_ending_string)
    if table_staring_position != -1:
        if table_ending_position == -1:
            table_ending_position = description.find(table_alternative_ending_string)
        table = description[table_staring_position:table_ending_position]
        table_rows = table.split('\r\n')
        table_rows = [value for value in table_rows if value != '']
        return table_rows[1:]
    else:
        return []
