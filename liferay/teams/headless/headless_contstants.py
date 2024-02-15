from utils.liferay_utils.sheets.sheets_constants import SheetInstance


class FileName:
    OUTPUT_BUG_THRESHOLD_INFO_FILE_NAME = "bug_threshold_output_info_headless.txt"
    OUTPUT_MESSAGE_FILE_NAME = "output_message_headless.txt"
    OUTPUT_INFO_FILE_NAME = "output_info_headless.txt"


class Filter:
    GSheets_Headless_All_Stories = 'filter=12516'
    Headless_All_verified_Bugs_in_master = 'filter=12514'
    Headless_Team_Ready_to_create_POSHI_Automation_Task = 'filter=13880'
    Integration_In_Development_Sub_task_creation_Headless_team = 'filter=12231'
    Product_QA_Test_Validation_Round_1 = 'filter=12232'


class HeadlessStrings:
    poshi_task_description = 'Create test automation to validate the critical test scenarios/cases of the related ' \
                             'story.\n\nThe focus of this task is to implement the CRITICAL, HIGH, and MID tests of ' \
                             'the related story, ' \
                             'but if you believe that can and have time to implement the LOW and TRIVIAL test cases, ' \
                             'please, ' \
                             'create one more subtask to it, and go ahead!\n\nh3. Test Scenarios\n'

    test_creation_description = '*Output*\n' \
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
    test_validation_round_1_description = '*Context*\n' \
                                          'Execute the tests of the parent story, and use the information in the  '\
                                          '*Test \n' \
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


class Sheets:
    HEADLESS_TESTMAP_ID = '19KSqxtKJQ5FHZbHKxDS3_TzptWeD0DrL-mLk0y0WFYY'


class Squads:
    QA = ['yanan.yuan@liferay.com', 'kevin.wan@liferay.com', 'magdalena.jedraszak@liferay.com']
    Front = ['carlos.montenegro@liferay.com']
    Back = ['carlos.correa@liferay.com', 'alejandro.tardin@liferay.com', 'luismiguel.barcos@liferay.com',
            'sergio.jdelcoso@liferay.com', 'matija.petanjek@liferay.com']
    Devs = Front + Back
    PO = ['pablo.agulla@liferay.com', 'benicio.herrero@liferay.com']
    EPM = ['bruno.fernandez@liferay.com']
    Discovery = PO + EPM
