from datetime import datetime
import pytz


def _update_collapse_group(sheet, spreadsheet_id, sheet_id, start, end, collapsed):
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
    _update_collapse_group(sheet, spreadsheet_id, sheet_id, start, end, True)


def create_collapse_group(sheet, spreadsheet_id, sheet_id, start, end):
    local_requests = [create_collapse_group_body(sheet_id, start, end)]
    body = {
        'requests': local_requests
    }
    sheet.batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body).execute()


def create_collapse_group_body(sheet_id, start, end):
    return [{
        "addDimensionGroup": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": start,
                "endIndex": end
            }
        }
    }]


def expand_group(sheet, spreadsheet_id, sheet_id, start, end):
    _update_collapse_group(sheet, spreadsheet_id, sheet_id, start, end, False)


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


def set_update_time_in_cell(sheet, sheet_id, cell):

    datetime_madrid = datetime.now(pytz.timezone('Europe/Madrid'))
    values = [
        [
            datetime_madrid.strftime("Last update: %m/%d/%Y at %H:%M:%S %Z")
        ]
    ]
    body = {
        'values': values
    }
    sheet.values().update(
        spreadsheetId=sheet_id, range=cell,
        valueInputOption='USER_ENTERED', body=body).execute()
