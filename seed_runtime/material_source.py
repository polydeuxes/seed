"""Exact material results across source-specific roads."""

from __future__ import annotations

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary


class MaterialSourceError(ValueError):
    """One exact material result is not intact."""


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
        _recorded_operator_material_source_reading,
    )

    if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND:
        try:
            _recorded_operator_material_source_reading(ledger, event.identity)
        except (TypeError, ValueError) as error:
            raise MaterialSourceError(
                "operator material source occurrence carries no intact physiology"
            ) from error
        return event
    raise MaterialSourceError(
        "exact material result is absent or corrupted"
    )
