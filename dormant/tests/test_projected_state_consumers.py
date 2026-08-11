import json

import scripts.seed_local as seed_local
from seed_runtime.projected_state_consumers import build_projected_state_consumers


def _row(surface: str):
    return next(row for row in build_projected_state_consumers() if row.surface == surface)


def test_cli_projected_state_consumers_renders_human_output(capsys):
    assert seed_local.main(["--projected-state-consumers"]) == 0

    output = capsys.readouterr().out

    assert "Projected State Consumers" in output
    assert "knowledge_reachability" in output
    assert "  kind: diagnostic" in output
    assert "sources: projected_state, repo_files" in output
    assert "boundary: read_only/no_record/no_mutation" in output


def test_cli_projected_state_consumers_json_renders_stable_json(capsys):
    assert seed_local.main(["--projected-state-consumers", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    by_surface = {row["surface"]: row for row in payload}

    row = by_surface["projected_state_consumers"]
    assert row["cli_flags"] == ["--projected-state-consumers"]
    assert row["consumer_kind"] == "inventory"
    assert row["uses_static_inventory"] is True
    assert row["uses_projected_state"] is False
    assert row["boundary"] == {
        "read_only": True,
        "records": False,
        "writes_event_ledger": False,
        "mutates_cluster": False,
        "executes_observation": False,
        "provider_acquisition": False,
        "permission_creation": False,
    }
    assert row["notes"]


def test_projected_state_consumers_marks_declared_source_classes_only():
    knowledge = _row("knowledge_reachability")
    assert knowledge.uses_projected_state is True
    assert knowledge.uses_repo_files is True
    assert knowledge.uses_static_inventory is False

    diagnostic_shape = _row("diagnostic_shape_audit")
    assert diagnostic_shape.uses_static_inventory is True
    assert diagnostic_shape.uses_projected_state is False

    documentation = _row("documentation_structure")
    assert documentation.uses_repo_files is True
    assert documentation.uses_projected_state is False

    audit_compare = _row("audit_compare")
    assert audit_compare.uses_projected_state is False
    assert audit_compare.uses_repo_files is False


def test_projected_state_consumers_boundary_is_read_only_no_record_no_mutation():
    for row in build_projected_state_consumers():
        assert row.boundary["read_only"] is True
        assert row.boundary["records"] is False
        assert row.boundary["writes_event_ledger"] is False
        assert row.boundary["mutates_cluster"] is False
        assert row.boundary["executes_observation"] is False
        assert row.boundary["provider_acquisition"] is False
        assert row.boundary["permission_creation"] is False
