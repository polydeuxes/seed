"""Live process entry for the operator console."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_console import run_persistent_operator_console

DEFAULT_WORKSPACE = "local"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="seed")
    parser.add_argument("--db", help="SQLite event ledger path")
    parser.add_argument("--workspace", default=DEFAULT_WORKSPACE, help="workspace id")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        run_persistent_operator_console(
            ledger=ledger,
            workspace_id=args.workspace,
            session_id=new_id("session"),
            input_stream=sys.stdin,
            output_stream=sys.stdout,
        )
        return 0
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


if __name__ == "__main__":
    raise SystemExit(main())
