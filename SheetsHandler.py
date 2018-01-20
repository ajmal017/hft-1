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
        self.spreadsheetId = '1JjWDWq0KVE2Jq2hl9WmmZE2VkeHxvpsbi2jmaiH0vhE'
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

    def check_and_build_sheets(self,data):
        pairs = []
        for x in data:
            pairs.append(x)

        sheet_info = self.get_spreadsheet_info()

        sheets = []
        for sheet in sheet_info['sheets']:
            sheets.append(sheet['properties']['title'])

        sheets = [x for x in pairs if x not in list(set(sheets).intersection(pairs))]

        # print sheets

        self.add_sheets(sheets)

    def batch_update(self,body):

        return self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body).execute()

    def insert_empty_rows(self,pairs):

        sheet_info = self.get_spreadsheet_info()

        for y in pairs:
            for x in sheet_info['sheets']:
                if x['properties']['title'] == y[0]:
                    y.append(x['properties']['sheetId'])

        body = {
            "requests": []
        }

        for pair in pairs:

            query = {
                "insertDimension": {
                    "range": {
                        "sheetId": pair[1],
                        "dimension": "ROWS",
                        "startIndex": 0,
                        "endIndex": 1
                    }
                }
            }

            body["requests"].append(query)
        
        # self.batch_update(body)

    def write_data(self,prices):

        body = {
            'valueInputOption':'USER_ENTERED',
            'data': []
        }

        for p in prices:

            data = {
              "range": p[0]+"!A1",
              # "majorDimension": "COLUMNS",
              "values": [
                [p[1],p[2]]
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
                                "rowCount": 20,
                                "columnCount": 2
                              }
                            }
                          }
                        }
                    ],
                }
            
            print self.batch_update(body)

        else:

            print "No new sheets"
