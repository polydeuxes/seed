"""Live process entry for the operator console."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.identities import new_identity
from seed_runtime.operator_console import run_persistent_operator_console
from scripts.operator_host_provider import invoke_operator_host
from scripts.primordial_host_escape import primordial_host_input


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="seed")
    parser.add_argument("--db", help="SQLite event ledger path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    raw_output_stream = getattr(sys.stdout, "buffer", None)
    raw_input_stream = getattr(sys.stdin, "buffer", sys.stdin)
    try:
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity=new_identity("locality"),
            input_stream=primordial_host_input(raw_input_stream),
            output_stream=sys.stdout,
            raw_output_stream=raw_output_stream,
            operator_invocation_provider=(
                invoke_operator_host if raw_output_stream is not None else None
            ),
        )
        return 0
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


if __name__ == "__main__":
    raise SystemExit(main())
