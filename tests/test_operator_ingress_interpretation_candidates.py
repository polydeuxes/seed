from dataclasses import fields, replace
from io import BytesIO, StringIO
import json

import pytest

from seed_runtime.contextual_interpretation_warrant_set import InterpretationCandidate
from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress_addressable_material import (
    OperatorIngressAddressableMaterial,
)
from seed_runtime.operator_ingress import (
    run_operator_ingress_attempt,
)
from seed_runtime.operator_ingress_interpretation_candidates import (
    BOUNDARY_NOTES,
    FORMATION_OCCURRENCE_REF_ABSENT,
    NO_CANDIDATES_UNKNOWN,
    PROPOSED_MEANING_ABSENT,
    REQUIRED_AUTHORITY_LIMITS,
    SOURCE_SPAN_REFS_ABSENT,
    AttributedInterpretationCandidateTestimony,
    OperatorIngressInterpretationCandidateSet,
    OperatorIngressInterpretationCandidateSetError,
    SuppliedInterpretationCandidateTestimony,
    candidate_set_id_from_fields,
    preserve_operator_ingress_interpretation_candidates,
)
from seed_runtime.operator_ingress_representation import capture_stdin_material


class ForeignString(str):
    pass


@pytest.fixture
def material():
    ledger = EventLedger()
    view = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(BytesIO(b" exact::text\r\n")),
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
        addressable,
        formation=None,
        unknowns=(FORMATION_OCCURRENCE_REF_ABSENT, FORMATION_OCCURRENCE_REF_ABSENT),
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
    assert attributed.supplied_unknowns == (
        FORMATION_OCCURRENCE_REF_ABSENT,
        FORMATION_OCCURRENCE_REF_ABSENT,
    )
    assert attributed.preservation_unknowns == (FORMATION_OCCURRENCE_REF_ABSENT,)
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
        (None, ("full",), "meaning", (FORMATION_OCCURRENCE_REF_ABSENT,)),
        ("event:f", (), "meaning", (SOURCE_SPAN_REFS_ABSENT,)),
        ("event:f", ("full",), "", (PROPOSED_MEANING_ABSENT,)),
        (
            None,
            (),
            "",
            (
                FORMATION_OCCURRENCE_REF_ABSENT,
                SOURCE_SPAN_REFS_ABSENT,
                PROPOSED_MEANING_ABSENT,
            ),
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
        (FORMATION_OCCURRENCE_REF_ABSENT,),
        (SOURCE_SPAN_REFS_ABSENT,),
        (PROPOSED_MEANING_ABSENT,),
        (PROPOSED_MEANING_ABSENT, FORMATION_OCCURRENCE_REF_ABSENT),
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


@pytest.mark.parametrize(
    "attributed_supplier",
    (
        "Seed candidate producer",
        "operator testimony",
        "external grammar source",
        "Unknown producer testimony",
    ),
)
def test_candidate_producer_topology_remains_attributed_and_open(
    material, attributed_supplier
):
    _, addressable = material
    item = replace(supplied(addressable), attributed_supplier=attributed_supplier)
    result = preserve(addressable, item)

    assert result.candidate_testimonies[0].attributed_supplier == attributed_supplier
    declarations = " ".join(result.boundary_notes).lower()
    assert "production remains attributed" in declarations
    assert "external or caller-supplied" not in declarations
    assert "not seed-generated" not in declarations
    assert "relocate candidate production" in declarations
    assert "manufacture missing producer or formation standing" in declarations


@pytest.mark.parametrize("count", (0, 1, 3))
def test_set_authority_preserves_without_claiming_candidate_production(material, count):
    _, addressable = material
    items = tuple(
        supplied(addressable, ref=f"candidate:{index}") for index in range(count)
    )
    result = preserve(addressable, *items)
    authority = " ".join(result.preservation_authority_limits).lower()

    assert "preserves supplied interpretation-candidate testimony only" in authority
    assert "does not itself propose or generate an interpretation" in authority
    assert "proposes one possible interpretation" not in authority
    assert "repository generated candidate meaning" not in authority


def test_derived_findings_are_exact_field_local_absences(material):
    _, addressable = material
    result = preserve(
        addressable, supplied(addressable, formation=None, refs=(), meaning="")
    )
    findings = result.candidate_testimonies[0].preservation_unknowns

    assert findings == (
        FORMATION_OCCURRENCE_REF_ABSENT,
        SOURCE_SPAN_REFS_ABSENT,
        PROPOSED_MEANING_ABSENT,
    )
    joined = " ".join(findings)
    assert "candidate formation occurrence Unknown" not in joined
    assert "candidate source-material relation unavailable" not in joined
    assert "candidate proposition unavailable" not in joined


def test_preservation_copies_supplier_owned_testimony_without_normalization(material):
    _, addressable = material
    repeated = ("duplicate", "duplicate", "final")
    item = replace(
        supplied(addressable),
        supplier_provenance=repeated,
        known_loss=repeated,
        supplied_unknowns=repeated,
        conflicts=repeated,
        supplied_authority_limits=repeated,
    )
    testimony = preserve(addressable, item).candidate_testimonies[0]

    for field in (
        "supplier_provenance",
        "known_loss",
        "supplied_unknowns",
        "conflicts",
        "supplied_authority_limits",
    ):
        assert getattr(testimony, field) == repeated


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


def test_direct_and_json_construction_refuse_stale_repository_wording(material):
    _, addressable = material
    result = preserve(addressable, supplied(addressable, formation=None))
    stale_boundary = (
        "Candidate testimony is attributed external or caller-supplied grammar, not Seed-generated meaning.",
        *result.boundary_notes[1:],
    )
    stale_authority = (
        "proposes one possible interpretation only",
        *result.preservation_authority_limits[1:],
    )

    for field, stale in (
        ("boundary_notes", stale_boundary),
        ("preservation_authority_limits", stale_authority),
    ):
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            replace(result, **{field: stale})
        encoded = json.loads(json.dumps(result.to_json_dict()))
        encoded[field] = list(stale)
        with pytest.raises(OperatorIngressInterpretationCandidateSetError):
            OperatorIngressInterpretationCandidateSet.from_json_dict(encoded)


def test_identity_changes_with_repository_owned_declarations(material):
    _, addressable = material
    result = preserve(addressable, supplied(addressable))
    fields_for_identity = {
        "addressable_material": result.addressable_material,
        "candidate_testimonies": result.candidate_testimonies,
        "supplied_set_unknowns": result.supplied_set_unknowns,
        "preservation_set_unknowns": result.preservation_set_unknowns,
        "set_conflicts": result.set_conflicts,
        "boundary_notes": result.boundary_notes,
        "preservation_authority_limits": result.preservation_authority_limits,
        "convention": result.convention,
    }
    assert (
        candidate_set_id_from_fields(**fields_for_identity) == result.candidate_set_id
    )
    changed = {**fields_for_identity, "boundary_notes": ("changed",)}
    assert candidate_set_id_from_fields(**changed) != result.candidate_set_id


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
                testimony,
                preservation_unknowns=(ForeignString(FORMATION_OCCURRENCE_REF_ABSENT),),
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
