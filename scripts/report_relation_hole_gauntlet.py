"""Combine independently bounded relation-hole observer artifacts."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any


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
        family["relation_bearing_reference"],
    )


def _vacancy_key(family: dict[str, Any]) -> tuple[object, ...]:
    return (
        family["event_kind"],
        family["book_reference"],
        tuple(family["coordinate_path"]),
    )


def _coordinate_material(path: list[object]) -> list[str]:
    words = []
    for part in path:
        if not isinstance(part, str) or part == "#":
            continue
        words.extend(re.findall(r"[A-Za-z]+", part.replace("_", " ").lower()))
    return words


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
        if value.get("observer") != (
            "exact append-order occurrence references; bare handoffs are "
            "questions and establish no relation"
        ):
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
    coordinate_words: Counter[str] = Counter()
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
            coordinate_words.update(_coordinate_material(family["reference_path"]))
        for family in artifact["relation_coordinate_missing_content_families"]:
            missing_content_groups[_vacancy_key(family)].append((path, family))
            coordinate_words.update(_coordinate_material(family["coordinate_path"]))
        for family in artifact["unrendered_relation_occurrence_families"]:
            unrendered_groups[_vacancy_key(family)].append((path, family))
            coordinate_words.update(_coordinate_material(family["coordinate_path"]))

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
                    "relation_bearing_reference": first[
                        "relation_bearing_reference"
                    ],
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
        bearing = [member for _path, member in members if member["relation_bearing_reference"]]
        bare = [member for _path, member in members if not member["relation_bearing_reference"]]
        transition_rows.append(
            {
                "source_kind": source_kind,
                "destination_kind": destination_kind,
                "source_book_reference": source_book,
                "destination_book_reference": destination_book,
                "source_file_count": len({path.name for path, _member in members}),
                "bare_occurrence_pair_count": sum(
                    member["occurrence_pair_count"] for member in bare
                ),
                "relation_bearing_occurrence_pair_count": sum(
                    member["occurrence_pair_count"] for member in bearing
                ),
                "bare_samples": [
                    {"artifact": path.name, **member["samples"][0]}
                    for path, member in members
                    if not member["relation_bearing_reference"]
                    and member["samples"]
                ][:3],
                "relation_bearing_samples": [
                    {"artifact": path.name, **member["samples"][0]}
                    for path, member in members
                    if member["relation_bearing_reference"] and member["samples"]
                ][:3],
            }
        )
    transition_rows.sort(
        key=lambda item: (
            bool(item["relation_bearing_occurrence_pair_count"]),
            -item["source_file_count"],
            -item["bare_occurrence_pair_count"],
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
        "opaque_coordinate_material": [
            {"material": word, "occurrence_count": count}
            for word, count in sorted(
                coordinate_words.items(), key=lambda item: (-item[1], item[0])
            )
        ],
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
