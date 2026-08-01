from dataclasses import FrozenInstanceError

import pytest

from seed_runtime.bounded_constitutional_question import (
    BoundedConstitutionalQuestion,
    bounded_constitutional_question_json,
    format_bounded_constitutional_question,
)


def _artifact() -> BoundedConstitutionalQuestion:
    return BoundedConstitutionalQuestion(
        bounded_question_id="test:bounded-constitutional-question",
        operator_inquiry="Can this repository explain constitutional compatibility?\nKeep my wording.",
        inquiry_provenance="operator:terminal-session:test",
        bounded_question="Explain constitutional compatibility for the supplied inquiry.",
        constitutional_intent="compatibility explanation requested by caller",
        scope_status="caller-bounded; not independently verified",
        uncertainty=("caller scope may be incomplete",),
        unknowns=("no projection has been produced",),
        caller_supplied_fields=(("admission", "caller supplied"), ("source", "test")),
    )


def test_bounded_constitutional_question_is_immutable():
    artifact = _artifact()

    with pytest.raises(FrozenInstanceError):
        artifact.operator_inquiry = "changed"

    with pytest.raises(TypeError):
        artifact.uncertainty[0] = "changed"


def test_default_negative_authority_and_read_only_fields():
    artifact = _artifact()

    assert artifact.testimony_status == "operator testimony preserved as evidence, not established fact"
    assert "no established fact promotion" in artifact.read_only_boundaries
    assert "no constitutional authority creation" in artifact.read_only_boundaries
    assert "no authoritative capability creation" in artifact.read_only_boundaries
    assert "no constitutional view selection" in artifact.read_only_boundaries
    assert "no QuestionProjection production" in artifact.read_only_boundaries
    assert artifact.read_only is True
    assert artifact.writes_event_ledger is False
    assert artifact.mutates_cluster is False


def test_json_ready_serialization_preserves_artifact_shape():
    payload = bounded_constitutional_question_json(_artifact())

    assert payload["bounded_question_id"] == "test:bounded-constitutional-question"
    assert payload["uncertainty"] == ("caller scope may be incomplete",)
    assert payload["unknowns"] == ("no projection has been produced",)
    assert payload["caller_supplied_fields"] == (("admission", "caller supplied"), ("source", "test"))
    assert "established_fact" not in payload
    assert "verified_claim" not in payload
    assert "authoritative_capability" not in payload
    assert "selected_view_names" not in payload
    assert "selection_keys" not in payload


def test_human_formatting_preserves_artifact_values_and_boundaries():
    rendered = format_bounded_constitutional_question(_artifact())

    assert "bounded_question_id: test:bounded-constitutional-question" in rendered
    assert "operator_inquiry: Can this repository explain constitutional compatibility?" in rendered
    assert "writes_event_ledger: false" in rendered
    assert "mutates_cluster: false" in rendered
