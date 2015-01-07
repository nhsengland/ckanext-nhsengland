# -*- coding: utf-8 -*-
"""
"""
import logging
import sys

from ckan.lib.cli import CkanCommand


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
