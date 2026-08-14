import json
from pathlib import Path

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.external_expression_relation import (
    EXTERNAL_EXPRESSION_RELATION_RECORDED_KIND,
    ExternalExpressionRelationError,
    get_recorded_external_expression_relation,
    record_external_expression_relation,
    reconstruct_external_expression_relations,
)
from seed_runtime.preserved_material_measurement import INGRESS_OCCURRED_KIND


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = json.loads(
    (ROOT / "book_of_seed/grammar.json").read_text(encoding="utf-8")
)


def _source(
    ledger: EventLedger,
    expression: str,
    path: list[str],
    value: object,
):
    return ledger.append(
        INGRESS_OCCURRED_KIND,
        "w",
        {
            "material_origin": "operator",
            "decoded_text": json.dumps(
                {
                    "external_expression": expression,
                    "grammar_coordinates": [{"path": path, "value": value}],
                },
                sort_keys=True,
            )
        },
        actor="operator",
        locality_id="s",
    )


def test_source_carried_expression_relation_is_recorded_and_reconstructed():
    ledger = EventLedger()
    coordinate = GRAMMAR["structural_edges"]["yield"]
    source = _source(
        ledger,
        "Producer",
        ["structural_edges", "yield"],
        coordinate,
    )

    event = record_external_expression_relation(
        ledger,
        workspace_id="w",
        locality_id="s",
        source_occurrence_id=source.id,
        machine_grammar=GRAMMAR,
    )
    recorded = get_recorded_external_expression_relation(ledger, event.id)
    result = reconstruct_external_expression_relations(
        ledger,
        workspace_id="w",
        locality_id="s",
        external_expression="Producer",
        machine_grammar=GRAMMAR,
    )

    assert event.kind == EXTERNAL_EXPRESSION_RELATION_RECORDED_KIND
    assert recorded.source_occurrence_id == source.id
    assert recorded.external_expression == "Producer"
    assert result == {
        "external_expression": "Producer",
        "standing": "asserted",
        "assertions": [
            {
                "assertion_id": recorded.assertion_id,
                "source_occurrence_id": source.id,
                "relation_occurrence_id": event.id,
                "grammar_coordinates": [
                    {
                        "path": ["structural_edges", "yield"],
                        "value": coordinate,
                        "current_grammar": "exact",
                    }
                ],
                "standing": "asserted",
            }
        ],
        "distinct_coordinate_sets": 1,
    }


def test_absent_expression_relation_preserves_unknown():
    result = reconstruct_external_expression_relations(
        EventLedger(),
        workspace_id="w",
        locality_id="s",
        external_expression="Producer",
        machine_grammar=GRAMMAR,
    )

    assert result == {
        "external_expression": "Producer",
        "standing": "Unknown",
        "assertions": [],
        "distinct_coordinate_sets": 0,
    }


def test_equal_expression_does_not_collapse_different_source_relations():
    ledger = EventLedger()
    for name in ("yield", "locality"):
        source = _source(
            ledger,
            "Producer",
            ["structural_edges", name],
            GRAMMAR["structural_edges"][name],
        )
        record_external_expression_relation(
            ledger,
            workspace_id="w",
            locality_id="s",
            source_occurrence_id=source.id,
            machine_grammar=GRAMMAR,
        )

    result = reconstruct_external_expression_relations(
        ledger,
        workspace_id="w",
        locality_id="s",
        external_expression="Producer",
        machine_grammar=GRAMMAR,
    )

    assert len(result["assertions"]) == 2
    assert result["distinct_coordinate_sets"] == 2
    assert len(
        {item["source_occurrence_id"] for item in result["assertions"]}
    ) == 2


def test_current_grammar_difference_does_not_rewrite_preserved_assertion():
    ledger = EventLedger()
    source = _source(
        ledger,
        "Producer",
        ["structural_edges", "yield"],
        GRAMMAR["structural_edges"]["yield"],
    )
    event = record_external_expression_relation(
        ledger,
        workspace_id="w",
        locality_id="s",
        source_occurrence_id=source.id,
        machine_grammar=GRAMMAR,
    )
    changed = json.loads(json.dumps(GRAMMAR))
    changed["structural_edges"]["yield"]["to"] = "another_result"

    result = reconstruct_external_expression_relations(
        ledger,
        workspace_id="w",
        locality_id="s",
        external_expression="Producer",
        machine_grammar=changed,
    )

    assert result["assertions"][0]["relation_occurrence_id"] == event.id
    assert result["assertions"][0]["grammar_coordinates"][0][
        "current_grammar"
    ] == "different"


def test_training_material_must_match_the_supplied_machine_grammar():
    ledger = EventLedger()
    source = _source(
        ledger,
        "Producer",
        ["structural_edges", "yield"],
        {"from": "different", "to": "result"},
    )

    with pytest.raises(
        ExternalExpressionRelationError,
        match="differ from the supplied machine grammar",
    ):
        record_external_expression_relation(
            ledger,
            workspace_id="w",
            locality_id="s",
            source_occurrence_id=source.id,
            machine_grammar=GRAMMAR,
        )


def test_same_shaped_non_operator_material_cannot_train_a_relation():
    ledger = EventLedger()
    source = ledger.append(
        INGRESS_OCCURRED_KIND,
        "w",
        {
            "material_origin": "system",
            "decoded_text": json.dumps(
                {
                    "external_expression": "Producer",
                    "grammar_coordinates": [
                        {
                            "path": ["structural_edges", "yield"],
                            "value": GRAMMAR["structural_edges"]["yield"],
                        }
                    ],
                }
            ),
        },
        locality_id="s",
    )

    with pytest.raises(
        ExternalExpressionRelationError,
        match="operator-origin ingress occurrence",
    ):
        record_external_expression_relation(
            ledger,
            workspace_id="w",
            locality_id="s",
            source_occurrence_id=source.id,
            machine_grammar=GRAMMAR,
        )


def test_recovery_refuses_a_carrier_rewritten_away_from_its_source():
    ledger = EventLedger()
    source = _source(
        ledger,
        "Producer",
        ["structural_edges", "yield"],
        GRAMMAR["structural_edges"]["yield"],
    )
    event = record_external_expression_relation(
        ledger,
        workspace_id="w",
        locality_id="s",
        source_occurrence_id=source.id,
        machine_grammar=GRAMMAR,
    )
    changed = json.loads(json.dumps(event.payload))
    changed["external_expression"] = "different-expression"
    counterfeit = ledger.append(
        EXTERNAL_EXPRESSION_RELATION_RECORDED_KIND,
        "w",
        changed,
        locality_id="s",
    )

    with pytest.raises(
        ExternalExpressionRelationError,
        match="differs from its exact source occurrence",
    ):
        get_recorded_external_expression_relation(ledger, counterfeit.id)
