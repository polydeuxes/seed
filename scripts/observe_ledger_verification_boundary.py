"""Observe what each ledger can say about a stored occurrence's integrity.

Every Yield observer beside this one perturbs an occurrence held by an
in-memory ledger.  That ledger reports one thing about integrity and a durable
ledger reports another, so a reading taken from the first carries a constraint
the reading itself cannot show.

This records the difference so those readings can be read with it.

Usage:
    .venv/bin/python scripts/observe_ledger_verification_boundary.py
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
import sqlite3
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)

LOCALITY = "verification-boundary"
EXACT = b"2+2=5\n"


def _record(ledger):
    return record_operator_material_occurrence(
        ledger,
        locality_identity=LOCALITY,
        exact=EXACT,
        source_boundary="exact supplied material boundary",
    )


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    ledger = EventLedger()
    result = _record(ledger)
    act_evidence = ledger.get(result.material["responsible_act_evidence_identity"])
    before = ledger.integrity_of(act_evidence.identity)
    material = deepcopy(act_evidence.material)
    material["authority"] = "substituted"
    object.__setattr__(act_evidence, "material", material)
    after = ledger.integrity_of(act_evidence.identity)

    print("  in-memory ledger")
    print(f"    integrity before a change: {before}")
    print(f"    integrity after a change:  {after}")
    print(f"    reports corrupted:         {after == CORRUPTED}")
    print(
        f"    the reader returns the stored occurrence itself: "
        f"{ledger.get(act_evidence.identity) is act_evidence}"
    )
    print(
        "\n    A predicate asking whether an occurrence is not corrupted passes\n"
        "    here for every occurrence it is asked about, changed or not.  That\n"
        "    is this ledger's ordinary answer, and it is not the whole story:\n"
        "    observe_exact_relation_reach.py substitutes the reading, making the\n"
        "    ledger report one occurrence corrupted, and does exercise the\n"
        "    predicate's response to that value without reproducing the durable\n"
        "    boundary below."
    )

    with tempfile.TemporaryDirectory() as directory:
        database = str(Path(directory) / "boundary.sqlite")
        durable = SQLiteEventLedger(database)
        result = _record(durable)
        identity = result.material["responsible_act_evidence_identity"]
        stored = durable.get(identity)
        print("\n  durable ledger")
        print(f"    integrity of a recorded occurrence: {durable.integrity_of(identity)}")
        print(
            f"    the reader returns the stored occurrence itself: "
            f"{durable.get(identity) is stored}"
        )
        durable.close()

        connection = sqlite3.connect(database)
        blob = connection.execute(
            "SELECT material FROM events WHERE identity=?", (identity,)
        ).fetchone()[0]
        changed = bytes(blob[:-1]) + bytes([blob[-1] ^ 0x01])
        try:
            connection.execute(
                "UPDATE events SET material=? WHERE identity=?", (changed, identity)
            )
            outcome = "accepted"
        except sqlite3.IntegrityError as error:
            outcome = f"refused: {error}"
        connection.close()
        print(f"    changing a stored occurrence: {outcome}")

    print(
        "\n  So a change reached by holding an in-memory occurrence is not a\n"
        "  change a durable ledger permits.  Readings from the other observers\n"
        "  say what the predicates read from the material they are given.  They\n"
        "  do not say that any state they construct is reachable."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
