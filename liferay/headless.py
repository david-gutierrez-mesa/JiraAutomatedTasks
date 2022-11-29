#!/usr/bin/env python
from helpers_jira import initialize_subtask_test_creation, initialize_subtask_test_validation, \
    prepare_test_creation_subtask, prepare_test_validation_subtask, create_poshi_automation_task_for
from jira_liferay import get_jira_connection


def __create_poshi_task_for(jira_local, parent_story, poshi_automation_table):
    parent_key = parent_story.key
    parent_summary = parent_story.get_field('summary')
    print("Creating poshi automation task for story", parent_key)
    summary = 'Product QA | Automation Test Creation - ' + parent_key + ' - ' + parent_summary

    description = 'Create test automation to validate the critical test scenarios/cases of the related story.\n\nThe ' \
                  'focus of this task is to implement the CRITICAL, HIGH, and MID tests of the related story, ' \
                  'but if you believe that can and have time to implement the LOW and TRIVIAL test cases, please, ' \
                  'create one more subtask to it, and go ahead!\n\nh3. Test Scenarios\n' + poshi_automation_table
    new_issue = create_poshi_automation_task_for(jira_local, parent_story, summary, description)

    print("Poshi task ", new_issue.key, " created for", parent_key)


def create_creation_subtask(jira):
    print("Creating test creation subtasks for Headless team...")
    stories_without_testing_subtask = jira.search_issues('filter=54996')
    for story in stories_without_testing_subtask:
        print("Creating sub-tasks for story " + story.key)
        test_creation, components = prepare_test_creation_subtask(story)

        if test_creation:
            description = '*Output*' \
                          '\r\n # Our table with the Test scenarios/test cases to be validated in the ' \
                          'validation phase.' \
                          '\r\n # After being reviewed by the team, add a finalized table to the parent story ' \
                          'description' \
                          '\r\n # Add test cases to [Test ' \
                          'Map|https://docs.google.com/spreadsheets/d/19KSqxtKJQ5FHZbHKxDS3_TzptWeD0DrL-mLk0y0WFYY' \
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
            print("* Created sub-task: " + child.key)

    print("Subtasks for Headless team are up to date")


def create_validation_subtask(jira):
    print("Creating test validation subtasks for Headless team...")
    stories_without_testing_subtask = jira.search_issues('filter=54997')
    for story in stories_without_testing_subtask:
        print("Creating sub-tasks for story " + story.key)
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
            print("* Created sub-task: " + child.key)

    print("Subtasks for Headless team are up to date")


def create_poshi_automation_task(jira):
    print("Creating Poshi tasks...")
    output_message = ''
    stories_without_poshi_automation_created = jira.search_issues('filter=54999')
    for story in stories_without_poshi_automation_created:
        for subtask in story.get_field('subtasks'):
            if subtask.fields.summary == 'Test Scenarios Coverage | Test Creation':
                description = jira.issue(subtask.id, fields='description').fields.description
                table_starring_string = '||Requirement||'
                table_staring_position = description.find(table_starring_string)
                table_ending_string = '*Exploratory'
                table_ending_position = description.find(table_ending_string)
                poshi_automation_table = description[table_staring_position:table_ending_position - 1]
                __create_poshi_task_for(jira, story, poshi_automation_table)
                output_message = output_message + "Automation Test Creation created for " + story.get_field('summary')
    print(output_message)


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    create_creation_subtask(jira_connection)
    create_validation_subtask(jira_connection)
    create_poshi_automation_task(jira_connection)
