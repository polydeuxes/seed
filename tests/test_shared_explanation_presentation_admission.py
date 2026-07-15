from dataclasses import replace

import pytest

from seed_runtime.shared_explanation_membership_evidence_projection import (
    BoundedInquiryReference,
    PreservedLineageEvidence,
)
from seed_runtime.shared_explanation_membership_evidence_set import (
    build_shared_explanation_membership_evidence_set,
)
from seed_runtime.shared_explanation_presentation_admission import (
    PresentationAdmissionEvidence,
    RequestedPresentationBoundary,
    admit_shared_explanation_presentation,
    format_shared_explanation_presentation_admission,
    shared_explanation_presentation_admission_json,
)
from tests.test_shared_explanation_membership_evidence_set import _result


def _set(*results):
    return build_shared_explanation_membership_evidence_set(
        BoundedInquiryReference("inquiry:one", "demand:one"), tuple(results)
    )


def _boundary(ref="presentation:alpha"):
    return RequestedPresentationBoundary(ref, "inquiry:one", "demand:one")


def test_admission_is_presentation_local_and_does_not_rewrite_membership():
    first = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:first")
    second = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:second")
    evidence_set = _set(first, second)

    alpha = admit_shared_explanation_presentation(
        evidence_set,
        _boundary("presentation:alpha"),
        PresentationAdmissionEvidence("presentation:alpha", ("candidate:first",), ("rule:alpha",)),
    )
    beta = admit_shared_explanation_presentation(
        evidence_set,
        _boundary("presentation:beta"),
        PresentationAdmissionEvidence("presentation:beta", ("candidate:second",), ("rule:beta",)),
    )

    assert evidence_set.belongs_results == (first, second)
    assert alpha.admitted_to_sequencing_results == (first,)
    assert alpha.belonging_but_unadmitted_results == (second,)
    assert beta.admitted_to_sequencing_results == (second,)
    assert beta.belonging_but_unadmitted_results == (first,)
    assert alpha.admission_evidence_refs == ("rule:alpha",)
    assert beta.admission_evidence_refs == ("rule:beta",)


def test_belonging_but_unadmitted_keeps_reason_without_becoming_non_member():
    belongs = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:belongs")
    does_not = _result(
        PreservedLineageEvidence(incompatible_inquiry_refs=("inquiry:other",)), "candidate:not"
    )
    admission = admit_shared_explanation_presentation(
        _set(belongs, does_not),
        _boundary(),
        PresentationAdmissionEvidence(
            "presentation:alpha",
            (),
            non_admission_reasons_by_projection_ref={"candidate:belongs": ("presentation omitted by request",)},
        ),
    )

    assert admission.admitted_to_sequencing_results == ()
    assert admission.belonging_but_unadmitted_results == (belongs,)
    assert admission.non_admission_reasons_by_projection_ref["candidate:belongs"] == (
        "presentation omitted by request",
    )
    assert admission.non_member_results == (does_not,)
    assert does_not not in admission.belonging_but_unadmitted_results


def test_unknown_conflict_and_duplicates_remain_visible_without_admission_or_deduplication():
    admitted = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:dup")
    duplicate = _result(
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",), source_identity_refs=("source:dup", "source:dup")
        ),
        "candidate:dup",
    )
    unknown = _result(PreservedLineageEvidence(missing_lineage_refs=("missing",)), "candidate:unknown")
    conflict = _result(
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",), incompatible_references=("other",)
        ),
        "candidate:conflict",
    )

    admission = admit_shared_explanation_presentation(
        _set(admitted, duplicate, unknown, conflict),
        _boundary(),
        PresentationAdmissionEvidence("presentation:alpha", ("candidate:dup",)),
    )

    assert admission.admitted_to_sequencing_results == (admitted, duplicate)
    assert admission.admitted_to_sequencing_projection_refs == ("candidate:dup", "candidate:dup")
    assert admission.unknown_results == (unknown,)
    assert admission.conflict_results == (conflict,)
    source_occurrences = [
        o for o in admission.duplicate_identity_occurrences if o.identity_kind == "duplicate_source_identity_ref"
    ]
    assert [o.identity_ref for o in source_occurrences] == ["source:dup", "source:dup"]


def test_admitted_to_sequencing_is_not_first_encounter_order_or_composition():
    first = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:first")
    later = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:later")
    admission = admit_shared_explanation_presentation(
        _set(first, later),
        _boundary(),
        PresentationAdmissionEvidence("presentation:alpha", ("candidate:later",)),
    )

    assert admission.admitted_to_sequencing_results == (later,)
    assert admission.belonging_but_unadmitted_results == (first,)
    assert not hasattr(admission, "first_in_encounter_order")
    assert not hasattr(admission, "composed_view")
    assert not hasattr(admission, "sequence_rank")


def test_boundaries_are_explicit_and_output_is_read_only_json_and_text():
    result = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:a")
    admission = admit_shared_explanation_presentation(
        _set(result), _boundary(), PresentationAdmissionEvidence("presentation:alpha", ("candidate:a",))
    )

    text = format_shared_explanation_presentation_admission(admission)
    js = shared_explanation_presentation_admission_json(admission)

    assert "Admission to sequencing is not first encounter order" in text
    assert js["admitted_to_sequencing_projection_refs"] == ["candidate:a"]
    assert js["read_only"] is True
    assert js["writes_event_ledger"] is False
    assert js["mutates_cluster"] is False


def test_mismatched_inquiry_demand_or_presentation_boundary_is_refused():
    result = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:a")
    evidence_set = _set(result)

    with pytest.raises(ValueError, match="bounded inquiry"):
        admit_shared_explanation_presentation(
            evidence_set,
            replace(_boundary(), bounded_inquiry_ref="inquiry:other"),
            PresentationAdmissionEvidence("presentation:alpha", ("candidate:a",)),
        )
    with pytest.raises(ValueError, match="bounded demand"):
        admit_shared_explanation_presentation(
            evidence_set,
            replace(_boundary(), bounded_demand_ref="demand:other"),
            PresentationAdmissionEvidence("presentation:alpha", ("candidate:a",)),
        )
    with pytest.raises(ValueError, match="requested presentation"):
        admit_shared_explanation_presentation(
            evidence_set,
            _boundary("presentation:alpha"),
            PresentationAdmissionEvidence("presentation:other", ("candidate:a",)),
        )
