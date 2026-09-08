"""Render exact pressure from sharded open-world internal variation findings."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


INPUT = Path("/tmp/seed_open_world_internal_variation_manifest.json")
OUTPUT = Path("/tmp/seed_open_world_internal_variation_pressure.json")
SAMPLE_COUNT = 24


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: bytes) -> str:
    return sha256(value).hexdigest()


def _scalar_values(source: dict) -> tuple[str, ...]:
    return tuple(
        bytes.fromhex(record["utf8_hex"]).decode("utf-8")
        for record in source["scalar_materials"]
    )


def _production_material(
    finding: dict,
    production: dict,
    scalar_values: tuple[str, ...],
) -> str:
    coordinate_values = [
        scalar_values[index]
        for index in production["coordinate_material_indexes"]
    ]
    material = [""] * finding["coordinate_count"]
    for positions, value in zip(
        finding["coordinate_classes"], coordinate_values
    ):
        for position in positions:
            material[position] = value
    if any(value == "" for value in material):
        raise AssertionError("one production leaves a source coordinate empty")
    return "".join(material)


def _render(value: str) -> str:
    return value.encode("unicode_escape").decode("ascii")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    manifest_bytes = arguments.input.read_bytes()
    manifest = json.loads(manifest_bytes)
    position_histogram: Counter[int] = Counter()
    multi_position_extent_histogram: Counter[int] = Counter()
    source_results = []
    samples = []

    for source_address in manifest["source_artifacts"]:
        artifact_path = Path(source_address["artifact"])
        artifact_bytes = artifact_path.read_bytes()
        if len(artifact_bytes) != source_address["artifact_bytes"]:
            raise ValueError("source artifact byte count differs from manifest")
        if _digest(artifact_bytes) != source_address["artifact_sha256"]:
            raise ValueError("source artifact digest differs from manifest")
        artifact = json.loads(artifact_bytes)
        source = artifact["source"]
        scalar_values = _scalar_values(source)
        source_histogram = Counter(
            {
                int(key): value
                for key, value in source[
                    "varying_surface_count_by_position_count"
                ].items()
            }
        )
        position_histogram.update(source_histogram)
        multi_findings = [
            finding
            for finding in source["varying_surface_findings"]
            if finding["source_addressed_varying_position_count"] > 1
        ]
        multi_position_extent_histogram.update(
            finding["coordinate_count"] for finding in multi_findings
        )
        source_results.append(
            {
                "source": source["source"],
                "source_artifact_sha256": source_address["artifact_sha256"],
                "recurrent_surface_count": source["recurrent_surface_count"],
                "source_addressed_varying_position_histogram": dict(
                    sorted(source_histogram.items())
                ),
                "multi_position_surface_count": len(multi_findings),
                "maximum_source_addressed_varying_position_count": max(
                    (
                        finding["source_addressed_varying_position_count"]
                        for finding in multi_findings
                    ),
                    default=0,
                ),
                "maximum_multi_position_coordinate_count": max(
                    (finding["coordinate_count"] for finding in multi_findings),
                    default=0,
                ),
            }
        )

        for finding in multi_findings:
            productions = finding["recurrent_exact_productions"]
            productions_in_source_order = sorted(
                productions,
                key=lambda production: production["support_start_indexes"][0],
            )
            rendered_productions = [
                {
                    "material": _render(
                        _production_material(finding, production, scalar_values)
                    ),
                    "source_occurrence_count": len(
                        production["support_start_indexes"]
                    ),
                }
                for production in productions_in_source_order[:8]
            ]
            sample = {
                "source": source["source"],
                "finding_reference": finding["finding_reference"],
                "coordinate_count": finding["coordinate_count"],
                "source_occurrence_count": finding["source_occurrence_count"],
                "coordinate_class_count": len(finding["coordinate_classes"]),
                "source_addressed_varying_position_count": finding[
                    "source_addressed_varying_position_count"
                ],
                "varying_coordinate_classes": [
                    {
                        "coordinate_class_number": value[
                            "coordinate_class_number"
                        ],
                        "source_coordinate_positions": value[
                            "source_coordinate_positions"
                        ],
                        "recurrent_substitution_frame_count": value[
                            "recurrent_substitution_frame_count"
                        ],
                    }
                    for value in finding["variation_positions"]
                ],
                "recurrent_exact_production_count": len(productions),
                "first_exact_productions_in_source_order": rendered_productions,
            }
            samples.append(sample)

    samples.sort(
        key=lambda value: (
            -value["source_addressed_varying_position_count"],
            -value["coordinate_count"],
            -value["source_occurrence_count"],
            value["source"],
            value["finding_reference"],
        )
    )
    finding = {
        "internal_variation_manifest_sha256": _digest(manifest_bytes),
        "source_artifact_count": len(source_results),
        "known_loss": manifest["known_loss"],
        "source_addressed_varying_position_histogram": dict(
            sorted(position_histogram.items())
        ),
        "multi_position_extent_histogram": dict(
            sorted(multi_position_extent_histogram.items())
        ),
        "source_results": source_results,
        "strongest_source_addressed_examples": samples[:SAMPLE_COUNT],
        "finding": (
            "source-derived recurrent extents can expose several separately "
            "varying coordinate classes without a requested slot count; this "
            "does not establish direction among those coordinates"
        ),
    }
    encoded = _canonical(finding)
    arguments.output.write_bytes(encoded)

    print(
        "varying-position histogram: "
        f"{dict(sorted(position_histogram.items()))}"
    )
    print(
        "multi-position extent histogram: "
        f"{dict(sorted(multi_position_extent_histogram.items()))}"
    )
    print("strongest exact samples:")
    for sample in samples[:12]:
        materials = [
            production["material"]
            for production in sample["first_exact_productions_in_source_order"][:4]
        ]
        print(
            f"  n={sample['source_addressed_varying_position_count']:2} "
            f"k={sample['coordinate_count']:3} "
            f"support={sample['source_occurrence_count']:6} "
            f"{sample['source']} {materials}"
        )
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
