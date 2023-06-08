#!/usr/bin/env python

from helpers import create_output_files
from jira_constants import Filter
from jira_liferay import get_jira_connection
from helpers_testmap import *
from testmap_jira import get_testmap_connection

ECH0_DASHBOARD_ACTIONABLE_BUGS_TAB = 'Actionable Bugs'
ECH0_DASHBOARD_ACTIONABLE_BUGS_TAB_RANGE = ECH0_DASHBOARD_ACTIONABLE_BUGS_TAB + '!B4:G'
ECH0_DASHBOARD_BUGS_PER_AREA_TAB = 'Bugs Per area'
ECH0_DASHBOARD_BUGS_PER_AREA_TAB_RANGE = ECH0_DASHBOARD_BUGS_PER_AREA_TAB + '!B4:F'
ECH0_DASHBOARD_BUGS_PER_AREA_LAST_MONTH_RANGE = ECH0_DASHBOARD_BUGS_PER_AREA_TAB + '!W4:AA'
ECH0_DASHBOARD_ESCALATED_SECURITY = 'Escalates & Sec. Vuln. details'
ECH0_DASHBOARD_ESCALATED_SECURITY_ACTIONABLE_IMPEDIBUG_RANGE = ECH0_DASHBOARD_ESCALATED_SECURITY + '!AR8:AV'
ECH0_DASHBOARD_ESCALATED_SECURITY_CURRENT_CRITICAL_RANGE = ECH0_DASHBOARD_ESCALATED_SECURITY + '!C8:G'
ECH0_DASHBOARD_ESCALATED_SECURITY_CURRENT_ESCALATIONS_RANGE = ECH0_DASHBOARD_ESCALATED_SECURITY + '!AJ8:AN'
ECH0_DASHBOARD_ESCALATED_SECURITY_NON_CURRENT_CRITICAL_RANGE = ECH0_DASHBOARD_ESCALATED_SECURITY + '!L8:Q'
ECH0_DASHBOARD_ESCALATED_SECURITY_NON_SECURITY_VUL_RANGE = ECH0_DASHBOARD_ESCALATED_SECURITY + '!AB8:AF'
ECH0_DASHBOARD_ESCALATED_SECURITY_PENDING_BACKPORTS_RANGE = ECH0_DASHBOARD_ESCALATED_SECURITY + '!U8:Y'
ECH0_DASHBOARD_V3_0 = '1YFWbjajCUgotSC8YyhPbEMDi1ozJ_5EcyDXbYiJM34Q'
GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/'
OUTPUT_BUG_THRESHOLD_EXCEED_FILE_NAME = "bug_threshold_exceed_message_echo.txt"
OUTPUT_BUG_THRESHOLD_WARNING_FILE_NAME = "bug_threshold_warning_message_echo.txt"
OUTPUT_INFO_FILE_NAME = "output_info_echo.txt"
OUTPUT_MESSAGE_FILE_NAME = "output_message_echo.txt"


def _update_echo_bug_actionable_bugs_tab(sheet, jira):
    currently_open_bugs = get_all_issues(jira, Filter.Echo_Dashboard_v3_0_Actionable_bugs,
                                         ["key", "summary", "status", CustomField.Fix_Priority, "components",
                                          "created"])
    body_values = []
    for bug in currently_open_bugs:
        components = ', '.join(get_components(bug))
        fix_priority = ''
        if bug.get_field(CustomField.Fix_Priority) is not None:
            fix_priority = bug.get_field(CustomField.Fix_Priority).value
        body_values.append(['=HYPERLINK("' + Instance.Jira_URL + '/browse/' + bug.key + '","' + bug.key + '")',
                            bug.get_field('summary'),
                            bug.get_field('status').name,
                            fix_priority,
                            components,
                            bug.get_field('created')])

    update_table(sheet,
                 ECH0_DASHBOARD_V3_0,
                 ECH0_DASHBOARD_ACTIONABLE_BUGS_TAB_RANGE,
                 body_values,
                 ECH0_DASHBOARD_ACTIONABLE_BUGS_TAB)


def _update_echo_bug_threshold_bug_per_area_tab(sheet, jira):
    currently_open_bugs = get_all_issues(jira, Filter.Echo_bug_threshold,
                                         ["key", "summary", "status", CustomField.Fix_Priority, "components"])
    body_values = []
    for bug in currently_open_bugs:
        components = ', '.join(get_components(bug))
        fix_priority = ''
        if bug.get_field(CustomField.Fix_Priority) is not None:
            fix_priority = bug.get_field(CustomField.Fix_Priority).value
        body_values.append(['=HYPERLINK("' + Instance.Jira_URL + '/browse/' + bug.key + '","' + bug.key + '")',
                            bug.get_field('summary'),
                            bug.get_field('status').name,
                            fix_priority,
                            components])

    update_table(sheet,
                 ECH0_DASHBOARD_V3_0,
                 ECH0_DASHBOARD_BUGS_PER_AREA_TAB_RANGE,
                 body_values,
                 ECH0_DASHBOARD_BUGS_PER_AREA_TAB)

    currently_open_bugs_last_month = get_all_issues(jira, Filter.Echo_Dashboard_v3_0_Bugs_Per_Area_Last_month_bugs,
                                                    ["key", "status", CustomField.Fix_Priority,
                                                     "components", "resolution"])
    body_values = []
    for bug in currently_open_bugs_last_month:
        components = ', '.join(get_components(bug))
        fix_priority = ''
        if bug.get_field(CustomField.Fix_Priority) is not None:
            fix_priority = bug.get_field(CustomField.Fix_Priority).value
        body_values.append(['=HYPERLINK("' + Instance.Jira_URL + '/browse/' + bug.key + '","' + bug.key + '")',
                            bug.get_field('status').name,
                            fix_priority,
                            components,
                            bug.get_field('resolution').name
                            ])

    update_table(sheet,
                 ECH0_DASHBOARD_V3_0,
                 ECH0_DASHBOARD_BUGS_PER_AREA_LAST_MONTH_RANGE,
                 body_values,
                 ECH0_DASHBOARD_BUGS_PER_AREA_TAB)


def _update_echo_bug_th_esc_and_sec_vul_table(sheet, jira, jql, sheet_range):
    currently_open_bugs = get_all_issues(jira, jql,
                                         [CustomField.Fix_Priority, "status", "summary", "affectedVersion"])
    body_values = []
    for bug in currently_open_bugs:
        affected_version = ', '.join(get_affected_version(bug))
        fix_priority = ''
        if bug.get_field(CustomField.Fix_Priority) is not None:
            fix_priority = bug.get_field(CustomField.Fix_Priority).value
        body_values.append(['=HYPERLINK("' + Instance.Jira_URL + '/browse/' + bug.key + '","' + bug.key + '")',
                            fix_priority,
                            bug.get_field('status').name,
                            bug.get_field('summary'),
                            affected_version])

    update_table(sheet,
                 ECH0_DASHBOARD_V3_0,
                 sheet_range,
                 body_values,
                 ECH0_DASHBOARD_ESCALATED_SECURITY,
                 False)


def _update_echo_bug_threshold_actionable_bugs(sheet, jira):
    currently_open_bugs = get_all_issues(jira, Filter.Echo_Dashboard_v3_0_Impedibugs,
                                         ["status", "summary", "assignee", "created"])
    body_values = []
    for bug in currently_open_bugs:
        assignee = ''
        if bug.get_field('assignee') is not None:
            assignee = bug.get_field('assignee').name
        body_values.append(['=HYPERLINK("' + Instance.Jira_URL + '/browse/' + bug.key + '","' + bug.key + '")',
                            bug.get_field('status').name,
                            bug.get_field('summary'),
                            assignee,
                            bug.get_field('created')
                            ])

    update_table(sheet,
                 ECH0_DASHBOARD_V3_0,
                 ECH0_DASHBOARD_ESCALATED_SECURITY_ACTIONABLE_IMPEDIBUG_RANGE,
                 body_values,
                 ECH0_DASHBOARD_ESCALATED_SECURITY,
                 True)


def _update_echo_bug_threshold_current_critical_sec_vulnerabilities(sheet, jira):
    _update_echo_bug_th_esc_and_sec_vul_table(sheet, jira,
                                              Filter.Echo_Dashboard_v3_0_Current_Critical_Sec_Vul,
                                              ECH0_DASHBOARD_ESCALATED_SECURITY_CURRENT_CRITICAL_RANGE)


def _update_echo_bug_threshold_current_escalations(sheet, jira):
    _update_echo_bug_th_esc_and_sec_vul_table(sheet, jira,
                                              Filter.Echo_Dashboard_v3_0_Escalations,
                                              ECH0_DASHBOARD_ESCALATED_SECURITY_CURRENT_ESCALATIONS_RANGE)


def _update_echo_bug_threshold_non_current_critical_sec_vulnerabilities(sheet, jira):
    _update_echo_bug_th_esc_and_sec_vul_table(sheet, jira,
                                              Filter.Echo_Dashboard_v3_0_None_Critical_Security_Vulnerabilities,
                                              ECH0_DASHBOARD_ESCALATED_SECURITY_NON_CURRENT_CRITICAL_RANGE)


def _update_echo_bug_threshold_non_security_vul_wit_lps(sheet, jira):
    _update_echo_bug_th_esc_and_sec_vul_table(sheet, jira,
                                              Filter.Echo_Dashboard_v3_0_Non_Critical_Security_Vulnerabilities_with_LPP,
                                              ECH0_DASHBOARD_ESCALATED_SECURITY_NON_SECURITY_VUL_RANGE)


def _update_echo_bug_threshold_pending_backports(sheet, jira):
    _update_echo_bug_th_esc_and_sec_vul_table(sheet, jira,
                                              Filter.Echo_Dashboard_v3_0_Esc_Sec_Vul_Pending_Backports,
                                              ECH0_DASHBOARD_ESCALATED_SECURITY_PENDING_BACKPORTS_RANGE)


def _update_echo_bug_threshold_escalated_sec_vulnerabilities_tab(sheet, jira):
    _update_echo_bug_threshold_actionable_bugs(sheet, jira)
    _update_echo_bug_threshold_current_critical_sec_vulnerabilities(sheet, jira)
    _update_echo_bug_threshold_current_escalations(sheet, jira)
    _update_echo_bug_threshold_non_current_critical_sec_vulnerabilities(sheet, jira)
    _update_echo_bug_threshold_non_security_vul_wit_lps(sheet, jira)
    _update_echo_bug_threshold_pending_backports(sheet, jira)


def update_echo_bug_threshold(sheet, jira, output_info):
    _update_echo_bug_threshold_bug_per_area_tab(sheet, jira)
    _update_echo_bug_threshold_escalated_sec_vulnerabilities_tab(sheet, jira)
    _update_echo_bug_actionable_bugs_tab(sheet, jira)

    output_info += '<' + GOOGLE_SHEET_URL + ECH0_DASHBOARD_V3_0 + '|Dashboard v3.0 > updated\n'
    return output_info


if __name__ == "__main__":
    warning = ''
    info = ''
    bug_threshold_exceed = ''
    bug_threshold_warning = ''
    jira_connection = get_jira_connection()
    sheet_connection = get_testmap_connection()
    info = update_echo_bug_threshold(sheet_connection, jira_connection, info)
    create_output_files([warning, OUTPUT_MESSAGE_FILE_NAME],
                        [info, OUTPUT_INFO_FILE_NAME],
                        [bug_threshold_exceed, OUTPUT_BUG_THRESHOLD_EXCEED_FILE_NAME],
                        [bug_threshold_warning, OUTPUT_BUG_THRESHOLD_WARNING_FILE_NAME])
