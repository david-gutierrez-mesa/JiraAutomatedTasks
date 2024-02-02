#!/usr/bin/env python
from liferay.teams.frontend_infra.frontend_infra_constants import FileName, Roles
from utils.liferay_utils.file_helpers import create_output_files
from utils.liferay_utils.jira.jira_helpers import *
from utils.liferay_utils.jira.jira_helpers import __initialize_subtask_technical_test
from utils.liferay_utils.jira.jira_constants import Filter
from utils.liferay_utils.jira.jira_liferay import get_jira_connection
from utils.liferay_utils.sheets.sheets_constants import SheetInstance


def create_test_creation_subtask(jira, output_info):
    stories_without_testing_subtask = jira.search_issues(Filter.FI_Stories_without_test_creation_subtask,
                                                         fields=['key', 'id', 'subtasks', 'components'])
    for story in stories_without_testing_subtask:
        output_info += "Creating test scenarios coverage sub-task for story " + story.key
        test_creation, components = prepare_test_creation_subtask(story)

        if test_creation:
            description = '*Output*' \
                          '\n # Our table with the Test scenarios/test cases to be validated in the ' \
                          'validation phase.' \
                          '\n # After being reviewed by the team, add a finalized table to the parent story ' \
                          'description' \
                          '\n # Add test cases to [Test ' \
                          'Map|' + SheetInstance.GOOGLE_SHEET_URL + \
                          '/edit#gid=2145200593]' \
                          '\n' \
                          '\n*Test Scenarios:*' \
                          '\n||Requirement||Test Case||Covered by unit/integration test? (Yes/No)||Test Priority (' \
                          'business impact)||' \
                          '\n| | | | |' \
                          '\n' \
                          '\n*Exploratory testing to consider:*' \
                          '\n||Requirement||Test Scenarios||Test Priority (business impact)||Covered by ' \
                          'frontend/backend Unit Test?||' \
                          '\n| | | | |'
            subtask_test_creation = initialize_subtask_test_creation(story, components, description)
            child = jira.create_issue(fields=subtask_test_creation)
            output_info += "   * sub-task created: " + child.key

    output_info += "✓ Test scenarios coverage subtasks are up to date \n"
    return output_info


def create_test_validation_subtask(jira, output_info):
    stories_without_testing_subtask = jira.search_issues(Filter.FI_Ready_for_Testing_Stories_without_Test_Validation,
                                                         fields=['key', 'id', 'subtasks', 'components'])
    for story in stories_without_testing_subtask:
        output_info += "Creating test validation sub-task for story " + story.key
        test_validation, components = prepare_test_validation_subtask(story)

        if test_validation:
            description = '\n*Context*' \
                          '\nExecute the tests of the parent story, and use the information in the*Test ' \
                          'Information*section to perform the tests.' \
                          '\n' \
                          '\n*Output*' \
                          '\nTell in one comment (in the story ticket) the final status of this first round, ' \
                          'and in this ticket, fill the bug section.' \
                          '\nRemember to link the bug (if you discover it) with the Story ticket.' \
                          '\n{code:java}' \
                          '\n*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{' \
                          'color:#59afe1}BLOCKED{color}* Manual Testing following the steps in the description.' \
                          '\n' \
                          '\n*Verified on:*' \
                          '\n*Environment*: localhost' \
                          '\n*Github*: https://github.com/liferay/liferay-portal.git' \
                          '\n*Branch*: master' \
                          '\n*Bundle*: Liferay DXP' \
                          '\n*Database*: MySQL 5.7.22' \
                          '\n*Last Commit*: ? ' \
                          '\n' \
                          '\n|| Test Scenarios || Test Result ||' \
                          '\n| |*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{' \
                          'color:#59afe1}BLOCKED{color}*|' \
                          '\n| |*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{' \
                          'color:#59afe1}BLOCKED{color}*|' \
                          '\n...' \
                          '\n{code}' \
                          '\n*Bugs:*' \
                          '\n (/)- PASS' \
                          '\n (!)- To Do' \
                          '\n (x)- FAIL' \
                          '\n * *Impeditive:*' \
                          '\n||Ticket||Title||' \
                          '\n|?|?|' \
                          '\n * *Not Impeditive:*' \
                          '\n||Ticket||Title||' \
                          '\n|?|?|'
            subtask_test_validation = initialize_subtask_test_validation(story, components, description)
            child = jira.create_issue(fields=subtask_test_validation)
            output_info += "   * sub-task created: " + child.key

    output_info += "✓ Manual Test Validation subtasks are up to date \n"
    return output_info


def create_technical_sub_task_test_scope_out_of_scope_creation(jira, output_info):
    issues_to_update = jira.search_issues(Filter.FI_Test_Scope_out_of_Scope_Creation_task_creation,
                                          fields=['key', 'components'])
    summary = "Test Scenarios Coverage | Test Scope/out of Scope Creation"
    description = ""
    output_info += "Creating \"Test Scope/out of Scope Creation\" sub tasks"
    for story in issues_to_update:
        components = []
        for component in story.fields.components:
            components.append({'name': component.name})
        subtask_fields = __initialize_subtask_technical_test(story, components, summary, description)
        child = jira.create_issue(fields=subtask_fields)
        output_info += "   * sub-task created " + child.key + " created for story " + story.key
        jira.assign_issue(child.id, Roles.QA_JIRA_USER)

    return output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    jira_connection = get_jira_connection()
    info = create_test_creation_subtask(jira_connection, info)
    info = create_test_validation_subtask(jira_connection, info)
    create_technical_sub_task_test_scope_out_of_scope_creation(jira_connection, info)
    jira_connection.close()

    create_output_files([warning, FileName.OUTPUT_MESSAGE_FILE_NAME], [info, FileName.OUTPUT_INFO_FILE_NAME])
