"""Set the two boundary crossings of one round trip beside each other.

The last pass read the outbound crossing only, and asked where emission stops.
Rotating the boundary asks a different question: Seed emitting exact material is
the same event as something outside acquiring it, and the external function
returning its result is the same event as Seed acquiring that.

One round trip carries two crossings. They are set beside each other here by
coordinate, with the names emission and acquisition set aside, to see whether
two physiologies are stated or one physiology is stated twice from opposite
sides.

The witnesses are testimony about their own external invocations. That an
implementation carries a coordinate establishes nothing about what the Book
requires.

Usage:
    .venv/bin/python scripts/observe_boundary_crossing_symmetry.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[1]

# coordinate -> (outbound crossing, inbound crossing)
CROSSING = (
    ("exact material", "the material Seed offers", "the material Seed takes"),
    ("exact boundary", "the addressed write boundary",
     "the addressed source boundary"),
    ("Producer side", "this Seed", "the external implementation"),
    ("Consumer side", "the external boundary", "this Seed"),
    ("what the Consumer reports of its own consumption",
     "input_boundary_accepted_byte_count, an int the boundary returns",
     "exact_bytes, what Seed records itself as having taken"),
    ("provenance", "the source_reference the offered material carries",
     "provenance_occurrence_references on the acquisition"),
    ("known loss", "carried by the emission Responsibility",
     "carried by the acquisition"),
    ("the crossing occurrence",
     "the emission Act occurrence, taken from the Admission",
     "the acquisition Act occurrence"),
)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    invocation = (ROOT / "scripts/compiled_material_invocation.py").read_text()
    body = invocation.split("class MaterialInvocationOccurrence:", 1)[1].split(
        "def __post_init__", 1
    )[0]
    fields = [
        line.split(":", 1)[0].strip()
        for line in body.split("\n")
        if ":" in line and not line.strip().startswith("#") and line.startswith("    ")
    ]
    outbound = [
        f for f in fields
        if f in ("exact_material", "boundary_identity", "source_reference",
                 "input_boundary_accepted_byte_count", "implementation_function",
                 "invocation_position", "time_limit_second_count",
                 "material_byte_count_limit")
    ]
    inbound = [
        f for f in fields
        if f in ("returned", "returncode", "stdout_bytes", "stderr_bytes",
                 "time_limit_reached", "stdout_byte_count_limit_reached",
                 "stderr_byte_count_limit_reached")
    ]
    print("  One external invocation occurrence carries both crossings:\n")
    print(f"    outbound, Seed to the boundary  ({len(outbound)} coordinates)")
    for field in outbound:
        print(f"      {field}")
    print(f"\n    inbound, the boundary back to Seed  ({len(inbound)} coordinates)")
    for field in inbound:
        print(f"      {field}")

    print("\n  the two crossings by coordinate:\n")
    for name, out, back in CROSSING:
        print(f"    {name}")
        print(f"      outbound: {out}")
        print(f"      inbound:  {back}")

    print(
        "\n  The crossings carry the same coordinates with Producer and Consumer\n"
        "  exchanged. On both, the side that takes the material is the side that\n"
        "  reports what it took: outbound that report is an int the external\n"
        "  boundary returns, and inbound it is the exact bytes Seed records.\n"
        "\n  That places the accepted count. It is not a downstream effect and it\n"
        "  is not something this Seed establishes. It is the Consumer's testimony\n"
        "  about its own consumption, arriving across the boundary, and the\n"
        "  emission result carries it. So one coordinate of what the road calls\n"
        "  Seed's emission result was acquired rather than produced.\n"
        "\n  What the outbound road lacks is the whole inbound half. The invocation\n"
        "  occurrence carries a result from the external side; the emission road\n"
        "  carries a count and nothing else. Emission is the crossing where the\n"
        "  only thing acquired back is the Consumer's report.\n"
        "\n  Role turnover is visible between the two. The external boundary is\n"
        "  Consumer of the offered material, and the external implementation is\n"
        "  Producer of the result Seed later acquires. The keystroke witness shows\n"
        "  these are not one act: both inputs are consumed whole and the produced\n"
        "  results differ, so consuming did not produce. A separate external\n"
        "  Responsibility stands between them, and Seed holds no coordinate of it.\n"
        "\n  This does not name anything. It reports that one physiology appears\n"
        "  twice with its roles exchanged, and that the outbound instance is the\n"
        "  poorer of the two. Whether emission and acquisition are two kinds or\n"
        "  one kind read from two sides is not settled by a symmetry; identical\n"
        "  shape is not identical Responsibility.\n"
        "\n  Bounded to two witnesses and one road. Nothing is amended."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
