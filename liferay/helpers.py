AUTOMATION_TABLE_HEADER = '||Test Scenarios||Test Strategy||Kind of test||Is it covered by FrontEnd ? (' \
                          'JS-Unit)||Is it covered by BackEnd ? (unit or integration)||Could it be covered by ' \
                          'POSHI?||'


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


def create_poshi_automation_task_for_bug(jira_local, bug):
    parent_key = bug.key
    bug_summary = bug.fields.summary
    print("Creating automation task for bug", parent_key)
    summary = 'Poshi Automation for Bug ' + parent_key + ' '+ bug_summary

    description = 'We need to automate bug ' + parent_key + '\'' + bug_summary + '\' since it was a release blocker. ' \
                  'Feel free to create a new test or add new steps to an existing one '
    new_issue = create_poshi_automation_task_for(jira_local, bug, summary, description)
    print("Poshi task ", new_issue.key, " created for bug", parent_key)
    return new_issue


def get_property(local_case, property_name):
    test_property = 'TBD'
    string_start = local_case.find(property_name) + len(property_name)
    if string_start != -1:
        string_end = local_case.find('\r\n', string_start)
        test_property = local_case[string_start:string_end].strip()
    return test_property


def initialize_subtask_back_end(story, components):
    subtask_backend = {
        'project': {'key': 'LPS'},
        'summary': 'Test Scenarios Coverage | Backend',
        'description': '* Fill the Backend coverage on the test scenarios table, created in the parent story.\n'
                       '* Implement the Backend unit and/or integration tests that are missing, '
                       'comparing with the test scenarios table, created in the parent story.',
        'issuetype': {'name': 'Technical Testing'},
        'components': components,
        'parent': {'id': story.id},
    }
    return subtask_backend


def initialize_subtask_front_end(story, components):
    subtask_frontend = {
        'project': {'key': 'LPS'},
        'summary': 'Test Scenarios Coverage | Frontend',
        'description': '* Fill the Frontend coverage on the test scenarios table, '
                       'created in the parent story.\n'
                       '* Implement the Frontend unit and/or integration tests that are missing, '
                       'comparing with the test scenarios table, created in the parent story.',
        'issuetype': {'name': 'Technical Testing'},
        'components': components,
        'parent': {'id': story.id},
    }
    return subtask_frontend


def initialize_subtask_test_creation(story, components):
    subtask_test_creation = {
        'project': {'key': 'LPS'},
        'summary': 'Test Scenarios Coverage | Test Creation',
        'description': 'Define the test scenarios of the parent epic. Instructions [here '
                       '|https://liferay.atlassian.net/l/c/Ed0yE1to].',
        'issuetype': {'name': 'Technical Testing'},
        'components': components,
        'parent': {'id': story.id},
    }
    return subtask_test_creation


def initialize_subtask_test_validation(story, components):
    subtask_test_validation = {
        'project': {'key': 'LPS'},
        'summary': 'Product QA | Test Validation - Round 1',
        'description': 'Execute the tests of the parent epic. Instructions ['
                       'here|https://liferay.atlassian.net/l/c/VURAf9A3].',
        'issuetype': {'name': 'Technical Testing'},
        'components': components,
        'parent': {'id': story.id},
    }
    return subtask_test_validation


def initialize_subtask_test_automation(story, components, description):
    subtask_test_automation = {
        'project': {'key': 'LPS'},
        'summary': 'Product QA | Automation Test Creation',
        'description': description,
        'issuetype': {'name': 'Technical Testing'},
        'components': components,
        'parent': {'id': story.id},
    }
    return subtask_test_automation
