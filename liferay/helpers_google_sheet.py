from datetime import datetime

import pytz


def set_update_time_in_cell(sheet, sheet_id, cell):

    datetime_madrid = datetime.now(pytz.timezone('Europe/Madrid'))
    values = [
        [
            datetime_madrid.strftime("Last update: %H:%M:%S %Z")
        ]
    ]
    body = {
        'values': values
    }
    sheet.values().update(
        spreadsheetId=sheet_id, range=cell,
        valueInputOption='USER_ENTERED', body=body).execute()