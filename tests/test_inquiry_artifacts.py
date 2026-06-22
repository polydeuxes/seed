import json

import scripts.seed_local as seed_local
from seed_runtime.inquiry_artifacts import (
    build_inquiry_artifacts,
    inquiry_artifacts_json,
)
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit


def _artifact(payload, name):
    return next(item for item in payload["artifacts"] if item["artifact"] == name)


def test_cli_inquiry_artifacts_human_readable(capsys):
    assert seed_local.main(["--inquiry-artifacts"]) == 0

    output = capsys.readouterr().out

    assert "Inquiry Artifacts Visibility" in output
    assert "unknown: repository_visible" in output
    assert "boundary: repository_visible" in output
    assert "pressure: partially_visible" in output
    assert "read only" in output
    assert "no pressure transformation inference" in output
    assert "no inquiry graph creation" in output


def test_cli_inquiry_artifacts_json_valid(capsys):
    assert seed_local.main(["--inquiry-artifacts", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert set(payload) == {"artifacts", "boundary"}
    assert _artifact(payload, "unknown")["classification"] == "repository_visible"
    assert payload["boundary"]["read_only"] is True


def test_expected_artifact_visibility_classifications_are_conservative():
    payload = inquiry_artifacts_json(build_inquiry_artifacts())

    assert _artifact(payload, "unknown")["classification"] == "repository_visible"
    assert _artifact(payload, "boundary")["classification"] == "repository_visible"
    assert _artifact(payload, "pressure")["classification"] == "partially_visible"
    assert (
        _artifact(payload, "supported_conclusion")["classification"]
        == "document_visible"
    )
    assert (
        _artifact(payload, "unsupported_conclusion")["classification"]
        == "document_visible"
    )
    assert _artifact(payload, "open_question")["classification"] == "document_visible"
    assert _artifact(payload, "gap")["classification"] == "partially_visible"


def test_inquiry_artifacts_boundary_prevents_inference_and_mutation():
    payload = inquiry_artifacts_json(build_inquiry_artifacts())
    boundary = payload["boundary"]

    assert boundary["read_only"] is True
    assert boundary["supports_record"] is False
    assert boundary["writes_event_ledger"] is False
    assert boundary["mutates_cluster"] is False
    assert boundary["infers_pressure_transformation"] is False
    assert boundary["infers_inquiry_movement"] is False
    assert boundary["creates_inquiry_graph"] is False
    assert boundary["performs_workflow_or_planning"] is False


def test_inquiry_artifacts_registered_in_diagnostic_inventory():
    entry = next(
        entry for entry in DIAGNOSTIC_INVENTORY if entry.name == "inquiry_artifacts"
    )

    assert entry.cli_flags == ("--inquiry-artifacts",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False


def test_inquiry_artifacts_checked_by_diagnostic_shape_audit():
    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "inquiry_artifacts"
    ]

    assert rows
    assert [row for row in rows if row.status == "mismatch"] == []
    assert any(row.field == "supports_json" and row.observed is True for row in rows)
