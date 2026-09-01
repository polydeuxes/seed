#!/usr/bin/env python3
"""Enumerate exact structural relations across opaque source materials.

The operation receives raw bytes only.  It enumerates every recurring byte as
a possible row boundary and every other carried byte as a possible item
boundary.  It preserves every exact rectangular projection, every exact
material renaming between equal projections, every stable-middle frame, and
every exact or reversed endpoint relation between those frames.

No byte, source, coordinate, renaming, or frame is selected by a human-language
meaning.  Plain material is absent from the frozen artifact.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import time


OUTPUT = Path("/tmp/seed_cross_surface_structure_blind.json")

_FIRST = (
    b"1 + 1 = 2\n"
    b"1 + 2 = 3\n"
    b"2 + 2 = 4\n"
    b"2 + 3 = 5\n"
    b"3 + 3 = 6\n"
)
_SECOND = (
    b"one plus one equals two\n"
    b"one plus two equals three\n"
    b"two plus two equals four\n"
    b"two plus three equals five\n"
    b"three plus three equals six\n"
)
_THIRD = (
    b"1 is equal to one\n"
    b"2 is equal to two\n"
    b"3 is equal to three\n"
)
_FOURTH = b"one = 1\ntwo = 2\nthree = 3\n"

# The operation receives each group only by position.  The changed groups are
# exact controls, not labels supplied to the blind comparison.
SOURCE_GROUPS = (
    (_FIRST, _SECOND, _THIRD, _FOURTH),
    (_FIRST, _SECOND),
    (
        _FIRST,
        (
            b"one plus one equals two\n"
            b"one plus two equals three\n"
            b"two plus two equals four\n"
            b"three plus two equals five\n"
            b"three plus three equals six\n"
        ),
        _THIRD,
        _FOURTH,
    ),
    (
        _FIRST,
        _SECOND,
        _THIRD,
        b"one = 1\nthree = 2\ntwo = 3\n",
    ),
    (
        _FIRST,
        b"three plus three equals six\n"
        b"two plus three equals five\n"
        b"two plus two equals four\n"
        b"one plus two equals three\n"
        b"one plus one equals two\n",
        b"3 is equal to three\n2 is equal to two\n1 is equal to one\n",
        b"three = 3\ntwo = 2\none = 1\n",
    ),
    (
        _FIRST,
        (
            b"two plus two equals three\n"
            b"two plus three equals one\n"
            b"three plus three equals four\n"
            b"three plus one equals five\n"
            b"one plus one equals six\n"
        ),
        (
            b"1 is equal to two\n"
            b"2 is equal to three\n"
            b"3 is equal to one\n"
        ),
        b"two = 1\nthree = 2\none = 3\n",
    ),
    (_FIRST, _SECOND, _THIRD),
    (_FIRST, _SECOND, _FOURTH),
    tuple(
        b"zafeqor\n" + material + b"nivokasure\n"
        for material in (_FIRST, _SECOND, _THIRD, _FOURTH)
    ),
)


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _material_identity(material: bytes) -> str:
    return _digest(material)


def _projection_identity(
    source_number: int,
    row_boundary: int,
    item_boundary: int,
    first_row: int,
    later_row: int,
    rows: tuple[tuple[bytes, ...], ...],
) -> str:
    return _digest(
        _encoded(
            {
                "source_number": source_number,
                "row_boundary_sha256": _digest(bytes((row_boundary,))),
                "item_boundary_sha256": _digest(bytes((item_boundary,))),
                "first_row": first_row,
                "later_row": later_row,
                "rows": [
                    [_material_identity(item) for item in row]
                    for row in rows
                ],
            }
        )
    )


def _projections(source_number: int, material: bytes) -> list[dict]:
    findings = []
    carried_bytes = sorted(set(material))
    for row_boundary in carried_bytes:
        rows = material.split(bytes((row_boundary,)))
        if rows and rows[-1] == b"":
            rows = rows[:-1]
        if len(rows) < 3:
            continue
        for item_boundary in carried_bytes:
            if item_boundary == row_boundary:
                continue
            divided = tuple(
                tuple(row.split(bytes((item_boundary,)))) for row in rows
            )
            first_row = 0
            while first_row < len(divided):
                width = len(divided[first_row])
                valid = width >= 2 and all(divided[first_row])
                if not valid:
                    first_row += 1
                    continue
                later_row = first_row + 1
                while (
                    later_row < len(divided)
                    and len(divided[later_row]) == width
                    and all(divided[later_row])
                ):
                    later_row += 1
                if later_row - first_row >= 3:
                    carried_rows = divided[first_row:later_row]
                    findings.append(
                        {
                            "source_number": source_number,
                            "source_material_sha256": _digest(material),
                            "row_boundary_sha256": _digest(bytes((row_boundary,))),
                            "item_boundary_sha256": _digest(bytes((item_boundary,))),
                            "first_row": first_row,
                            "later_row": later_row,
                            "rows": carried_rows,
                            "projection_identity_sha256": _projection_identity(
                                source_number,
                                row_boundary,
                                item_boundary,
                                first_row,
                                later_row,
                                carried_rows,
                            ),
                        }
                    )
                first_row = later_row
    return findings


def _token_signatures(rows: tuple[tuple[bytes, ...], ...]) -> dict[bytes, tuple[int, ...]]:
    width = len(rows[0])
    tokens = {item for row in rows for item in row}
    return {
        token: tuple(
            sum(row[position] == token for row in rows)
            for position in range(width)
        )
        for token in tokens
    }


def _partial_mapping_can_continue(
    first_rows: tuple[tuple[bytes, ...], ...],
    later_rows: tuple[tuple[bytes, ...], ...],
    mapping: dict[bytes, bytes],
) -> bool:
    for first_row in first_rows:
        if not any(
            all(
                first_item not in mapping
                or mapping[first_item] == later_item
                for first_item, later_item in zip(first_row, later_row, strict=True)
            )
            for later_row in later_rows
        ):
            return False
    return True


def _exact_renamings(
    first_rows: tuple[tuple[bytes, ...], ...],
    later_rows: tuple[tuple[bytes, ...], ...],
) -> list[dict[bytes, bytes]]:
    if len(first_rows) != len(later_rows) or len(first_rows[0]) != len(later_rows[0]):
        return []
    first_signatures = _token_signatures(first_rows)
    later_signatures = _token_signatures(later_rows)
    first_by_signature: dict[tuple[int, ...], list[bytes]] = defaultdict(list)
    later_by_signature: dict[tuple[int, ...], list[bytes]] = defaultdict(list)
    for token, signature in first_signatures.items():
        first_by_signature[signature].append(token)
    for token, signature in later_signatures.items():
        later_by_signature[signature].append(token)
    if {
        signature: len(tokens) for signature, tokens in first_by_signature.items()
    } != {
        signature: len(tokens) for signature, tokens in later_by_signature.items()
    }:
        return []

    groups = sorted(
        (
            tuple(sorted(first_by_signature[signature])),
            tuple(sorted(later_by_signature[signature])),
        )
        for signature in first_by_signature
    )
    target = Counter(later_rows)
    answers: list[dict[bytes, bytes]] = []

    def walk(group_number: int, mapping: dict[bytes, bytes]) -> None:
        if group_number == len(groups):
            transformed = Counter(
                tuple(mapping[item] for item in row) for row in first_rows
            )
            if transformed == target:
                answers.append(dict(mapping))
            return
        first_tokens, later_tokens = groups[group_number]
        for ordering in permutations(later_tokens):
            added = dict(zip(first_tokens, ordering, strict=True))
            mapping.update(added)
            if _partial_mapping_can_continue(first_rows, later_rows, mapping):
                walk(group_number + 1, mapping)
            for token in first_tokens:
                mapping.pop(token)

    walk(0, {})
    return answers


def _renamings(projections: list[dict]) -> list[dict]:
    findings = []
    for first_number, first in enumerate(projections):
        for later in projections[first_number + 1 :]:
            if first["source_number"] == later["source_number"]:
                continue
            answers = _exact_renamings(first["rows"], later["rows"])
            for mapping in answers:
                transformed_in_order = tuple(
                    tuple(mapping[item] for item in row) for row in first["rows"]
                )
                findings.append(
                    {
                        "first_projection_identity_sha256": first[
                            "projection_identity_sha256"
                        ],
                        "later_projection_identity_sha256": later[
                            "projection_identity_sha256"
                        ],
                        "preserves_source_order": transformed_in_order
                        == later["rows"],
                        "material_renaming": [
                            [_material_identity(first_item), _material_identity(later_item)]
                            for first_item, later_item in sorted(mapping.items())
                        ],
                    }
                )
    return findings


def _frames(projections: list[dict]) -> list[dict]:
    findings = []
    for projection in projections:
        rows = projection["rows"]
        width = len(rows[0])
        for first_middle in range(1, width - 1):
            for later_middle in range(first_middle + 1, width):
                middle_materials = {
                    row[first_middle:later_middle] for row in rows
                }
                if len(middle_materials) != 1:
                    continue
                endpoint_pairs = tuple(
                    (row[:first_middle], row[later_middle:]) for row in rows
                )
                if len(set(endpoint_pairs)) < 2:
                    continue
                middle = next(iter(middle_materials))
                material = {
                    "projection_identity_sha256": projection[
                        "projection_identity_sha256"
                    ],
                    "first_middle_coordinate": first_middle,
                    "later_middle_coordinate": later_middle,
                    "middle_material": [_material_identity(item) for item in middle],
                    "endpoint_pairs": [
                        [
                            [_material_identity(item) for item in first],
                            [_material_identity(item) for item in later],
                        ]
                        for first, later in endpoint_pairs
                    ],
                }
                findings.append(
                    {
                        **material,
                        "frame_identity_sha256": _digest(_encoded(material)),
                        "_raw_endpoint_pairs": endpoint_pairs,
                    }
                )
    return findings


def _frame_relations(frames: list[dict], projections: list[dict]) -> list[dict]:
    source_by_projection = {
        projection["projection_identity_sha256"]: projection["source_number"]
        for projection in projections
    }
    findings = []
    for first_number, first in enumerate(frames):
        first_source = source_by_projection[first["projection_identity_sha256"]]
        first_pairs = Counter(first["_raw_endpoint_pairs"])
        for later in frames[first_number + 1 :]:
            later_source = source_by_projection[later["projection_identity_sha256"]]
            if first_source == later_source:
                continue
            later_pairs = Counter(later["_raw_endpoint_pairs"])
            relation = None
            if first_pairs == later_pairs:
                relation = "exact"
            elif Counter((right, left) for left, right in first_pairs.elements()) == later_pairs:
                relation = "reversed"
            if relation is not None:
                findings.append(
                    {
                        "first_frame_identity_sha256": first["frame_identity_sha256"],
                        "later_frame_identity_sha256": later["frame_identity_sha256"],
                        "endpoint_relation": relation,
                    }
                )
    return findings


def _relation_walks(
    frame_relations: list[dict],
    frames: list[dict],
    projections: list[dict],
    renamings: list[dict],
) -> list[dict]:
    frames_by_identity = {
        frame["frame_identity_sha256"]: frame for frame in frames
    }
    projections_by_identity = {
        projection["projection_identity_sha256"]: projection
        for projection in projections
    }
    findings = []
    for relation in frame_relations:
        first = frames_by_identity[relation["first_frame_identity_sha256"]]
        later = frames_by_identity[relation["later_frame_identity_sha256"]]
        forward_pairs = []
        for first_extent, later_extent in first["endpoint_pairs"]:
            if len(first_extent) == len(later_extent):
                forward_pairs.extend(zip(first_extent, later_extent, strict=True))
        orientations = (
            ("first-to-later", forward_pairs),
            ("later-to-first", [(later, first) for first, later in forward_pairs]),
        )
        compatible = []
        for orientation, anchor_pairs in orientations:
            for renaming in renamings:
                mapping = dict(renaming["material_renaming"])
                if anchor_pairs and all(
                    mapping.get(first_item) == later_item
                    for first_item, later_item in anchor_pairs
                ):
                    compatible.append(
                        {
                            "orientation": orientation,
                            "anchor_pairs": [list(pair) for pair in anchor_pairs],
                            "renaming": renaming,
                        }
                    )

        middle_walks = []
        for compatible_renaming in compatible:
            renaming = compatible_renaming["renaming"]
            first_projection = projections_by_identity[
                renaming["first_projection_identity_sha256"]
            ]
            later_projection = projections_by_identity[
                renaming["later_projection_identity_sha256"]
            ]
            mapping = dict(renaming["material_renaming"])
            for frame_position, frame in (("first", first), ("later", later)):
                middle = frame["middle_material"]
                if not all(item in mapping for item in middle):
                    continue
                for coordinate in range(
                    len(first_projection["rows"][0]) - len(middle) + 1
                ):
                    if not all(
                        row[coordinate : coordinate + len(middle)] == middle
                        for row in first_projection["rows"]
                    ):
                        continue
                    renamed_middle = [mapping[item] for item in middle]
                    if not all(
                        row[coordinate : coordinate + len(renamed_middle)]
                        == renamed_middle
                        for row in later_projection["rows"]
                    ):
                        continue
                    middle_walks.append(
                        {
                            "frame_position": frame_position,
                            "first_projection_identity_sha256": first_projection[
                                "projection_identity_sha256"
                            ],
                            "later_projection_identity_sha256": later_projection[
                                "projection_identity_sha256"
                            ],
                            "first_coordinate": coordinate,
                            "later_coordinate": coordinate + len(middle),
                            "first_middle_material": middle,
                            "later_middle_material": renamed_middle,
                        }
                    )

        findings.append(
            {
                "frame_relation": relation,
                "compatible_renaming_count": len(compatible),
                "compatible_renamings": compatible,
                "middle_walk_count": len(middle_walks),
                "middle_walks": middle_walks,
            }
        )
    return findings


def _render_projection(projection: dict) -> dict:
    return {
        key: value
        for key, value in projection.items()
        if key != "rows"
    } | {
        "row_count": len(projection["rows"]),
        "coordinate_count": len(projection["rows"][0]),
        "rows": [
            [_material_identity(item) for item in row]
            for row in projection["rows"]
        ],
    }


def _observe_group(group_number: int, sources: tuple[bytes, ...]) -> dict:
    begun = time.perf_counter()
    projections = [
        projection
        for source_number, material in enumerate(sources)
        for projection in _projections(source_number, material)
    ]
    renamings = _renamings(projections)
    frames = _frames(projections)
    frame_relations = _frame_relations(frames, projections)
    relation_walks = _relation_walks(
        frame_relations, frames, [_render_projection(item) for item in projections], renamings
    )
    return {
        "group_number": group_number,
        "source_materials": [
            {
                "source_number": number,
                "byte_count": len(material),
                "material_sha256": _digest(material),
            }
            for number, material in enumerate(sources)
        ],
        "projection_count": len(projections),
        "projections": [_render_projection(projection) for projection in projections],
        "exact_material_renaming_count": len(renamings),
        "exact_material_renamings": renamings,
        "stable_middle_frame_count": len(frames),
        "stable_middle_frames": [
            {key: value for key, value in frame.items() if not key.startswith("_raw")}
            for frame in frames
        ],
        "exact_endpoint_frame_relation_count": len(frame_relations),
        "exact_endpoint_frame_relations": frame_relations,
        "frame_relation_walk_count": len(relation_walks),
        "frame_relation_walks": relation_walks,
        "known_loss": None,
        "wall_seconds": time.perf_counter() - begun,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    begun = time.perf_counter()
    groups = [_observe_group(number, sources) for number, sources in enumerate(SOURCE_GROUPS)]
    result = {
        "operation": (
            "all recurring-byte row/item apertures; all exact rectangular "
            "material renamings; all stable-middle frames; all exact or "
            "reversed endpoint relations"
        ),
        "group_count": len(groups),
        "groups": [
            {key: value for key, value in group.items() if key != "wall_seconds"}
            for group in groups
        ],
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    for group in groups:
        print(
            f"group {group['group_number']} "
            f"projections={group['projection_count']} "
            f"renamings={group['exact_material_renaming_count']} "
            f"frames={group['stable_middle_frame_count']} "
            f"frame-relations={group['exact_endpoint_frame_relation_count']} "
            f"walks={group['frame_relation_walk_count']} "
            f"{group['wall_seconds']:.3f}s"
        )
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
