"""Measure exact scalar sameness between inward frames and their neighbors.

This findings-only observer applies the same operation to every frozen frame.
It reads top-level scalar coordinates from the frozen occurrence source but no
event label, Book coordinate, machine grammar, runtime constant, or requested
coordinate name. Exact values are represented only by type and digest.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path


SOURCE = Path("/tmp/seed_inward_occurrence_material.json")
SURFACES = Path("/tmp/seed_inward_occurrence_surfaces_blind.json")
FRAMES = Path("/tmp/seed_inward_coordinate_frames_blind.json")
OUTPUT = Path("/tmp/seed_inward_frame_neighbor_equalities_blind.json")


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _coordinate_digest(material: str) -> str:
    return _digest(material.encode())


def _scalar_coordinates(material: dict) -> dict[tuple[str, str], list[str]]:
    by_value: dict[tuple[str, str], list[str]] = defaultdict(list)
    for coordinate, value in material.items():
        scalar_type = (
            "none"
            if value is None
            else "boolean"
            if type(value) is bool
            else "integer"
            if type(value) is int
            else "number"
            if type(value) is float
            else "text"
            if type(value) is str
            else None
        )
        if scalar_type is None:
            continue
        value_digest = _digest(_encoded([scalar_type, value]))
        by_value[(scalar_type, value_digest)].append(
            _coordinate_digest(coordinate)
        )
    return by_value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--surfaces", type=Path, default=SURFACES)
    parser.add_argument("--frames", type=Path, default=FRAMES)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    source_bytes = arguments.source.read_bytes()
    surface_bytes = arguments.surfaces.read_bytes()
    frame_bytes = arguments.frames.read_bytes()
    source = json.loads(source_bytes)
    surfaces = json.loads(surface_bytes)
    frames = json.loads(frame_bytes)
    if any(
        artifact.get("known_loss") is not None
        for artifact in (source, surfaces, frames)
    ):
        raise ValueError("one inward artifact carries known loss")
    if surfaces.get("source_artifact_sha256") != _digest(source_bytes):
        raise ValueError("occurrence surfaces do not address the supplied source")
    if frames.get("occurrence_surface_artifact_sha256") != _digest(surface_bytes):
        raise ValueError("coordinate frames do not address the supplied surfaces")

    surface_at = {}
    for surface in surfaces["surfaces"]:
        for address in surface["occurrences"]:
            key = tuple(address)
            if key in surface_at:
                raise ValueError("one append address carries two surfaces")
            surface_at[key] = surface["coordinate_surface_sha256"]

    source_materials = []
    for recorded_source in source["sources"]:
        materials = []
        for occurrence in recorded_source["occurrences"]:
            expected = len(materials)
            if occurrence["append_position"] != expected:
                raise ValueError("source occurrence addresses are not exact")
            materials.append(occurrence["material"])
        source_materials.append(materials)

    equalities_by_surface = defaultdict(lambda: defaultdict(list))
    for source_number, materials in enumerate(source_materials):
        scalars = [_scalar_coordinates(material) for material in materials]
        for append_position, current in enumerate(scalars):
            current_surface = surface_at[(source_number, append_position)]
            for direction, neighbor_position in (
                ("prior", append_position - 1),
                ("later", append_position + 1),
            ):
                if neighbor_position < 0 or neighbor_position >= len(materials):
                    continue
                neighbor = scalars[neighbor_position]
                for scalar in current.keys() & neighbor.keys():
                    scalar_type, value_digest = scalar
                    for current_coordinate in current[scalar]:
                        for neighbor_coordinate in neighbor[scalar]:
                            equalities_by_surface[current_surface][
                                (
                                    direction,
                                    current_coordinate,
                                    neighbor_coordinate,
                                    scalar_type,
                                    value_digest,
                                )
                            ].append([source_number, append_position])

    findings = []
    for frame_number, frame in enumerate(frames["frames"]):
        frame_coordinates = set(frame["coordinate_material_sha256s"])
        combined = defaultdict(list)
        for surface in frame["coordinate_surface_sha256s"]:
            for equality, occurrences in equalities_by_surface[surface].items():
                if equality[1] not in frame_coordinates:
                    continue
                combined[equality].extend(occurrences)
        equalities = []
        for equality, occurrences in combined.items():
            addressed_sources = {source_number for source_number, _ in occurrences}
            if len(addressed_sources) != len(source_materials):
                continue
            (
                direction,
                current_coordinate,
                neighbor_coordinate,
                scalar_type,
                value_digest,
            ) = equality
            equalities.append(
                {
                    "direction": direction,
                    "frame_coordinate_material_sha256": current_coordinate,
                    "neighbor_coordinate_material_sha256": neighbor_coordinate,
                    "scalar_type": scalar_type,
                    "scalar_value_sha256": value_digest,
                    "occurrences": sorted(occurrences),
                    "occurrence_count": len(occurrences),
                    "source_count": len(addressed_sources),
                }
            )
        equalities.sort(
            key=lambda finding: (
                finding["direction"],
                finding["frame_coordinate_material_sha256"],
                finding["neighbor_coordinate_material_sha256"],
                finding["scalar_type"],
                finding["scalar_value_sha256"],
            )
        )
        findings.append(
            {
                "frame_number": frame_number,
                "coordinate_material_sha256s": frame[
                    "coordinate_material_sha256s"
                ],
                "source_recurring_neighbor_equalities": equalities,
            }
        )

    result = {
        "source_artifact_sha256": _digest(source_bytes),
        "occurrence_surface_artifact_sha256": _digest(surface_bytes),
        "coordinate_frame_artifact_sha256": _digest(frame_bytes),
        "operation": (
            "exact top-level scalar sameness from every frozen frame occurrence "
            "to its immediate prior and later occurrence, retaining findings "
            "addressed in every supplied source"
        ),
        "frame_count": len(findings),
        "findings": findings,
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"frames measured: {len(findings)}")
    print(
        "source-recurring equalities: "
        f"{sum(len(f['source_recurring_neighbor_equalities']) for f in findings)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
