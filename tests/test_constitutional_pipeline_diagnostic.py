import json
from dataclasses import asdict, replace

import scripts.seed_local as seed_local
from seed_runtime.constitutional_pipeline import ConstitutionalPipelineRequest
from seed_runtime.constitutional_pipeline_diagnostic import (
    build_constitutional_pipeline_diagnostic,
    constitutional_pipeline_diagnostic_json,
    format_constitutional_pipeline_diagnostic,
)
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.read_model_ownership import (
    CONSTITUTIONAL_READ_MODEL_CONTRACTS,
    constitutional_read_model_registration,
)


def _request(**overrides):
    values = {
        "operator_inquiry": "Operator says process should be visible; testimony only.",
        "inquiry_provenance": "operator:constitutional-pipeline-diagnostic-test",
        "bounded_question": "Explain explicitly selected constitutional process view.",
        "constitutional_intent": "caller supplied diagnostic inquiry",
        "scope_status": "caller-bounded; not independently verified",
        "uncertainty": ("caller uncertainty preserved",),
        "unknowns": (),
        "caller_supplied_fields": (("selection_key", "process"),),
        "composition_purpose": "diagnostic",
        "output_format": "json",
    }
    values.update(overrides)
    return ConstitutionalPipelineRequest(**values)


def _stage(result, name):
    return next(stage for stage in result.stages if stage.pipeline_stage == name)


def _cli(*extra):
    return [
        "--constitutional-pipeline-diagnostic",
        "--operator-inquiry", "Operator says process should be visible; testimony only.",
        "--inquiry-provenance", "operator:cli-diagnostic-test",
        "--bounded-question", "Explain explicitly selected constitutional process view.",
        "--constitutional-intent", "caller supplied diagnostic inquiry",
        "--scope-status", "caller-bounded; not independently verified",
        *extra,
    ]


def test_diagnostic_observes_real_complete_pipeline_and_successful_composition():
    result = build_constitutional_pipeline_diagnostic(_request())

    assert result.name == "constitutional_pipeline_diagnostic"
    assert result.stage_order == (
        "bounded_question",
        "question_projection",
        "capability_projection",
        "selection",
        "composition_request",
        "composition",
    )
    assert result.selected_views == ("constitutional_process",)
    assert _stage(result, "selection").status == "complete"
    assert _stage(result, "composition").status in {"complete", "unknown"}
    assert result.pipeline_result.selection.selected_view_names == ("constitutional_process",)
    assert result.pipeline_read_only is True
    assert result.writes_event_ledger is False
    assert result.mutates_cluster is False
    assert "not established fact" in result.testimony_boundary
    assert "established_fact" not in json.dumps(constitutional_pipeline_diagnostic_json(result))


def test_diagnostic_uses_existing_pipeline_invocation(monkeypatch):
    import seed_runtime.constitutional_pipeline_diagnostic as diagnostic

    calls = []
    original = diagnostic.invoke_constitutional_pipeline

    def spy(request):
        calls.append(request)
        return original(request)

    monkeypatch.setattr(diagnostic, "invoke_constitutional_pipeline", spy)
    result = build_constitutional_pipeline_diagnostic(_request())

    assert len(calls) == 1
    assert calls[0] == result.pipeline_request
    assert "does not own stage algorithms" in result.diagnostic_boundary


def test_empty_question_keys_are_distinct_from_unsupported_keys():
    empty = build_constitutional_pipeline_diagnostic(_request(caller_supplied_fields=()))
    unsupported = build_constitutional_pipeline_diagnostic(
        _request(caller_supplied_fields=(("selection_key", "missing"),))
    )

    assert _stage(empty, "question_projection").status == "empty"
    assert _stage(empty, "selection").status == "empty"
    assert _stage(empty, "selection").unsupported_keys == ()
    assert "no registered constitutional view matched deterministic projection keys" in empty.no_view_selection_reasons
    assert _stage(unsupported, "question_projection").status == "complete"
    assert _stage(unsupported, "selection").status == "unsupported"
    assert _stage(unsupported, "selection").unsupported_keys == ("missing",)


def test_missing_capability_evidence_is_distinct_from_unmatched_key():
    contract = replace(
        CONSTITUTIONAL_READ_MODEL_CONTRACTS[0],
        name="constitutional_display_only",
        cli_flag="--display-only",
    )
    registration = constitutional_read_model_registration(contract)
    missing_capability = build_constitutional_pipeline_diagnostic(
        _request(
            capability_contracts=(contract,),
            capability_registrations=(registration,),
            capability_view_builders={},
        )
    )

    assert _stage(missing_capability, "capability_projection").status == "unknown"
    assert _stage(missing_capability, "capability_projection").unknowns == ("constitutional_display_only",)
    assert _stage(missing_capability, "selection").status == "unsupported"
    assert _stage(missing_capability, "selection").unsupported_keys == ("process",)


def test_selection_uncertainty_unknowns_refusals_and_empty_composition_remain_visible():
    governance = build_constitutional_pipeline_diagnostic(
        _request(caller_supplied_fields=(("selection_key", "governance"),))
    )
    empty = build_constitutional_pipeline_diagnostic(_request(caller_supplied_fields=()))
    unknown = build_constitutional_pipeline_diagnostic(_request(unknowns=("operator assertion not verified",)))

    assert "caller uncertainty preserved" in _stage(governance, "selection").uncertainty
    assert _stage(governance, "composition").status == "refused"
    assert _stage(governance, "composition").refusal_count >= 1
    assert _stage(governance, "composition").unknown_count >= 1
    assert _stage(empty, "composition_request").status == "empty"
    assert _stage(empty, "composition").status == "empty"
    assert empty.composition_compatibility_answer == "No."
    assert _stage(unknown, "bounded_question").status == "unknown"
    assert "unknown: operator assertion not verified" in _stage(unknown, "selection").uncertainty


def test_json_and_human_output_are_deterministic_and_distinct_from_public_surface(capsys):
    request = _request()
    first = constitutional_pipeline_diagnostic_json(build_constitutional_pipeline_diagnostic(request))
    second = constitutional_pipeline_diagnostic_json(build_constitutional_pipeline_diagnostic(request))
    assert first == second

    human1 = format_constitutional_pipeline_diagnostic(build_constitutional_pipeline_diagnostic(request))
    human2 = format_constitutional_pipeline_diagnostic(build_constitutional_pipeline_diagnostic(request))
    assert human1 == human2
    assert "Constitutional Pipeline Diagnostic" in human1
    assert "Pipeline stage | Status" in human1
    assert "constitutional authority" in human1

    assert seed_local.main(_cli("--selection-key", "process", "--json")) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["name"] == "constitutional_pipeline_diagnostic"
    assert "stages" in payload
    assert seed_local.main([
        "--constitutional-pipeline", "--operator-inquiry", "x", "--inquiry-provenance", "p",
        "--bounded-question", "q", "--constitutional-intent", "i", "--scope-status", "s", "--json",
    ]) == 0
    public_payload = json.loads(capsys.readouterr().out)
    assert "stages" not in public_payload


def test_non_recording_event_ledger_and_cluster_mutation_contract(tmp_path):
    db = tmp_path / "events.sqlite"
    assert seed_local.main(["--db", str(db), *_cli("--selection-key", "process")]) == 0
    assert not db.exists()
    result = build_constitutional_pipeline_diagnostic(_request())
    assert result.recordability == "read-only non-recording diagnostic; record_scope=none"
    assert result.event_ledger_status == "no event-ledger writes"
    assert result.cluster_mutation_status == "no cluster mutation"


def test_inventory_and_shape_audit_expose_real_diagnostic_fields():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "constitutional_pipeline_diagnostic")
    rows = [r for r in build_diagnostic_shape_audit() if r.diagnostic == "constitutional_pipeline_diagnostic"]

    assert entry.cli_flags == ("--constitutional-pipeline-diagnostic",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    assert rows
    assert all(row.status == "consistent" for row in rows)
