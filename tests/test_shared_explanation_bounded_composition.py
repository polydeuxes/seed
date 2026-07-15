from seed_runtime.shared_explanation_bounded_composition import (
    compose_shared_explanation_bounded_view,
    format_shared_explanation_bounded_composition,
    shared_explanation_bounded_composition_json,
)
from seed_runtime.shared_explanation_encounter_sequencing import (
    PresentationLocalSequencingEvidence,
    sequence_shared_explanation_encounters,
)
from seed_runtime.shared_explanation_membership_evidence_projection import (
    PreservedLineageEvidence,
)
from tests.test_shared_explanation_encounter_sequencing import _admission
from tests.test_shared_explanation_membership_evidence_set import _result


def test_composition_preserves_one_sequencing_snapshot_without_reordering_or_role_assignment():
    first_derived = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:first",
    )
    second_derived = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:second",
    )
    unsequenced = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:unsequenced",
    )
    sequencing = sequence_shared_explanation_encounters(
        _admission(
            first_derived,
            second_derived,
            unsequenced,
            admitted_refs=(
                "candidate:first",
                "candidate:second",
                "candidate:unsequenced",
            ),
        ),
        (
            PresentationLocalSequencingEvidence(
                "candidate:second", 7, ("operator:second-first",), "answer"
            ),
            PresentationLocalSequencingEvidence(
                "candidate:first", 9, ("operator:first-second",), "support"
            ),
        ),
    )

    composition = compose_shared_explanation_bounded_view(sequencing)

    assert composition.source_sequencing_artifact_type == "SharedExplanationEncounterSequencing"
    assert composition.source_sequencing_producer == "sequence_shared_explanation_encounters"
    assert composition.constitutional_derivation_projection_refs == (
        "candidate:first",
        "candidate:second",
        "candidate:unsequenced",
    )
    assert composition.encounter_sequence_projection_refs == (
        "candidate:second",
        "candidate:first",
    )
    assert composition.encounter_sequence_results == sequencing.encounter_sequence_results
    assert composition.encounter_sequence_results[0] is second_derived
    assert composition.unsequenced_admitted_results == (unsequenced,)
    assert composition.unsequenced_admitted_projection_refs == ("candidate:unsequenced",)
    assert composition.optional_roles_by_projection_ref == {
        "candidate:second": "answer",
        "candidate:first": "support",
    }


def test_composition_preserves_unresolved_non_member_duplicate_and_source_identity_material():
    admitted = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:dup",
    )
    duplicate = _result(
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",),
            source_identity_refs=("source:x", "source:x"),
        ),
        "candidate:dup",
    )
    unknown = _result(
        PreservedLineageEvidence(missing_lineage_refs=("missing",)),
        "candidate:unknown",
    )
    conflict = _result(
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",), incompatible_references=("other",)
        ),
        "candidate:conflict",
    )
    non_member = _result(
        PreservedLineageEvidence(incompatible_inquiry_refs=("inquiry:other",)),
        "candidate:non-member",
    )
    unadmitted = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:unadmitted",
    )
    sequencing = sequence_shared_explanation_encounters(
        _admission(
            admitted,
            duplicate,
            unknown,
            conflict,
            non_member,
            unadmitted,
            admitted_refs=("candidate:dup",),
        ),
        (PresentationLocalSequencingEvidence("candidate:dup", 0),),
    )

    composition = compose_shared_explanation_bounded_view(sequencing)

    assert composition.unknown_results == (unknown,)
    assert composition.conflict_results == (conflict,)
    assert composition.non_member_results == (non_member,)
    assert composition.belonging_but_unadmitted_results == (unadmitted,)
    assert composition.duplicate_identity_occurrences == sequencing.duplicate_identity_occurrences
    duplicate_candidate_refs = [
        o.identity_ref
        for o in composition.duplicate_identity_occurrences
        if o.identity_kind == "candidate_projection_ref"
    ]
    assert duplicate_candidate_refs.count("candidate:dup") == 2
    assert composition.sequencing_evidence_by_projection_ref is sequencing.sequencing_evidence_by_projection_ref


def test_json_and_text_preserve_read_only_boundaries_and_open_inquiry_status():
    admitted = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:admitted",
    )
    sequencing = sequence_shared_explanation_encounters(
        _admission(admitted, admitted_refs=("candidate:admitted",)),
        (PresentationLocalSequencingEvidence("candidate:admitted", 0),),
    )
    composition = compose_shared_explanation_bounded_view(sequencing)

    text = format_shared_explanation_bounded_composition(composition)
    js = shared_explanation_bounded_composition_json(composition)

    assert "complete bounded presentation is not a completed inquiry" in text
    assert "does not imply the operator is finished" in text
    assert "Does not reorder, select, assign roles, deduplicate" in text
    assert "record" in text
    assert js["read_only"] is True
    assert js["writes_event_ledger"] is False
    assert js["mutates_cluster"] is False
    assert js["encounter_sequence_projection_refs"] == ["candidate:admitted"]
    assert js["constitutional_derivation_projection_refs"] == ["candidate:admitted"]
