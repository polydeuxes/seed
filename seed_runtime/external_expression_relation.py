"""Preserve source-carried Assertions relating external expressions to grammar.

This module does not infer a relation from adjacency or repetition. One exact
operator-origin occurrence carries the asserted relation. Seed verifies that
the named coordinates exist in the supplied machine grammar, records the
Assertion with its source occurrence, and can later compare the preserved
coordinates with a current grammar representation.

The result is evidence-relative. It is not a relation beyond its source or
constitutional grammar by identity.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.ids import new_id
from seed_runtime.preserved_material_measurement import (
    INGRESS_OCCURRED_KIND,
    PreservedMaterialMeasurementError,
)
from seed_runtime.yield_evidence import _record_yield_evidence, yield_commitment


EXTERNAL_EXPRESSION_RELATION_RECORDED_KIND = (
    "operator.external_expression.relation_asserted"
)
EXTERNAL_EXPRESSION_RELATION_ACT_EVIDENCE_KIND = (
    "operator.external_expression.relation_act_evidenced"
)
EXTERNAL_EXPRESSION_RELATION_CARRIAGE_EVIDENCE_KIND = (
    "operator.external_expression.relation_carriage_evidenced"
)
EXTERNAL_EXPRESSION_RELATION_CONVENTION = "external_expression_relation_v1"
EXTERNAL_EXPRESSION_RELATION_RESPONSIBILITY = (
    "preserve one source-carried Assertion relating one exact external "
    "expression to exact machine-grammar coordinates"
)
EXTERNAL_EXPRESSION_RELATION_UNKNOWNS = [
    "whether this source-carried relation applies beyond this source and locality remains Unknown"
]


class ExternalExpressionRelationError(ValueError):
    """An exact external-expression relation could not be preserved."""


@dataclass(frozen=True)
class RecordedExternalExpressionRelation:
    event_id: str
    assertion_id: str
    source_occurrence_id: str
    external_expression: str
    grammar_coordinates: tuple[dict[str, object], ...]
    act_occurrence_id: str


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _assertion_identity(
    source_occurrence_id: str,
    expression: str,
    coordinates: list[dict[str, object]],
) -> str:
    return "external-expression-relation:" + yield_commitment(
        EXTERNAL_EXPRESSION_RELATION_CONVENTION,
        {
            "source_occurrence_id": source_occurrence_id,
            "external_expression": expression,
            "grammar_coordinates": coordinates,
        },
    )


def _read_path(grammar: object, path: list[str]) -> tuple[bool, object]:
    value = grammar
    for coordinate in path:
        if not isinstance(value, dict) or coordinate not in value:
            return False, None
        value = value[coordinate]
    return True, value


def _validate_training_material(
    value: object,
    *,
    machine_grammar: dict[str, object] | None,
) -> tuple[str, list[dict[str, object]]]:
    if not isinstance(value, dict):
        raise ExternalExpressionRelationError(
            "external-expression training material must be one exact JSON object"
        )
    expression = value.get("external_expression")
    coordinates = value.get("grammar_coordinates")
    if (
        not isinstance(expression, str)
        or not expression
        or not isinstance(coordinates, list)
        or not coordinates
    ):
        raise ExternalExpressionRelationError(
            "training material requires one expression and grammar coordinates"
        )
    preserved: list[dict[str, object]] = []
    paths: set[tuple[str, ...]] = set()
    for coordinate in coordinates:
        if not isinstance(coordinate, dict) or set(coordinate) != {"path", "value"}:
            raise ExternalExpressionRelationError(
                "each grammar coordinate requires only path and value"
            )
        path = coordinate.get("path")
        if (
            not isinstance(path, list)
            or not path
            or not all(isinstance(part, str) and part for part in path)
        ):
            raise ExternalExpressionRelationError(
                "a grammar coordinate path must contain exact names"
            )
        path_identity = tuple(path)
        if path_identity in paths:
            raise ExternalExpressionRelationError(
                "one grammar coordinate was supplied more than once"
            )
        paths.add(path_identity)
        if machine_grammar is not None:
            present, actual = _read_path(machine_grammar, path)
            if not present or _canonical(actual) != _canonical(coordinate.get("value")):
                raise ExternalExpressionRelationError(
                    "source-carried coordinates differ from the supplied machine grammar"
                )
        preserved.append({"path": list(path), "value": coordinate.get("value")})
    return expression, preserved


def _source_material(event: Event) -> dict[str, object]:
    if (
        event.kind != INGRESS_OCCURRED_KIND
        or event.payload.get("material_origin") != "operator"
    ):
        raise ExternalExpressionRelationError(
            "an external-expression relation requires one operator-origin ingress occurrence"
        )
    text = event.payload.get("decoded_text")
    if not isinstance(text, str):
        raise ExternalExpressionRelationError(
            "the source occurrence carries no exact decoded material"
        )
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ExternalExpressionRelationError(
            "external-expression training material is not exact JSON"
        ) from exc
    if not isinstance(value, dict):
        raise ExternalExpressionRelationError(
            "external-expression training material must be one exact JSON object"
        )
    return value


def record_external_expression_relation(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    source_occurrence_id: str,
    machine_grammar: dict[str, object],
) -> Event:
    """Record one source-carried relation Assertion after exact grammar Compare."""

    source = ledger.get(source_occurrence_id)
    if (
        source is None
        or ledger.integrity_of(source_occurrence_id) == CORRUPTED
        or source.workspace_id != workspace_id
        or source.session_id != session_id
    ):
        raise ExternalExpressionRelationError(
            "the external-expression source occurrence does not reconstruct locally"
        )
    source_material = _source_material(source)
    expression, coordinates = _validate_training_material(
        source_material,
        machine_grammar=machine_grammar,
    )
    act_id = new_id("external_expression_relation_act")
    act_occurrence_id = new_id("external_expression_relation_act_occurrence")
    assertion_id = _assertion_identity(
        source_occurrence_id,
        expression,
        coordinates,
    )
    result = {
        "assertion_id": assertion_id,
        "source_occurrence_id": source_occurrence_id,
        "external_expression": expression,
        "grammar_coordinates": coordinates,
        "standing": "asserted",
        "unknowns": list(EXTERNAL_EXPRESSION_RELATION_UNKNOWNS),
    }
    commitment = yield_commitment(EXTERNAL_EXPRESSION_RELATION_CONVENTION, result)
    act_evidence = ledger.append(
        EXTERNAL_EXPRESSION_RELATION_ACT_EVIDENCE_KIND,
        workspace_id,
        {
            "target_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "responsibility": EXTERNAL_EXPRESSION_RELATION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "input_applicability": [
                {
                    "input_ref": source_occurrence_id,
                    "role": "source-carried relation Assertion",
                    "standing": "applicable",
                }
            ],
            "result_commitment": commitment,
            "standing": "occurred",
        },
        session_id=session_id,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        workspace_id=workspace_id,
        session_id=session_id,
        convention=EXTERNAL_EXPRESSION_RELATION_CONVENTION,
        yielding_act="preserve one external-expression relation Assertion",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind="external-expression relation Assertion",
        result_identity=assertion_id,
        yielded_content=result,
        responsibility=EXTERNAL_EXPRESSION_RELATION_RESPONSIBILITY,
        live_boundary="external_expression_relation",
        responsible_boundary="this Seed",
    )
    carriage_evidence = ledger.append(
        EXTERNAL_EXPRESSION_RELATION_CARRIAGE_EVIDENCE_KIND,
        workspace_id,
        {
            "act_occurrence_id": act_occurrence_id,
            "carried_content": result,
            "standing": "carried",
        },
        session_id=session_id,
    )
    return ledger.append(
        EXTERNAL_EXPRESSION_RELATION_RECORDED_KIND,
        workspace_id,
        {
            **result,
            "target_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "responsibility": EXTERNAL_EXPRESSION_RELATION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "responsible_act_evidence_id": act_evidence.id,
            "yield_evidence_id": yield_evidence.id,
            "carriage_evidence_id": carriage_evidence.id,
            "authority": (
                "preserves this source-carried relation Assertion only; does not "
                "make it grammar beyond this source or establish another source's use"
            ),
        },
        session_id=session_id,
    )


def get_recorded_external_expression_relation(
    ledger: EventLedger,
    event_id: str,
) -> RecordedExternalExpressionRelation | None:
    """Recover one exact relation Assertion without consulting Rosetta."""

    carrier = ledger.get(event_id)
    if carrier is None:
        return None
    if (
        carrier.kind != EXTERNAL_EXPRESSION_RELATION_RECORDED_KIND
        or ledger.integrity_of(event_id) == CORRUPTED
    ):
        raise ExternalExpressionRelationError(
            "the external-expression relation carrier is absent or corrupted"
        )
    source_id = carrier.payload.get("source_occurrence_id")
    source = ledger.get(source_id) if isinstance(source_id, str) else None
    if (
        source is None
        or ledger.integrity_of(source_id) == CORRUPTED
        or source.workspace_id != carrier.workspace_id
        or source.session_id != carrier.session_id
    ):
        raise ExternalExpressionRelationError(
            "the external-expression source occurrence does not reconstruct"
        )
    source_material = _source_material(source)
    expression, coordinates = _validate_training_material(
        source_material,
        machine_grammar=None,
    )
    result = {
        "assertion_id": _assertion_identity(source_id, expression, coordinates),
        "source_occurrence_id": source_id,
        "external_expression": expression,
        "grammar_coordinates": coordinates,
        "standing": "asserted",
        "unknowns": list(EXTERNAL_EXPRESSION_RELATION_UNKNOWNS),
    }
    if any(
        carrier.payload.get(key) != value
        for key, value in result.items()
    ):
        raise ExternalExpressionRelationError(
            "the carried relation differs from its exact source occurrence"
        )
    evidence_ids = (
        carrier.payload.get("responsible_act_evidence_id"),
        carrier.payload.get("yield_evidence_id"),
        carrier.payload.get("carriage_evidence_id"),
    )
    if not all(isinstance(value, str) and value for value in evidence_ids):
        raise ExternalExpressionRelationError(
            "the carried relation names incomplete edge Evidence"
        )
    act_evidence, yield_evidence, carriage_evidence = (
        ledger.get(value) for value in evidence_ids
    )
    act_occurrence_id = carrier.payload.get("act_occurrence_id")
    commitment = yield_commitment(EXTERNAL_EXPRESSION_RELATION_CONVENTION, result)
    if (
        act_evidence is None
        or act_evidence.kind != EXTERNAL_EXPRESSION_RELATION_ACT_EVIDENCE_KIND
        or ledger.integrity_of(act_evidence.id) == CORRUPTED
        or yield_evidence is None
        or yield_evidence.kind != "operator.yield.evidence_recorded"
        or ledger.integrity_of(yield_evidence.id) == CORRUPTED
        or carriage_evidence is None
        or carriage_evidence.kind
        != EXTERNAL_EXPRESSION_RELATION_CARRIAGE_EVIDENCE_KIND
        or ledger.integrity_of(carriage_evidence.id) == CORRUPTED
        or act_evidence.payload.get("target_act_id")
        != carrier.payload.get("target_act_id")
        or act_evidence.payload.get("act_occurrence_id") != act_occurrence_id
        or act_evidence.payload.get("responsibility")
        != EXTERNAL_EXPRESSION_RELATION_RESPONSIBILITY
        or act_evidence.payload.get("responsible_boundary") != "this Seed"
        or yield_evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != act_occurrence_id
        or carriage_evidence.payload.get("act_occurrence_id") != act_occurrence_id
        or carriage_evidence.payload.get("standing") != "carried"
        or act_evidence.payload.get("result_commitment") != commitment
        or yield_evidence.payload.get("yield_commitment") != commitment
        or yield_evidence.payload.get("yield_convention")
        != EXTERNAL_EXPRESSION_RELATION_CONVENTION
        or carriage_evidence.payload.get("carried_content") != result
        or act_evidence.payload.get("input_applicability")
        != [
            {
                "input_ref": source_id,
                "role": "source-carried relation Assertion",
                "standing": "applicable",
            }
        ]
    ):
        raise ExternalExpressionRelationError(
            "the external-expression relation edge Evidence does not reconstruct"
        )
    return RecordedExternalExpressionRelation(
        event_id=event_id,
        assertion_id=result["assertion_id"],
        source_occurrence_id=source_id,
        external_expression=expression,
        grammar_coordinates=tuple(coordinates),
        act_occurrence_id=act_occurrence_id,
    )


def reconstruct_external_expression_relations(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    external_expression: str,
    machine_grammar: dict[str, object],
) -> dict[str, object]:
    """Return every exact source-carried relation and its current grammar match."""

    assertions = []
    for event in ledger.iter_session_kind(
        workspace_id,
        session_id,
        EXTERNAL_EXPRESSION_RELATION_RECORDED_KIND,
    ):
        recorded = get_recorded_external_expression_relation(ledger, event.id)
        if recorded is None or recorded.external_expression != external_expression:
            continue
        compared = []
        for coordinate in recorded.grammar_coordinates:
            present, current = _read_path(machine_grammar, coordinate["path"])
            compared.append(
                {
                    **coordinate,
                    "current_grammar": (
                        "exact"
                        if present
                        and _canonical(current) == _canonical(coordinate["value"])
                        else "different"
                        if present
                        else "absent"
                    ),
                }
            )
        assertions.append(
            {
                "assertion_id": recorded.assertion_id,
                "source_occurrence_id": recorded.source_occurrence_id,
                "relation_occurrence_id": recorded.event_id,
                "grammar_coordinates": compared,
                "standing": "asserted",
            }
        )
    return {
        "external_expression": external_expression,
        "standing": "Unknown" if not assertions else "asserted",
        "assertions": assertions,
        "distinct_coordinate_sets": len(
            {
                _canonical(assertion["grammar_coordinates"])
                for assertion in assertions
            }
        ),
    }
