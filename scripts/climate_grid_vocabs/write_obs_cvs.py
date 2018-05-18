#!/usr/bin/env python

"""
write_obs_cvs.py
================

Writes JSON CV files from the `config_tables.xls` vocabs from Climate-Grid package.

"""

# Third-party imports
import pandas
import simplejson
import numpy

CONFIG_XLS = 'config_tables.xls'
json_tmpl = {
    "version_metadata":{
        "author":"Ag Stephens <ag.stephens@stfc.ac.uk>",
        "creation_date":"Tue Jun 06 07:45:06 2017 -0100",
        "institution_id":"STFC",
        "previous_commit":""
    }
}

sheet_map = {'CF_metadata': ('variables', 'short_name'),
             'grid_properties': ('grid_properties', 'grid_name'),
             'projected_crs': ('projected_crs', 'epsg'), 
             'geographic_crs': ('geographic_crs', 'epsg')}


def _serialise(name, content):
    output_path = "../../UKCP18_obs_{}.json".format(name)
    resp = json_tmpl.copy()
    resp[name] = content

    with open(output_path, 'w') as writer:
        simplejson.dump(resp, writer, indent=4, sort_keys=True)

    print "Wrote: {}".format(output_path)


def write_json(sheet, name, key_name):
    df = pandas.read_excel(CONFIG_XLS, sheetname=sheet, na_values="")
    t = df.T # transposed
    variables = {}

    for i in range(t.shape[1]):
        data = dict(t[i])
        d = {}
    
        for key, value in data.items():
            if pandas.isnull(value): value = ""
            d[key] = value

        sn = d[key_name]

        if sn:
            variables[sn] = d.copy()

    _serialise(name, variables)


def main():
    for sheet, (name, key_name) in sheet_map.items():
        write_json(sheet, name, key_name)

if __name__ == "__main__":

    main()

