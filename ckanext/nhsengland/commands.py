# -*- coding: utf-8 -*-
"""
"""
import logging
import sys

from ckan.logic import NotFound
from ckan.lib.cli import CkanCommand
from ckanapi import LocalCKAN

class ZapCommand(CkanCommand):
    """
    Zaps a publisher and all of its datasets

    Purges the supplied organization and all of its datasets so that
    the organization name can be re-used.
    """
    summary = "Zaps a publisher and all of its datasets"
    usage = __doc__
    max_args = 1
    min_args = 1

    def __init__(self, name):
        super(ZapCommand, self).__init__(name)

    def command(self):
        self._load_config()

        import ckan.model as model
        model.Session.remove()
        model.Session.configure(bind=model.meta.engine)

        group = model.Group.get(self.args[0])
        packages = model.Session.query(model.Package).filter(model.Package.owner_org==group.id)
        package_count = packages.count()
        print "Found {} packages to delete".format(package_count)

        if package_count:
            for package in packages:
                package.purge()
                print "Purged dataset '{}'".format(package.name)
            model.Session.commit()

        group.purge()
        model.Session.commit()


class ForceDatastoreCommand(CkanCommand):
    """
    Forces the reloading of datastore tables.

    This is for either all resources, or a single resource whose
    id is specified as an argument
    """
    summary = "Forces the reloading of datastore tables."
    usage = __doc__
    max_args = 1
    min_args = 0

    def __init__(self, name):
        super(ForceDatastoreCommand, self).__init__(name)

    def command(self):
        self._load_config()

        import ckan.model as model
        model.Session.remove()
        model.Session.configure(bind=model.meta.engine)

        self.ckan = LocalCKAN()

        if len(self.args) == 1:
            self.force_resource(self.args[0])
            return

        # Going to re-process everything - this may:
        #   1. Take some time
        #   2. Put some pressure on the queue
        resources = model.Session.query(model.Resource).all()
        for resource in resources:
            self.force_resource(resource.id)


    def force_resource(self, id):
        """
        Forces a single resource to delete the datastore table and
        reload the data from the resource url.
        """
        import ckan.model as model

        resource = model.Resource.get(id)
        if not resource:
            print "Could not find resource {}".format(id)
            return

        print "Processing resource '{}' [{}]".format(resource.name, id)

        try:
            self.ckan.action.datastore_delete(resource_id=id, force=True)
            print " + Datastore table deleted"
        except NotFound:
            print " - No datastore table found"

        success = self.ckan.action.datapusher_submit(resource_id=id, ignore_hash=True)
        print " + Job submitted to datapusher: {}".format(success)
