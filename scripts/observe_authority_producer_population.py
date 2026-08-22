"""Change each Authority producer in turn and observe what follows.

One producer has been changed at its source and only recorded material followed.
Whether that holds of the others is not settled by their sharing a key name, so
each is changed separately and the same lawful sequence is recorded twice.

Producers are kept apart and never joined under the word they are keyed by.
Each is disposed only by what its change reached:

    changed an outcome      an operative distinction was observed
    changed material only   nothing this sequence reaches read it
    never called            this sequence does not reach it
    takes an input          not context free, and read separately

A producer this sequence never calls is disposed as unreached rather than as
passive, because nothing here asked it anything.

Disposition after five roads, recorded here with the evidence rather than
apart from it:

    the context-free producers tested
        No independent responsibility was recovered for what they emit.  On
        every road reaching one, changing the value changed the material
        recorded and changed nothing the road produced.  Together with their
        taking no occurrence-specific input, and with the boundedness that does
        move with an occurrence being carried by Scope, what they emit is
        described as a written label rather than as a recovered Authority.

    the context-free producers no road here reaches
        Unknown, each on its own.  They resemble the tested ones in shape, and
        resemblance has been wrong often enough on this branch that it decides
        nothing.  The resemblance is a reason to look, never a disposition.

    the producers taking an input
        A separate physiology, untouched.  Perturbing them at their source
        would answer a question nobody asked; they have to be varied at the
        input that produces the value.

None of this says Authority is absent from the Book's grammar, that these
labels are Locality, or that recording them is wrong.  It says that on these
roads nothing established what they emit as Authority, and nothing read it.

Usage:
    .venv/bin/python scripts/observe_authority_producer_population.py
"""

from __future__ import annotations

import argparse
import importlib
import inspect
from pathlib import Path
import re
import sys
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger

PRODUCERS = [
    ("addressed_byte_occurrence_reference_determination", "_authority"),
    ("byte_measurement", "_source_assertion_authority"),
    ("candidate_results_from_exact_result_assertions", "_authority"),
    ("candidate_results_from_exact_result_assertions", "_applicability_authority"),
    ("comparison_of_ordered_path_source_position_material", "_authority"),
    ("comparison_of_ordered_relation_path_with_recorded_pair_findings", "_authority"),
    ("comparison_of_recorded_byte_pair_measurements", "_authority"),
    ("measurement_of_shared_position_of_byte_pair_occurrences", "_authority"),
    ("operator_checkpoint", "_authority"),
    ("operator_material_acquisition", "_authority"),
    ("operator_representation_admission", "_authority"),
    ("standing_boundary_locality", "_authority"),
]


def _by_position(value: Any, positions: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {
            _by_position(k, positions): _by_position(v, positions)
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_by_position(v, positions) for v in value]
    if isinstance(value, str):
        return re.sub(r"_\d{6}\b", "_#", positions.get(value, value))
    return value


def _acquisition_sequence() -> dict[str, Any]:
    from tests.operator_material_acquisition_test_witness import (
        record_operator_material_occurrence,
    )

    ledger = EventLedger()
    try:
        record_operator_material_occurrence(
            ledger,
            locality_identity="producer-population",
            exact=b"2+2=5\n",
            source_boundary="exact supplied material boundary",
        )
        refusal = None
    except Exception as error:
        refusal = f"{type(error).__name__}: {error}"
    return _reading(ledger, refusal)


def _determination_sequence() -> dict[str, Any]:
    from tests.test_addressed_byte_occurrence_reference_determination import _record

    ledger = EventLedger()
    try:
        _record(ledger)
        refusal = None
    except Exception as error:
        refusal = f"{type(error).__name__}: {error}"
    return _reading(ledger, refusal)


def _reading(ledger: EventLedger, refusal) -> dict[str, Any]:
    occurrences = ledger.list()
    positions = {e.identity: f"#append-{i}" for i, e in enumerate(occurrences)}
    return {
        "refusal": refusal,
        "kinds_in_order": [e.kind for e in occurrences],
        "count": len(occurrences),
        "exact_material": [
            None if e.exact_material is None else e.exact_material.hex()
            for e in occurrences
        ],
        "material": [_by_position(e.material, positions) for e in occurrences],
    }


def _ordered_path_sequence() -> dict[str, Any]:
    from tests.test_comparison_of_ordered_path_source_position_material import (
        _comparisons,
    )

    ledger = EventLedger()
    try:
        _comparisons(ledger, locality="producer-population", exact=b"aba")
        refusal = None
    except Exception as error:
        refusal = f"{type(error).__name__}: {error}"
    return _reading(ledger, refusal)


def _standing_boundary_sequence() -> dict[str, Any]:
    from tests.test_operator_checkpoint import _act, _assignment, _context

    ledger = EventLedger()
    try:
        standing, _representation, command = _context(ledger)
        assignment = _assignment(ledger, standing, command)
        _act(ledger, assignment)
        refusal = None
    except Exception as error:
        refusal = f"{type(error).__name__}: {error}"
    return _reading(ledger, refusal)


def _shared_position_sequence() -> dict[str, Any]:
    from tests.test_measurement_of_shared_position_of_byte_pair_occurrences import (
        _fixture,
    )

    ledger = EventLedger()
    try:
        _fixture(ledger=ledger, locality="producer-population")
        refusal = None
    except Exception as error:
        refusal = f"{type(error).__name__}: {error}"
    return _reading(ledger, refusal)


SEQUENCES: list[tuple[str, Callable[[], dict[str, Any]]]] = [
    ("acquisition", _acquisition_sequence),
    ("determination", _determination_sequence),
    ("ordered path comparison", _ordered_path_sequence),
    ("standing boundary reference", _standing_boundary_sequence),
    ("shared position", _shared_position_sequence),
]


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    for sequence_name, sequence in SEQUENCES:
        print(f"\n  sequence: {sequence_name}\n")
        baseline = sequence()
        for module_name, producer_name in PRODUCERS:
            module = importlib.import_module(f"seed_runtime.{module_name}")
            producer = getattr(module, producer_name, None)
            if producer is None:
                continue
            parameters = list(inspect.signature(producer).parameters)
            calls = {"count": 0}

            def substituted(*arguments, _producer=producer, _calls=calls, **keywords):
                _calls["count"] += 1
                produced = _producer(*arguments, **keywords)
                if isinstance(produced, dict):
                    changed = dict(produced)
                    changed["standing"] = "substituted standing"
                    changed["limit"] = "a different sentence entirely"
                    return changed
                return produced

            setattr(module, producer_name, substituted)
            try:
                after = sequence()
            except Exception as error:
                after = {"refusal": f"{type(error).__name__}: {error}"}
            finally:
                setattr(module, producer_name, producer)

            label = f"{module_name}.{producer_name}"
            if not calls["count"]:
                disposition = "unreached by this sequence"
            elif parameters:
                disposition = f"takes input {parameters}, read separately"
            else:
                outcomes = [
                    key
                    for key in ("refusal", "count", "kinds_in_order", "exact_material")
                    if baseline.get(key) != after.get(key)
                ]
                if outcomes:
                    disposition = f"CHANGED an outcome: {', '.join(outcomes)}"
                elif baseline["material"] != after["material"]:
                    disposition = "changed recorded material only"
                else:
                    disposition = "changed nothing at all"
            print(f"    {calls['count']:4} calls   {disposition:44} {label}")

    print(
        "\n  A producer disposed as changing recorded material only was read by\n"
        "  nothing these sequences reach.  None of the observed outputs changed;\n"
        "  no internal branch was traced, so a branch that changed and converged\n"
        "  on the same outputs would not be seen here."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
