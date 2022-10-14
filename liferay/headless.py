#!/usr/bin/env python
from liferay.helpers import initialize_subtask_test_creation, initialize_subtask_test_validation, \
    initialize_subtask_test_automation
from liferay.jira_liferay import get_jira_connection


def create_headless_testing_subtasks():
    print("Creating subtasks for Headless team...")
    jira = get_jira_connection()
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
            subtask_test_creation = initialize_subtask_test_creation(story, components)
            child = jira.create_issue(fields=subtask_test_creation)
            print("* Created sub-task: " + child.key)

        if test_validation:
            subtask_test_validation = initialize_subtask_test_validation(story, components)
            child = jira.create_issue(fields=subtask_test_validation)
            print("* Created sub-task: " + child.key)

        if automation_test_creation:
            subtask_test_automation = initialize_subtask_test_automation(story, components)
            child = jira.create_issue(fields=subtask_test_automation)
            print("* Created sub-task: " + child.key)

    print("Subtasks for Headless team are up to date")


if __name__ == "__main__":
    create_headless_testing_subtasks()
