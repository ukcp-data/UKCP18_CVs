from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-ukcp18.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = '../client_secret.json'
APPLICATION_NAME = 'Write UKCP18 variables from google sheets'


def get_credentials():
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
                                   'sheets.googleapis.com-ukcp18.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_spreadsheet():
    """
    Creates a Sheets API service object and gets the contents of the
    spreadsheet.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1Ij3R3skvYhKnMSqXB6KHaxH0BSST5R0DI8zp2Qi82vw'
    rangeName = 'Climate_variables!A2:R'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    return result.get('values', [])


def make_dict_from_sheet(spreadsheet):
    """
    Group rows by variable id.

    @return a dict where
                key = variable id
                value = list of matching rows
    """
    id_column = 0
    data = {}
    for row in spreadsheet:
        if row[id_column] in data.keys():
            data[row[id_column]].append(row)
        else:
            data[row[id_column]] = [row]
    return data


def process_data(data):
    """
    Create a data structure to represent a variable

    @return a dict
    """
    variable = {}
    strand = set()
    time_step = set()
    time_averaging = set()
    notes = set()
    cmip6_cmor_tables_row_id = set()

    for row in data:
        if variable == {}:
            # these fields are common to all the rows for a variable
            variable['name'] = row[1]
            if row[11] != "":
                variable['um_stash'] = row[11]
            if row[12] != "" and row[12] != "None":
                variable['standard_name'] = row[12]
            if row[13] != "":
                variable['units'] = row[13]
            try:
                if row[14] != "" and row[14] != "None":
                    variable['cmip6_name'] = row[14]
                if row[15] != ""and row[15] != "None":
                    variable['cmip6_standard_name'] = row[15]
            except IndexError:
                pass

        # now sort out the differences between rows
        if row[2] != "":
            time_step.add(row[2])
        if row[3] != "":
            time_averaging.add(row[3])
        if row[10] != "":
            notes.add(row[10])

        try:
            if row[16] != "" and row[16] != "None":
                cmip6_cmor_tables_row_id.add(row[16])
        except IndexError:
            pass

        if row[4] is not None:
            strand.add('observations')
        if row[5] is not None:
            strand.add('marine')
        if row[6] is not None:
            strand.add('land strand 1')
        if row[7] is not None:
            strand.add('land strand 2')
        if row[8] is not None:
            strand.add('land strand 3 12km')
        if row[9] is not None:
            strand.add('land strand 3 2km')

    if len(time_step) > 0:
        variable['time_step'] = sorted(list(time_step))
    if len(time_averaging) > 0:
        variable['time_averaging'] = sorted(list(time_averaging))
    if len(strand) > 0:
        variable['strand'] = sorted(list(strand))
    if len(notes) > 0:
        variable['notes'] = sorted(list(notes))
    if len(cmip6_cmor_tables_row_id) > 0:
        variable['cmip6_cmor_tables_row_id'] = sorted(
            list(cmip6_cmor_tables_row_id))

    return variable


def main():
    spreadsheet = get_spreadsheet()
    variables = {}
    data = make_dict_from_sheet(spreadsheet)
    for key in data.keys():
        variables[key] = process_data(data[key])

    output = {'variable': variables}

    with open('../UKCP18_variable.json', 'w') as the_file:
        the_file.write(json.dumps(output, sort_keys=True,
                                  indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()
