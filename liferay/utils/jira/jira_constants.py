class CustomField:
    Bug_type = 'customfield_10240'
    Epic_Link = 'customfield_10014'
    Fix_Priority = 'customfield_10211'
    QA_Engineer = 'customfield_10227'


class Filter:
    All_bugs_in_Ready_for_Release = 'filter=11502'
    Assign_QA_Engineer = 'filter=11500'
    Closed_Bugs_with_FP4_and_FP5_without_automation_task = 'filter=11675'
    Echo_7_4_CE_GA_All = 'filter=11478'
    Echo_Dashboard_v3_0_Actionable_bugs = 'filter=11520'
    Echo_Dashboard_v3_0_Bugs_Per_Area_Last_month_bugs = 'filter=11527'
    Echo_Dashboard_v3_0_Current_Critical_Sec_Vul = 'filter=11521'
    Echo_Dashboard_v3_0_Current_month_closed_bugs = 'project = LPS AND filter = "Components | LPS-Echo" AND (' \
                                                    'issuetype = Bug OR issuetype = "Regression Bug") AND filter = ' \
                                                    '"Misc | Bug Version Filtering" AND status changed to Closed ' \
                                                    'after startOfMonth({month}) before endOfMonth({month})  AND ' \
                                                    'status = Closed '
    Echo_Dashboard_v3_0_Current_month_reported_bugs = 'project = LPS AND filter = "Components | LPS-Echo" AND (' \
                                                      'issuetype = Bug OR issuetype = "Regression Bug") AND filter = ' \
                                                      '"Misc | Bug Version Filtering" AND (status changed to ' \
                                                      'verified after startOfMonth({month}) before endOfMonth({' \
                                                      'month})  AND NOT status changed to verified before endofmonth(' \
                                                      '{last_month})  OR status changed to "In progress" from open ' \
                                                      'after startOfMonth({month}) before endOfMonth({month})  AND ' \
                                                      'created >= startOfMonth({month}) AND created <= endOfMonth({' \
                                                      'month})) '
    Echo_Dashboard_v3_0_Esc_Sec_Vul_Pending_Backports = 'filter=13089'
    Echo_Dashboard_v3_0_Escalations = 'filter=11524'
    Echo_Dashboard_v3_0_Impedibugs = 'filter=11525'
    Echo_Dashboard_v3_0_Non_Critical_Security_Vulnerabilities_with_LPP = 'filter=13091'
    Echo_Dashboard_v3_0_None_Critical_Security_Vulnerabilities = 'filter=13090'
    Echo_bug_threshold = 'filter=11519'
    Echo_Stories_with_impedibug_opened_by_PM_UX = 'filter=13504'
    FI_ALL_bugs_unresolved_Manoel = 'filter=11516'
    FI_Ready_for_Testing_Stories_without_Test_Validation = 'filter=12425'
    FI_Stories_without_test_creation_subtask = 'filter=12424'
    FI_Test_Scope_out_of_Scope_Creation_task_creation = 'filter=12855'
    GSheets_FI_7_4_CE_GA_All = 'filter=13335'
    GSheets_Headless_All_Stories = 'filter=12516'
    Headless_All_verified_Bugs_in_master = 'filter=12514'
    Headless_Team_Ready_to_create_POSHI_Automation_Task = 'filter=13880'
    Integration_In_Development_Sub_task_creation_Headless_team = 'filter=12231'
    Integration_Sub_task_creation = 'filter=12131'
    Peds_Bugs_Unresolved = 'filter=12726'
    Peds_7_4_CE_GA_All = 'filter=13148'
    Product_QA_Test_Validation_Round_1 = 'filter=12232'
    Ready_to_create_POSHI_automation_task = 'filter=12213'
    Ready_to_create_test_table_on_description = 'filter=12111'
    Round_tasks_without_description = 'filter=11517'
    Stories_ready_to_be_closed = 'filter=12230'
    Stories_to_add_into_test_map = 'filter=11512'
    Uniform_Bugs_Unresolved = 'filter=12957'
    Uniform_7_4_CE_GA_All = 'filter=13150'


class Instance:
    Jira_URL = "https://liferay.atlassian.net"
    Type = "Cloud"


class Status:
    Closed = 'Closed'
    In_Testing = 'In Testing'
    Open = 'Open'
    Ready_for_testing = '10619'


class Transition:
    Closed = 'Closed'
    In_Testing = 'In Testing'
    Ready_for_Product_Review = 'Ready for Product Review'
    Selected_for_development = 'Selected for Development'
