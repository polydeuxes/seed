"""Project a complete monolithic internal-variation artifact into source shards.

This changes representation only.  It refuses an input carrying known loss,
preserves each complete source finding verbatim beneath a source wrapper, and
emits a digest manifest over the independently bounded source artifacts.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


INPUT = Path("/tmp/seed_open_world_internal_variation_blind.json")
OUTPUT = Path("/tmp/seed_open_world_internal_variation_manifest.json")
SOURCE_OUTPUT_DIRECTORY = Path(
    "/tmp/seed_open_world_internal_variation_sources"
)


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: bytes) -> str:
    return sha256(value).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--source-output-directory",
        type=Path,
        default=SOURCE_OUTPUT_DIRECTORY,
    )
    arguments = parser.parse_args()

    monolith = json.loads(arguments.input.read_text(encoding="utf-8"))
    if monolith["known_loss"] is not None:
        raise ValueError("cannot shard an unfinished internal-variation artifact")
    arguments.source_output_directory.mkdir(parents=True, exist_ok=True)
    source_artifacts = []
    for source in monolith["sources"]:
        source_finding = {
            "operation": monolith["operation"],
            "source": source,
            "known_loss": None,
        }
        encoded = _canonical(source_finding)
        source_reference = _digest(source["source"].encode())
        artifact_sha256 = _digest(encoded)
        output = (
            arguments.source_output_directory
            / f"{source_reference}-{artifact_sha256}.json"
        )
        output.write_bytes(encoded)
        source_artifacts.append(
            {
                "source": source["source"],
                "first_line": source["first_line"],
                "line_count": source["line_count"],
                "material_sha256": source["material_sha256"],
                "artifact": str(output),
                "artifact_bytes": len(encoded),
                "artifact_sha256": artifact_sha256,
                "recurrent_surface_count": source["recurrent_surface_count"],
                "varying_surface_finding_count": len(
                    source["varying_surface_findings"]
                ),
                "varying_surface_count_by_position_count": source[
                    "varying_surface_count_by_position_count"
                ],
                "maximum_recurrent_coordinate_count": source[
                    "maximum_recurrent_coordinate_count"
                ],
            }
        )
    manifest = {
        "source_aperture_artifact_sha256": monolith[
            "source_aperture_artifact_sha256"
        ],
        "operation": monolith["operation"],
        "source_artifacts": source_artifacts,
        "known_loss": None,
    }
    encoded = _canonical(manifest)
    arguments.output.write_bytes(encoded)
    print(f"source artifacts: {len(source_artifacts)}")
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
