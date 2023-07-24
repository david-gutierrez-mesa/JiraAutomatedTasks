class FileName:
    OUTPUT_BUG_THRESHOLD_EXCEED_FILE_NAME = "bug_threshold_exceed_message_echo.txt"
    OUTPUT_BUG_THRESHOLD_WARNING_FILE_NAME = "bug_threshold_warning_message_echo.txt"
    OUTPUT_INFO_FILE_NAME = "output_info_echo.txt"
    OUTPUT_MESSAGE_FILE_NAME = "output_message_echo.txt"


class Strings:
    Round_1_description = "h1. Bugs found:\n(/) - PASS\n(!) - To Do\n(x) - FAIL\nh2. " \
                          "Impeditive:\n||Ticket||Title||QA Status||\n|?|?|(!)|\nh2. Not " \
                          "impeditive:\n||Ticket||Title||QA Status||\n|?|?|(!)|\n\nh3.Test Cases\n\n*Case 1:* "


class Roles:
    Design_lead = 'carolina.rodriguez'


class Sheets:
    ECH0_DASHBOARD_V3_0 = '1YFWbjajCUgotSC8YyhPbEMDi1ozJ_5EcyDXbYiJM34Q'
    ECHO_TESTMAP_ID = '1-7-qJE-J3-jChauzSyCnDvvSbTWeJkSr7u5D_VBOIP0'


class Squads:
    QA = ['yang.cao@liferay.com', 'lu.liu@liferay.com', 'david.gutierrez@liferay.com', 'alessandro.alves@liferay.com',
          'rafaella.jordao@liferay.com']
    Front = ['pablo.molina@liferay.com', 'victor.galan@liferay.com', 'sandro.chinea@liferay.com',
             'veronica.gonzalez@liferay.com', 'clara.izquierdo@liferay.com', 'diego.hu@liferay.com',
             'stefan.tanasie@liferay.com', 'barbara.cabrera@liferay.com']
    Back = ['eudaldo.alonso@liferay.com', 'jurgen.kappler@liferay.com', 'ruben.pulido@liferay.com',
            'lourdes.fernandez@liferay.com', 'mikel.lorza@liferay.com', 'yurena.cabrera@liferay.com']
    Devs = Front + Back
    Design = ['carolina.rodriguez@liferay.com', 'maria.arce@liferay.com']
    PO = ['julia.molano@liferay.com', 'mateo.hermosin@liferay.com', 'benicio.herrero@liferay.com',
          'javier.burgueno@liferay.com']
    EPM = ['maria.muriel@liferay.com']
    Discovery = Design + PO + EPM
