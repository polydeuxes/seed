from datetime import datetime, timezone
import json

from seed_runtime.capability_candidates import build_capability_candidates
from seed_runtime.capability_catalog import CapabilityCatalog, CapabilityCatalogEntry, CapabilityRecommendation
from seed_runtime.evidence import Evidence
from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.single_capability_state_projection import (
    build_single_capability_state_projection,
    format_single_capability_state_projection,
    single_capability_state_projection_json,
)
from seed_runtime.state import StateProjector
from seed_runtime.verification_evidence import build_verification_evidence

from test_seed_local_script import load_seed_local_module

BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _project(ledger):
    return StateProjector(ledger).project("ws")


def _package_fact(package="python3"):
    return Fact(id=f"fact_{package}", subject_id="localhost", predicate="package_installed", value=package, evidence_ids=[f"evd_{package}"], observed_at=BASE_TIME, source_type="discovery")


def _ledger():
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact())})
    return ledger


def _catalog():
    return CapabilityCatalog([CapabilityCatalogEntry(capability="python_runtime", summary="Python", recommendations=[CapabilityRecommendation(provider="manual", summary="advisory only")])])


def _projection(ledger=None, *, path_env=""):
    ledger = ledger or _ledger()
    state = _project(ledger)
    candidates = build_capability_candidates(state, filter_text="python_runtime")
    evidence = build_verification_evidence(state, filter_text="python_runtime", path_env=path_env, candidate_inspection=candidates)
    return build_single_capability_state_projection(state, "Python Runtime", catalog=_catalog(), candidate_inspection=candidates, verification_evidence_inspection=evidence), state, ledger


def test_projection_normalizes_and_exposes_boundaries_without_selection():
    projection, state, ledger = _projection()

    assert projection.capability_name == "python_runtime"
    assert projection.catalog_known is True
    assert projection.provider_recommendations[0].provider == "manual"
    assert projection.registered_operations == []
    assert projection.candidate_evidence[0].candidate == "python_runtime"
    assert projection.verification_evidence == []
    assert "same_normalized_string_correlation_only" in projection.boundary_notes
    assert "no_provider_selection" in projection.boundary_notes
    assert "no_operation_selection" in projection.boundary_notes
    assert not hasattr(state, "pending_" + "actions")
    assert not hasattr(state, "action_" + "plans")
    before = [event.id for event in ledger.list_events("ws")]
    single_capability_state_projection_json(projection)
    format_single_capability_state_projection(projection)
    assert [event.id for event in ledger.list_events("ws")] == before


def test_absent_candidate_and_verification_evidence_are_not_absence_or_failure():
    ledger = EventLedger()
    state = _project(ledger)
    candidates = build_capability_candidates(state, filter_text="python_runtime")
    evidence = build_verification_evidence(state, filter_text="python_runtime", path_env="", candidate_inspection=candidates)

    projection = build_single_capability_state_projection(
        state,
        "Python Runtime",
        catalog=_catalog(),
        candidate_inspection=candidates,
        verification_evidence_inspection=evidence,
    )
    rendered = format_single_capability_state_projection(projection)

    assert projection.candidate_evidence == []
    assert projection.verification_evidence == []
    assert "empty is not capability absence" in rendered
    assert "empty is not verification failure" in rendered


def test_json_shape_is_stable_and_typed():
    projection, _, _ = _projection()
    payload = single_capability_state_projection_json(projection)

    assert list(payload) == [
        "capability_name", "catalog_known", "provider_recommendations",
        "registered_operations", "candidate_evidence", "verification_evidence",
        "unknowns",
        "boundary_notes", "read_only", "writes_event_ledger", "mutates_cluster",
    ]
    assert payload["provider_recommendations"][0]["provider"] == "manual"
    assert payload["registered_operations"] == []
    assert payload["read_only"] is True
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False


def test_missing_owner_artifacts_are_preserved_as_unknowns():
    state = _project(EventLedger())
    projection = build_single_capability_state_projection(state, "Python Runtime")

    assert projection.catalog_known == "unknown"
    assert "catalog_owner_artifact_missing" in projection.unknowns
    assert "candidate_inspection_owner_artifact_missing" in projection.unknowns
    assert "verification_evidence_owner_artifact_missing" in projection.unknowns


def test_cli_human_and_json_are_read_only(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.jsonl"

    assert seed_local.main(["--db", str(db_path), "--single-capability-state", "Python Runtime"]) == 0
    human = capsys.readouterr().out
    assert "same normalized string correlation only" in human
    before = db_path.read_bytes() if db_path.exists() else b""

    assert seed_local.main(["--db", str(db_path), "--single-capability-state", "Python Runtime", "--json"]) == 0
    output = capsys.readouterr().out
    payload = json.loads(output[output.index("{"):])
    assert payload["capability_name"] == "python_runtime"
    assert payload["read_only"] is True
    assert (db_path.read_bytes() if db_path.exists() else b"") == before
