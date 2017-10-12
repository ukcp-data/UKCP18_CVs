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
    Group rows by variable name.

    @return a dict where
                key = variable name
                value = list of matching rows
    """
    data = {}
    for row in spreadsheet:
        if row[1] in data.keys():
            data[row[1]].append(row)
        else:
            data[row[1]] = [row]
    return data


def get_id(name):
    """
    Make an id from the name.

    @return a string containing the id
    """
    id_ = name.replace(' ', '_')
    id_ = id_.replace('.', '')
    id_ = id_.replace('(', '')
    id_ = id_.replace(')', '')
    id_ = id_.lower()
    return id_


def process_data(data):
    """
    Create a data structure to represent a variable

    @return a dict
    """
    variable = {}

    for row in data:
        if variable == {}:
            # these fields are common to all the rows for a variable
            variable['name'] = row[1]
            variable['um_stash'] = row[11]
            variable['standard_name'] = row[12]
            variable['units'] = row[13]
            variable['subset'] = []

        # now sort out the differences between rows
        subset = {}
        try:
            subset['time_step'] = row[2]
            subset['time_averaging'] = row[3]
            subset['notes'] = row[10]
            subset['cmip6_name'] = row[14]
            subset['cmip6_standard_name'] = row[15]
        except IndexError:
            pass

        subset['strand'] = []
        if row[4] is not None:
            subset['strand'].append('observations')
        if row[5] is not None:
            subset['strand'].append('marine')
        if row[6] is not None:
            subset['strand'].append('land strand 1')
        if row[7] is not None:
            subset['strand'].append('land strand 2')
        if row[8] is not None:
            subset['strand'].append('land strand 3 12km')
        if row[9] is not None:
            subset['strand'].append('land strand 3 2km')

        variable['subset'].append(subset)

    return variable


def main():
    spreadsheet = get_spreadsheet()
    variables = {}
    data = make_dict_from_sheet(spreadsheet)
    for key in data.keys():
        id_ = get_id(key)
        variables[id_] = process_data(data[key])

    output = {'variable': variables}

    with open('../UKCP18_variable.json', 'w') as the_file:
        the_file.write(json.dumps(output, sort_keys=True,
                                  indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()
