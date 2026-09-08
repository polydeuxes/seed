"""Measure exact scalar sameness across frozen inward walk boundaries.

The walk artifact is already frozen.  For each adjacent pair of opaque walk
identities, this observer compares the final occurrence of the first walk with
the first occurrence of the later walk.  It reads no event label, plaintext
coordinate material, Book, machine grammar, runtime constant, or expected walk
pair.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from observe_inward_frame_coordinate_continuities import (  # noqa: E402
    _scalar_coordinates,
    _same_scalar_groups,
)


SOURCE = Path("/tmp/seed_inward_occurrence_material.json")
SURFACES = Path("/tmp/seed_inward_occurrence_surfaces_blind.json")
WALKS = Path("/tmp/seed_inward_frame_walks_blind.json")
OUTPUT = Path("/tmp/seed_inward_walk_continuities_blind.json")
COORDINATE_MATERIAL_OUTPUT = Path(
    "/tmp/seed_inward_walk_continuity_coordinate_materials.json"
)


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _walk_transitions(source_walk_sequences: list[dict]) -> list[dict[str, object]]:
    transitions = []
    for source in source_walk_sequences:
        identities = source["walk_identity_sha256s"]
        addresses = source["walk_addresses"]
        if len(identities) != len(addresses):
            raise ValueError("one source does not address every exact walk")
        for walk_number in range(len(identities) - 1):
            first_start, first_end = addresses[walk_number]
            later_start, later_end = addresses[walk_number + 1]
            if first_end != later_start:
                raise ValueError("two adjacent walks do not share one exact boundary")
            transitions.append(
                {
                    "source_number": source["source_number"],
                    "first_walk_identity_sha256": identities[walk_number],
                    "later_walk_identity_sha256": identities[walk_number + 1],
                    "first_walk_start_append_position": first_start,
                    "first_walk_last_append_position": first_end - 1,
                    "later_walk_first_append_position": later_start,
                    "later_walk_end_append_position": later_end,
                }
            )
    return transitions


def _same_scalar_findings(
    accumulated: dict[tuple, list[list[object]]], transition_count: int
) -> list[dict[str, object]]:
    findings = []
    for equality, occurrences_and_values in accumulated.items():
        scalar_type, later_coordinates, first_coordinates = equality
        addressed = frozenset(
            (source_number, first_position, later_position)
            for source_number, first_position, later_position, _value in (
                occurrences_and_values
            )
        )
        findings.append(
            {
                "scalar_type": scalar_type,
                "later_walk_first_coordinates": [
                    {
                        "coordinate_address_sha256": address,
                        "top_coordinate_material_sha256": top_coordinate,
                    }
                    for address, top_coordinate in later_coordinates
                ],
                "first_walk_last_coordinates": [
                    {
                        "coordinate_address_sha256": address,
                        "top_coordinate_material_sha256": top_coordinate,
                    }
                    for address, top_coordinate in first_coordinates
                ],
                "occurrences": sorted(occurrences_and_values),
                "transition_count": len(addressed),
                "carried_by_every_exact_transition": (
                    len(addressed) == transition_count
                ),
            }
        )
    findings.sort(
        key=lambda finding: (
            finding["scalar_type"],
            repr(finding["later_walk_first_coordinates"]),
            repr(finding["first_walk_last_coordinates"]),
        )
    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--surfaces", type=Path, default=SURFACES)
    parser.add_argument("--walks", type=Path, default=WALKS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--coordinate-material-output",
        type=Path,
        default=COORDINATE_MATERIAL_OUTPUT,
    )
    arguments = parser.parse_args()

    source_bytes = arguments.source.read_bytes()
    surface_bytes = arguments.surfaces.read_bytes()
    walk_bytes = arguments.walks.read_bytes()
    source = json.loads(source_bytes)
    surfaces = json.loads(surface_bytes)
    walks = json.loads(walk_bytes)
    if any(
        artifact.get("known_loss") is not None
        for artifact in (source, surfaces, walks)
    ):
        raise ValueError("one inward artifact carries known loss")
    if surfaces.get("source_artifact_sha256") != _digest(source_bytes):
        raise ValueError("occurrence surfaces do not address the supplied source")
    if walks.get("occurrence_surface_artifact_sha256") != _digest(surface_bytes):
        raise ValueError("walks do not address the supplied surfaces")

    source_materials = []
    for source_number, recorded_source in enumerate(source["sources"]):
        if recorded_source["source_number"] != source_number:
            raise ValueError("one recorded source has a changed source number")
        materials = []
        for occurrence in recorded_source["occurrences"]:
            if occurrence["append_position"] != len(materials):
                raise ValueError("source occurrence addresses are not exact")
            materials.append(occurrence["material"])
        source_materials.append(materials)

    transitions = _walk_transitions(walks["source_walk_sequences"])
    coordinate_materials = {}
    address_materials = {}
    coordinate_sha256s = {}
    scalar_sha256s = {}
    scalar_coordinates = {}

    def scalars_at(source_number: int, append_position: int):
        address = (source_number, append_position)
        if address not in scalar_coordinates:
            scalar_coordinates[address] = _scalar_coordinates(
                source_materials[source_number][append_position],
                coordinate_materials,
                address_materials,
                None,
                coordinate_sha256s,
                scalar_sha256s,
            )
        return scalar_coordinates[address]

    by_pair = defaultdict(list)
    for transition in transitions:
        pair = (
            transition["first_walk_identity_sha256"],
            transition["later_walk_identity_sha256"],
        )
        by_pair[pair].append(transition)

    pair_findings = []
    for pair, addressed_transitions in sorted(by_pair.items()):
        accumulated = defaultdict(list)
        for transition in addressed_transitions:
            source_number = transition["source_number"]
            first_position = transition["first_walk_last_append_position"]
            later_position = transition["later_walk_first_append_position"]
            later_scalars = scalars_at(source_number, later_position)
            first_scalars = scalars_at(source_number, first_position)
            for (
                scalar_type,
                value_sha256,
                later_coordinates,
                first_coordinates,
            ) in _same_scalar_groups(later_scalars, first_scalars):
                accumulated[
                    (scalar_type, later_coordinates, first_coordinates)
                ].append(
                    [source_number, first_position, later_position, value_sha256]
                )
        pair_findings.append(
            {
                "first_walk_identity_sha256": pair[0],
                "later_walk_identity_sha256": pair[1],
                "transitions": addressed_transitions,
                "transition_count": len(addressed_transitions),
                "source_count": len(
                    frozenset(
                        transition["source_number"]
                        for transition in addressed_transitions
                    )
                ),
                "same_scalar_findings": _same_scalar_findings(
                    accumulated, len(addressed_transitions)
                ),
            }
        )

    result = {
        "source_artifact_sha256": _digest(source_bytes),
        "occurrence_surface_artifact_sha256": _digest(surface_bytes),
        "walk_artifact_sha256": _digest(walk_bytes),
        "operation": (
            "exact nested scalar sameness from the final occurrence of every "
            "opaque walk to the first occurrence of its exact later walk, "
            "grouped by the two frozen walk identities"
        ),
        "transition_count": len(transitions),
        "walk_identity_pair_count": len(pair_findings),
        "walk_identity_pairs": pair_findings,
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    coordinate_material_finding = {
        "source_artifact_sha256": _digest(source_bytes),
        "occurrence_surface_artifact_sha256": _digest(surface_bytes),
        "walk_artifact_sha256": _digest(walk_bytes),
        "walk_continuity_artifact_sha256": _digest(encoded),
        "coordinate_materials": coordinate_materials,
        "coordinate_address_materials": address_materials,
        "known_loss": None,
    }
    coordinate_material_encoded = _encoded(coordinate_material_finding)
    arguments.coordinate_material_output.write_bytes(coordinate_material_encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"coordinate material: {arguments.coordinate_material_output}")
    print(
        "coordinate material sha256: "
        f"{_digest(coordinate_material_encoded)}"
    )
    print(f"transitions: {len(transitions)}")
    print(f"walk identity pairs: {len(pair_findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
