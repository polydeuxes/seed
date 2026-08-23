"""Render only the recurrent substitution physiologies of a blind artifact.

No Book, machine grammar, dictionary, expected word, or human grammar category
is read.  Wall timings are excluded from the findings projection so its digest
depends only on exact inputs, observer coordinates, and recovered findings.

Usage:
    .venv/bin/python scripts/report_recurrent_aperture_physiologies.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path


ARTIFACT = Path("/tmp/seed_open_world_apertures_blind.json")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _material(source: dict, reference: str) -> bytes:
    return bytes.fromhex(source["materials"][reference]["hex"])


def _render(value: bytes) -> str:
    return repr(value.decode("utf-8", "backslashreplace"))


def _minimal_change(first: bytes, second: bytes) -> tuple[bytes, bytes]:
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
    changed = (first[prefix:first_end], second[prefix:second_end])
    return tuple(sorted(changed))


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
                used_materials.add(frame["left_material"])
                used_materials.add(frame["right_material"])
                used_materials.update(
                    occupant["material"] for occupant in frame["occupants"]
                )
            delimiters.append(
                {
                    "separator_byte": delimiter["separator_byte"],
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
            "source_windows": artifact["observer_choices"]["source_windows"],
            "scope_division": artifact["observer_choices"]["scope_division"],
            "aperture_resolution": artifact["observer_choices"]["aperture_resolution"],
            "recurrent_substitution": artifact["observer_choices"][
                "recurrent_substitution"
            ],
        },
        "sources": sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=ARTIFACT)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    artifact = json.loads(arguments.artifact.read_text(encoding="utf-8"))
    projection = _projection(artifact)
    encoded = _canonical(projection)
    if arguments.output is not None:
        arguments.output.write_bytes(encoded)

    print(f"  source-enumerated apertures: {sum(source['enumerated_separator_count'] for source in projection['sources'])}")
    print(
        "  recurrent substitution frames: "
        f"{sum(len(delimiter['recurrent_substitution_frames']) for source in projection['sources'] for delimiter in source['delimiters'])}"
    )
    print(f"  findings sha256: {sha256(encoded).hexdigest()}\n")

    exact_shapes: dict[tuple[int, bytes, bytes], list[tuple[str, dict]]] = defaultdict(list)
    frames_by_source: dict[str, list[dict]] = defaultdict(list)
    change_signatures: dict[tuple[tuple[bytes, bytes], ...], list[int]] = defaultdict(list)
    number = 0
    for source in projection["sources"]:
        for delimiter in source["delimiters"]:
            separator = delimiter["separator_byte"]
            for frame in delimiter["recurrent_substitution_frames"]:
                number += 1
                left = _material(source, frame["left_material"])
                right = _material(source, frame["right_material"])
                exact_shapes[(separator, left, right)].append((source["source"], frame))
                full_occurrences = []
                print(f"  F{number}")
                print(f"    source: {source['source']}")
                print(f"    exact source window sha256: {source['material_sha256']}")
                print(f"    separator: {_render(bytes((separator,)))} (byte {separator})")
                print(f"    stable first span: {_render(left)}")
                print(f"    substitution span:")
                for occupant in frame["occupants"]:
                    material = _material(source, occupant["material"])
                    ranges = tuple(tuple(found) for found in occupant["source_ranges"])
                    print(f"      {_render(material)}  count={len(ranges)}  ranges={ranges}")
                    for start, end in ranges:
                        full_occurrences.append(
                            (start - len(left) - 1, end + 1 + len(right))
                        )
                occupant_materials = tuple(
                    _material(source, occupant["material"])
                    for occupant in frame["occupants"]
                )
                changes = tuple(
                    sorted(
                        _minimal_change(first, second)
                        for first_position, first in enumerate(occupant_materials)
                        for second in occupant_materials[first_position + 1 :]
                    )
                )
                change_signatures[changes].append(number)
                print(f"    stable final span: {_render(right)}")
                print(f"    exact full-frame ranges: {tuple(sorted(full_occurrences))}\n")
                frames_by_source[source["source"]].append(
                    {
                        "number": number,
                        "ranges": tuple(sorted(full_occurrences)),
                    }
                )

    print("  exact frame-shape equivalence across independently bounded sources:\n")
    repeated_shapes = 0
    for (separator, left, right), occurrences in sorted(
        exact_shapes.items(), key=lambda item: (-len(item[1]), item[0])
    ):
        if len(occurrences) < 2:
            continue
        repeated_shapes += 1
        print(
            f"    {_render(left)} <{_render(bytes((separator,)))}> _ "
            f"<{_render(bytes((separator,)))}> {_render(right)}"
        )
        for source, _frame in occurrences:
            print(f"      {source}")
    if not repeated_shapes:
        print("    none")

    print("\n  exact minimal occupant-change equivalence across findings:\n")
    repeated_changes = 0
    for changes, numbers in sorted(
        change_signatures.items(), key=lambda item: (-len(item[1]), item[0])
    ):
        if len(numbers) < 2:
            continue
        repeated_changes += 1
        print(f"    findings: {', '.join('F' + str(number) for number in numbers)}")
        for first, second in changes:
            print(f"      {_render(first)}  <->  {_render(second)}")
    if not repeated_changes:
        print("    none")

    print("\n  exact occurrence-range containment among findings in one source:\n")
    containment_count = 0
    for source, frames in frames_by_source.items():
        for inner in frames:
            for outer in frames:
                if inner is outer:
                    continue
                if inner["ranges"] and all(
                    any(
                        outer_start <= inner_start and inner_end <= outer_end
                        for outer_start, outer_end in outer["ranges"]
                    )
                    for inner_start, inner_end in inner["ranges"]
                ):
                    containment_count += 1
                    print(
                        f"    {source}: every F{inner['number']} range is carried "
                        f"inside an F{outer['number']} range"
                    )
    if not containment_count:
        print("    none")

    print("\n  overlap and exact translation among findings in one source:\n")
    relation_count = 0
    for source, frames in frames_by_source.items():
        for first_position, first in enumerate(frames):
            for second in frames[first_position + 1 :]:
                overlaps = sum(
                    1
                    for first_start, first_end in first["ranges"]
                    if any(
                        first_start < second_end and second_start < first_end
                        for second_start, second_end in second["ranges"]
                    )
                )
                translation = None
                if len(first["ranges"]) == len(second["ranges"]):
                    deltas = {
                        (second_start - first_start, second_end - first_end)
                        for (first_start, first_end), (second_start, second_end) in zip(
                            first["ranges"], second["ranges"]
                        )
                    }
                    if len(deltas) == 1:
                        translation = next(iter(deltas))
                if not overlaps and translation is None:
                    continue
                relation_count += 1
                print(
                    f"    {source}: F{first['number']} / F{second['number']}  "
                    f"overlapping first ranges={overlaps}"
                    + (
                        f"  exact ordered range translation={translation}"
                        if translation is not None
                        else ""
                    )
                )
    if not relation_count:
        print("    none")

    print(
        "\n  Exact frame equality and exact range containment are the only\n"
        "  relations tested between findings. Similar spelling, nearby source\n"
        "  positions, human grammar, and current Seed vocabulary were not read."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
