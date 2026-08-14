from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_representation import (
    emit_operator_representation,
    record_operator_representation,
    render_operator_representation,
)
from seed_runtime.operator_response_comparison import (
    run_operator_response_comparison_and_identification,
)
from seed_runtime.operator_session_standing import read_operator_session_standing
from tests.closed_choice_fixture import CLOSED_CHOICE_FIXTURE_SOURCES
from seed_runtime.operator_console import run_persistent_operator_console


def _standing(ledger, *, workspace="w", session="s"):
    return read_operator_session_standing(
        ledger, workspace_id=workspace, session_id=session
    )


def _emit_representation(ledger, *, workspace="w", session="s"):
    representation = record_operator_representation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        session_standing=_standing(ledger, workspace=workspace, session=session),
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    return emit_operator_representation(
        ledger, representation=representation, output_stream=StringIO()
    )


def _capture_after(ledger, representation, text, *, workspace="w", session="s"):
    attempt_standing = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id=workspace,
        session_id=session,
        captured_ingress=capture_stdin_material(StringIO(text)),
        output_stream=StringIO(),
    )
    return attempt_standing["current_standing"]["preserved_ingress"]["evidence_event_id"]


def _compare(ledger, representation, ingress_event_id, *, workspace="w", session="s"):
    return run_operator_response_comparison_and_identification(
        ledger,
        workspace_id=workspace,
        session_id=session,
        representation=representation,
        response_ingress_event_id=ingress_event_id,
    )


def _exchange(ledger, text, *, workspace="w", session="s"):
    representation = _emit_representation(ledger, workspace=workspace, session=session)
    ingress_event_id = _capture_after(
        ledger, representation, text, workspace=workspace, session=session
    )
    finding = _compare(
        ledger, representation, ingress_event_id, workspace=workspace, session=session
    )
    return representation, ingress_event_id, finding


def test_compare_requires_an_emitted_representation_with_recorded_reference():
    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        workspace_id="w",
        session_id="s",
        session_standing=_standing(ledger),
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    ingress_event_id = _capture_after(ledger, representation, "1\n")

    with pytest.raises(ValueError, match="no emission evidence"):
        _compare(ledger, representation, ingress_event_id)

    # The recorded-chain preconditions that remain are still enforced.
    emitted = _emit_representation(ledger)
    with pytest.raises(ValueError, match="not a representation event"):
        _compare(
            ledger,
            {**emitted, "representation_event_id": ingress_event_id},
            _capture_after(ledger, emitted, "1\n"),
        )

    # Nothing asserts here that an arbitrary recorded Representation and an
    # arbitrary recorded ingress may participate in one Compare.  The recency
    # pairing that was removed was false, and its absence does not make every
    # pairing applicable: 01.Standing.E.1 requires the Responsibility
    # performing the exact Act to determine Applicability for each proposed
    # input, and a caller supplying two references is not that determination.
    # That route is unestablished, so this machinery stays dormant.


def test_comparison_provenance_records_the_subjects_that_participated():
    ledger = EventLedger()
    representation, ingress_event_id, finding = _exchange(ledger, "1\n")

    # The ingress names no Representation; the comparison's provenance is what
    # records which subjects it input.
    ingress = ledger.get(ingress_event_id)
    assert not any(k.startswith("yielded_after") for k in ingress.payload)
    comparison_event = ledger.get(finding["comparison"]["event_id"])
    assert comparison_event.payload["provenance_occurrence_refs"] == [
        representation["representation_event_id"],
        representation["emitted_event_id"],
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
        "no-represented-alternative-identified"
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
    assert comparison_event.payload["exact_act"] != (
        identification_event.payload["exact_act"]
    )
    assert comparison_event.payload["dimensions"]["responsibility"] != (
        identification_event.payload["dimensions"]["responsibility"]
    )


def test_match_with_applicable_binding_identifies_alternative():
    ledger = EventLedger()
    representation, _, finding = _exchange(ledger, "3\n")

    identified = finding["identification"]["identified_alternative"]
    assert finding["identification"]["basis"] == "identified"
    assert identified["role"] == "representation-navigation"
    assert identified["response_coordinate"] == "3"
    assert identified["alternative_id"] == (
        representation["coordinate_bindings"]["3"]
    )


def _record_malformed_representation(ledger, mutate_bindings, *, workspace="w", session="s"):
    """Record Representation source coordinates whose binding relation is malformed.

    A well-formed representation Act supplies the payload shape; the malformed C is
    then recorded as its own representation Act and emission events, so the broken
    binding belongs to recorded payload rather than a mutated dictionary.
    """
    template = record_operator_representation(
        ledger,
        workspace_id=workspace,
        session_id=session,
        session_standing=_standing(ledger, workspace=workspace, session=session),
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    template_payload = ledger.get(template["representation_event_id"]).payload
    representation_id = template["representation_id"] + "-malformed"
    payload = {
        **template_payload,
        "representation_ref": representation_id,
        "coordinate_bindings": mutate_bindings(
            dict(template_payload["coordinate_bindings"])
        ),
        "dimensions": {
            **template_payload["dimensions"],
            "identity": representation_id,
        },
    }
    formed = ledger.append(
        "operator.representation.recorded", workspace, payload, session_id=session
    )
    malformed_representation = {
        "representation_id": representation_id,
        "workspace_id": workspace,
        "session_id": session,
        "representation_event_id": formed.id,
        "emitted_event_id": None,
        "alternatives": template_payload["alternatives"],
        "prior_exchange_finding": None,
        "represented_relation": None,
    }
    emit_operator_representation(
        ledger, representation=malformed_representation, output_stream=StringIO()
    )
    return {
        "representation_id": representation_id,
        "representation_event_id": formed.id,
        "emitted_event_id": malformed_representation["emitted_event_id"],
    }


def test_recorded_broken_binding_does_not_identify_an_alternative():
    # Recorded binding maps the matched coordinate to an alternative outside
    # this exact representation: no lawful identification, and no unsupported A.
    ledger = EventLedger()
    inapplicable = _record_malformed_representation(
        ledger, lambda bindings: {**bindings, "2": "represented_alternative_foreign"}
    )
    ingress_event_id = _capture_after(ledger, inapplicable, "2\n")
    finding = _compare(ledger, inapplicable, ingress_event_id)
    assert finding["comparison"]["matched_coordinate"] == "2"
    assert finding["identification"]["identified_alternative"] is None
    assert finding["identification"]["basis"] == "binding-inapplicable"

    # Recorded coordinate whose binding is absent: match, then no lawful
    # identification -- distinct from no-coordinate-match.
    absent_ledger = EventLedger()
    absent = _record_malformed_representation(
        absent_ledger,
        lambda bindings: {k: v for k, v in bindings.items() if k != "2"},
    )
    ingress_event_id = _capture_after(absent_ledger, absent, "2\n")
    finding = _compare(absent_ledger, absent, ingress_event_id)
    assert finding["comparison"]["matched_coordinate"] == "2"
    assert finding["identification"]["identified_alternative"] is None
    assert finding["identification"]["basis"] == "binding-absent"


def test_mutated_representation_is_structurally_refused():
    # The recorded representation payload is authoritative; a supplied attempt_standing
    # that disagrees with it is refused rather than compared.
    ledger = EventLedger()
    representation = _emit_representation(ledger)
    ingress_event_id = _capture_after(ledger, representation, "2\n")

    mutated = dict(representation)
    mutated["coordinate_bindings"] = {
        **representation["coordinate_bindings"],
        "2": "represented_alternative_foreign",
    }
    with pytest.raises(ValueError, match="disagrees with recorded"):
        _compare(ledger, mutated, ingress_event_id)


def test_incomplete_recorded_chain_is_refused():
    ledger = EventLedger()
    first = _emit_representation(ledger)
    second = _emit_representation(ledger)
    ingress_event_id = _capture_after(ledger, second, "1\n")

    # Emission evidence naming a different representation's emission.
    crossed = dict(second)
    crossed["emitted_event_id"] = first["emitted_event_id"]
    with pytest.raises(ValueError, match="does not record this exact representation"):
        _compare(ledger, crossed, ingress_event_id)

    # Representation Act evidence that is not a representation event.
    wrong_kind = dict(second)
    wrong_kind["representation_event_id"] = ingress_event_id
    with pytest.raises(ValueError, match="not a representation event"):
        _compare(ledger, wrong_kind, ingress_event_id)


def test_no_match_establishes_no_negative_standing():
    ledger = EventLedger()
    _, _, finding = _exchange(ledger, "unmatched material\n")

    comparison_event = ledger.get(finding["comparison"]["event_id"])
    payload = comparison_event.payload
    assert payload["unknowns"] == [
        "response represented relation Unknown",
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


def test_identification_does_not_establish_represented_source():
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
    # No exact source identity or candidate relation is carried; the word
    # `represented relation` may appear only inside the authority denial.
    assert "source:" not in flattened
    assert identified["rendered_label"] in flattened
    assert "establish richer shared grammar with the operator" not in flattened


def test_representation_act_event_evidences_bindings_despite_empty_upstream_lists():
    ledger = EventLedger()
    representation, _, finding = _exchange(ledger, "1\n")

    identification_event = ledger.get(finding["identification"]["event_id"])
    assert identification_event.payload["representation_event_id"] == (
        representation["representation_event_id"]
    )
    assert representation["representation_event_id"] in (
        identification_event.payload["provenance_occurrence_refs"]
    )
    representation_event = ledger.get(representation["representation_event_id"])
    for alternative in representation_event.payload["alternatives"]:
        assert alternative["representation"]["evidence_event_ids"] == []


def test_no_synthetic_developer_source_evidence_event_is_created():
    ledger = EventLedger()
    _exchange(ledger, "1\n")

    kinds = {event.kind for event in ledger.list("w")}
    assert kinds == {
        "operator.ingress.raw_material_captured",
        "operator.ingress.representation_examined",
        "operator.ingress.ingress_occurred",
        "operator.representation.recorded",
        "operator.representation.emission_attempted",
        "operator.representation.emitted",
        "operator.exchange.comparison_occurred",
        "operator.exchange.identification_occurred",
    }


def test_cross_session_and_cross_workspace_material_cannot_participate():
    ledger = EventLedger()
    foreign = _emit_representation(ledger, workspace="w", session="other")
    ingress_event_id = _capture_after(ledger, foreign, "1\n")

    with pytest.raises(ValueError, match="another workspace or session"):
        _compare(ledger, foreign, ingress_event_id)

    own = _emit_representation(ledger)
    foreign_workspace = _emit_representation(ledger, workspace="w2")
    own_ingress = _capture_after(ledger, own, "1\n")
    with pytest.raises(ValueError, match="another workspace or session"):
        _compare(ledger, foreign_workspace, own_ingress, workspace="w2")


def test_session_projector_validates_findings_deterministically():
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


def test_later_representation_reads_findings_without_stronger_standing():
    ledger = EventLedger()
    _exchange(ledger, "1\n")

    later = record_operator_representation(
        ledger,
        workspace_id="w",
        session_id="s",
        session_standing=_standing(ledger),
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    finding = later["prior_exchange_finding"]
    assert finding["identification"]["basis"] == "identified"
    representation_event = ledger.get(later["representation_event_id"])
    assert representation_event.payload["prior_exchange_finding"] == finding
    rendered = str(representation_event.payload)
    assert "Operator selected" not in rendered
    assert "intended" not in rendered


def test_exit_boundary_is_explicit_and_unambiguous():
    # `exit` escapes before ingress recording, after the ordinary C0 path.
    ledger = EventLedger()
    output = StringIO()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("exit\n"),
        output_stream=output,
    )
    assert [event.kind for event in ledger.list("w")] == [
        "operator.representation.recorded",
        "operator.representation.emission_attempted",
        "operator.representation.emitted",
    ]

    # The recorded representation coordinate is disjoint from the exit byte
    # form, and choosing it flows through recorded Compare/Identification
    # without closing the interaction or recording a stopping occurrence.
    exchange_ledger = EventLedger()
    representation, _, finding = _exchange(exchange_ledger, "3\n")
    assert "exit" not in representation["coordinate_bindings"]
    assert finding["identification"]["identified_alternative"]["role"] == (
        "representation-navigation"
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
    malformed = _record_malformed_representation(
        ledger, lambda bindings: {**bindings, "2": "represented_alternative_foreign"}
    )
    ingress_event_id = _capture_after(ledger, malformed, "2\n")
    _compare(ledger, malformed, ingress_event_id)

    later = record_operator_representation(
        ledger,
        workspace_id="w",
        session_id="s",
        session_standing=_standing(ledger),
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    from seed_runtime.operator_representation import render_operator_representation

    rendered = render_operator_representation(later)
    assert (
        "coordinate 2 matched within" in rendered
        and "no represented alternative was lawfully identified "
        "(binding-inapplicable)" in rendered
    )
    assert "no coordinate match" not in rendered
    assert "corresponds to the captured material" not in rendered


def test_exchange_findings_are_exposed_by_a_later_representation():
    # The console no longer selects participants by recency, so the exchange is
    # driven directly here.  What is proved is unchanged: recorded findings are
    # exposed by a later Representation without being strengthened.
    ledger = EventLedger()
    _, _, match = _exchange(ledger, "1\n")
    _, _, no_match = _exchange(ledger, "unmatched words\n")

    standing = _standing(ledger)
    assert len(standing["comparisons"]) == 2
    assert len(standing["identifications"]) == 2
    assert standing["latest_exchange_finding"]["comparison"]["outcome"] == (
        "no-coordinate-match"
    )

    later = record_operator_representation(
        ledger,
        workspace_id="w",
        session_id="s",
        session_standing=standing,
        alternative_sources=CLOSED_CHOICE_FIXTURE_SOURCES,
    )
    rendered = render_operator_representation(later)
    assert "Prior exchange: no coordinate match within" in rendered
    assert "requested treatment remain Unknown" in rendered
    assert match["identification"]["basis"] == "identified"
    assert no_match["identification"]["basis"] == "no-coordinate-match"
