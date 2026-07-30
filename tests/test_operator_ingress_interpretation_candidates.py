from dataclasses import replace

import pytest

from seed_runtime.contextual_interpretation_warrant_set import (
    ExactOperatorMaterial,
    InterpretationCandidate,
    SourceSpan,
)
from seed_runtime.operator_ingress_addressable_material import (
    OperatorIngressAddressableMaterial,
)
from seed_runtime.operator_ingress_interpretation_candidates import (
    FORMATION_UNKNOWN,
    NO_CANDIDATES_UNKNOWN,
    AttributedInterpretationCandidateTestimony,
    OperatorIngressInterpretationCandidateSet,
    OperatorIngressInterpretationCandidateSetError,
    preserve_operator_ingress_interpretation_candidates,
)

EXACT_TEXT = " deploy::alpha | keep residual\r\n"


def _material():
    exact = ExactOperatorMaterial(
        material_ref="event:ingress",
        exact_text=EXACT_TEXT,
        source_spans=(
            SourceSpan("span:deploy", "event:ingress", 1, 14, "deploy::alpha"),
            SourceSpan("span:overlap", "event:ingress", 1, 7, "deploy"),
        ),
        provenance=("event:raw", "event:examination", "event:ingress"),
    )
    return OperatorIngressAddressableMaterial(
        artifact_type="operator_ingress_addressable_material",
        material_projection_id="projection:exact",
        ingress_event_ref="event:ingress",
        raw_material_event_ref="event:raw",
        representation_examination_event_ref="event:examination",
        exact_operator_material=exact,
        source_role="operator-origin material",
        provenance=exact.provenance,
        scope=("workspace:w",),
        known_loss=(),
        unknowns=("meaning Unknown",),
        authority_limits=("addressability only",),
    )


def _testimony(
    ref="candidate:one",
    span_refs=("span:deploy",),
    supplier="operator-supplied testimony",
    formation="event:formation",
    meaning="  proposed::meaning  ",
):
    return AttributedInterpretationCandidateTestimony(
        candidate=InterpretationCandidate(ref, "display label", span_refs, meaning),
        attributed_supplier=supplier,
        supplier_provenance=("submission:7", "provider:external"),
        formation_occurrence_ref=formation,
        declared_scope=("this material only",),
        known_loss=("speaker context unavailable",),
        unknowns=("candidate-local unknown",),
        conflicts=("candidate-local conflict",),
        authority_limits=("caller testimony only",),
    )


def _preserve(*testimonies, **kwargs):
    return preserve_operator_ingress_interpretation_candidates(
        addressable_material=_material(), candidate_testimonies=testimonies, **kwargs
    )


def test_one_attributed_candidate_preserves_exact_material_and_testimony():
    testimony = _testimony()
    result = _preserve(testimony)
    preserved = result.candidate_testimonies[0]
    assert result.exact_operator_material == _material().exact_operator_material
    assert result.exact_operator_material.exact_text == EXACT_TEXT
    assert preserved.candidate.label == "display label"
    assert preserved.candidate.proposed_meaning == "  proposed::meaning  "
    assert preserved.attributed_supplier == testimony.attributed_supplier
    assert preserved.supplier_provenance == testimony.supplier_provenance
    assert preserved.formation_occurrence_ref == "event:formation"
    assert preserved.declared_scope == testimony.declared_scope
    assert preserved.known_loss == testimony.known_loss
    assert preserved.unknowns == testimony.unknowns
    assert preserved.conflicts == testimony.conflicts
    assert "selected" not in result.to_json_dict()
    assert result.read_only and not result.writes_event_ledger
    assert not result.mutates_state and not result.mutates_cluster


def test_absent_formation_and_blank_proposition_remain_unknown_not_refused():
    result = _preserve(_testimony(formation=None, meaning=""))
    testimony = result.candidate_testimonies[0]
    assert testimony.formation_occurrence_ref is None
    assert FORMATION_UNKNOWN in testimony.unknowns
    assert "candidate proposition unavailable" in testimony.unknowns


def test_zero_candidates_is_lawful_and_has_set_unknown():
    result = _preserve()
    assert result.candidate_testimonies == ()
    assert result.set_unknowns == (NO_CANDIDATES_UNKNOWN,)


def test_overlapping_candidates_and_residual_material_are_lawful_and_distinct():
    result = _preserve(
        _testimony(ref="candidate:whole", span_refs=("span:deploy",), meaning="same"),
        _testimony(ref="candidate:part", span_refs=("span:overlap",), meaning="same"),
    )
    assert [item.candidate.candidate_ref for item in result.candidate_testimonies] == [
        "candidate:whole",
        "candidate:part",
    ]
    assert len(result.candidate_testimonies) == 2
    assert "rank" not in result.to_json_dict()
    assert "selected" not in result.to_json_dict()


def test_candidate_and_set_unknowns_and_conflicts_remain_separate():
    result = _preserve(
        _testimony(),
        set_unknowns=("set unknown",),
        set_conflicts=("set conflict",),
    )
    assert result.set_unknowns == ("set unknown",)
    assert result.set_conflicts == ("set conflict",)
    assert result.candidate_testimonies[0].unknowns == ("candidate-local unknown",)
    assert result.candidate_testimonies[0].conflicts == ("candidate-local conflict",)


def test_duplicate_candidate_refs_foreign_spans_and_missing_supplier_are_refused():
    with pytest.raises(OperatorIngressInterpretationCandidateSetError, match="unique"):
        _preserve(_testimony(), _testimony())
    with pytest.raises(OperatorIngressInterpretationCandidateSetError, match="foreign"):
        _preserve(_testimony(span_refs=("span:another-material",)))
    with pytest.raises(
        OperatorIngressInterpretationCandidateSetError, match="supplier"
    ):
        _preserve(_testimony(supplier=""))


@pytest.mark.parametrize(
    "changed",
    [
        lambda value: replace(value, artifact_type="other"),
        lambda value: replace(value, read_only=False),
        lambda value: replace(value, writes_event_ledger=True),
        lambda value: replace(
            value,
            exact_operator_material=replace(
                value.exact_operator_material, material_ref="event:foreign"
            ),
        ),
        lambda value: replace(
            value,
            exact_operator_material=replace(
                value.exact_operator_material, provenance=("different",)
            ),
        ),
    ],
)
def test_invalid_addressable_material_is_refused(changed):
    with pytest.raises(OperatorIngressInterpretationCandidateSetError):
        preserve_operator_ingress_interpretation_candidates(
            addressable_material=changed(_material()), candidate_testimonies=()
        )


def test_foreign_or_mismatched_source_span_text_is_refused():
    material = _material()
    original = material.exact_operator_material.source_spans[0]
    for span in (
        replace(original, source_ref="event:foreign"),
        replace(original, exact_text="normalized"),
    ):
        exact = replace(material.exact_operator_material, source_spans=(span,))
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            preserve_operator_ingress_interpretation_candidates(
                addressable_material=replace(material, exact_operator_material=exact),
                candidate_testimonies=(),
            )


def test_identity_includes_supplier_formation_and_candidate_identity():
    base = _preserve(_testimony()).candidate_set_id
    assert (
        _preserve(_testimony(supplier="developer-supplied testimony")).candidate_set_id
        != base
    )
    assert _preserve(_testimony(formation=None)).candidate_set_id != base
    first = _preserve(_testimony(ref="candidate:a", meaning="same")).candidate_set_id
    second = _preserve(_testimony(ref="candidate:b", meaning="same")).candidate_set_id
    assert first != second
    assert _preserve(_testimony()).candidate_set_id == base


def test_serialization_round_trips_exactly_including_none():
    result = _preserve(_testimony(formation=None))
    encoded = result.to_json_dict()
    assert encoded["candidate_testimonies"][0]["formation_occurrence_ref"] is None
    assert OperatorIngressInterpretationCandidateSet.from_json_dict(encoded) == result


def test_preservation_does_not_call_warrant_producer(monkeypatch):
    import seed_runtime.contextual_interpretation_warrant_set as warrants

    monkeypatch.setattr(
        warrants,
        "produce_contextual_interpretation_warrant_set",
        lambda **kwargs: pytest.fail("warrant production must remain disconnected"),
    )
    assert _preserve(_testimony()).candidate_testimonies
