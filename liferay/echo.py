#!/usr/bin/env python
from helpers import get_property, initialize_subtask_front_end, initialize_subtask_back_end, AUTOMATION_TABLE_HEADER, \
    initialize_subtask_test_automation, create_poshi_automation_task_for, create_poshi_automation_task_for_bug
from jira_liferay import get_jira_connection


def __create_poshi_task_for_story(jira_local, parent_story, poshi_automation_table):
    parent_key = parent_story.key
    print("Creating automation task for ", parent_key)
    summary = parent_key + ' - Product QA | Test Automation Creation'

    description = 'Create test automation to validate the critical test scenarios/cases of the related story.\n\nThe ' \
                  'focus of this task is to implement the CRITICAL, HIGH, and MID tests of the related story, ' \
                  'but if you believe that can and have time to implement the LOW and TRIVIAL test cases, please, ' \
                  'create one more subtask to it, and go ahead!\n\nh3. Test Scenarios\n' + poshi_automation_table
    new_issue = create_poshi_automation_task_for(jira_local, parent_story, summary, description)
    print("Poshi task ", new_issue.key, " created for", parent_key)


def __initialize_subtask_test_automation(story, components):
    description = 'Create test automation to validate the critical test scenarios/cases of the related story.'
    return initialize_subtask_test_automation(story, components, description)


def assign_qa_engineer(jira):
    print("Assigning QA Engineer to LPS tasks...")
    stories_without_qa_engineer = jira.search_issues('filter=54607', fields="assignee, customfield_24852")
    for story in stories_without_qa_engineer:
        qa_engineer = [{'name': story.fields.assignee.name}]
        story.update(
            fields={'customfield_24852': qa_engineer}
        )

    print("LPS have QA Engineer field up to date")


def close_ready_for_release_bugs(jira):
    print("Closing bugs in Ready for Release status...")
    bugs_in_ready_for_release = jira.search_issues('filter=54632')
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
            if status != 'Closed':
                can_be_closed = False
                break
        if can_be_closed:
            jira.transition_issue(bug_id, transition='Closed')
            jira.add_comment(bug_id, 'Closing directly since we are not considering Ready for Release status so far',
                             visibility={'type': 'group', 'value': 'liferay-qa'})
        else:
            all_bugs_closed = False

    if not all_bugs_closed:
        raise TypeError("Not all bugs were closed since some of them has not closed subtask")

    print("Ready for Release status are closed")


def creating_testing_subtasks(jira):
    print("Creating subtasks for Echo team...")
    stories_without_testing_subtask = jira.search_issues('filter=54572')
    for story in stories_without_testing_subtask:
        print("Creating sub-task for story " + story.id)
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


def create_testing_table_for_stories(jira):
    print("Creating tests table for Echo team...")
    stories_without_testing_table = jira.search_issues('filter=54772')
    for story in stories_without_testing_table:
        current_description = story.fields.description
        poshi_automation_table = AUTOMATION_TABLE_HEADER + '\r\n'
        for subtask in story.fields.subtasks:
            summary = subtask.fields.summary
            if summary == 'Test Scenarios Coverage | Test Creation':
                test_definitions = jira.issue(subtask.id, fields='description').fields.description.split('\r\n*Case')
                for case in test_definitions[1:]:
                    case_summary = get_property(case, ':*\r\n')
                    case_priority = get_property(case, 'Test Strategy:')
                    can_be_automated = get_property(case, 'Can be covered by POSHI?:')

                    poshi_automation_table += '|' + case_summary + '|' + case_priority + '|Manual|TBD|TBD|' \
                                              + can_be_automated + '|' + '\r\n'
                break

        updated_description = current_description + '\r\n\r\nh3. Test Scenarios\r\n' + poshi_automation_table
        print("Crating table for story " + story.key)
        story.update(fields={'description': updated_description})

    print("All stories have testing table")


def create_poshi_automation_task(jira):
    print("Creating Poshi tasks...")
    output_message = ''
    stories_without_poshi_automation_created = jira.search_issues('filter=54646')
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
                        output_message += "Table for story " + story.key + " is not uptodate. Skipping.\n"
                        skip_story = True
                        break
                    elif (cells[4].casefold() == 'No'.casefold() and cells[5].casefold() == 'No'.casefold()) \
                            and cells[6].casefold() == 'Yes'.casefold():
                        is_automation_task_needed = True
                    poshi_automation_table += row + ' | |' + '\r\n'
                else:
                    break
            if skip_story:
                break
            if is_automation_task_needed:
                hash_poshi_subtask = [subtask for subtask in story.get_field('subtasks') if subtask.fields.summary ==
                                      'Product QA | Functional Automation']
                if hash_poshi_subtask:
                    output_message += "Story " + story.key + " has already a POSHI subtask.\n"
                else:
                    __create_poshi_task_for_story(jira, story, poshi_automation_table)

            else:
                jira.add_comment(story, "No Poshi automation is needed.")
                story.fields.labels.append("poshi_test_not_needed")
                story.update(fields={"labels": story.fields.labels})
                print("Automation task not needed or not possible to create")
        else:
            output_message += "Story " + story.key + " don't have test table. \n"

    print(output_message)


def create_poshi_automation_task_for_bugs(jira):
    bugs_without_poshi_automation_created = jira.search_issues('filter=51790')
    for bug in bugs_without_poshi_automation_created:
        poshi_task = create_poshi_automation_task_for_bug(jira, bug)
        jira.transition_issue(poshi_task, transition='10022')


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    assign_qa_engineer(jira_connection)
    creating_testing_subtasks(jira_connection)
    create_testing_table_for_stories(jira_connection)
    create_poshi_automation_task(jira_connection)
    create_poshi_automation_task_for_bugs(jira_connection)
    close_ready_for_release_bugs(jira_connection)
