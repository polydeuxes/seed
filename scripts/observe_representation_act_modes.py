"""Ask whether a Representation Act names one thing.

The Book says a Representation Act preserves exact material from one exact
source result, and that its result carries that material and its source
coordinates.  Whether the runtime records one thing under that name is not
settled by the name.

The same recorder is called both ways it permits, with a source result and
without one, and what each records is read.

Nothing here says which mode is right, that either should change, or what
Representation ought to be.

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
    return ledger.get(recorded["representation_event_identity"]), acquired


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

    print(
        "  One recorder, two modes.  Called with a source result it preserves\n"
        "  that result's exact material and names the occurrence it came from.\n"
        "  Called without one it records neither, and what it does record under\n"
        "  representation_result is the same sentence either way.\n"
        "\n  So the sentence the Book states describes one of the two.  This does\n"
        "  not say the other is wrong, that Representation names too much, or\n"
        "  what a Representation Act with no source result establishes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
