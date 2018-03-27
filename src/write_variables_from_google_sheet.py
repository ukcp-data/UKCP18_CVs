from __future__ import print_function

import argparse
import io
import json
import os

from apiclient import discovery
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


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
    rangeName = 'Climate_variables!A2:X'
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
        if len(row) < 2:
            continue
        
        key = row[id_column].strip()
        if key in data.keys():
            data[key].append(row)
        else:
            data[key] = [row]
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

    col_anomaly_type = 2
    col_time_step = 3
    col_long_name = 4
    col_description = 5
    col_plot_label = 6
    col_standard_name = 7
    col_units = 8
    col_label_units = 9
    col_level = 10
    col_cmip6_var_id = 11
    col_time_averaging = 12
    col_observations = 13
    col_marine = 14
    col_land_strand_1 = 15
    col_land_strand_2 = 16
    col_land_strand_3_12km = 17
    col_land_strand_3_2km = 18
    col_notes = 19
    col_um_stash = 20
    col_cmip6_standard_name = 21
    col_cmip6_cmor_tables_row_id = 22

    for row in data:
        row = [item.strip() for item in row]

        if variable == {}:
            # these fields are common to all the rows for a variable
            variable['long_name'] = row[col_long_name]
            variable['description'] = row[col_description]
            variable['plot_label'] = row[col_plot_label]

            if (row[col_standard_name] != "" and
                    row[col_standard_name] != "None"):
                variable['standard_name'] = row[col_standard_name]
            if (row[col_anomaly_type] != "" and
                    row[col_anomaly_type] != "none"):
                variable['anomaly_type'] = row[col_anomaly_type]
            if row[col_units] != "":
                variable['units'] = row[col_units]
            if row[col_label_units] != "":
                variable['label_units'] = row[col_label_units].encode('utf-8')
            if row[col_level] != "":
                variable['level'] = row[col_level]

            try:
                if (row[col_cmip6_var_id] != "" and
                        row[col_cmip6_var_id] != "None"):
                    variable['cmip6_name'] = row[col_cmip6_var_id]
                if row[col_um_stash] != "":
                    variable['um_stash'] = row[col_um_stash]
                if (row[col_cmip6_standard_name] != "" and
                        row[col_cmip6_standard_name] != "None"):
                    variable['cmip6_standard_name'] = row[col_cmip6_standard_name]
            except IndexError:
                pass

        # now sort out the differences between rows
        if row[col_time_step] != "":
            time_step.add(row[col_time_step])
        if row[col_time_averaging] != "":
            time_averaging.add(row[col_time_averaging])

        try:
            if row[col_observations] is not None:
                strand.add('observations')
            if row[col_marine] is not None:
                strand.add('marine')
            if row[col_land_strand_1] is not None:
                strand.add('land strand 1')
            if row[col_land_strand_2] is not None:
                strand.add('land strand 2')
            if row[col_land_strand_3_12km] is not None:
                strand.add('land strand 3 12km')
            if row[col_land_strand_3_2km] is not None:
                strand.add('land strand 3 2km')

            if row[col_notes] != "":
                notes.add(row[col_notes])

            if (row[col_cmip6_cmor_tables_row_id] != "" and
                    row[col_cmip6_cmor_tables_row_id] != "None"):
                cmip6_cmor_tables_row_id.add(row[col_cmip6_cmor_tables_row_id])
        except IndexError:
            pass

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

    variable_json = '../UKCP18_variable.json'
    with io.open(variable_json, 'w', encoding='utf8') as json_file:
        data = json.dumps(output, sort_keys=True, indent=4,
                          separators=(',', ': '), ensure_ascii=False,
                          encoding='utf8')
        json_file.write(unicode(data))

    print('Wrote new version of: {}'.format(variable_json))


if __name__ == '__main__':
    main()
