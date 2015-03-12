from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-nhsengland',
    version=version,
    description="Modifications to CKAN required specifically by NHSEngland.",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='IIT Team NHSEngland',
    author_email='nhsenglandiit2@googlegroups.com',
    url='http://www.england.nhs.uk/',
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.nhsengland'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pylibmc==1.4.1"
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        nhsengland_skin=ckanext.nhsengland.plugin:NHSEnglandPlugin

        [paste.paster_command]
        zap = ckanext.nhsengland.commands:ZapCommand
    ''',
)
