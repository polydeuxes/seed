"""Ask where emission stops, using two external witnesses as testimony.

07.Emission says the destination is an operator boundary and that five things
are separate occurrences. Two material witnesses address that boundary from
outside, and neither is constitutional warrant: each is testimony about one
external invocation.

The keystroke witness offers two exact materials to a PTY. The style witness
offers two exact materials to an isolated terminal and asks it for two different
result surfaces. Both say something about what full acceptance at a boundary
does and does not settle.

The emission road is then read for its occurrence identities, because the count
of occurrences is a question about identities and never about how many event
kinds an implementation appends.

Usage:
    .venv/bin/python scripts/observe_where_emission_stops.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    keystroke = (ROOT / "material_witnesses/test_terminal_keystroke.py").read_text()
    style = (ROOT / "material_witnesses/test_terminal_style.py").read_text()
    emission = (ROOT / "seed_runtime/operator_representation.py").read_text().split(
        "def emit_operator_representation_material", 1
    )[1]

    print("  the keystroke witness, one PTY boundary\n")
    print("    offered   b'printf 012x\\x7f3\\rexit\\r'   18 bytes")
    print("    offered   b'printf 0123\\rexit\\r'        17 bytes")
    accepted = "input_boundary_accepted_byte_count" in keystroke
    print(f"    both accepted at their full byte count: {accepted}")
    print(f"    stdout differs between them: "
          f"{'invocations[0].stdout_bytes != invocations[1].stdout_bytes' in keystroke}")
    print("    one DEL byte, fully accepted, and the external result is not the same.\n")
    print("    So full acceptance settles what the boundary took, and settles")
    print("    nothing about what follows from it.\n")

    print("  the style witness, one terminal boundary asked twice\n")
    print("    offered   b'Seed material witness\\n'")
    print("    offered   the same words carrying SGR colour and bold")
    print(f"    plain cell results equal:  "
          f"{'plain_results[0].exact_material == plain_results[1].exact_material' in style}")
    print(f"    styled results differ:     "
          f"{'styled_results[0].exact_material != styled_results[1].exact_material' in style}")
    print("    One destination, two exact result surfaces from the same bytes.")
    print("    Which result exists depends on what was separately acquired from")
    print("    the terminal, not on what was emitted to it.\n")

    print("  the emission road, by identity rather than by event kind\n")
    for name in ("emission_act_identity", "act_occurrence_identity", "result_identity"):
        from_admission = f'{name} = admission[' in emission
        print(f"    {name:26} taken from the Admission: {from_admission}")
    minted = emission.count("new_identity(")
    print(f"\n    identities minted anywhere in the emission road: {minted}")
    failure = emission.split("boundary_failure", 1)
    print(f"    the failure road mints its own Act, occurrence and result: "
          f"{'operator_representation_boundary_failure_act' in emission}")
    kinds = sorted(
        {word.rstrip(",") for word in emission.split() if word.endswith("_KIND,")}
    )
    print(f"    event kinds appended along the road: {len(kinds)}")

    print(
        "\n  So of the five the chapter calls separate occurrences, the road\n"
        "  carries two. Attempt, accepted write and emission share one Act\n"
        "  occurrence identity, taken from the Admission, one result identity and\n"
        "  one Yield; the accepted count is a coordinate of that one result. A\n"
        "  failure is a separate occurrence and mints its own Act, occurrence and\n"
        "  result, and a partial write is reported inside it, since the boundary\n"
        "  reporting fewer bytes than were offered is what raises it.\n"
        "\n  Where emission stops, on this evidence: at the boundary that reports.\n"
        "  Seed offers exact material to one addressed boundary and receives one\n"
        "  count. Everything the keystroke and style witnesses show past that\n"
        "  point, a PTY editing a line, a terminal interpreting control bytes,\n"
        "  cells, colour, anything an operator would see, is produced by further\n"
        "  external occurrences and reaches Seed only by being acquired.\n"
        "\n  That is a question about the wording `destination operator boundary`.\n"
        "  The boundary the road addresses is the one it writes to and hears back\n"
        "  from. The operator, in the style witness, is several external\n"
        "  occurrences downstream of it.\n"
        "\n  Both witnesses are testimony about their own external invocations and\n"
        "  neither establishes any Seed Act, Authority, Admission or emission.\n"
        "  The identity readings are read from the road's source rather than run.\n"
        "  Nothing is amended."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
