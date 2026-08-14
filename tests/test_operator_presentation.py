from io import StringIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_presentation import (
    emit_operator_presentation,
    form_operator_presentation,
    render_operator_presentation,
)
from seed_runtime.operator_session_standing import project_operator_session_standing
from tests.closed_choice_fixture import CLOSED_CHOICE_FIXTURE_SOURCES
from seed_runtime.operator_console import run_persistent_operator_console

_INGRESS_KINDS = (
    "operator.ingress.raw_material_captured",
    "operator.ingress.representation_examined",
    "operator.ingress.ingress_occurred",
)


def _run_console(text, *, workspace="w", session="s"):
    ledger = EventLedger()
    output = StringIO()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id=workspace,
        session_id=session,
        input_stream=StringIO(text),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _fixture_presentation(ledger, *, workspace="w", session="s"):
    """Form one closed-choice Presentation from the explicit fixture.

    The console no longer supplies alternatives; a caller with warrant does.
    These tests exercise the closed-choice shape itself, so they construct it.
    """
    presentation = form_operator_presentation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        session_standing=_standing(ledger, workspace=workspace, session=session),
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    emit_operator_presentation(
        ledger, presentation=presentation, output_stream=StringIO()
    )
    return presentation


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
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    return emit_operator_presentation(
        ledger, presentation=presentation, output_stream=StringIO()
    )


def test_console_forms_c0_before_first_ingress_and_preserves_provenance_only():
    ledger, _ = _run_console("hello\n")

    # A current Presentation existing does not make the newest ingress and the
    # most recently emitted Presentation participants in one Compare.  The
    # occurrence and its produced-after occurrence relation are preserved; no Compare or
    # Identification follows.
    kinds = [event.kind for event in ledger.list("w")]
    assert kinds == [
        "operator.presentation.formed",
        "operator.presentation.emitted",
        *_INGRESS_KINDS,
        "operator.presentation.formed",
        "operator.presentation.emitted",
    ]
    assert "operator.exchange.comparison_occurred" not in kinds
    assert "operator.exchange.identification_occurred" not in kinds
    c0_formed, c0_emitted = ledger.list("w")[:2]
    assert c0_formed.payload["session_standing_as_of_event_id"] is None
    assert c0_formed.payload["prior_exchange_finding"] is None
    assert c0_formed.payload["recovered_represented_relation"] is None
    assert c0_formed.payload["unknowns"] == []
    # The console attaches no Presentation to the capture: several emissions
    # may precede it and nothing determines which, if any, it relates to.
    ingress = next(
        event
        for event in ledger.list("w")
        if event.kind == "operator.ingress.ingress_occurred"
    )
    assert "produced_after_presentation_ref" not in ingress.payload
    assert "produced_after_presentation_formed_event_id" not in ingress.payload
    assert "produced_after_presentation_emitted_event_id" not in ingress.payload
    assert c0_emitted.kind == "operator.presentation.emitted"


def test_no_compare_or_identification_follows_console_ingress():
    # The required proving: C emitted, E preserved, production provenance
    # retained, and no Compare or Identification occurrence.  Recency does not
    # make C and E participants in one act; 01.Standing.E.1 requires the act
    # owner to determine input-to-act Applicability, and no recovered
    # Responsibility presently proposes those subjects.
    ledger, _ = _run_console("hello\nsecond\nthird\n")

    kinds = [event.kind for event in ledger.list("w")]
    assert "operator.exchange.comparison_occurred" not in kinds
    assert "operator.exchange.identification_occurred" not in kinds
    assert "operator.presentation.source_recovered" not in kinds
    assert "operator.presentation.represented_relation_established" not in kinds
    assert not any(kind.startswith("operator.interaction.") for kind in kinds)

    # Every ingress still carries its exact produced-after occurrence relation.
    presentations = [e for e in ledger.list("w") if e.kind == "operator.presentation.formed"]
    ingresses = [e for e in ledger.list("w") if e.kind == "operator.ingress.ingress_occurred"]
    assert len(ingresses) == 3
    for ingress in ingresses:
        assert "produced_after_presentation_ref" not in ingress.payload

    # Standing projection remains valid and records the occurrences.
    standing = _standing(ledger)
    assert len(standing["preserved_ingress_occurrences"]) == 3
    assert standing["comparisons"] == {}
    assert standing["identifications"] == {}
    assert standing["latest_exchange_finding"] is None


def test_c0_presents_standing_with_no_developer_semantics():
    ledger = EventLedger()
    standing = _standing(ledger)
    c0 = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=standing
    )
    emit_operator_presentation(ledger, presentation=c0, output_stream=StringIO())

    # Empty Standing is legitimately input: the formation occurred and
    # recorded what it input, rather than being skipped.
    payload = ledger.get(c0["formed_event_id"]).payload
    assert payload["session_standing_as_of_event_id"] is None
    assert payload["prior_exchange_finding"] is None
    assert payload["recovered_represented_relation"] is None
    assert payload["unknowns"] == []
    assert payload["conflicts"] == []

    # No developer-supplied alternatives, sources, represented relations, or treatment.
    assert payload["alternatives"] == []
    assert payload["coordinate_bindings"] == {}
    flattened = str(payload)
    for injected in (
        "Establish richer shared grammar",
        "Show current Standing",
        "establish no such result relation and stop locally",
        "developer-supplied",
    ):
        assert injected not in flattened, injected
    rendered = render_operator_presentation(c0)
    assert rendered == f"Bounded Presentation {c0['presentation_id']}\n"
    assert "Respond with exactly one token" not in rendered


def test_formation_dimensions_record_only_coordinates_that_exist():
    ledger = EventLedger()
    standing = _standing(ledger)

    zero = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=standing
    )
    dimensions = ledger.get(zero["formed_event_id"]).payload["dimensions"]
    assert dimensions["content"] == (
        "bounded Presentation of current session Standing"
    )
    assert dimensions["occurrence_preservation"] == (
        "Presentation formation durably recorded"
    )
    # No claim of coordinates this Presentation does not carry, and no
    # classification of the resulting combination as a shape or kind.
    flattened = str(dimensions).lower()
    for claim in (
        "closed-choice",
        "closed choice",
        "alternatives",
        "role-tagged",
        "bindings",
        "represented-source",
    ):
        assert claim not in flattened, claim

    explicit = form_operator_presentation(
        ledger,
        workspace_id="w",
        session_id="s",
        session_standing=standing,
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    # Exact alternative coordinates are recorded because they exist. The
    # combination is not classified: supplying alternatives does not make the
    # Presentation a different constitutional kind.
    dimensions = ledger.get(explicit["formed_event_id"]).payload["dimensions"]
    assert dimensions["content"] == (
        "bounded Presentation of current session Standing with "
        "3 presented alternatives"
    )
    assert dimensions["occurrence_preservation"] == (
        "3 alternatives, roles, response-coordinate bindings, and "
        "represented provenance occurrences durably recorded"
    )
    assert "closed-choice" not in str(dimensions).lower()
    assert "closed choice" not in str(dimensions).lower()


def test_console_presents_standing_only_across_an_ingress():
    ledger, _ = _run_console("hello\n")

    kinds = [event.kind for event in ledger.list("w")]
    assert kinds == [
        "operator.presentation.formed",
        "operator.presentation.emitted",
        *_INGRESS_KINDS,
        "operator.presentation.formed",
        "operator.presentation.emitted",
    ]
    # No automatic exchange, recovery, relation, or result-establishment occurrence.
    assert not any(k.startswith("operator.exchange.") for k in kinds)
    assert not any(k.startswith("operator.interaction.") for k in kinds)
    assert "operator.presentation.source_recovered" not in kinds
    assert "operator.presentation.represented_relation_established" not in kinds

    c0, _, _, _, ingress, c1, _ = ledger.list("w")
    # C1 is formed from Standing that now contains the preserved ingress.
    # C1's Standing was taken through the last event recorded before it,
    # C0's own formation and emission included.
    assert (
        c1.payload["session_standing_as_of_event_id"] == ledger.list("w")[4].id
    )
    assert c0.payload["alternatives"] == [] and c1.payload["alternatives"] == []
    assert "produced_after_presentation_ref" not in ingress.payload
    # No developer result semantics anywhere in the session.
    session = str([e.payload for e in ledger.list("w")])
    assert "developer-supplied" not in session
    assert "Establish richer shared grammar" not in session


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


def test_alternatives_carry_complete_coordinates_and_provenance_evidence():
    ledger = EventLedger()
    _fixture_presentation(ledger)

    standing = _standing(ledger)
    presentation = list(standing["presentations"].values())[-1]
    assert presentation is not None
    assert presentation["formation_result"]
    assert presentation["scope"] == "workspace:w;session:s"
    # provenance is the input Standing's as-of boundary; None here is the
    # recorded absence of prior session events, not a fabricated Unknown.
    assert "provenance" in presentation
    assert presentation["known_loss"] == [
        "rendered label compresses represented candidate relation"
    ]
    # No response occurrence exists at formation; that is absence, not
    # Unknown, so the formed Presentation carries no Unknowns.
    assert presentation["unknowns"] == []
    assert presentation["conflicts"] == []
    # Absent for a formation from empty Standing: recorded absence of a prior
    # input occurrence, not absence of participation.
    assert presentation["session_standing_as_of_event_id"] is None
    assert len(presentation["alternatives"]) == 3
    formation_results = set()
    for alternative in presentation["alternatives"]:
        assert alternative["alternative_id"]
        assert alternative["role"] == "presentation-navigation"
        assert alternative["response_coordinate"]
        assert alternative["rendered_label"]
        source = alternative["represented_source"]
        assert source["identity"].startswith("source:")
        assert source["identity"] != source["represented_result"]
        assert source["kind"]
        assert source["source_role"] == "developer-supplied"
        assert source["represented_result"]
        assert source["reference"]
        representation = alternative["representation"]
        assert representation["formation_result"]
        formation_results.add(representation["formation_result"])
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
    # The three representation relations carry distinct formation results.
    assert len(formation_results) == 3


def test_no_new_represented_relation_candidate_is_synthesized():
    ledger = EventLedger()
    _fixture_presentation(ledger)

    presentation = list(_standing(ledger)["presentations"].values())[-1]
    assert len(presentation["alternatives"]) == 3
    assert all(
        alternative["represented_source"]["source_role"] == "developer-supplied"
        for alternative in presentation["alternatives"]
    )
    assert " means " not in render_operator_presentation(presentation)


def test_presentations_from_other_workspaces_or_sessions_cannot_enter():
    ledger = EventLedger()
    _form_and_emit(ledger, workspace="w", session="s1")
    _form_and_emit(ledger, workspace="other-w", session="s1")

    same_workspace_other_session = _standing(ledger, workspace="w", session="s2")
    assert same_workspace_other_session["presentations"] == {}
    assert same_workspace_other_session["presentations"] == {}
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
    recovered = list(_standing(ledger)["presentations"].values())[-1]
    assert recovered["presentation_id"] == c1["presentation_id"]
    assert recovered["alternatives"] == c1["alternatives"]
    assert recovered["coordinate_bindings"] == c1["coordinate_bindings"]
    assert recovered["emitted_event_id"] == c1["emitted_event_id"]

    # Through the console: the second iteration has as input Standing containing
    # C1 and forms C2.
    console_ledger, output = _run_console("first\nsecond\n")
    standing = _standing(console_ledger)
    assert len(standing["presentations"]) == 3
    assert output.count("Bounded Presentation") == 3
    _, second_id, third_id = list(standing["presentations"])
    assert list(standing["presentations"])[-1] == third_id
    c1 = standing["presentations"][second_id]
    c2 = standing["presentations"][third_id]
    # C2's Standing boundary stands after C1's formation and emission
    # occurrences, so both fall inside the prefix it input.
    positions = {
        event.id: index for index, event in enumerate(console_ledger.list("w"))
    }
    boundary = positions[c2["session_standing_as_of_event_id"]]
    assert positions[c1["formed_event_id"]] < boundary
    assert positions[c1["emitted_event_id"]] < boundary
    # The represented source candidates keep stable exact identities
    # across formations.
    identities = lambda presentation: [
        alternative["represented_source"]["identity"]
        for alternative in presentation["alternatives"]
    ]
    assert identities(c1) == identities(c2)


def test_first_interaction_attaches_no_presentation_to_the_capture():
    ledger, _ = _run_console("first\n")

    # No Presentation is named by the capture.  Emission and ingress
    # occurrences are preserved independently; any relation between them is a
    # later responsible occurrence's to establish and record.
    kinds = {event.kind for event in ledger.list("w")}
    assert kinds == {
        *_INGRESS_KINDS,
        "operator.presentation.formed",
        "operator.presentation.emitted",
    }
    ingress = next(
        event
        for event in ledger.list("w")
        if event.kind == "operator.ingress.ingress_occurred"
    )
    first_presentation = next(iter(_standing(ledger)["presentations"].values()))
    assert "produced_after_presentation_ref" not in ingress.payload
    assert first_presentation["presentation_id"]


def test_formation_is_recorded_before_emission_and_they_stay_distinct():
    ledger = EventLedger()
    presentation = form_operator_presentation(
        ledger,
        workspace_id="w",
        session_id="s",
        session_standing=_standing(ledger),
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    assert presentation["emitted_event_id"] is None
    # Formation is recovered; its emission coordinate stays unrecorded until
    # an emission occurrence supplies it.
    recorded = list(_standing(ledger)["presentations"].values())[-1]
    assert recorded["formed_event_id"] == presentation["formed_event_id"]
    assert recorded["emitted_event_id"] is None

    emit_operator_presentation(
        ledger, presentation=presentation, output_stream=StringIO()
    )
    recovered = list(_standing(ledger)["presentations"].values())[-1]
    assert recovered["presentation_id"] == presentation["presentation_id"]
