#!/usr/bin/env python3
"""Walk every source-supported frame relation into exact larger structure.

The blind operation begins with raw material projections and every exact frame
relation they produce.  It does not compute complete material renamings first.
Each relation supplies only its endpoint pairs.  Those pairs address projection
rows that can answer; the operation then walks source coordinates in order and
retains every complete one-to-one continuation.

Plain source material is absent from the frozen artifact.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import time

from observe_cross_surface_structure import (
    SOURCE_GROUPS,
    _digest,
    _encoded,
    _frame_relations,
    _frames,
    _material_identity,
    _projections,
)


OUTPUT = Path("/tmp/seed_cross_surface_frame_continuation_blind.json")

_FIRST, _SECOND, _THIRD, _FOURTH = SOURCE_GROUPS[0]
_CHANGED_SECOND, _CHANGED_THIRD, _CHANGED_FOURTH = SOURCE_GROUPS[5][1:]

SOURCE_GROUPS_WITH_COMPETING_FRAMES = (
    (
        _FIRST,
        _SECOND,
        _THIRD,
        _FOURTH,
        _CHANGED_THIRD,
        _CHANGED_FOURTH,
    ),
    (
        _THIRD,
        _FOURTH,
        _CHANGED_THIRD,
        _CHANGED_FOURTH,
    ),
    (
        _FIRST,
        _CHANGED_SECOND,
        _THIRD,
        _FOURTH,
        _CHANGED_THIRD,
        _CHANGED_FOURTH,
    ),
    (
        _FIRST,
        _SECOND,
        _CHANGED_SECOND,
        _THIRD,
        _FOURTH,
        _CHANGED_THIRD,
        _CHANGED_FOURTH,
    ),
)


def _exact_mapping(
    pairs: tuple[tuple[bytes, bytes], ...],
) -> dict[bytes, bytes] | None:
    mapping: dict[bytes, bytes] = {}
    reverse: dict[bytes, bytes] = {}
    for first, later in pairs:
        if (
            (first in mapping and mapping[first] != later)
            or (later in reverse and reverse[later] != first)
        ):
            return None
        mapping[first] = later
        reverse[later] = first
    return mapping


def _frame_orientations(frame: dict) -> tuple[dict, ...]:
    pairs: list[tuple[bytes, bytes]] = []
    for first_material, later_material in frame["_raw_endpoint_pairs"]:
        if len(first_material) == len(later_material):
            pairs.extend(zip(first_material, later_material, strict=True))
    if not pairs:
        return ()

    findings = []
    for name, oriented in (
        ("first-to-later", tuple(pairs)),
        ("later-to-first", tuple((later, first) for first, later in pairs)),
    ):
        mapping = _exact_mapping(oriented)
        if mapping is None:
            continue
        material = {
            "orientation": name,
            "anchor_pairs": [
                [_material_identity(first), _material_identity(later)]
                for first, later in sorted(mapping.items())
            ],
        }
        findings.append(
            {
                **material,
                "orientation_identity_sha256": _digest(_encoded(material)),
                "_raw_mapping": mapping,
            }
        )
    return tuple(findings)


def _row_can_answer(
    first_row: tuple[bytes, ...],
    later_row: tuple[bytes, ...],
    mapping: dict[bytes, bytes],
) -> bool:
    reverse = {later: first for first, later in mapping.items()}
    return all(
        (first not in mapping or mapping[first] == later)
        and (later not in reverse or reverse[later] == first)
        for first, later in zip(first_row, later_row, strict=True)
    )


def _row_pairings(
    first_rows: tuple[tuple[bytes, ...], ...],
    later_rows: tuple[tuple[bytes, ...], ...],
    mapping: dict[bytes, bytes],
) -> tuple[tuple[int, ...], ...]:
    if (
        len(first_rows) != len(later_rows)
        or not first_rows
        or not later_rows
        or len(first_rows[0]) != len(later_rows[0])
    ):
        return ()

    answers = tuple(
        tuple(
            later_number
            for later_number, later_row in enumerate(later_rows)
            if _row_can_answer(first_row, later_row, mapping)
        )
        for first_row in first_rows
    )
    if any(not row_answers for row_answers in answers):
        return ()

    order = tuple(
        sorted(range(len(first_rows)), key=lambda number: len(answers[number]))
    )
    assigned = [-1] * len(first_rows)
    used: dict[int, None] = {}
    findings: list[tuple[int, ...]] = []

    def walk(position: int) -> None:
        if position == len(order):
            findings.append(tuple(assigned))
            return
        first_number = order[position]
        for later_number in answers[first_number]:
            if later_number in used:
                continue
            assigned[first_number] = later_number
            used[later_number] = None
            walk(position + 1)
            used.pop(later_number)
            assigned[first_number] = -1

    walk(0)
    return tuple(findings)


def _walk_coordinates(
    first_rows: tuple[tuple[bytes, ...], ...],
    later_rows: tuple[tuple[bytes, ...], ...],
    row_pairing: tuple[int, ...],
    anchor_mapping: dict[bytes, bytes],
) -> dict | None:
    mapping = dict(anchor_mapping)
    reverse = {later: first for first, later in mapping.items()}
    added = []
    for first_row_number, coordinate in (
        (row_number, coordinate)
        for row_number in range(len(first_rows))
        for coordinate in range(len(first_rows[row_number]))
    ):
        later_row_number = row_pairing[first_row_number]
        first = first_rows[first_row_number][coordinate]
        later = later_rows[later_row_number][coordinate]
        if (
            (first in mapping and mapping[first] != later)
            or (later in reverse and reverse[later] != first)
        ):
            return None
        if first not in mapping:
            mapping[first] = later
            reverse[later] = first
            added.append(
                {
                    "first_row": first_row_number,
                    "later_row": later_row_number,
                    "coordinate": coordinate,
                    "first_material_sha256": _material_identity(first),
                    "later_material_sha256": _material_identity(later),
                }
            )

    if any(
        tuple(mapping[item] for item in first_rows[first_row_number])
        != later_rows[later_row_number]
        for first_row_number, later_row_number in enumerate(row_pairing)
    ):
        return None

    material = {
        "row_pairing": list(row_pairing),
        "added_pairs": added,
        "complete_mapping": [
            [_material_identity(first), _material_identity(later)]
            for first, later in sorted(mapping.items())
        ],
    }
    return {
        **material,
        "continuation_identity_sha256": _digest(_encoded(material)),
        "complete_mapping_count": len(mapping),
        "added_mapping_count": len(mapping) - len(anchor_mapping),
    }


def _relation_continuations(
    relation: dict,
    frames_by_identity: dict[str, dict],
    projections: list[dict],
) -> dict:
    first_frame = frames_by_identity[relation["first_frame_identity_sha256"]]
    orientations = _frame_orientations(first_frame)
    findings = []
    addressed_projection_pairs = 0
    addressed_row_pairings = 0

    for orientation in orientations:
        mapping = orientation["_raw_mapping"]
        first_materials = tuple(mapping)
        later_materials = tuple(mapping.values())
        for first in projections:
            carried_first = {
                item: None for row in first["rows"] for item in row
            }
            if any(item not in carried_first for item in first_materials):
                continue
            for later in projections:
                if (
                    first["projection_identity_sha256"]
                    == later["projection_identity_sha256"]
                ):
                    continue
                carried_later = {
                    item: None for row in later["rows"] for item in row
                }
                if any(item not in carried_later for item in later_materials):
                    continue
                if (
                    len(first["rows"]) != len(later["rows"])
                    or len(first["rows"][0]) != len(later["rows"][0])
                ):
                    continue
                addressed_projection_pairs += 1
                pairings = _row_pairings(first["rows"], later["rows"], mapping)
                addressed_row_pairings += len(pairings)
                for pairing in pairings:
                    continuation = _walk_coordinates(
                        first["rows"], later["rows"], pairing, mapping
                    )
                    if continuation is None or continuation["added_mapping_count"] == 0:
                        continue
                    findings.append(
                        {
                            "orientation_identity_sha256": orientation[
                                "orientation_identity_sha256"
                            ],
                            "first_projection_identity_sha256": first[
                                "projection_identity_sha256"
                            ],
                            "later_projection_identity_sha256": later[
                                "projection_identity_sha256"
                            ],
                            **continuation,
                        }
                    )

    unique = {
        (
            finding["orientation_identity_sha256"],
            finding["first_projection_identity_sha256"],
            finding["later_projection_identity_sha256"],
            tuple(tuple(pair) for pair in finding["complete_mapping"]),
        ): finding
        for finding in findings
    }
    ordered = sorted(
        unique.values(),
        key=lambda finding: (
            finding["orientation_identity_sha256"],
            finding["first_projection_identity_sha256"],
            finding["later_projection_identity_sha256"],
            finding["complete_mapping"],
        ),
    )
    greatest = max(
        (finding["complete_mapping_count"] for finding in ordered), default=0
    )
    return {
        "frame_relation": relation,
        "orientation_count": len(orientations),
        "orientations": [
            {
                key: value
                for key, value in orientation.items()
                if not key.startswith("_raw")
            }
            for orientation in orientations
        ],
        "addressed_projection_pair_count": addressed_projection_pairs,
        "addressed_row_pairing_count": addressed_row_pairings,
        "continuation_count": len(ordered),
        "greatest_complete_mapping_count": greatest,
        "continuations": ordered,
    }


def _observe_group(group_number: int, sources: tuple[bytes, ...]) -> dict:
    begun = time.perf_counter()
    projections = [
        projection
        for source_number, material in enumerate(sources)
        for projection in _projections(source_number, material)
    ]
    frames = _frames(projections)
    relations = _frame_relations(frames, projections)
    frames_by_identity = {
        frame["frame_identity_sha256"]: frame for frame in frames
    }
    continuations = [
        _relation_continuations(relation, frames_by_identity, projections)
        for relation in relations
    ]
    return {
        "group_number": group_number,
        "source_materials": [
            {
                "source_number": source_number,
                "byte_count": len(material),
                "material_sha256": sha256(material).hexdigest(),
            }
            for source_number, material in enumerate(sources)
        ],
        "projection_count": len(projections),
        "frame_count": len(frames),
        "frame_relation_count": len(relations),
        "frame_relation_continuations": continuations,
        "known_loss": None,
        "wall_seconds": time.perf_counter() - begun,
    }


def observe() -> dict:
    groups = [
        _observe_group(group_number, sources)
        for group_number, sources in enumerate(SOURCE_GROUPS_WITH_COMPETING_FRAMES)
    ]
    return {
        "operation": (
            "all recurring-byte projections; all source-supported frame relations; "
            "each relation addresses only projection rows answering its endpoint "
            "pairs; exact coordinate continuation"
        ),
        "group_count": len(groups),
        "groups": [
            {key: value for key, value in group.items() if key != "wall_seconds"}
            for group in groups
        ],
        "known_loss": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    begun = time.perf_counter()
    result = observe()
    encoded = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {sha256(encoded).hexdigest()}")
    for group in result["groups"]:
        print(
            f"group {group['group_number']} "
            f"projections={group['projection_count']} "
            f"frames={group['frame_count']} "
            f"relations={group['frame_relation_count']} "
            f"continuations={[item['continuation_count'] for item in group['frame_relation_continuations']]} "
            f"greatest={[item['greatest_complete_mapping_count'] for item in group['frame_relation_continuations']]}"
        )
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
