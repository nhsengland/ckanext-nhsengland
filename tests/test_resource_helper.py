
from ckanext.nhsengland.helpers import split_resources

FAKE_PKG = {
    "resources": [
        {"name": "test1", "format": "XLS"},
        {"name": "test2", "format": "XLS"},
        {"name": "test3", "format": "PDF"},
        {"name": "test4", "format": "DOC"},
        {"name": "test5", "format": "DOCX"},
        {"name": "test6", "format": "CSV"},
        {"name": "test7", "format": ""},
        {"name": "test5", "format": "SHP"},
    ]
}

def test_resource_helper():
    documents, data = split_resources(FAKE_PKG)
    assert len(documents) == 3
    assert len(data) == 5

    names = [d["name"] for d in documents]
    assert "test3" in names
    assert "test4" in names
    assert "test5" in names

