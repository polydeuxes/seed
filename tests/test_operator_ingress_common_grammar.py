from io import BytesIO, StringIO
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import subprocess
import sys

import pytest

from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishmentError,
    establish_bounded_operator_goal_from_closed_choice,
)
from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    ClosedChoiceSelectionBindingError,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
    bind_closed_choice_selection,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_ingress_common_grammar_prerequisite import (
    CHOICE_SET_REF,
    ALTERNATIVE_SOURCES,
    RENDERING_KNOWN_LOSS,
    SOURCE_PROPOSITIONS,
    APPLICATION_SOURCE_MEANING_CONVENTION,
    APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY,
    APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION,
    APPLICATION_PRESENTATION_ELIGIBILITY_CONVENTION,
    ApplicationPresentationPurposeDeclaration,
    ApplicationSourceMeaningTestimony,
    ApplicationSourceRoleTestimony,
    POTENTIAL_GOAL_SOURCE_REF,
    SOURCE_MEANING_CONVENTIONS,
    SOURCE_MEANING_TESTIMONIES,
    _examine_meaning_relation_for_bounded_operator_goal_establishment,
    _warrant_source_meaning_relation,
    _examine_potential_goal_standing,
    _examine_presentation_eligibility,
    application_presentation_purpose,
    common_grammar_choice_set,
    _recover_represented_source,
    run_operator_ingress_common_grammar_probe_attempt,
    validate_capture_for_probe,
)
from seed_runtime.operator_ingress_representation import (
    CapturedOperatorMaterial,
    capture_stdin_material,
)
from seed_runtime.state import StateProjector
from scripts import seed_local


def run_attempt(text, ledger=None, session="s"):
    ledger = ledger or EventLedger()
    output = StringIO()
    input_stream = StringIO(text)
    captured_ingress = capture_stdin_material(input_stream)
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id=session,
        captured_ingress=captured_ingress,
        response_input_stream=input_stream,
        output_stream=output,
    )
    return ledger, view, output.getvalue()


def examine_standing(
    *,
    testimony=APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY,
    convention=APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION,
):
    ledger = EventLedger()
    event = _examine_potential_goal_standing(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        testimony=testimony,
        convention=convention,
    )
    return event


def examine_eligibility(
    *,
    standing_marker="canonical",
    purpose_marker="canonical",
    authority_marker="canonical",
):
    ledger = EventLedger()
    standing = _examine_potential_goal_standing(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        testimony=APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY,
        convention=APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION,
    )
    purpose = application_presentation_purpose("presentation:test")
    occurrence = _examine_presentation_eligibility(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        standing_occurrence=(
            standing if standing_marker == "canonical" else standing_marker
        ),
        presentation_ref="presentation:test",
        purpose_declaration=(
            purpose if purpose_marker == "canonical" else purpose_marker
        ),
        convention=(
            APPLICATION_PRESENTATION_ELIGIBILITY_CONVENTION
            if authority_marker == "canonical"
            else authority_marker
        ),
    )
    return ledger, standing, occurrence


def test_exact_recorded_standing_is_consumed_for_only_presentation_eligibility():
    _, standing, occurrence = examine_eligibility()
    assert occurrence.payload["eligibility_result"] == "eligible"
    assert occurrence.payload["upstream_standing_occurrence_id"] == standing.id
    assert (
        occurrence.payload["upstream_standing_relation"]
        == "has bounded potential-goal standing"
    )
    assert occurrence.payload["upstream_standing_result"] == "established"
    assert occurrence.payload["source_ref"] == POTENTIAL_GOAL_SOURCE_REF
    for key in (
        "establishes_alternative_formation",
        "establishes_exact_set_participation",
        "establishes_presentation",
        "establishes_selection",
        "establishes_meaning",
        "establishes_applicability",
        "establishes_admission",
        "establishes_bounded_goal",
        "establishes_stopping",
        "establishes_movement",
        "establishes_authority",
        "establishes_performance",
    ):
        assert occurrence.payload[key] is False


@pytest.mark.parametrize(
    "substitute",
    [
        APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY,
        SOURCE_MEANING_TESTIMONIES[POTENTIAL_GOAL_SOURCE_REF],
        "potential-goal candidate",
    ],
)
def test_testimony_or_role_string_cannot_establish_presentation_eligibility(substitute):
    assert (
        examine_eligibility(standing_marker=substitute)[2].payload["eligibility_result"]
        == "refused"
    )


def test_copied_foreign_and_unrecorded_standing_evidence_is_refused():
    _, standing, _ = examine_eligibility()
    assert (
        examine_eligibility(standing_marker=deepcopy(standing.payload))[2].payload[
            "eligibility_result"
        ]
        == "refused"
    )
    assert (
        examine_eligibility(standing_marker=standing)[2].payload["eligibility_result"]
        == "refused"
    )


def test_duplicate_standing_occurrences_are_refused():
    ledger = EventLedger()
    kwargs = dict(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        testimony=APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY,
        convention=APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION,
    )
    standing = _examine_potential_goal_standing(**kwargs)
    _examine_potential_goal_standing(**kwargs)
    occurrence = _examine_presentation_eligibility(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        standing_occurrence=standing,
        presentation_ref="presentation:test",
        purpose_declaration=application_presentation_purpose("presentation:test"),
        convention=APPLICATION_PRESENTATION_ELIGIBILITY_CONVENTION,
    )
    assert occurrence.payload["eligibility_result"] == "refused"


def test_missing_standing_is_unknown_not_ineligible():
    result = examine_eligibility(standing_marker=None)[2].payload
    assert result["eligibility_result"] == "unknown"
    assert result["eligibility_result"] != "ineligible"


@pytest.mark.parametrize(
    ("field", "expected"), [("unknowns", "unknown"), ("conflicts", "conflict")]
)
def test_exact_carried_upstream_states_are_preserved(field, expected):
    ledger = EventLedger()
    testimony = replace(
        APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY, **{field: ("carried",)}
    )
    standing = _examine_potential_goal_standing(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        testimony=testimony,
        convention=APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION,
    )
    occurrence = _examine_presentation_eligibility(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        standing_occurrence=standing,
        presentation_ref="presentation:test",
        purpose_declaration=application_presentation_purpose("presentation:test"),
        convention=APPLICATION_PRESENTATION_ELIGIBILITY_CONVENTION,
    )
    assert occurrence.payload["eligibility_result"] == expected


def test_exact_upstream_refusal_does_not_become_ineligible():
    ledger = EventLedger()
    standing = _examine_potential_goal_standing(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        testimony=replace(
            APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY, attributed_role="wrong"
        ),
        convention=APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION,
    )
    occurrence = _examine_presentation_eligibility(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        standing_occurrence=standing,
        presentation_ref="presentation:test",
        purpose_declaration=application_presentation_purpose("presentation:test"),
        convention=APPLICATION_PRESENTATION_ELIGIBILITY_CONVENTION,
    )
    assert occurrence.payload["eligibility_result"] == "refused"


@pytest.mark.parametrize(
    "purpose",
    [
        replace(
            application_presentation_purpose("presentation:test"),
            presentation_ref="wrong",
        ),
        replace(application_presentation_purpose("presentation:test"), purpose="wrong"),
        replace(application_presentation_purpose("presentation:test"), provenance=()),
        ApplicationPresentationPurposeDeclaration("forged", "presentation:test"),
    ],
)
def test_wrong_missing_or_forged_purpose_is_refused(purpose):
    assert (
        examine_eligibility(purpose_marker=purpose)[2].payload["eligibility_result"]
        == "refused"
    )


def test_missing_authority_is_unknown_and_forged_authority_is_refused():
    assert (
        examine_eligibility(authority_marker=None)[2].payload["eligibility_result"]
        == "unknown"
    )
    forged = replace(APPLICATION_PRESENTATION_ELIGIBILITY_CONVENTION, scope="wrong")
    assert (
        examine_eligibility(authority_marker=forged)[2].payload["eligibility_result"]
        == "refused"
    )


def test_structural_purpose_failure_precedes_carried_unknowns():
    purpose = replace(
        application_presentation_purpose("presentation:test"),
        scope="wrong",
        unknowns=("carried",),
    )
    occurrence = examine_eligibility(purpose_marker=purpose)[2]
    assert occurrence.payload["eligibility_result"] == "refused"


@pytest.mark.parametrize(
    ("coordinate", "value"),
    [
        ("standing_subject", "source:wrong"),
        ("standing_relation", "expresses"),
    ],
)
def test_wrong_upstream_source_or_relation_is_refused(coordinate, value):
    original = examine_standing()
    forged = original.model_copy(deep=True)
    forged.payload[coordinate] = value
    ledger = EventLedger()
    ledger.extend([forged])
    recorded = ledger.get(forged.id)
    occurrence = _examine_presentation_eligibility(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:test",
        standing_occurrence=recorded,
        presentation_ref="presentation:test",
        purpose_declaration=application_presentation_purpose("presentation:test"),
        convention=APPLICATION_PRESENTATION_ELIGIBILITY_CONVENTION,
    )
    assert occurrence.payload["eligibility_result"] == "refused"


def test_live_eligibility_is_once_after_standing_before_probe_and_not_for_local_stop():
    ledger, view, output = run_attempt("ingress\n2\n")
    events = ledger.list("w")
    kinds = [event.kind for event in events]
    eligibility = [
        event
        for event in events
        if event.kind.endswith("presentation_eligibility_examined")
    ]
    assert len(eligibility) == 1
    assert (
        kinds.index("operator.ingress.common_grammar.potential_goal_standing_examined")
        < kinds.index(
            "operator.ingress.common_grammar.presentation_eligibility_examined"
        )
        < kinds.index("operator.ingress.common_grammar.probe_produced")
        < kinds.index("operator.ingress.common_grammar.alternatives_represented")
    )
    assert eligibility[0].payload["source_ref"] == POTENTIAL_GOAL_SOURCE_REF
    assert "local-stop" not in eligibility[0].payload["source_ref"]
    assert (
        view["current_standing"]["presentation_eligibility"]["evidence_event_id"]
        == eligibility[0].id
    )
    assert output.count("Select one alternative") == 1


def test_role_testimony_and_authority_are_distinct_from_meaning_warrant():
    role = APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY
    meaning = SOURCE_MEANING_TESTIMONIES[POTENTIAL_GOAL_SOURCE_REF]
    authority = APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION
    assert isinstance(role, ApplicationSourceRoleTestimony)
    assert isinstance(meaning, ApplicationSourceMeaningTestimony)
    assert role.testimony_id != meaning.testimony_id
    assert "standing" not in role.authority_limits[0].split("does not establish ")[0]
    assert not hasattr(authority, "source_ref")
    assert not hasattr(authority, "attributed_role")
    for testimony in (meaning, "potential-goal candidate"):
        occurrence = examine_standing(testimony=testimony)
        assert occurrence.payload["standing_result"] == "refused"
        assert occurrence.payload["examination_reason"] == "inadmissible_testimony_form"


def test_exact_role_testimony_under_bounded_authority_establishes_only_standing():
    occurrence = examine_standing()
    assert occurrence.payload["standing_result"] == "established"
    assert occurrence.payload["examination_reason"] == (
        "exact_admissible_role_testimony_under_applicable_bounded_authority"
    )
    assert (
        occurrence.payload["source_role_testimony_ref"]
        == APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY.testimony_id
    )
    assert (
        occurrence.payload["constitutive_authority_ref"]
        == APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION.convention_id
    )
    assert occurrence.payload["establishes_presentation_eligibility"] is False
    assert occurrence.payload["establishes_exact_set_participation"] is False
    forbidden = (
        "applicability",
        "admission",
        "bounded_goal",
        "stopping",
        "acquisition",
        "movement",
        "authority_standing",
    )
    assert not any(name in occurrence.payload for name in forbidden)


@pytest.mark.parametrize(
    "coordinate",
    [
        "testimony_id",
        "source_ref",
        "attributed_role",
        "attributed_supplier",
        "producer_declaration_ref",
        "purpose",
        "scope",
        "provenance",
    ],
)
def test_missing_role_testimony_coordinate_is_refused(coordinate):
    value = () if coordinate == "provenance" else ""
    occurrence = examine_standing(
        testimony=replace(
            APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY, **{coordinate: value}
        )
    )
    assert occurrence.payload["standing_result"] == "refused"


def test_missing_forged_wrong_unknown_and_conflicting_standing_inputs():
    assert examine_standing(testimony=None).payload["standing_result"] == "unknown"
    assert (
        examine_standing(
            testimony=replace(
                APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY, testimony_id="forged"
            )
        ).payload["examination_reason"]
        == "forged_source_role_testimony"
    )
    assert (
        examine_standing(
            testimony=replace(
                APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY, source_ref="source:wrong"
            )
        ).payload["examination_reason"]
        == "source_identity_mismatch"
    )
    assert (
        examine_standing(
            testimony=replace(
                APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY, attributed_role="local-stop"
            )
        ).payload["examination_reason"]
        == "attributed_role_mismatch"
    )
    assert (
        examine_standing(
            testimony=replace(
                APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY,
                unknowns=("material unknown",),
            )
        ).payload["standing_result"]
        == "unknown"
    )
    assert (
        examine_standing(
            testimony=replace(
                APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY, conflicts=("conflict",)
            )
        ).payload["standing_result"]
        == "conflict"
    )
    assert (
        examine_standing(
            convention=replace(
                APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION, unknowns=("unknown",)
            )
        ).payload["standing_result"]
        == "unknown"
    )
    assert (
        examine_standing(
            convention=replace(
                APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION, conflicts=("conflict",)
            )
        ).payload["standing_result"]
        == "conflict"
    )
    assert (
        examine_standing(
            convention=replace(
                APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION, scope="elsewhere"
            )
        ).payload["standing_result"]
        == "refused"
    )


@pytest.mark.parametrize(
    ("changes", "carried_content", "reason"),
    [
        (
            {"source_ref": "source:wrong"},
            {"unknowns": ("material unknown",)},
            "source_identity_mismatch",
        ),
        (
            {"source_ref": "source:wrong"},
            {"conflicts": ("material conflict",)},
            "source_identity_mismatch",
        ),
        (
            {"attributed_role": "local-stop"},
            {"unknowns": ("material unknown",)},
            "attributed_role_mismatch",
        ),
        (
            {"testimony_id": "testimony:forged"},
            {"conflicts": ("material conflict",)},
            "forged_source_role_testimony",
        ),
    ],
)
def test_testimony_inadmissibility_precedes_carried_unknowns_or_conflicts(
    changes, carried_content, reason
):
    testimony = replace(
        APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY, **changes, **carried_content
    )
    occurrence = examine_standing(testimony=testimony)
    assert occurrence.payload["standing_result"] == "refused"
    assert occurrence.payload["examination_reason"] == reason
    assert occurrence.payload["refusal_reason"] == reason


@pytest.mark.parametrize(
    ("changes", "carried_content"),
    [
        ({"scope": "scope:wrong"}, {"unknowns": ("material unknown",)}),
        (
            {"convention_id": "convention:forged"},
            {"conflicts": ("material conflict",)},
        ),
    ],
)
def test_authority_inapplicability_precedes_carried_unknowns_or_conflicts(
    changes, carried_content
):
    convention = replace(
        APPLICATION_POTENTIAL_GOAL_STANDING_CONVENTION, **changes, **carried_content
    )
    occurrence = examine_standing(convention=convention)
    assert occurrence.payload["standing_result"] == "refused"
    assert occurrence.payload["examination_reason"] == (
        "forged_or_inapplicable_constitutive_authority"
    )


def test_wrong_authority_type_is_refused_before_conflict_shaped_content():
    class ConflictShapedAuthority:
        conflicts = ("material conflict",)
        unknowns = ()

    occurrence = examine_standing(convention=ConflictShapedAuthority())
    assert occurrence.payload["standing_result"] == "refused"
    assert (
        occurrence.payload["examination_reason"]
        == "inapplicable_constitutive_authority_form"
    )


@pytest.mark.parametrize("token", ["1", "2"])
def test_live_standing_precedes_formation_without_crossing_eligibility(token):
    ledger, view, output = run_attempt(f"unknown request\n{token}\n")
    events = ledger.list_events("w")
    standing = [
        e for e in events if e.kind.endswith("potential_goal_standing_examined")
    ]
    represented = next(e for e in events if e.kind.endswith("alternatives_represented"))
    assert len(standing) == 1
    assert events.index(standing[0]) < events.index(represented)
    assert standing[0].payload["standing_subject"] == POTENTIAL_GOAL_SOURCE_REF
    assert standing[0].payload["standing_result"] == "established"
    assert standing[0].payload["attributed_role"] != "local-stop"
    assert (
        view["current_standing"]["source_role_testimony"]["testimony"][
            "attributed_role"
        ]
        == "potential-goal candidate"
    )
    assert (
        view["current_standing"]["potential_goal_standing"]["dimensions"]["standing"]
        == "established"
    )
    assert output.count("Select one alternative") == 1


def test_representation_evidence_precedes_response_and_preserves_distinctions():
    ledger, view, _ = run_attempt("unknown request\n1\n")
    events = ledger.list_events("w")
    represented = next(e for e in events if e.kind.endswith("alternatives_represented"))
    response = next(e for e in events if e.kind.endswith("response_captured"))
    assert events.index(represented) < events.index(response)
    row = represented.payload["representations"][0]
    assert (
        len(
            {
                "1",
                row["presented_alternative_ref"],
                row["represented_source_ref"],
                row["rendered_label"],
                row["proposition_assertion"],
            }
        )
        == 5
    )
    assert (
        row["representation_relation"]
        == "presented_alternative_represents_application_owned_source"
    )
    assert row["exact_set_participation"] == (
        "participates_in_exact_presented_choice_set_for_declared_purpose"
    )
    assert row["rendered_label"] != row["proposition_assertion"]
    assert row["known_loss"] == (
        "rendered label is a compressed presentation and does not carry the complete source proposition",
    )
    assert (
        row["producer_occurrence_ref"] == represented.payload["dimensions"]["identity"]
    )
    assert (
        view["current_standing"]["alternative_representations"]["evidence_event_id"]
        == represented.id
    )


def test_recovery_consumes_recorded_occurrence_and_preserves_full_lineage():
    ledger, _, _ = run_attempt("unknown request\n1\n")
    events = ledger.list_events("w")
    represented = next(e for e in events if e.kind.endswith("alternatives_represented"))
    presentation = next(e for e in events if e.kind.endswith("presentation_occurred"))
    response = next(e for e in events if e.kind.endswith("response_captured"))
    binding = next(e for e in events if e.kind.endswith("binding_completed"))
    selection = next(e for e in events if e.kind.endswith("alternative_selected"))
    recovery = next(e for e in events if e.kind.endswith("source_recovered"))
    assert recovery.payload["representation_occurrence_id"] == represented.id
    assert recovery.payload["binding_occurrence_id"] == binding.id
    assert recovery.payload["lineage"] == [
        represented.id,
        presentation.id,
        binding.id,
        selection.id,
    ]
    assert response.id in binding.payload["lineage"]
    assert (
        tuple(recovery.payload["known_loss"])
        == represented.payload["representations"][0]["known_loss"]
    )
    projected = (
        StateProjector(ledger)
        .project("w")
        .operator_ingress_common_grammar_attempts[represented.payload["attempt_ref"]]
    )
    assert RENDERING_KNOWN_LOSS[0] in projected["known_loss"]


@pytest.mark.parametrize("token", ["1", "2"])
def test_testimony_and_convention_are_distinct_inputs_to_exact_warrant(token):
    ledger, view, _ = run_attempt(f"unknown request\n{token}\n")
    events = ledger.list_events("w")
    recovery = next(e for e in events if e.kind.endswith("source_recovered"))
    warrant = next(e for e in events if e.kind.endswith("meaning_relation_warranted"))
    testimony = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    convention = SOURCE_MEANING_CONVENTIONS[recovery.payload["recovered_source_ref"]]
    assert convention is APPLICATION_SOURCE_MEANING_CONVENTION
    assert not hasattr(convention, "source_ref") and not hasattr(
        convention, "proposition"
    )
    assert warrant.payload["meaning_testimony_ref"] == testimony.testimony_id
    assert warrant.payload["constitutive_convention_ref"] == convention.convention_id
    assert warrant.payload["source_recovery_occurrence_id"] == recovery.id
    assert warrant.payload["relation_assertion"] == "expresses"
    assert warrant.payload["source_ref"] == testimony.source_ref
    assert warrant.payload["proposition"] == testimony.proposition
    assert "implementation_status" not in warrant.payload
    assert "not_established" not in warrant.payload
    assert warrant.payload["lineage"][-1] == recovery.id
    assert RENDERING_KNOWN_LOSS[0] in warrant.payload["known_loss"]
    assert view["meaning_testimony_ref"] == testimony.testimony_id
    assert view["constitutive_convention_ref"] == convention.convention_id
    assert view.get("bounded_goal") is None and view.get("closed") is None


def test_potential_goal_relation_reaches_consumer_boundary_as_unknown():
    ledger, view, _ = run_attempt("unknown request\n1\n")
    events = ledger.list_events("w")
    warrant = next(e for e in events if e.kind.endswith("meaning_relation_warranted"))
    finding = next(e for e in events if e.kind.endswith("applicability_examined"))
    assert warrant.payload["source_role"] == "potential-goal candidate"
    assert finding.payload["applicability"] == "unknown"
    assert finding.payload["condition_evidence"] == []
    assert finding.payload["meaning_relation_warrant_occurrence"] == warrant.model_dump(
        mode="json"
    )
    assert (
        view["current_standing"]["bounded_operator_goal_establishment_applicability"][
            "evidence_event_id"
        ]
        == finding.id
    )
    assert not any(
        "admission" in event.kind or event.kind.endswith(".goal_established")
        for event in events
    )


def test_local_stop_relation_has_no_bounded_goal_applicability_or_stopping():
    ledger, view, _ = run_attempt("unknown request\n2\n")
    events = ledger.list_events("w")
    warrant = next(e for e in events if e.kind.endswith("meaning_relation_warranted"))
    assert warrant.payload["source_role"] == "local-stop"
    assert (
        view["current_standing"]["meaning_relation"]["evidence_event_id"] == warrant.id
    )
    assert (
        view["current_standing"]["bounded_operator_goal_establishment_applicability"]
        is None
    )
    assert not any(
        "applicability" in event.kind or "stopping" in event.kind for event in events
    )


def test_unrecorded_relation_is_refused_without_inapplicability():
    ledger, _, _ = run_attempt("unknown request\n1\n")
    warrant = next(
        e
        for e in ledger.list_events("w")
        if e.kind.endswith("meaning_relation_warranted")
    )
    forged = warrant.model_copy(update={"id": "event:forged"})
    refusal = _examine_meaning_relation_for_bounded_operator_goal_establishment(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref=warrant.payload["attempt_ref"],
        meaning_relation=forged,
    )
    assert refusal.payload["applicability"] == "unknown"
    assert (
        refusal.payload["refusal_reason"]
        == "supplied_meaning_relation_is_not_exact_recorded_warrant"
    )


def _rewarrant(ledger, recovery, *, testimony=None, convention=None):
    return _warrant_source_meaning_relation(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref=recovery.payload["attempt_ref"],
        source_recovery=recovery,
        testimony=testimony,
        convention=convention,
    )


@pytest.mark.parametrize(
    "change,reason",
    [
        ({"testimony_id": "wrong"}, "meaning_testimony_identity_mismatch"),
        ({"source_ref": "source:wrong"}, "meaning_testimony_identity_mismatch"),
        ({"source_role": "wrong"}, "source_role_mismatch"),
        ({"proposition": "changed"}, "proposition_mismatch"),
        (
            {"relation_assertion": "identifies"},
            "meaning_testimony_relation_not_expresses",
        ),
        (
            {"attributed_supplier": ""},
            "meaning_testimony_attribution_absent_or_mismatched",
        ),
        (
            {"producer_declaration_ref": ""},
            "meaning_testimony_declaration_reference_absent",
        ),
        ({"provenance": ()}, "meaning_testimony_provenance_absent"),
        (
            {"declared_application_purpose": "wrong"},
            "meaning_testimony_purpose_mismatch",
        ),
        ({"scope": "wrong"}, "meaning_testimony_scope_mismatch"),
        ({"unknowns": ("unknown",)}, "meaning_testimony_unknown"),
        ({"conflicts": ("conflict",)}, "meaning_testimony_conflicting"),
    ],
)
def test_changed_or_incomplete_testimony_refuses(change, reason):
    ledger, _, _ = run_attempt("unknown request\n1\n")
    recovery = next(
        e for e in ledger.list_events("w") if e.kind.endswith("source_recovered")
    )
    testimony = replace(
        SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]], **change
    )
    assert (
        _rewarrant(
            ledger,
            recovery,
            testimony=testimony,
            convention=APPLICATION_SOURCE_MEANING_CONVENTION,
        ).payload["refusal_reason"]
        == reason
    )


@pytest.mark.parametrize(
    "change,reason",
    [
        ({"convention_id": "wrong"}, "constitutive_convention_identity_mismatch"),
        (
            {"attribution": ""},
            "constitutive_convention_attribution_absent_or_mismatched",
        ),
        ({"applicable_authority": ()}, "constitutive_convention_authority_absent"),
        (
            {"permitted_testimony_kind": "Other"},
            "constitutive_convention_testimony_form_not_permitted",
        ),
        (
            {"permitted_relation_form": "represents"},
            "constitutive_convention_does_not_permit_expresses",
        ),
        ({"purpose": ""}, "constitutive_convention_purpose_mismatch"),
        ({"scope": ""}, "constitutive_convention_scope_mismatch"),
        ({"unknowns": ("unknown",)}, "constitutive_convention_unknown"),
        ({"conflicts": ("conflict",)}, "constitutive_convention_conflicting"),
    ],
)
def test_changed_or_incomplete_convention_refuses(change, reason):
    ledger, _, _ = run_attempt("unknown request\n1\n")
    recovery = next(
        e for e in ledger.list_events("w") if e.kind.endswith("source_recovered")
    )
    convention = replace(APPLICATION_SOURCE_MEANING_CONVENTION, **change)
    testimony = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    assert (
        _rewarrant(
            ledger, recovery, testimony=testimony, convention=convention
        ).payload["refusal_reason"]
        == reason
    )


def test_missing_inputs_other_source_and_forged_recovery_refuse_without_negation():
    ledger, _, _ = run_attempt("unknown request\n1\n")
    recovery = next(
        e for e in ledger.list_events("w") if e.kind.endswith("source_recovered")
    )
    exact = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    assert (
        _rewarrant(
            ledger,
            recovery,
            testimony=None,
            convention=APPLICATION_SOURCE_MEANING_CONVENTION,
        ).payload["refusal_reason"]
        == "missing_meaning_testimony"
    )
    assert (
        _rewarrant(ledger, recovery, testimony=exact, convention=None).payload[
            "refusal_reason"
        ]
        == "missing_constitutive_convention"
    )
    other = SOURCE_MEANING_TESTIMONIES["source:operator-common-grammar-local-stop:v1"]
    assert (
        _rewarrant(
            ledger,
            recovery,
            testimony=other,
            convention=APPLICATION_SOURCE_MEANING_CONVENTION,
        ).payload["refusal_reason"]
        == "source_identity_mismatch"
    )
    forged = recovery.model_copy(deep=True)
    forged.payload["recovered_source_proposition"] = "forged"
    refusal = _rewarrant(
        ledger,
        forged,
        testimony=exact,
        convention=APPLICATION_SOURCE_MEANING_CONVENTION,
    )
    assert (
        refusal.payload["refusal_reason"]
        == "supplied_source_recovery_is_not_recorded_occurrence"
    )
    assert "remains Unknown" in refusal.payload["unknowns"][0]


def test_missing_duplicate_and_unknown_upstream_recovery_refuse():
    empty = EventLedger()
    refusal = _warrant_source_meaning_relation(
        ledger=empty,
        workspace_id="w",
        session_id="s",
        attempt_ref="missing",
        source_recovery=None,
        testimony=None,
        convention=None,
    )
    assert (
        refusal.payload["refusal_reason"]
        == "no_exact_recorded_source_recovery_occurrence"
    )
    ledger, _, _ = run_attempt("unknown request\n1\n", session="upstream")
    recovery = next(
        e for e in ledger.list_events("w") if e.kind.endswith("source_recovered")
    )
    testimony = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    representation = ledger.get(recovery.payload["representation_occurrence_id"])
    representation.payload["unknowns"] = ["relevant representation Unknown"]
    refusal = _warrant_source_meaning_relation(
        ledger=ledger,
        workspace_id="w",
        session_id="upstream",
        attempt_ref=recovery.payload["attempt_ref"],
        source_recovery=recovery,
        testimony=testimony,
        convention=APPLICATION_SOURCE_MEANING_CONVENTION,
    )
    assert refusal.payload["refusal_reason"] == "upstream_representation_unknown"


@pytest.mark.parametrize(
    "token,alternative",
    [("1", "common-grammar-acquisition"), ("2", "local-stop")],
)
def test_exact_alternatives_recover_sources_without_goal_or_stop(token, alternative):
    ledger, view, output = run_attempt(f"do something exactly\n{token}\n")
    assert view["selected_presented_alternative_ref"] == alternative
    assert view.get("closed") is None
    kinds = [event.kind for event in ledger.list_events("w")]
    assert "operator.ingress.common_grammar.alternative_selected" in kinds
    assert "operator.ingress.common_grammar.source_recovered" in kinds
    assert "operator.ingress.common_grammar.stopping_occurred" not in kinds
    source_ref = ALTERNATIVE_SOURCES[alternative]
    assert view["recovered_source_ref"] == source_ref
    assert view["recovered_source_role"] == SOURCE_PROPOSITIONS[source_ref][0]
    assert view["recovered_source_proposition"] == SOURCE_PROPOSITIONS[source_ref][1]
    assert view.get("bounded_goal") is None
    assert not any(
        any(
            word in event.kind
            for word in ("demand", "acquisition", "interpretation", "cluster")
        )
        for event in ledger.list_events("w")
    )
    assert "1. Select bounded common-grammar acquisition alternative." in output


@pytest.mark.parametrize(
    "token", ["", " ", "1 ", " 1", "ONE", "Acquisition", "01", "2 "]
)
def test_near_matches_and_empty_are_unsupported_with_semantic_unknowns(token):
    ledger, view, output = run_attempt(f"hello\n{token}\n")
    assert (
        view["current_standing"]["binding_finding"]["dimensions"]["standing"]
        == "unsupported"
    )
    assert view["unknowns"] == [
        "operator intent Unknown",
        "requested alternative Unknown",
        "response meaning Unknown",
    ]
    assert "Unsupported response" in output
    assert not any(
        event.kind == "operator.ingress.common_grammar.alternative_selected"
        for event in ledger.list_events()
    )
    assert not any(
        event.kind == "operator.ingress.common_grammar.stopping_occurred"
        for event in ledger.list_events()
    )


def test_eof_is_distinct_from_empty_response():
    eof_ledger, eof, _ = run_attempt("hello\n")
    _, empty, _ = run_attempt("hello\n\n", session="empty")
    assert eof["response_kind"] == "eof"
    assert empty["response_kind"] == "empty"
    eof_kinds = [event.kind for event in eof_ledger.list_events("w")]
    assert "operator.ingress.common_grammar.response_eof_occurred" in eof_kinds
    assert "operator.ingress.common_grammar.stopping_occurred" in eof_kinds
    assert "operator.ingress.common_grammar.response_captured" not in eof_kinds
    assert "operator.ingress.common_grammar.binding_completed" not in eof_kinds
    assert "operator.ingress.common_grammar.unsupported_finding" not in eof_kinds
    assert "capture_ref" not in eof
    assert "binding_id" not in eof


def test_initial_eof_records_eof_and_separate_stop_without_probe():
    ledger, view, output = run_attempt("")
    assert [event.kind for event in ledger.list_events("w")] == [
        "operator.ingress.common_grammar.raw_material_captured",
        "operator.ingress.common_grammar.initial_eof_occurred",
        "operator.ingress.common_grammar.stopping_occurred",
    ]
    assert view["representation_examinations"] == {}
    assert view["closed"] is True
    assert (
        view["current_standing"]["interaction_closure"]["dimensions"]["standing"]
        == "closed"
    )
    assert output == "Operator-ingress common-grammar interaction stopped locally.\n"
    stop = ledger.list_events("w")[-1]
    assert stop.payload["dimensions"]["authority_warrant"] == (
        "closes only this interaction"
    )


def test_exact_ingress_preservation_all_dimensions_and_durable_replay(tmp_path):
    path = tmp_path / "events.db"
    ledger, view, _ = run_attempt(
        "  Mixed CASE ingress  \n2\n", SQLiteEventLedger(str(path))
    )
    ingress = next(
        e
        for e in ledger.list_events("w")
        if e.kind == "operator.ingress.common_grammar.ingress_occurred"
    )
    assert ingress.payload["raw_input"] == "  Mixed CASE ingress  \n"
    assert ingress.payload["known_loss"] == [
        "original transport bytes and prior decoder behavior are unavailable"
    ]
    assert len(view["dimensional_standing"]) == 15
    assert all(
        set(item["dimensions"])
        == {
            "identity",
            "content",
            "standing",
            "source_provenance",
            "responsibility",
            "authority_warrant",
            "scope_locality",
            "occurrence_preservation",
        }
        for item in view["dimensional_standing"].values()
    )
    assert all(
        item["lineage"] for item in list(view["dimensional_standing"].values())[1:]
    )
    assert (
        view["current_standing"]["presentation"]["dimensions"]["standing"] == "consumed"
    )
    assert view["current_standing"]["response"]["dimensions"]["standing"] == "consumed"
    assert (
        view["current_standing"]["binding_finding"]["dimensions"]["standing"] == "bound"
    )
    assert (
        view["current_standing"]["presentation"]["dimensions"]["standing"] == "consumed"
    )
    assert (
        view["current_standing"]["raw_response_material"]["dimensions"]["standing"]
        == "captured"
    )
    attempt_ref = ingress.payload["attempt_ref"]
    ledger.close()
    reopened = SQLiteEventLedger(str(path))
    replayed = (
        StateProjector(reopened)
        .project("w")
        .operator_ingress_common_grammar_attempts[attempt_ref]
    )
    assert replayed == view
    assert all(
        event.payload["mutates_cluster"] is False for event in reopened.list_events("w")
    )


@pytest.mark.parametrize(
    "text,present,response,binding,alternative,closure",
    [
        ("hello\n1\n", "consumed", "consumed", "bound", "selected", None),
        ("hello\nwat\n", "consumed", "consumed", "unsupported", None, None),
        ("hello\n2\n", "consumed", "consumed", "bound", "selected", None),
        ("", None, None, None, None, "closed"),
        ("hello\n", "consumed", "occurred", None, None, "closed"),
    ],
)
def test_subject_local_current_standing_is_asymmetric(
    text, present, response, binding, alternative, closure
):
    _, view, _ = run_attempt(text)

    def standing(subject):
        current = view["current_standing"][subject]
        return current and current["dimensions"]["standing"]

    assert standing("preserved_ingress") == "preserved"
    assert standing("presentation") == present
    assert standing("response") == response
    assert standing("binding_finding") == binding
    assert standing("alternative_selection") == alternative
    assert standing("interaction_closure") == closure


def _recorded_probe_inputs(ledger):
    events = ledger.list_events("w")
    ingress = events[0]
    response = next(
        e
        for e in events
        if e.kind == "operator.ingress.common_grammar.response_captured"
    )
    choice = common_grammar_choice_set(response.payload["presentation_ref"])
    capture = OperatorSelectionTokenCapture(
        response.payload["capture_ref"], CHOICE_SET_REF, "1"
    )
    return ingress.payload["attempt_ref"], choice, capture


def test_probe_identity_fingerprint_and_consumption_guards():
    ledger, _, _ = run_attempt("hello\n1\n")
    attempt, choice, capture = _recorded_probe_inputs(ledger)
    with pytest.raises(ClosedChoiceSelectionBindingError):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=common_grammar_choice_set("presentation:wrong"),
            capture=capture,
        )
    wrong_set_capture = OperatorSelectionTokenCapture(
        capture.capture_ref, "goal-choice-set:wrong", capture.captured_token
    )
    with pytest.raises(ClosedChoiceSelectionBindingError):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=choice,
            capture=wrong_set_capture,
        )
    altered = PresentedClosedChoiceSet(
        CHOICE_SET_REF,
        choice.prompt,
        (ClosedChoiceOption("1", "different", "Different"), *choice.options[1:]),
        choice.presentation_ref,
    )
    with pytest.raises(ClosedChoiceSelectionBindingError):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=altered,
            capture=capture,
        )
    with pytest.raises(ClosedChoiceSelectionBindingError, match="already consumed"):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=choice,
            capture=capture,
        )


def test_communication_binding_lacks_positive_boge_admission():
    ledger, view, _ = run_attempt("hello\n1\n")
    attempt, choice, capture = _recorded_probe_inputs(ledger)
    binding_event = next(
        e
        for e in ledger.list_events("w")
        if e.kind == "operator.ingress.common_grammar.binding_completed"
    )
    # Re-create the immutable binding only to exercise the downstream boundary;
    # production already consumed this capture and records the same binding identity.
    from seed_runtime.closed_choice_selection_binding import (
        bind_closed_choice_selection,
    )

    binding = bind_closed_choice_selection(choice, capture)
    assert (
        binding.binding_id == binding_event.payload["binding_id"] == view["binding_id"]
    )
    with pytest.raises(BoundedOperatorGoalEstablishmentError):
        establish_bounded_operator_goal_from_closed_choice(binding)


def test_two_durable_attempts_in_same_session_remain_distinct(tmp_path):
    path = tmp_path / "attempts.db"
    ledger = SQLiteEventLedger(str(path))
    _, first, _ = run_attempt("first\n1\n", ledger, session="same")
    _, second, _ = run_attempt("second\n2\n", ledger, session="same")
    attempt_refs = {e.payload["attempt_ref"] for e in ledger.list_events("w")}
    assert len(attempt_refs) == 2
    assert first["event_ids"] != second["event_ids"]
    ledger.close()
    reopened = SQLiteEventLedger(str(path))
    projection = (
        StateProjector(reopened).project("w").operator_ingress_common_grammar_attempts
    )
    assert set(projection) == attempt_refs
    assert {
        view["selected_presented_alternative_ref"] for view in projection.values()
    } == {
        "common-grammar-acquisition",
        "local-stop",
    }


def test_consumed_capture_replay_is_refused_after_durable_reconstruction(tmp_path):
    path = tmp_path / "replay.db"
    ledger, _, _ = run_attempt("hello\n1\n", SQLiteEventLedger(str(path)))
    attempt, choice, capture = _recorded_probe_inputs(ledger)
    ledger.close()
    reopened = SQLiteEventLedger(str(path))
    with pytest.raises(ClosedChoiceSelectionBindingError, match="already consumed"):
        validate_capture_for_probe(
            ledger=reopened,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=choice,
            capture=capture,
        )


class _RawStdin:
    def __init__(self, material: bytes, encoding="utf-8"):
        self.buffer = BytesIO(material)
        self.encoding = encoding


def run_raw(material: bytes, *, ledger=None):
    ledger = ledger or EventLedger()
    output = StringIO()
    input_stream = _RawStdin(material)
    captured_ingress = capture_stdin_material(input_stream)
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="raw-w",
        session_id="raw-s",
        captured_ingress=captured_ingress,
        response_input_stream=input_stream,
        output_stream=output,
    )
    return ledger, view, output.getvalue()


def run_console(material: bytes):
    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="console-w",
        session_id="console-s",
        input_stream=_RawStdin(material),
        output_stream=output,
    )
    return ledger, output.getvalue()


def test_bare_seed_enters_persistent_console_and_announces_exit():
    completed = subprocess.run(
        [sys.executable, "scripts/seed_local.py"],
        input=b"exit\n",
        capture_output=True,
        check=True,
    )
    assert completed.stdout == b"Seed console: `exit` exits.\n"
    assert completed.returncode == 0


def test_console_passes_its_capture_unchanged_to_the_bounded_attempt(monkeypatch):
    supplied = _RawStdin(b"ordinary ingress\r\n2\nexit\n")
    received = []

    def bounded_attempt(**kwargs):
        received.append(kwargs)
        # Response ownership remains inside the bounded attempt.
        assert kwargs["response_input_stream"].buffer.readline() == b"2\n"

    monkeypatch.setattr(
        seed_local,
        "run_operator_ingress_common_grammar_probe_attempt",
        bounded_attempt,
    )
    seed_local.run_persistent_operator_console(
        ledger=EventLedger(),
        workspace_id="w",
        session_id="s",
        input_stream=supplied,
        output_stream=StringIO(),
    )

    assert len(received) == 1
    capture = received[0]["captured_ingress"]
    assert capture.exact_bytes == b"ordinary ingress\r\n"
    assert capture.delimiter_hex == "0d0a"
    assert capture.capture_boundary == "stdin.buffer.readline"
    assert capture.byte_material_origin == "direct_boundary_observation"
    assert received[0]["response_input_stream"] is supplied


def test_existing_capture_provenance_is_recorded_without_reinference():
    capture = CapturedOperatorMaterial(
        exact_bytes=b"captured elsewhere\n",
        eof=False,
        delimiter_hex="0a",
        capture_boundary="explicit-test-boundary",
        byte_material_origin="explicit-test-origin",
        encoding_testimony="utf-8",
        known_loss=("explicit-test-loss",),
    )
    ledger = EventLedger()
    run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture,
        response_input_stream=BytesIO(b"2\n"),
        output_stream=StringIO(),
    )
    recorded = ledger.list_events("w")[0].payload
    assert recorded["capture_boundary"] == capture.capture_boundary
    assert recorded["byte_material_origin"] == capture.byte_material_origin
    assert recorded["exact_bytes_hex"] == capture.exact_bytes.hex()
    assert recorded["known_loss"] == list(capture.known_loss)


def test_parser_has_no_alternate_operator_ingress_controller():
    parser = seed_local.build_parser()
    assert not any(
        action.dest == "operator_ingress_common_grammar" for action in parser._actions
    )


def test_console_runs_multiple_bounded_interactions_after_local_stop_and_unsupported():
    ledger, output = run_console(
        b"first ingress\n2\nsecond ingress\nnot-a-token\nexit\n"
    )
    attempts = (
        StateProjector(ledger)
        .project("console-w")
        .operator_ingress_common_grammar_attempts
    )
    assert len(attempts) == 2
    assert {
        view.get("selected_presented_alternative_ref") for view in attempts.values()
    } == {
        "local-stop",
        None,
    }
    assert any(
        view.get("current_standing", {})
        .get("binding_finding", {})
        .get("dimensions", {})
        .get("standing")
        == "unsupported"
        for view in attempts.values()
    )
    assert output.count("Select one alternative by its exact token:") == 2
    assert "Local-stop source recovered; bounded stop was not established." in output
    assert "Unsupported response" in output


def test_outer_exit_is_not_operator_ingress_and_capture_keeps_provenance():
    ledger, _ = run_console(b"\xff\nexit\n")
    events = ledger.list_events("console-w")
    captures = [
        event
        for event in events
        if event.kind == "operator.ingress.common_grammar.raw_material_captured"
    ]
    assert len(captures) == 1
    assert captures[0].payload["exact_bytes_hex"] == "ff0a"
    assert captures[0].payload["capture_boundary"] == "stdin.buffer.readline"
    assert captures[0].payload["byte_material_origin"] == "direct_boundary_observation"
    assert b"exit\n".hex() not in str([event.payload for event in events])


def test_stdin_buffer_capture_preserves_exact_boundary_bytes_and_decoder_testimony(
    tmp_path,
):
    path = tmp_path / "raw.db"
    ledger, view, _ = run_raw("é\r\n2\n".encode(), ledger=SQLiteEventLedger(str(path)))
    raw, examination = ledger.list_events("raw-w")[:2]
    assert raw.payload["exact_bytes_hex"] == "é\r\n".encode().hex()
    assert raw.payload["delimiter_hex"] == "0d0a"
    assert raw.payload["capture_boundary"] == "stdin.buffer.readline"
    assert raw.payload["byte_material_origin"] == "direct_boundary_observation"
    assert raw.payload["encoding_testimony"] == "utf-8"
    assert examination.kind == "operator.ingress.common_grammar.representation_examined"
    assert examination.payload["decoder_mechanism"] == "utf-8"
    assert examination.payload["decoder_succeeded"] is True
    assert examination.payload["decoder_failure"] is None
    projected = view["representation_examinations"]["initial_ingress"]
    assert projected["decoder_succeeded"] is True
    assert "admission" not in projected
    assert "competency" not in str(projected).lower()
    ledger.close()
    replay = StateProjector(SQLiteEventLedger(str(path))).project("raw-w")
    assert (
        replay.operator_ingress_common_grammar_attempts[
            next(iter(replay.operator_ingress_common_grammar_attempts))
        ]
        == view
    )


def test_stringio_capture_identifies_text_reencoding_and_preserves_known_loss():
    ledger, _, _ = run_attempt("hello\n2\n")
    raw = ledger.list_events("w")[0]
    assert raw.payload["exact_bytes_hex"] == b"hello\n".hex()
    assert raw.payload["byte_material_origin"] == "text_reencoding_after_prior_decoding"
    assert raw.payload["encoding_testimony"] is None
    assert raw.payload["capture_boundary"] == "text-stream adapter after prior decoding"
    assert raw.payload["known_loss"] == [
        "original transport bytes and prior decoder behavior are unavailable"
    ]
    examination = ledger.list_events("w")[1]
    assert examination.payload["decoder_mechanism"] == "utf-8"
    assert (
        examination.payload["decoder_mechanism_selection"]
        == "implementation_utf8_fallback"
    )
    assert examination.payload["decoder_outcome"] == "decoded"


def test_decoder_success_does_not_claim_admission_interpretation_or_competency():
    ledger, view, _ = run_raw(b"ASCII\n2\n")
    examination = ledger.list_events("raw-w")[1]
    assert examination.payload["decoder_succeeded"] is True
    forbidden = ("admission", "admitted", "interpretation", "competency")
    assert not any(word in str(examination.payload).lower() for word in forbidden)
    assert not any(
        word in str(view["representation_examinations"]).lower() for word in forbidden
    )


def test_production_operator_ingress_contains_no_pesc_identifier_or_payload():
    forbidden = "pe" + "sc"
    production = Path(
        "seed_runtime/operator_ingress_common_grammar_prerequisite.py"
    ).read_text()
    production += Path("seed_runtime/operator_ingress_representation.py").read_text()
    assert forbidden not in production.lower()


def test_production_and_event_payloads_do_not_claim_source_relative_original_bytes():
    forbidden = "original_transport" + "_bytes"
    production = Path(
        "seed_runtime/operator_ingress_common_grammar_prerequisite.py"
    ).read_text()
    production += Path("seed_runtime/operator_ingress_representation.py").read_text()
    assert forbidden not in production

    ledgers = (run_raw(b"hello\n2\n")[0], run_attempt("hello\n2\n")[0])
    for ledger in ledgers:
        assert forbidden not in str([event.payload for event in ledger.list_events()])


def test_invalid_initial_bytes_are_preserved_without_replacement_and_stop_before_enum():
    ledger, view, output = run_raw(b"\xff\n1\n")
    assert output == (
        "Representation insufficient: captured material did not decode under "
        "the selected decoder mechanism.\n"
    )
    events = ledger.list_events("raw-w")
    assert events[0].payload["exact_bytes_hex"] == "ff0a"
    assert events[1].payload["decoder_succeeded"] is False
    assert "\ufffd" not in str([event.payload for event in events])
    assert not any(
        e.kind
        in {
            "operator.ingress.common_grammar.probe_produced",
            "operator.ingress.common_grammar.presentation_occurred",
            "operator.ingress.common_grammar.response_captured",
            "operator.ingress.common_grammar.binding_completed",
        }
        for e in events
    )
    assert (
        view["representation_examinations"]["initial_ingress"]["decoder_succeeded"]
        is False
    )


def test_invalid_enum_bytes_stop_before_token_capture_or_binding():
    ledger, _, output = run_raw(b"hello\n\xff\n")
    assert "Select one alternative" in output
    assert output.endswith(
        "Representation insufficient: captured response did not decode under the selected decoder mechanism.\n"
    )
    events = ledger.list_events("raw-w")
    assert not any(
        e.kind
        in {
            "operator.ingress.common_grammar.response_captured",
            "operator.ingress.common_grammar.binding_completed",
            "operator.ingress.common_grammar.unsupported_finding",
        }
        for e in events
    )
    assert not any(
        any(
            term in e.kind
            for term in (
                "demand",
                "acquisition",
                "bounded-goal-applicability",
                "cluster",
            )
        )
        for e in events
    )


def test_empty_material_and_eof_have_distinct_raw_evidence():
    empty_ledger, _, _ = run_raw(b"\n2\n")
    eof_ledger, _, _ = run_raw(b"")
    empty = empty_ledger.list_events("raw-w")[0].payload
    eof = eof_ledger.list_events("raw-w")[0].payload
    assert (empty["exact_bytes_hex"], empty["eof"], empty["delimiter_hex"]) == (
        "0a",
        False,
        "0a",
    )
    assert (eof["exact_bytes_hex"], eof["eof"], eof["delimiter_hex"]) == (
        "",
        True,
        None,
    )


def test_initial_and_response_eof_do_not_claim_representation_examination():
    initial_ledger, initial_view, _ = run_raw(b"")
    response_ledger, response_view, _ = run_raw(b"hello\n")
    assert not any(
        event.kind == "operator.ingress.common_grammar.representation_examined"
        for event in initial_ledger.list_events("raw-w")
    )
    response_examinations = [
        event
        for event in response_ledger.list_events("raw-w")
        if event.kind == "operator.ingress.common_grammar.representation_examined"
    ]
    assert [event.payload["material_role"] for event in response_examinations] == [
        "initial_ingress"
    ]
    assert initial_view["representation_examinations"] == {}
    assert "enum_response" not in response_view["representation_examinations"]
    eof_event = next(
        event
        for event in response_ledger.list_events("raw-w")
        if event.kind == "operator.ingress.common_grammar.response_eof_occurred"
    )
    raw_response = next(
        event
        for event in response_ledger.list_events("raw-w")
        if event.kind == "operator.ingress.common_grammar.raw_material_captured"
        and event.payload["material_role"] == "enum_response"
    )
    assert raw_response.id in eof_event.payload["lineage"]


def test_decoder_outcomes_and_selection_sources_remain_distinct():
    unavailable_ledger, _, _ = run_operator_with_stream(
        _RawStdin(b"hello\n", "x-no-such-codec")
    )
    rejected_ledger, _, _ = run_raw(b"\xff\n")
    success_ledger, _, _ = run_raw(b"hello\n2\n")
    unavailable = unavailable_ledger.list_events("raw-w")[1].payload
    rejected = rejected_ledger.list_events("raw-w")[1].payload
    success = success_ledger.list_events("raw-w")[1].payload
    assert unavailable["decoder_outcome"] == "decoder_unavailable"
    assert unavailable["decoder_mechanism_selection"] == "stream_encoding_testimony"
    assert unavailable["decoder_failure"].startswith("LookupError:")
    assert rejected["decoder_outcome"] == "bytes_rejected"
    assert rejected["decoder_failure"].startswith("UnicodeDecodeError:")
    assert success["decoder_outcome"] == "decoded"
    assert success["decoder_failure"] is None

    for ledger, expected in (
        (unavailable_ledger, "decoder_unavailable"),
        (rejected_ledger, "bytes_rejected"),
        (success_ledger, "decoded"),
    ):
        examination = ledger.list_events("raw-w")[1]
        assert examination.payload["dimensions"]["standing"] == expected


def run_operator_with_stream(stream):
    ledger = EventLedger()
    output = StringIO()
    captured_ingress = capture_stdin_material(stream)
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="raw-w",
        session_id="raw-s",
        captured_ingress=captured_ingress,
        response_input_stream=stream,
        output_stream=output,
    )
    return ledger, view, output.getvalue()


def test_utf8_fallback_is_implementation_selected_and_direct_bytesio_is_exact():
    ledger, _, _ = run_operator_with_stream(BytesIO(b"\xc3\xa9\n2\n"))
    raw, examination = ledger.list_events("raw-w")[:2]
    assert raw.payload["exact_bytes_hex"] == b"\xc3\xa9\n".hex()
    assert raw.payload["byte_material_origin"] == "direct_boundary_observation"
    assert (
        raw.payload["capture_boundary"]
        == "binary-stream.readline (bytes observed directly)"
    )
    assert raw.payload["encoding_testimony"] is None
    assert examination.payload["decoder_mechanism"] == "utf-8"
    assert (
        examination.payload["decoder_mechanism_selection"]
        == "implementation_utf8_fallback"
    )


def test_representation_evidence_produces_no_broader_standing():
    ledger, view, _ = run_raw(b"hello\n2\n")
    evidence = str(
        [
            event.payload
            for event in ledger.list_events("raw-w")
            if event.kind
            in {
                "operator.ingress.common_grammar.raw_material_captured",
                "operator.ingress.common_grammar.representation_examined",
            }
        ]
        + [view["representation_examinations"]]
    ).lower()
    assert not any(
        word in evidence
        for word in (
            "admission",
            "interpretation",
            "competency",
            "demand",
            "bounded-goal-applicability",
        )
    )


@pytest.mark.parametrize(
    "mutation,reason",
    [
        (lambda event: None, "no_recorded_representation_occurrence"),
        (
            lambda event: event.model_copy(
                update={"payload": {**event.payload, "attempt_ref": "wrong-attempt"}}
            ),
            "wrong_attempt",
        ),
        (
            lambda event: event.model_copy(
                update={
                    "payload": {
                        **event.payload,
                        "presentation_ref": "wrong-presentation",
                    }
                }
            ),
            "wrong_presentation",
        ),
        (
            lambda event: event.model_copy(
                update={"payload": {**event.payload, "choice_set_ref": "wrong-set"}}
            ),
            "wrong_choice_set",
        ),
        (
            lambda event: event.model_copy(
                update={"payload": {**event.payload, "choice_set_fingerprint": "wrong"}}
            ),
            "wrong_set_fingerprint",
        ),
        (
            lambda event: event.model_copy(
                update={
                    "payload": {
                        **event.payload,
                        "representations": [
                            {
                                **event.payload["representations"][0],
                                "represented_source_ref": "source:forged",
                            },
                            *event.payload["representations"][1:],
                        ],
                    }
                }
            ),
            "forged_relation_payload",
        ),
    ],
)
def test_recovery_refuses_missing_or_mismatched_recorded_evidence(mutation, reason):
    ledger, _, _ = run_attempt("unknown request\n1\n")
    events = ledger.list_events("w")
    occurrence = next(e for e in events if e.kind.endswith("alternatives_represented"))
    presentation = next(e for e in events if e.kind.endswith("presentation_occurred"))
    response = next(e for e in events if e.kind.endswith("response_captured"))
    attempt = occurrence.payload["attempt_ref"]
    choice = common_grammar_choice_set(occurrence.payload["presentation_ref"])
    binding = bind_closed_choice_selection(
        choice,
        OperatorSelectionTokenCapture(
            response.payload["capture_ref"],
            CHOICE_SET_REF,
            "1",
            provenance=(response.id,),
        ),
    )
    recovered, refusal = _recover_represented_source(
        binding,
        choice,
        mutation(occurrence),
        ledger=ledger,
        workspace_id="w",
        attempt_ref=attempt,
        presentation_occurrence=presentation,
        selection_occurrence=next(
            e for e in events if e.kind.endswith("alternative_selected")
        ),
    )
    assert recovered is None
    assert refusal == reason


def _recover_after_binding_event_mutation(mutate):
    ledger, _, _ = run_attempt("unknown request\n1\n")
    events = ledger.list_events("w")
    represented = next(e for e in events if e.kind.endswith("alternatives_represented"))
    presentation = next(e for e in events if e.kind.endswith("presentation_occurred"))
    response = next(e for e in events if e.kind.endswith("response_captured"))
    binding_event = next(e for e in events if e.kind.endswith("binding_completed"))
    selection = next(e for e in events if e.kind.endswith("alternative_selected"))
    choice = common_grammar_choice_set(represented.payload["presentation_ref"])
    binding = bind_closed_choice_selection(
        choice,
        OperatorSelectionTokenCapture(
            response.payload["capture_ref"],
            CHOICE_SET_REF,
            "1",
            provenance=(response.id,),
        ),
    )
    mutate(ledger, binding_event, selection)
    return _recover_represented_source(
        binding,
        choice,
        represented,
        ledger=ledger,
        workspace_id="w",
        attempt_ref=represented.payload["attempt_ref"],
        presentation_occurrence=presentation,
        selection_occurrence=selection,
    )


def _remove_binding_occurrence(ledger, binding_event, _selection):
    ledger._events.remove(binding_event)
    ledger._by_workspace["w"].remove(binding_event)
    del ledger._by_id[binding_event.id]


def _duplicate_binding_occurrence(ledger, binding_event, _selection):
    ledger.append(
        binding_event.kind,
        "w",
        deepcopy(binding_event.payload),
        session_id=binding_event.session_id,
    )


@pytest.mark.parametrize(
    "mutation,reason",
    [
        (_remove_binding_occurrence, "no_recorded_binding_occurrence"),
        (_duplicate_binding_occurrence, "multiple_recorded_binding_occurrences"),
        (
            lambda _ledger, event, _selection: event.payload.__setitem__(
                "binding_id", "binding:wrong"
            ),
            "binding_id_mismatch",
        ),
        (
            lambda _ledger, event, _selection: event.payload.__setitem__(
                "choice_set_ref", "choice-set:wrong"
            ),
            "binding_choice_set_mismatch",
        ),
        (
            lambda _ledger, event, _selection: event.payload.__setitem__(
                "choice_set_fingerprint", "fingerprint:wrong"
            ),
            "binding_set_fingerprint_mismatch",
        ),
        (
            lambda _ledger, event, _selection: event.payload.__setitem__(
                "presented_options", list(reversed(event.payload["presented_options"]))
            ),
            "binding_presented_options_mismatch",
        ),
        (
            lambda _ledger, event, _selection: event.payload.__setitem__(
                "selected_presented_alternative_ref", "local-stop"
            ),
            "binding_selected_alternative_mismatch",
        ),
        (
            lambda _ledger, event, _selection: event.payload[
                "binding_testimony"
            ].__setitem__("binding_reason", "forged"),
            "recorded_binding_payload_mismatch",
        ),
        (
            lambda _ledger, event, _selection: event.payload.__setitem__(
                "lineage", event.payload["lineage"][1:]
            ),
            "binding_lineage_mismatch",
        ),
        (
            lambda _ledger, _event, selection: selection.payload.__setitem__(
                "selected_presented_alternative_ref", "local-stop"
            ),
            "selected_alternative_occurrence_mismatch",
        ),
    ],
)
def test_recovery_requires_the_exact_recorded_binding_occurrence(mutation, reason):
    recovered, refusal = _recover_after_binding_event_mutation(mutation)
    assert recovered is None
    assert refusal == reason
