class TestCasesForComponent:
    def __init__(self, component, test_cases):
        self.component = component
        self.test_cases = test_cases


def __update_collapse_group(sheet, spreadsheet_id, sheet_id, start, end, collapsed):
    local_requests = [{
        "updateDimensionGroup": {
            "dimensionGroup": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": start,
                    "endIndex": end
                },
                "depth": 1,
                "collapsed": collapsed
            },
            "fields": "collapsed"
        }
    }]
    body = {
        'requests': local_requests
    }
    sheet.batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body).execute()


def collapse_group(sheet, spreadsheet_id, sheet_id, start, end):
    __update_collapse_group(sheet, spreadsheet_id, sheet_id, start, end, True)


def component_row(component, matrix):
    for i, matrix_i in enumerate(matrix):
        if component in matrix_i[0]:
            return i
    return 0


def expand_group(sheet, spreadsheet_id, sheet_id, start, end):
    __update_collapse_group(sheet, spreadsheet_id, sheet_id, start, end, False)


def get_group_start_and_end_position(component, matrix):
    header_length = 2
    starting = component_row(component, matrix)
    for i in range(starting + 1, len(matrix)):
        if 'Component:' in matrix[i][0]:
            return starting + header_length + 1, i + header_length
    return 0, 0


def get_mapped_stories(sheet, test_map_id, test_map_range):
    lps_list = sheet.values().get(spreadsheetId=test_map_id, range=test_map_range).execute().get('values', [])
    lps_list_strings = []
    for matrix_i in enumerate(lps_list):
        if len(matrix_i[1]) != 0:
            value = matrix_i[1][0]
            if value not in lps_list_strings:
                lps_list_strings.append(value)

    return lps_list_strings


def is_mapped(element, lps_list_strings):
    if element in lps_list_strings:
        return False
    else:
        return True


def insert_line_after(sheet, spreadsheet_id, sheet_id, sheet_name, sheet_last_column, index, line):
    insert_one_row_after(sheet, spreadsheet_id, sheet_id, index)
    body = {
        'values': line
    }
    range_name = sheet_name + '!A' + str(index + 1) + ':' + sheet_last_column + str(index)
    sheet.values().append(
        spreadsheetId=spreadsheet_id, range=range_name, valueInputOption='USER_ENTERED', body=body).execute()


def insert_lines_in_component(sheet, spreadsheet_id, sheet_id, sheet_name, sheet_last_column, test_cases_to_create,
                              component_column, first_column_number):
    test_map_cases_column = sheet_name + '!' + component_column + str(first_column_number) + ':' + component_column
    matrix = sheet.values().get(spreadsheetId=spreadsheet_id, range=test_map_cases_column).execute() \
        .get('values', [])
    start, end = get_group_start_and_end_position(test_cases_to_create.component, matrix)

    expand_group(sheet, spreadsheet_id, sheet_id, start, end)

    for test_case in reversed(test_cases_to_create.test_cases):
        insert_line_after(sheet, spreadsheet_id, sheet_id, sheet_name, sheet_last_column, end, test_case)

    collapse_group(sheet, spreadsheet_id, sheet_id, start, end + len(test_cases_to_create.test_cases))


def insert_one_row_after(sheet, spreadsheet_id, sheet_id, index):
    local_requests = [{
        "insertDimension": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": index,
                "endIndex": index + 1
            },
            "inheritFromBefore": "true"
        }
    }]
    body = {
        'requests': local_requests
    }
    sheet.batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body).execute()


def line_data(lps, summary, priority, test_type, test_status, test_case, test_name, comments, blocked_reason):
    priority_text = ''
    match priority:
        case 2:
            priority_text = '2 - Low'
        case 3:
            priority_text = '3 - Medium'
        case 4:
            priority_text = '4 - High'
        case 5:
            priority_text = '5 - Critical'
    line = [['N', 'N', 'N', 'N', 'N', 'Y\n(Original)', lps, '=IF(REGEXMATCH(G4, ","), HYPERLINK(CONCATENATE('
                                                            '"https://issues.liferay.com/issues/?jql=key%20in%20(", '
                                                            'G4, ")" ),"Here"), HYPERLINK(CONCAT('
                                                            '"https://issues.liferay.com/browse/",G4),"Here"))',
             summary, priority_text, '', test_type, test_status, test_case, test_name, comments, blocked_reason]]
    return line
