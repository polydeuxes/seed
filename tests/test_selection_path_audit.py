import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.state import StateProjector

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "seed_local.py"


def load_seed_local():
    spec = importlib.util.spec_from_file_location(
        "seed_local_selection_path", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def ingest(seed_local, db_path, *observations):
    argv = ["--db", str(db_path), "--quiet-output"]
    for subject, predicate, value in observations:
        argv.extend(["--observe", subject, predicate, value])
    assert seed_local.main(argv) == 0


def seeded_db(tmp_path):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
    )
    return seed_local, db


def test_selection_path_renders(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert seed_local.main(["--db", str(db), "--selection-path", "current_focus"]) == 0
    output = capsys.readouterr().out

    assert "Selection Path" in output
    assert "Selected:" in output
    assert "Candidate Set:" in output
    assert "Selection Factors:" in output
    assert "Non-selected Candidates:" in output
    assert "Boundary:" in output


def test_selection_path_json_is_valid_and_surfaces_selection_details(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db), "--selection-path", "current_focus", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["selected"]
    assert payload["candidates"]
    assert {"candidate", "score", "rank", "reason", "evidence"} <= set(
        payload["candidates"][0]
    )
    assert payload["selection_factors"]
    assert "descending score" in payload["selection_factors"][0]
    assert isinstance(payload["non_selected"], list)
    assert payload["evidence"]
    assert payload["boundary"]["records_facts"] is False
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_cluster"] is False


def test_selection_path_preserves_result_and_lineage_at_compatibility_handoff(
    tmp_path, capsys
):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db), "--selection-path", "current_focus", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["selected"] == payload["outcome"]["selected"]
    assert payload["candidates"]
    assert payload["selection_factors"]
    assert payload["evidence"]
    assert "candidates" not in payload["outcome"]
    assert "selection_factors" not in payload["outcome"]
    assert "evidence" not in payload["outcome"]


def test_selection_path_unknown_logic_remains_explicit(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db), "--selection-path", "not_a_selection", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["selected"] == "unknown"
    assert payload["selection_factors"] == ["unknown"]
    assert payload["unknowns"]
    assert (
        "no implementation-backed selection evidence"
        in payload["unknowns"][0]["reason"]
    )


def test_selection_answer_and_reason_payloads_are_separate():
    from seed_runtime.selection_path_audit import (
        _SelectionCandidateSetPayload,
        _SelectionFactorPayload,
        _SelectionLineagePayload,
        _SelectionNonSelectedPayload,
        _SelectionReasonPayload,
        _SelectionResultPayload,
        _SelectionSupportingEvidencePayload,
        _SelectionUnknownPayload,
        _selection_path_from_payloads,
    )

    result = _SelectionResultPayload(selected="primary pressure")
    reason = _SelectionReasonPayload(
        outcome={
            "selected": "primary pressure",
            "reason": "pressure audit selected the highest-ranked candidate",
        }
    )
    support = _SelectionSupportingEvidencePayload(evidence=[])
    lineage = _SelectionLineagePayload(
        candidate_set=_SelectionCandidateSetPayload(candidates=[]),
        factors=_SelectionFactorPayload(selection_factors=[]),
        non_selected=_SelectionNonSelectedPayload(non_selected=[]),
        unknowns=_SelectionUnknownPayload(unknowns=[]),
    )

    audit = _selection_path_from_payloads(
        target="primary_pressure",
        result=result,
        reason=reason,
        support=support,
        lineage=lineage,
    )

    assert audit.selected == "primary pressure"
    assert audit.outcome == reason.outcome
    assert "outcome" not in result.__dataclass_fields__
    assert "selected" not in reason.__dataclass_fields__
    assert "candidates" not in reason.__dataclass_fields__


def test_selection_reason_and_supporting_evidence_payloads_are_separate():
    from seed_runtime.selection_path_audit import (
        _SelectionCandidateSetPayload,
        _SelectionFactorPayload,
        _SelectionLineagePayload,
        _SelectionNonSelectedPayload,
        _SelectionReasonPayload,
        _SelectionResultPayload,
        _SelectionSupportingEvidencePayload,
        _SelectionUnknownPayload,
        _selection_path_from_payloads,
    )

    reason = _SelectionReasonPayload(
        outcome={"selected": "primary pressure", "summary": "primary pressure selected"}
    )
    support = _SelectionSupportingEvidencePayload(
        evidence=[{"surface": "pressure_audit", "score": 2}]
    )
    lineage = _SelectionLineagePayload(
        candidate_set=_SelectionCandidateSetPayload(candidates=[]),
        factors=_SelectionFactorPayload(selection_factors=[]),
        non_selected=_SelectionNonSelectedPayload(non_selected=[]),
        unknowns=_SelectionUnknownPayload(unknowns=[]),
    )

    audit = _selection_path_from_payloads(
        target="primary_pressure",
        result=_SelectionResultPayload(selected="primary pressure"),
        reason=reason,
        support=support,
        lineage=lineage,
    )

    assert audit.outcome == reason.outcome
    assert audit.evidence == support.evidence
    assert "evidence" not in reason.__dataclass_fields__
    assert "outcome" not in support.__dataclass_fields__
    assert "evidence" not in lineage.__dataclass_fields__


def test_selection_candidate_set_payload_is_separate_from_lineage_explanation():
    from seed_runtime.selection_path_audit import (
        _SelectionCandidateSetPayload,
        _SelectionFactorPayload,
        _SelectionLineagePayload,
        _SelectionNonSelectedPayload,
        _SelectionReasonPayload,
        _SelectionResultPayload,
        _SelectionSupportingEvidencePayload,
        _SelectionUnknownPayload,
        _selection_path_from_payloads,
    )

    candidate_set = _SelectionCandidateSetPayload(
        candidates=[
            {
                "candidate": "runtime reachability",
                "score": 2,
                "rank": 1,
                "reason": "pressure candidate",
                "evidence": ["source"],
            }
        ]
    )
    lineage = _SelectionLineagePayload(
        candidate_set=candidate_set,
        factors=_SelectionFactorPayload(
            selection_factors=["pressure audit orders candidates"]
        ),
        non_selected=_SelectionNonSelectedPayload(non_selected=[]),
        unknowns=_SelectionUnknownPayload(unknowns=[]),
    )

    audit = _selection_path_from_payloads(
        target="primary_pressure",
        result=_SelectionResultPayload(selected="runtime reachability"),
        reason=_SelectionReasonPayload(outcome={"selected": "runtime reachability"}),
        support=_SelectionSupportingEvidencePayload(evidence=[]),
        lineage=lineage,
    )

    assert audit.candidates == candidate_set.candidates
    assert lineage.candidate_set == candidate_set
    assert "factors" not in candidate_set.__dataclass_fields__
    assert "non_selected" not in candidate_set.__dataclass_fields__
    assert "unknowns" not in candidate_set.__dataclass_fields__


def test_selection_factor_payload_is_separate_from_candidate_set_and_unknowns():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import _selection_factors_from_pressures

    pressure = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )

    payload = _selection_factors_from_pressures((pressure,))

    assert payload.selection_factors == [
        "pressure audit orders candidates by descending score, then category name"
    ]
    assert _selection_factors_from_pressures(()).selection_factors == ["unknown"]
    assert "candidates" not in payload.__dataclass_fields__
    assert "non_selected" not in payload.__dataclass_fields__
    assert "unknowns" not in payload.__dataclass_fields__


def test_selection_unknown_payload_is_separate_from_candidate_lineage():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import _selection_unknowns_from_pressures

    pressure = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )

    populated = _selection_unknowns_from_pressures((pressure,))
    empty = _selection_unknowns_from_pressures(())

    assert populated.unknowns == []
    assert empty.unknowns[0].unknown_type == "Evidence Gap"
    assert empty.unknowns[0].area == "candidate_set"
    assert "candidates" not in empty.__dataclass_fields__
    assert "selection_factors" not in empty.__dataclass_fields__
    assert "non_selected" not in empty.__dataclass_fields__


def test_selection_non_selected_payload_is_separate_from_candidate_set():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import _non_selected_from_pressures

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )
    lower = PressureItem(
        category="Documentation drift",
        score=1,
        reason="lower pressure",
        evidence={"source": "lower evidence"},
        recommended_command="seed --pressure-audit",
    )

    payload = _non_selected_from_pressures((selected, lower), selected)

    assert payload.non_selected == [
        {
            "candidate": "documentation drift",
            "score": 1,
            "reason": "lower pressure score than selected candidate",
        }
    ]
    assert "candidates" not in payload.__dataclass_fields__
    assert "factors" not in payload.__dataclass_fields__
    assert "unknowns" not in payload.__dataclass_fields__


def test_pressure_selection_lineage_payload_is_owned_by_local_helper():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import (
        _SelectionUnknownPayload,
        _pressure_selection_lineage_payload,
    )

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )
    lower = PressureItem(
        category="Documentation drift",
        score=1,
        reason="lower pressure",
        evidence={"source": "lower evidence"},
        recommended_command="seed --pressure-audit",
    )
    unknowns = _SelectionUnknownPayload(unknowns=[])

    payload = _pressure_selection_lineage_payload((selected, lower), selected, unknowns)

    assert payload.candidate_set.candidates == [
        {
            "candidate": "runtime reachability",
            "score": 3,
            "rank": 1,
            "reason": "selected pressure",
            "evidence": {"source": "selected evidence"},
        },
        {
            "candidate": "documentation drift",
            "score": 1,
            "rank": 2,
            "reason": "lower pressure",
            "evidence": {"source": "lower evidence"},
        },
    ]
    assert payload.factors.selection_factors == [
        "pressure audit orders candidates by descending score, then category name"
    ]
    assert payload.non_selected.non_selected == [
        {
            "candidate": "documentation drift",
            "score": 1,
            "reason": "lower pressure score than selected candidate",
        }
    ]
    assert payload.unknowns == unknowns
    assert "outcome" not in payload.__dataclass_fields__
    assert "evidence" not in payload.__dataclass_fields__
    assert "selected" not in payload.__dataclass_fields__


def test_pressure_selection_supporting_evidence_payload_is_owned_by_local_helper():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import (
        _pressure_selection_supporting_evidence_payload,
    )

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )

    payload = _pressure_selection_supporting_evidence_payload(selected)

    assert payload.evidence == [
        {
            "surface": "pressure_audit",
            "category": "Runtime reachability",
            "score": 3,
            "reason": "selected pressure",
            "evidence": {"source": "selected evidence"},
        }
    ]
    assert _pressure_selection_supporting_evidence_payload(None).evidence == []
    assert "outcome" not in payload.__dataclass_fields__
    assert "candidates" not in payload.__dataclass_fields__
    assert "selection_factors" not in payload.__dataclass_fields__


def test_selected_pressure_item_lookup_is_owned_by_local_helper():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import _selected_pressure_item

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )
    lower = PressureItem(
        category="Documentation drift",
        score=1,
        reason="lower pressure",
        evidence={"source": "lower evidence"},
        recommended_command="seed --pressure-audit",
    )

    assert _selected_pressure_item((selected, lower)) == selected
    assert _selected_pressure_item(()) is None


def test_focus_selection_selected_name_is_owned_by_local_helper():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import (
        _focus_selection_selected_name,
        _normalize_target,
    )

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )

    assert (
        _focus_selection_selected_name(
            _normalize_target("current_focus"), selected, "Runtime reachability"
        )
        == "Runtime reachability"
    )
    assert (
        _focus_selection_selected_name(
            _normalize_target("primary pressure"), selected, "Runtime reachability"
        )
        == "runtime reachability"
    )
    assert (
        _focus_selection_selected_name(
            _normalize_target("primary pressure"), None, "Runtime reachability"
        )
        == "Runtime reachability"
    )


def test_pressure_category_selection_selected_name_is_owned_by_local_helper():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import (
        _pressure_category_selection_selected_name,
    )

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )

    assert (
        _pressure_category_selection_selected_name(selected, "Runtime reachability")
        == "runtime reachability"
    )
    assert (
        _pressure_category_selection_selected_name(None, "Runtime reachability")
        == "Runtime reachability"
    )


def test_pressure_category_selection_is_owned_by_local_helper():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import _from_pressure_category_selection

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )
    lower = PressureItem(
        category="Documentation drift",
        score=1,
        reason="lower pressure",
        evidence={"source": "lower evidence"},
        recommended_command="seed --pressure-audit",
    )

    audit = _from_pressure_category_selection(
        "runtime_reachability", (selected, lower), "Runtime reachability"
    )

    assert audit.target == "runtime_reachability"
    assert audit.selected == "runtime reachability"
    assert audit.outcome == {
        "selected": "runtime reachability",
        "focus": "Runtime reachability",
        "summary": "runtime reachability selected",
    }
    assert audit.candidates[0]["candidate"] == "runtime reachability"
    assert audit.evidence[0]["surface"] == "pressure_audit"
    assert audit.non_selected == [
        {
            "candidate": "documentation drift",
            "score": 1,
            "reason": "lower pressure score than selected candidate",
        }
    ]
    assert audit.boundary["mutates_cluster"] is False


def test_focus_selection_is_owned_by_local_helper():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import (
        _from_focus_selection,
        _normalize_target,
    )

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )
    lower = PressureItem(
        category="Documentation drift",
        score=1,
        reason="lower pressure",
        evidence={"source": "lower evidence"},
        recommended_command="seed --pressure-audit",
    )

    audit = _from_focus_selection(
        "primary_pressure",
        _normalize_target("primary pressure"),
        (selected, lower),
        "Runtime reachability",
    )

    assert audit.target == "primary_pressure"
    assert audit.selected == "runtime reachability"
    assert audit.outcome == {
        "selected": "runtime reachability",
        "focus": "Runtime reachability",
        "summary": "runtime reachability selected",
    }
    assert audit.candidates[0]["candidate"] == "runtime reachability"
    assert audit.evidence[0]["surface"] == "pressure_audit"
    assert audit.non_selected == [
        {
            "candidate": "documentation drift",
            "score": 1,
            "reason": "lower pressure score than selected candidate",
        }
    ]
    assert audit.boundary["mutates_cluster"] is False


def test_focus_selection_helper_preserves_current_focus_compatibility_case():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import (
        _from_focus_selection,
        _normalize_target,
    )

    selected = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )

    audit = _from_focus_selection(
        "current_focus",
        _normalize_target("current-focus"),
        (selected,),
        "Runtime reachability",
    )

    assert audit.selected == "Runtime reachability"
    assert audit.outcome["summary"] == "Runtime reachability selected"
    assert audit.candidates[0]["candidate"] == "runtime reachability"


def test_pressure_selection_result_payload_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import _pressure_selection_result_payload

    payload = _pressure_selection_result_payload("runtime reachability")

    assert payload.selected == "runtime reachability"
    assert "outcome" not in payload.__dataclass_fields__
    assert "evidence" not in payload.__dataclass_fields__
    assert "candidates" not in payload.__dataclass_fields__


def test_pressure_selection_reason_payload_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import _pressure_selection_reason_payload

    payload = _pressure_selection_reason_payload(
        "runtime reachability", "Runtime reachability"
    )

    assert payload.outcome == {
        "selected": "runtime reachability",
        "focus": "Runtime reachability",
        "summary": "runtime reachability selected",
    }
    assert "evidence" not in payload.__dataclass_fields__
    assert "candidates" not in payload.__dataclass_fields__
    assert "selection_factors" not in payload.__dataclass_fields__


def test_focus_selection_target_matching_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import (
        _normalize_target,
        _target_matches_focus_selection,
    )

    assert _target_matches_focus_selection(
        _normalize_target("current-focus"), "Runtime reachability"
    )
    assert _target_matches_focus_selection(
        _normalize_target("primary pressure"), "Runtime reachability"
    )
    assert _target_matches_focus_selection(
        _normalize_target("reachability"), "Runtime reachability"
    )
    assert not _target_matches_focus_selection(
        _normalize_target("not_a_selection"), "Runtime reachability"
    )


def test_pressure_category_target_matching_is_owned_by_local_helper():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import (
        _normalize_target,
        _target_matches_pressure_category,
    )

    pressure = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )

    assert _target_matches_pressure_category(
        _normalize_target("runtime-reachability"), (pressure,)
    )
    assert _target_matches_pressure_category(
        _normalize_target("reachability"), (pressure,)
    )
    assert not _target_matches_pressure_category(
        _normalize_target("not_a_selection"), (pressure,)
    )


def test_selection_path_repo_root_preparation_is_owned_by_local_helper(tmp_path):
    from seed_runtime.selection_path_audit import _selection_path_repo_root

    explicit_root = tmp_path / "repo"

    assert _selection_path_repo_root(explicit_root) == explicit_root
    assert _selection_path_repo_root(str(explicit_root)) == explicit_root
    assert _selection_path_repo_root(None) == ROOT


def test_selection_path_input_collection_is_owned_by_local_helper(
    monkeypatch, tmp_path
):
    import seed_runtime.selection_path_audit as selection_path_audit
    from seed_runtime.pressure_audit import PressureItem

    pressure = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )
    calls = []

    def fake_pressure_audit(state, *, repo_root):
        calls.append(("pressure", state, repo_root))
        return type("PressureAudit", (), {"pressures": (pressure,)})()

    def fake_operational_story(state, *, repo_root):
        calls.append(("story", state, repo_root))
        return type("OperationalStory", (), {"focus": "Runtime reachability"})()

    monkeypatch.setattr(
        selection_path_audit, "build_pressure_audit", fake_pressure_audit
    )
    monkeypatch.setattr(
        selection_path_audit, "build_operational_story", fake_operational_story
    )

    state = object()
    payload = selection_path_audit._selection_path_inputs(state, tmp_path)

    assert payload.pressures == (pressure,)
    assert payload.focus == "Runtime reachability"
    assert calls == [("pressure", state, tmp_path), ("story", state, tmp_path)]
    assert "target" not in payload.__dataclass_fields__
    assert "selected" not in payload.__dataclass_fields__
    assert "outcome" not in payload.__dataclass_fields__


def test_unsupported_target_selection_refusal_is_prepared_separately():
    from seed_runtime.pressure_audit import PressureItem
    from seed_runtime.selection_path_audit import _unsupported_target_selection

    pressure = PressureItem(
        category="Runtime reachability",
        score=3,
        reason="selected pressure",
        evidence={"source": "selected evidence"},
        recommended_command="seed --pressure-audit",
    )

    audit = _unsupported_target_selection("not_a_selection", (pressure,))

    assert audit.target == "not_a_selection"
    assert audit.selected == "unknown"
    assert audit.outcome == {
        "selected": "unknown",
        "reason": "target is not an implemented selection surface",
    }
    assert audit.candidates == [
        {
            "candidate": "runtime reachability",
            "score": 3,
            "rank": 1,
            "reason": "selected pressure",
            "evidence": {"source": "selected evidence"},
        }
    ]
    assert audit.selection_factors == ["unknown"]
    assert audit.non_selected == []
    assert audit.evidence == []
    assert audit.unknowns == [
        {
            "area": "selection_logic",
            "reason": "no implementation-backed selection evidence discovered for target",
        }
    ]
    assert audit.boundary["mutates_cluster"] is False


def test_unsupported_target_result_payload_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import _unsupported_target_result_payload

    payload = _unsupported_target_result_payload()

    assert payload.selected == "unknown"
    assert "outcome" not in payload.__dataclass_fields__
    assert "evidence" not in payload.__dataclass_fields__
    assert "candidates" not in payload.__dataclass_fields__


def test_unsupported_target_reason_payload_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import _unsupported_target_reason_payload

    payload = _unsupported_target_reason_payload()

    assert payload.outcome == {
        "selected": "unknown",
        "reason": "target is not an implemented selection surface",
    }
    assert "evidence" not in payload.__dataclass_fields__
    assert "candidates" not in payload.__dataclass_fields__
    assert "selection_factors" not in payload.__dataclass_fields__


def test_unsupported_target_supporting_evidence_payload_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import (
        _unsupported_target_supporting_evidence_payload,
    )

    payload = _unsupported_target_supporting_evidence_payload()

    assert payload.evidence == []
    assert "outcome" not in payload.__dataclass_fields__
    assert "candidates" not in payload.__dataclass_fields__
    assert "selection_factors" not in payload.__dataclass_fields__


def test_unsupported_target_factor_payload_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import _unsupported_target_factor_payload

    payload = _unsupported_target_factor_payload()

    assert payload.selection_factors == ["unknown"]
    assert "candidates" not in payload.__dataclass_fields__
    assert "non_selected" not in payload.__dataclass_fields__
    assert "unknowns" not in payload.__dataclass_fields__


def test_unsupported_target_non_selected_payload_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import (
        _unsupported_target_non_selected_payload,
    )

    payload = _unsupported_target_non_selected_payload()

    assert payload.non_selected == []
    assert "candidates" not in payload.__dataclass_fields__
    assert "selection_factors" not in payload.__dataclass_fields__
    assert "unknowns" not in payload.__dataclass_fields__


def test_unsupported_target_unknown_payload_is_owned_by_local_helper():
    from seed_runtime.selection_path_audit import _unsupported_target_unknown_payload

    payload = _unsupported_target_unknown_payload()

    assert len(payload.unknowns) == 1
    assert payload.unknowns[0].unknown_type == "Implementation Unknown"
    assert payload.unknowns[0].area == "selection_logic"
    assert (
        payload.unknowns[0].reason
        == "no implementation-backed selection evidence discovered for target"
    )
    assert "candidates" not in payload.__dataclass_fields__
    assert "selection_factors" not in payload.__dataclass_fields__
    assert "non_selected" not in payload.__dataclass_fields__


def test_selection_path_does_not_change_operational_story_selection(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert seed_local.main(["--db", str(db), "--operational-story", "--json"]) == 0
    story_before = json.loads(capsys.readouterr().out)
    assert (
        seed_local.main(
            ["--db", str(db), "--selection-path", "current_focus", "--json"]
        )
        == 0
    )
    selection = json.loads(capsys.readouterr().out)
    assert seed_local.main(["--db", str(db), "--operational-story", "--json"]) == 0
    story_after = json.loads(capsys.readouterr().out)

    assert story_after == story_before
    assert selection["outcome"]["focus"] == story_before["focus"]


def test_selection_path_does_not_write_events_or_mutate_cluster(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    ledger = SQLiteEventLedger(str(db))
    try:
        before = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()

    before_state = StateProjector(SQLiteEventLedger(db)).project(
        seed_local.DEFAULT_WORKSPACE
    )
    before_facts = dict(before_state.facts)
    assert seed_local.main(["--db", str(db), "--selection-path", "current_focus"]) == 0
    capsys.readouterr()

    ledger = SQLiteEventLedger(str(db))
    try:
        after = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
        after_state = StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()

    assert [event.id for event in after] == [event.id for event in before]
    assert dict(after_state.facts) == before_facts


def test_selection_path_registered_in_visibility_contracts():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit

    entry = next(item for item in DIAGNOSTIC_INVENTORY if item.name == "selection_path")
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False

    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "selection_path"
    ]
    assert rows
    assert {row.status for row in rows} <= {"consistent"}


def test_selection_path_lineage_owns_typed_unknown_before_public_handoff():
    from seed_runtime.selection_path_audit import (
        _SelectionCandidateSetPayload,
        _SelectionFactorPayload,
        _SelectionLineagePayload,
        _SelectionNonSelectedPayload,
        _SelectionReasonPayload,
        _SelectionResultPayload,
        _SelectionSupportingEvidencePayload,
        _SelectionUnknownPayload,
        _selection_path_from_payloads,
    )
    from seed_runtime.typed_unknowns import preserve_typed_unknown

    typed_unknown = preserve_typed_unknown(
        unknown_type="Implementation Unknown",
        area="selection_logic",
        reason="no implementation-backed selection evidence discovered for target",
    )
    lineage = _SelectionLineagePayload(
        _SelectionCandidateSetPayload(candidates=[]),
        _SelectionFactorPayload(selection_factors=["unknown"]),
        _SelectionNonSelectedPayload(non_selected=[]),
        _SelectionUnknownPayload(unknowns=[typed_unknown]),
    )

    audit = _selection_path_from_payloads(
        target="not_a_selection",
        result=_SelectionResultPayload(selected="unknown"),
        reason=_SelectionReasonPayload(outcome={"selected": "unknown"}),
        support=_SelectionSupportingEvidencePayload(evidence=[]),
        lineage=lineage,
    )

    assert lineage.unknowns.unknowns[0].unknown_type == "Implementation Unknown"
    assert audit.unknowns == [
        {
            "area": "selection_logic",
            "reason": "no implementation-backed selection evidence discovered for target",
        }
    ]
