from io import StringIO
from pathlib import Path

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_interaction_goal import (
    run_interaction_goal_establishment,
)
from seed_runtime.operator_presentation import (
    emit_operator_presentation,
    form_operator_presentation,
    render_operator_presentation,
)
from seed_runtime.operator_response_comparison import (
    run_operator_response_comparison_and_identification,
)
from seed_runtime.operator_session_standing import (
    determine_goal_applicability,
    project_operator_session_standing,
)
from seed_runtime.operator_source_recovery import (
    run_operator_source_recovery_and_meaning_relation,
)
from scripts import seed_local

_GOAL_MEANING = "establish richer shared grammar with the operator"
_GOAL_KINDS = (
    "operator.interaction.goal_applicability_established",
    "operator.interaction.goal_admission_established",
    "operator.interaction.goal_consumption_occurred",
    "operator.interaction.goal_standing_established",
)


def _standing(ledger, *, workspace="w", session="s"):
    return project_operator_session_standing(
        ledger, workspace_id=workspace, session_id=session
    )


def _exchange_with_relation(ledger, text, *, workspace="w", session="s"):
    presentation = form_operator_presentation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        session_standing=_standing(ledger, workspace=workspace, session=session),
    )
    emit_operator_presentation(
        ledger, presentation=presentation, output_stream=StringIO()
    )
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id=workspace,
        session_id=session,
        captured_ingress=capture_stdin_material(StringIO(text)),
        output_stream=StringIO(),
        produced_after_presentation=presentation,
    )
    finding = run_operator_response_comparison_and_identification(
        ledger,
        workspace_id=workspace,
        session_id=session,
        presentation=presentation,
        response_ingress_event_id=(
            projection["current_standing"]["preserved_ingress"]["evidence_event_id"]
        ),
    )
    run_operator_source_recovery_and_meaning_relation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        identification_event_id=finding["identification"]["event_id"],
    )
    return presentation, finding


def _establish(ledger, *, workspace="w", session="s"):
    return run_interaction_goal_establishment(
        ledger, workspace_id=workspace, session_id=session
    )


def test_only_a_validated_projected_relation_may_enter_applicability():
    ledger = EventLedger()
    result = _establish(ledger)
    assert result == {"outcome": "no-validated-meaning-relation"}
    assert ledger.list("w") == []

    _exchange_with_relation(ledger, "1\n")
    result = _establish(ledger)
    assert result["outcome"] == "goal-standing-established"


def test_caller_cannot_supply_or_mutate_the_relation_input():
    # The Consumer's only input channel is the validated session projection;
    # its interface accepts no relation dictionary at all.
    import inspect

    parameters = inspect.signature(run_interaction_goal_establishment).parameters
    assert set(parameters) == {"ledger", "workspace_id", "session_id"}


def test_applicability_is_structural_not_lexical():
    module_source = Path("seed_runtime/operator_interaction_goal.py").read_text()
    projection_source = Path(
        "seed_runtime/operator_session_standing.py"
    ).read_text()
    derivation_start = projection_source.index("def determine_goal_applicability")
    derivation = projection_source[
        derivation_start : projection_source.index(
            "def project_operator_session_standing"
        )
    ]
    # The determination consumes structure only; no proposition wording is
    # inspected anywhere on the applicability path.
    for keyword in ('"grammar"', '"learn"', '"goal-like"', "proposition.split"):
        assert keyword not in derivation
        assert keyword not in module_source
    assert "in relation[\"proposition\"]" not in derivation
    assert "in relation[\"proposition\"]" not in module_source


def test_changed_proposition_wording_does_not_alter_applicability():
    # Custom recorded testimony with entirely different wording but the same
    # structural relations is equally applicable.
    ledger = EventLedger()
    template = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    template_payload = ledger.get(template["formed_event_id"]).payload
    presentation_id = template["presentation_id"] + "-reworded"
    reworded = "acquire shared vocabulary with the operator"
    alternatives = []
    for alternative in template_payload["alternatives"]:
        alternative = {
            **alternative,
            "represented_source": dict(alternative["represented_source"]),
        }
        if alternative["role"] == "potential-goal":
            alternative["represented_source"]["meaning"] = reworded
            treatment = alternative["consumer_treatment"]
            alternative["consumer_treatment"] = {
                **treatment,
                "proposition": reworded,
                "consumer_authority": {
                    **treatment["consumer_authority"],
                    "scope": {
                        **treatment["consumer_authority"]["scope"],
                        "proposition": reworded,
                    },
                },
            }
        alternatives.append(alternative)
    formed = ledger.append(
        "operator.presentation.formed",
        "w",
        {
            **template_payload,
            "presentation_ref": presentation_id,
            "alternatives": alternatives,
            "dimensions": {
                **template_payload["dimensions"],
                "identity": presentation_id,
            },
        },
        session_id="s",
    )
    custom = {
        "presentation_id": presentation_id,
        "workspace_id": "w",
        "session_id": "s",
        "formed_event_id": formed.id,
        "emitted_event_id": None,
        "alternatives": alternatives,
        "prior_exchange_finding": None,
        "recovered_meaning_relation": None,
        "current_interaction_goal": None,
    }
    emit_operator_presentation(ledger, presentation=custom, output_stream=StringIO())
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO("1\n")),
        output_stream=StringIO(),
        produced_after_presentation=custom,
    )
    finding = run_operator_response_comparison_and_identification(
        ledger,
        workspace_id="w",
        session_id="s",
        presentation=custom,
        response_ingress_event_id=(
            projection["current_standing"]["preserved_ingress"]["evidence_event_id"]
        ),
    )
    run_operator_source_recovery_and_meaning_relation(
        ledger,
        workspace_id="w",
        session_id="s",
        identification_event_id=finding["identification"]["event_id"],
    )
    result = _establish(ledger)
    assert result["outcome"] == "goal-standing-established"
    assert result["goal_standing"]["proposition"] == reworded


def test_navigation_alternative_is_inapplicable_to_this_consumer():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "2\n")
    result = _establish(ledger)
    assert result["outcome"] == "inapplicable"
    assert result["basis"] == "role-not-potential-goal"
    kinds = {event.kind for event in ledger.list("w")}
    assert "operator.interaction.goal_applicability_established" in kinds
    assert "operator.interaction.goal_admission_established" not in kinds


def test_local_stop_alternative_is_inapplicable_to_this_consumer():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "3\n")
    result = _establish(ledger)
    assert result["outcome"] == "inapplicable"
    assert result["basis"] == "role-not-potential-goal"
    # Inapplicability is Consumer-local: the applicability finding names
    # this exact Consumer purpose, not every Consumer.
    applicability_event = ledger.get(result["applicability"]["event_id"])
    assert applicability_event.payload["consumer_purpose"]
    assert "every" not in applicability_event.payload["consumer_purpose"]


def test_each_act_requires_the_previous_recorded_act():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "1\n")
    result = _establish(ledger)

    events = {event.kind: event for event in ledger.list("w")}
    applicability = events["operator.interaction.goal_applicability_established"]
    admission = events["operator.interaction.goal_admission_established"]
    consumption = events["operator.interaction.goal_consumption_occurred"]
    goal = events["operator.interaction.goal_standing_established"]
    # Distinct identities, purposes, and consumed evidence at each step.
    assert admission.payload["applicability_event_id"] == applicability.id
    assert consumption.payload["admission_event_id"] == admission.id
    assert goal.payload["consumption_event_id"] == consumption.id
    responsibilities = {
        event.payload["dimensions"]["responsibility"]
        for event in (applicability, admission, consumption, goal)
    }
    assert len(responsibilities) == 4
    assert result["outcome"] == "goal-standing-established"


def test_forged_admission_without_applicable_standing_is_refused():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "3\n")
    inapplicable = _establish(ledger)
    assert inapplicable["outcome"] == "inapplicable"
    good_applicability = ledger.get(inapplicable["applicability"]["event_id"])
    ledger.append(
        "operator.interaction.goal_admission_established",
        "w",
        {
            "attempt_ref": None,
            "admission_ref": "forged",
            "applicability_event_id": good_applicability.id,
            "applicability_ref": good_applicability.payload["applicability_ref"],
            "consumer_ref": good_applicability.payload["consumer_ref"],
            "consumer_purpose": good_applicability.payload["consumer_purpose"],
            "meaning_relation_event_id": good_applicability.payload[
                "meaning_relation_event_id"
            ],
            "alternative_id": good_applicability.payload["alternative"][
                "alternative_id"
            ],
            "source_identity": good_applicability.payload["source_identity"],
            "proposition": good_applicability.payload["proposition"],
            "consumer_scope": good_applicability.payload["consumer_scope"],
            "standing": "admitted",
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "mutates_cluster": False,
        },
        session_id="s",
    )
    with pytest.raises(ValueError, match="recorded applicable finding"):
        _standing(ledger)


def test_goal_standing_requires_the_full_recorded_chain():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "1\n")
    result = _establish(ledger)

    good_goal = ledger.get(result["goal_standing"]["event_id"])
    ledger.append(
        "operator.interaction.goal_standing_established",
        "w",
        {
            **good_goal.payload,
            "goal_standing_ref": "forged",
            "consumption_event_id": "evt_forged",
        },
        session_id="s",
    )
    with pytest.raises(ValueError, match="recorded consumption occurrence"):
        _standing(ledger)


def test_identification_alone_cannot_produce_goal_standing():
    # A matched, identified exchange with no meaning relation recorded:
    # the Consumer reports absence and records nothing.
    ledger = EventLedger()
    presentation = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    emit_operator_presentation(
        ledger, presentation=presentation, output_stream=StringIO()
    )
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO("1\n")),
        output_stream=StringIO(),
        produced_after_presentation=presentation,
    )
    run_operator_response_comparison_and_identification(
        ledger,
        workspace_id="w",
        session_id="s",
        presentation=presentation,
        response_ingress_event_id=(
            projection["current_standing"]["preserved_ingress"]["evidence_event_id"]
        ),
    )
    result = _establish(ledger)
    assert result == {"outcome": "no-validated-meaning-relation"}
    assert not any(
        event.kind.startswith("operator.interaction.") for event in ledger.list("w")
    )


def test_missing_consumer_treatment_prevents_goal_standing():
    # Recorded testimony whose potential-goal alternative carries no
    # treatment relation: applicable-looking role, but the exact
    # goal-consumption gap is preserved.
    ledger = EventLedger()
    template = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    template_payload = ledger.get(template["formed_event_id"]).payload
    presentation_id = template["presentation_id"] + "-untreated"
    alternatives = [
        {**alternative, "consumer_treatment": None}
        for alternative in template_payload["alternatives"]
    ]
    formed = ledger.append(
        "operator.presentation.formed",
        "w",
        {
            **template_payload,
            "presentation_ref": presentation_id,
            "alternatives": alternatives,
            "dimensions": {
                **template_payload["dimensions"],
                "identity": presentation_id,
            },
        },
        session_id="s",
    )
    untreated = {
        "presentation_id": presentation_id,
        "workspace_id": "w",
        "session_id": "s",
        "formed_event_id": formed.id,
        "emitted_event_id": None,
        "alternatives": alternatives,
        "prior_exchange_finding": None,
        "recovered_meaning_relation": None,
        "current_interaction_goal": None,
    }
    emit_operator_presentation(
        ledger, presentation=untreated, output_stream=StringIO()
    )
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO("1\n")),
        output_stream=StringIO(),
        produced_after_presentation=untreated,
    )
    finding = run_operator_response_comparison_and_identification(
        ledger,
        workspace_id="w",
        session_id="s",
        presentation=untreated,
        response_ingress_event_id=(
            projection["current_standing"]["preserved_ingress"]["evidence_event_id"]
        ),
    )
    run_operator_source_recovery_and_meaning_relation(
        ledger,
        workspace_id="w",
        session_id="s",
        identification_event_id=finding["identification"]["event_id"],
    )
    result = _establish(ledger)
    assert result["outcome"] == "inapplicable"
    assert result["basis"] == "no-consumer-treatment-relation"
    kinds = {event.kind for event in ledger.list("w")}
    assert "operator.interaction.goal_standing_established" not in kinds


def test_role_and_label_cannot_substitute_for_the_treatment_relation():
    # determine_goal_applicability consumes the treatment relation, never
    # the rendered label; a role of potential-goal without a treatment
    # relation is inapplicable.
    relation = {
        "source_identity": "source:x",
        "proposition": "anything",
        "representation_scope": "workspace:w;session:s",
        "authority_separation": {
            "meaning_warrant": {"standing": "established"},
            "source_authority": {"standing": "bounded"},
            "response_comparison_authority": {"standing": "bounded"},
        },
    }
    recovery = {
        "alternative": {
            "alternative_id": "a1",
            "role": "potential-goal",
        }
    }
    standing, basis = determine_goal_applicability(
        relation, recovery, None, scope="workspace:w;session:s"
    )
    assert (standing, basis) == ("inapplicable", "no-consumer-treatment-relation")


def test_operator_authority_remains_structurally_unresolved():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "1\n")
    result = _establish(ledger)

    goal_event = ledger.get(result["goal_standing"]["event_id"])
    assert goal_event.payload["operator_authority"] == {
        "standing": "unresolved",
        "supports": [],
        "evidence_event_ids": [],
        "scope": {"proposition": _GOAL_MEANING},
    }
    standing = _standing(ledger)
    assert standing["latest_interaction_goal_standing"]["operator_authority"][
        "standing"
    ] == "unresolved"


def test_goal_standing_establishes_no_intent_selection_or_learning():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "1\n")
    result = _establish(ledger)

    goal_event = ledger.get(result["goal_standing"]["event_id"])
    assert goal_event.payload["unknowns"] == [
        "operator intent Unknown",
        "operator selection occurrence Unknown",
    ]
    flattened = str(goal_event.payload)
    assert "Operator selected" not in flattened
    assert "Operator intended" not in flattened
    kinds = {event.kind for event in ledger.list("w")}
    assert not any("learning" in kind or "remember" in kind for kind in kinds)
    authority = goal_event.payload["dimensions"]["authority_warrant"]
    assert "no operator intent, selection, authorization" in authority
    assert "learning, or remembering" in authority


def test_projector_refuses_forged_goal_chain_events():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "1\n")
    _establish(ledger)

    good = next(
        event
        for event in ledger.list("w")
        if event.kind == "operator.interaction.goal_applicability_established"
    )
    ledger.append(
        good.kind,
        "w",
        {**good.payload, "applicability_ref": "forged", "standing": "applicable",
         "basis": "structural-agreement", "consumer_treatment": None},
        session_id="s",
    )
    with pytest.raises(ValueError, match="derived from recorded testimony"):
        _standing(ledger)


def test_projector_refuses_duplicate_goal_references():
    for kind in _GOAL_KINDS:
        ledger = EventLedger()
        _exchange_with_relation(ledger, "1\n")
        _establish(ledger)
        original = next(
            event for event in ledger.list("w") if event.kind == kind
        )
        ledger.append(kind, "w", dict(original.payload), session_id="s")
        with pytest.raises(ValueError, match="duplicate"):
            _standing(ledger)


def test_later_presentation_exposes_the_bounded_goal_without_strengthening():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "1\n")
    _establish(ledger)

    later = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    rendered = render_operator_presentation(later)
    assert (
        f'Current bounded interaction goal: "{_GOAL_MEANING}"' in rendered
    )
    assert "Source: source:developer-supplied-grammar-acquisition-candidate" in (
        rendered
    )
    assert "Applicability: established for this exact Consumer purpose" in rendered
    assert "Admission: established" in rendered
    assert "Consumption: occurred" in rendered
    assert "Operator intent remains Unknown" in rendered
    assert "Operator Authority for the proposition remains unresolved" in rendered
    # The narrower claim: this path establishes no Learning Standing; it
    # does not assert positive nonoccurrence of Learning anywhere.
    assert "No Learning Standing is established by this path" in rendered
    assert "Learning has not occurred" not in rendered
    assert "Operator selected" not in rendered
    assert "goal achieved" not in rendered


def test_console_establishes_the_goal_end_to_end():
    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("Hello\n1\nexit\n"),
        output_stream=output,
    )
    standing = _standing(ledger)
    goal = standing["latest_interaction_goal_standing"]
    assert goal is not None
    assert goal["proposition"] == _GOAL_MEANING
    assert "Current bounded interaction goal" in output.getvalue()


def test_consumer_responsibility_and_authority_are_structural():
    ledger = EventLedger()
    _exchange_with_relation(ledger, "1\n")
    result = _establish(ledger)

    applicability_event = ledger.get(result["applicability"]["event_id"])
    responsibility = applicability_event.payload["consumer_responsibility"]
    assert set(responsibility) == {
        "identity",
        "purpose",
        "consumer",
        "scope",
        "authority",
        "evidence_event_ids",
    }
    assert responsibility["identity"] == result["consumer_ref"]
    authority = responsibility["authority"]
    assert authority["kind"] == "bounded-interaction-goal-establishment"
    assert authority["identity"].startswith("treatment-relation:")
    assert authority["supports"] == [
        "admit-exact-meaning-relation",
        "consume-exact-admitted-relation",
        "establish-bounded-interaction-goal-standing",
    ]
    assert set(authority["scope"]) == {
        "alternative_id",
        "source_identity",
        "proposition",
        "consumer_purpose",
        "session_scope",
    }
    # Every later Act references the same Responsibility and carries its
    # explicit basis with the exact authority support it moved under.
    admission_event = ledger.get(result["admission"]["event_id"])
    consumption_event = ledger.get(result["consumption"]["event_id"])
    goal_event = ledger.get(result["goal_standing"]["event_id"])
    for event, support in (
        (admission_event, "admit-exact-meaning-relation"),
        (consumption_event, "consume-exact-admitted-relation"),
        (goal_event, "establish-bounded-interaction-goal-standing"),
    ):
        assert event.payload["consumer_responsibility_identity"] == (
            result["consumer_ref"]
        )
        assert event.payload["basis"]["authority_support"] == support
    # The consumption and goal carry the full structural authority, scoped
    # to the exact A / G / M / purpose / session.
    assert consumption_event.payload["consumer_authority"] == authority
    assert goal_event.payload["consumer_authority"] == authority


def test_projector_refuses_forged_goal_standing_claims():
    for forged_fields in (
        {"standing": "globally established goal"},
        {"locality": "every interaction"},
        {"unknowns": []},
        {"basis": None},
    ):
        ledger = EventLedger()
        _exchange_with_relation(ledger, "1\n")
        _establish(ledger)
        good = next(
            event
            for event in ledger.list("w")
            if event.kind == "operator.interaction.goal_standing_established"
        )
        ledger.append(
            good.kind,
            "w",
            {**good.payload, "goal_standing_ref": "forged", **forged_fields},
            session_id="s",
        )
        with pytest.raises(ValueError, match="derived from recorded testimony"):
            _standing(ledger)


def test_projector_refuses_forged_admission_and_consumption_boundaries():
    for kind, forged_fields in (
        (
            "operator.interaction.goal_admission_established",
            {"unknowns": [], "known_loss": ["nothing"]},
        ),
        (
            "operator.interaction.goal_consumption_occurred",
            {
                "basis": {
                    "admission_event_id": "evt_forged",
                    "consumer_responsibility_identity": "forged",
                    "authority_support": "establish-anything",
                }
            },
        ),
    ):
        ledger = EventLedger()
        _exchange_with_relation(ledger, "1\n")
        _establish(ledger)
        good = next(event for event in ledger.list("w") if event.kind == kind)
        reference_key = (
            "admission_ref"
            if "admission" in kind
            else "consumption_ref"
        )
        ledger.append(
            kind,
            "w",
            {**good.payload, reference_key: "forged", **forged_fields},
            session_id="s",
        )
        with pytest.raises(ValueError, match="basis and boundary"):
            _standing(ledger)


def test_recorded_treatment_without_structural_authority_is_inapplicable():
    # Same A/G/M/purpose/scope, but the recorded treatment carries a foreign
    # kind or a conflicted inventory: structurally inapplicable, without
    # parsing any prose.
    for mutation, expected_basis in (
        (
            lambda treatment: {**treatment, "treatment_kind": "unrelated-kind"},
            "treatment-kind-mismatch",
        ),
        (
            lambda treatment: {**treatment, "consumer_authority": None},
            "consumer-authority-not-established",
        ),
        (
            lambda treatment: {**treatment, "conflicts": ["recorded conflict"]},
            "treatment-conflicted",
        ),
    ):
        ledger = EventLedger()
        template = form_operator_presentation(
            ledger,
            workspace_id="w",
            session_id="s",
            session_standing=_standing(ledger),
        )
        template_payload = ledger.get(template["formed_event_id"]).payload
        presentation_id = template["presentation_id"] + "-" + expected_basis
        alternatives = []
        for alternative in template_payload["alternatives"]:
            alternative = dict(alternative)
            if alternative["role"] == "potential-goal":
                alternative["consumer_treatment"] = mutation(
                    alternative["consumer_treatment"]
                )
            alternatives.append(alternative)
        formed = ledger.append(
            "operator.presentation.formed",
            "w",
            {
                **template_payload,
                "presentation_ref": presentation_id,
                "alternatives": alternatives,
                "dimensions": {
                    **template_payload["dimensions"],
                    "identity": presentation_id,
                },
            },
            session_id="s",
        )
        custom = {
            "presentation_id": presentation_id,
            "workspace_id": "w",
            "session_id": "s",
            "formed_event_id": formed.id,
            "emitted_event_id": None,
            "alternatives": alternatives,
            "prior_exchange_finding": None,
            "recovered_meaning_relation": None,
            "current_interaction_goal": None,
        }
        emit_operator_presentation(
            ledger, presentation=custom, output_stream=StringIO()
        )
        projection = run_operator_ingress_attempt(
            ledger=ledger,
            workspace_id="w",
            session_id="s",
            captured_ingress=capture_stdin_material(StringIO("1\n")),
            output_stream=StringIO(),
            produced_after_presentation=custom,
        )
        finding = run_operator_response_comparison_and_identification(
            ledger,
            workspace_id="w",
            session_id="s",
            presentation=custom,
            response_ingress_event_id=(
                projection["current_standing"]["preserved_ingress"][
                    "evidence_event_id"
                ]
            ),
        )
        run_operator_source_recovery_and_meaning_relation(
            ledger,
            workspace_id="w",
            session_id="s",
            identification_event_id=finding["identification"]["event_id"],
        )
        result = _establish(ledger)
        assert result["outcome"] == "inapplicable", expected_basis
        assert result["basis"] == expected_basis


def test_no_code_or_payload_names_boge():
    for module in (
        "seed_runtime/operator_interaction_goal.py",
        "seed_runtime/operator_presentation.py",
        "seed_runtime/operator_session_standing.py",
    ):
        assert "BOGE" not in Path(module).read_text()
    ledger = EventLedger()
    _exchange_with_relation(ledger, "1\n")
    _establish(ledger)
    for event in ledger.list("w"):
        assert "BOGE" not in str(event.payload)
        assert "BOGE" not in event.kind
