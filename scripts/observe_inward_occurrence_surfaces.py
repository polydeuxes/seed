"""Measure recurring coordinate surfaces in recorded Seed occurrences.

The input is the frozen output of ``record_inward_occurrence_material.py``.
This observer reads only each occurrence's material and append address.  It does
not read event labels, the Book, machine grammar, runtime constants, or expected
Responsibility/Act coordinates.

Scalar values are withheld from the surface. The first aperture measures only
the exact top-level coordinate material and each immediate value type. An exact
structure digest separately retains each immediate container's member count.
No nested coordinate is inferred from this first surface.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


INPUT = Path("/tmp/seed_inward_occurrence_material.json")
OUTPUT = Path("/tmp/seed_inward_occurrence_surfaces_blind.json")
COORDINATE_MATERIAL_OUTPUT = Path(
    "/tmp/seed_inward_occurrence_coordinate_materials.json"
)


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _material_digest(material: str) -> str:
    return _digest(material.encode())


def _surface(
    value: Any,
    coordinate_materials: dict[str, str],
) -> tuple[str, str, frozenset[str], int, int]:
    if type(value) is not dict:
        raise ValueError("one recorded occurrence must carry top-level coordinates")
    exact_parts = [b"mapping\0"]
    coordinate_parts = [b"mapping\0"]
    carried_coordinates = set()
    container_count = 1
    scalar_count = 0
    entries = []
    for key, child in value.items():
        if type(key) is not str:
            raise ValueError("recorded occurrence material has a non-text key")
        key_digest = _material_digest(key)
        prior = coordinate_materials.setdefault(key_digest, key)
        if prior != key:
            raise ValueError("two coordinate materials have one digest")
        value_type = (
            "mapping"
            if type(child) is dict
            else "list"
            if type(child) is list
            else "none"
            if child is None
            else "boolean"
            if type(child) is bool
            else "integer"
            if type(child) is int
            else "number"
            if type(child) is float
            else "text"
            if type(child) is str
            else None
        )
        if value_type is None:
            raise ValueError(f"unaddressed scalar type: {type(child).__name__}")
        member_count = len(child) if type(child) in (dict, list) else None
        entries.append((key_digest, value_type, member_count))
    for key_digest, value_type, member_count in sorted(entries):
        part = bytes.fromhex(key_digest) + b"\0" + value_type.encode() + b"\0"
        coordinate_parts.append(part)
        exact_parts.append(part)
        carried_coordinates.add(key_digest)
        if member_count is None:
            scalar_count += 1
        else:
            container_count += 1
            exact_parts.append(member_count.to_bytes(8, "big"))
    return (
        _digest(b"".join(exact_parts)),
        _digest(b"".join(coordinate_parts)),
        frozenset(carried_coordinates),
        container_count,
        scalar_count,
    )


def _adjacent_sequences(sequence: tuple[str, ...], length: int) -> set[tuple[str, ...]]:
    return {
        sequence[start : start + length]
        for start in range(len(sequence) - length + 1)
    }


def _common_adjacent_sequences(
    source_sequences: list[tuple[str, ...]],
) -> tuple[dict[str, int], int, list[tuple[str, ...]]]:
    counts_by_length = {}
    latest = []
    maximum_length = 0
    for length in range(1, min(map(len, source_sequences)) + 1):
        common = set.intersection(
            *(_adjacent_sequences(sequence, length) for sequence in source_sequences)
        )
        if not common:
            break
        counts_by_length[str(length)] = len(common)
        maximum_length = length
        latest = sorted(common)
    return counts_by_length, maximum_length, latest


def _occurrences_of_sequence(
    sequence: tuple[str, ...], sought: tuple[str, ...]
) -> list[int]:
    width = len(sought)
    return [
        start
        for start in range(len(sequence) - width + 1)
        if sequence[start : start + width] == sought
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--coordinate-material-output",
        type=Path,
        default=COORDINATE_MATERIAL_OUTPUT,
    )
    arguments = parser.parse_args()

    input_bytes = arguments.input.read_bytes()
    recorded = json.loads(input_bytes)
    if recorded.get("known_loss") is not None:
        raise ValueError("recorded inward source carries known loss")

    coordinate_materials = {}
    surfaces: dict[str, dict] = {}
    source_sequences = []
    for source in recorded["sources"]:
        if source.get("known_loss") is not None:
            raise ValueError("one recorded inward source carries known loss")
        sequence = []
        for occurrence in source["occurrences"]:
            exact, coordinate, carried, containers, scalars = _surface(
                occurrence["material"], coordinate_materials
            )
            sequence.append(coordinate)
            finding = surfaces.setdefault(
                coordinate,
                {
                    "coordinate_surface_sha256": coordinate,
                    "coordinate_material_sha256s": sorted(carried),
                    "exact_structure_sha256s": set(),
                    "container_count_minimum": containers,
                    "container_count_maximum": containers,
                    "scalar_count_minimum": scalars,
                    "scalar_count_maximum": scalars,
                    "occurrences": [],
                },
            )
            finding["exact_structure_sha256s"].add(exact)
            finding["container_count_minimum"] = min(
                finding["container_count_minimum"], containers
            )
            finding["container_count_maximum"] = max(
                finding["container_count_maximum"], containers
            )
            finding["scalar_count_minimum"] = min(
                finding["scalar_count_minimum"], scalars
            )
            finding["scalar_count_maximum"] = max(
                finding["scalar_count_maximum"], scalars
            )
            finding["occurrences"].append(
                [source["source_number"], occurrence["append_position"]]
            )
        source_sequences.append(tuple(sequence))

    for finding in surfaces.values():
        finding["exact_structure_sha256s"] = sorted(
            finding["exact_structure_sha256s"]
        )
        finding["source_count"] = len(
            {source_number for source_number, _position in finding["occurrences"]}
        )

    counts_by_length, maximum_length, longest = _common_adjacent_sequences(
        source_sequences
    )
    longest_records = []
    for sequence in longest:
        longest_records.append(
            {
                "coordinate_surface_sha256s": list(sequence),
                "occurrences": [
                    {
                        "source_number": source_number,
                        "start_append_positions": _occurrences_of_sequence(
                            source_sequence, sequence
                        ),
                    }
                    for source_number, source_sequence in enumerate(source_sequences)
                ],
            }
        )

    middle_by_flanks: dict[tuple[str, str], set[str]] = defaultdict(set)
    flank_occurrences: dict[tuple[str, str], list[list[int]]] = defaultdict(list)
    for source_number, sequence in enumerate(source_sequences):
        for position in range(1, len(sequence) - 1):
            flanks = (sequence[position - 1], sequence[position + 1])
            middle_by_flanks[flanks].add(sequence[position])
            flank_occurrences[flanks].append([source_number, position])
    varying_middle_frames = []
    for flanks, middles in middle_by_flanks.items():
        addressed_sources = {
            source_number for source_number, _position in flank_occurrences[flanks]
        }
        if len(middles) < 2 or len(addressed_sources) != len(source_sequences):
            continue
        varying_middle_frames.append(
            {
                "first_coordinate_surface_sha256": flanks[0],
                "middle_coordinate_surface_sha256s": sorted(middles),
                "last_coordinate_surface_sha256": flanks[1],
                "occurrences": flank_occurrences[flanks],
            }
        )
    varying_middle_frames.sort(
        key=lambda finding: (
            finding["first_coordinate_surface_sha256"],
            finding["last_coordinate_surface_sha256"],
        )
    )

    finding = {
        "source_artifact_sha256": _digest(input_bytes),
        "operation": (
            "exact occurrence-material coordinate structure with scalar values "
            "and event labels withheld; recurring source-order frames measured "
            "across every supplied source"
        ),
        "source_occurrence_counts": [len(sequence) for sequence in source_sequences],
        "surface_count": len(surfaces),
        "surfaces": sorted(
            surfaces.values(), key=lambda item: item["coordinate_surface_sha256"]
        ),
        "common_adjacent_sequence_count_by_length": counts_by_length,
        "maximum_common_adjacent_sequence_length": maximum_length,
        "maximum_common_adjacent_sequences": longest_records,
        "varying_middle_frames": varying_middle_frames,
        "known_loss": None,
    }
    encoded = _encoded(finding)
    arguments.output.write_bytes(encoded)
    coordinate_material_finding = {
        "source_artifact_sha256": _digest(input_bytes),
        "occurrence_surface_artifact_sha256": _digest(encoded),
        "coordinate_materials": coordinate_materials,
        "known_loss": None,
    }
    coordinate_material_encoded = _encoded(coordinate_material_finding)
    arguments.coordinate_material_output.write_bytes(coordinate_material_encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"coordinate material: {arguments.coordinate_material_output}")
    print(
        "coordinate material sha256: "
        f"{_digest(coordinate_material_encoded)}"
    )
    print(f"occurrences: {sum(finding['source_occurrence_counts'])}")
    print(f"coordinate surfaces: {finding['surface_count']}")
    print(f"maximum common adjacent length: {maximum_length}")
    print(f"maximum common adjacent sequences: {len(longest_records)}")
    print(f"varying-middle frames: {len(varying_middle_frames)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
