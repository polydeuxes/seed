import pytest

from seed_runtime.shared_explanation_encounter_sequencing import (
    PresentationLocalSequencingEvidence,
    format_shared_explanation_encounter_sequencing,
    sequence_shared_explanation_encounters,
    shared_explanation_encounter_sequencing_json,
)
from seed_runtime.shared_explanation_membership_evidence_projection import (
    PreservedLineageEvidence,
)
from seed_runtime.shared_explanation_presentation_admission import (
    PresentationAdmissionEvidence,
    RequestedPresentationBoundary,
    admit_shared_explanation_presentation,
)
from tests.test_shared_explanation_presentation_admission import _set
from tests.test_shared_explanation_membership_evidence_set import _result


def _admission(*results, admitted_refs=()):
    return admit_shared_explanation_presentation(
        _set(*results),
        RequestedPresentationBoundary(
            "presentation:alpha", "inquiry:one", "demand:one"
        ),
        PresentationAdmissionEvidence("presentation:alpha", admitted_refs),
    )


def test_explicit_encounter_evidence_reorders_admitted_without_losing_derivation_lineage():
    first_derived = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:first",
    )
    second_derived = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:second",
    )
    admission = _admission(
        first_derived,
        second_derived,
        admitted_refs=("candidate:first", "candidate:second"),
    )

    sequencing = sequence_shared_explanation_encounters(
        admission,
        (
            PresentationLocalSequencingEvidence(
                "candidate:second", 0, ("operator-map:second-first",), "answer"
            ),
            PresentationLocalSequencingEvidence(
                "candidate:first", 1, ("operator-map:first-second",), "support"
            ),
        ),
    )

    assert sequencing.constitutional_derivation_projection_refs == (
        "candidate:first",
        "candidate:second",
    )
    assert sequencing.encounter_sequence_projection_refs == (
        "candidate:second",
        "candidate:first",
    )
    assert sequencing.encounter_sequence_results == (second_derived, first_derived)
    assert (
        sequencing.encounter_sequence_results[0].candidate_source_explanation_ref
        == "candidate:second"
    )
    assert (
        sequencing.encounter_sequence_results[1].supporting_references
        == first_derived.supporting_references
    )
    assert sequencing.optional_roles_by_projection_ref == {
        "candidate:second": "answer",
        "candidate:first": "support",
    }
    assert not hasattr(sequencing, "composed_view")
    assert not hasattr(sequencing, "constitutional_rank")


def test_non_admitted_unknown_conflict_duplicates_and_unsequenced_obligations_remain_visible():
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
    unsequenced = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:later",
    )
    unknown = _result(
        PreservedLineageEvidence(missing_lineage_refs=("missing",)), "candidate:unknown"
    )
    conflict = _result(
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",), incompatible_references=("other",)
        ),
        "candidate:conflict",
    )
    admission = _admission(
        admitted,
        duplicate,
        unsequenced,
        unknown,
        conflict,
        admitted_refs=("candidate:dup", "candidate:later"),
    )

    sequencing = sequence_shared_explanation_encounters(
        admission,
        (PresentationLocalSequencingEvidence("candidate:dup", 2, ("explicit:dup",)),),
    )

    assert sequencing.encounter_sequence_projection_refs == (
        "candidate:dup",
        "candidate:dup",
    )
    assert sequencing.unsequenced_admitted_projection_refs == ("candidate:later",)
    assert sequencing.unknown_results == (unknown,)
    assert sequencing.conflict_results == (conflict,)
    assert sequencing.belonging_but_unadmitted_results == ()
    duplicate_candidate_refs = [
        o.identity_ref
        for o in sequencing.duplicate_identity_occurrences
        if o.identity_kind == "candidate_projection_ref"
    ]
    assert duplicate_candidate_refs.count("candidate:dup") == 2


def test_ignores_non_admitted_evidence_and_remains_read_only_non_composing_json_and_text():
    admitted = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:admitted",
    )
    unadmitted = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:unadmitted",
    )
    admission = _admission(admitted, unadmitted, admitted_refs=("candidate:admitted",))

    sequencing = sequence_shared_explanation_encounters(
        admission,
        (
            PresentationLocalSequencingEvidence(
                "candidate:unadmitted", 0, ("ignored:not-admitted",)
            ),
            PresentationLocalSequencingEvidence(
                "candidate:admitted", 1, ("explicit:admitted",)
            ),
        ),
    )
    text = format_shared_explanation_encounter_sequencing(sequencing)
    js = shared_explanation_encounter_sequencing_json(sequencing)

    assert sequencing.encounter_sequence_projection_refs == ("candidate:admitted",)
    assert sequencing.belonging_but_unadmitted_results == (unadmitted,)
    assert (
        "candidate:unadmitted" not in sequencing.sequencing_evidence_by_projection_ref
    )
    assert "constitutional_derivation_projection_refs:" in text
    assert "encounter_sequence_projection_refs:" in text
    assert "not composition, constitutional ranking, deduplication" in text
    assert js["read_only"] is True
    assert js["writes_event_ledger"] is False
    assert js["mutates_cluster"] is False


def test_optional_roles_are_not_invented_and_unsupported_roles_are_refused():
    admitted = _result(
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
        "candidate:admitted",
    )
    admission = _admission(admitted, admitted_refs=("candidate:admitted",))

    sequencing = sequence_shared_explanation_encounters(
        admission,
        (
            PresentationLocalSequencingEvidence(
                "candidate:admitted", 0, ("explicit:admitted",)
            ),
        ),
    )

    assert sequencing.optional_roles_by_projection_ref == {}
    with pytest.raises(ValueError, match="unsupported optional encounter role"):
        PresentationLocalSequencingEvidence(
            "candidate:admitted", 0, optional_role="blocker"
        )
