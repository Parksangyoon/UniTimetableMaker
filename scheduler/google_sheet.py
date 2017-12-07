import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_sheet(sheet_name, tab_name):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('google_sheet_keyfile.json', scope)
    client = gspread.authorize(credentials)

    return client.open(sheet_name).worksheet(tab_name)
