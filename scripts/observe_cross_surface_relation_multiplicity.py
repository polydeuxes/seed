#!/usr/bin/env python3
"""Pressure-test directional multiplicity in cross-surface relation walks.

The operation begins with raw bytes and the same blind projection/frame
physiology as the earlier cross-surface observers.  For every exact frame
relation it walks all four directional conflict rules.  No rule is preferred.

Plain source material is absent from the frozen artifact.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import time

from observe_cross_surface_structure import (
    SOURCE_GROUPS as EARLIER_SOURCE_GROUPS,
    _digest,
    _encoded,
    _frame_relations,
    _frames,
    _material_identity,
    _projections,
)


OUTPUT = Path("/tmp/seed_cross_surface_relation_multiplicity_blind.json")

_MANY_TO_ONE_FIRST = (
    b"qa : qa = td\n"
    b"rb : rb = td\n"
    b"sc : sc = td\n"
)
_MANY_TO_ONE_LATER = (
    b"zu ; zu ~ vx\n"
    b"zu ; zu ~ vx\n"
    b"zu ; zu ~ vx\n"
)
_MANY_TO_ONE_BRIDGE = b"qa @ zu\nrb @ zu\nsc @ zu\n"
_MANY_TO_ONE_REVERSED = b"zu # qa\nzu # rb\nzu # sc\n"

SOURCE_GROUPS = (
    EARLIER_SOURCE_GROUPS[0],
    (
        _MANY_TO_ONE_FIRST,
        _MANY_TO_ONE_LATER,
        _MANY_TO_ONE_BRIDGE,
        _MANY_TO_ONE_REVERSED,
    ),
    (_MANY_TO_ONE_BRIDGE, _MANY_TO_ONE_REVERSED),
)

RULES = tuple(
    {
        "same_first_changed_second_conflicts": first_conflicts,
        "changed_first_same_second_conflicts": second_conflicts,
    }
    for first_conflicts in (False, True)
    for second_conflicts in (False, True)
)


def _rule_identity(rule: dict[str, bool]) -> str:
    return _digest(_encoded(rule))


def _pair_can_enter(
    carried_pairs: set[tuple[bytes, bytes]],
    proposed_pair: tuple[bytes, bytes],
    rule: dict[str, bool],
) -> bool:
    first, later = proposed_pair
    if proposed_pair in carried_pairs:
        return True
    if rule["same_first_changed_second_conflicts"] and any(
        carried_first == first and carried_later != later
        for carried_first, carried_later in carried_pairs
    ):
        return False
    if rule["changed_first_same_second_conflicts"] and any(
        carried_later == later and carried_first != first
        for carried_first, carried_later in carried_pairs
    ):
        return False
    return True


def _relation_from_pairs(
    pairs: tuple[tuple[bytes, bytes], ...],
    rule: dict[str, bool],
) -> set[tuple[bytes, bytes]] | None:
    carried: set[tuple[bytes, bytes]] = set()
    for pair in pairs:
        if not _pair_can_enter(carried, pair, rule):
            return None
        carried.add(pair)
    return carried


def _frame_orientations(frame: dict, rule: dict[str, bool]) -> tuple[dict, ...]:
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
        carried = _relation_from_pairs(oriented, rule)
        if carried is None:
            continue
        material = {
            "orientation": name,
            "anchor_pairs": [
                [_material_identity(first), _material_identity(later)]
                for first, later in sorted(carried)
            ],
            "rule_identity_sha256": _rule_identity(rule),
        }
        findings.append(
            {
                **material,
                "orientation_identity_sha256": _digest(_encoded(material)),
                "_raw_pairs": carried,
            }
        )
    return tuple(findings)


def _row_can_answer(
    first_row: tuple[bytes, ...],
    later_row: tuple[bytes, ...],
    carried_pairs: set[tuple[bytes, bytes]],
    rule: dict[str, bool],
) -> bool:
    proposed = set(carried_pairs)
    for pair in zip(first_row, later_row, strict=True):
        if not _pair_can_enter(proposed, pair, rule):
            return False
        proposed.add(pair)
    return True


def _row_pairings(
    first_rows: tuple[tuple[bytes, ...], ...],
    later_rows: tuple[tuple[bytes, ...], ...],
    carried_pairs: set[tuple[bytes, bytes]],
    rule: dict[str, bool],
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
            if _row_can_answer(first_row, later_row, carried_pairs, rule)
        )
        for first_row in first_rows
    )
    if any(not row_answers for row_answers in answers):
        return ()

    order = tuple(
        sorted(range(len(first_rows)), key=lambda number: len(answers[number]))
    )
    assigned = [-1] * len(first_rows)
    used: set[int] = set()
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
            used.add(later_number)
            walk(position + 1)
            used.remove(later_number)
            assigned[first_number] = -1

    walk(0)
    return tuple(findings)


def _walk_coordinates(
    first_rows: tuple[tuple[bytes, ...], ...],
    later_rows: tuple[tuple[bytes, ...], ...],
    row_pairing: tuple[int, ...],
    anchor_pairs: set[tuple[bytes, bytes]],
    rule: dict[str, bool],
) -> dict | None:
    carried_pairs = set(anchor_pairs)
    added = []
    for first_row_number, coordinate in (
        (row_number, coordinate)
        for row_number in range(len(first_rows))
        for coordinate in range(len(first_rows[row_number]))
    ):
        later_row_number = row_pairing[first_row_number]
        pair = (
            first_rows[first_row_number][coordinate],
            later_rows[later_row_number][coordinate],
        )
        if not _pair_can_enter(carried_pairs, pair, rule):
            return None
        if pair not in carried_pairs:
            carried_pairs.add(pair)
            added.append(
                {
                    "first_row": first_row_number,
                    "later_row": later_row_number,
                    "coordinate": coordinate,
                    "first_material_sha256": _material_identity(pair[0]),
                    "later_material_sha256": _material_identity(pair[1]),
                }
            )

    if any(
        any(
            (first, later) not in carried_pairs
            for first, later in zip(
                first_rows[first_row_number],
                later_rows[later_row_number],
                strict=True,
            )
        )
        for first_row_number, later_row_number in enumerate(row_pairing)
    ):
        return None

    material = {
        "row_pairing": list(row_pairing),
        "added_pairs": added,
        "complete_relation": [
            [_material_identity(first), _material_identity(later)]
            for first, later in sorted(carried_pairs)
        ],
    }
    return {
        **material,
        "continuation_identity_sha256": _digest(_encoded(material)),
        "complete_relation_pair_count": len(carried_pairs),
        "added_pair_count": len(carried_pairs) - len(anchor_pairs),
    }


def _relation_continuations(
    relation: dict,
    frames_by_identity: dict[str, dict],
    projections: list[dict],
    rule: dict[str, bool],
) -> dict:
    first_frame = frames_by_identity[relation["first_frame_identity_sha256"]]
    orientations = _frame_orientations(first_frame, rule)
    findings = []

    for orientation in orientations:
        carried_pairs = orientation["_raw_pairs"]
        first_materials = {first for first, _later in carried_pairs}
        later_materials = {later for _first, later in carried_pairs}
        for first in projections:
            carried_first = {item for row in first["rows"] for item in row}
            if not first_materials.issubset(carried_first):
                continue
            for later in projections:
                if (
                    first["projection_identity_sha256"]
                    == later["projection_identity_sha256"]
                ):
                    continue
                carried_later = {item for row in later["rows"] for item in row}
                if not later_materials.issubset(carried_later):
                    continue
                pairings = _row_pairings(
                    first["rows"], later["rows"], carried_pairs, rule
                )
                for pairing in pairings:
                    continuation = _walk_coordinates(
                        first["rows"], later["rows"], pairing, carried_pairs, rule
                    )
                    if continuation is None or continuation["added_pair_count"] == 0:
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
            tuple(tuple(pair) for pair in finding["complete_relation"]),
        ): finding
        for finding in findings
    }
    return {
        "rule_identity_sha256": _rule_identity(rule),
        "orientation_count": len(orientations),
        "continuation_count": len(unique),
        "continuations": sorted(
            unique.values(),
            key=lambda finding: (
                finding["orientation_identity_sha256"],
                finding["first_projection_identity_sha256"],
                finding["later_projection_identity_sha256"],
                finding["complete_relation"],
            ),
        ),
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
        "rule_findings": [
            {
                "rule": rule,
                "rule_identity_sha256": _rule_identity(rule),
                "relation_continuations": [
                    _relation_continuations(
                        relation, frames_by_identity, projections, rule
                    )
                    for relation in relations
                ],
            }
            for rule in RULES
        ],
        "known_loss": None,
        "wall_seconds": time.perf_counter() - begun,
    }


def observe() -> dict:
    groups = [
        _observe_group(group_number, sources)
        for group_number, sources in enumerate(SOURCE_GROUPS)
    ]
    return {
        "operation": (
            "all recurring-byte projections; all source-supported frame relations; "
            "all four directional pair-conflict rules; exact coordinate continuation"
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
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {sha256(encoded).hexdigest()}")
    for group in result["groups"]:
        rule_counts = [
            (
                item["rule"],
                [
                    relation["continuation_count"]
                    for relation in item["relation_continuations"]
                ],
            )
            for item in group["rule_findings"]
        ]
        print(
            f"group {group['group_number']} "
            f"projections={group['projection_count']} "
            f"frames={group['frame_count']} "
            f"relations={group['frame_relation_count']} "
            f"rules={rule_counts}"
        )
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
