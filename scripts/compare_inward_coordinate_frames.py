"""Compare every frozen inward coordinate frame and its blind neighbors.

The operation is exhaustive over the frozen frames. It reads no occurrence
label, Book coordinate, machine grammar, runtime constant, or requested frame.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path


FRAMES = Path("/tmp/seed_inward_coordinate_frames_blind.json")
NEIGHBORS = Path("/tmp/seed_inward_frame_neighbors_blind.json")
OUTPUT = Path("/tmp/seed_inward_coordinate_frame_comparisons_blind.json")


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _neighbor_signature(finding: dict) -> str:
    return _digest(
        _encoded(
            {
                "prior": finding["prior_coordinate_surfaces"],
                "later": finding["later_coordinate_surfaces"],
                "pairs": finding["prior_later_coordinate_surface_pairs"],
                "first_boundary": finding["source_first_boundary_count"],
                "last_boundary": finding["source_last_boundary_count"],
            }
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=Path, default=FRAMES)
    parser.add_argument("--neighbors", type=Path, default=NEIGHBORS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    frame_bytes = arguments.frames.read_bytes()
    neighbor_bytes = arguments.neighbors.read_bytes()
    frames_artifact = json.loads(frame_bytes)
    neighbors_artifact = json.loads(neighbor_bytes)
    if (
        frames_artifact.get("known_loss") is not None
        or neighbors_artifact.get("known_loss") is not None
    ):
        raise ValueError("one blind inward artifact carries known loss")
    if neighbors_artifact.get("coordinate_frame_artifact_sha256") != _digest(
        frame_bytes
    ):
        raise ValueError("neighbor findings do not address the supplied frames")

    frames = [
        frozenset(frame["coordinate_material_sha256s"])
        for frame in frames_artifact["frames"]
    ]
    if len(frames) != len(set(frames)):
        raise ValueError("two frozen frames carry the same coordinates")
    neighbor_signatures = [
        _neighbor_signature(finding)
        for finding in neighbors_artifact["findings"]
    ]
    by_neighbor_signature = defaultdict(list)
    for frame_number, signature in enumerate(neighbor_signatures):
        by_neighbor_signature[signature].append(frame_number)

    relation_counts = Counter()
    comparisons = []
    for first_number, first in enumerate(frames):
        for second_number in range(first_number + 1, len(frames)):
            second = frames[second_number]
            shared = first & second
            if not shared:
                relation = "disjoint"
            elif first < second:
                relation = "first_within_second"
            elif second < first:
                relation = "second_within_first"
            else:
                relation = "partial_overlap"
            relation_counts[relation] += 1
            comparisons.append(
                [
                    first_number,
                    second_number,
                    relation,
                    len(shared),
                    len(first - second),
                    len(second - first),
                    neighbor_signatures[first_number]
                    == neighbor_signatures[second_number],
                ]
            )

    frame_findings = []
    for frame_number, frame in enumerate(frames):
        containing = [
            other_number
            for other_number, other in enumerate(frames)
            if frame_number != other_number and frame < other
        ]
        contained = [
            other_number
            for other_number, other in enumerate(frames)
            if frame_number != other_number and other < frame
        ]
        immediate_containing = [
            other_number
            for other_number in containing
            if not any(
                frame < frames[middle_number] < frames[other_number]
                for middle_number in containing
                if middle_number != other_number
            )
        ]
        immediate_contained = [
            other_number
            for other_number in contained
            if not any(
                frames[other_number] < frames[middle_number] < frame
                for middle_number in contained
                if middle_number != other_number
            )
        ]
        signature = neighbor_signatures[frame_number]
        frame_findings.append(
            {
                "frame_number": frame_number,
                "coordinate_material_sha256s": sorted(frame),
                "coordinate_identity_sha256": _digest(
                    _encoded(sorted(frame))
                ),
                "immediate_containing_frame_numbers": sorted(
                    immediate_containing
                ),
                "immediate_contained_frame_numbers": sorted(immediate_contained),
                "neighbor_signature_sha256": signature,
                "frames_with_same_neighbor_signature": sorted(
                    by_neighbor_signature[signature]
                ),
            }
        )

    result = {
        "coordinate_frame_artifact_sha256": _digest(frame_bytes),
        "frame_neighbor_artifact_sha256": _digest(neighbor_bytes),
        "operation": (
            "exhaustive exact coordinate containment and overlap comparison, "
            "plus exact prior/later signature equality, for every frozen frame"
        ),
        "comparison_schema": [
            "first_frame_number",
            "second_frame_number",
            "coordinate_relation",
            "shared_coordinate_count",
            "first_only_coordinate_count",
            "second_only_coordinate_count",
            "same_neighbor_signature",
        ],
        "pair_relation_counts": dict(sorted(relation_counts.items())),
        "pair_comparisons": comparisons,
        "frame_findings": frame_findings,
        "coordinate_unique_frame_count": len(set(frames)),
        "neighbor_signature_count": len(by_neighbor_signature),
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"frames: {len(frames)}")
    print(f"coordinate-unique frames: {result['coordinate_unique_frame_count']}")
    print(f"neighbor signatures: {result['neighbor_signature_count']}")
    print(f"pair relations: {result['pair_relation_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
