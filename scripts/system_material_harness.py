#!/usr/bin/env python3
"""Perform an invocation on Seed's behalf and hand it exactly what came back.

Provisional, and expected to be deleted. Its purpose is to separate two things
that operator ingest has been carrying at once:

```text
  operator path   "learn english"            instruction and testimony
  system path     the books themselves       material
```

Until now every book was stuffed through operator ingest, so material Seed was
meant to acquire occurred as though the operator had typed it. That muddled the
experiment, and this is the smallest thing that unmuddles it.

**This harness performs the invocation. The runtime does not.** The subprocess
runs here, in a script, under whatever authority the operator already has — not
inside Seed, and not on Seed's authority.

It attributes the performance to itself and takes no `--performed-by`. A caller
could otherwise name a party the harness cannot speak for, in the one mechanism
whose entire purpose is preserving that line. What a caller may attest to is
what it did.

The record carries no coordinate asserting that Seed did *not* invoke. This
harness knows locally that it ran the subprocess; that does not let a durable
occurrence turn the absence of Evidence about Seed into a negative finding.

**It declares two occurrences and relates neither to the other.** The invocation
declaration and the material are separate subjects. Whether this material is the
answer to that invocation is a third thing with its own participants and its own
Evidence, and this harness does not establish it — it prints both identities so
a later act has them.

That is the whole point of building it. When Seed may eventually invoke on its
own authority, the difference between these records and those ones is exactly
what has to be read, and it will be visible rather than remembered.

Usage:

    system_material_harness.py --db seed.db -- ls -la corpus/
    system_material_harness.py --db seed.db --file corpus/x.txt
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.ids import new_id
from seed_runtime.material_ingest import ingested_material_bytes
from seed_runtime.system_material import preserve_system_material


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True)
    parser.add_argument("--locality", default=None)
    parser.add_argument("--file", default=None,
                        help="read this file instead of running a command")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    if args.file:
        material = Path(args.file).read_bytes()
        boundary = "operator harness, file read"
    else:
        command = [item for item in args.command if item != "--"]
        if not command:
            parser.error("give a command after -- , or use --file")
        completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # stderr is separate material and is not merged into stdout here; a
        # combined stream would preserve neither exactly.
        material = completed.stdout
        boundary = f"operator harness, subprocess stdout (exit {completed.returncode})"

    ledger = SQLiteEventLedger(args.db)
    try:
        locality = args.locality or new_id("locality")
        occurred = preserve_system_material(
            ledger,
            locality_id=locality,
            exact_bytes=material,
            observed_boundary=boundary,
        )
        assert ingested_material_bytes(occurred) == material
    finally:
        ledger.close()

    print(f"  locality     {locality}")
    print(f"  material     {len(material):,} bytes")
    print(f"  material     {occurred.id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
