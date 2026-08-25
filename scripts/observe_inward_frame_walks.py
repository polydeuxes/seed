"""Measure bounded source-order walks beginning at one frozen inward frame.

The caller addresses a frame only after the blind coordinate-frame artifact is
frozen.  Each occurrence of that frame begins one walk.  The walk ends before
the next occurrence of the same frame or at exact source end.

This observer reads coordinate-surface hashes and coordinate hashes only.  It
does not read occurrence labels, plaintext coordinate material, the Book,
machine grammar, runtime constants, or an expected walk length.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path


SURFACES = Path("/tmp/seed_inward_occurrence_surfaces_blind.json")
FRAMES = Path("/tmp/seed_inward_coordinate_frames_blind.json")
OUTPUT = Path("/tmp/seed_inward_frame_walks_blind.json")


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _source_sequences(surfaces: dict) -> list[list[str]]:
    sequences = [
        [None] * occurrence_count
        for occurrence_count in surfaces["source_occurrence_counts"]
    ]
    for surface in surfaces["surfaces"]:
        identity = surface["coordinate_surface_sha256"]
        for source_number, append_position in surface["occurrences"]:
            if sequences[source_number][append_position] is not None:
                raise ValueError("one append address carries two surfaces")
            sequences[source_number][append_position] = identity
    if any(any(identity is None for identity in sequence) for sequence in sequences):
        raise ValueError("one append address carries no surface")
    return sequences


def _frame_walks(
    sequences: list[list[str]], carrying_surfaces: frozenset[str]
) -> list[dict[str, object]]:
    walks = []
    for source_number, sequence in enumerate(sequences):
        starts = [
            append_position
            for append_position, surface in enumerate(sequence)
            if surface in carrying_surfaces
        ]
        for start_number, start in enumerate(starts):
            end = (
                starts[start_number + 1]
                if start_number + 1 < len(starts)
                else len(sequence)
            )
            walks.append(
                {
                    "source_number": source_number,
                    "start_append_position": start,
                    "end_append_position": end,
                    "coordinate_surface_sha256s": sequence[start:end],
                }
            )
    return walks


def _aligned_coordinate_intersections(
    walks: list[dict[str, object]], surface_coordinates: dict[str, frozenset[str]]
) -> list[dict[str, object]]:
    lengths = frozenset(
        len(walk["coordinate_surface_sha256s"]) for walk in walks
    )
    if len(lengths) != 1:
        raise ValueError("aligned walks do not have one exact length")
    length = next(iter(lengths))
    findings = []
    for walk_position in range(length):
        surfaces = sorted(
            frozenset(
                walk["coordinate_surface_sha256s"][walk_position]
                for walk in walks
            )
        )
        coordinates = surface_coordinates[surfaces[0]]
        for surface in surfaces[1:]:
            coordinates = coordinates.intersection(surface_coordinates[surface])
        findings.append(
            {
                "walk_position": walk_position,
                "coordinate_surface_sha256s": surfaces,
                "coordinate_material_sha256s": sorted(coordinates),
                "coordinate_count": len(coordinates),
            }
        )
    return findings


def _shared_ends(
    sequences: list[list[str]],
) -> tuple[list[str], list[str], list[list[str]]]:
    shortest = min(len(sequence) for sequence in sequences)
    first_count = 0
    while first_count < shortest and len(
        frozenset(sequence[first_count] for sequence in sequences)
    ) == 1:
        first_count += 1
    last_count = 0
    remaining = shortest - first_count
    while last_count < remaining and len(
        frozenset(sequence[-1 - last_count] for sequence in sequences)
    ) == 1:
        last_count += 1
    first = sequences[0][:first_count]
    last = sequences[0][len(sequences[0]) - last_count :] if last_count else []
    middles = [
        sequence[first_count : len(sequence) - last_count if last_count else None]
        for sequence in sequences
    ]
    return first, last, middles


def _maximum_common_adjacent(
    sequences: list[list[str]],
) -> tuple[int, list[list[str]]]:
    latest = []
    maximum_length = 0
    for width in range(1, min(len(sequence) for sequence in sequences) + 1):
        common = None
        for sequence in sequences:
            adjacent = frozenset(
                tuple(sequence[start : start + width])
                for start in range(len(sequence) - width + 1)
            )
            common = adjacent if common is None else common.intersection(adjacent)
        if not common:
            break
        maximum_length = width
        latest = [list(sequence) for sequence in sorted(common)]
    return maximum_length, latest


def _repeated_walks(
    shared_first: list[str], middle_by_source: list[list[str]]
) -> tuple[list[str], list[str], list[int]]:
    nonempty = [middle for middle in middle_by_source if middle]
    if not nonempty:
        return shared_first, [], [0] * len(middle_by_source)
    repeated = []
    for width in range(1, min(len(middle) for middle in nonempty) + 1):
        possible = nonempty[0][:width]
        if all(
            len(middle) % width == 0
            and middle == possible * (len(middle) // width)
            for middle in nonempty
        ):
            repeated = possible
            break
    if not repeated:
        return shared_first, [], [0] * len(middle_by_source)
    first = list(shared_first)
    first_repetition_count = 0
    while len(first) >= len(repeated) and first[-len(repeated) :] == repeated:
        del first[-len(repeated) :]
        first_repetition_count += 1
    counts = [
        first_repetition_count + len(middle) // len(repeated)
        for middle in middle_by_source
    ]
    return first, repeated, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surfaces", type=Path, default=SURFACES)
    parser.add_argument("--frames", type=Path, default=FRAMES)
    parser.add_argument("--frame-number", type=int, required=True)
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
    if arguments.frame_number < 0 or arguments.frame_number >= len(frames["frames"]):
        raise ValueError("frame number lies outside the frozen frame artifact")

    frame = frames["frames"][arguments.frame_number]
    carrying_surfaces = frozenset(frame["coordinate_surface_sha256s"])
    sequences = _source_sequences(surfaces)
    walks = _frame_walks(sequences, carrying_surfaces)
    surface_coordinates = {
        surface["coordinate_surface_sha256"]: frozenset(
            surface["coordinate_material_sha256s"]
        )
        for surface in surfaces["surfaces"]
    }

    exact_walks = defaultdict(list)
    walks_by_length = defaultdict(list)
    for walk in walks:
        surface_sequence = tuple(walk["coordinate_surface_sha256s"])
        walk["walk_identity_sha256"] = _digest(_encoded(surface_sequence))
        address = [
            walk["source_number"],
            walk["start_append_position"],
            walk["end_append_position"],
        ]
        exact_walks[surface_sequence].append(address)
        walks_by_length[len(surface_sequence)].append(walk)

    exact_walk_findings = []
    for sequence, addresses in exact_walks.items():
        exact_walk_findings.append(
            {
                "coordinate_surface_sha256s": list(sequence),
                "walk_identity_sha256": _digest(_encoded(sequence)),
                "walk_length": len(sequence),
                "addresses": sorted(addresses),
                "occurrence_count": len(addresses),
                "source_count": len(
                    frozenset(address[0] for address in addresses)
                ),
            }
        )
    exact_walk_findings.sort(
        key=lambda finding: (
            finding["walk_length"],
            finding["coordinate_surface_sha256s"],
        )
    )

    length_findings = []
    for length, addressed_walks in sorted(walks_by_length.items()):
        length_findings.append(
            {
                "walk_length": length,
                "walk_occurrence_count": len(addressed_walks),
                "exact_walk_count": len(
                    frozenset(
                        tuple(walk["coordinate_surface_sha256s"])
                        for walk in addressed_walks
                    )
                ),
                "source_count": len(
                    frozenset(
                        walk["source_number"] for walk in addressed_walks
                    )
                ),
                "aligned_coordinate_intersections": (
                    _aligned_coordinate_intersections(
                        addressed_walks, surface_coordinates
                    )
                ),
            }
        )

    adjacent = defaultdict(list)
    for walk in walks:
        sequence = walk["coordinate_surface_sha256s"]
        for width in range(1, len(sequence) + 1):
            for start in range(len(sequence) - width + 1):
                adjacent[tuple(sequence[start : start + width])].append(
                    [
                        walk["source_number"],
                        walk["start_append_position"],
                        walk["start_append_position"] + start,
                    ]
                )
    source_recurring_adjacent = []
    for sequence, occurrences in adjacent.items():
        addressed_sources = frozenset(
            occurrence[0] for occurrence in occurrences
        )
        if len(occurrences) < 2 or len(addressed_sources) != len(sequences):
            continue
        source_recurring_adjacent.append(
            {
                "coordinate_surface_sha256s": list(sequence),
                "adjacent_length": len(sequence),
                "occurrences": sorted(occurrences),
                "occurrence_count": len(occurrences),
                "source_count": len(addressed_sources),
            }
        )
    source_recurring_adjacent.sort(
        key=lambda finding: (
            finding["adjacent_length"],
            finding["coordinate_surface_sha256s"],
        )
    )

    source_walk_sequences = []
    walk_identity_sequences = []
    for source_number in range(len(sequences)):
        addressed_walks = [
            walk for walk in walks if walk["source_number"] == source_number
        ]
        identities = [
            walk["walk_identity_sha256"] for walk in addressed_walks
        ]
        walk_identity_sequences.append(identities)
        source_walk_sequences.append(
            {
                "source_number": source_number,
                "walk_identity_sha256s": identities,
                "walk_addresses": [
                    [
                        walk["start_append_position"],
                        walk["end_append_position"],
                    ]
                    for walk in addressed_walks
                ],
            }
        )
    shared_first, shared_last, varying_middles = _shared_ends(
        walk_identity_sequences
    )
    first_before_repetition, repeated_walks, repetition_counts = _repeated_walks(
        shared_first, varying_middles
    )
    maximum_common_length, maximum_common = _maximum_common_adjacent(
        walk_identity_sequences
    )

    result = {
        "occurrence_surface_artifact_sha256": _digest(surface_bytes),
        "coordinate_frame_artifact_sha256": _digest(frame_bytes),
        "frame_number": arguments.frame_number,
        "frame_coordinate_material_sha256s": frame[
            "coordinate_material_sha256s"
        ],
        "operation": (
            "every exact source-order walk beginning with one frozen frame and "
            "ending immediately before its next occurrence or at exact source "
            "end; exact walks, source-established lengths, aligned coordinate "
            "intersections, and every source-recurring adjacent sequence"
        ),
        "walk_count": len(walks),
        "exact_walk_count": len(exact_walk_findings),
        "exact_walks": exact_walk_findings,
        "walk_lengths": length_findings,
        "source_recurring_adjacent_sequences": source_recurring_adjacent,
        "source_walk_sequences": source_walk_sequences,
        "shared_first_walk_identity_sha256s": shared_first,
        "shared_first_before_repetition_walk_identity_sha256s": (
            first_before_repetition
        ),
        "repeated_walk_identity_sha256s": repeated_walks,
        "repetition_count_by_source": repetition_counts,
        "shared_last_walk_identity_sha256s": shared_last,
        "middle_walk_identity_sha256s_by_source": varying_middles,
        "maximum_common_adjacent_walk_length": maximum_common_length,
        "maximum_common_adjacent_walk_identity_sha256s": maximum_common,
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"walks: {len(walks)}")
    print(f"exact walks: {len(exact_walk_findings)}")
    print(f"walk lengths: {[(x['walk_length'], x['walk_occurrence_count']) for x in length_findings]}")
    print(f"source-recurring adjacent sequences: {len(source_recurring_adjacent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
