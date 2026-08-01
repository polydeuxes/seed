import importlib

import pytest

from scripts import seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import IMPLEMENTATION_SPECS


DELETED_FLAGS = (
    "--constitutional-pipeline",
    "--constitutional-pipeline-diagnostic",
    "--constitutional-process",
    "--constitutional-governance",
    "--constitutional-fidelity",
    "--constitutional-view-composition",
    "--operator-inquiry",
    "--inquiry-provenance",
    "--bounded-question",
    "--constitutional-intent",
    "--scope-status",
    "--selection-key",
    "--pipeline-uncertainty",
    "--pipeline-unknown",
    "--composition-purpose",
    "--examination-frontier",
)
DELETED_DIAGNOSTICS = {
    "constitutional_pipeline",
    "constitutional_pipeline_diagnostic",
    "constitutional_process",
    "constitutional_governance",
    "constitutional_fidelity",
    "constitutional_view_composition",
}
DELETED_FRONTIER_MODULES = (
    "seed_runtime.bounded_constitutional_question",
    "seed_runtime.examination_frontier",
)
DELETED_EXAMINATION_STAGING_MODULES = (
    "seed_runtime.candidate_examination_work",
    "seed_runtime.examination_method_applicability",
    "seed_runtime.examination_policy_projection",
    "seed_runtime.examination_work_selection",
    "seed_runtime.examination_probe_request",
)


def test_deleted_static_flags_are_not_parser_options():
    parser = seed_local.build_parser()
    option_strings = {option for action in parser._actions for option in action.option_strings}

    assert option_strings.isdisjoint(DELETED_FLAGS)
    for flag in DELETED_FLAGS:
        with pytest.raises(SystemExit):
            parser.parse_args([flag])


def test_deleted_static_diagnostics_and_frontier_are_absent():
    inventory_names = {entry.name for entry in DIAGNOSTIC_INVENTORY}

    assert inventory_names.isdisjoint(DELETED_DIAGNOSTICS)
    assert DELETED_DIAGNOSTICS.isdisjoint(IMPLEMENTATION_SPECS)
    assert "examination_frontier" not in inventory_names
    assert "examination_frontier" not in IMPLEMENTATION_SPECS


def test_frontier_district_modules_are_absent():
    for module_name in DELETED_FRONTIER_MODULES:
        assert importlib.util.find_spec(module_name) is None


def test_disconnected_examination_staging_modules_are_absent():
    for module_name in DELETED_EXAMINATION_STAGING_MODULES:
        assert importlib.util.find_spec(module_name) is None
