#!/usr/bin/env python
from liferay.teams.headless.headless_contstants import Strings
from liferay.utils.jira.jira_constants import Filter
from liferay.utils.jira.jira_constants import Status
from liferay.utils.jira.jira_helpers import create_poshi_automation_task_for, close_functional_automation_subtask
from liferay.utils.jira.jira_liferay import get_jira_connection


def _create_poshi_task_for(jira_local, parent_story, poshi_automation_table):
    parent_key = parent_story.key
    parent_summary = parent_story.get_field('summary')
    print("Creating poshi automation task for story", parent_key)
    summary = 'Product QA | Functional Automation - ' + parent_key + ' - ' + parent_summary

    description = Strings.poshi_task_description + poshi_automation_table
    new_issue = create_poshi_automation_task_for(jira_local, parent_story, summary, description)

    print("Poshi task ", new_issue.key, " created for", parent_key)
    return new_issue


def update_creation_subtask(jira):
    print("Updating test creation subtasks for Headless team...")
    stories_with_test_creation_subtask = \
        jira.search_issues(Filter.Integration_In_Development_Sub_task_creation_Headless_team)
    for story in stories_with_test_creation_subtask:
        for subtask in story.fields.subtasks:
            summary = subtask.fields.summary
            key = subtask.key
            assignee = jira.issue(key, fields='assignee')
            if summary == 'Test Scenarios Coverage | Test Creation':
                print("Updating "+key+" ...")
                if subtask.fields.status.name == Status.Open:
                    description = Strings.test_creation_description
                    subtask.update(fields={'description': description})
                    if assignee != 'Support QA':
                        jira.assign_issue(subtask.id, 'support-qa')
                    break
    print("Subtasks Test Creation for Headless team are up to date")


def update_validation_subtask(jira):
    print("Updating test validation subtasks for Headless team...")
    stories_with_test_validation_subtask = jira.search_issues(Filter.Product_QA_Test_Validation_Round_1)
    for story in stories_with_test_validation_subtask:
        for subtask in story.fields.subtasks:
            summary = subtask.fields.summary
            key = subtask.key
            assignee = jira.issue(key, fields='assignee')
            if 'Product QA | Test Validation' in summary:
                if subtask.fields.status.name == Status.Open:
                    print("Updating "+key+" ...")
                    description = Strings.test_validation_round_1_description
                    subtask.update(fields={'description': description})
                    if assignee != 'Support QA':
                        jira.assign_issue(subtask.id, 'support-qa')
                    break
    print("Validation subtasks for Headless team are up to date")


def create_poshi_automation_task(jira):
    print("Creating Poshi tasks...")
    output_message = ''
    stories_without_poshi_automation_created = \
        jira.search_issues(Filter.Headless_Team_Ready_to_create_POSHI_Automation_Task)
    for story in stories_without_poshi_automation_created:
        for subtask in story.get_field('subtasks'):
            if subtask.fields.summary == 'Test Scenarios Coverage | Test Creation':
                description = jira.issue(subtask.id, fields='description').fields.description
                table_starring_string = ''
                if description.find('||*Requirement*||') != -1:
                    table_starring_string = '||*Requirement*||'
                elif description.find('||Requirement||') != -1:
                    table_starring_string = '||Requirement||'
                table_staring_position = description.find(table_starring_string)
                table_ending_string = ''
                if description.find('*Exploratory') != -1:
                    table_ending_string = '*Exploratory'
                elif description.find('Exploratory') != -1:
                    table_ending_string = 'Exploratory'
                table_ending_position = description.find(table_ending_string)
                poshi_automation_table = description[table_staring_position:table_ending_position - 1]
                poshi_task = _create_poshi_task_for(jira, story, poshi_automation_table)
                close_functional_automation_subtask(jira, story, poshi_task.key)
                output_message = output_message + "Functional Automation created for " + story.get_field('summary')
    print(output_message)


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    update_creation_subtask(jira_connection)
    update_validation_subtask(jira_connection)
    create_poshi_automation_task(jira_connection)
