AUTOMATION_TABLE_HEADER = '||Test Scenarios||Test Strategy||Kind of test||Is it covered by FrontEnd ? (' \
                          'JS-Unit)||Is it covered by BackEnd ? (unit or integration)||Could it be covered by ' \
                          'POSHI?||'


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
