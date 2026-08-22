"""Combine independently bounded relation-hole observer artifacts."""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.observe_relation_holes import OBSERVER_STATEMENT  # noqa: E402


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def _family_key(family: dict[str, Any]) -> tuple[object, ...]:
    return (
        family["source_kind"],
        family["destination_kind"],
        tuple(family["reference_path"]),
        family["source_book_reference"],
        family["destination_book_reference"],
        family["recorded_relation"],
    )


def _vacancy_key(family: dict[str, Any]) -> tuple[object, ...]:
    return (
        family["event_kind"],
        family["book_reference"],
        tuple(family["coordinate_path"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    artifacts = []
    for path in sorted(arguments.directory.glob("*.json")):
        if path.name == "manifest.json" or path == arguments.output:
            continue
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("observer") != OBSERVER_STATEMENT:
            continue
        artifacts.append((path, value))

    reference_groups: dict[tuple[object, ...], list[tuple[Path, dict[str, Any]]]] = (
        defaultdict(list)
    )
    transition_groups: dict[
        tuple[object, ...], list[tuple[Path, dict[str, Any]]]
    ] = defaultdict(list)
    missing_content_groups = defaultdict(list)
    unrendered_groups = defaultdict(list)
    for path, artifact in artifacts:
        for family in artifact["reference_transition_families"]:
            transition_key = (
                family["source_kind"],
                family["destination_kind"],
                family["source_book_reference"],
                family["destination_book_reference"],
            )
            transition_groups[transition_key].append((path, family))
        for family in artifact["repeated_bare_handoff_families"]:
            reference_groups[_family_key(family)].append((path, family))
        for family in artifact["relation_coordinate_missing_content_families"]:
            missing_content_groups[_vacancy_key(family)].append((path, family))
        for family in artifact["unrendered_relation_occurrence_families"]:
            unrendered_groups[_vacancy_key(family)].append((path, family))

    def merged_references():
        result = []
        for key, members in reference_groups.items():
            first = members[0][1]
            result.append(
                {
                    "source_kind": first["source_kind"],
                    "destination_kind": first["destination_kind"],
                    "reference_path": first["reference_path"],
                    "source_book_reference": first["source_book_reference"],
                    "destination_book_reference": first[
                        "destination_book_reference"
                    ],
                    "recorded_relation": first["recorded_relation"],
                    "source_file_count": len(members),
                    "occurrence_count": sum(
                        member["occurrence_count"] for _path, member in members
                    ),
                    "test_count": sum(
                        member["test_count"] for _path, member in members
                    ),
                    "maximum_later_rungs": max(
                        member["maximum_later_rungs"]
                        for _path, member in members
                    ),
                    "source_artifacts": [path.name for path, _member in members],
                    "samples": [
                        {"artifact": path.name, **member["samples"][0]}
                        for path, member in members[:3]
                        if member["samples"]
                    ],
                }
            )
        result.sort(
            key=lambda item: (
                -item["source_file_count"],
                -item["test_count"],
                -item["occurrence_count"],
                item["source_kind"],
                item["destination_kind"],
                tuple(map(str, item["reference_path"])),
            )
        )
        return result

    def merged_vacancies(groups):
        result = []
        for _key, members in groups.items():
            first = members[0][1]
            result.append(
                {
                    "event_kind": first["event_kind"],
                    "book_reference": first["book_reference"],
                    "coordinate_path": first["coordinate_path"],
                    "source_file_count": len(members),
                    "occurrence_count": sum(
                        member["occurrence_count"] for _path, member in members
                    ),
                    "test_count": sum(
                        member["test_count"] for _path, member in members
                    ),
                    "source_artifacts": [path.name for path, _member in members],
                    "samples": [
                        {"artifact": path.name, **member["samples"][0]}
                        for path, member in members[:3]
                        if member["samples"]
                    ],
                }
            )
        result.sort(
            key=lambda item: (
                -item["source_file_count"],
                -item["test_count"],
                -item["occurrence_count"],
                item["event_kind"],
                tuple(map(str, item["coordinate_path"])),
            )
        )
        return result

    transition_rows = []
    for key, members in transition_groups.items():
        source_kind, destination_kind, source_book, destination_book = key
        carried = [
            member
            for _path, member in members
            if member["recorded_relation"] != "no_recorded_relation"
        ]
        uncarried = [
            member
            for _path, member in members
            if member["recorded_relation"] == "no_recorded_relation"
        ]
        transition_rows.append(
            {
                "source_kind": source_kind,
                "destination_kind": destination_kind,
                "source_book_reference": source_book,
                "destination_book_reference": destination_book,
                "source_file_count": len({path.name for path, _member in members}),
                "no_recorded_relation_occurrence_pair_count": sum(
                    member["occurrence_pair_count"] for member in uncarried
                ),
                "recorded_relation_occurrence_pair_count": sum(
                    member["occurrence_pair_count"] for member in carried
                ),
                "no_recorded_relation_samples": [
                    {"artifact": path.name, **member["samples"][0]}
                    for path, member in members
                    if member["recorded_relation"] == "no_recorded_relation"
                    and member["samples"]
                ][:3],
                "recorded_relation_samples": [
                    {"artifact": path.name, **member["samples"][0]}
                    for path, member in members
                    if member["recorded_relation"] != "no_recorded_relation"
                    and member["samples"]
                ][:3],
            }
        )
    transition_rows.sort(
        key=lambda item: (
            bool(item["recorded_relation_occurrence_pair_count"]),
            -item["source_file_count"],
            -item["no_recorded_relation_occurrence_pair_count"],
            item["source_kind"],
            item["destination_kind"],
        )
    )

    result = {
        "observer": "combined independently bounded relation-hole populations",
        "artifact_count": len(artifacts),
        "captured_test_count": sum(
            artifact["captured_test_count"] for _path, artifact in artifacts
        ),
        "event_count": sum(
            artifact["event_count"] for _path, artifact in artifacts
        ),
        "reference_edge_count": sum(
            artifact["reference_edge_count"] for _path, artifact in artifacts
        ),
        "repeated_bare_handoff_families": merged_references(),
        "reference_transition_coverage": transition_rows,
        "relation_coordinate_missing_content_families": merged_vacancies(
            missing_content_groups
        ),
        "unrendered_relation_occurrence_families": merged_vacancies(
            unrendered_groups
        ),
    }
    result["structural_digest"] = _digest(result)
    arguments.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(
        f"{arguments.output} artifacts={result['artifact_count']} "
        f"tests={result['captured_test_count']} events={result['event_count']} "
        f"digest={result['structural_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
