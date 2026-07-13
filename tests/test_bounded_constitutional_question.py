from dataclasses import FrozenInstanceError

import pytest

from seed_runtime.bounded_constitutional_question import (
    BoundedConstitutionalQuestion,
    bounded_constitutional_question_json,
    produce_bounded_constitutional_question,
)


def _produce(**overrides):
    inputs = {
        "operator_inquiry": "Can this repository explain constitutional compatibility?\nKeep my wording.",
        "inquiry_provenance": "operator:terminal-session:test",
        "bounded_question": "Explain constitutional compatibility for the supplied inquiry.",
        "constitutional_intent": "compatibility explanation requested by caller",
        "scope_status": "caller-bounded; not independently verified",
        "uncertainty": ["caller scope may be incomplete"],
        "unknowns": ["no projection has been produced"],
        "caller_supplied_fields": {"admission": "caller supplied", "source": "test"},
    }
    inputs.update(overrides)
    return produce_bounded_constitutional_question(**inputs)


def test_bounded_constitutional_question_is_immutable():
    artifact = _produce()

    with pytest.raises(FrozenInstanceError):
        artifact.operator_inquiry = "changed"

    with pytest.raises(TypeError):
        artifact.uncertainty[0] = "changed"

    assert isinstance(artifact, BoundedConstitutionalQuestion)


def test_production_is_deterministic_from_explicit_inputs():
    first = _produce()
    second = _produce()

    assert first == second
    assert first.bounded_question_id == second.bounded_question_id

    explicit_first = _produce(bounded_question_id="caller:id")
    explicit_second = _produce(bounded_question_id="caller:id")
    assert explicit_first == explicit_second
    assert explicit_first.bounded_question_id == "caller:id"


def test_operator_inquiry_and_provenance_are_preserved_exactly():
    inquiry = "Operator words preserved:  spaces  \n punctuation?!"
    artifact = _produce(operator_inquiry=inquiry, inquiry_provenance="source:operator:testimony")

    assert artifact.operator_inquiry == inquiry
    assert artifact.inquiry_provenance == "source:operator:testimony"


def test_explicit_bounded_fields_uncertainty_and_unknowns_are_preserved():
    uncertainty = ["uncertain admission", "uncertain scope"]
    unknowns = ["unknown projection", "unknown selected views"]
    caller_fields = {"z": "last", "a": "first"}

    artifact = _produce(
        bounded_question="Bounded content supplied explicitly.",
        constitutional_intent="caller supplied intent",
        scope_status="caller supplied scope",
        uncertainty=uncertainty,
        unknowns=unknowns,
        caller_supplied_fields=caller_fields,
    )

    assert artifact.bounded_question == "Bounded content supplied explicitly."
    assert artifact.constitutional_intent == "caller supplied intent"
    assert artifact.scope_status == "caller supplied scope"
    assert artifact.uncertainty == tuple(uncertainty)
    assert artifact.unknowns == tuple(unknowns)
    assert artifact.caller_supplied_fields == (("a", "first"), ("z", "last"))


def test_testimony_is_not_fact_authority_capability_selection_or_projection():
    artifact = _produce()
    payload = bounded_constitutional_question_json(artifact)

    assert artifact.testimony_status == "operator testimony preserved as evidence, not established fact"
    assert "no established fact promotion" in artifact.read_only_boundaries
    assert "no constitutional authority creation" in artifact.read_only_boundaries
    assert "no authoritative capability creation" in artifact.read_only_boundaries
    assert "no constitutional view selection" in artifact.read_only_boundaries
    assert "no QuestionProjection production" in artifact.read_only_boundaries
    assert "established_fact" not in payload
    assert "verified_claim" not in payload
    assert "authoritative_capability" not in payload
    assert "selected_view_names" not in payload
    assert "selection_keys" not in payload


def test_read_only_no_event_ledger_and_no_cluster_mutation():
    artifact = _produce()

    assert artifact.read_only is True
    assert artifact.writes_event_ledger is False
    assert artifact.mutates_cluster is False


def test_production_does_not_mutate_caller_owned_input_collections():
    uncertainty = ["before"]
    unknowns = ["unknown before"]
    caller_fields = {"source": "before"}

    artifact = _produce(
        uncertainty=uncertainty,
        unknowns=unknowns,
        caller_supplied_fields=caller_fields,
    )

    uncertainty.append("after")
    unknowns.append("unknown after")
    caller_fields["source"] = "after"

    assert artifact.uncertainty == ("before",)
    assert artifact.unknowns == ("unknown before",)
    assert artifact.caller_supplied_fields == (("source", "before"),)
