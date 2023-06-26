#!/usr/bin/env python
from liferay.utils.jira.jira_constants import Filter
from liferay.utils.jira.jira_constants import Status
from liferay.utils.jira.jira_helpers import create_poshi_automation_task_for, close_functional_automation_subtask
from liferay.utils.jira.jira_liferay import get_jira_connection
from liferay.utils.sheets.sheets_constants import SheetInstance


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
                    description = '*Output*\n' \
                                  ' # Our table with the Test scenarios/test cases to be validated in the \n' \
                                  'validation phase.\n' \
                                  ' # After being reviewed by the team, add a finalized table ' \
                                  'to the parent story \n' \
                                  'description\n' \
                                  ' # Add test cases to [Test ' \
                                  'Map|' + SheetInstance.GOOGLE_SHEET_URL + \
                                  '19KSqxtKJQ5FHZbHKxDS3_TzptWeD0DrL-mLk0y0WFYY' \
                                  '/edit#gid=2145200593]\n' \
                                  '\n' \
                                  '*Test Scenarios:*\n' \
                                  '||Requirement||Test Case||Covered by unit/integration test? (Yes/No)' \
                                  '||Test Priority (\n' \
                                  'business impact)||\n' \
                                  '| | | | |\n' \
                                  '\n' \
                                  '*Exploratory testing to consider:*\n' \
                                  '||Requirement||Test Scenarios||Test Priority (business impact)||Covered by \n' \
                                  'frontend/backend Unit Test?||\n' \
                                  '| | | | |\n'
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
                    description = '*Context*\n' \
                                  'Execute the tests of the parent story, and use the information in the *Test \n' \
                                  'Information* section to perform the tests.\n' \
                                  '\n' \
                                  '*Output*\n' \
                                  'Tell in one comment (in the story ticket) ' \
                                  'the final status of this first round, \n' \
                                  'and in this ticket, fill the bug section.\n' \
                                  'Remember to link the bug (if you discover it) with the Story ticket.\n' \
                                  '{code:java}\n' \
                                  '*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{\n' \
                                  'color:#59afe1}BLOCKED{color}* ' \
                                  'Manual Testing following the steps in the description.\n' \
                                  '\n' \
                                  '*Verified on:*\n' \
                                  '*Environment*: localhost\n' \
                                  '*Github*: https://github.com/liferay/liferay-portal.git\n' \
                                  '*Branch*: master\n' \
                                  '*Bundle*: Liferay DXP\n' \
                                  '*Database*: MySQL 5.7.22\n' \
                                  '*Last Commit*: ? \n' \
                                  '\n' \
                                  '|| Test Scenarios || Test Result ||\n' \
                                  '| |*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{\n' \
                                  'color:#59afe1}BLOCKED{color}*|\n' \
                                  '| |*{color:#14892c}PASSED{color}* / *{color:#d04437}FAILED{color}* / *{\n' \
                                  'color:#59afe1}BLOCKED{color}*|\n' \
                                  '...\n' \
                                  '{code}\n' \
                                  '*Bugs:*\n' \
                                  ' (/)- PASS\n' \
                                  ' (!)- To Do\n' \
                                  ' (x)- FAIL\n' \
                                  ' * *Impeditive:*\n' \
                                  '||Ticket||Title||\n' \
                                  '|?|?|\n' \
                                  ' * *Not Impeditive:*\n' \
                                  '||Ticket||Title||\n' \
                                  '|?|?|\n'
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
