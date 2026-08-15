from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_representation import (
    emit_operator_representation,
    read_operator_representation,
    record_operator_representation,
)
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from tests.bounded_alternative_fixture import BOUNDED_ALTERNATIVE_FIXTURE_SOURCES
from seed_runtime.operator_console import run_persistent_operator_console

_INGEST_KINDS = (
    "material.ingest.act_evidenced",
    "operator.yield.evidence_recorded",
    "material.ingest.occurred",
)
_EMISSION_EDGE_EVIDENCE_KINDS = (
    "operator.representation.emission_attempt_locality_evidenced",
    "operator.representation.emission_act_evidenced",
    "operator.representation.emission_locality_evidenced",
    "operator.yield.evidence_recorded",
)
_FAILED_EMISSION_EVIDENCE_KINDS = (
    "operator.representation.emission_outcome_act_evidenced",
    "operator.yield.evidence_recorded",
)
_REPRESENTATION_EDGE_EVIDENCE_KINDS = (
    "operator.representation.act_evidenced",
    "operator.yield.evidence_recorded",
    "operator.representation.locality_evidenced",
)


def _run_console(text, *, locality="s"):
    ledger = EventLedger()
    output = StringIO()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=locality,
        input_stream=binary_input(text),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _fixture_representation(ledger, *, locality="s"):
    """Record one bounded-alternative Representation from the explicit fixture."""
    representation = record_operator_representation(
        ledger,
        locality_identity=locality,
        locality_standing=_standing(ledger, locality=locality),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    emit_operator_representation(
        ledger, representation=representation, output_stream=StringIO()
    )
    return representation


def _standing(ledger, *, locality="s"):
    return read_operator_locality_standing(
        ledger, locality_identity=locality
    )


def _record_and_emit(ledger, *, locality="s"):
    representation = record_operator_representation(
        ledger,
        locality_identity=locality,
        locality_standing=_standing(ledger, locality=locality),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    return emit_operator_representation(
        ledger, representation=representation, output_stream=StringIO()
    )


def _recorded_representation(ledger, *, locality="s"):
    representation = record_operator_representation(
        ledger,
        locality_identity=locality,
        locality_standing=_standing(ledger, locality=locality),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    return representation, ledger.get(representation["representation_event_identity"])


def test_representation_reader_reads_the_exact_recorded_representation():
    ledger = EventLedger()
    representation, event = _recorded_representation(ledger)

    recorded = read_operator_representation(ledger, event.identity)

    assert recorded == {
        "representation_identity": representation["representation_identity"],
        "representation_act_identity": representation["representation_act_identity"],
        "act_occurrence_identity": representation["act_occurrence_identity"],
        "locality_identity": representation["locality_identity"],
        "representation_result": representation["representation_result"],
        "alternative_material": representation["alternative_material"],
        "coordinate_binding": representation["coordinate_binding"],
        "representation_event_identity": representation["representation_event_identity"],
        "emission_text": representation["emission_text"],
    }


@pytest.mark.parametrize(
    "coordinate",
    ("responsible_act_evidence_identity", "locality_evidence_identity", "yield_evidence_identity"),
)
def test_representation_reader_refuses_each_missing_evidence_pointer(coordinate):
    ledger = EventLedger()
    _, event = _recorded_representation(ledger)
    event.material[coordinate] = "missing-evidence"

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_representation_reader_refuses_a_developer_formed_event():
    ledger = EventLedger()
    event = ledger.append(
        "operator.representation.recorded",
        {
            "representation_reference": "developer-supplied",
            "representation_act_identity": "developer-supplied-act",
            "act_occurrence_identity": "developer-supplied-occurrence",
        },
        locality_identity="s",
    )

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_representation_reader_refuses_a_different_carried_result():
    ledger = EventLedger()
    _, event = _recorded_representation(ledger)
    event.material["emission_text"] += "different"

    with pytest.raises(ValueError, match="Yield is not exact"):
        read_operator_representation(ledger, event.identity)


@pytest.mark.parametrize(
    "evidence_coordinate,event_coordinate",
    (
        ("act_occurrence_identity", "act_occurrence_identity"),
        ("representation_act_identity", "representation_act_identity"),
    ),
)
def test_representation_reader_refuses_different_act_evidence_coordinates(
    evidence_coordinate, event_coordinate
):
    ledger = EventLedger()
    _, event = _recorded_representation(ledger)
    evidence = ledger.get(event.material["responsible_act_evidence_identity"])
    evidence.material[evidence_coordinate] = (
        f"different-{event.material[event_coordinate]}"
    )

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_representation_reader_refuses_different_locality_evidence_content():
    ledger = EventLedger()
    _, event = _recorded_representation(ledger)
    evidence = ledger.get(event.material["locality_evidence_identity"])
    evidence.material["carried_content"]["emission_text"] += "different"

    with pytest.raises(ValueError, match="coordinates are not exact"):
        read_operator_representation(ledger, event.identity)


def test_console_forms_c0_before_first_ingress_and_preserves_provenance_only():
    ledger, _ = _run_console("hello\n")

    # A current Representation existing does not make the newest Ingest and the
    # most recently emitted Representation participants in one Compare.  The
    # occurrence and its yielded-after occurrence relation are preserved; no Compare or
    # Identification follows.
    kinds = [event.kind for event in ledger.list()]
    assert kinds == [
        *_REPRESENTATION_EDGE_EVIDENCE_KINDS,
        "operator.representation.recorded",
        "operator.representation.emission_attempt_recorded",
        *_EMISSION_EDGE_EVIDENCE_KINDS,
        "operator.representation.emitted",
        *_INGEST_KINDS,
        *_REPRESENTATION_EDGE_EVIDENCE_KINDS,
        "operator.representation.recorded",
        "operator.representation.emission_attempt_recorded",
        *_EMISSION_EDGE_EVIDENCE_KINDS,
        "operator.representation.emitted",
    ]
    c0_formed = next(
        event
        for event in ledger.list()
        if event.kind == "operator.representation.recorded"
    )
    c0_emitted = next(
        event
        for event in ledger.list()
        if event.kind == "operator.representation.emitted"
    )
    assert c0_formed.material["locality_standing_as_of_event_identity"] is None
    assert c0_formed.material["unknowns"] == []
    # The console attaches no Representation to the Ingest: several emissions
    # may precede it and nothing determines which, if any, it relates to.
    ingest = next(
        event
        for event in ledger.list()
        if event.kind == "material.ingest.occurred"
    )
    assert "yielded_after_representation_reference" not in ingest.material
    assert "yielded_after_representation_event_identity" not in ingest.material
    assert "yielded_after_representation_emitted_event_identity" not in ingest.material
    assert c0_emitted.kind == "operator.representation.emitted"


def test_console_ingest_adds_only_its_exact_occurrences():
    # The required proving: C emitted, E preserved, yield provenance
    # retained, and no Compare or Identification occurrence.  Recency does not
    # make C and E participants in one act; 01.Standing.E.1 requires the act
    # responsible boundary to determine input-to-Act Applicability, and no read
    # Responsibility presently proposes those subjects.
    ledger, _ = _run_console("hello\nsecond\nthird\n")

    kinds = [event.kind for event in ledger.list()]
    assert not any(kind.startswith("operator.interaction.") for kind in kinds)

    # Every Ingest remains independent of adjacent Representation occurrences.
    representations = [e for e in ledger.list() if e.kind == "operator.representation.recorded"]
    ingests = [e for e in ledger.list() if e.kind == "material.ingest.occurred"]
    assert len(ingests) == 3
    for ingest in ingests:
        assert "yielded_after_representation_reference" not in ingest.material

    # Standing read remains valid and records the occurrences.
    standing = _standing(ledger)
    assert len(standing["ingest_occurrences"]) == 3
    assert all(
        set(occurrence)
        == {
            "ingest_reference",
            "subject_reference",
            "standing",
            "authority",
            "evidence_event_identity",
            "source_role",
        }
        for occurrence in standing["ingest_occurrences"]
    )


def test_c0_presents_standing_with_no_developer_semantics():
    ledger = EventLedger()
    standing = _standing(ledger)
    c0 = record_operator_representation(
        ledger, locality_identity="s", locality_standing=standing
    )
    emit_operator_representation(ledger, representation=c0, output_stream=StringIO())

    # Empty Standing is legitimately input: the representation Act occurred and
    # recorded what it input, rather than being skipped.
    material = ledger.get(c0["representation_event_identity"]).material
    assert material["locality_standing_as_of_event_identity"] is None
    assert material["unknowns"] == []
    assert material["conflicts"] == []

    # No developer-supplied alternative_material, sources, represented relations, or treatment.
    assert material["alternative_material"] == []
    assert material["coordinate_binding"] == {}
    flattened = str(material)
    for injected in (
        "Establish richer shared grammar",
        "Show current Standing",
        "establish no such result relation and stop locally",
        "developer-supplied",
    ):
        assert injected not in flattened, injected
    emission_text = c0["emission_text"]
    assert emission_text == f"Bounded Representation {c0['representation_identity']}\n"
    assert "Respond with exactly one token" not in emission_text


def test_representation_act_dimensions_record_only_coordinates_that_exist():
    ledger = EventLedger()
    standing = _standing(ledger)

    zero = record_operator_representation(
        ledger, locality_identity="s", locality_standing=standing
    )
    dimensions = ledger.get(zero["representation_event_identity"]).material["dimensions"]
    assert dimensions["content"] == (
        "bounded Representation of current Locality Standing"
    )
    assert dimensions["occurrence_preservation"] == (
        "Representation Act durably recorded"
    )
    # No Assertion of coordinates this Representation does not carry, and no
    # classification of the resulting combination as a shape or kind.
    flattened = str(dimensions).lower()
    for forbidden_text in (
        "bounded-alternative",
        "bounded alternative",
        "alternative_material",
        "role-tagged",
        "bindings",
        "represented-source",
    ):
        assert forbidden_text not in flattened, forbidden_text

    explicit = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=standing,
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    dimensions = ledger.get(explicit["representation_event_identity"]).material["dimensions"]
    assert dimensions["content"] == (
        "bounded Representation of current Locality Standing with "
        "alternative material count 3"
    )
    assert dimensions["occurrence_preservation"] == (
        "alternative material count 3; roles, response-coordinate binding, "
        "and represented provenance occurrences durably recorded"
    )
    assert "bounded-alternative" not in str(dimensions).lower()
    assert "bounded alternative" not in str(dimensions).lower()


def test_console_presents_standing_only_across_an_ingest():
    ledger, _ = _run_console("hello\n")

    kinds = [event.kind for event in ledger.list()]
    assert kinds == [
        *_REPRESENTATION_EDGE_EVIDENCE_KINDS,
        "operator.representation.recorded",
        "operator.representation.emission_attempt_recorded",
        *_EMISSION_EDGE_EVIDENCE_KINDS,
        "operator.representation.emitted",
        *_INGEST_KINDS,
        *_REPRESENTATION_EDGE_EVIDENCE_KINDS,
        "operator.representation.recorded",
        "operator.representation.emission_attempt_recorded",
        *_EMISSION_EDGE_EVIDENCE_KINDS,
        "operator.representation.emitted",
    ]
    # No relation or result-Standing occurrence follows by identity.
    assert not any(k.startswith("operator.interaction.") for k in kinds)

    events = ledger.list()
    representations = [
        event for event in events if event.kind == "operator.representation.recorded"
    ]
    c0, c1 = representations
    ingest = next(
        event for event in events if event.kind == "material.ingest.occurred"
    )
    # C1 uses Standing that now contains the Ingest occurrence.
    # C1's Standing was taken through the last event recorded before it,
    # C0's own representation Act and emission included.
    assert (
        c1.material["locality_standing_as_of_event_identity"] == ingest.identity
    )
    assert c0.material["alternative_material"] == [] and c1.material["alternative_material"] == []
    assert "yielded_after_representation_reference" not in ingest.material
    # No developer result semantics anywhere in the locality.
    locality = str([e.material for e in ledger.list()])
    assert "developer-supplied" not in locality
    assert "Establish richer shared grammar" not in locality


def test_c0_and_c1_are_recorded_and_emitted_in_order():
    ledger, output = _run_console("hello\n")

    events = ledger.list()
    ingest_index = next(
        index
        for index, event in enumerate(events)
        if event.kind == "material.ingest.occurred"
    )
    recorded = [
        i for i, event in enumerate(events)
        if event.kind == "operator.representation.recorded"
    ]
    emitted = [i for i, event in enumerate(events) if event.kind == "operator.representation.emitted"]
    assert recorded[0] < emitted[0] < ingest_index < recorded[1] < emitted[1]
    assert output.count("Bounded Representation") == 2


def test_alternatives_carry_complete_coordinates_and_provenance_evidence():
    ledger = EventLedger()
    _fixture_representation(ledger)

    standing = _standing(ledger)
    representation_record = list(standing["representations"].values())[-1]
    assert representation_record is not None
    assert representation_record["representation_result"]
    assert representation_record["scope"] == "locality:s"
    # provenance is the input Standing's as-of boundary; None here is the
    # recorded absence of prior locality events, not a fabricated Unknown.
    assert "provenance" in representation_record
    assert representation_record["known_loss"] == [
        "label compresses represented candidate relation"
    ]
    # No response occurrence exists at representation Act; that is absence, not
    # Unknown, so the supplied Representation carries no Unknowns.
    assert representation_record["unknowns"] == []
    assert representation_record["conflicts"] == []
    # Absent for a representation Act from empty Standing: recorded absence of a prior
    # input occurrence, not absence of participation.
    assert representation_record["locality_standing_as_of_event_identity"] is None
    assert len(representation_record["alternative_material"]) == 3
    representation_results = set()
    for alternative in representation_record["alternative_material"]:
        assert alternative["alternative_identity"]
        assert alternative["role"] == "representation-navigation"
        assert alternative["response_coordinate"]
        assert alternative["label"]
        source = alternative["represented_source"]
        assert source["identity"].startswith("source:")
        assert source["identity"] != source["represented_result"]
        assert source["kind"]
        assert source["source_role"] == "developer-supplied"
        assert source["represented_result"]
        assert source["reference"]
        relation_coordinates = alternative["representation"]
        assert relation_coordinates["representation_result"]
        representation_results.add(relation_coordinates["representation_result"])
        assert relation_coordinates["scope"] == "locality:s"
        assert relation_coordinates["provenance"] == source["reference"]
        assert "evidence_event_identities" not in relation_coordinates
        assert relation_coordinates["known_loss"]
        assert relation_coordinates["unknowns"] == []
        assert relation_coordinates["conflicts"] == []
        assert (
            representation_record["coordinate_binding"][alternative["response_coordinate"]]
            == alternative["alternative_identity"]
        )
    # The three representation relations carry distinct representation Act results.
    assert len(representation_results) == 3


def test_no_new_represented_relation_candidate_is_supplied():
    ledger = EventLedger()
    _fixture_representation(ledger)

    representation = list(_standing(ledger)["representations"].values())[-1]
    assert len(representation["alternative_material"]) == 3
    assert all(
        alternative["represented_source"]["source_role"] == "developer-supplied"
        for alternative in representation["alternative_material"]
    )
    assert " means " not in representation["emission_text"]


def test_representations_from_other_localities_cannot_enter():
    ledger = EventLedger()
    _record_and_emit(ledger, locality="s1")
    _record_and_emit(ledger, locality="s2")

    absent = _standing(ledger, locality="s3")
    assert absent["representations"] == {}
    own = _standing(ledger, locality="s1")
    assert len(own["representations"]) == 1


def test_representation_representation_is_deterministic_under_unrelated_events():
    ledger = EventLedger()
    _record_and_emit(ledger)
    before = _standing(ledger)

    ledger.append("unrelated.kind", {"noise": True}, locality_identity="s")
    _record_and_emit(ledger, locality="elsewhere")
    after = _standing(ledger)

    assert after == before


def test_next_console_iteration_validates_c1_and_forms_c2():
    # Direct read: after C1 is recorded, the read side returns its
    # complete alternative_material and bindings.
    ledger = EventLedger()
    c1 = _record_and_emit(ledger)
    read = list(_standing(ledger)["representations"].values())[-1]
    assert read["representation_identity"] == c1["representation_identity"]
    assert read["alternative_material"] == c1["alternative_material"]
    assert read["coordinate_binding"] == c1["coordinate_binding"]
    assert read["emitted_event_identity"] == c1["emitted_event_identity"]

    # Through the console: the second iteration has as input Standing containing
    # C1 and represents C2.
    console_ledger, output = _run_console("first\nsecond\n")
    standing = _standing(console_ledger)
    assert len(standing["representations"]) == 3
    assert output.count("Bounded Representation") == 3
    _, second_identity, third_identity = list(standing["representations"])
    assert list(standing["representations"])[-1] == third_identity
    c1 = standing["representations"][second_identity]
    c2 = standing["representations"][third_identity]
    # C2's Standing boundary stands after C1's representation Act and emission
    # occurrences, so both fall inside the prefix it input.
    positions = {
        event.identity: index for index, event in enumerate(console_ledger.list())
    }
    boundary = positions[c2["locality_standing_as_of_event_identity"]]
    assert positions[c1["representation_event_identity"]] < boundary
    assert positions[c1["emitted_event_identity"]] < boundary
    # The represented source candidates keep stable exact identities
    # across representation Acts.
    identities = lambda representation: [
        alternative["represented_source"]["identity"]
        for alternative in representation["alternative_material"]
    ]
    assert identities(c1) == identities(c2)


def test_first_interaction_attaches_no_representation_to_the_ingest():
    ledger, _ = _run_console("first\n")

    # No Representation is named by the Ingest. Emission and Ingest
    # occurrences are preserved independently; any relation between them is a
    # later responsible occurrence's to establish and record.
    kinds = {event.kind for event in ledger.list()}
    assert kinds == {
        *_INGEST_KINDS,
        "operator.representation.act_evidenced",
        "operator.representation.locality_evidenced",
        "operator.representation.recorded",
        "operator.representation.emission_attempt_recorded",
        *_EMISSION_EDGE_EVIDENCE_KINDS,
        "operator.representation.emitted",
    }
    ingest = next(
        event
        for event in ledger.list()
        if event.kind == "material.ingest.occurred"
    )
    first_representation = next(iter(_standing(ledger)["representations"].values()))
    assert "yielded_after_representation_reference" not in ingest.material
    assert first_representation["representation_identity"]


def test_representation_act_is_recorded_before_emission_and_they_stay_distinct():
    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    assert representation["emitted_event_identity"] is None
    # Representation Act is read; its emission coordinate stays unrecorded until
    # an emission occurrence supplies it.
    recorded = list(_standing(ledger)["representations"].values())[-1]
    assert recorded["representation_event_identity"] == representation["representation_event_identity"]
    assert recorded["emitted_event_identity"] is None

    representation_event = ledger.get(representation["representation_event_identity"])
    act_evidence = ledger.get(
        representation_event.material["responsible_act_evidence_identity"]
    )
    yield_evidence = ledger.get(representation_event.material["yield_evidence_identity"])
    locality_evidence = ledger.get(
        representation_event.material["locality_evidence_identity"]
    )
    assert representation["representation_act_identity"] == act_evidence.material[
        "representation_act_identity"
    ]
    assert representation["act_occurrence_identity"] == act_evidence.material[
        "act_occurrence_identity"
    ]
    assert representation["act_occurrence_identity"] == yield_evidence.material[
        "dimensions"
    ]["act_occurrence_identity"]
    assert representation["act_occurrence_identity"] == locality_evidence.material[
        "act_occurrence_identity"
    ]
    assert locality_evidence.material["carried_content"]["representation_reference"] == (
        representation["representation_identity"]
    )
    assert "input_role" not in representation_event.material

    emit_operator_representation(
        ledger, representation=representation, output_stream=StringIO()
    )
    read = list(_standing(ledger)["representations"].values())[-1]
    assert read["representation_identity"] == representation["representation_identity"]


def test_emission_preserves_the_exact_text_written_to_its_boundary():
    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    output = StringIO()

    emit_operator_representation(
        ledger, representation=representation, output_stream=output
    )

    emission = ledger.get(representation["emitted_event_identity"])
    assert emission.material["emitted_representation"] == output.getvalue()
    assert emission.material["emitted_representation_kind"] == "text"
    assert emission.material["output_boundary"] == "text_stream_write"
    assert emission.material["write_count"] == len(output.getvalue())
    assert emission.material["provenance_occurrence_references"] == [
        representation["representation_event_identity"],
        representation["emission_attempt_event_identity"],
    ]
    attempt = ledger.get(representation["emission_attempt_event_identity"])
    attempt_locality_evidence = ledger.get(
        representation["emission_attempt_locality_evidence_identity"]
    )
    assert attempt.material["representation"] == output.getvalue()
    assert attempt_locality_evidence.material["carried_content"] == output.getvalue()
    assert attempt_locality_evidence.material["attempt_event_identity"] == attempt.identity
    assert "standing" not in attempt.material["dimensions"]
    assert (
        "output-boundary acceptance remains Unknown until an outcome is recorded"
        in attempt.material["unknowns"]
    )
    assert attempt.identity != emission.material["act_occurrence_identity"]
    assert emission.material["input_role"] == "exact bounded Representation"
    assert emission.material["boundary_result"] == {
        "boundary": "text_stream_write",
        "accepted_representation": output.getvalue(),
        "accepted_representation_kind": "text",
        "accepted_count": len(output.getvalue()),
    }
    act_evidence = ledger.get(emission.material["responsible_act_evidence_identity"])
    locality_evidence = ledger.get(emission.material["locality_evidence_identity"])
    yield_evidence = ledger.get(emission.material["yield_evidence_identity"])
    assert act_evidence.material["representation_reference"] == representation[
        "representation_identity"
    ]
    assert act_evidence.material["act_occurrence_identity"] == emission.material[
        "act_occurrence_identity"
    ]
    assert locality_evidence.material["carried_content"] == output.getvalue()
    assert locality_evidence.material["act_occurrence_identity"] == emission.material[
        "act_occurrence_identity"
    ]
    assert locality_evidence.material["act_occurrence_identity"] != attempt.identity
    assert yield_evidence.material["dimensions"]["act_occurrence_identity"] == emission.material[
        "act_occurrence_identity"
    ]
    assert representation["emission_outcome_event_identity"] == emission.identity


def test_partial_output_write_preserves_attempt_and_failed_occurrences():
    class PartialOutput(StringIO):
        def write(self, value):
            super().write(value[:-1])
            return len(value) - 1

    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
    )

    with pytest.raises(
        ValueError, match="did not accept the exact representation"
    ):
        emit_operator_representation(
            ledger, representation=representation, output_stream=PartialOutput()
        )

    assert [event.kind for event in ledger.list()] == [
        *_REPRESENTATION_EDGE_EVIDENCE_KINDS,
        "operator.representation.recorded",
        "operator.representation.emission_attempt_recorded",
        "operator.representation.emission_attempt_locality_evidenced",
        *_FAILED_EMISSION_EVIDENCE_KINDS,
        "operator.representation.emission_outcome_recorded",
    ]
    failure = ledger.get(representation["emission_outcome_event_identity"])
    assert failure.material["boundary"] == "text_stream_write"
    assert failure.material["write_count"] == len(
        representation["emission_text"]
    ) - 1
    assert failure.material["error"] is None
    assert failure.material["emitted_event_identity"] is None
    assert representation["emitted_event_identity"] is None


def test_write_exception_preserves_unknown_boundary_acceptance():
    class WriteFailure(StringIO):
        def write(self, value):
            super().write(value[:1])
            raise OSError("write failed after an unreported boundary revision")

    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
    )
    output = WriteFailure()

    with pytest.raises(OSError, match="unreported boundary revision"):
        emit_operator_representation(
            ledger, representation=representation, output_stream=output
        )

    assert output.getvalue()
    failure = ledger.get(representation["emission_outcome_event_identity"])
    assert failure.material["boundary"] == "text_stream_write"
    assert failure.material["write_count"] is None
    assert failure.material["error"] == (
        "OSError('write failed after an unreported boundary revision')"
    )
    assert (
        "output-boundary acceptance remains Unknown because write reported no count"
        in failure.material["unknowns"]
    )
    assert representation["emitted_event_identity"] is None


def test_flush_failure_does_not_erase_the_completed_text_stream_write():
    class FlushFailure(StringIO):
        def flush(self):
            raise OSError("flush failed")

    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
    )

    with pytest.raises(OSError, match="flush failed"):
        emit_operator_representation(
            ledger, representation=representation, output_stream=FlushFailure()
        )

    assert [event.kind for event in ledger.list()] == [
        *_REPRESENTATION_EDGE_EVIDENCE_KINDS,
        "operator.representation.recorded",
        "operator.representation.emission_attempt_recorded",
        *_EMISSION_EDGE_EVIDENCE_KINDS,
        "operator.representation.emitted",
        *_FAILED_EMISSION_EVIDENCE_KINDS,
        "operator.representation.emission_outcome_recorded",
    ]
    emitted = ledger.get(representation["emitted_event_identity"])
    failure = ledger.get(representation["emission_outcome_event_identity"])
    assert emitted.material["output_boundary"] == "text_stream_write"
    assert failure.material["boundary"] == "text_stream_flush"
    assert failure.material["write_count"] == len(representation["emission_text"])
    assert failure.material["emitted_event_identity"] == emitted.identity
    assert failure.material["error"] == "OSError('flush failed')"


def test_process_death_after_attempt_leaves_output_outcome_unknown():
    class SimulatedProcessDeath(BaseException):
        pass

    class CrashingOutput(StringIO):
        def write(self, value):
            raise SimulatedProcessDeath()

    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
    )

    with pytest.raises(SimulatedProcessDeath):
        emit_operator_representation(
            ledger, representation=representation, output_stream=CrashingOutput()
        )

    assert [event.kind for event in ledger.list()] == [
        *_REPRESENTATION_EDGE_EVIDENCE_KINDS,
        "operator.representation.recorded",
        "operator.representation.emission_attempt_recorded",
        "operator.representation.emission_attempt_locality_evidenced",
    ]
    read = list(_standing(ledger)["representations"].values())[-1]
    assert read["emission_attempt_event_identity"] is not None
    assert read["emission_attempt_locality_evidence_identity"] is not None
    assert read["emission_outcome_event_identity"] is None
    assert read["emitted_event_identity"] is None
