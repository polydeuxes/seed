from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_presentation import (
    emit_operator_presentation,
    form_operator_presentation,
)
from seed_runtime.operator_response_comparison import (
    run_operator_response_comparison_and_identification,
)
from seed_runtime.operator_session_standing import project_operator_session_standing
from scripts import seed_local


def _standing(ledger, *, workspace="w", session="s"):
    return project_operator_session_standing(
        ledger, workspace_id=workspace, session_id=session
    )


def _emit_presentation(ledger, *, workspace="w", session="s"):
    presentation = form_operator_presentation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        session_standing=_standing(ledger, workspace=workspace, session=session),
    )
    return emit_operator_presentation(
        ledger, presentation=presentation, output_stream=StringIO()
    )


def _capture_after(ledger, presentation, text, *, workspace="w", session="s"):
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id=workspace,
        session_id=session,
        captured_ingress=capture_stdin_material(StringIO(text)),
        output_stream=StringIO(),
        produced_after_presentation=presentation,
    )
    return projection["current_standing"]["preserved_ingress"]["evidence_event_id"]


def _compare(ledger, presentation, ingress_event_id, *, workspace="w", session="s"):
    return run_operator_response_comparison_and_identification(
        ledger,
        workspace_id=workspace,
        session_id=session,
        presentation=presentation,
        response_ingress_event_id=ingress_event_id,
    )


def _exchange(ledger, text, *, workspace="w", session="s"):
    presentation = _emit_presentation(ledger, workspace=workspace, session=session)
    ingress_event_id = _capture_after(
        ledger, presentation, text, workspace=workspace, session=session
    )
    finding = _compare(
        ledger, presentation, ingress_event_id, workspace=workspace, session=session
    )
    return presentation, ingress_event_id, finding


def test_compare_requires_an_emitted_presentation_with_recorded_reference():
    ledger = EventLedger()
    presentation = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    ingress_event_id = _capture_after(ledger, presentation, "1\n")

    with pytest.raises(ValueError, match="no emission evidence"):
        _compare(ledger, presentation, ingress_event_id)

    emitted = _emit_presentation(ledger)
    unreferenced = _capture_after(ledger, None, "1\n")
    with pytest.raises(ValueError, match="does not record production after"):
        _compare(ledger, emitted, unreferenced)


def test_response_preserves_exact_lineage_to_formation_and_emission():
    ledger = EventLedger()
    presentation, ingress_event_id, finding = _exchange(ledger, "1\n")

    ingress = ledger.get(ingress_event_id)
    assert ingress.payload["produced_after_presentation_ref"] == (
        presentation["presentation_id"]
    )
    assert ingress.payload["produced_after_presentation_formed_event_id"] == (
        presentation["formed_event_id"]
    )
    assert ingress.payload["produced_after_presentation_emitted_event_id"] == (
        presentation["emitted_event_id"]
    )
    comparison_event = ledger.get(finding["comparison"]["event_id"])
    assert comparison_event.payload["lineage"] == [
        presentation["formed_event_id"],
        presentation["emitted_event_id"],
        ingress.payload["raw_material_event_id"],
        ingress_event_id,
    ]


def test_exact_matching_coordinate_records_match():
    ledger = EventLedger()
    _, _, finding = _exchange(ledger, "1\n")

    assert finding["comparison"]["matched_coordinate"] == "1"
    assert finding["comparison"]["outcome"] == "match:1"
    assert finding["comparison"]["compared_representation"] == "1"
    assert finding["comparison"]["coordinate_set"] == ["1", "2", "3"]


def test_nonmatching_material_records_no_coordinate_match():
    ledger = EventLedger()
    _, _, finding = _exchange(ledger, "please restart prometheus\n")

    assert finding["comparison"]["matched_coordinate"] is None
    assert finding["comparison"]["outcome"] == "no-coordinate-match"
    assert finding["identification"]["outcome"] == (
        "no-presented-alternative-identified"
    )
    assert finding["identification"]["basis"] == "no-coordinate-match"


def test_compare_does_not_normalize_beyond_the_representation_boundary():
    # The compared representation is the ingress occurrence's recorded
    # content: decoded text with the single trailing line delimiter removed.
    # Nothing else is trimmed, folded, or interpreted.
    for material, expected in (
        ("1\n", "1"),
        ("1\r\n", "1"),
        ("1 \n", None),
        (" 1\n", None),
        ("01\n", None),
        ("1.\n", None),
        ("\n", None),
    ):
        ledger = EventLedger()
        _, _, finding = _exchange(ledger, material)
        assert finding["comparison"]["matched_coordinate"] == expected, material


def test_compare_and_identification_are_distinct_recorded_results():
    ledger = EventLedger()
    _, _, finding = _exchange(ledger, "2\n")

    comparison_event = ledger.get(finding["comparison"]["event_id"])
    identification_event = ledger.get(finding["identification"]["event_id"])
    assert comparison_event.id != identification_event.id
    assert comparison_event.kind == "operator.exchange.comparison_occurred"
    assert identification_event.kind == "operator.exchange.identification_occurred"
    assert identification_event.payload["comparison_event_id"] == comparison_event.id
    assert comparison_event.payload["purpose"] != (
        identification_event.payload["purpose"]
    )
    assert comparison_event.payload["dimensions"]["responsibility"] != (
        identification_event.payload["dimensions"]["responsibility"]
    )


def test_match_with_applicable_binding_identifies_alternative():
    ledger = EventLedger()
    presentation, _, finding = _exchange(ledger, "3\n")

    identified = finding["identification"]["identified_alternative"]
    assert finding["identification"]["basis"] == "identified"
    assert identified["role"] == "local-stop"
    assert identified["response_coordinate"] == "3"
    assert identified["alternative_id"] == (
        presentation["coordinate_bindings"]["3"]
    )


def _record_malformed_presentation(ledger, mutate_bindings, *, workspace="w", session="s"):
    """Record Presentation testimony whose binding relation is malformed.

    A well-formed formation supplies the payload shape; the malformed C is
    then recorded as its own formation and emission events, so the broken
    binding belongs to recorded testimony rather than a mutated dictionary.
    """
    template = form_operator_presentation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        session_standing=_standing(ledger, workspace=workspace, session=session),
    )
    template_payload = ledger.get(template["formed_event_id"]).payload
    presentation_id = template["presentation_id"] + "-malformed"
    payload = {
        **template_payload,
        "presentation_ref": presentation_id,
        "coordinate_bindings": mutate_bindings(
            dict(template_payload["coordinate_bindings"])
        ),
        "dimensions": {
            **template_payload["dimensions"],
            "identity": presentation_id,
        },
    }
    formed = ledger.append(
        "operator.presentation.formed", workspace, payload, session_id=session
    )
    emitted = ledger.append(
        "operator.presentation.emitted",
        workspace,
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
        session_id=session,
    )
    return {
        "presentation_id": presentation_id,
        "formed_event_id": formed.id,
        "emitted_event_id": emitted.id,
    }


def test_recorded_broken_binding_does_not_identify_an_alternative():
    # Recorded binding maps the matched coordinate to an alternative outside
    # this exact presentation: no lawful identification, and no invented A.
    ledger = EventLedger()
    inapplicable = _record_malformed_presentation(
        ledger, lambda bindings: {**bindings, "2": "presented_alternative_foreign"}
    )
    ingress_event_id = _capture_after(ledger, inapplicable, "2\n")
    finding = _compare(ledger, inapplicable, ingress_event_id)
    assert finding["comparison"]["matched_coordinate"] == "2"
    assert finding["identification"]["identified_alternative"] is None
    assert finding["identification"]["basis"] == "binding-inapplicable"

    # Recorded coordinate whose binding is absent: match, then no lawful
    # identification -- distinct from no-coordinate-match.
    absent_ledger = EventLedger()
    absent = _record_malformed_presentation(
        absent_ledger,
        lambda bindings: {k: v for k, v in bindings.items() if k != "2"},
    )
    ingress_event_id = _capture_after(absent_ledger, absent, "2\n")
    finding = _compare(absent_ledger, absent, ingress_event_id)
    assert finding["comparison"]["matched_coordinate"] == "2"
    assert finding["identification"]["identified_alternative"] is None
    assert finding["identification"]["basis"] == "binding-absent"


def test_mutated_projection_is_structurally_refused():
    # The recorded formation payload is authoritative; a supplied projection
    # that disagrees with it is refused rather than compared.
    ledger = EventLedger()
    presentation = _emit_presentation(ledger)
    ingress_event_id = _capture_after(ledger, presentation, "2\n")

    mutated = dict(presentation)
    mutated["coordinate_bindings"] = {
        **presentation["coordinate_bindings"],
        "2": "presented_alternative_foreign",
    }
    with pytest.raises(ValueError, match="disagrees with recorded"):
        _compare(ledger, mutated, ingress_event_id)


def test_incomplete_recorded_chain_is_refused():
    ledger = EventLedger()
    first = _emit_presentation(ledger)
    second = _emit_presentation(ledger)
    ingress_event_id = _capture_after(ledger, second, "1\n")

    # Emission evidence naming a different presentation's emission.
    crossed = dict(second)
    crossed["emitted_event_id"] = first["emitted_event_id"]
    with pytest.raises(ValueError, match="does not record this exact presentation"):
        _compare(ledger, crossed, ingress_event_id)

    # Formation evidence that is not a formation event.
    wrong_kind = dict(second)
    wrong_kind["formed_event_id"] = ingress_event_id
    with pytest.raises(ValueError, match="not a presentation formation event"):
        _compare(ledger, wrong_kind, ingress_event_id)


def test_no_match_establishes_no_negative_standing():
    ledger = EventLedger()
    _, _, finding = _exchange(ledger, "unmatched material\n")

    comparison_event = ledger.get(finding["comparison"]["event_id"])
    payload = comparison_event.payload
    assert payload["unknowns"] == [
        "response meaning Unknown",
        "operator intent Unknown",
        "operator selection occurrence Unknown",
        "requested treatment Unknown",
    ]
    assert payload["conflicts"] == []
    # No recorded coordinate asserts nonresponse, nonparticipation,
    # negative intent, or selection.
    flattened = str(payload)
    assert "not a response" not in flattened
    assert "nonparticipation" not in flattened
    assert "selected" not in flattened


def test_identification_does_not_recover_represented_source():
    ledger = EventLedger()
    _, _, finding = _exchange(ledger, "1\n")

    identified = finding["identification"]["identified_alternative"]
    assert set(identified) == {
        "alternative_id",
        "role",
        "response_coordinate",
        "rendered_label",
    }
    identification_event = ledger.get(finding["identification"]["event_id"])
    flattened = str(identification_event.payload)
    # No exact source identity or candidate meaning is carried; the word
    # `meaning` may appear only inside the authority denial.
    assert "source:" not in flattened
    assert identified["rendered_label"] in flattened
    assert "establish richer shared grammar with the operator" not in flattened


def test_formation_event_evidences_bindings_despite_empty_upstream_lists():
    ledger = EventLedger()
    presentation, _, finding = _exchange(ledger, "1\n")

    identification_event = ledger.get(finding["identification"]["event_id"])
    assert identification_event.payload["presentation_formed_event_id"] == (
        presentation["formed_event_id"]
    )
    assert presentation["formed_event_id"] in (
        identification_event.payload["lineage"]
    )
    formed_event = ledger.get(presentation["formed_event_id"])
    for alternative in formed_event.payload["alternatives"]:
        assert alternative["representation"]["evidence_event_ids"] == []


def test_no_synthetic_developer_source_evidence_event_is_created():
    ledger = EventLedger()
    _exchange(ledger, "1\n")

    kinds = {event.kind for event in ledger.list("w")}
    assert kinds == {
        "operator.ingress.raw_material_captured",
        "operator.ingress.representation_examined",
        "operator.ingress.ingress_occurred",
        "operator.presentation.formed",
        "operator.presentation.emitted",
        "operator.exchange.comparison_occurred",
        "operator.exchange.identification_occurred",
    }


def test_cross_session_and_cross_workspace_material_cannot_participate():
    ledger = EventLedger()
    foreign = _emit_presentation(ledger, workspace="w", session="other")
    ingress_event_id = _capture_after(ledger, foreign, "1\n")

    with pytest.raises(ValueError, match="another workspace or session"):
        _compare(ledger, foreign, ingress_event_id)

    own = _emit_presentation(ledger)
    foreign_workspace = _emit_presentation(ledger, workspace="w2")
    own_ingress = _capture_after(ledger, own, "1\n")
    with pytest.raises(ValueError, match="another workspace or session"):
        _compare(ledger, foreign_workspace, own_ingress, workspace="w2")


def test_session_projector_recovers_findings_deterministically():
    ledger = EventLedger()
    _, _, finding = _exchange(ledger, "1\n")

    before = _standing(ledger)
    assert list(before["comparisons"]) == [finding["comparison"]["comparison_ref"]]
    assert list(before["identifications"]) == [
        finding["identification"]["identification_ref"]
    ]
    latest = before["latest_exchange_finding"]
    assert latest["comparison"]["matched_coordinate"] == "1"
    assert latest["identification"]["basis"] == "identified"

    ledger.append("unrelated.kind", "w", {"noise": True}, session_id="s")
    assert _standing(ledger) == before


def test_later_presentation_consumes_findings_without_stronger_standing():
    ledger = EventLedger()
    _exchange(ledger, "1\n")

    later = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    finding = later["prior_exchange_finding"]
    assert finding["identification"]["basis"] == "identified"
    formed_event = ledger.get(later["formed_event_id"])
    assert formed_event.payload["prior_exchange_finding"] == finding
    rendered = str(formed_event.payload)
    assert "Operator selected" not in rendered
    assert "intended" not in rendered


def test_exit_boundary_is_explicit_and_unambiguous():
    # `exit` escapes the process boundary before any recording: no events.
    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("exit\n"),
        output_stream=output,
    )
    assert ledger.list("w") == []

    # The recorded local-stop coordinate is disjoint from the exit byte
    # form, and choosing it flows through recorded Compare/Identification
    # without closing the interaction or recording a stopping occurrence.
    exchange_ledger = EventLedger()
    presentation, _, finding = _exchange(exchange_ledger, "3\n")
    assert "exit" not in presentation["coordinate_bindings"]
    assert finding["identification"]["identified_alternative"]["role"] == (
        "local-stop"
    )
    kinds = {event.kind for event in exchange_ledger.list("w")}
    assert "operator.ingress.stopping_occurred" not in kinds


def test_projector_refuses_identification_paired_with_wrong_comparison():
    ledger = EventLedger()
    _, _, finding = _exchange(ledger, "1\n")

    good_identification = ledger.get(finding["identification"]["event_id"])
    ledger.append(
        "operator.exchange.identification_occurred",
        "w",
        {
            **good_identification.payload,
            "identification_ref": "operator_alternative_identification_forged",
            "comparison_event_id": "evt_nonexistent",
        },
        session_id="s",
    )
    with pytest.raises(ValueError, match="does not agree with its recorded"):
        _standing(ledger)


def test_matched_but_unidentified_is_not_rendered_as_no_match():
    ledger = EventLedger()
    malformed = _record_malformed_presentation(
        ledger, lambda bindings: {**bindings, "2": "presented_alternative_foreign"}
    )
    ingress_event_id = _capture_after(ledger, malformed, "2\n")
    _compare(ledger, malformed, ingress_event_id)

    later = form_operator_presentation(
        ledger, workspace_id="w", session_id="s", session_standing=_standing(ledger)
    )
    from seed_runtime.operator_presentation import render_operator_presentation

    rendered = render_operator_presentation(later)
    assert (
        "coordinate 2 matched within" in rendered
        and "no presented alternative was lawfully identified "
        "(binding-inapplicable)" in rendered
    )
    assert "no coordinate match" not in rendered
    assert "corresponds to the captured material" not in rendered


def test_console_full_exchange_and_next_presentation_exposes_finding():
    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("Hello\n1\nunmatched words\nexit\n"),
        output_stream=output,
    )
    rendered = output.getvalue()

    assert rendered.count("Bounded Presentation") == 3
    assert (
        "Prior exchange: alternative 1 (Establish richer shared grammar with "
        "the Operator) corresponds to the captured material within" in rendered
    )
    assert "Operator intent and selection remain Unknown." in rendered
    assert "Prior exchange: no coordinate match within" in rendered
    assert "requested treatment remain Unknown" in rendered
    standing = _standing(ledger)
    assert len(standing["comparisons"]) == 2
    assert len(standing["identifications"]) == 2
    assert standing["latest_exchange_finding"]["comparison"]["outcome"] == (
        "no-coordinate-match"
    )
