"""Ask what the flat coordinate table cannot carry.

Two fields sit in the Grammar for reasons that are not physiology.
`book_reference` cites the Book clause a surface projects, which is an address.
`branch_of_current_Standing` was defended on the ground that a flat table has
nowhere else to carry containment, which is an argument about the shape of the
file rather than about Seed.

The Book states a topology: current Standing carries exact Responsibility
branches, and a branch carries its result. A dict of clause identity to body
states no containment at all, so a clause that is a branch of the Standing
carrying another clause's result has to say so in its own body.

What that workaround actually produces is measured here, before any shape is
proposed.

Usage:
    .venv/bin/python scripts/observe_flat_projection_shape.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed" / "witness_grammar.json"

# every key the Grammar uses, and what it is
PHYSIOLOGY = (
    "subject", "subjects", "Responsibility", "exact_Act", "result", "requires",
    "relations", "relation", "carried_coordinates", "coordinates", "current",
    "first_subject", "second_subject", "bounds", "rule", "role",
    "responsibility_subject_set", "completeness_boundary", "required_Admission",
    "Applicability", "Admission", "Participation",
    "one_occurrence", "separate_occurrence", "boundary", "occurrence",
    "Applicability_subject_for",
)
ADDRESS = ("book_reference", "branch_of_current_Standing")


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declared = grammar["book_coordinates"]

    keys: set[str] = set()

    def walk(value):
        if isinstance(value, dict):
            for key, nested in value.items():
                keys.add(key)
                walk(nested)
        elif isinstance(value, list):
            for nested in value:
                walk(nested)

    walk({k: v for k, v in grammar.items() if k != "book_coordinates"})
    for body in declared.values():
        walk(body)

    physiology = sorted(k for k in keys if k in PHYSIOLOGY)
    address = sorted(k for k in keys if k in ADDRESS)
    other = sorted(keys - set(PHYSIOLOGY) - set(ADDRESS) - set(declared))

    print(f"  constitutional physiology keys: {len(physiology)}")
    print(f"    {', '.join(physiology)}\n")
    print(f"  address keys: {len(address)}")
    print(f"    {', '.join(address)}\n")
    if other:
        print(f"  unclassified: {', '.join(other)}\n")

    citing = [
        (path, body["book_reference"])
        for path, body in (
            ("standing.current", grammar["standing"]["current"]),
            *((f"relations.{n}", b) for n, b in grammar["relations"].items()),
        )
        if "book_reference" in body
    ]
    print(f"  surfaces citing a Book clause: {len(citing)}")
    for path, reference in citing:
        print(f"    {path:26} {reference}")

    print("\n  what each branch coordinate names, and whether it resolves:\n")
    results = {
        body["result"]: name
        for name, body in declared.items()
        if isinstance(body.get("result"), str)
    }
    resolves = unresolved = 0
    for name, body in declared.items():
        value = body.get("branch_of_current_Standing")
        if not value:
            continue
        named = value.replace("current_Standing_carrying_", "")
        found = [
            coordinate
            for result, coordinate in results.items()
            if result in named or named.endswith(result)
        ]
        if found:
            resolves += 1
        else:
            unresolved += 1
        print(f"    {name:16} names {named}")
        print(f"      {'resolves to ' + ', '.join(found) if found else 'resolves to nothing'}")

    print(
        f"\n  {resolves} of {resolves + unresolved} resolve.\n"
        "\n  So the key is not a coordinate and is not working serialization\n"
        "  either. Its value is a description where an address is needed: one\n"
        "  names a result another clause declares, one names a result no clause\n"
        "  declares, and one is a pronoun. Nothing can follow any of them.\n"
        "\n  The loss the flat table takes is therefore real and measurable. The\n"
        "  Book states that a Responsibility is a branch of the Standing carrying\n"
        "  a particular result, which is a reference from one clause to another,\n"
        "  and a dict from clause identity to body has no place to put one.\n"
        "\n  The smallest shape that removes the loss is not nesting. It is making\n"
        "  the reference resolvable: name the coordinate whose result that\n"
        "  Standing carries, so a reader can follow it and a test can check it.\n"
        "  Nesting book_coordinates under Standing would mix clause identity with\n"
        "  topology and rewrite every consumer; an address changes the two clauses\n"
        "  that carry one, and the one I introduced last commit that carries a\n"
        "  pronoun.\n"
        "\n  Where clause citation belongs is a separate question with the same\n"
        "  answer as the address table: `book_reference` says which Book law a\n"
        "  surface projects, which is not Standing, a relation, or a coordinate.\n"
        "  Five of its six uses predate this campaign and sit on the relations.\n"
        "\n  Nothing is amended. This measures the two fields and the loss; it does\n"
        "  not establish that either shape is the one to build."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
