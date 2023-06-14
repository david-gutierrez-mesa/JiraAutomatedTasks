from __future__ import print_function

import os.path
from os.path import expanduser, abspath
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from liferay.utils.sheets.sheets_constants import SheetInstance


def get_testmap_connection():
    home = Path(expanduser("~"))
    folder = home / ".testmap_user"
    credentials_file = folder / "credentials.json"
    token_file = "../../token.json"
    creds = None
    if os.path.exists('../../token.json'):
        creds = Credentials.from_authorized_user_file(abspath(token_file), SheetInstance.SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                abspath(credentials_file), SheetInstance.SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        return sheet
    except HttpError as err:
        print(err)
