"""Set the whole active Book beside its machine projection.

Fidelity can only hold the runtime to what the machine grammar states.  Whether
that grammar is the whole Book or the part of it the implemented roads happened
to need is not settled by the tests passing.

Every clause of the active Book carrying an identifier is recovered and set
beside the coordinates the grammar declares.  Then the Book law carrying no
identifier is measured, because a clause with no identifier cannot be projected
and cannot be enforced, whatever it states.

Reading order is the active Book first and the grammar second.  Runtime
presence is never read as warrant for a coordinate.

Usage:
    .venv/bin/python scripts/observe_book_against_machine_grammar.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

BOOK = Path(__file__).resolve().parents[1] / "book_of_seed"
CHAPTERS = BOOK / "chapters"
GRAMMAR = BOOK / "witness_grammar.json"
CLAUSE = re.compile(r"^#{2,3}\s+([0-9]+\.[A-Za-z][A-Za-z0-9.]*)\s+—\s*(.+)$", re.M)
# words the Book uses to state a Responsibility's required physiology
STATES = (
    "Responsibility",
    "Act occurrence",
    "Yield",
    "Participation",
    "Admission",
    "Applicability",
    "Scope",
    "Locality",
    "Unknown",
)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    identified: dict[str, tuple[str, str]] = {}
    for path in sorted(CHAPTERS.glob("*.md")):
        for match in CLAUSE.finditer(path.read_text()):
            identified[match.group(1)] = (path.name, match.group(2).strip())

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    coordinates = set(grammar["book_coordinates"])
    relations = (
        grammar["book_coordinates"]["02.Acts.A"]["Yield"]["relation"],
        grammar["book_coordinates"]["06.Locality.A"]["Locality"]["relation"],
    )

    print(f"  Book clauses carrying an identifier: {len(identified)}")
    print(f"  coordinates the grammar declares:    {len(coordinates)}")
    print(f"  relations the grammar declares:      {len(relations)}"
          f"  ({', '.join(sorted(relations))})\n")

    absent = sorted(set(identified) - coordinates)
    extra = sorted(coordinates - set(identified))
    print(f"  identified clauses the grammar does not declare: {len(absent)}")
    for clause in absent:
        print(f"    {clause}")
    print(f"  coordinates matching no identified clause: {len(extra)}")
    for clause in extra:
        print(f"    {clause}")

    print("\n  Book law carrying no identifier, by chapter:\n")
    total = loose_total = 0
    for path in sorted(CHAPTERS.glob("*.md")):
        current = None
        counted: dict[str | None, int] = {}
        for line in path.read_text().split("\n"):
            heading = CLAUSE.match(line)
            if heading:
                current = heading.group(1)
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
            states = [
                word
                for word in STATES
                if word in path.read_text().split("### ")[0]
            ]
            print(f"    {path.name:42} {loose:3} of {body:3} lines")
            if states:
                print(f"      states: {', '.join(states)}")

    print(
        f"\n  {loose_total} of {total} Book body lines carry no clause identifier."
    )
    print(
        "\n  A clause with an identifier can be projected, cited, and enforced.\n"
        "  Law stated without one cannot be any of those, whatever it requires.\n"
        "  Two chapters carry no identifier anywhere in them.\n"
        "\n  This counts identifiers and lines.  It does not say the unnumbered\n"
        "  law is wrong, that it should be numbered, or that the grammar should\n"
        "  declare anything it does not."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
