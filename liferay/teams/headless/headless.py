#!/usr/bin/env python
from liferay.utils.jira.helpers_jira import create_poshi_automation_task_for, close_functional_automation_subtask
from liferay.utils.jira.jira_constants import Status, Filter
from liferay.utils.jira.jira_liferay import get_jira_connection


def _create_poshi_task_for(jira_local, parent_story, poshi_automation_table):
    parent_key = parent_story.key
    parent_summary = parent_story.get_field('summary')
    print("Creating poshi automation task for story", parent_key)
    summary = 'Product QA | Functional Automation - ' + parent_key + ' - ' + parent_summary

    description = 'Create test automation to validate the critical test scenarios/cases of the related story.\n\nThe ' \
                  'focus of this task is to implement the CRITICAL, HIGH, and MID tests of the related story, ' \
                  'but if you believe that can and have time to implement the LOW and TRIVIAL test cases, please, ' \
                  'create one more subtask to it, and go ahead!\n\nh3. Test Scenarios\n' + poshi_automation_table
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
                    description = '*Output*\r\n' \
                                  ' # Our table with the Test scenarios/test cases to be validated in the \r\n' \
                                  'validation phase.\r\n' \
                                  ' # After being reviewed by the team, add a finalized table ' \
                                  'to the parent story \r\n' \
                                  'description\r\n' \
                                  ' # Add test cases to [Test ' \
                                  'Map|https://docs.google.com/spreadsheets/d/' \
                                  '19KSqxtKJQ5FHZbHKxDS3_TzptWeD0DrL-mLk0y0WFYY' \
                                  '/edit#gid=2145200593]\r\n' \
                                  '\r\n' \
                                  '*Test Scenarios:*\r\n' \
                                  '||Requirement||Test Case||Covered by unit/integration test? (Yes/No)' \
                                  '||Test Priority (\r\n' \
                                  'business impact)||\r\n' \
                                  '| | | | |\r\n' \
                                  '\r\n' \
                                  '*Exploratory testing to consider:*\r\n' \
                                  '||Requirement||Test Scenarios||Test Priority (business impact)||Covered by \r\n' \
                                  'frontend/backend Unit Test?||\r\n' \
                                  '| | | | |\r\n'
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
                    description = '*Context*\r\n' \
                                  'Execute the tests of the parent story, and use the information in the *Test \r\n' \
                                  'Information* section to perform the tests.\r\n' \
                                  '\r\n' \
                                  '*Output*\r\n' \
                                  'Tell in one comment (in the story ticket) ' \
                                  'the final status of this first round, \r\n' \
                                  'and in this ticket, fill the bug section.\r\n' \
                                  'Remember to link the bug (if you discover it) with the Story ticket.\r\n' \
                                  '{code:java}\r\n' \
                                  '*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{\r\n' \
                                  'color:#59afe1}BLOCKED{color}* ' \
                                  'Manual Testing following the steps in the description.\r\n' \
                                  '\r\n' \
                                  '*Verified on:*\r\n' \
                                  '*Environment*: localhost\r\n' \
                                  '*Github*: https://github.com/liferay/liferay-portal.git\r\n' \
                                  '*Branch*: master\r\n' \
                                  '*Bundle*: Liferay DXP\r\n' \
                                  '*Database*: MySQL 5.7.22\r\n' \
                                  '*Last Commit*: ? \r\n' \
                                  '\r\n' \
                                  '|| Test Scenarios || Test Result ||\r\n' \
                                  '| |*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{\r\n' \
                                  'color:#59afe1}BLOCKED{color}*|\r\n' \
                                  '| |*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{\r\n' \
                                  'color:#59afe1}BLOCKED{color}*|\r\n' \
                                  '...\r\n' \
                                  '{code}\r\n' \
                                  '*Bugs:*\r\n' \
                                  ' (/)- PASS\r\n' \
                                  ' (!)- To Do\r\n' \
                                  ' (x)- FAIL\r\n' \
                                  ' * *Impeditive:*\r\n' \
                                  '||Ticket||Title||\r\n' \
                                  '|?|?|\r\n' \
                                  ' * *Not Impeditive:*\r\n' \
                                  '||Ticket||Title||\r\n' \
                                  '|?|?|\r\n'
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
                table_starring_string = '||Requirement||'
                table_staring_position = description.find(table_starring_string)
                table_ending_string = '*Exploratory'
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
