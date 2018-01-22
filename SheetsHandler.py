import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Trader'

class sheets(object):

    def __init__(self):
        self.spreadsheetId = '1eoHBhm6zubsyIsbB8XHiqRP-qsc-Uf5XF-IsA0R8yUQ'
        self.discovery()

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def discovery(self):

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

    def get_spreadsheet_info(self):

        return self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()

    def check_and_build_sheets(self,p):
        pairs = []

        for x in p:
            pairs.append(x[0])

        sheet_info = self.get_spreadsheet_info()

        sheets = []
        for sheet in sheet_info['sheets']:
            sheets.append(sheet['properties']['title'])

        sheets = [x for x in pairs if x not in list(set(sheets).intersection(pairs))]

        self.add_sheets(sheets)

    def batch_update(self,body):

        return self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body).execute()

    def insert_empty_rows(self):

        sheet_info = self.get_spreadsheet_info()

        sheet_ids = []

        for x in sheet_info['sheets']:
            sheet_ids.append(x['properties']['sheetId'])

        body = {
            "requests": []
        }

        for sheet_id in sheet_ids:

            query = {
                "insertDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "ROWS",
                        "startIndex": 1,
                        "endIndex": 2
                    }
                }
            }

            body["requests"].append(query)

        self.batch_update(body)

    def write_summary_data(self,prices):

        values = [prices]
        range_name = 'Summary!A2'
        body = {
            'values': values
        }

        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()


    def write_detailed_data(self,prices):

        body = {
            'valueInputOption':'USER_ENTERED',
            'data': []
        }

        for p in prices:

            data = {
              "range": p[0]+"!A2",
              "values": [
                p[1:]
              ]
            }

            body["data"].append(data)

        result = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=body).execute()

    def write_summary_headers(self,headers):

        values = [headers]
        range_name = 'Summary!A1'
        body = {
            'values': values
        }

        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        
    def write_detailed_headers(self,pairs):

        body = {
            'valueInputOption':'USER_ENTERED',
            'data': []
        }

        array = ['ts','SellVolume','Volume','SellBaseVolume','LastPrice','TradePairId','High','BidPrice','Low','BuyBaseVolume','Close','BaseVolume','Open','AskPrice','Change','BuyVolume']

        for p in pairs:

            data = {
              "range": p[0]+"!A1",
              # "majorDimension": "COLUMNS",
              "values": [
                array
              ]
            }

            body["data"].append(data)

        result = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=body).execute()

    def add_sheets(self,sheets):

        if len(sheets) > 0:

            for sheet in sheets:

                body = {
                    "requests": [
                        {
                          "addSheet": {
                            "properties": {
                              "title": sheet,
                              "gridProperties": {
                                "rowCount": 2,
                                "columnCount": 2
                              }
                            }
                          }
                        }
                    ],
                }
            
                print self.batch_update(body)

        else:

            return False
