"""Test each grammar key by removing it, not by looking its name up in the Book.

The previous pass classified a key as exact grammar when the Book used the same
phrase.  That is two authored surfaces agreeing, which is not corroboration:
`test_subject` passed because chapter 04 contains the words "one test subject".
Every disposition warranted that way is withdrawn here.

The unit is a distinction, not a word.  For each key: ignore its name, recover
what distinction it claims to preserve, substitute the smallest already-stated
grammar that could carry the same thing, and ask what becomes impossible to
tell apart afterwards.  A key survives only when removing it destroys a
distinction recoverable independently of the key.

Two mechanical facts feed the readings and neither decides one: a key whose
value never varies has not been shown to discriminate anything, and a key whose
value repeats another key in the same body carries that key's content twice.

Usage:
    .venv/bin/python scripts/observe_grammar_distinctions_by_elimination.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

GRAMMAR = (
    Path(__file__).resolve().parents[1] / "book_of_seed" / "witness_grammar.json"
)

# key -> (disposition, what it claims, what it is substituted with, what is lost)
ELIMINATION = {
    "test_subject": (
        "decomposes",
        "that the Book-material-acquisition witness is a subject of a deterministic test",
        "subject, plus a Participation relation to that test Act occurrence",
        "which Act occurrence the subject participates in — and that is lost only "
        "because the deterministic test is never declared as an Act. The compound "
        "is the residue of an undeclared Act, and it kept the positive half of a "
        "sentence whose content is a denial: 'and no other subject'",
    ),
    "result_boundary": (
        "decomposes",
        "that the Candidate result is bounded by its Act occurrence and Yield",
        "relations: [yield] and result",
        "nothing; both substitutes are already in the same clause body",
    ),
    "subject_boundary": (
        "decomposes",
        "that the exact Candidate result bounds what the Compare subject is",
        "subject, plus the clause's own denial",
        "nothing the denial would not carry better: the Book says a source "
        "Assertion reference is no other Compare subject, and that denial is dropped",
    ),
    "boundary": (
        "decomposes",
        "the boundary at which Admission is required",
        "required_Admission",
        "nothing; its only value restates the key beside it",
    ),
    "witness_grammar": (
        "decomposes",
        "that this Grammar is a subject carrying this Book and no relations",
        "the this_Grammar reference already declared",
        "nothing recoverable: relations is an empty list, and an empty list cannot "
        "be told apart from an absent one, so the denial it looks like is not stated",
    ),
    "role": (
        "decomposes at its one site",
        "the Act-local role a subject participates under",
        "subject",
        "nothing here; its only value repeats the subject beside it. An Act-local "
        "role is a real distinction in 02.Acts.A and this site does not carry one",
    ),
    "input": (
        "unsupported",
        "what an Act takes in",
        "nothing, because the Book puts these coordinates elsewhere",
        "the Book's input is a position a support relation reaches, and what an "
        "input requires is its Applicability result and Participation relation. "
        "The JSON lists that requirement as the input, so requirement and "
        "requirer are exchanged",
    ),
    "path": (
        "unsupported",
        "the ordered coordinates Standing requires",
        "the requires list already used elsewhere in the file",
        "an ordering the Book never states. 01.Standing states each Responsibility "
        "as a branch of Standing, and every Book use of path is a provenance path "
        "or an ordered relation path, neither of which this is",
    ),
    "source_references": (
        "unsupported",
        "that certain names in this file address certain subjects",
        "nothing in the Book; it is this file's own token table",
        "the Book's exact source references are coordinates of a Candidate result, "
        "a different responsibility under the same words",
    ),
    "book_material_reference": (
        "unsupported",
        "which Book the material is",
        "nothing",
        "nothing: three uses, one value, never varying, so no two things are told "
        "apart by it",
    ),
    "establishes_no": (
        "survives",
        "that a clause denies something rather than being silent about it",
        "nothing else in the schema",
        "every denial. It is the only key that can refuse anything, and the Book's "
        "grammar is mostly denial",
    ),
    "later_Standing": (
        "survives",
        "Standing established after, as against current Standing",
        "standing.current",
        "01.Standing.A.1 entirely: that a result is one coordinate of current "
        "Standing and establishes no later Standing occurrence cannot be said once "
        "the two collapse",
    ),
    "rule": (
        "survives",
        "the declared rule a Compare runs under",
        "subject and Responsibility",
        "the difference between two Compares over the same subjects under "
        "different rules, which 04.Compare states as a Responsibility coordinate",
    ),
    "responsibility_subject_set": (
        "survives",
        "the bounded subject set a Responsibility is exhaustive over",
        "nothing else in the schema",
        "what exhaustiveness is exhaustive over. 01.Standing.D turns on it",
    ),
    "carried_coordinates": (
        "survives",
        "coordinates carried by a subject as against established by it",
        "coordinates",
        "the carried-versus-established distinction. Whether it duplicates the "
        "carriage relation of 02.Acts.A is not settled here",
    ),
    "required_Admission": (
        "survives",
        "that this boundary requires Admission prior to Participation",
        "Admission",
        "the difference between a boundary requiring Admission and one not "
        "requiring it. That is a property of the boundary and this key attaches "
        "it to Admission, so the distinction survives and its placement does not",
    ),
    "book_reference": (
        "survives",
        "which clause warrants a declared relation",
        "nothing else in the schema",
        "the warrant for each relation; four distinct values across five uses",
    ),
    "completeness_boundary": (
        "Unknown",
        "what a result is complete over",
        "responsibility_subject_set",
        "not determinable here. What a result is complete over and what a "
        "Responsibility is exhaustive over are separable, and its one value sets "
        "them equal while later_Standing in the same body denies completion over "
        "that set",
    ),
    "responsibility_source": (
        "Unknown",
        "which current Standing a Responsibility is a branch of",
        "nothing else in the schema",
        "not determinable here. Nothing else carries it, and it may be a branch "
        "relation written as a coordinate — the same question standing.path raises",
    ),
}


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    values: dict[str, list[str]] = defaultdict(list)

    def walk(value):
        if isinstance(value, dict):
            for key, nested in value.items():
                if isinstance(nested, (str, list)):
                    values[key].append(json.dumps(nested))
                walk(nested)
        elif isinstance(value, list):
            for nested in value:
                walk(nested)

    walk(grammar)

    print("  Withdrawn: every disposition of the previous pass warranted only by")
    print("  the Book using the same word. The Book using a word and the JSON")
    print("  repeating it are one authored surface twice, not two witnesses.\n")

    constant = sorted(k for k, v in values.items() if len(set(v)) == 1)
    print(f"  keys whose value never varies, so nothing is told apart by them: {len(constant)}")
    for key in constant:
        print(f"    {key:28} {len(values[key])} use(s)")

    print()
    for name in ("survives", "decomposes", "unsupported", "Unknown"):
        rows = {
            k: v
            for k, v in ELIMINATION.items()
            if v[0] == name or v[0].startswith(name)
        }
        print(f"  {name}: {len(rows)}\n")
        for key, (_d, claims, substitute, lost) in rows.items():
            print(f"    {key}")
            print(f"      claims:      {claims}")
            print(f"      substituted: {substitute}")
            print(f"      lost:        {lost}")
        print()

    print(
        "  The words `test` and `deterministic` are both in the Book's 198-word\n"
        "  admission list. That records that the Book uses them, which is the same\n"
        "  fact as the Book using them, so it warrants no coordinate either.\n"
        "\n  The structural findings of the previous pass stand and none of them\n"
        "  rested on vocabulary: eighteen exact_Act values naming an Act the Book\n"
        "  never names, twenty-two of twenty-four clauses dropping their denial,\n"
        "  one of four Compare clauses carrying required Admission, and six\n"
        "  clauses whose result repeats their subject.\n"
        "\n  Each disposition above is a reading of a substitution, recorded per key\n"
        "  so it can be disagreed with at the row that states it. The two\n"
        "  mechanical facts are measured and decide nothing on their own: a key\n"
        "  used once has not been shown to discriminate, which is not the same as\n"
        "  being shown not to. Nothing is amended."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
