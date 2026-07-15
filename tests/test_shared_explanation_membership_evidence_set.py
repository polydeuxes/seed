from dataclasses import replace

import pytest

from seed_runtime.shared_explanation_membership_evidence_projection import (
    BoundedInquiryReference,
    PreservedLineageEvidence,
    project_shared_explanation_membership_evidence,
)
from seed_runtime.shared_explanation_membership_evidence_set import (
    build_shared_explanation_membership_evidence_set,
    format_shared_explanation_membership_evidence_set,
    shared_explanation_membership_evidence_set_json,
)
from tests.test_shared_explanation_membership_evidence_projection import _candidate


def _result(state_inputs, candidate_ref):
    candidate = replace(_candidate(), source_explanation_identity=candidate_ref)
    return project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one", "demand:one"),
        candidate,
        state_inputs,
    )


def test_same_inquiry_and_demand_constructs_lawful_read_only_set():
    first = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:a")
    second = _result(PreservedLineageEvidence(missing_lineage_refs=("lineage:missing",)), "candidate:b")

    evidence_set = build_shared_explanation_membership_evidence_set(
        BoundedInquiryReference("inquiry:one", "demand:one"), (first, second)
    )

    assert evidence_set.bounded_inquiry_ref == "inquiry:one"
    assert evidence_set.bounded_demand_ref == "demand:one"
    assert evidence_set.membership_results == (first, second)
    assert evidence_set.belongs_results == (first,)
    assert evidence_set.read_only is True
    assert evidence_set.writes_event_ledger is False
    assert evidence_set.mutates_cluster is False
    assert not hasattr(evidence_set, "selected_rendering_projections")


def test_mixed_explicit_inquiry_or_demand_is_refused():
    lawful = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:a")
    wrong_inquiry = replace(lawful, bounded_inquiry_ref="inquiry:other")
    wrong_demand = replace(lawful, bounded_demand_ref="demand:other")

    with pytest.raises(ValueError, match="bounded inquiry"):
        build_shared_explanation_membership_evidence_set(
            BoundedInquiryReference("inquiry:one", "demand:one"), (lawful, wrong_inquiry)
        )

    with pytest.raises(ValueError, match="bounded demand"):
        build_shared_explanation_membership_evidence_set(
            BoundedInquiryReference("inquiry:one", "demand:one"), (lawful, wrong_demand)
        )


def test_every_supplied_result_and_duplicate_occurrence_remains_visible_without_deduplication():
    first = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:dup")
    second = _result(
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",),
            source_identity_refs=("source:x", "source:x"),
        ),
        "candidate:dup",
    )

    evidence_set = build_shared_explanation_membership_evidence_set(
        BoundedInquiryReference("inquiry:one", "demand:one"), (first, second)
    )

    assert evidence_set.membership_results == (first, second)
    assert evidence_set.belongs_results == (first, second)
    candidate_occurrences = [
        o for o in evidence_set.duplicate_identity_occurrences if o.identity_kind == "candidate_projection_ref"
    ]
    assert [o.identity_ref for o in candidate_occurrences] == ["candidate:dup", "candidate:dup"]
    source_occurrences = [
        o for o in evidence_set.duplicate_identity_occurrences if o.identity_kind == "duplicate_source_identity_ref"
    ]
    assert [o.identity_ref for o in source_occurrences] == ["source:x", "source:x"]


def test_general_collection_and_state_partitions_are_mechanical_over_existing_states_only():
    belongs = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:belongs")
    does_not = _result(
        PreservedLineageEvidence(
            incompatible_inquiry_refs=("inquiry:other",),
            incompatible_references=("lineage:other",),
        ),
        "candidate:not",
    )
    unknown = _result(PreservedLineageEvidence(missing_lineage_refs=("lineage:missing",)), "candidate:unknown")
    conflict = _result(
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",),
            incompatible_demand_refs=("demand:other",),
            supporting_references=("lineage:target",),
            incompatible_references=("lineage:other",),
        ),
        "candidate:conflict",
    )

    evidence_set = build_shared_explanation_membership_evidence_set(
        BoundedInquiryReference("inquiry:one", "demand:one"), (belongs, does_not, unknown, conflict)
    )

    assert evidence_set.membership_results == (belongs, does_not, unknown, conflict)
    assert evidence_set.belongs_results == (belongs,)
    assert evidence_set.does_not_belong_results == (does_not,)
    assert evidence_set.unknown_results == (unknown,)
    assert evidence_set.conflict_results == (conflict,)
    assert [r.membership_state for r in evidence_set.membership_results] == [
        "belongs",
        "does_not_belong",
        "unknown",
        "conflict",
    ]
    assert {r.membership_state for r in evidence_set.belongs_results} == {"belongs"}
    assert {r.membership_state for r in evidence_set.does_not_belong_results} == {"does_not_belong"}
    assert {r.membership_state for r in evidence_set.unknown_results} == {"unknown"}
    assert {r.membership_state for r in evidence_set.conflict_results} == {"conflict"}
    assert evidence_set.state_partitions == {
        "belongs": ("candidate:belongs",),
        "does_not_belong": ("candidate:not",),
        "unknown": ("candidate:unknown",),
        "conflict": ("candidate:conflict",),
    }


def test_empty_and_partial_collection_truth_makes_no_completeness_claim_and_fabricates_no_unknowns():
    evidence_set = build_shared_explanation_membership_evidence_set(
        BoundedInquiryReference("inquiry:one", "demand:one"), ()
    )

    assert evidence_set.collection_empty is True
    assert evidence_set.collection_partial is True
    assert evidence_set.supplied_result_count == 0
    assert evidence_set.membership_results == ()
    assert evidence_set.belongs_results == ()
    assert evidence_set.state_partitions["unknown"] == ()
    assert evidence_set.completeness_claim == "none; supplied collection only"


def test_human_and_json_render_same_bounded_set_meaning():
    result = _result(PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)), "candidate:a")
    evidence_set = build_shared_explanation_membership_evidence_set(
        BoundedInquiryReference("inquiry:one", "demand:one"), (result,)
    )

    text = format_shared_explanation_membership_evidence_set(evidence_set)
    js = shared_explanation_membership_evidence_set_json(evidence_set)

    assert "bounded_inquiry_ref: inquiry:one" in text
    assert js["bounded_inquiry_ref"] == "inquiry:one"
    assert "belongs_result_identities:" in text
    assert "  belongs:" in text
    assert js["membership_results"][0]["candidate_projection_ref"] == "candidate:a"
    assert js["belongs_results"][0]["candidate_projection_ref"] == "candidate:a"
    assert js["state_partitions"]["belongs"] == ["candidate:a"]
    obsolete_alias = "belonging" + "_results"
    assert not hasattr(evidence_set, obsolete_alias)
    assert obsolete_alias not in js
    assert obsolete_alias + "_compatibility_note" not in js
    assert obsolete_alias not in text
    assert "Does not select rendering projections" in text
    assert js["writes_event_ledger"] is False
