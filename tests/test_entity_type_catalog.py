import json

import pytest

from seed_runtime.entity_type_catalog import EntityTypeCatalog


def test_builtin_entity_type_catalog_contains_initial_types():
    catalog = EntityTypeCatalog.load()

    assert {entry.entity_type for entry in catalog.list_entity_types()} == {
        "host",
        "service",
        "group",
        "endpoint",
        "monitoring_system",
        "capability",
        "unknown",
    }


def test_entity_type_catalog_requires_unknown(tmp_path):
    path = tmp_path / "entity-types.json"
    path.write_text(json.dumps({"entity_types": [{"entity_type": "host"}]}))

    with pytest.raises(ValueError, match="must define 'unknown'"):
        EntityTypeCatalog.load(path)
