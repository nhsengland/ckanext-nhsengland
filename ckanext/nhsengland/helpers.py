import ckan.logic as logic
from ckan.lib.helpers import _create_url_with_params
from ckan.plugins.toolkit import request


def split_resources(pkg_dict):
    """
    Splits the resources in the provided package based on the format field
    with DOC, DOCX, PDF being returned as documents, all other formats as data
    """
    document_formats = ["DOC", "DOCX", "PDF"]
    documents, data = [], []
    for resource in pkg_dict["resources"]:
        target = documents if resource.get("format", "").upper() in document_formats \
                           else data
        target.append(resource)
    return documents, data


def get_collection(name):
    if name is None:
        return {}
    try:
        return logic.get_action('group_show')({}, {'id': name})
    except (logic.NotFound, logic.ValidationError, logic.NotAuthorized):
        return {}

def get_extras(extras):
    return {i['key']:i['value'] for i in extras}


def is_archived(tags):
    return any(t['name'] == 'archived' for t in tags)


def archived_on(extras):
    for extra in extras:
        if extra['key'] == 'date_archived':
            return extra['value']

    return False


def remove_archived_marker(facets):
    try:
        del facets['include_archives']
    except KeyError:
        pass

    return facets


def toggle_archives_url():
    key = 'include_archives'

    if key in request.params:
        params = [p for p in request.params.items() if p[0] != key]
    else:
        params = [p for p in request.params.items()]
        params.append((key, True))

    return _create_url_with_params(params=params)
