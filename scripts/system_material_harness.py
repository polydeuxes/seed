#!/usr/bin/env python3
"""Supply exact system material through Ingest."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.identities import new_identity
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
        material = completed.stdout
        boundary = f"operator harness, subprocess stdout (exit {completed.returncode})"

    ledger = SQLiteEventLedger(args.db)
    try:
        locality = args.locality or new_identity("locality")
        occurred = preserve_system_material(
            ledger,
            locality_identity=locality,
            exact_bytes=material,
            source_boundary=boundary,
        )
        assert ingested_material_bytes(occurred) == material
    finally:
        ledger.close()

    print(f"  locality     {locality}")
    print(f"  material     {len(material):,} bytes")
    print(f"  material     {occurred.identity}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
