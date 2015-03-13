CKANEXT-NHSEngland
------------------

A plugin that modifies a basic CKAN instance to fulfil the following:

* Some simple CSS updates to make a CKAN site look like it belongs to NHSEngland.
* Static pages required by NHSEngland.
* Custom fields for metadata associated with datasets required by NHSEngland.

Installation Instructions
-------------------------

* Activate the CKAN virtualenv
* Clone the repository to /usr/lib/ckan/default/src
* cd into ckanext-nhsengland
* $ python setup.py develop

Configure CKAN:

* Add to ckan.plugins: nhsengland_skin
* Change ckan.site_logo to: /images/nhsengland_logo.png


Resetting the datastore
-------------------------

To reset the datastore you can use the force-datastore paster command.
This command will allow you to force reload on a single resource (if you
provide its ID), or all resources in the system.

Force all resources to reload into datastore

    paster --plugin=ckanext-nhsengland force-datastore -c /etc/ckan/default/production.ini

Force a single resource to reload into datastore

    paster --plugin=ckanext-nhsengland force-datastore <ID> -c /etc/ckan/default/production.ini

**Note** This command only submits the task to the datapusher.