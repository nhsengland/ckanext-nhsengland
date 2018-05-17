import routes.mapper
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base
import copy
import datetime
import time


def convert_to_extras(key, data, errors, context):
    """
    Rewrite of the same-named function in ckan.logic.converters that is
    accurately wrong. I've submitted a bug/fix to CKAN so this function can
    probably be removed at some later date, if/when the patch is merged.
    """
    # There is no tally for the number of fields converted to extras.
    extras = [k for k in data.keys() if k[0] == 'extras' and len(k) > 1]
    new_pos = 0
    if extras:
        extras.sort()
        new_pos = extras[-1][-2] + 1  # e.g. ('extras', 5, 'value')
    data[('extras', new_pos, 'key')] = key[-1]
    data[('extras', new_pos, 'value')] = data[key]


def is_date(value):
    """
    Ensures that the passed in value is a valid date expressed as YYYY-MM-DD.
    """
    date = value.strip()
    if date:
        try:
            checked_date = datetime.date(*time.strptime(date, '%Y-%m-%d')[:3])
        except:
            raise toolkit.Invalid("Not a valid date. Must be YYYY-MM-DD.")
    return date


def create_frequencies():
    """
    Defines the choices for publication frequency associated with a dataset:

    Hourly, Daily, Weekly, Monthly, Quarterly, Annually, Other
    """
    frequencies = [
        u'Hourly',
        u'Daily',
        u'Weekly',
        u'Monthly',
        u'Quarterly',
        u'Annually',
        u'Other',
    ]
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'frequency'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'frequency'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in frequencies:
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)


def frequencies():
    """
    Returns a list of tags representing valid publication frequencies.
    """
    create_frequencies()
    try:
        tag_list = toolkit.get_action('tag_list')
        frequencies = tag_list(data_dict={'vocabulary_id': 'frequency'})
        return frequencies
    except toolkit.ObjectNotFound:
        return None


class NHSEnglandPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    """
    Mainly theme related "stuff".

    The customisation of dataset metadata was implemented in line with this
    tutorial:

    http://docs.ckan.org/en/latest/extensions/adding-custom-fields.html#customizing-dataset-and-resource-metadata-fields-using-idatasetform

    The additional metadata fields are:

    Coverage start date
    Coverage end date
    Origin
    Frequency
    Homepage

    Should we need more, it is relatively easy to add them.
    """

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController)

    def get_helpers(self):
        from ckanext.nhsengland.helpers import (
            archived_on, get_collection, get_extras, is_archived,
            remove_archived_marker, split_resources, toggle_archives_url,
            dataset_search
        )
        return {
            'archived_on': archived_on,
            'frequencies': frequencies,
            'get_collection': get_collection,
            'get_extras': get_extras,
            'is_archived': is_archived,
            'remove_archived_marker': remove_archived_marker,
            'split_resources': split_resources,
            'toggle_archives_url': toggle_archives_url,
            'dataset_search': dataset_search
        }

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
            m.connect('boardreport', '/boardreport', action='boardreport')
            m.connect('howto', '/howto', action='howto')
        return route_map

    def after_map(self, route_map):
        return route_map

    def _modify_package_schema(self, schema):
        """
        Adds fields and validators to the schema.
        """
        schema.update({
            'coverage_start_date': [toolkit.get_validator('ignore_missing'),
                                    is_date,
                                    convert_to_extras, ],
            'coverage_end_date': [toolkit.get_validator('ignore_missing'),
                                  is_date,
                                  convert_to_extras, ],
            'origin': [toolkit.get_validator('ignore_missing'),
                       convert_to_extras, ],
            'frequency': [toolkit.get_validator('ignore_missing'),
                          toolkit.get_converter('convert_to_tags')
                                               ('frequency'), ],
            'homepage': [toolkit.get_validator('ignore_missing'),
                         convert_to_extras, ],
            'directoryprojectlink': [toolkit.get_validator('ignore_missing'),
                         convert_to_extras, ],
            'directoryprojectname': [toolkit.get_validator('ignore_missing'),
                         convert_to_extras, ],
        })
        return schema

    def create_package_schema(self):
        schema = super(NHSEnglandPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(NHSEnglandPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(NHSEnglandPlugin, self).show_package_schema()
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'coverage_start_date': [toolkit.get_converter('convert_from_extras'),
                           toolkit.get_validator('ignore_missing'), ],
            'coverage_end_date': [toolkit.get_converter('convert_from_extras'),
                         toolkit.get_validator('ignore_missing'), ],
            'origin': [toolkit.get_converter('convert_from_extras'),
                       toolkit.get_validator('ignore_missing'), ],
            'frequency': [toolkit.get_converter('convert_from_tags')
                                               ('frequency'),
                          toolkit.get_validator('ignore_missing'), ],
            'homepage': [toolkit.get_converter('convert_from_extras'),
                         toolkit.get_validator('ignore_missing'), ],
            'directoryprojectlink': [toolkit.get_converter('convert_from_extras'),
                         toolkit.get_validator('ignore_missing'), ],
            'directoryprojectname': [toolkit.get_converter('convert_from_extras'),
                                     toolkit.get_validator('ignore_missing'), ],
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def after_create(self, context, pkg_dict):
        return pkg_dict

    def after_delete(self, context, pkg_dict):
        return pkg_dict

    def after_search(self, search_results, search_params):
        return search_results

    def after_show(self, context, pkg_dict):
        return pkg_dict

    def after_update(self, context, pkg_dict):
        return pkg_dict

    def before_index(self, pkg_dict):
        return pkg_dict

    def _get_archived_params(self, q):
        hide_archives = 'NOT tags:archived'
        if q is None:
            return hide_archives

        if hide_archives not in q:
            return hide_archives if q == '' else '{} {}'.format(q, hide_archives)

        if q.startswith(hide_archives) or q.endswith(hide_archives):
            return q.replace(hide_archives, '').strip(' ')

        before, _, after = q.partition(hide_archives + ' ')
        return before + after

    def before_search(self, search_params):
        include_archives = toolkit.request.params.get('include_archives')
        if include_archives:
            # Remove our include_archives param from the full query string.
            # This is added by CKAN because we added to the GET params.
            fq = search_params.get('fq', '')
            new_params = copy.deepcopy(search_params)
            new_params['fq'] = fq.replace('include_archives:"True" ', '')
            return new_params

        # Generate new search params with a modified q key including our
        # archived tag filter.
        new_params = copy.deepcopy(search_params)
        new_params['q'] = self._get_archived_params(search_params.get('q'))
        return new_params

    def before_view(self, pkg_dict):
        return pkg_dict

    def create(self, entity):
        return entity

    def delete(self, entity):
        return entity

    def edit(self, entity):
        return entity

    def read(self, entity):
        return entity


class NHSEController(base.BaseController):
    """
    Methods for displaying custom static pages (see names of methods for hint).

    :-)
    """

    def howto(self):
        return base.render('howto.html')

    def boardreport(self):
        return base.render('boardreport.html')
