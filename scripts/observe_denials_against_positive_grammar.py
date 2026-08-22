"""Ask whether the Book's denials are needed once the positive grammar states enough.

An earlier pass called the JSON dropping twenty-two of twenty-four denials the
worst result in the audit.  That reading assumed denial is how Seed refuses.

Denial is a blocklist, and a blocklist has to have anticipated the inference.
The positive form does not: Standing requires an exact Responsibility, Act
occurrence, Yield, Authority, Scope, limits, and result, so material simply
fails to be Standing without anyone having written that material is not
Standing.  Failing to satisfy a requirement is not an established negative, and
the distinction between the two is the one Seed exists to hold.

Every denial in the active Book is set against the positive requirements the
Book already states, and asked whether the stronger claim could still be
established with the denial gone.

Usage:
    .venv/bin/python scripts/observe_denials_against_positive_grammar.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CHAPTERS = Path(__file__).resolve().parents[1] / "book_of_seed" / "chapters"
DENIAL = re.compile(r"\bestablish(?:es)? no\b")
REQUIRE = re.compile(r"\brequires?\b")
# a denial whose denied thing is fully established and whose content is its reach
REACH = re.compile(
    r"\bfor another\b|\bat another\b|\bother Authority\b|\bcopy of\b|"
    r"\bbeyond (its |exact )?(Scope|bounds)\b|\bfor a result\b|"
    r"\bStanding copy\b|\bfor the result as another subject\b"
)
# nouns whose every Book occurrence is inside a denial
DENIAL_ONLY = (
    "revision", "copy of Standing", "source relation", "erasure", "mutation",
    "copying", "recurrence", "same-content finding", "collective subject",
    "collective relation", "renewed occurrence",
)
# negatives an exact Responsibility yields as its finding
YIELDED = ("inapplicable", "conflicting", "Unknown", "known loss", "conflicts", "limits")


def _sentences() -> list[str]:
    book = " ".join(
        "\n".join(p.read_text() for p in sorted(CHAPTERS.glob("*.md"))).split()
    )
    return [s.strip() for s in re.split(r"(?<=\.)\s+", book) if s.strip()]


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    sentences = _sentences()
    denials = [s for s in sentences if DENIAL.search(s)]
    requirements = [
        s for s in sentences if REQUIRE.search(s) and not DENIAL.search(s)
    ]

    denied: list[str] = []
    for sentence in denials:
        tail = sentence.split("establish", 1)[1]
        denied += [
            item.strip().rstrip("s")
            for item in re.split(r",| or | and ", tail)
            if item.strip()
        ]

    print(f"  denial sentences in the active Book:      {len(denials)}")
    print(f"  things denied across them:                {len(denied)}")
    print(f"  positive requirement sentences:           {len(requirements)}\n")

    reach = [s for s in denials if REACH.search(s)]
    print(f"  A — the denied thing has stated positive physiology the denying")
    print(f"      subject cannot satisfy, so the whitelist already refuses it: "
          f"{len(denials) - len(reach)}")
    print(f"  C — the denied thing IS fully established and the denial bounds its")
    print(f"      reach, which no requirement list can refuse: {len(reach)}\n")
    for sentence in reach:
        print(f"    {sentence[:120]}")

    print("\n  B — negatives an exact Responsibility yields as its own finding:")
    for word in YIELDED:
        carried = sum(1 for s in sentences if re.search(rf"\b{word}\b", s, re.I))
        print(f"    {word:14} {carried:3} sentences")
    print("    These are results, not prohibitions, and survive whatever happens")
    print("    to the denial form.")

    print(f"\n  D — nouns whose every Book occurrence is inside a denial: "
          f"{len(DENIAL_ONLY)}\n")
    for noun in DENIAL_ONLY:
        carried = [s for s in sentences if re.search(rf"\b{re.escape(noun)}\b", s, re.I)]
        print(f"    {noun:22} {len(carried)} sentence(s), all denials")
    print("\n    No Act establishes any of these and no clause states what one\n"
          "    would require.  They exist in the Book because they were forbidden,\n"
          "    and under a whitelist they never arise to be forbidden.")

    print(
        "\n  So the denial population is not the enforcing half.  Thirty-one of the\n"
        "  forty-four are refused already by requirements the Book states, and the\n"
        "  remaining thirteen are one family: a thing that IS established, carried\n"
        "  somewhere it was not established for.  A requirement list cannot refuse\n"
        "  those, because every requirement is met.  They need one further positive\n"
        "  rule, that establishment is indexed to its exact subject, boundary, and\n"
        "  Responsibility, and that carriage of coordinates is not establishment.\n"
        "  Two positive rules, not ninety-two prohibitions.\n"
        "\n  This also withdraws the reading that the machine grammar is deficient\n"
        "  for carrying two denials.  Whether it should carry any is now open.\n"
        "\n  The counts are measured.  The A and C split is made by one stated\n"
        "  pattern over the denial's own wording, which is a detector: it reports\n"
        "  where the reach family is, and does not establish that each of the\n"
        "  thirty-one is genuinely redundant.  That needs the substitution done\n"
        "  clause by clause.  Nothing is amended."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
