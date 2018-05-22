import json
from os import path


def enum(**named_values):
    return type('Enum', (), named_values)


CV_Type = enum(ACTIVITY_ID='activity_id',
               ADMIN_REGION='admin_region',
               COLLECTION='collection',
               COORDINATE='coordinate',
               COUNTRY='country',
               DATASET_ID='dataset_id',
               DOMAIN='domain',
               ENSEMBLE_MEMBER='ensemble_member',
               EXPERIMENT_ID='experiment_id',
               FREQUENCY='frequency',
               INSTITUTION_ID='institution_id',
               LICENSE='license',
               MARINE_INPUT_MODEL='marine_input_model',
               OBS_GEAGRAPHIC_CRS='obs_geographic_crs',
               OBS_GRID_PROPERTIES='obs_grid_properties',
               OBS_PROJECTED_CRS='obs_projected_crs',
               OBS_VARIABLES='obs_variables',
               PROB_DATA_TYPE='prob_data_type',
               PROJECT='project',
               PROJECTION='projection',
               RESOLUTION='resolution',
               RIVER_BASIN='river_basin',
               SCENARIO='scenario',
               VARIABLE='variable',
               )


def get_cv(cv_type):
    """
    Get a json representation of the CV.

    @param cv_type(CV_Type): the CV of interest

    @return a json object containing details of the CV
    """
    if not _is_cv_type(cv_type):
        raise ValueError('Invalid CV_Type: {}'.format(cv_type))
    file_name = 'UKCP18_{}.json'.format(cv_type)
    cv_file = path.join('../UKCP18_CVs', file_name)
    with open(cv_file) as json_data:
        cvs = json.load(json_data)
    return cvs


def _is_cv_type(cv_type):
    for key in CV_Type.__dict__.keys():
        if '__' not in key:
            if cv_type == CV_Type.__dict__[key]:
                return True
    return False


if __name__ == '__main__':
    print get_cv(CV_Type.ADMIN_REGION)

    for key in CV_Type.__dict__.keys():
        if '__' not in key:
            print key
            print get_cv(CV_Type.__dict__[key])

    print get_cv('junk')
