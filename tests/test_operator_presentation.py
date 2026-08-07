from io import StringIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_ingress_view import format_operator_ingress_view
from seed_runtime.operator_presentation import (
    emit_operator_presentation,
    form_operator_presentation,
    render_operator_presentation,
)
from seed_runtime.operator_session_standing import project_operator_session_standing
from scripts import seed_local

_INGRESS_KINDS = (
    "operator.ingress.raw_material_captured",
    "operator.ingress.representation_examined",
    "operator.ingress.ingress_occurred",
)


def _run_console(text, *, workspace="w", session="s"):
    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id=workspace,
        session_id=session,
        input_stream=StringIO(text),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _standing(ledger, *, workspace="w", session="s"):
    return project_operator_session_standing(
        ledger, workspace_id=workspace, session_id=session
    )


def _form_and_emit(ledger, *, workspace="w", session="s"):
    presentation = form_operator_presentation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        session_standing=_standing(ledger, workspace=workspace, session=session),
    )
    return emit_operator_presentation(
        ledger, presentation=presentation, output_stream=StringIO()
    )


def test_console_forms_c0_before_first_ingress_and_uses_existing_response_path():
    ledger, _ = _run_console("hello\n")

    kinds = [event.kind for event in ledger.list("w")]
    assert kinds == [
        "operator.presentation.formed",
        "operator.presentation.emitted",
        *_INGRESS_KINDS,
        "operator.exchange.comparison_occurred",
        "operator.exchange.identification_occurred",
        "operator.presentation.formed",
        "operator.presentation.emitted",
    ]
    c0_formed, c0_emitted = ledger.list("w")[:2]
    assert c0_formed.payload["session_standing_evidence_ids"] == []
    assert c0_formed.payload["prior_exchange_finding"] is None
    assert c0_formed.payload["recovered_meaning_relation"] is None
    assert c0_formed.payload["current_interaction_goal"] is None
    assert c0_formed.payload["unknowns"] == []
    ingress = ledger.list("w")[4]
    assert ingress.payload["produced_after_presentation_ref"] == c0_formed.payload["presentation_ref"]
    assert ingress.payload["produced_after_presentation_formed_event_id"] == c0_formed.id
    assert ingress.payload["produced_after_presentation_emitted_event_id"] == c0_emitted.id


def test_c0_and_c1_are_formed_and_emitted_in_order():
    ledger, output = _run_console("hello\n")

    events = ledger.list("w")
    ingress_index = next(
        index
        for index, event in enumerate(events)
        if event.kind == "operator.ingress.ingress_occurred"
    )
    formed = [i for i, event in enumerate(events) if event.kind == "operator.presentation.formed"]
    emitted = [i for i, event in enumerate(events) if event.kind == "operator.presentation.emitted"]
    assert formed[0] < emitted[0] < ingress_index < formed[1] < emitted[1]
    assert output.count("Bounded Presentation") == 2


def test_alternatives_carry_complete_coordinates_and_evidence_lineage():
    ledger, _ = _run_console("hello\n")

    standing = _standing(ledger)
    presentation = standing["current_presentation"]
    assert presentation is not None
    assert presentation["purpose"]
    assert presentation["scope"] == "workspace:w;session:s"
    assert presentation["provenance"] is not None
    assert presentation["known_loss"] == [
        "rendered label compresses represented candidate meaning"
    ]
    # No response occurrence exists at formation; that is absence, not
    # Unknown, so the formed Presentation carries no Unknowns.
    assert presentation["unknowns"] == []
    assert presentation["conflicts"] == []
    assert presentation["session_standing_evidence_ids"]
    recorded_ids = {event.id for event in ledger.list("w")}
    assert set(presentation["session_standing_evidence_ids"]) <= recorded_ids
    assert len(presentation["alternatives"]) == 3
    purposes = set()
    for alternative in presentation["alternatives"]:
        assert alternative["alternative_id"]
        assert alternative["role"] in {
            "potential-goal",
            "presentation-navigation",
            "local-stop",
        }
        assert alternative["response_coordinate"]
        assert alternative["rendered_label"]
        source = alternative["represented_source"]
        assert source["identity"].startswith("source:")
        assert source["identity"] != source["meaning"]
        assert source["kind"]
        assert source["attribution"] == "developer-supplied"
        assert source["meaning"]
        assert source["reference"]
        representation = alternative["representation"]
        assert representation["purpose"]
        purposes.add(representation["purpose"])
        assert representation["scope"] == "workspace:w;session:s"
        assert representation["provenance"] == source["reference"]
        assert representation["evidence_event_ids"] == []
        assert representation["known_loss"]
        assert representation["unknowns"] == []
        assert representation["conflicts"] == []
        assert (
            presentation["coordinate_bindings"][alternative["response_coordinate"]]
            == alternative["alternative_id"]
        )
    # The three representation relations carry distinct purposes.
    assert len(purposes) == 3


def test_grammar_acquisition_candidate_is_developer_supplied_not_inferred():
    ledger, _ = _run_console("Learn Klingon immediately\n")

    presentation = _standing(ledger)["current_presentation"]
    goal_alternatives = [
        alternative
        for alternative in presentation["alternatives"]
        if alternative["role"] == "potential-goal"
    ]
    assert len(goal_alternatives) == 1
    source = goal_alternatives[0]["represented_source"]
    assert source["meaning"] == "establish richer shared grammar with the operator"
    assert source["attribution"] == "developer-supplied"
    for field in (source["meaning"], source["kind"], source["reference"]):
        assert "Klingon" not in field


def test_local_stop_alternative_is_not_represented_as_a_goal():
    ledger, _ = _run_console("hello\n")

    presentation = _standing(ledger)["current_presentation"]
    stops = [
        alternative
        for alternative in presentation["alternatives"]
        if alternative["role"] == "local-stop"
    ]
    assert len(stops) == 1
    assert stops[0]["role"] != "potential-goal"
    assert stops[0]["represented_source"]["kind"] == (
        "developer-supplied-local-stop-treatment"
    )
    assert (
        stops[0]["represented_source"]["meaning"]
        == "establish no such goal and stop locally"
    )


def test_navigation_alternative_is_distinct_and_leads_to_the_existing_view():
    ledger, _ = _run_console("hello\n")

    presentation = _standing(ledger)["current_presentation"]
    navigation = [
        alternative
        for alternative in presentation["alternatives"]
        if alternative["role"] == "presentation-navigation"
    ]
    assert len(navigation) == 1
    assert navigation[0]["represented_source"]["reference"] == (
        "seed_runtime.operator_ingress_view.format_operator_ingress_view"
    )
    # The referenced View remains an independently consumable renderer.
    direct = run_operator_ingress_attempt(
        ledger=EventLedger(),
        workspace_id="direct",
        session_id="direct",
        captured_ingress=capture_stdin_material(StringIO("direct material\n")),
        output_stream=StringIO(),
    )
    assert "Operator ingress View" in format_operator_ingress_view(direct)


def test_no_new_meaning_candidate_is_synthesized():
    ledger, output = _run_console("hello\n")

    presentation = _standing(ledger)["current_presentation"]
    assert len(presentation["alternatives"]) == 3
    assert all(
        alternative["represented_source"]["attribution"] == "developer-supplied"
        for alternative in presentation["alternatives"]
    )
    assert " means " not in output
    assert " means " not in render_operator_presentation(presentation)


def test_presentations_from_other_workspaces_or_sessions_cannot_enter():
    ledger = EventLedger()
    _form_and_emit(ledger, workspace="w", session="s1")
    _form_and_emit(ledger, workspace="other-w", session="s1")

    same_workspace_other_session = _standing(ledger, workspace="w", session="s2")
    assert same_workspace_other_session["presentations"] == {}
    assert same_workspace_other_session["current_presentation"] is None
    own = _standing(ledger, workspace="w", session="s1")
    assert len(own["presentations"]) == 1


def test_presentation_projection_is_deterministic_under_unrelated_events():
    ledger = EventLedger()
    _form_and_emit(ledger)
    before = _standing(ledger)

    ledger.append("unrelated.kind", "w", {"noise": True}, session_id="s")
    _form_and_emit(ledger, session="elsewhere")
    after = _standing(ledger)

    assert after == before


def test_next_console_iteration_recovers_c1_and_forms_c2():
    # Direct recovery: after C1 is recorded, the read side returns its
    # complete alternatives and bindings.
    ledger = EventLedger()
    c1 = _form_and_emit(ledger)
    recovered = _standing(ledger)["current_presentation"]
    assert recovered["presentation_id"] == c1["presentation_id"]
    assert recovered["alternatives"] == c1["alternatives"]
    assert recovered["coordinate_bindings"] == c1["coordinate_bindings"]
    assert recovered["emitted_event_id"] == c1["emitted_event_id"]

    # Through the console: the second iteration consumes Standing containing
    # C1 and forms C2.
    console_ledger, output = _run_console("first\nsecond\n")
    standing = _standing(console_ledger)
    assert len(standing["presentations"]) == 3
    assert output.count("Bounded Presentation") == 3
    _, second_id, third_id = list(standing["presentations"])
    assert standing["current_presentation"]["presentation_id"] == third_id
    c1 = standing["presentations"][second_id]
    c2 = standing["presentations"][third_id]
    # C2's recorded formation consumed the Standing Evidence containing
    # C1's formation and emission occurrences, not merely later events.
    assert c1["formed_event_id"] in c2["session_standing_evidence_ids"]
    assert c1["emitted_event_id"] in c2["session_standing_evidence_ids"]
    # The represented source candidates keep stable exact identities
    # across formations.
    identities = lambda presentation: [
        alternative["represented_source"]["identity"]
        for alternative in presentation["alternatives"]
    ]
    assert identities(c1) == identities(c2)


def test_first_interaction_compares_against_initial_presentation():
    ledger, _ = _run_console("first\n")

    kinds = {event.kind for event in ledger.list("w")}
    assert kinds == {
        *_INGRESS_KINDS,
        "operator.presentation.formed",
        "operator.presentation.emitted",
        "operator.exchange.comparison_occurred",
        "operator.exchange.identification_occurred",
    }
    ingress = next(
        event
        for event in ledger.list("w")
        if event.kind == "operator.ingress.ingress_occurred"
    )
    first_presentation = next(iter(_standing(ledger)["presentations"].values()))
    assert ingress.payload["produced_after_presentation_ref"] == first_presentation["presentation_id"]


def test_direct_one_attempt_view_behavior_remains_valid():
    ledger = EventLedger()
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO("direct material\n")),
        output_stream=StringIO(),
    )

    rendered = format_operator_ingress_view(projection)
    assert 'Represented material: "direct material\\n"' in rendered
    assert "Bounded Presentation" not in rendered
    kinds = [event.kind for event in ledger.list("w")]
    assert kinds == list(_INGRESS_KINDS)


def test_formation_is_recorded_before_emission_and_they_stay_distinct():
    ledger = EventLedger()
    presentation = form_operator_presentation(
        ledger,
        workspace_id="w",
        session_id="s",
        session_standing=_standing(ledger),
    )
    assert presentation["emitted_event_id"] is None
    assert _standing(ledger)["current_presentation"] is None

    emit_operator_presentation(
        ledger, presentation=presentation, output_stream=StringIO()
    )
    recovered = _standing(ledger)["current_presentation"]
    assert recovered["presentation_id"] == presentation["presentation_id"]
