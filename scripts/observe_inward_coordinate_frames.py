"""Enumerate closed coordinate frames from frozen blind occurrence surfaces.

This findings-only observer reads no occurrence label, Book coordinate, machine
grammar, runtime constant, or expected frame. It intersects every exact
top-level coordinate surface until no new intersection exists, then retains
each closed frame carried by at least two distinct surfaces and every supplied
source.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


INPUT = Path("/tmp/seed_inward_occurrence_surfaces_blind.json")
OUTPUT = Path("/tmp/seed_inward_coordinate_frames_blind.json")


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    input_bytes = arguments.input.read_bytes()
    observed = json.loads(input_bytes)
    if observed.get("known_loss") is not None:
        raise ValueError("blind occurrence-surface artifact carries known loss")
    surfaces = observed["surfaces"]
    source_count = len(observed["source_occurrence_counts"])

    frames = {
        frozenset(surface["coordinate_material_sha256s"])
        for surface in surfaces
    }
    prior_count = -1
    while len(frames) != prior_count:
        prior_count = len(frames)
        current = list(frames)
        for first_number, first in enumerate(current):
            for second in current[first_number + 1 :]:
                intersection = first & second
                if intersection:
                    frames.add(intersection)

    findings = []
    for frame in frames:
        carrying = [
            surface
            for surface in surfaces
            if frame.issubset(surface["coordinate_material_sha256s"])
        ]
        if len(carrying) < 2:
            continue
        exact_intersection = set(carrying[0]["coordinate_material_sha256s"])
        for surface in carrying[1:]:
            exact_intersection.intersection_update(
                surface["coordinate_material_sha256s"]
            )
        if exact_intersection != set(frame):
            continue
        occurrences = [
            occurrence
            for surface in carrying
            for occurrence in surface["occurrences"]
        ]
        sources = {source_number for source_number, _position in occurrences}
        if len(sources) != source_count:
            continue
        findings.append(
            {
                "coordinate_material_sha256s": sorted(frame),
                "coordinate_count": len(frame),
                "coordinate_surface_sha256s": sorted(
                    surface["coordinate_surface_sha256"] for surface in carrying
                ),
                "coordinate_surface_count": len(carrying),
                "occurrence_count": len(occurrences),
                "source_count": len(sources),
            }
        )
    findings.sort(
        key=lambda finding: (
            -finding["coordinate_count"],
            -finding["coordinate_surface_count"],
            finding["coordinate_material_sha256s"],
        )
    )

    result = {
        "occurrence_surface_artifact_sha256": _digest(input_bytes),
        "operation": (
            "all closed nonempty intersections of exact top-level coordinate "
            "surfaces, retaining frames carried by at least two distinct "
            "surfaces and every supplied source"
        ),
        "intersected_frame_count": len(frames),
        "source_recurring_closed_frame_count": len(findings),
        "frames": findings,
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"intersected frames: {len(frames)}")
    print(f"source-recurring closed frames: {len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
