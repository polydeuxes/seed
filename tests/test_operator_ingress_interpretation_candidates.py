from dataclasses import replace
from io import BytesIO, StringIO

import pytest

from seed_runtime.contextual_interpretation_warrant_set import InterpretationCandidate
from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress_addressable_material import (
    OperatorIngressAddressableMaterial,
)
from seed_runtime.operator_ingress_common_grammar_prerequisite import (
    run_operator_ingress_common_grammar_probe_attempt,
)
from seed_runtime.operator_ingress_interpretation_candidates import (
    FORMATION_UNKNOWN,
    NO_CANDIDATES_UNKNOWN,
    REQUIRED_AUTHORITY_LIMITS,
    SOURCE_RELATION_UNKNOWN,
    AttributedInterpretationCandidateTestimony,
    OperatorIngressInterpretationCandidateSet,
    OperatorIngressInterpretationCandidateSetError,
    preserve_operator_ingress_interpretation_candidates,
)
from seed_runtime.operator_ingress_representation import capture_stdin_material

EXACT_TEXT = " deploy::alpha | keep residual\r\n"


class _UnreadableResponse:
    def readline(self):
        pytest.fail("candidate preservation must not read additional ingress")


@pytest.fixture
def ingress_material():
    ledger = EventLedger()
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(BytesIO(EXACT_TEXT.encode())),
        response_input_stream=_UnreadableResponse(),
        output_stream=StringIO(),
    )
    artifact = OperatorIngressAddressableMaterial.from_json_dict(
        view["addressable_operator_material"]
    )
    return ledger, artifact


def _testimony(
    material,
    ref="candidate:one",
    span_refs=None,
    supplier="operator-supplied testimony",
    formation="event:formation",
    meaning="  proposed::meaning  ",
    limits=("caller testimony only",),
):
    if span_refs is None:
        span_refs = (material.exact_operator_material.source_spans[0].span_ref,)
    return AttributedInterpretationCandidateTestimony(
        candidate=InterpretationCandidate(ref, "display label", span_refs, meaning),
        attributed_supplier=supplier,
        supplier_provenance=("submission:7", "provider:external"),
        formation_occurrence_ref=formation,
        declared_scope=("this material only",),
        known_loss=("speaker context unavailable",),
        unknowns=("candidate-local unknown",),
        conflicts=("candidate-local conflict",),
        supplied_authority_limits=limits,
    )


def _preserve(material, *testimonies, **kwargs):
    return preserve_operator_ingress_interpretation_candidates(
        addressable_material=material, candidate_testimonies=testimonies, **kwargs
    )


def test_real_ingress_complete_material_and_three_limit_owners_survive(
    ingress_material,
):
    ledger, material = ingress_material
    shared_text = material.authority_limits[0]
    testimony = _testimony(material, limits=(shared_text, shared_text))
    before = testimony
    event_count = len(ledger.list_events("w"))
    result = _preserve(material, testimony)

    assert result.addressable_material is material
    assert result.addressable_material == material
    assert material.provenance == (
        material.raw_material_event_ref,
        material.representation_examination_event_ref,
        material.ingress_event_ref,
    )
    assert (
        material.source_role
        == "operator-origin material at the preserved ingress boundary"
    )
    assert material.scope[0:2] == ("workspace:w", "session:s")
    assert material.scope[2].startswith("attempt:")
    assert material.known_loss == (
        "transport bytes before the supplied binary-stream boundary are not observable",
    )
    assert material.unknowns
    assert result.addressable_material.authority_limits == material.authority_limits
    preserved = result.candidate_testimonies[0]
    assert preserved.supplied_authority_limits == (shared_text, shared_text)
    assert result.preservation_authority_limits == REQUIRED_AUTHORITY_LIMITS
    assert shared_text in material.authority_limits
    assert shared_text in preserved.supplied_authority_limits
    assert testimony == before
    assert testimony.unknowns == ("candidate-local unknown",)
    assert preserved.candidate.proposed_meaning == "  proposed::meaning  "
    assert len(ledger.list_events("w")) == event_count
    assert result.read_only and not result.writes_event_ledger
    assert not result.mutates_state and not result.mutates_cluster


def test_absent_formation_zero_refs_and_blank_proposition_add_local_unknowns(
    ingress_material,
):
    _, material = ingress_material
    result = _preserve(
        material, _testimony(material, formation=None, span_refs=(), meaning="")
    )
    testimony = result.candidate_testimonies[0]
    assert testimony.formation_occurrence_ref is None
    assert FORMATION_UNKNOWN in testimony.unknowns
    assert SOURCE_RELATION_UNKNOWN in testimony.unknowns
    assert "candidate proposition unavailable" in testimony.unknowns


def test_empty_formation_is_distinct_from_none_and_refused(ingress_material):
    _, material = ingress_material
    with pytest.raises(
        OperatorIngressInterpretationCandidateSetError, match="formation"
    ):
        _preserve(material, _testimony(material, formation=""))


def test_zero_one_and_many_candidates_have_no_selection_or_ranking(ingress_material):
    _, material = ingress_material
    zero = _preserve(material)
    assert zero.candidate_testimonies == ()
    assert zero.set_unknowns == (NO_CANDIDATES_UNKNOWN,)
    one = _preserve(material, _testimony(material))
    same_span = material.exact_operator_material.source_spans[0].span_ref
    many = _preserve(
        material,
        _testimony(material, ref="candidate:a", span_refs=(same_span,), meaning="same"),
        _testimony(material, ref="candidate:b", span_refs=(same_span,), meaning="same"),
    )
    assert len(material.exact_operator_material.source_spans) == 1
    span = material.exact_operator_material.source_spans[0]
    assert (span.start, span.end, span.exact_text) == (0, len(EXACT_TEXT), EXACT_TEXT)
    assert len(many.candidate_testimonies) == 2
    for artifact in (one, many):
        encoded = artifact.to_json_dict()
        assert (
            "selected" not in encoded
            and "rank" not in encoded
            and "warrant" not in encoded
        )


def test_candidate_ref_supplier_and_source_validation(ingress_material):
    _, material = ingress_material
    with pytest.raises(OperatorIngressInterpretationCandidateSetError, match="unique"):
        _preserve(material, _testimony(material), _testimony(material))
    with pytest.raises(OperatorIngressInterpretationCandidateSetError, match="foreign"):
        _preserve(material, _testimony(material, span_refs=("span:foreign",)))
    with pytest.raises(
        OperatorIngressInterpretationCandidateSetError, match="supplier"
    ):
        _preserve(material, _testimony(material, supplier=""))


@pytest.mark.parametrize(
    "change",
    [
        lambda value: replace(value, artifact_type="other"),
        lambda value: replace(value, read_only=False),
        lambda value: replace(value, writes_event_ledger=True),
        lambda value: replace(value, provenance=value.provenance[::-1]),
        lambda value: replace(value, raw_material_event_ref="event:foreign"),
        lambda value: replace(value, material_projection_id="projection:forged"),
    ],
)
def test_invalid_complete_addressable_material_is_refused(ingress_material, change):
    _, material = ingress_material
    with pytest.raises(OperatorIngressInterpretationCandidateSetError):
        _preserve(change(material))


def test_identity_covers_each_authority_owner(ingress_material):
    _, material = ingress_material
    testimony = _testimony(material)
    base = _preserve(material, testimony).candidate_set_id
    assert (
        _preserve(
            replace(
                material,
                authority_limits=material.authority_limits + ("new material limit",),
            ),
            testimony,
        ).candidate_set_id
        != base
    )
    assert (
        _preserve(
            material,
            replace(testimony, supplied_authority_limits=("new supplier limit",)),
        ).candidate_set_id
        != base
    )
    assert (
        _preserve(
            material,
            testimony,
            preservation_authority_limits=REQUIRED_AUTHORITY_LIMITS
            + ("new preservation limit",),
        ).candidate_set_id
        != base
    )


def test_exact_round_trip_and_serialized_ownership_shape(ingress_material):
    _, material = ingress_material
    result = _preserve(material, _testimony(material, formation=None))
    encoded = result.to_json_dict()
    assert "addressable_material" in encoded
    assert "authority_limits" in encoded["addressable_material"]
    assert "supplied_authority_limits" in encoded["candidate_testimonies"][0]
    assert "authority_limits" not in encoded["candidate_testimonies"][0]
    assert encoded["candidate_testimonies"][0]["formation_occurrence_ref"] is None
    assert OperatorIngressInterpretationCandidateSet.from_json_dict(encoded) == result


@pytest.mark.parametrize(
    "field", ["read_only", "writes_event_ledger", "mutates_state", "mutates_cluster"]
)
@pytest.mark.parametrize("bad", ["true", "false", 1, 0, None])
def test_malformed_booleans_are_refused(ingress_material, field, bad):
    _, material = ingress_material
    encoded = _preserve(material, _testimony(material)).to_json_dict()
    encoded[field] = bad
    with pytest.raises(OperatorIngressInterpretationCandidateSetError, match="boolean"):
        OperatorIngressInterpretationCandidateSet.from_json_dict(encoded)


@pytest.mark.parametrize(
    ("path", "bad"),
    [
        (("set_unknowns",), "not-a-sequence"),
        (("preservation_authority_limits",), [1]),
        (("addressable_material", "scope"), ["valid", 2]),
        (("addressable_material", "authority_limits"), "not-a-sequence"),
        (("candidate_testimonies", 0, "supplier_provenance"), [object()]),
        (("candidate_testimonies", 0, "candidate", "source_span_refs"), "span:string"),
    ],
)
def test_malformed_string_sequences_are_refused(ingress_material, path, bad):
    _, material = ingress_material
    encoded = _preserve(material, _testimony(material)).to_json_dict()
    cursor = encoded
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = bad
    with pytest.raises(OperatorIngressInterpretationCandidateSetError):
        OperatorIngressInterpretationCandidateSet.from_json_dict(encoded)


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("artifact_type", "other"),
        ("convention", "other"),
        ("candidate_set_id", "forged"),
    ],
)
def test_wrong_type_convention_and_identity_are_refused(ingress_material, field, bad):
    _, material = ingress_material
    encoded = _preserve(material, _testimony(material)).to_json_dict()
    encoded[field] = bad
    with pytest.raises(OperatorIngressInterpretationCandidateSetError):
        OperatorIngressInterpretationCandidateSet.from_json_dict(encoded)


def test_nested_forged_projection_identity_is_refused(ingress_material):
    _, material = ingress_material
    encoded = _preserve(material, _testimony(material)).to_json_dict()
    encoded["addressable_material"]["material_projection_id"] = "forged"
    with pytest.raises(
        OperatorIngressInterpretationCandidateSetError, match="identity"
    ):
        OperatorIngressInterpretationCandidateSet.from_json_dict(encoded)


def test_preservation_does_not_call_warrant_producer(ingress_material, monkeypatch):
    import seed_runtime.contextual_interpretation_warrant_set as warrants

    monkeypatch.setattr(
        warrants,
        "produce_contextual_interpretation_warrant_set",
        lambda **kwargs: pytest.fail("warrant production must remain disconnected"),
    )
    _, material = ingress_material
    assert _preserve(material, _testimony(material)).candidate_testimonies
