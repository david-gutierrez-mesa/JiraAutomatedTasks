#!/usr/bin/env python
from echo_team.echo_constants import Roles
from helpers import create_output_files
from helpers_jira import *
from jira_constants import Status, CustomField, Filter
from jira_liferay import get_jira_connection

OUTPUT_MESSAGE_FILE_NAME = "output_message_echo.txt"
OUTPUT_INFO_FILE_NAME = "output_info_echo.txt"


def _create_poshi_task_for_story(jira_local, parent_story, poshi_automation_table):
    parent_key = parent_story.key
    print("Creating automation task for ", parent_key)
    summary = parent_key + ' - Product QA | Test Automation Creation'

    description = 'Create test automation to validate the critical test scenarios/cases of the related story.\n\nThe ' \
                  'focus of this task is to implement the CRITICAL, HIGH, and MID tests of the related story, ' \
                  'but if you believe that can and have time to implement the LOW and TRIVIAL test cases, please, ' \
                  'create one more subtask to it, and go ahead!\n\nh3. Test Scenarios\n' + poshi_automation_table
    new_issue = create_poshi_automation_task_for(jira_local, parent_story, summary, description)
    print("Poshi task ", new_issue.key, " created for", parent_key)
    return new_issue


def assign_qa_engineer(jira, output_info):
    stories_without_qa_engineer = jira.search_issues(Filter.Assign_QA_Engineer,
                                                     fields=['key', 'assignee', CustomField.QA_Engineer])
    for story in stories_without_qa_engineer:
        qa_engineer = [{'name': story.fields.assignee.name}]
        story.update(
            fields={CustomField.QA_Engineer: qa_engineer}
        )
        output_info += "* " + story.fields.assignee.name + " has been assigned as QA for " + \
                       html_issue_with_link(story) + "\n "

    return output_info


def close_ready_for_release_bugs(jira):
    print("Closing bugs in Ready for Release status...")
    bugs_in_ready_for_release = jira.search_issues(Filter.All_bugs_in_Ready_for_Release)
    all_bugs_closed = True
    for bug in bugs_in_ready_for_release:
        bug_id = bug.id
        print("Closing ", bug.key)
        if not bug.fields.fixVersions:
            fix_version = [{'name': 'Master'}]
            bug.update(
                fields={'fixVersions': fix_version}
            )
        can_be_closed = True
        for subtask in bug.fields.subtasks:
            status = subtask.fields.status.name
            if status != Status.Closed:
                can_be_closed = False
                break
        if can_be_closed:
            jira.transition_issue(bug_id, transition=Status.Closed)
            jira.add_comment(bug_id, 'Closing directly since we are not considering Ready for Release status so far',
                             visibility={'type': 'group', 'value': 'liferay-qa'})
        else:
            all_bugs_closed = False

    if not all_bugs_closed:
        raise TypeError("Not all bugs were closed since some of them has not closed subtask")

    print("Ready for Release status are closed")


def creating_testing_subtasks(jira):
    print("Creating subtasks for Echo team...")
    stories_without_testing_subtask = jira.search_issues(Filter.Integration_Sub_task_creation)
    for story in stories_without_testing_subtask:
        print("Creating sub-task for story " + story.key)
        needs_backend = True
        needs_frontend = True
        for subtask in story.fields.subtasks:
            summary = subtask.fields.summary
            if summary == 'Test Scenarios Coverage | Backend':
                needs_backend = False
            elif summary == 'Test Scenarios Coverage | Frontend':
                needs_frontend = False

        components = []
        for component in story.fields.components:
            components.append({'name': component.name})

        if needs_backend:
            subtask_backend = initialize_subtask_back_end(story, components)
            child = jira.create_issue(fields=subtask_backend)
            print("* Created sub-task: " + child.key)

        if needs_frontend:
            subtask_frontend = initialize_subtask_front_end(story, components)
            child = jira.create_issue(fields=subtask_frontend)
            print("* Created sub-task: " + child.key)

    print("Subtasks for Echo team are up to date")


def create_testing_table_for_stories(jira, output_info):
    stories_without_testing_table = jira.search_issues(Filter.Ready_to_create_test_table_on_description)
    for story in stories_without_testing_table:
        current_description = story.fields.description
        poshi_automation_table = AUTOMATION_TABLE_HEADER + '\r\n'
        for subtask in story.fields.subtasks:
            summary = subtask.fields.summary
            if summary == 'Test Scenarios Coverage | Test Creation':
                test_definitions = jira.issue(subtask.id, fields='description').fields.description.replace('\t', '') \
                    .split('\r\n*Case ')
                for case in test_definitions[1:]:
                    case_summary = get_property(case, ':*\r\n')
                    case_priority = get_property(case, 'Test Strategy:')
                    can_be_automated = get_property(case, 'Can be covered by POSHI?:')

                    poshi_automation_table += '|' + case_summary + '|' + case_priority + '|Manual|TBD|TBD|' \
                                              + can_be_automated + '|' + '\r\n'
                break

        updated_description = current_description + '\r\n\r\nh3. Test Scenarios\r\n' + poshi_automation_table
        output_info += "* Testing table created for story " + html_issue_with_link(story) + "\n "
        story.update(fields={'description': updated_description})
    return output_info


def create_poshi_automation_task(jira, output_warning, output_info):
    stories_without_poshi_automation_created = jira.search_issues(Filter.Ready_to_create_POSHI_automation_task)
    for story in stories_without_poshi_automation_created:
        is_automation_task_needed = False
        description = story.fields.description
        table_starring_string = '||Test Scenarios||'
        table_staring_position = description.find(table_starring_string)
        if table_staring_position != -1:
            skip_story = False
            table = description[table_staring_position:]
            table_rows = table.split('\r\n')
            poshi_automation_table = table_rows[0] + 'testcase||Test Name||' + '\r\n'
            for row in table_rows[1:]:
                if row.count('|') == 7:
                    cells = row.split('|')
                    if cells[2].casefold() == 'TBD'.casefold() \
                            or cells[4].casefold() == 'TBD'.casefold() \
                            or cells[5].casefold() == 'TBD'.casefold():
                        output_info += "Table for story " + story.key + "(" + Instance.Jira_URL + "/browse/" \
                                       + story.key + ") is not up to date. Skipping.\n"
                        skip_story = True
                        break
                    elif (cells[4].casefold() == 'No'.casefold() and cells[5].casefold() == 'No'.casefold()) \
                            and cells[6].casefold() == 'Yes'.casefold():
                        poshi_automation_table += row + ' | |' + '\r\n'
                        is_automation_task_needed = True
                    else:
                        poshi_automation_table += '|-' + cells[1].strip() + '-|-' + cells[2].strip() + '-|-' + \
                                                  cells[3].strip() + '-|-' + cells[4].strip() + '-|-' + \
                                                  cells[5].strip() + '-|-' + cells[6].strip() + '-| | |' + '\r\n'
                else:
                    break
            if skip_story:
                continue
            if is_automation_task_needed:
                poshi_task = _create_poshi_task_for_story(jira, story, poshi_automation_table)
                output_info += "* Automation task created for story " + html_issue_with_link(story) + "\n "
                close_functional_automation_subtask(jira, story, poshi_task.key)
            else:
                jira.add_comment(story, "No Poshi automation is needed.")
                story.fields.labels.append("poshi_test_not_needed")
                story.update(fields={"labels": story.fields.labels})
                output_info += "* Automation task not needed or not possible to create for story " + \
                               html_issue_with_link(story) + "\n "
                close_functional_automation_subtask(jira, story)
        else:
            output_warning += "Story " + story.key + " don't have test table. \n"

    return output_warning, output_info


def create_poshi_automation_task_for_bugs(jira, output_info):
    bugs_without_poshi_automation_created = \
        jira.search_issues(Filter.Closed_Bugs_with_FP4_and_FP5_without_automation_task)
    for bug in bugs_without_poshi_automation_created:
        poshi_task = create_poshi_automation_task_for_bug(jira, bug)
        jira.transition_issue(poshi_task, transition=Status.Selected_for_development)
        output_info += "* Automation task created for bug " + html_issue_with_link(bug) + "\n "

    return output_info


def fill_round_technical_testing_description(jira, output_info):
    round_technical_testing_sub_tasks = jira.search_issues(Filter.Round_tasks_without_description, fields="key")
    for task in round_technical_testing_sub_tasks:
        updated_description = "h1. Bugs found:\n(/) - PASS\n(!) - To Do\n(x) - FAIL\nh2. " \
                              "Impeditive:\n||Ticket||Title||QA Status||\n|?|?|(!)|\nh2. Not " \
                              "impeditive:\n||Ticket||Title||QA Status||\n|?|?|(!)|\n\nh3.Test Cases\n\n*Case 1:* "
        task.update(fields={'description': updated_description})
    return output_info


def transition_story_to_ready_for_pm_review(jira, output_warning, output_info):
    story_to_ready_for_pm_review = jira.search_issues(Filter.Stories_ready_to_be_closed,
                                                      fields=['key', 'id', 'description', 'labels',
                                                              'issuelinks', 'status'])
    for story in story_to_ready_for_pm_review:
        test_cases = read_test_cases_table_from_description(story.fields.description)
        can_be_closed = True
        for row in test_cases:
            if row.count('|') == 7:
                cells = row.split('|')
                if cells[2].casefold() == 'TBD'.casefold() \
                        or cells[4].casefold() == 'TBD'.casefold() \
                        or cells[5].casefold() == 'TBD'.casefold():
                    output_warning += "* Table for story " + html_issue_with_link(story) +\
                                      " is not uptodate. Skipping.\n"
                    can_be_closed = False
                    break
        if can_be_closed:
            if 'poshi_test_not_needed' not in story.get_field("labels"):
                for link in story.fields.issuelinks:
                    linked_issue_key = ""
                    if hasattr(link, "inwardIssue"):
                        linked_issue_key = link.inwardIssue
                    elif hasattr(link, "outwardIssue"):
                        linked_issue_key = link.outwardIssue
                    if linked_issue_key.fields.summary.endswith(' - Product QA | Test Automation Creation'):
                        if linked_issue_key.fields.status.name == 'Open':
                            jira.transition_issue(linked_issue_key.id, transition=Status.Selected_for_development)
                        break
            if story.get_field("status").id == Status.Ready_for_testing:
                jira.transition_issue(story.id, transition=Status.In_Testing)
            jira.transition_issue(story.id, transition=Status.Ready_for_Product_Review)
            jira.assign_issue(story.id, Roles.Design_lead)
            output_info += "* Story " + html_issue_with_link(story) + " has been send for PM review.\n"
    return output_warning, output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    jira_connection = get_jira_connection()
    info = assign_qa_engineer(jira_connection, info)
    info = fill_round_technical_testing_description(jira_connection, info)
    creating_testing_subtasks(jira_connection)
    warning, info = create_poshi_automation_task(jira_connection, warning, info)
    info = create_testing_table_for_stories(jira_connection, info)
    info = create_poshi_automation_task_for_bugs(jira_connection, info)
    close_ready_for_release_bugs(jira_connection)
    warning, info = transition_story_to_ready_for_pm_review(jira_connection, warning, info)

    create_output_files([warning, OUTPUT_MESSAGE_FILE_NAME], [info, OUTPUT_INFO_FILE_NAME])
