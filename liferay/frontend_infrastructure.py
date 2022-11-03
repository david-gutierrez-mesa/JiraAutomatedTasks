#!/usr/bin/env python
from helpers import initialize_subtask_test_creation, initialize_subtask_test_validation, \
    initialize_subtask_test_automation
from jira_liferay import get_jira_connection


def __initialize_subtask_test_automation_fi(story, components):
    description = 'Create test automation to validate the critical test scenarios/cases of the related story. ' \
                  'Instructions [here|https://liferay.atlassian.net/l/c/FUSUocqi]. '
    return initialize_subtask_test_automation(story, components, description)


def create_fi_testing_subtasks(jira):
    print("Creating subtasks for Frontend Infrastructure team...")
    stories_without_testing_subtask = jira.search_issues('filter=54596')
    for story in stories_without_testing_subtask:
        print("Creating sub-tasks for story " + story.key)
        test_creation = True
        test_validation = True
        automation_test_creation = True
        for subtask in story.fields.subtasks:
            summary = subtask.fields.summary
            if summary == 'Test Scenarios Coverage | Test Creation':
                test_creation = False
            elif summary == 'Product QA | Test Validation - Round 1':
                test_validation = False
            elif summary == 'Product QA | Automation Test Creation':
                automation_test_creation = False

        components = []
        for component in story.fields.components:
            components.append({'name': component.name})

        if test_creation:
            description = 'Define the test scenarios of the parent epic. Instructions [here ' \
                          '|https://liferay.atlassian.net/l/c/Ed0yE1to].'
            subtask_test_creation = initialize_subtask_test_creation(story, components, description)
            child = jira.create_issue(fields=subtask_test_creation)
            print("* Created sub-task: " + child.key)

        if test_validation:
            description = 'Execute the tests of the parent epic. Instructions ['\
                          'here|https://liferay.atlassian.net/l/c/VURAf9A3].'
            subtask_test_validation = initialize_subtask_test_validation(story, components, description)
            child = jira.create_issue(fields=subtask_test_validation)
            print("* Created sub-task: " + child.key)

        if automation_test_creation:
            subtask_test_automation = __initialize_subtask_test_automation_fi(story, components)
            child = jira.create_issue(fields=subtask_test_automation)
            print("* Created sub-task: " + child.key)

    print("Subtasks for Frontend Infrastructure team are up to date")


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    create_fi_testing_subtasks(jira_connection)