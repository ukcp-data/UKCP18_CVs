#!/usr/bin/env python

"""
write_misc_cvs.py
================

Writes JSON Controlled Vocabularies for various UKCP18 terms.

"""

# Third-party imports
import simplejson
from datetime import datetime

# Local variables
now = str(datetime.now())
print now

json_tmpl = {
    "version_metadata":{
        "author":"Ag Stephens <ag.stephens@stfc.ac.uk>",
        "creation_date":now,
        "institution_id":"STFC",
        "previous_commit":""
    }
}


def _serialise(name, content):
    output_path = "UKCP18_{}.json".format(name)
    resp = json_tmpl.copy()
    resp[name] = content

    with open(output_path, 'w') as writer:
        simplejson.dump(resp, writer, indent=4, sort_keys=True)

    print "Wrote: {}".format(output_path)


def write_ensemble_members():
    data = ['r001i1p00000', 'r001i1p00090', 'r001i1p00605', 'r001i1p00834', 
            'r001i1p01113', 'r001i1p01554', 'r001i1p01649', 'r001i1p01843', 
            'r001i1p01935', 'r001i1p02089', 'r001i1p02123', 'r001i1p02242', 
            'r001i1p02305', 'r001i1p02335', 'r001i1p02491', 'r001i1p02753', 
            'r001i1p02832', 'r001i1p02868', 'r001i1p02884', 'r001i1p02914']

    dct = {}
    name = "ensemble_members"

    for key in data:
        dct[key] = key

    _serialise(name, dct)


def main():
    for func in (write_ensemble_members,):
        func()


if __name__ == "__main__":

    main()

