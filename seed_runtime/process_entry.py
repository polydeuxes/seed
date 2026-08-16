"""Live process entry for the operator console."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.identities import new_identity
from seed_runtime.operator_console import run_persistent_operator_console

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="seed")
    parser.add_argument("--db", help="SQLite event ledger path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity=new_identity("locality"),
            input_stream=getattr(sys.stdin, "buffer", sys.stdin),
            output_stream=sys.stdout,
            emit_initial_representation=False,
            raw_output_stream=getattr(sys.stdout, "buffer", None),
        )
        return 0
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


if __name__ == "__main__":
    raise SystemExit(main())
