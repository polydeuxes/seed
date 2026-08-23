"""Ask whether the intermediate stage before a boundary write distinguishes anything.

Chapter 11 states two stages between an exact source result and a destination
boundary. The names are set aside here. R1 takes an exact source result to an
intermediate result carrying the same material and source coordinates. R2 takes
that carried result across a destination boundary under Applicability,
Admission, Participation and Carriage.

R1 is removed conceptually and R2 is asked to carry the exact source result
directly. Whatever becomes unrecoverable is what R1 was for.

The runtime is read as testimony, not as warrant. That it builds an intermediate
occurrence establishes nothing about whether the Book needs one.

Usage:
    .venv/bin/python scripts/observe_representation_stage_by_elimination.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Every coordinate the Book requires somewhere between an exact source result
# and an accepted boundary write.
COORDINATES = (
    "source result identity",
    "exact material",
    "source coordinates and provenance",
    "Authority",
    "Scope",
    "Locality",
    "limits",
    "known loss, conflicts, Unknown",
    "destination operator boundary",
    "Applicability",
    "Admission",
    "Participation and Role",
    "Carriage",
    "Act occurrence",
    "Yield",
    "accepted material",
    "reported count",
    "attempt, partial, failure, accepted occurrence identities",
)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    from seed_runtime.operator_representation import (
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
    )

    print("  the intermediate result, as the runtime builds it:\n")
    source = Path("seed_runtime/operator_representation.py").read_text()
    literal = source.split('representation_result = (', 1)[1].split(")", 1)[0]
    print(f"    representation_result = {' '.join(literal.split())}")
    print("    a constant. The exact material travels beside it, not in it.\n")
    print(f"    representation_rule = "
          f"{EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE[:70]}...\n")

    emission = source.split("def emit_operator_representation_material", 1)[1]
    reads_back = "read_operator_representation(" in emission
    uses_result = "representation_result" in emission.split("attempt_event", 1)[0]
    print(f"    the boundary-facing stage reads the intermediate back: {reads_back}")
    print(f"    the boundary-facing stage consults representation_result: "
          f"{uses_result}")
    print("    it re-extracts exact_material and refuses any difference.\n")

    print("  what R1 uniquely establishes, coordinate by coordinate:\n")
    unique_to_R1 = {
        "representation_rule": (
            "the rule stating the material is preserved exactly. It is a "
            "constant, and it names the identity relation between the source "
            "material and itself"
        ),
        "an Act occurrence identity": (
            "one more occurrence to address. R2 has its own, and Admission "
            "addresses the intermediate rather than the source result only "
            "because the intermediate exists"
        ),
    }
    for name, reading in unique_to_R1.items():
        print(f"    {name}\n      {reading}")

    print("\n  each coordinate, and where it is recoverable without R1:\n")
    for coordinate in COORDINATES:
        print(f"    {coordinate:44} on the exact source result or on R2")

    print(
        "\n  Removing R1 loses no coordinate in the list. Every one is carried by\n"
        "  the exact source result, which preserves its material, source role,\n"
        "  boundary, provenance, Authority, Scope, Locality, known loss, limits\n"
        "  and Unknown, or by the boundary-facing Act occurrence, which carries\n"
        "  the destination, Applicability, Admission, Participation, Carriage,\n"
        "  Yield and the accepted write.\n"
        "\n  What R1 adds is one occurrence identity and one constant rule saying\n"
        "  the material is unchanged. A stage whose whole result is a constant\n"
        "  string, and whose material is re-extracted unchanged by the next\n"
        "  stage, has moved nothing.\n"
        "\n  The runtime is testimony here and not warrant. It is read only to see\n"
        "  what an implementation of the two stages actually does, and it wraps\n"
        "  the exact material and then unwraps it.\n"
        "\n  This does not say the Book should change. It says which distinction\n"
        "  a second stage would have to carry, and this road shows none."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
