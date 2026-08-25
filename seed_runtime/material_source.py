"""Exact yielded material results across source-specific roads."""

from __future__ import annotations

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
)


MATERIAL_RESULT_UNKNOWN = ("source_relation",)


class MaterialSourceError(ValueError):
    """One exact yielded material result is not intact."""


def _append_exact_material_result_occurrence(
    ledger: EventLedger,
    *,
    result_event: Event,
) -> Event:
    """Append family-built material only after its exact prior Act and Yield."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("exact material result requires one EventLedger")
    if type(result_event) is not Event:
        raise MaterialSourceError("exact material result occurrence required")
    act_occurrence_event_identity = result_event.material.get(
        "act_occurrence_event_identity"
    )
    yield_relation_identity = result_event.material.get(
        "yield_relation_identity"
    )
    if (
        type(result_event.exact_material) is not bytes
        or type(result_event.locality_identity) is not str
        or not result_event.locality_identity
        or type(act_occurrence_event_identity) is not str
        or not act_occurrence_event_identity
        or type(yield_relation_identity) is not str
        or not yield_relation_identity
    ):
        raise MaterialSourceError("exact material result occurrence required")
    act_occurrence = ledger.get(act_occurrence_event_identity)
    yield_relation = ledger.get(
        yield_relation_identity
    )
    yield_material = (
        yield_relation.material
        if yield_relation is not None
        else None
    )
    yield_dimensions = (
        yield_material.get("dimensions") if type(yield_material) is dict else None
    )
    result_coordinates = (
        yield_material.get("coordinates_of_recorded_result")
        if type(yield_material) is dict
        else None
    )
    carried_result = {}
    if type(result_coordinates) is dict:
        for coordinate, carried_at in result_coordinates.items():
            value = result_event.material
            if type(carried_at) is not list or not carried_at:
                break
            for part in carried_at:
                if type(value) is not dict or part not in value:
                    break
                value = value[part]
            else:
                carried_result[coordinate] = value
                continue
            break
    if (
        act_occurrence is None
        or yield_relation is None
        or yield_relation.kind
        != RECORDED_YIELD_RELATION_EVENT
        or act_occurrence.locality_identity
        != result_event.locality_identity
        or yield_relation.locality_identity
        != result_event.locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or type(yield_material) is not dict
        or type(yield_dimensions) is not dict
        or yield_material.get("act_occurrence_event_identity")
        != act_occurrence.identity
        or act_occurrence.material.get("act_occurrence_identity")
        != yield_dimensions.get("act_occurrence_identity")
        or yield_relation.exact_material
        != result_event.exact_material
        or carried_result != yield_material.get("result")
    ):
        raise MaterialSourceError(
            "exact material result requires its prior intact Act and Yield"
        )
    try:
        ledger.occurrences_in_append_order(
            (
                act_occurrence.identity,
                yield_relation.identity,
            ),
            locality_identity=result_event.locality_identity,
        )
    except ValueError as error:
        raise MaterialSourceError(
            "exact material result requires its prior intact Act and Yield"
        ) from error
    return ledger.append_many((result_event,))[0]


def exact_material_result_bytes(event: Event) -> bytes:
    """Return bytes already admitted by one source-specific result reader."""

    if type(event) is not Event:
        raise MaterialSourceError(
            "one exact material result occurrence required"
        )
    exact = event.exact_material
    if type(exact) is not bytes:
        raise MaterialSourceError("material result carries no exact bytes")
    return exact


def iter_exact_material_results(
    ledger: EventLedger,
    locality_identity: str,
    *,
    through: EventLedgerBoundary | None = None,
):
    """Yield exact material results without a Locality-wide read."""

    from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND
    from seed_runtime.operator_material_source import (
        OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
    )

    witness = iter(
        ledger.iter_locality_kind_identities(
            locality_identity,
            WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
            through=through,
        )
    )
    operator = iter(
        ledger.iter_locality_kind_identities(
            locality_identity,
            OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
            through=through,
        )
    )
    absent = object()
    witness_identity = next(witness, absent)
    operator_identity = next(operator, absent)
    while witness_identity is not absent or operator_identity is not absent:
        if witness_identity is absent:
            selected = operator_identity
            operator_identity = next(operator, absent)
        elif operator_identity is absent:
            selected = witness_identity
            witness_identity = next(witness, absent)
        else:
            try:
                ledger.occurrences_in_append_order(
                    (witness_identity, operator_identity),
                    locality_identity=locality_identity,
                )
            except ValueError:
                try:
                    ledger.occurrences_in_append_order(
                        (operator_identity, witness_identity),
                        locality_identity=locality_identity,
                    )
                except ValueError as error:
                    raise MaterialSourceError(
                        "exact material results carry no append order"
                    ) from error
                selected = operator_identity
                operator_identity = next(operator, absent)
            else:
                selected = witness_identity
                witness_identity = next(witness, absent)
        yield read_exact_material_result(ledger, selected)


def read_exact_material_result(
    ledger: EventLedger, event_identity: str
) -> Event:
    """Read one material result through its source-specific physiology."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("exact material result read requires one EventLedger")
    if type(event_identity) is not str or not event_identity:
        raise MaterialSourceError(
            "exact material result read requires one occurrence identity"
        )
    event = ledger.get(event_identity)
    if event is None or ledger.integrity_of(event.identity) == CORRUPTED:
        raise MaterialSourceError(
            "exact material result is absent or corrupted"
        )

    from seed_runtime.witness_material_source import (
        WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
        _read_witness_material_source_result,
    )

    if event.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND:
        return _read_witness_material_source_result(ledger, event)

    from seed_runtime.operator_material_source import (
        OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
        get_recorded_operator_material_source,
    )

    if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND:
        try:
            get_recorded_operator_material_source(ledger, event.identity)
        except (TypeError, ValueError) as error:
            raise MaterialSourceError(
                "operator material source occurrence carries no intact physiology"
            ) from error
        return event
    raise MaterialSourceError(
        "exact material result is absent or corrupted"
    )


def read_material_locality_relation_requirements(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
) -> dict[str, bool]:
    """Read one source-specific material-to-this-Seed Locality relation."""

    result = read_exact_material_result(
        ledger, recorded_result_event_identity
    )
    from seed_runtime.witness_material_source import (
        WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
        read_witness_material_source_locality_relation_requirements,
    )

    if result.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND:
        return read_witness_material_source_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=result.identity,
        )

    from seed_runtime.operator_material_source import (
        read_operator_material_source_locality_relation_requirements,
    )

    operator_requirements = (
        read_operator_material_source_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=result.identity,
        )
    )
    return {
        "exact_relation": operator_requirements["exact_relation"],
        "relation_occurrence": operator_requirements["occurrence_witness"],
        "intact_source_occurrence": operator_requirements["intact_occurrence"],
    }
