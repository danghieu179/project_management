from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json


class GoogleAPI(object):
    def __init__(self, credentials=None):
        self.credentials = credentials

    def call_the_sheets_api(self):
        # Load credentials from the session.
        credentials = Credentials(**self.credentials)
        service = build('sheets', 'v4', credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()
        return sheet

    def get_data(self, sheet, spreadsheetId, sheetsrange):
        try:
            result = sheet.values().get(
                spreadsheetId=spreadsheetId, range=sheetsrange).execute()
            return 200, result
        except HttpError as err:
            if err.resp.get('content-type', '').startswith('application/json'):
                reason = json.loads(err.content).get('error').get('message')
                return err.resp.status, reason
