"""Ask whether a Representation Act names one thing.

The Book says a Representation Act preserves exact material from one exact
source result, and that its result carries that material and its source
coordinates.  Whether the runtime records one thing under that name is not
settled by the name.

The same recorder is called both ways it permits, with a source result and
without one.  What each records is read, and so is the Responsibility each Act
evidence claims, because a difference in what a function was passed is not a
difference in what an occurrence is responsible for.

Nothing here says either call is wrong, that Representation names too much, or
what a Representation Act ought to require.

Usage:
    .venv/bin/python scripts/observe_representation_act_modes.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation import record_operator_representation

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)


def _recorded(source: bool):
    ledger = EventLedger()
    acquired = record_operator_material_occurrence(
        ledger,
        locality_identity="representation-modes",
        exact=b"2+2=5\n",
        source_boundary="exact supplied material boundary",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="representation-modes"
    )
    recorded = record_operator_representation(
        ledger,
        locality_identity="representation-modes",
        locality_standing=standing,
        source_occurrence_reference=acquired.identity if source else None,
    )
    event = ledger.get(recorded["representation_event_identity"])
    _LEDGERS[event.identity] = ledger
    return event, acquired


def _act_evidence(event):
    from seed_runtime.events import EventLedger  # noqa: F401

    return _LEDGERS[event.identity].get(
        event.material["responsible_act_evidence_identity"]
    ).material


_LEDGERS: dict = {}


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    print("  the Book: a Representation Act preserves exact material from one")
    print("  exact source result, and the result carries that material and its")
    print("  source coordinates.\n")

    for source in (True, False):
        event, acquired = _recorded(source)
        carried = (
            None
            if event.exact_material is None
            else len(event.exact_material)
        )
        print(f"  called {'with' if source else 'without'} a source result")
        print(f"    exact material carried: {carried if carried is not None else 'none'}")
        print(
            f"    same bytes as the source result: "
            f"{event.exact_material == acquired.exact_material}"
        )
        print(
            f"    source occurrence named: "
            f"{event.material.get('source_occurrence_reference')}"
        )
        print(
            f"    representation_result: "
            f"{str(event.material.get('representation_result'))[:64]!r}\n"
        )

    sourced, _ = _recorded(True)
    sourceless, _ = _recorded(False)
    import seed_runtime.events as _  # noqa: F401

    print("  the Responsibility each Act evidence claims:\n")
    for label, event in (("with a source", sourced), ("without one", sourceless)):
        evidence = _act_evidence(event)
        print(f"    {label:16} {evidence.get('responsibility')!r}")
        print(f"    {'':16} act: {evidence.get('act')!r}")
    print(
        "\n  Both claim one Responsibility and one Act, and their Act evidence\n"
        "  differs in no coordinate.  So these are two invocation shapes and not\n"
        "  two Responsibilities: what a caller passed is not what an occurrence\n"
        "  is responsible for.\n"
        "\n  The claimed Responsibility yields a Representation from carried\n"
        "  Locality coordinates.  The Book's Representation Act preserves exact\n"
        "  material from one exact source result.  Those are not the same\n"
        "  requirement, and the call carrying no source result satisfies the\n"
        "  first while meeting nothing the second states.\n"
        "\n  What Responsibility that occurrence witnesses is not established\n"
        "  here, and no second Representation is invented to hold it."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
