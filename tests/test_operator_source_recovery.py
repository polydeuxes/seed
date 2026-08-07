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
    malformed_presentation = {
        "presentation_id": presentation_id,
        "workspace_id": "w",
        "session_id": "s",
        "formed_event_id": formed.id,
        "emitted_event_id": None,
        "alternatives": template_payload["alternatives"],
        "prior_exchange_finding": None,
        "recovered_meaning_relation": None,
    }
    emit_operator_presentation(
        ledger, presentation=malformed_presentation, output_stream=StringIO()
    )
    emitted_event_id = malformed_presentation["emitted_event_id"]
    malformed = {
        "presentation_id": presentation_id,
        "formed_event_id": formed.id,
        "emitted_event_id": emitted_event_id,
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


def test_four_authorities_are_distinct_structural_coordinates():
    ledger = EventLedger()
    presentation, finding, result = _recovered_exchange(ledger)

    relation_event = ledger.get(result["meaning_relation"]["event_id"])
    separation = relation_event.payload["authority_separation"]
    assert set(separation) == {
        "source_authority",
        "response_comparison_authority",
        "meaning_warrant",
        "operator_authority",
    }
    # Each coordinate is structural -- standing, supported claims, Evidence,
    # and Scope -- with testimony alongside, not as the only representation.
    for coordinate in separation.values():
        assert set(coordinate) == {
            "standing",
            "supports",
            "evidence_event_ids",
            "scope",
            "testimony",
        }
    assert separation["source_authority"]["standing"] == "bounded"
    assert separation["source_authority"]["evidence_event_ids"] == [
        presentation["formed_event_id"]
    ]
    assert separation["response_comparison_authority"]["supports"] == [
        "response-matched-coordinate-within-presentation"
    ]
    assert separation["response_comparison_authority"]["evidence_event_ids"] == [
        finding["comparison"]["event_id"]
    ]
    assert separation["meaning_warrant"]["standing"] == "established"
    assert separation["meaning_warrant"]["evidence_event_ids"] == [
        presentation["formed_event_id"],
        result["source_recovery"]["event_id"],
    ]
    assert separation["meaning_warrant"]["supports"] == [
        "source-expresses-proposition"
    ]


def test_operator_authority_for_proposition_remains_unresolved():
    ledger = EventLedger()
    _, _, result = _recovered_exchange(ledger)

    relation_event = ledger.get(result["meaning_relation"]["event_id"])
    operator_authority = relation_event.payload["authority_separation"][
        "operator_authority"
    ]
    assert operator_authority["standing"] == "unresolved"
    assert operator_authority["supports"] == []
    assert operator_authority["evidence_event_ids"] == []
    assert operator_authority["scope"] == {"proposition": _GOAL_MEANING}
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


def test_forged_identification_over_no_match_is_refused():
    # Compare recorded no-coordinate-match; a forged identification claiming
    # a valid alternative from C must not produce recovery.
    ledger = EventLedger()
    presentation, finding = _exchange(ledger, "not a coordinate\n")
    good_payload = ledger.get(finding["identification"]["event_id"]).payload
    formed_payload = ledger.get(presentation["formed_event_id"]).payload
    valid_alternative = formed_payload["alternatives"][0]
    forged = ledger.append(
        "operator.exchange.identification_occurred",
        "w",
        {
            **good_payload,
            "identification_ref": "forged",
            "basis": "identified",
            "outcome": "alternative-identified",
            "identified_alternative": {
                "alternative_id": valid_alternative["alternative_id"],
                "role": valid_alternative["role"],
                "response_coordinate": valid_alternative["response_coordinate"],
                "rendered_label": valid_alternative["rendered_label"],
            },
        },
        session_id="s",
    )
    with pytest.raises(ValueError, match="recorded no coordinate match"):
        _recover(ledger, forged.id)


def test_binding_that_bypasses_the_matched_coordinate_is_refused():
    # Recorded C binds coordinate 1 to the alternative whose own coordinate
    # is 2: identification lawfully follows the recorded binding, but
    # recovery refuses because the matched coordinate does not belong to
    # the identified alternative.
    ledger = EventLedger()
    template = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    template_payload = ledger.get(template["formed_event_id"]).payload
    presentation_id = template["presentation_id"] + "-crossbound"
    crossbound_bindings = dict(template_payload["coordinate_bindings"])
    crossbound_bindings["1"] = template_payload["coordinate_bindings"]["2"]
    formed = ledger.append(
        "operator.presentation.formed",
        "w",
        {
            **template_payload,
            "presentation_ref": presentation_id,
            "coordinate_bindings": crossbound_bindings,
            "dimensions": {
                **template_payload["dimensions"],
                "identity": presentation_id,
            },
        },
        session_id="s",
    )
    crossbound = {
        "presentation_id": presentation_id,
        "workspace_id": "w",
        "session_id": "s",
        "formed_event_id": formed.id,
        "emitted_event_id": None,
        "alternatives": template_payload["alternatives"],
        "prior_exchange_finding": None,
        "recovered_meaning_relation": None,
    }
    emit_operator_presentation(
        ledger, presentation=crossbound, output_stream=StringIO()
    )
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO("1\n")),
        output_stream=StringIO(),
        produced_after_presentation=crossbound,
    )
    finding = run_operator_response_comparison_and_identification(
        ledger,
        workspace_id="w",
        session_id="s",
        presentation=crossbound,
        response_ingress_event_id=(
            projection["current_standing"]["preserved_ingress"]["evidence_event_id"]
        ),
    )
    assert finding["identification"]["basis"] == "identified"
    assert finding["identification"]["identified_alternative"][
        "response_coordinate"
    ] == "2"
    with pytest.raises(ValueError, match="does not belong to the identified"):
        _recover(ledger, finding["identification"]["event_id"])


def test_recovery_lineage_carries_the_complete_exchange_chain():
    ledger = EventLedger()
    presentation, finding, result = _recovered_exchange(ledger)

    recovery_event = ledger.get(result["source_recovery"]["event_id"])
    ingress_event_id = ledger.get(finding["comparison"]["event_id"]).payload[
        "response_ingress_event_id"
    ]
    capture_event_id = ledger.get(finding["comparison"]["event_id"]).payload[
        "response_capture_event_id"
    ]
    assert recovery_event.payload["lineage"] == [
        presentation["formed_event_id"],
        presentation["emitted_event_id"],
        capture_event_id,
        ingress_event_id,
        finding["comparison"]["event_id"],
        finding["identification"]["event_id"],
    ]


def test_projector_refuses_a_forged_proposition_or_attribution():
    for forged_fields in (
        {"proposition": "restart every service immediately"},
        {"source_attribution": "operator-supplied"},
    ):
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
            {**good.payload, "relation_ref": "forged", **forged_fields},
            session_id="s",
        )
        with pytest.raises(ValueError, match="does not agree"):
            _standing(ledger)


def test_projector_refuses_recovery_with_false_occurrence_lineage():
    # Correct C/A/G identities with forged occurrence lineage or attempt.
    for forged_fields in (
        {"presentation_emitted_event_id": "evt_forged"},
        {"comparison_event_id": "evt_forged"},
        {"response_attempt_ref": "operator_ingress_attempt_forged"},
    ):
        ledger = EventLedger()
        _recovered_exchange(ledger)
        good = next(
            event
            for event in ledger.list("w")
            if event.kind == "operator.presentation.source_recovered"
        )
        ledger.append(
            "operator.presentation.source_recovered",
            "w",
            {**good.payload, "recovery_ref": "forged", **forged_fields},
            session_id="s",
        )
        with pytest.raises(ValueError):
            _standing(ledger)


def test_projector_refuses_forged_authority_coordinates():
    forgeries = (
        ("operator_authority", "standing", "established"),
        ("operator_authority", "supports", ["goal-establishment"]),
        ("meaning_warrant", "evidence_event_ids", ["evt_unrelated"]),
        ("source_authority", "scope", {"source_identity": "source:other"}),
    )
    for name, field, forged_value in forgeries:
        ledger = EventLedger()
        _recovered_exchange(ledger)
        good = next(
            event
            for event in ledger.list("w")
            if event.kind == "operator.presentation.meaning_relation_established"
        )
        separation = {
            key: dict(value)
            for key, value in good.payload["authority_separation"].items()
        }
        separation[name][field] = forged_value
        ledger.append(
            "operator.presentation.meaning_relation_established",
            "w",
            {
                **good.payload,
                "relation_ref": "forged",
                "authority_separation": separation,
            },
            session_id="s",
        )
        with pytest.raises(
            ValueError, match=f"does not agree with recorded testimony on {name}"
        ):
            _standing(ledger)


def test_projected_results_preserve_the_complete_validated_boundary():
    ledger = EventLedger()
    presentation, finding, result = _recovered_exchange(ledger)

    standing = _standing(ledger)
    recovery = standing["latest_source_recovery"]
    assert recovery["presentation_emitted_event_id"] == (
        presentation["emitted_event_id"]
    )
    assert recovery["comparison_event_id"] == finding["comparison"]["event_id"]
    comparison_payload = ledger.get(finding["comparison"]["event_id"]).payload
    assert recovery["response_ingress_event_id"] == (
        comparison_payload["response_ingress_event_id"]
    )
    assert recovery["response_capture_event_id"] == (
        comparison_payload["response_capture_event_id"]
    )
    assert set(recovery["representation"]) == {
        "purpose",
        "scope",
        "provenance",
        "evidence_event_ids",
        "known_loss",
        "unknowns",
        "conflicts",
    }

    relation = standing["latest_meaning_relation"]
    relation_payload = ledger.get(result["meaning_relation"]["event_id"]).payload
    for key in (
        "presentation_formed_event_id",
        "source_reference",
        "representation_purpose",
        "representation_scope",
        "warrant_basis",
        "known_loss",
        "conflicts",
    ):
        assert relation[key] == relation_payload[key], key
    # Authority coordinates in Standing are the validated reconstruction.
    assert relation["authority_separation"]["operator_authority"]["standing"] == (
        "unresolved"
    )
    assert relation["authority_separation"]["meaning_warrant"][
        "evidence_event_ids"
    ] == [
        presentation["formed_event_id"],
        result["source_recovery"]["event_id"],
    ]


def test_projector_refuses_identified_basis_over_a_no_match_comparison():
    # The malformed chain curator named: no-match comparison, forged
    # identification claiming a valid alternative, forged recovery with
    # correct C/A/G identities. The projector now refuses at the
    # identification, before any recovery can rest on it.
    ledger = EventLedger()
    presentation, finding = _exchange(ledger, "not a coordinate\n")
    good_payload = ledger.get(finding["identification"]["event_id"]).payload
    formed_payload = ledger.get(presentation["formed_event_id"]).payload
    valid_alternative = formed_payload["alternatives"][0]
    ledger.append(
        "operator.exchange.identification_occurred",
        "w",
        {
            **good_payload,
            "identification_ref": "forged",
            "basis": "identified",
            "outcome": "alternative-identified",
            "identified_alternative": {
                "alternative_id": valid_alternative["alternative_id"],
                "role": valid_alternative["role"],
                "response_coordinate": valid_alternative["response_coordinate"],
                "rendered_label": valid_alternative["rendered_label"],
            },
        },
        session_id="s",
    )
    with pytest.raises(
        ValueError, match="derived from its recorded comparison"
    ):
        _standing(ledger)


def test_projector_refuses_forged_representation_and_response_evidence():
    for forged_fields in (
        {
            "representation": {
                "purpose": "forged purpose",
                "scope": "workspace:w;session:s",
                "provenance": "forged",
                "evidence_event_ids": [],
                "known_loss": [],
                "unknowns": [],
                "conflicts": [],
            }
        },
        {"response_ingress_event_id": "evt_forged"},
        {"response_capture_event_id": "evt_forged"},
    ):
        ledger = EventLedger()
        _recovered_exchange(ledger)
        good = next(
            event
            for event in ledger.list("w")
            if event.kind == "operator.presentation.source_recovered"
        )
        ledger.append(
            "operator.presentation.source_recovered",
            "w",
            {**good.payload, "recovery_ref": "forged", **forged_fields},
            session_id="s",
        )
        with pytest.raises(ValueError):
            _standing(ledger)


def test_projector_refuses_forged_relation_standing_coordinates():
    for forged_fields in (
        {"warrant_basis": "derived from operator response text"},
        {"known_loss": ["nothing was lost"]},
        {"unknowns": []},
        {"conflicts": ["fabricated conflict"]},
    ):
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
            {**good.payload, "relation_ref": "forged", **forged_fields},
            session_id="s",
        )
        with pytest.raises(ValueError, match="does not agree"):
            _standing(ledger)


def test_projector_refuses_emission_naming_a_foreign_formation():
    ledger = EventLedger()
    first = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    second = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    ledger.append(
        "operator.presentation.emitted",
        "w",
        {
            "attempt_ref": None,
            "presentation_ref": second["presentation_id"],
            "formed_event_id": first["formed_event_id"],
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "lineage": [first["formed_event_id"]],
            "mutates_cluster": False,
        },
        session_id="s",
    )
    with pytest.raises(
        ValueError, match="does not name its recorded formation"
    ):
        _standing(ledger)


def test_projector_refuses_comparison_contradicting_recorded_ingress():
    # The deepest forged chain: real ingress "not a coordinate", forged
    # comparison using the real ingress and capture identities but claiming
    # match:1. The projector re-derives the result from recorded R and C
    # and refuses the contradiction.
    ledger = EventLedger()
    _, finding = _exchange(ledger, "not a coordinate\n")
    good_payload = ledger.get(finding["comparison"]["event_id"]).payload
    ledger.append(
        "operator.exchange.comparison_occurred",
        "w",
        {
            **good_payload,
            "comparison_ref": "forged",
            "compared_representation": "1",
            "matched_coordinate": "1",
            "outcome": "match:1",
            "unknowns": [
                "operator intent Unknown",
                "operator selection occurrence Unknown",
            ],
        },
        session_id="s",
    )
    with pytest.raises(
        ValueError, match="derived from recorded testimony on compared_representation"
    ):
        _standing(ledger)


def test_projector_refuses_forged_identified_alternative_testimony():
    # Correct coordinate and binding, forged role and label: the complete
    # identified alternative must equal the recorded reconstruction.
    ledger = EventLedger()
    _, finding = _exchange(ledger, "1\n")
    good_payload = ledger.get(finding["identification"]["event_id"]).payload
    ledger.append(
        "operator.exchange.identification_occurred",
        "w",
        {
            **good_payload,
            "identification_ref": "forged",
            "identified_alternative": {
                **good_payload["identified_alternative"],
                "role": "local-stop",
                "rendered_label": "Stop immediately",
            },
        },
        session_id="s",
    )
    with pytest.raises(
        ValueError, match="derived from its recorded comparison and binding"
    ):
        _standing(ledger)


def test_projector_refuses_duplicate_semantic_references():
    # A later event reusing a prior semantic reference must not overwrite
    # what earlier joins resolved to.
    cases = (
        ("operator.exchange.comparison_occurred", "comparison_ref"),
        ("operator.exchange.identification_occurred", "identification_ref"),
        ("operator.presentation.source_recovered", "recovery_ref"),
        (
            "operator.presentation.meaning_relation_established",
            "relation_ref",
        ),
        ("operator.presentation.formed", "presentation_ref"),
    )
    for kind, reference_key in cases:
        ledger = EventLedger()
        _recovered_exchange(ledger)
        original = next(
            event for event in ledger.list("w") if event.kind == kind
        )
        ledger.append(kind, "w", dict(original.payload), session_id="s")
        with pytest.raises(ValueError, match="duplicate"):
            _standing(ledger)


def test_recovery_runs_only_for_identified_exchanges():
    # Driven directly rather than through the console, which no longer selects
    # participants by recency.  The proof is unchanged: recovery follows an
    # identified exchange only, and a no-match exchange exposes no relation.
    ledger = EventLedger()
    _recovered_exchange(ledger, "1\n")
    _, no_match = _exchange(ledger, "not a coordinate\n")
    assert no_match["identification"]["basis"] == "no-coordinate-match"

    standing = _standing(ledger)
    assert len(standing["source_recoveries"]) == 1
    assert len(standing["meaning_relations"]) == 1

    later = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=standing
    )
    # The latest finding is the no-match, so no recovered relation is exposed.
    assert later["recovered_meaning_relation"] is None
    assert "Recovered source" not in render_operator_presentation(later)
