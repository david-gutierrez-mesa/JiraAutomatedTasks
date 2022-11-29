from jira_liferay import get_jira_connection
from liferay.helpers import read_test_cases_table_from_description
from liferay.helpers_testmap import is_mapped, get_mapped_stories
from liferay.testmap_jira import get_testmap_connection

ECHO_TESTMAP_ID = '1-7-qJE-J3-jChauzSyCnDvvSbTWeJkSr7u5D_VBOIP0'
JIRA_TESTMAP_MAPPED_RANGE = 'JIRA-TestMap-7.4!A3:B'
TESTMAP_MAPPED_RANGE = 'Test Map!G4:G'


def add_test_cases_to_test_map(jira):
    print("Adding stories into echo test map")
    sheet = get_testmap_connection()
    stories_to_check = jira.search_issues('filter=55104', fields="key, issuelinks, labels, components, description")
    lps_list = get_mapped_stories(sheet, ECHO_TESTMAP_ID, TESTMAP_MAPPED_RANGE)
    for story in stories_to_check:
        if is_mapped(story.key, lps_list):
            print("Processing ", story.key)
            labels = story.get_field("labels")
            test_cases_table = read_test_cases_table_from_description(story.fields.description)
            if 'poshi_test_not_needed' not in labels:
                needs_manual_review = True
                for link in story.fields.issuelinks:
                    linked_issue_key = ""
                    if hasattr(link, "inwardIssue"):
                        linked_issue_key = link.inwardIssue
                    elif hasattr(link, "outwardIssue"):
                        linked_issue_key = link.outwardIssue
                    if linked_issue_key.fields.summary.endswith(' - Product QA | Test Automation Creation'):
                        linked_issue = jira.issue(linked_issue_key.key)
                        test_cases_table = read_test_cases_table_from_description(linked_issue.fields.description)
                        if linked_issue_key.fields.status.name == 'Closed':
                            print("Poshi automation done. Adding as automated by Poshi")
                        else:
                            print("Poshi automation in progress. Adding as need automation")
                        needs_manual_review = False
                        break
                if needs_manual_review:
                    print("Needs manual review")

            else:
                print('Tests covered by integration or not possible to automate')
                test_cases_table = read_test_cases_table_from_description(story.fields.description)
        else:
            print(story.key, 'is already mapped')


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    add_test_cases_to_test_map(jira_connection)
