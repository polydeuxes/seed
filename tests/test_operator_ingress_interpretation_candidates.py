from dataclasses import fields, replace
from io import BytesIO, StringIO
import json

import pytest

from seed_runtime.contextual_interpretation_warrant_set import InterpretationCandidate
from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress_addressable_material import (
    OperatorIngressAddressableMaterial,
)
from seed_runtime.operator_ingress_common_grammar_prerequisite import (
    run_operator_ingress_common_grammar_probe_attempt,
)
from seed_runtime.operator_ingress_interpretation_candidates import (
    BOUNDARY_NOTES,
    FORMATION_UNKNOWN,
    NO_CANDIDATES_UNKNOWN,
    PROPOSITION_UNKNOWN,
    REQUIRED_AUTHORITY_LIMITS,
    SOURCE_RELATION_UNKNOWN,
    AttributedInterpretationCandidateTestimony,
    OperatorIngressInterpretationCandidateSet,
    OperatorIngressInterpretationCandidateSetError,
    SuppliedInterpretationCandidateTestimony,
    preserve_operator_ingress_interpretation_candidates,
)
from seed_runtime.operator_ingress_representation import capture_stdin_material


class ForeignString(str):
    pass


@pytest.fixture
def material():
    ledger = EventLedger()
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(BytesIO(b" exact::text\r\n")),
        response_input_stream=BytesIO(),
        output_stream=StringIO(),
    )
    return ledger, OperatorIngressAddressableMaterial.from_json_dict(
        view["addressable_operator_material"]
    )


def supplied(
    material,
    *,
    ref="candidate:one",
    formation="event:formation",
    refs=None,
    meaning="meaning",
    unknowns=("supplier unknown",),
    authority_limits=("testimony only",),
):
    if refs is None:
        refs = (material.exact_operator_material.source_spans[0].span_ref,)
    return SuppliedInterpretationCandidateTestimony(
        candidate=InterpretationCandidate(ref, "label", refs, meaning),
        attributed_supplier="external supplier",
        supplier_provenance=("submission:1",),
        formation_occurrence_ref=formation,
        declared_scope=("this material",),
        known_loss=("context unavailable",),
        supplied_unknowns=unknowns,
        conflicts=("supplied conflict",),
        supplied_authority_limits=authority_limits,
    )


def preserve(material, *items, **kwargs):
    return preserve_operator_ingress_interpretation_candidates(
        addressable_material=material, candidate_testimonies=items, **kwargs
    )


def test_supplier_and_preserved_types_have_distinct_unknown_ownership(material):
    ledger, addressable = material
    item = supplied(
        addressable, formation=None, unknowns=(FORMATION_UNKNOWN, FORMATION_UNKNOWN)
    )
    before = item
    count = len(ledger.list_events("w"))
    result = preserve(
        addressable,
        item,
        supplied_set_unknowns=(NO_CANDIDATES_UNKNOWN, NO_CANDIDATES_UNKNOWN),
    )
    attributed = result.candidate_testimonies[0]
    assert item == before and attributed is not item
    assert "preservation_unknowns" not in {field.name for field in fields(item)}
    assert attributed.supplied_unknowns == (FORMATION_UNKNOWN, FORMATION_UNKNOWN)
    assert attributed.preservation_unknowns == (FORMATION_UNKNOWN,)
    assert result.supplied_set_unknowns == (
        NO_CANDIDATES_UNKNOWN,
        NO_CANDIDATES_UNKNOWN,
    )
    assert result.preservation_set_unknowns == ()
    assert (
        addressable.unknowns
        and attributed.supplied_unknowns
        and result.supplied_set_unknowns
    )
    assert len(ledger.list_events("w")) == count


@pytest.mark.parametrize(
    ("formation", "refs", "meaning", "expected"),
    [
        (None, ("full",), "meaning", (FORMATION_UNKNOWN,)),
        ("event:f", (), "meaning", (SOURCE_RELATION_UNKNOWN,)),
        ("event:f", ("full",), "", (PROPOSITION_UNKNOWN,)),
        (
            None,
            (),
            "",
            (FORMATION_UNKNOWN, SOURCE_RELATION_UNKNOWN, PROPOSITION_UNKNOWN),
        ),
        ("event:f", ("full",), "meaning", ()),
    ],
)
def test_preservation_unknowns_are_derived_in_fixed_order(
    material, formation, refs, meaning, expected
):
    _, addressable = material
    full = addressable.exact_operator_material.source_spans[0].span_ref
    actual_refs = tuple(full if ref == "full" else ref for ref in refs)
    result = preserve(
        addressable,
        supplied(addressable, formation=formation, refs=actual_refs, meaning=meaning),
    )
    assert result.candidate_testimonies[0].preservation_unknowns == expected


@pytest.mark.parametrize(
    "bad",
    [
        (),
        (FORMATION_UNKNOWN,),
        (SOURCE_RELATION_UNKNOWN,),
        (PROPOSITION_UNKNOWN,),
        (PROPOSITION_UNKNOWN, FORMATION_UNKNOWN),
        ("extra",),
    ],
)
def test_attributed_testimony_refuses_wrong_preservation_findings(material, bad):
    _, addressable = material
    item = supplied(addressable, formation=None, refs=(), meaning="")
    with pytest.raises(
        OperatorIngressInterpretationCandidateSetError, match="preservation_unknowns"
    ):
        AttributedInterpretationCandidateTestimony(
            **{field.name: getattr(item, field.name) for field in fields(item)},
            preservation_unknowns=bad,
        )


@pytest.mark.parametrize(
    "field",
    [
        "supplier_provenance",
        "declared_scope",
        "known_loss",
        "supplied_unknowns",
        "conflicts",
        "supplied_authority_limits",
    ],
)
@pytest.mark.parametrize("bad", ["string", ["list"], ("valid", 1)])
def test_supplier_direct_tuple_shape_is_intrinsic(material, field, bad):
    _, addressable = material
    with pytest.raises(OperatorIngressInterpretationCandidateSetError):
        replace(supplied(addressable), **{field: bad})


@pytest.mark.parametrize(
    ("owner", "field"),
    [
        ("candidate", "candidate_ref"),
        ("candidate", "proposed_meaning"),
        ("testimony", "attributed_supplier"),
        ("testimony", "formation_occurrence_ref"),
    ],
)
def test_supplier_direct_scalar_coordinates_require_exact_strings(
    material, owner, field
):
    _, addressable = material
    item = supplied(addressable)
    if owner == "candidate":
        candidate = replace(item.candidate, **{field: ForeignString("x")})
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            replace(item, candidate=candidate)
    else:
        changes = {field: ForeignString(getattr(item, field))}
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            replace(item, **changes)


@pytest.mark.parametrize(
    ("owner", "field"),
    [
        ("candidate", "source_span_refs"),
        ("supplier", "supplier_provenance"),
        ("supplier", "declared_scope"),
        ("supplier", "supplied_authority_limits"),
    ],
)
def test_supplier_direct_tuple_members_require_exact_strings(material, owner, field):
    _, addressable = material
    item = supplied(addressable)
    if owner == "candidate":
        candidate = replace(
            item.candidate,
            source_span_refs=(ForeignString(item.candidate.source_span_refs[0]),),
        )
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            replace(item, candidate=candidate)
    else:
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            replace(item, **{field: (ForeignString("x"),)})


def test_zero_one_many_candidates_and_set_unknown_ownership(material):
    _, addressable = material
    zero = preserve(addressable, supplied_set_unknowns=(NO_CANDIDATES_UNKNOWN,))
    assert zero.candidate_testimonies == ()
    assert zero.supplied_set_unknowns == (NO_CANDIDATES_UNKNOWN,)
    assert zero.preservation_set_unknowns == (NO_CANDIDATES_UNKNOWN,)
    one = preserve(addressable, supplied(addressable))
    many = preserve(
        addressable, supplied(addressable, ref="a"), supplied(addressable, ref="b")
    )
    assert one.preservation_set_unknowns == () and len(many.candidate_testimonies) == 2


def test_candidate_set_direct_construction_refuses_pending_forgery_and_stale_findings(
    material,
):
    _, addressable = material
    valid = preserve(addressable, supplied(addressable))
    for change in (
        {"candidate_set_id": "pending"},
        {"candidate_set_id": "forged"},
        {"preservation_set_unknowns": (NO_CANDIDATES_UNKNOWN,)},
        {"boundary_notes": ()},
        {"preservation_authority_limits": ()},
        {"read_only": False},
    ):
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            replace(valid, **change)


def test_candidate_uniqueness_and_source_relation_are_enforced(material):
    _, addressable = material
    with pytest.raises(OperatorIngressInterpretationCandidateSetError, match="unique"):
        preserve(addressable, supplied(addressable), supplied(addressable))
    with pytest.raises(OperatorIngressInterpretationCandidateSetError, match="foreign"):
        preserve(addressable, supplied(addressable, refs=("foreign",)))


def test_round_trip_and_forged_json_use_same_invariant_boundary(material):
    _, addressable = material
    result = preserve(addressable, supplied(addressable, formation=None))
    encoded = result.to_json_dict()
    assert OperatorIngressInterpretationCandidateSet.from_json_dict(encoded) == result
    encoded["candidate_set_id"] = "pending"
    with pytest.raises(OperatorIngressInterpretationCandidateSetError, match="forged"):
        OperatorIngressInterpretationCandidateSet.from_json_dict(encoded)


def test_addressable_material_and_candidate_set_round_trip_over_json_wire(material):
    _, addressable = material
    result = preserve(
        addressable,
        supplied(addressable, formation=None),
        supplied_set_unknowns=("set unknown",),
        set_conflicts=("set conflict",),
    )

    for artifact, artifact_type in (
        (addressable, OperatorIngressAddressableMaterial),
        (result, OperatorIngressInterpretationCandidateSet),
    ):
        mapping = artifact.to_json_dict()
        if artifact is addressable:
            assert type(mapping["provenance"]) is tuple
        else:
            assert type(mapping["candidate_testimonies"]) is tuple
            assert (
                type(
                    mapping["candidate_testimonies"][0]["candidate"]["source_span_refs"]
                )
                is tuple
            )
        encoded = json.dumps(mapping)
        decoded = json.loads(encoded)
        if artifact is addressable:
            assert type(decoded["provenance"]) is list
        else:
            assert type(decoded["candidate_testimonies"]) is list
            assert (
                type(
                    decoded["candidate_testimonies"][0]["candidate"]["source_span_refs"]
                )
                is list
            )
        rebuilt = artifact_type.from_json_dict(decoded)
        assert rebuilt == artifact
        rebuilt_tuple = (
            rebuilt.provenance
            if artifact is addressable
            else rebuilt.candidate_testimonies
        )
        assert type(rebuilt_tuple) is tuple


@pytest.mark.parametrize(
    "field",
    [
        "preservation_unknowns",
        "supplied_set_unknowns",
        "set_conflicts",
        "boundary_notes",
        "preservation_authority_limits",
    ],
)
def test_preservation_and_set_tuple_members_require_exact_strings(material, field):
    _, addressable = material
    valid = preserve(addressable, supplied(addressable, formation=None))
    if field == "preservation_unknowns":
        testimony = valid.candidate_testimonies[0]
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            replace(
                testimony, preservation_unknowns=(ForeignString(FORMATION_UNKNOWN),)
            )
    else:
        current = getattr(valid, field)
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            replace(
                valid,
                **{field: (ForeignString(current[0] if current else "x"),)},
            )


@pytest.mark.parametrize("field", ["candidate_set_id", "artifact_type", "convention"])
def test_candidate_set_scalar_identity_coordinates_require_exact_strings(
    material, field
):
    _, addressable = material
    valid = preserve(addressable, supplied(addressable))
    with pytest.raises(OperatorIngressInterpretationCandidateSetError):
        replace(valid, **{field: ForeignString(getattr(valid, field))})


def test_exact_builtin_strings_remain_accepted_at_all_ownership_layers(material):
    _, addressable = material
    item = supplied(addressable)
    result = preserve(
        addressable,
        item,
        supplied_set_unknowns=("set unknown",),
        set_conflicts=("set conflict",),
    )
    assert type(result.candidate_set_id) is str
    assert all(
        type(value) is str
        for value in (
            item.candidate.candidate_ref,
            item.attributed_supplier,
            item.supplier_provenance[0],
            result.boundary_notes[0],
        )
    )


def test_identity_covers_each_unknown_owner_and_is_deterministic(material):
    _, addressable = material
    item = supplied(addressable)
    first = preserve(addressable, item)
    assert preserve(addressable, item).candidate_set_id == first.candidate_set_id
    assert (
        preserve(
            addressable, replace(item, supplied_unknowns=("changed",))
        ).candidate_set_id
        != first.candidate_set_id
    )
    assert (
        preserve(addressable, item, supplied_set_unknowns=("changed",)).candidate_set_id
        != first.candidate_set_id
    )
    missing = supplied(addressable, formation=None)
    assert preserve(addressable, missing).candidate_set_id != first.candidate_set_id


def test_producer_accepts_only_supplier_input_and_exact_tuples(material):
    _, addressable = material
    attributed = preserve(addressable, supplied(addressable)).candidate_testimonies[0]
    with pytest.raises(
        OperatorIngressInterpretationCandidateSetError, match="supplied"
    ):
        preserve(addressable, attributed)
    with pytest.raises(
        OperatorIngressInterpretationCandidateSetError, match="exact tuple"
    ):
        preserve_operator_ingress_interpretation_candidates(
            addressable_material=addressable, candidate_testimonies=[]
        )
    with pytest.raises(TypeError):
        preserve(addressable, set_unknowns=())


def test_authority_owners_remain_separate_and_repository_declarations_fixed(material):
    _, addressable = material
    shared_authority_text = addressable.authority_limits[0]
    supplier_limits = (shared_authority_text, shared_authority_text)
    result = preserve(
        addressable,
        supplied(addressable, authority_limits=supplier_limits),
    )
    testimony = result.candidate_testimonies[0]
    assert shared_authority_text in addressable.authority_limits
    assert testimony.supplied_authority_limits == supplier_limits
    assert testimony.supplied_authority_limits.count(shared_authority_text) == 2
    assert result.preservation_authority_limits == REQUIRED_AUTHORITY_LIMITS
    assert set(REQUIRED_AUTHORITY_LIMITS).isdisjoint(
        testimony.supplied_authority_limits
    )
    assert BOUNDARY_NOTES == result.boundary_notes


def test_no_warrant_producer_is_called(material, monkeypatch):
    import seed_runtime.contextual_interpretation_warrant_set as warrants

    monkeypatch.setattr(
        warrants,
        "produce_contextual_interpretation_warrant_set",
        lambda **kwargs: pytest.fail("must remain disconnected"),
    )
    _, addressable = material
    assert preserve(addressable, supplied(addressable)).candidate_testimonies
