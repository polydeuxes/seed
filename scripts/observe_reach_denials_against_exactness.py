"""Test the reach denials against exactness alone, with no new rule.

The previous pass proposed one further positive rule — that establishment is
indexed to its exact subject, boundary and Responsibility — to cover thirteen
denials the requirement lists could not refuse.  That is a universal rule minted
to replace prohibitions, which is the same move as minting an Act where a clause
names none.  Withdrawn, and tested instead against what the Book already states.

The sharper question is not whether establishment has bounded reach.  It is
whether a thing's own exact coordinates already make it not the thing another
Responsibility requires.  Authority carries its Responsibility.  Scope bounds
one exact Responsibility.  Standing is Standing for one exact subject.  Where
that holds, the other Responsibility does not hold a forbidden copy; it holds
nothing.

Each of the thirteen is read for the one coordinate that would settle it, and
the answer comes from the denied thing's own stated physiology.

Usage:
    .venv/bin/python scripts/observe_reach_denials_against_exactness.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CHAPTERS = Path(__file__).resolve().parents[1] / "book_of_seed" / "chapters"

# denied thing -> (its stated physiology, the coordinate that settles reach)
PHYSIOLOGY = {
    "Authority": (
        "carries one exact source, Responsibility, subject, Act, occurrence, "
        "result, Scope, and limits",
        "Responsibility",
    ),
    "Scope": (
        "bounds the subjects, relations, Acts, occurrences, results, Localities, "
        "and limits addressed by one exact Responsibility",
        "Responsibility",
    ),
    "Standing": (
        "Standing for one exact subject requires an exact Responsibility, Act "
        "occurrence, Yield, Authority, Scope, limits, and result for that subject",
        "subject",
    ),
    "Participation": (
        "requires its own relation occurrence and the exact applicable "
        "subject-to-Act position",
        "subject-to-Act position",
    ),
    "Applicability": (
        "carries one exact subject-to-Act position; its responsible occurrence "
        "carries the subject, Act, Authority, Scope, Locality, and limits",
        "subject-to-Act position",
    ),
    "Locality relation": (
        "requires its relation occurrence, Responsibility, Act, Authority, "
        "Scope, limits, and Unknown",
        "Responsibility",
    ),
    "Admission": (
        "carries an exact occurrence prior to Participation",
        None,
    ),
    "completion": (
        "stated only in chapter 12, which carries no clause identifier",
        None,
    ),
}

# denial -> (denied thing, disposition, reading)
READING = {
    "Material carrying exact Authority coordinates establishes no other Authority": (
        "Authority", "removed by existing positive grammar",
        "an Authority carries its Responsibility, so the Authority established "
        "for one Responsibility is not the Authority another requires. Carriage "
        "of the coordinates also yields no occurrence, and an Authority requires "
        "one",
    ),
    "One Scope establishes no Scope for another Responsibility": (
        "Scope", "removed by existing positive grammar",
        "a Scope bounds what one exact Responsibility addresses, so it is not a "
        "Scope for another; the second Responsibility holds no forbidden copy, "
        "it holds nothing",
    ),
    "Carriage of exact Authority or Scope coordinates establishes no Authority or Scope at another boundary": (
        "Authority", "removed by existing positive grammar",
        "same as the two above, and carriage is a relation from content to an "
        "Act occurrence, which yields neither an Authority nor a Scope",
    ),
    "Support establishes no Participation, result, or Standing beyond exact bounds": (
        "Participation", "removed by existing positive grammar",
        "Participation requires its own relation occurrence and an applicable "
        "subject-to-Act position, and a support relation occurrence is neither",
    ),
    "Applicability establishes no Admission, Participation, Act occurrence, result, or Standing for a result": (
        "Participation", "removed by existing positive grammar",
        "an Applicability occurrence is not a Participation relation occurrence, "
        "and Standing for a result would need that result as its exact subject",
    ),
    "It establishes no copy of Standing and no Applicability, Participation, Compare result, or relation beyond its Scope": (
        "Standing", "removed by existing positive grammar",
        "Standing is Standing for one exact subject and requires a Responsibility, "
        "Act occurrence and Yield; a preserved boundary reference is none of those. "
        "`copy of Standing` has no positive physiology anywhere, so nothing could "
        "establish one",
    ),
    "It establishes no copy of addressed Standing": (
        "Standing", "removed by existing positive grammar",
        "as above; the noun exists only in its own denial",
    ),
    "The reference establishes no copy of Standing and establishes no Locality relation, Applicability, Participation, Compare result, movement, or Authority for another Act": (
        "Standing", "removed by existing positive grammar",
        "a reference satisfies none of these physiologies, and each names its own "
        "required occurrence",
    ),
    "That provenance establishes no Applicability, Participation, or operator Standing copy": (
        "Applicability", "removed by existing positive grammar",
        "provenance is an ordered reference path and carries no responsible "
        "occurrence, which every one of the three requires",
    ),
    "The result as one coordinate of that Responsibility branch establishes no Standing for the result as another subject, and no later Standing occurrence": (
        "Standing", "removed by existing positive grammar",
        "Standing is for one exact subject, so Standing for subject S is already "
        "not Standing for subject R. This is 01.Standing.A.1, which I drafted, "
        "and under the whitelist it states what exactness states",
    ),
    "An exhaustive bounded subject set for one Responsibility establishes no order, Applicability, or completion for another Responsibility": (
        "completion", "Unknown",
        "the Applicability half is removed by exactness. Order and completion "
        "cannot be tested: completion's only physiology is in chapter 12, which "
        "carries no clause identifier, and order has none anywhere",
    ),
    "The exhaustive bounded subject set establishes no order for another Responsibility": (
        "completion", "Unknown",
        "order has no stated physiology in the Book, so there is nothing to "
        "compare the denial against",
    ),
    "Admission for one boundary or Act establishes no Admission for another": (
        "Admission", "exposes a genuinely missing positive distinction",
        "Admission's whole stated physiology is that it carries an exact "
        "occurrence prior to Participation. It carries no boundary and no Act. "
        "So nothing in an Admission's own identity says which boundary admitted "
        "what, and the denial is the only thing standing between one Admission "
        "and every other boundary. Exactness cannot remove this one because the "
        "Book never made Admission exact",
    ),
}


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    book = " ".join(
        "\n".join(p.read_text() for p in sorted(CHAPTERS.glob("*.md"))).split()
    )
    sentences = [s.strip() for s in re.split(r"(?<=\.)\s+", book) if s.strip()]

    print("  Withdrawn: the proposed rule that establishment is indexed to its")
    print("  exact subject, boundary and Responsibility. It is a universal rule")
    print("  minted to replace prohibitions, and the Book already states the")
    print("  coordinates it would have generalised.\n")

    print("  what each denied thing's own physiology carries:\n")
    for thing, (stated, settles) in PHYSIOLOGY.items():
        print(f"    {thing}")
        print(f"      {stated}")
        print(f"      settles reach by its own {settles}" if settles
              else "      carries NO coordinate that settles reach")
    print()

    for name in (
        "removed by existing positive grammar",
        "exposes a genuinely missing positive distinction",
        "Unknown",
    ):
        rows = {k: v for k, v in READING.items() if v[1] == name}
        print(f"  {name}: {len(rows)}\n")
        for denial, (_thing, _d, reading) in rows.items():
            print(f"    {denial[:110]}")
            print(f"      {reading}\n")

    print("  nouns occurring in the Book only inside a denial, as deletion")
    print("  candidates rather than nouns needing a negative clause kept for them:\n")
    for noun in (
        "revision", "copy of Standing", "source relation", "erasure", "mutation",
        "copying", "recurrence", "same-content finding", "collective subject",
        "collective relation", "renewed occurrence",
    ):
        carried = [s for s in sentences if re.search(rf"\b{re.escape(noun)}\b", s, re.I)]
        print(f"    {noun:22} {len(carried)} sentence(s), no Act establishes it, "
              f"no clause states what one would require")
    print("\n    Removing the denial leaves no positive physiology anywhere for any\n"
          "    of them, so under a whitelist there is nothing to forbid. That is\n"
          "    the deletion case, and it is the denial that was keeping the noun.\n")

    print("  the six words bundled as negatives last pass, recovered separately:\n")
    for word in ("inapplicable", "conflicting", "known loss", "conflicts", "limits", "Unknown"):
        carried = [s for s in sentences if re.search(rf"\b{word}\b", s, re.I)]
        listed = sum(
            1 for s in carried if re.search(rf"(,|and) {word}\b", s, re.I)
        )
        print(f"    {word:14} {len(carried):3} sentences, {listed:3} inside a "
              f"carried-coordinate list")
    print(
        "\n    inapplicable and conflicting occur once each, in the one sentence\n"
        "    giving Applicability's determined positions. They are findings.\n"
        "    known loss, conflicts and limits occur only inside preserved-coordinate\n"
        "    lists. They are carried coordinates and were wrongly bundled with the\n"
        "    findings last pass. Unknown is in both places and so is two things\n"
        "    under one word."
    )

    print(
        "\n  Ten of the thirteen fall to exactness with no new rule. Two are\n"
        "  Unknown for want of a physiology to compare against. One does not\n"
        "  fall, and it is the useful result: Admission carries an occurrence and\n"
        "  no boundary, so its own identity cannot say which boundary admitted\n"
        "  what. That denial is load-bearing because the positive grammar is\n"
        "  incomplete, and the repair is a coordinate on Admission rather than a\n"
        "  prohibition around it.\n"
        "\n  Each disposition is a reading of one denial against one recovered\n"
        "  physiology, recorded so it can be disagreed with at the row that\n"
        "  states it. Nothing is amended."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
