from jira_liferay import get_jira_connection


def add_test_cases_to_test_map(jira):
    print("Adding stories into echo test map")
    stories_to_check = jira.search_issues('filter=55104', fields="key, issuelinks, labels")
    #stories_to_check = jira.search_issues('filter=55104')
    for story in stories_to_check:
        print("Processing ", story.key)
        labels = story.get_field("labels")
        if 'poshi_test_not_needed' not in labels:
            for link in story.fields.issuelinks:
                linked_issue_key = ""
                if hasattr(link, "inwardIssue"):
                    linked_issue_key = link.inwardIssue
                elif hasattr(link, "outwardIssue"):
                    linked_issue_key = link.outwardIssue
                if linked_issue_key.fields.summary.endswith(' - Product QA | Test Automation Creation'):
                    if linked_issue_key.fields.status.name == 'Closed':
                        print("Poshi automation done. Adding as automated by Poshi")
                        linked_issue = jira.issue(linked_issue_key.key)
                        description = linked_issue.get_field('description')
                    else:
                        print("Poshi automation in progress. Adding as need automation")

        else:
            print('Tests covered by integration or not possible to automate')


if __name__ == "__main__":
    jira_connection = get_jira_connection()
    add_test_cases_to_test_map(jira_connection)
