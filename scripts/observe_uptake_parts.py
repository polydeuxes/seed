"""Observe whether Seed can stand on the consumer side of what it produced.

A result is produced and something has to take it up before anything further
can be asked of it.  Rosetta decomposes that: Uptake is availability with
Applicability and Participation.

So each part is read separately, by how often the runtime speaks of it and by
how many recorded coordinates carry it.  Speaking of something and recording it
are different, and a part spoken of but never recorded cannot be one an
occurrence establishes.

Nothing here proposes a coordinate, a relation, or a Book amendment.

Usage:
    .venv/bin/python scripts/observe_uptake_parts.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

RUNTIME = Path(__file__).resolve().parents[1] / "seed_runtime"
PARTS = ("availability", "applicability", "participation")


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    sources = {p.name: p.read_text() for p in sorted(RUNTIME.glob("*.py"))}
    joined = "\n".join(sources.values())

    print("  Uptake is availability with Applicability and Participation")
    print("  (rosetta/roots.md:94)\n")
    print("  part            spoken of   recorded coordinates carrying it")
    for part in PARTS:
        spoken = len(re.findall(rf"\b{part}\b", joined, re.I))
        recorded = len(
            {
                name
                for name in re.findall(r'"([a-z_.]+)"', joined)
                if part in name
            }
        )
        print(f"    {part:14} {spoken:6}      {recorded}")

    uptake = [
        f"{name}:{line}"
        for name, text in sources.items()
        for line, content in enumerate(text.split("\n"), start=1)
        if re.search(r"\buptake\b", content, re.I)
    ]
    print(f"\n  the whole named: {len(uptake)} mention(s)")
    for where in uptake:
        name, line = where.rsplit(":", 1)
        content = sources[name].split("\n")[int(line) - 1].strip()
        print(f"    {where}  {content[:76]}")

    print(
        "\n  Two parts are recorded and carried by occurrences.  One is spoken of\n"
        "  and carried by none, so no occurrence records it.  The whole is named\n"
        "  once, to say the module does not claim it.\n"
        "\n  This counts what the runtime says and records.  It does not say what\n"
        "  Uptake should require, that the missing part belongs in the Book, or\n"
        "  that anything ought to be built."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
