"""Live process entry for the operator console and its visibility boundary."""

from __future__ import annotations

import argparse
import json
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
    visibility = parser.add_mutually_exclusive_group()
    visibility.add_argument(
        "--diagnostic-inventory",
        action="store_true",
        help="list active and compatibility-only diagnostic surfaces",
    )
    visibility.add_argument(
        "--diagnostic-shape-audit",
        action="store_true",
        help="audit registered diagnostic implementation shapes",
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output", help="emit JSON"
    )
    parser.add_argument(
        "--status",
        choices=("consistent", "warning", "mismatch", "unknown"),
        help="filter diagnostic shape rows by status",
    )
    parser.add_argument(
        "--mismatches",
        action="store_true",
        help="show only diagnostic shape mismatches",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.json_output and not (
        args.diagnostic_inventory or args.diagnostic_shape_audit
    ):
        parser.error("--json requires a visibility command")
    if (args.status or args.mismatches) and not args.diagnostic_shape_audit:
        parser.error("--status and --mismatches require --diagnostic-shape-audit")

    if args.diagnostic_inventory:
        from seed_runtime.diagnostic_inventory import (
            diagnostic_inventory_json,
            format_diagnostic_inventory,
        )

        output = (
            json.dumps(diagnostic_inventory_json(), indent=2)
            if args.json_output
            else format_diagnostic_inventory()
        )
        print(output)
        return 0

    if args.diagnostic_shape_audit:
        from seed_runtime.diagnostic_shape_audit import (
            build_diagnostic_shape_audit,
            diagnostic_shape_audit_json,
            format_diagnostic_shape_audit,
        )

        rows = build_diagnostic_shape_audit()
        status = "mismatch" if args.mismatches else args.status
        output = (
            json.dumps(diagnostic_shape_audit_json(rows, status=status), indent=2)
            if args.json_output
            else format_diagnostic_shape_audit(rows, status=status)
        )
        print(output)
        return 0

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
