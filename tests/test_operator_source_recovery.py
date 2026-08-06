from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_presentation import (
    emit_operator_presentation,
    form_operator_presentation,
    render_operator_presentation,
)
from seed_runtime.operator_response_comparison import (
    run_operator_response_comparison_and_identification,
)
from seed_runtime.operator_session_standing import project_operator_session_standing
from seed_runtime.operator_source_recovery import (
    run_operator_source_recovery_and_meaning_relation,
)
from scripts import seed_local

_GOAL_MEANING = "establish richer shared grammar with the operator"


def _standing(ledger, *, workspace="w", session="s"):
    return project_operator_session_standing(
        ledger, workspace_id=workspace, session_id=session
    )


def _exchange(ledger, text, *, workspace="w", session="s"):
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
    return presentation, finding


def _recover(ledger, identification_event_id, *, workspace="w", session="s"):
    return run_operator_source_recovery_and_meaning_relation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        identification_event_id=identification_event_id,
    )


def _recovered_exchange(ledger, text="1\n", **kwargs):
    presentation, finding = _exchange(ledger, text, **kwargs)
    result = _recover(
        ledger, finding["identification"]["event_id"], **kwargs
    )
    return presentation, finding, result


def test_recovery_requires_a_successful_recorded_identification():
    ledger = EventLedger()
    with pytest.raises(ValueError, match="identification event not recorded"):
        _recover(ledger, "evt_nonexistent")

    presentation, finding = _exchange(ledger, "1\n")
    with pytest.raises(ValueError, match="not a .* event"):
        _recover(ledger, finding["comparison"]["event_id"])


def test_no_match_produces_no_source_recovery():
    ledger = EventLedger()
    _, finding = _exchange(ledger, "no coordinate here\n")

    with pytest.raises(ValueError, match="did not identify"):
        _recover(ledger, finding["identification"]["event_id"])
    kinds = {event.kind for event in ledger.list("w")}
    assert "operator.presentation.source_recovered" not in kinds


def test_failed_identification_produces_no_source_recovery():
    # Recorded testimony whose binding maps outside the exact presentation:
    # match, failed identification, and recovery structurally refuses.
    ledger = EventLedger()
    template = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    template_payload = ledger.get(template["formed_event_id"]).payload
    presentation_id = template["presentation_id"] + "-malformed"
    formed = ledger.append(
        "operator.presentation.formed",
        "w",
        {
            **template_payload,
            "presentation_ref": presentation_id,
            "coordinate_bindings": {
                **template_payload["coordinate_bindings"],
                "1": "presented_alternative_foreign",
            },
            "dimensions": {
                **template_payload["dimensions"],
                "identity": presentation_id,
            },
        },
        session_id="s",
    )
    emitted = ledger.append(
        "operator.presentation.emitted",
        "w",
        {
            "attempt_ref": None,
            "presentation_ref": presentation_id,
            "formed_event_id": formed.id,
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "lineage": [formed.id],
            "mutates_cluster": False,
        },
        session_id="s",
    )
    malformed = {
        "presentation_id": presentation_id,
        "formed_event_id": formed.id,
        "emitted_event_id": emitted.id,
    }
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO("1\n")),
        output_stream=StringIO(),
        produced_after_presentation=malformed,
    )
    finding = run_operator_response_comparison_and_identification(
        ledger,
        workspace_id="w",
        session_id="s",
        presentation=malformed,
        response_ingress_event_id=(
            projection["current_standing"]["preserved_ingress"]["evidence_event_id"]
        ),
    )
    assert finding["identification"]["basis"] == "binding-inapplicable"
    with pytest.raises(ValueError, match="did not identify"):
        _recover(ledger, finding["identification"]["event_id"])


def test_recovery_consumes_recorded_formation_not_a_mutable_projection():
    # The interface takes only recorded event identities; there is no
    # projection argument to mutate, and the recovered source equals the
    # recorded formation testimony exactly.
    ledger = EventLedger()
    presentation, finding, result = _recovered_exchange(ledger)

    formed_payload = ledger.get(presentation["formed_event_id"]).payload
    recorded_alternative = next(
        alternative
        for alternative in formed_payload["alternatives"]
        if alternative["alternative_id"]
        == finding["identification"]["identified_alternative"]["alternative_id"]
    )
    recovery_event = ledger.get(result["source_recovery"]["event_id"])
    assert recovery_event.payload["source"] == {
        "identity": recorded_alternative["represented_source"]["identity"],
        "kind": recorded_alternative["represented_source"]["kind"],
        "attribution": recorded_alternative["represented_source"]["attribution"],
        "reference": recorded_alternative["represented_source"]["reference"],
    }
    assert recovery_event.payload["representation"] == (
        recorded_alternative["representation"]
    )


def test_exact_alternative_recovers_only_its_exact_source():
    ledger = EventLedger()
    _, _, goal_result = _recovered_exchange(ledger, "1\n")
    _, _, stop_result = _recovered_exchange(ledger, "3\n")

    assert goal_result["source_recovery"]["source_identity"] == (
        "source:developer-supplied-grammar-acquisition-candidate"
    )
    assert stop_result["source_recovery"]["source_identity"] == (
        "source:developer-supplied-local-stop-treatment"
    )


def test_foreign_testimony_structurally_refuses():
    ledger = EventLedger()
    _, finding = _exchange(ledger, "1\n", workspace="w", session="other")

    with pytest.raises(ValueError, match="another workspace or session"):
        _recover(ledger, finding["identification"]["event_id"], session="s")

    # An identification whose carried alternative disagrees with the
    # recorded formation payload is refused.
    own_ledger = EventLedger()
    _, own_finding = _exchange(own_ledger, "1\n")
    good_identification = own_ledger.get(own_finding["identification"]["event_id"])
    forged = own_ledger.append(
        "operator.exchange.identification_occurred",
        "w",
        {
            **good_identification.payload,
            "identification_ref": "forged",
            "identified_alternative": {
                **good_identification.payload["identified_alternative"],
                "role": "local-stop",
            },
        },
        session_id="s",
    )
    with pytest.raises(ValueError, match="disagrees with recorded role"):
        _recover(own_ledger, forged.id)


def test_formation_event_evidences_the_representation_relation():
    ledger = EventLedger()
    presentation, _, result = _recovered_exchange(ledger)

    recovery_event = ledger.get(result["source_recovery"]["event_id"])
    assert presentation["formed_event_id"] in recovery_event.payload["lineage"]
    assert recovery_event.payload["presentation_formed_event_id"] == (
        presentation["formed_event_id"]
    )
    formed_payload = ledger.get(presentation["formed_event_id"]).payload
    for alternative in formed_payload["alternatives"]:
        assert alternative["representation"]["evidence_event_ids"] == []


def test_no_synthetic_developer_source_evidence_event_is_created():
    ledger = EventLedger()
    _recovered_exchange(ledger)

    kinds = {event.kind for event in ledger.list("w")}
    assert kinds == {
        "operator.ingress.raw_material_captured",
        "operator.ingress.representation_examined",
        "operator.ingress.ingress_occurred",
        "operator.presentation.formed",
        "operator.presentation.emitted",
        "operator.exchange.comparison_occurred",
        "operator.exchange.identification_occurred",
        "operator.presentation.source_recovered",
        "operator.presentation.meaning_relation_established",
    }


def test_recovery_does_not_carry_meaning_as_established():
    ledger = EventLedger()
    _, _, result = _recovered_exchange(ledger)

    recovery_event = ledger.get(result["source_recovery"]["event_id"])
    assert "meaning" not in recovery_event.payload["source"]
    assert "proposition" not in recovery_event.payload
    assert _GOAL_MEANING not in str(recovery_event.payload)


def test_meaning_consumption_requires_recorded_source_recovery():
    ledger = EventLedger()
    _, _, result = _recovered_exchange(ledger)

    relation_event = ledger.get(result["meaning_relation"]["event_id"])
    assert relation_event.payload["source_recovery_event_id"] == (
        result["source_recovery"]["event_id"]
    )
    # A meaning relation recorded without its recovery refuses at projection.
    forged_ledger = EventLedger()
    _recovered_exchange(forged_ledger)
    good = next(
        event
        for event in forged_ledger.list("w")
        if event.kind == "operator.presentation.meaning_relation_established"
    )
    forged_ledger.append(
        "operator.presentation.meaning_relation_established",
        "w",
        {**good.payload, "relation_ref": "forged", "recovery_ref": "missing"},
        session_id="s",
    )
    with pytest.raises(ValueError, match="without recorded source recovery"):
        _standing(forged_ledger)


def test_proposition_comes_only_from_attributed_formation_testimony():
    ledger = EventLedger()
    presentation, _, result = _recovered_exchange(ledger)

    formed_payload = ledger.get(presentation["formed_event_id"]).payload
    recorded_meaning = next(
        alternative["represented_source"]["meaning"]
        for alternative in formed_payload["alternatives"]
        if alternative["role"] == "potential-goal"
    )
    assert result["meaning_relation"]["proposition"] == recorded_meaning
    relation_event = ledger.get(result["meaning_relation"]["event_id"])
    assert relation_event.payload["source_attribution"] == "developer-supplied"
    assert relation_event.payload["warrant_basis"] == (
        "attributed developer-supplied meaning testimony preserved by the "
        "recorded formation occurrence"
    )


def test_operator_ingress_text_cannot_alter_the_proposition():
    ledger = EventLedger()
    # The captured coordinate text is "1"; the proposition is the attributed
    # testimony, not anything derived from operator material.
    _, _, result = _recovered_exchange(ledger, "1\n")
    assert result["meaning_relation"]["proposition"] == _GOAL_MEANING
    assert result["meaning_relation"]["proposition"] != "1"


def test_four_authorities_remain_distinct_and_queryable():
    ledger = EventLedger()
    _, _, result = _recovered_exchange(ledger)

    relation_event = ledger.get(result["meaning_relation"]["event_id"])
    separation = relation_event.payload["authority_separation"]
    assert set(separation) == {
        "source_authority",
        "response_comparison_authority",
        "meaning_warrant",
        "operator_authority",
    }
    assert len({value for value in separation.values()}) == 4


def test_operator_authority_for_proposition_remains_unresolved():
    ledger = EventLedger()
    _, _, result = _recovered_exchange(ledger)

    relation_event = ledger.get(result["meaning_relation"]["event_id"])
    assert relation_event.payload["authority_separation"]["operator_authority"] == (
        "unresolved for this proposition; not established by production, "
        "match, identification, or this relation"
    )
    flattened = str(relation_event.payload)
    assert "Operator intended" not in flattened
    assert "Operator selected" not in flattened
    assert "Operator authorized" not in flattened


def test_meaning_relation_establishes_no_goal_or_treatment():
    ledger = EventLedger()
    _, _, result = _recovered_exchange(ledger)

    kinds = {event.kind for event in ledger.list("w")}
    assert not any("goal" in kind for kind in kinds)
    assert "operator.ingress.stopping_occurred" not in kinds
    relation_event = ledger.get(result["meaning_relation"]["event_id"])
    authority = relation_event.payload["dimensions"]["authority_warrant"]
    assert "no operator intent, selection, authorization, goal standing" in (
        authority.replace("establishes ", "")
    )


def test_session_projection_validates_the_recovery_meaning_pair():
    ledger = EventLedger()
    _recovered_exchange(ledger)

    good = next(
        event
        for event in ledger.list("w")
        if event.kind == "operator.presentation.meaning_relation_established"
    )
    ledger.append(
        "operator.presentation.meaning_relation_established",
        "w",
        {
            **good.payload,
            "relation_ref": "forged",
            "source_identity": "source:forged-other-source",
        },
        session_id="s",
    )
    with pytest.raises(ValueError, match="does not agree .* source_identity"):
        _standing(ledger)


def test_later_presentation_exposes_bounded_relations_without_strengthening():
    ledger = EventLedger()
    _recovered_exchange(ledger, "1\n")

    later = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    relation = later["recovered_meaning_relation"]
    assert relation["source_identity"] == (
        "source:developer-supplied-grammar-acquisition-candidate"
    )
    rendered = render_operator_presentation(later)
    assert (
        "Recovered source source:developer-supplied-grammar-acquisition-"
        "candidate expresses: \"establish richer shared grammar with the "
        "operator\" (developer-supplied)." in rendered
    )
    assert (
        "Operator intent and selection remain Unknown; Operator Authority "
        "for this proposition remains unresolved." in rendered
    )
    assert "goal established" not in rendered
    assert "goal Standing" not in rendered
    assert "Operator selected" not in rendered
    assert "Operator intended" not in rendered


def test_console_runs_recovery_only_for_identified_exchanges():
    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("Hello\n1\nnot a coordinate\nexit\n"),
        output_stream=output,
    )

    standing = _standing(ledger)
    assert len(standing["source_recoveries"]) == 1
    assert len(standing["meaning_relations"]) == 1
    rendered = output.getvalue()
    assert rendered.count("Recovered source") == 1
    # The no-match exchange exposes no recovered relation.
    final_presentation = rendered[rendered.rindex("Bounded Presentation") :]
    assert "Recovered source" not in final_presentation
