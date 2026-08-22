"""Read each candidate word against each anonymous relation physiology.

Two physiologies on one road carry no name the grammar states.  Nine candidate
words were brought from preserved usage.  Each word is read against each
physiology, eighteen readings, and no word is chosen in advance.

The physiology is fixed.  A dictionary definition is testimony about how English
may name a relation, never authority over what the relation is.  A word survives
only where its ordinary relational distinction neither erases a distinction the
physiology carries nor adds one it does not.

Every disposition below is a reading, made by whoever wrote this file, of a
recovered definition against recovered coordinates.  The coordinates and the
definitions are measured; the reading between them is not, and is recorded so it
can be disagreed with rather than taken.

Usage:
    .venv/bin/python scripts/compare_relation_words_against_physiology.py
"""

from __future__ import annotations

import argparse

# Recovered by scripts/observe_unstated_relation_signatures.py, one road.
PHYSIOLOGY = {
    "R1": {
        "occurrences": 6,
        "first subject names": "an addressed coordinate reference and a result reference",
        "second subject names": "an Act, its occurrence, the exact Act, and a result",
        "the mapping also carries": (
            "a completeness boundary, a Locality, a responsibility assignment "
            "reference, and a source material acquisition occurrence"
        ),
        "carries no": "through, and no relation occurrence identity",
    },
    "R2": {
        "occurrences": 4,
        "first subject names": "one recorded occurrence",
        "second subject names": "an Act occurrence, the exact Act, and a measurement Act",
        "the mapping also carries": "a through",
        "carries no": (
            "completeness boundary, Locality, responsibility assignment, result, "
            "and no relation occurrence identity"
        ),
    },
}

# Recovered from corpus/webster_dictionary.txt.
SENSE = {
    "of": "from, or out from; that from which anything proceeds; possession; the material of which composed",
    "in": "situation or place with respect to surrounding, encompassment; a whole which includes the part",
    "to": "approach and arrival, motion made in the direction of a thing and attaining it",
    "by": "in the neighborhood of; near to, while passing; adjacent dimensions",
    "for": "in consideration of, in view of, or with reference to which anything is done; the antecedent cause or occasion of an action; the remoter and indirect object of an act",
    "with": "nearness, proximity, association, connection",
    "on": "situation or condition with respect to contact or support beneath",
    "from": "out of the neighborhood of; lessening or losing proximity to; leaving behind",
    "under": "below or lower, with the idea of being covered; figuratively, under thy conduct",
}

# reading -> (disposition, what the definition supports, what it contradicts,
#             what it leaves undecided)
READING = {
    ("of", "R1"): ("refused", "", "names the second as what the first proceeds from, and the first is what the Act addresses, not its source", "possession, which neither carries"),
    ("of", "R2"): ("refused", "", "reverses the direction: the recorded occurrence does not proceed from the Act", "possession"),
    ("in", "R1"): ("refused", "boundedness, which R1 carries as a completeness boundary", "puts the first inside the second, and the Act does not contain the references", "which boundary is meant"),
    ("in", "R2"): ("refused", "", "adds containment, and R2 carries no boundary of any kind", ""),
    ("to", "R1"): ("survives", "direction from the references toward the Act, and arrival at it", "", "the completeness boundary, the Locality, and the result"),
    ("to", "R2"): ("survives", "direction from the recorded occurrence toward the Act occurrence, and arrival", "", "the through"),
    ("by", "R1"): ("refused", "", "names neighbourhood, and co-presence establishes no relation", "agency, which the recovered senses do not carry"),
    ("by", "R2"): ("refused", "", "names neighbourhood rather than direction", "agency"),
    ("for", "R1"): ("survives", "the remoter and indirect object of an act, which is what the addressed references are to the Act", "", "the completeness boundary and the responsibility assignment"),
    ("for", "R2"): ("survives", "that in view of which the Act is done", "", "the through"),
    ("with", "R1"): ("refused", "", "association is not ordered, and R1 runs from a first subject to a second", ""),
    ("with", "R2"): ("refused", "", "association is not ordered, and R2 runs from a first subject to a second", ""),
    ("on", "R1"): ("refused", "", "contact and support beneath, which neither subject carries", ""),
    ("on", "R2"): ("refused", "", "contact and support beneath, which neither subject carries", ""),
    ("from", "R1"): ("refused", "", "direction away from, and R1 runs toward the Act", ""),
    ("from", "R2"): ("refused", "", "direction away from, and R2 runs toward the Act occurrence", ""),
    ("under", "R1"): ("survives", "being governed, which R1 carries as a responsibility assignment reference and a completeness boundary", "", "whether the covering is the Act or the boundary"),
    ("under", "R2"): ("refused", "", "adds governance, and R2 carries no assignment, boundary, or Locality", ""),
}


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    for name, coordinates in PHYSIOLOGY.items():
        print(f"  {name}, {coordinates['occurrences']} occurrences")
        for key, value in coordinates.items():
            if key != "occurrences":
                print(f"    {key}: {value}")
        print()

    for name in PHYSIOLOGY:
        print(f"  read against {name}:\n")
        for word in SENSE:
            disposition, supports, contradicts, undecided = READING[(word, name)]
            print(f"    {disposition:9} {word}")
            if supports:
                print(f"      supports:    {supports}")
            if contradicts:
                print(f"      contradicts: {contradicts}")
            if undecided:
                print(f"      undecided:   {undecided}")
        print()

    for name in PHYSIOLOGY:
        surviving = [
            word for word in SENSE if READING[(word, name)][0] == "survives"
        ]
        print(f"  surviving for {name}: {', '.join(surviving) or 'none'}")

    print(
        "\n  Ties are preserved.  Nothing here forces one word per physiology,\n"
        "  and a word surviving both is not thereby the same word for both.\n"
        "\n  The coordinates are measured and the definitions are recovered.  The\n"
        "  reading between them is this file's and is recorded rather than\n"
        "  asserted, so a disposition can be disagreed with at the line that\n"
        "  states it."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
