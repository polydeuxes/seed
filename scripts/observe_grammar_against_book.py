"""Audit the machine grammar against the Book, grammar first.

The earlier recovery walked the Book and asked what the grammar was missing.
It could not have found anything the grammar authored, and reporting nothing
unsupported was reporting the one result that instrument could produce.

This walks the other way.  Every schema key, every authored value, and every
one of the thirty-one clause bodies is read against the active Book, and a
matching identifier is not read as a faithful body.

Each term is classified: an exact Book term, faithful serialization under an
authored name, machine-schema syntax carrying no constitutional meaning, a
compression of several Book distinctions, an unsupported distinction the JSON
authored, or Unknown.

The counts are measured.  The classification is a reading, and is recorded per
term so it can be disagreed with at the row that states it.

Usage:
    .venv/bin/python scripts/observe_grammar_against_book.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

BOOK = Path(__file__).resolve().parents[1] / "book_of_seed"
GRAMMAR = BOOK / "witness_grammar.json"

# key -> (class, reading)
KEYS = {
    "Admission": ("A", "the Book states Admission and required Admission prior to Participation"),
    "Applicability": ("A", "01.Standing.E.1 states Applicability and its result"),
    "Participation": ("A", "02.Acts.A states Participation as an exact relation"),
    "Responsibility": ("A", "stated throughout"),
    "boundary": ("A", "the Book carries boundary in 39 places"),
    "coordinate": ("A", "stated throughout"),
    "coordinates": ("A", "stated throughout"),
    "current": ("A", "current Standing is stated throughout"),
    "exact_Act": ("A", "02.Acts.A — one exact Responsibility bounds one exact Act"),
    "first_subject": ("A", "stated as the first subject of a relation"),
    "second_subject": ("A", "stated as the second subject of a relation"),
    "occurrence": ("A", "stated throughout"),
    "reference": ("A", "stated throughout"),
    "relation": ("A", "stated throughout"),
    "relations": ("A", "02.Authority states relations; 12 states required support relations"),
    "requires": ("A", "stated throughout"),
    "responsibility": ("A", "stated throughout"),
    "result": ("A", "stated throughout"),
    "role": ("A", "02.Acts.A states one Act-local role"),
    "rule": ("A", "04.Compare — a Compare Responsibility carries its exact rule"),
    "standing": ("A", "stated throughout"),
    "subject": ("A", "stated throughout"),
    "completeness_boundary": ("A", "01.Source.D and 04.Compare state the completeness boundary"),
    "result_boundary": ("A", "01.Source.E.1 states the Candidate result boundary"),
    "test_subject": ("A", "01.Source.C — it is one test subject and no other subject"),
    "witness_grammar": ("A", "01.Source.C names this witness grammar as a Fidelity subject"),
    "source_references": ("A", "01.Source.E and 04.Compare.B state exact source references"),
    "later_Standing": ("A", "stated in six places"),
    "required_Admission": ("A", "01.Source.E.1 and 04.Compare state required Admission"),
    "establishes_no": ("B", "serializes the Book's 'establishes no', its dominant grammar"),
    "responsibility_source": ("B", "serializes 'is a branch of current Standing carrying ...'; the name is authored"),
    "responsibility_subject_set": ("B", "serializes 'the bounded subject set is exhaustive'; the name is authored"),
    "subject_boundary": ("B", "serializes 'the Candidate is the exact Compare subject'; the name is authored"),
    "carried_coordinates": ("B", "serializes 'coordinates carried by that Candidate'; the name is authored"),
    "book_coordinates": ("C", "container of clause projections; addresses clauses, states none"),
    "book_reference": ("C", "a citation address"),
    "book_material_reference": ("C", "a citation address"),
    "input": ("E", "the Book's input is a position a support relation reaches, and what an input REQUIRES is its Applicability result and Participation; the JSON lists the requirement AS the input, reversing which is which"),
    "path": ("E", "every Book use of path is a provenance path or an ordered relation path; standing.path is an ordered required-coordinate chain, and 01.Standing states Responsibilities as branches, not a path"),
}


def _clause_text() -> dict[str, str]:
    found = {}
    for path in sorted((BOOK / "chapters").glob("*.md")):
        for part in re.split(r"^### ", path.read_text(), flags=re.M)[1:]:
            body = part.split("\n", 1)[1].split("\n## ")[0]
            found[part.split(" —")[0]] = " ".join(body.split())
    return found


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declared = grammar["book_coordinates"]
    clause = _clause_text()
    book = " ".join(
        "\n".join(p.read_text() for p in sorted((BOOK / "chapters").glob("*.md")))
        .lower()
        .split()
    )

    values = set()

    def walk(value):
        if isinstance(value, dict):
            for nested in value.values():
                walk(nested)
        elif isinstance(value, list):
            for nested in value:
                walk(nested)
        elif isinstance(value, str):
            values.add(value)

    walk(grammar)

    print(f"  {len(KEYS)} distinct schema keys, {len(values)} distinct authored values,")
    print(f"  {len(declared)} clause bodies.\n")

    for mark, name in (
        ("A", "exact Book term"),
        ("B", "faithful serialization under an authored name"),
        ("C", "machine-schema syntax, no constitutional meaning"),
        ("D", "compression of several Book distinctions"),
        ("E", "unsupported distinction the JSON authored"),
        ("F", "Unknown"),
    ):
        rows = {k: v for k, v in KEYS.items() if v[0] == mark}
        print(f"  {mark} — {name}: {len(rows)}")
        if mark == "D":
            print("      no key compresses.  Compression is in the bodies, counted below.")
        if mark in ("B", "E"):
            for key, (_m, reading) in rows.items():
                print(f"      {key}")
                print(f"        {reading}")
    print()

    # An Act the Book never names, minted to fill a required schema slot.
    minted = []
    for identity, body in declared.items():
        act = body.get("exact_Act")
        if act and act.replace("_", " ").lower() not in book:
            minted.append((identity, act, act == body.get("Responsibility")))
    doubled = [row for row in minted if row[2]]
    print(f"  exact_Act values naming an Act the Book never names: {len(minted)}/30")
    print(f"    of those, identical to the clause's Responsibility: {len(doubled)}")
    for identity, act, _ in minted:
        print(f"      {identity:16} {act}")

    # Denials are the Book's dominant grammar and the enforceable half.
    denied = total = 0
    dropped = []
    for identity, body in declared.items():
        matches = re.findall(r"establishes? no ([^.]+)\.", clause[identity], re.I)
        if not matches:
            continue
        total += 1
        for match in matches:
            denied += len(re.split(r",| or ", match))
        if "establishes_no" not in body:
            dropped.append(identity)
    print(f"\n  clauses whose Book text carries a denial: {total}/{len(declared)}")
    print(f"  distinct things denied across them: about {denied}")
    print(f"  of those clauses, carrying no establishes_no in the JSON: {len(dropped)}")

    print("\n  two clauses where the minted Act comes out of the denial itself:\n")
    for identity in ("01.Standing.A", "01.Standing.D"):
        print(f"    {identity}")
        print(f"      Book: {clause[identity][:150]}")
        print(f"      JSON subject: {declared[identity]['subject']}")
        print(f"      JSON Act:     {declared[identity]['exact_Act']}")
        print(f"      JSON result:  {declared[identity]['result']}")

    same = [
        identity
        for identity, body in declared.items()
        if body.get("subject") and body["subject"] == body.get("result")
    ]
    print(f"\n  clauses whose declared result repeats their declared subject: {len(same)}")
    print(f"    {', '.join(same)}")

    compare = {k: v.get("input") for k, v in declared.items() if k.startswith("04.Compare")}
    carrying = [k for k, v in compare.items() if v and "exact_Admission_occurrence" in v]
    print(f"\n  Compare clauses whose Book text requires Admission prior to Participation: {len(compare)}")
    print(f"  Compare clauses whose JSON carries it: {len(carrying)}  {carrying}")

    print(
        "\n  A matching identifier is not a faithful body.  The Book's grammar is\n"
        "  mostly denial, and the denials are the half that can refuse anything;\n"
        "  the projection carries them for two of the twenty-four clauses that\n"
        "  state one.\n"
        "\n  Where a clause names no Act, the schema still required one, and a name\n"
        "  was made from the Responsibility's own words.  Naming an Act there\n"
        "  moves the gap rather than closing it, and Fidelity then compares a Seed\n"
        "  occurrence against an Act no witness states.\n"
        "\n  Counts are measured.  Each classification is a reading of two recovered\n"
        "  texts, recorded per term so it can be disagreed with at the row that\n"
        "  states it.  Nothing is amended and nothing here says which side changes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
