from dataclasses import replace

from seed_runtime.representation_grammar_applicability import (
    explain_representation_grammar_applicability_advancement,
)
from seed_runtime.shared_explanation_membership_evidence_projection import (
    BoundedInquiryReference,
    PreservedLineageEvidence,
    format_shared_explanation_membership_evidence,
    project_shared_explanation_membership_evidence,
    shared_explanation_membership_evidence_json,
)
from seed_runtime.shared_explanation_rendering_projection import project_shared_explanation_rendering
from tests.test_representation_grammar_applicability import demand, proj


def _candidate(state="applicable"):
    return project_shared_explanation_rendering(
        explain_representation_grammar_applicability_advancement(
            proj(applicability_state=state, d=demand(required_structures=("table",)))
        )
    )


def test_matching_grammar_applicability_inquiry_lineage_belongs():
    result = project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one", "demand:one"),
        _candidate(),
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",),
            supporting_references=("lineage:source-a",),
            source_identity_refs=("source:a",),
        ),
    )

    assert result.membership_state == "belongs"
    assert result.supporting_references == ("lineage:source-a",)
    assert result.incompatible_references == ()


def test_positive_lineage_to_another_incompatible_inquiry_does_not_belong():
    result = project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one"),
        _candidate(),
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:other",),
            incompatible_inquiry_refs=("inquiry:other",),
            incompatible_references=("lineage:other-positive",),
        ),
    )

    assert result.membership_state == "does_not_belong"
    assert result.incompatible_references == ("lineage:other-positive",)


def test_missing_lineage_evidence_remains_unknown_not_non_membership():
    result = project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one"),
        _candidate(),
        PreservedLineageEvidence(missing_lineage_refs=("lineage:not-preserved",)),
    )

    assert result.membership_state == "unknown"
    assert result.missing_lineage_refs == ("lineage:not-preserved",)
    assert result.incompatible_references == ()


def test_incompatible_inquiry_or_demand_references_with_matching_lineage_conflict():
    result = project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one", "demand:one"),
        _candidate(),
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",),
            incompatible_demand_refs=("demand:other",),
            supporting_references=("lineage:target",),
            incompatible_references=("lineage:other-demand",),
        ),
    )

    assert result.membership_state == "conflict"
    assert result.conflicting_references == ("lineage:target", "lineage:other-demand")


def test_duplicate_source_identity_remains_visible_and_is_not_deduplicated():
    result = project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one"),
        _candidate(),
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",),
            source_identity_refs=("source:a", "source:a", "source:b"),
        ),
    )

    assert result.membership_state == "belongs"
    assert result.duplicate_source_identity_refs == ("source:a", "source:a", "source:b")


def test_shared_state_wording_or_stage_does_not_establish_membership():
    first = _candidate()
    second = replace(_candidate(), source_state=first.source_state, source_reason=first.source_reason)

    result = project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one"),
        second,
        PreservedLineageEvidence(missing_lineage_refs=("no explicit inquiry lineage",)),
    )

    assert first.source_state == second.source_state
    assert first.source_reason == second.source_reason
    assert result.membership_state == "unknown"


def test_human_and_json_render_the_same_membership_meaning():
    result = project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one"),
        _candidate(),
        PreservedLineageEvidence(
            positive_inquiry_refs=("inquiry:one",),
            supporting_references=("lineage:source-a",),
        ),
    )

    text = format_shared_explanation_membership_evidence(result)
    js = shared_explanation_membership_evidence_json(result)

    assert "membership_state: belongs" in text
    assert js["membership_state"] == "belongs"
    assert "- lineage:source-a" in text
    assert js["supporting_references"] == ["lineage:source-a"]


def test_projection_writes_no_events_mutates_no_cluster_and_does_not_select():
    result = project_shared_explanation_membership_evidence(
        BoundedInquiryReference("inquiry:one"),
        _candidate(),
        PreservedLineageEvidence(positive_inquiry_refs=("inquiry:one",)),
    )
    text = format_shared_explanation_membership_evidence(result)

    assert result.read_only is True
    assert result.writes_event_ledger is False
    assert result.mutates_cluster is False
    assert not hasattr(result, "selected_candidate")
    assert "does not select, rank, deduplicate" in text
