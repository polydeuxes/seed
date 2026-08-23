"""Freeze and render recurrent Unicode-scalar aperture physiologies.

This reads no Book, machine grammar, dictionary, translation, expected word,
or human grammar category.  It also compares only population counts with the
independent byte-aperture artifact, exposing where UTF-8 transport positions
created findings that scalar positions do not carry.

Usage:
    .venv/bin/python scripts/report_scalar_aperture_physiologies.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path


SCALAR_ARTIFACT = Path("/tmp/seed_open_world_scalar_apertures_blind.json")
BYTE_ARTIFACT = Path("/tmp/seed_open_world_apertures_blind.json")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _material(source: dict, reference: str) -> str:
    return bytes.fromhex(source["materials"][reference]["utf8_hex"]).decode("utf-8")


def _minimal_change(first: str, second: str) -> tuple[str, str]:
    prefix = 0
    while (
        prefix < len(first)
        and prefix < len(second)
        and first[prefix] == second[prefix]
    ):
        prefix += 1
    suffix = 0
    while (
        suffix < len(first) - prefix
        and suffix < len(second) - prefix
        and first[len(first) - suffix - 1] == second[len(second) - suffix - 1]
    ):
        suffix += 1
    first_end = len(first) - suffix if suffix else len(first)
    second_end = len(second) - suffix if suffix else len(second)
    return tuple(sorted((first[prefix:first_end], second[prefix:second_end])))


def _projection(artifact: dict) -> dict:
    sources = []
    for source in artifact["sources"]:
        delimiters = []
        used_materials = set()
        for delimiter in source["delimiters"]:
            frames = delimiter["recurrent_substitution_frames"]
            if not frames:
                continue
            for frame in frames:
                used_materials.update(
                    (frame["left_material"], frame["right_material"])
                )
                used_materials.update(
                    occupant["material"] for occupant in frame["occupants"]
                )
            delimiters.append(
                {
                    "separator_scalar": delimiter["separator_scalar"],
                    "separator_codepoint": delimiter["separator_codepoint"],
                    "occurrence_count": delimiter["occurrence_count"],
                    "span_count": delimiter["span_count"],
                    "recurrent_substitution_frames": frames,
                }
            )
        sources.append(
            {
                "source": source["source"],
                "population": source["population"],
                "first_line": source["first_line"],
                "line_count": source["line_count"],
                "byte_count": source["byte_count"],
                "scalar_count": source["scalar_count"],
                "material_sha256": source["material_sha256"],
                "scope_count": source["scope_count"],
                "enumerated_separator_count": source["enumerated_separator_count"],
                "materials": {
                    reference: source["materials"][reference]
                    for reference in sorted(used_materials)
                },
                "delimiters": delimiters,
            }
        )
    return {
        "observer_choices": {
            key: value
            for key, value in artifact["observer_choices"].items()
            if key not in {"substitution"}
        },
        "sources": sources,
    }


def _count_frames(source: dict) -> int:
    return sum(
        len(delimiter["recurrent_substitution_frames"])
        for delimiter in source["delimiters"]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=SCALAR_ARTIFACT)
    parser.add_argument("--byte-artifact", type=Path, default=BYTE_ARTIFACT)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    scalar = json.loads(arguments.artifact.read_text(encoding="utf-8"))
    projection = _projection(scalar)
    encoded = _canonical(projection)
    if arguments.output is not None:
        arguments.output.write_bytes(encoded)
    print(f"  source-enumerated scalar apertures: {sum(source['enumerated_separator_count'] for source in projection['sources'])}")
    print(f"  recurrent scalar substitution frames: {sum(_count_frames(source) for source in projection['sources'])}")
    print(f"  findings sha256: {sha256(encoded).hexdigest()}\n")

    if arguments.byte_artifact.is_file():
        byte = json.loads(arguments.byte_artifact.read_text(encoding="utf-8"))
        byte_by_source = {source["source"]: source for source in byte["sources"]}
        print("  transport-byte findings versus Unicode-scalar findings:\n")
        for source in projection["sources"]:
            byte_count = _count_frames(byte_by_source[source["source"]])
            scalar_count = _count_frames(source)
            if byte_count or scalar_count:
                print(
                    f"    {source['source']:48} {byte_count:4} -> {scalar_count:4}"
                )
        print()

    shapes: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    changes: dict[tuple[tuple[str, str], ...], list[int]] = defaultdict(list)
    number = 0
    for source in projection["sources"]:
        for delimiter in source["delimiters"]:
            separator = delimiter["separator_scalar"]
            for frame in delimiter["recurrent_substitution_frames"]:
                number += 1
                left = _material(source, frame["left_material"])
                right = _material(source, frame["right_material"])
                occupants = tuple(
                    _material(source, occupant["material"])
                    for occupant in frame["occupants"]
                )
                shapes[(separator, left, right)].append(number)
                changes[
                    tuple(
                        sorted(
                            _minimal_change(first, second)
                            for first_position, first in enumerate(occupants)
                            for second in occupants[first_position + 1 :]
                        )
                    )
                ].append(number)
                print(f"  F{number}  {source['source']}")
                print(
                    f"    {left!r} <{separator!r}> _ <{separator!r}> {right!r}"
                )
                for occupant in frame["occupants"]:
                    found = _material(source, occupant["material"])
                    ranges = tuple(
                        tuple(value) for value in occupant["source_scalar_ranges"]
                    )
                    print(f"      {found!r}  count={len(ranges)}  ranges={ranges}")
                print()

    print("  repeated exact frame shapes:\n")
    repeated = 0
    for shape, numbers in sorted(shapes.items(), key=lambda item: (-len(item[1]), item[0])):
        if len(numbers) < 2:
            continue
        repeated += 1
        separator, left, right = shape
        print(
            f"    {left!r} <{separator!r}> _ <{separator!r}> {right!r}: "
            + ", ".join(f"F{number}" for number in numbers)
        )
    if not repeated:
        print("    none")

    print("\n  repeated exact minimal occupant changes:\n")
    repeated = 0
    for change, numbers in sorted(changes.items(), key=lambda item: (-len(item[1]), item[0])):
        if len(numbers) < 2:
            continue
        repeated += 1
        print("    " + ", ".join(f"F{number}" for number in numbers))
        for first, second in change:
            print(f"      {first!r} <-> {second!r}")
    if not repeated:
        print("    none")

    print(
        "\n  No translation or language name was read. Exact frame equality and\n"
        "  minimal source-material change are the only cross-finding relations."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
