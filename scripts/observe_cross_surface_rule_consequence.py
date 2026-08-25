#!/usr/bin/env python3
"""Walk later raw material from relations shared by every multiplicity rule.

The operation first recovers complete cross-surface relations carried under
all four directional conflict rules.  Each shared relation is then held exact
while later raw material changes the relation consequences.  No rule or
orientation is preferred.

Plain source material is absent from the frozen artifact.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import time

from observe_cross_surface_relation_multiplicity import (
    RULES,
    SOURCE_GROUPS as MULTIPLICITY_SOURCE_GROUPS,
    _observe_group as _observe_multiplicity_group,
    _row_pairings,
    _rule_identity,
    _walk_coordinates,
)
from observe_cross_surface_structure import (
    SOURCE_GROUPS as EARLIER_SOURCE_GROUPS,
    _digest,
    _encoded,
    _material_identity,
    _projections,
)


OUTPUT = Path("/tmp/seed_cross_surface_rule_consequence_blind.json")

_FIRST, _SECOND, _THIRD, _FOURTH = EARLIER_SOURCE_GROUPS[0]

_SAME_FIRST_CHANGED_SECOND = (
    b"one plus one equals two\n"
    b"one add two equals three\n"
    b"two add two equals four\n"
    b"two add three equals five\n"
    b"three add three equals six\n"
)
_CHANGED_FIRST_SAME_SECOND = (
    b"1 + 1 = 2\n"
    b"1 * 2 = 3\n"
    b"2 * 2 = 4\n"
    b"2 * 3 = 5\n"
    b"3 * 3 = 6\n"
)
_BOTH_DIRECTIONAL_REPETITIONS_FIRST = (
    b"1 + 1 = 2\n"
    b"1 + 2 = 3\n"
    b"2 * 2 = 4\n"
    b"2 * 3 = 5\n"
    b"3 * 3 = 6\n"
)
_BOTH_DIRECTIONAL_REPETITIONS_LATER = (
    b"one plus one equals two\n"
    b"one add two equals three\n"
    b"two plus two equals four\n"
    b"two add three equals five\n"
    b"three add three equals six\n"
)

CONSEQUENCE_GROUPS = (
    (_FIRST, _SECOND),
    (_FIRST, _SAME_FIRST_CHANGED_SECOND),
    (_CHANGED_FIRST_SAME_SECOND, _SECOND),
    (
        _BOTH_DIRECTIONAL_REPETITIONS_FIRST,
        _BOTH_DIRECTIONAL_REPETITIONS_LATER,
    ),
)


def _raw_material_by_identity(projections: list[dict]) -> dict[str, bytes]:
    materials: dict[str, bytes] = {}
    for projection in projections:
        for row in projection["rows"]:
            for material in row:
                materials[_material_identity(material)] = material
    return materials


def _complete_relations_by_rule(group: dict) -> dict[str, set[tuple]]:
    findings: dict[str, set[tuple]] = {}
    for rule_finding in group["rule_findings"]:
        relations = {
            tuple(tuple(pair) for pair in continuation["complete_relation"])
            for relation in rule_finding["relation_continuations"]
            for continuation in relation["continuations"]
        }
        findings[rule_finding["rule_identity_sha256"]] = relations
    return findings


def _shared_complete_relations(group: dict) -> tuple[tuple, ...]:
    by_rule = _complete_relations_by_rule(group)
    shared = set.intersection(*(relations for relations in by_rule.values()))
    return tuple(sorted(shared))


def _resolve_relation(
    relation: tuple[tuple[str, str], ...],
    materials: dict[str, bytes],
) -> set[tuple[bytes, bytes]]:
    return {(materials[first], materials[later]) for first, later in relation}


def _walk_later_material(
    sources: tuple[bytes, ...],
    carried_pairs: set[tuple[bytes, bytes]],
    rule: dict[str, bool],
) -> dict:
    projections = [
        projection
        for source_number, material in enumerate(sources)
        for projection in _projections(source_number, material)
    ]
    first_materials = {first for first, _later in carried_pairs}
    later_materials = {later for _first, later in carried_pairs}
    addressed_projection_pairs = 0
    addressed_row_pairings = 0
    compatible = []

    for first in projections:
        first_carried = {material for row in first["rows"] for material in row}
        if not first_materials.issubset(first_carried):
            continue
        for later in projections:
            if (
                first["projection_identity_sha256"]
                == later["projection_identity_sha256"]
            ):
                continue
            later_carried = {
                material for row in later["rows"] for material in row
            }
            if not later_materials.issubset(later_carried):
                continue
            if (
                len(first["rows"]) != len(later["rows"])
                or len(first["rows"][0]) != len(later["rows"][0])
            ):
                continue
            addressed_projection_pairs += 1
            pairings = _row_pairings(
                first["rows"], later["rows"], carried_pairs, rule
            )
            addressed_row_pairings += len(pairings)
            for pairing in pairings:
                result = _walk_coordinates(
                    first["rows"], later["rows"], pairing, carried_pairs, rule
                )
                if result is None:
                    continue
                compatible.append(
                    {
                        "first_projection_identity_sha256": first[
                            "projection_identity_sha256"
                        ],
                        "later_projection_identity_sha256": later[
                            "projection_identity_sha256"
                        ],
                        **result,
                    }
                )

    unique = {
        (
            finding["first_projection_identity_sha256"],
            finding["later_projection_identity_sha256"],
            tuple(finding["row_pairing"]),
            tuple(tuple(pair) for pair in finding["complete_relation"]),
        ): finding
        for finding in compatible
    }
    ordered = sorted(
        unique.values(),
        key=lambda finding: (
            finding["first_projection_identity_sha256"],
            finding["later_projection_identity_sha256"],
            finding["row_pairing"],
            finding["complete_relation"],
        ),
    )
    return {
        "addressed_projection_pair_count": addressed_projection_pairs,
        "addressed_row_pairing_count": addressed_row_pairings,
        "compatible_count": len(ordered),
        "extension_count": sum(
            finding["added_pair_count"] > 0 for finding in ordered
        ),
        "findings": ordered,
    }


def observe() -> dict:
    begun = time.perf_counter()
    initial_sources = MULTIPLICITY_SOURCE_GROUPS[0]
    initial_projections = [
        projection
        for source_number, material in enumerate(initial_sources)
        for projection in _projections(source_number, material)
    ]
    materials = _raw_material_by_identity(initial_projections)
    initial = _observe_multiplicity_group(0, initial_sources)
    shared_relations = _shared_complete_relations(initial)

    consequence_groups = []
    for group_number, sources in enumerate(CONSEQUENCE_GROUPS):
        consequence_groups.append(
            {
                "group_number": group_number,
                "source_materials": [
                    {
                        "source_number": source_number,
                        "byte_count": len(material),
                        "material_sha256": sha256(material).hexdigest(),
                    }
                    for source_number, material in enumerate(sources)
                ],
                "shared_relation_findings": [
                    {
                        "shared_relation_identity_sha256": _digest(
                            _encoded(shared_relation)
                        ),
                        "rule_findings": [
                            {
                                "rule": rule,
                                "rule_identity_sha256": _rule_identity(rule),
                                **_walk_later_material(
                                    sources,
                                    _resolve_relation(shared_relation, materials),
                                    rule,
                                ),
                            }
                            for rule in RULES
                        ],
                    }
                    for shared_relation in shared_relations
                ],
            }
        )

    return {
        "operation": (
            "complete relations shared by all four directional conflict rules; "
            "each shared relation walks every later raw-material consequence "
            "under every rule"
        ),
        "initial_shared_relation_count": len(shared_relations),
        "consequence_groups": consequence_groups,
        "known_loss": None,
        "wall_seconds": time.perf_counter() - begun,
    }


def _frozen(result: dict) -> dict:
    return {key: value for key, value in result.items() if key != "wall_seconds"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    result = observe()
    frozen = _frozen(result)
    encoded = json.dumps(frozen, sort_keys=True, separators=(",", ":")).encode()
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {sha256(encoded).hexdigest()}")
    print(f"initial shared relations: {result['initial_shared_relation_count']}")
    for group in result["consequence_groups"]:
        rule_counts = [
            [
                finding["extension_count"]
                for finding in relation["rule_findings"]
            ]
            for relation in group["shared_relation_findings"]
        ]
        print(
            f"group {group['group_number']} "
            f"rules={rule_counts}"
        )
    print(f"wall seconds: {result['wall_seconds']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
