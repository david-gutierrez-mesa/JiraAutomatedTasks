class EchoStrings:
    Round_1_description = "h1. Bugs found:\n(/) - PASS\n(!) - To Do\n(x) - FAIL\nh2. " \
                          "Impeditive:\n||Ticket||Title||QA Status||\n|?|?|(!)|\n\nh2. Not " \
                          "impeditive:\n||Ticket||Title||QA Status||\n|?|?|(!)|\n\nh3.Test Cases\n\n*Case 1:* "


class FileName:
    OUTPUT_BUG_THRESHOLD_EXCEED_FILE_NAME = "bug_threshold_exceed_message_echo.txt"
    OUTPUT_BUG_THRESHOLD_WARNING_FILE_NAME = "bug_threshold_warning_message_echo.txt"
    OUTPUT_INFO_FILE_NAME = "output_info_echo.txt"
    OUTPUT_MESSAGE_FILE_NAME = "output_message_echo.txt"


class Filter:
    All_bugs_in_Ready_for_Release = 'filter=11502'
    Assign_QA_Engineer = 'filter=11500'
    Closed_Bugs_with_FP4_and_FP5_without_automation_task = 'filter=11675'
    Design_Sub_task_creation = 'filter=14709'
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
    Integration_Sub_task_creation = 'filter=12131'
    Ready_to_create_POSHI_automation_task = 'filter=12213'
    Ready_to_create_test_table_on_description = 'filter=12111'
    Round_tasks_without_description = 'filter=11517'
    Stories_ready_to_be_closed = 'filter=12230'
    Stories_to_add_into_test_map = 'filter=11512'


class Relationship:
    PM_PO_matrix = {
        'mateo.hermosin@liferay.com': 'javier.burgueno@liferay.com',
        'julia.molano@liferay.com': 'ruth.alves@liferay.com'
    }


class Roles:
    Design_lead = 'maria.arce'


class Sheets:
    ECH0_DASHBOARD_V3_0 = '1YFWbjajCUgotSC8YyhPbEMDi1ozJ_5EcyDXbYiJM34Q'
    ECHO_TESTMAP_ID = '1-7-qJE-J3-jChauzSyCnDvvSbTWeJkSr7u5D_VBOIP0'


class Squads:
    QA = ['yang.cao@liferay.com', 'lu.liu@liferay.com', 'david.gutierrez@liferay.com', 'alessandro.alves@liferay.com',
          'rafaella.jordao@liferay.com', 'beatriz.alvarez@liferay.com']
    Front = ['pablo.molina@liferay.com', 'victor.galan@liferay.com', 'sandro.chinea@liferay.com',
             'veronica.gonzalez@liferay.com', 'clara.izquierdo@liferay.com', 'diego.hu@liferay.com',
             'stefan.tanasie@liferay.com', 'barbara.cabrera@liferay.com']
    Back = ['eudaldo.alonso@liferay.com', 'jurgen.kappler@liferay.com', 'ruben.pulido@liferay.com',
            'lourdes.fernandez@liferay.com', 'mikel.lorza@liferay.com', 'yurena.cabrera@liferay.com']
    Devs = Front + Back
    Design = ['carolina.rodriguez@liferay.com', 'maria.arce@liferay.com']
    PM = ['julia.molano@liferay.com', 'mateo.hermosin@liferay.com']
    PO = ['javier.burgueno@liferay.com', 'ruth.alves@liferay.com']
    EPM = ['maria.muriel@liferay.com']
    Discovery = Design + PM + PO + EPM
