#!/usr/bin/env python3
"""Perform an invocation on Seed's behalf and hand it exactly what came back.

Provisional, and expected to be deleted. Its purpose is to separate two things
that operator ingress has been carrying at once:

```text
  operator path   "learn english"            instruction and testimony
  system path     the books themselves       material
```

Until now every book was stuffed through operator ingress, so material Seed was
meant to acquire arrived as though the operator had typed it. That muddled the
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
what has to be recovered, and it will be visible rather than remembered.

Usage:

    system_material_harness.py --db seed.db --workspace local -- ls -la corpus/
    system_material_harness.py --db seed.db --workspace local --file corpus/x.txt
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.system_material import (
    DeclaredInvocation,
    declare_invocation,
    preserve_system_material,
    system_material_bytes,
)


HARNESS = "operator system-material harness"
SESSION_PREFIX = "system_invocation_session"


def _next_invocation_session(ledger: SQLiteEventLedger, workspace_id: str) -> str:
    """One unused bounded exchange, derived from what the store already holds.

    `new_id` is process-local, and a durable store only reserves the identity
    prefixes it knows about — `SESSION_PREFIX` is not among them. So minting one
    reissued `..._000001` on every run and put separate invocations into one
    exchange, which is exactly the property this boundary claims to keep.

    Deriving it from the store instead makes the identity a fact about the
    store rather than about the process that happened to mint it.
    """

    highest = 0
    for event in ledger.list(workspace_id):
        session_id = event.session_id or ""
        if not session_id.startswith(f"{SESSION_PREFIX}_"):
            continue
        suffix = session_id[len(SESSION_PREFIX) + 1:]
        if suffix.isdigit():
            highest = max(highest, int(suffix))
    return f"{SESSION_PREFIX}_{highest + 1:06d}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True)
    parser.add_argument("--workspace", default="local")
    parser.add_argument("--session", default=None,
                        help="default: one new bounded exchange per invocation")
    parser.add_argument("--file", default=None,
                        help="read this file instead of running a command")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    if args.file:
        material = Path(args.file).read_bytes()
        invocation = f"read {args.file}"
        boundary = "operator harness, file read"
    else:
        command = [item for item in args.command if item != "--"]
        if not command:
            parser.error("give a command after -- , or use --file")
        completed = subprocess.run(command, capture_output=True)
        # stderr is separate material and is not merged into stdout here; a
        # combined stream would preserve neither exactly.
        material = completed.stdout
        invocation = " ".join(command)
        boundary = f"operator harness, subprocess stdout (exit {completed.returncode})"

    ledger = SQLiteEventLedger(args.db)
    try:
        session = args.session or _next_invocation_session(ledger, args.workspace)
        declaration = declare_invocation(
            ledger,
            workspace_id=args.workspace,
            session_id=session,
            declared=DeclaredInvocation(
                invocation=invocation,
                declared_performer=HARNESS,
                on_behalf_of="this Seed",
            ),
        )
        occurred = preserve_system_material(
            ledger,
            workspace_id=args.workspace,
            session_id=session,
            exact_bytes=material,
            observed_boundary=boundary,
        )
        assert system_material_bytes(occurred) == material
    finally:
        ledger.close()

    text = occurred.payload["text_representation"]
    print(f"  invocation   {invocation}")
    print(f"  performed by {HARNESS}")
    print(f"  session      {session}")
    print(f"  material     {len(material):,} bytes, text representation "
          f"{'available' if text['available'] else text['decoder_outcome']}")
    print(f"  declaration  {declaration.id}")
    print(f"  material     {occurred.id}   (not related to the declaration here)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
