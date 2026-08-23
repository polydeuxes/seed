"""Report the Book law that carries no clause identifier.

Law stated without an identifier cannot be projected, cited or enforced,
whatever it requires. This counts what remains in that state.

The earlier form of this file carried a hand-written inventory of thirty-eight
distinctions recovered from unnumbered prose. Every chapter it described has
since been recovered, deleted or numbered, so the inventory described a Book
that no longer exists and is gone. What remains is the measurement.

Usage:
    .venv/bin/python scripts/observe_unprojected_book_law.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

BOOK = Path(__file__).resolve().parents[1] / "book_of_seed"
CLAUSE = re.compile(r"^#{2,3}\s+([0-9]+\.[A-Za-z][A-Za-z0-9.]*)\s+—", re.M)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    declared = json.loads(
        (BOOK / "witness_grammar.json").read_text(encoding="utf-8")
    )["book_coordinates"]

    total = loose_total = 0
    unnumbered: dict[str, int] = {}
    for path in sorted((BOOK / "chapters").glob("*.md")):
        current = None
        counted: dict[str | None, int] = {}
        for line in path.read_text(encoding="utf-8").split("\n"):
            if CLAUSE.match(line):
                current = "clause"
                continue
            if line.startswith("#") or line.strip().startswith("- ["):
                current = "references" if line.strip().startswith("- [") else None
                continue
            if line.strip():
                counted[current] = counted.get(current, 0) + 1
        body = sum(v for k, v in counted.items() if k != "references")
        loose = counted.get(None, 0)
        total += body
        loose_total += loose
        if loose:
            unnumbered[path.name] = loose

    print(f"  chapters: {len(list((BOOK / 'chapters').glob('*.md')))}")
    print(f"  clauses carrying an identifier: {len(declared)}")
    print(f"  coordinates the grammar declares: {len(declared)}")
    print(f"  Book body lines: {total}")
    print(f"  body lines carrying no clause identifier: {loose_total}\n")
    for name, loose in unnumbered.items():
        print(f"    {name:42} {loose}")
    if not unnumbered:
        print("    none")

    print(
        "\n  A clause with an identifier can be projected, cited and enforced.\n"
        "  This counts identifiers and lines. It does not say unnumbered law is\n"
        "  wrong, or that any line should be numbered."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
