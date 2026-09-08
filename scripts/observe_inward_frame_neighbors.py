"""Measure immediate source-order neighbors of every frozen inward frame.

This findings-only observer reads the blind occurrence surfaces and blind closed
coordinate frames. It receives no target frame, occurrence label, Book
coordinate, machine grammar, or expected direction. Every frozen frame is
given the same immediate prior/later measurement.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


SURFACES = Path("/tmp/seed_inward_occurrence_surfaces_blind.json")
FRAMES = Path("/tmp/seed_inward_coordinate_frames_blind.json")
OUTPUT = Path("/tmp/seed_inward_frame_neighbors_blind.json")


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _counts(counter: Counter[str]) -> list[dict[str, object]]:
    return [
        {"coordinate_surface_sha256": surface, "occurrence_count": count}
        for surface, count in sorted(counter.items())
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surfaces", type=Path, default=SURFACES)
    parser.add_argument("--frames", type=Path, default=FRAMES)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    surface_bytes = arguments.surfaces.read_bytes()
    frame_bytes = arguments.frames.read_bytes()
    surfaces = json.loads(surface_bytes)
    frames = json.loads(frame_bytes)
    if surfaces.get("known_loss") is not None or frames.get("known_loss") is not None:
        raise ValueError("one blind inward artifact carries known loss")
    if frames.get("occurrence_surface_artifact_sha256") != _digest(surface_bytes):
        raise ValueError("coordinate frames do not address the supplied surfaces")

    sequences = [
        [None] * occurrence_count
        for occurrence_count in surfaces["source_occurrence_counts"]
    ]
    for surface in surfaces["surfaces"]:
        identity = surface["coordinate_surface_sha256"]
        for source_number, append_position in surface["occurrences"]:
            if sequences[source_number][append_position] is not None:
                raise ValueError("one append address carries two coordinate surfaces")
            sequences[source_number][append_position] = identity
    if any(any(identity is None for identity in sequence) for sequence in sequences):
        raise ValueError("one append address carries no coordinate surface")

    findings = []
    for frame_number, frame in enumerate(frames["frames"]):
        carrying_surfaces = set(frame["coordinate_surface_sha256s"])
        prior = Counter()
        later = Counter()
        pairs = Counter()
        first_boundary_count = 0
        last_boundary_count = 0
        addressed = []
        for source_number, sequence in enumerate(sequences):
            for append_position, surface in enumerate(sequence):
                if surface not in carrying_surfaces:
                    continue
                prior_surface = (
                    None if append_position == 0 else sequence[append_position - 1]
                )
                later_surface = (
                    None
                    if append_position + 1 == len(sequence)
                    else sequence[append_position + 1]
                )
                if prior_surface is None:
                    first_boundary_count += 1
                else:
                    prior[prior_surface] += 1
                if later_surface is None:
                    last_boundary_count += 1
                else:
                    later[later_surface] += 1
                if prior_surface is not None and later_surface is not None:
                    pairs[(prior_surface, later_surface)] += 1
                addressed.append([source_number, append_position])
        findings.append(
            {
                "frame_number": frame_number,
                "coordinate_material_sha256s": frame[
                    "coordinate_material_sha256s"
                ],
                "addressed_occurrences": addressed,
                "prior_coordinate_surfaces": _counts(prior),
                "later_coordinate_surfaces": _counts(later),
                "prior_later_coordinate_surface_pairs": [
                    {
                        "prior_coordinate_surface_sha256": pair[0],
                        "later_coordinate_surface_sha256": pair[1],
                        "occurrence_count": count,
                    }
                    for pair, count in sorted(pairs.items())
                ],
                "source_first_boundary_count": first_boundary_count,
                "source_last_boundary_count": last_boundary_count,
            }
        )

    result = {
        "occurrence_surface_artifact_sha256": _digest(surface_bytes),
        "coordinate_frame_artifact_sha256": _digest(frame_bytes),
        "operation": (
            "immediate prior and later exact coordinate surfaces for every "
            "occurrence carrying every frozen source-recurring closed frame"
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
    print(f"frames walked: {len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
