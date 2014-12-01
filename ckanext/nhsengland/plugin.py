import routes.mapper
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base


class NHSEnglandPlugin(plugins.SingletonPlugin):
    """
    Mainly theme related "stuff".
    """

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'nhsengland')

    def before_map(self, route_map):
        """
        Adds "howto" static pages (and maybe others at a later date).
        """
        with routes.mapper.SubMapper(route_map,
            controller='ckanext.nhsengland.plugin:NHSEController') as m:
            m.connect('howto', '/howto', action='howto')
        return route_map

    def after_map(self, route_map):
        return route_map


class NHSEController(base.BaseController):
    """
    Methods for displaying custom static pages (see names of methods for hint).

    :-)
    """

    def howto(self):
        return base.render('howto.html')
