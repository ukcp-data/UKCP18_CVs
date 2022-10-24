from setuptools import setup, find_packages

from ukcp_cv import __version__


def readme():
    with open('README.md') as f:
        return f.read()


reqs = [line.strip() for line in open('requirements.txt')]


GIT_REPO = "https://github.com/ukcp-data/UKCP18_CVs"

setup(
    name                 = "ukcp-controlled-vocabularies",
    version              = __version__,
    description          = "Python library for reading UKCP controlled vocabularies .",
    long_description     = readme(),
    license              = "",
    author               = "Ag Stephens",
    author_email         = "ag.stephens@stfc.ac.uk",
    url                  = GIT_REPO,
    packages             = find_packages(),
    install_requires     = reqs,
    tests_require        = ['pytest'],
    classifiers          = [
        'Development Status :: 2 - ???',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: ???',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    include_package_data = True,
    scripts=[],
    entry_points = {},
    package_data = {'': [
            '../UKCP18_CVs/UKCP18_activity_id.json',
            '../UKCP18_CVs/UKCP18_admin_region.json',
            '../UKCP18_CVs/UKCP18_baseline_period.json',
            '../UKCP18_CVs/UKCP18_climate_change_type.json',
            '../UKCP18_CVs/UKCP18_collection.json',
            '../UKCP18_CVs/UKCP18_coordinate.json',
            '../UKCP18_CVs/UKCP18_country.json',
            '../UKCP18_CVs/UKCP18_domain.json',
            '../UKCP18_CVs/UKCP18_ensemble_group.json',
            '../UKCP18_CVs/UKCP18_ensemble_member.json',
            '../UKCP18_CVs/UKCP18_ensemble_short_name.json',
            '../UKCP18_CVs/UKCP18_frequency.json',
            '../UKCP18_CVs/UKCP18_institution_id.json',
            '../UKCP18_CVs/UKCP18_license.json',
            '../UKCP18_CVs/UKCP18_marine_input_model.json',
            '../UKCP18_CVs/UKCP18_prob_data_type.json',
            '../UKCP18_CVs/UKCP18_projection.json',
            '../UKCP18_CVs/UKCP18_project.json',
            '../UKCP18_CVs/UKCP18_resolution.json',
            '../UKCP18_CVs/UKCP18_river_basin.json',
            '../UKCP18_CVs/UKCP18_scenario.json',
            '../UKCP18_CVs/UKCP18_time_slice_20y.json',
            '../UKCP18_CVs/UKCP18_time_slice_30y.json',
            '../UKCP18_CVs/UKCP18_time_slice_type.json',
            '../UKCP18_CVs/UKCP18_variable.json'
            ]}
)
