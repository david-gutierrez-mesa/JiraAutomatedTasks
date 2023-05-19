#!/usr/bin/env python
from helpers import create_output_files
from helpers_jira import *
from helpers_jira import __initialize_subtask_technical_test
from jira_constants import Filter
from jira_liferay import get_jira_connection

QA_JIRA_USER = 'carlos.brichete'
OUTPUT_MESSAGE_FILE_NAME = "output_message.txt"
OUTPUT_INFO_FILE_NAME = "output_info.txt"


def create_test_creation_subtask(jira, output_info):
    stories_without_testing_subtask = jira.search_issues(Filter.FI_Stories_without_test_creation_subtask)
    for story in stories_without_testing_subtask:
        output_info += "Creating test scenarios coverage sub-task for story " + story.key
        test_creation, components = prepare_test_creation_subtask(story)

        if test_creation:
            description = '*Output*' \
                          '\r\n # Our table with the Test scenarios/test cases to be validated in the ' \
                          'validation phase.' \
                          '\r\n # After being reviewed by the team, add a finalized table to the parent story ' \
                          'description' \
                          '\r\n # Add test cases to [Test ' \
                          'Map|https://docs.google.com/spreadsheets/d/1_liLRC1XHBydH_mfeeDifgKxBWN3kfRtX7uqbKgJ72k' \
                          '/edit#gid=2145200593]' \
                          '\r\n' \
                          '\r\n*Test Scenarios:*' \
                          '\r\n||Requirement||Test Case||Covered by unit/integration test? (Yes/No)||Test Priority (' \
                          'business impact)||' \
                          '\r\n| | | | |' \
                          '\r\n' \
                          '\r\n*Exploratory testing to consider:*' \
                          '\r\n||Requirement||Test Scenarios||Test Priority (business impact)||Covered by ' \
                          'frontend/backend Unit Test?||' \
                          '\r\n| | | | |'
            subtask_test_creation = initialize_subtask_test_creation(story, components, description)
            child = jira.create_issue(fields=subtask_test_creation)
            output_info += "   * sub-task created: " + child.key

    output_info += "✓ Test scenarios coverage subtasks are up to date \n"
    return output_info


def create_test_validation_subtask(jira, output_info):
    stories_without_testing_subtask = jira.search_issues(Filter.FI_Ready_for_Testing_Stories_without_Test_Validation)
    for story in stories_without_testing_subtask:
        output_info += "Creating test validation sub-task for story " + story.key
        test_validation, components = prepare_test_validation_subtask(story)

        if test_validation:
            description = '\r\n*Context*' \
                          '\r\nExecute the tests of the parent story, and use the information in the*Test ' \
                          'Information*section to perform the tests.' \
                          '\r\n' \
                          '\r\n*Output*' \
                          '\r\nTell in one comment (in the story ticket) the final status of this first round, ' \
                          'and in this ticket, fill the bug section.' \
                          '\r\nRemember to link the bug (if you discover it) with the Story ticket.' \
                          '\r\n{code:java}' \
                          '\r\n*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{' \
                          'color:#59afe1}BLOCKED{color}* Manual Testing following the steps in the description.' \
                          '\r\n' \
                          '\r\n*Verified on:*' \
                          '\r\n*Environment*: localhost' \
                          '\r\n*Github*: https://github.com/liferay/liferay-portal.git' \
                          '\r\n*Branch*: master' \
                          '\r\n*Bundle*: Liferay DXP' \
                          '\r\n*Database*: MySQL 5.7.22' \
                          '\r\n*Last Commit*: ? ' \
                          '\r\n' \
                          '\r\n|| Test Scenarios || Test Result ||' \
                          '\r\n| |*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{' \
                          'color:#59afe1}BLOCKED{color}*|' \
                          '\r\n| |*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{' \
                          'color:#59afe1}BLOCKED{color}*|' \
                          '\r\n...' \
                          '\r\n{code}' \
                          '\r\n*Bugs:*' \
                          '\r\n (/)- PASS' \
                          '\r\n (!)- To Do' \
                          '\r\n (x)- FAIL' \
                          '\r\n * *Impeditive:*' \
                          '\r\n||Ticket||Title||' \
                          '\r\n|?|?|' \
                          '\r\n * *Not Impeditive:*' \
                          '\r\n||Ticket||Title||' \
                          '\r\n|?|?|'
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
        jira.assign_issue(child.id, QA_JIRA_USER)

    return output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    jira_connection = get_jira_connection()
    info = create_test_creation_subtask(jira_connection, info)
    info = create_test_validation_subtask(jira_connection, info)
    create_technical_sub_task_test_scope_out_of_scope_creation(jira_connection, info)

    create_output_files([warning, OUTPUT_MESSAGE_FILE_NAME], [info, OUTPUT_INFO_FILE_NAME])
