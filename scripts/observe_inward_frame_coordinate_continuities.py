"""Measure nested scalar sameness through one frozen inward frame.

The source, occurrence surfaces, and closed frames must already be frozen.  A
caller addresses one frame by its frozen number.  The operation reads no event
label, Book material, machine grammar, runtime constant, or expected
coordinate name.

Every mapping key is replaced by its digest before a nested coordinate address
enters the blind artifact.  Plaintext coordinate material is written to a
separate file that is not read by this operation or by any preceding blind
operation.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import struct
import time
from typing import Any


SOURCE = Path("/tmp/seed_inward_occurrence_material.json")
SURFACES = Path("/tmp/seed_inward_occurrence_surfaces_blind.json")
FRAMES = Path("/tmp/seed_inward_coordinate_frames_blind.json")
OUTPUT = Path("/tmp/seed_inward_frame_coordinate_continuities_blind.json")
COORDINATE_MATERIAL_OUTPUT = Path(
    "/tmp/seed_inward_frame_coordinate_address_materials.json"
)
COMPLETE_OUTPUT = Path(
    "/tmp/seed_inward_frame_coordinate_continuities_complete.json"
)
MEASUREMENT_IDENTITY = "inward_frame_nested_scalar_sameness_002"


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _coordinate_digest(material: str) -> str:
    return _digest(material.encode())


def _scalar_digest(scalar_type: str, value: Any) -> str:
    if scalar_type == "none":
        exact = b"n"
    elif scalar_type == "boolean":
        exact = b"b1" if value else b"b0"
    elif scalar_type == "integer":
        exact = b"i" + str(value).encode()
    elif scalar_type == "number":
        exact = b"f" + struct.pack(">d", value)
    elif scalar_type == "text":
        material = value.encode()
        exact = b"t" + len(material).to_bytes(8, "big") + material
    else:
        raise ValueError(f"unaddressed scalar type: {scalar_type}")
    return _digest(exact)


def _address_digest(blind_address: list[list[object]]) -> str:
    parts = []
    for address_type, material in blind_address:
        if address_type == "coordinate":
            parts.extend((b"c", bytes.fromhex(material)))
        elif address_type == "list_position":
            parts.extend((b"l", material.to_bytes(8, "big")))
        else:
            raise ValueError(f"unaddressed coordinate address type: {address_type}")
    return _digest(b"".join(parts))


def _scalar_type(value: Any) -> str | None:
    if value is None:
        return "none"
    if type(value) is bool:
        return "boolean"
    if type(value) is int:
        return "integer"
    if type(value) is float:
        return "number"
    if type(value) is str:
        return "text"
    return None


def _scalar_coordinates(
    material: dict,
    coordinate_materials: dict[str, str],
    address_materials: dict[str, list[list[object]]],
    sought_scalars: frozenset[tuple[str, str]] | None = None,
    coordinate_sha256s: dict[str, str] | None = None,
    scalar_sha256s: dict[tuple[str, object], str] | None = None,
) -> dict[tuple[str, str], list[tuple[str, str]]]:
    """Return scalar identity -> (nested address, top coordinate) entries."""

    if type(material) is not dict:
        raise ValueError("one occurrence must carry top-level coordinates")
    if coordinate_sha256s is None:
        coordinate_sha256s = {}
    if scalar_sha256s is None:
        scalar_sha256s = {}
    by_value: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)

    def walk(value: Any, blind_address: list[list[object]], clear_address):
        if type(value) is dict:
            for coordinate, child in value.items():
                if type(coordinate) is not str:
                    raise ValueError("one occurrence carries a non-text coordinate")
                coordinate_sha256 = coordinate_sha256s.get(coordinate)
                if coordinate_sha256 is None:
                    coordinate_sha256 = _coordinate_digest(coordinate)
                    coordinate_sha256s[coordinate] = coordinate_sha256
                prior = coordinate_materials.setdefault(
                    coordinate_sha256, coordinate
                )
                if prior != coordinate:
                    raise ValueError("two coordinate materials have one digest")
                walk(
                    child,
                    blind_address + [["coordinate", coordinate_sha256]],
                    clear_address + [["coordinate", coordinate]],
                )
            return
        if type(value) is list:
            for position, child in enumerate(value):
                walk(
                    child,
                    blind_address + [["list_position", position]],
                    clear_address + [["list_position", position]],
                )
            return
        scalar_type = _scalar_type(value)
        if scalar_type is None:
            raise ValueError(f"unaddressed scalar type: {type(value).__name__}")
        scalar = (scalar_type, value)
        value_sha256 = scalar_sha256s.get(scalar)
        if value_sha256 is None:
            value_sha256 = _scalar_digest(scalar_type, value)
            scalar_sha256s[scalar] = value_sha256
        if sought_scalars is not None and (
            scalar_type,
            value_sha256,
        ) not in sought_scalars:
            return
        if not blind_address or blind_address[0][0] != "coordinate":
            raise ValueError("one scalar has no top-level coordinate")
        address_sha256 = _address_digest(blind_address)
        prior_address = address_materials.setdefault(address_sha256, clear_address)
        if prior_address != clear_address:
            raise ValueError("two nested coordinate addresses have one digest")
        top_coordinate_sha256 = blind_address[0][1]
        by_value[(scalar_type, value_sha256)].append(
            (address_sha256, top_coordinate_sha256)
        )

    walk(material, [], [])
    return by_value


def _surface_addresses(surfaces: dict) -> dict[tuple[int, int], str]:
    addressed = {}
    for surface in surfaces["surfaces"]:
        identity = surface["coordinate_surface_sha256"]
        for address in surface["occurrences"]:
            key = tuple(address)
            if key in addressed:
                raise ValueError("one append address carries two surfaces")
            addressed[key] = identity
    return addressed


def _complete_existing(
    *,
    output: Path,
    coordinate_material_output: Path,
    complete_output: Path,
    surface_sha256: str,
    frame_sha256: str,
    frame_number: int,
) -> tuple[bytes, bytes] | None:
    if (
        not output.exists()
        or not coordinate_material_output.exists()
        or not complete_output.exists()
    ):
        return None
    encoded = output.read_bytes()
    coordinate_material_encoded = coordinate_material_output.read_bytes()
    try:
        complete = json.loads(complete_output.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    required = {
        "measurement_identity": MEASUREMENT_IDENTITY,
        "occurrence_surface_artifact_sha256": surface_sha256,
        "coordinate_frame_artifact_sha256": frame_sha256,
        "frame_number": frame_number,
        "known_loss": None,
    }
    if any(complete.get(key) != value for key, value in required.items()):
        return None
    if complete.get("frame_continuity_artifact_sha256") != _digest(encoded):
        return None
    if complete.get("coordinate_material_artifact_sha256") != _digest(
        coordinate_material_encoded
    ):
        return None
    return encoded, coordinate_material_encoded


def _same_scalar_groups(
    first: dict[tuple[str, str], list[tuple[str, str]]],
    second: dict[tuple[str, str], list[tuple[str, str]]],
) -> list[tuple[str, str, tuple[tuple[str, str], ...], tuple[tuple[str, str], ...]]]:
    found = []
    for scalar_type, value_sha256 in first.keys() & second.keys():
        scalar = (scalar_type, value_sha256)
        found.append(
            (
                scalar_type,
                value_sha256,
                tuple(sorted(first[scalar])),
                tuple(sorted(second[scalar])),
            )
        )
    return found


def _equality_findings(
    accumulated: dict[tuple, list[list[object]]],
    occurrence_count: int,
) -> list[dict[str, object]]:
    findings = []
    for equality, occurrences_and_values in accumulated.items():
        (
            direction,
            scalar_type,
            current_coordinates,
            neighbor_coordinates,
        ) = equality
        addressed_occurrences = {
            (source_number, append_position)
            for source_number, append_position, _value_sha256 in occurrences_and_values
        }
        findings.append(
            {
                "direction": direction,
                "scalar_type": scalar_type,
                "current_coordinates": [
                    {
                        "coordinate_address_sha256": address,
                        "top_coordinate_material_sha256": top_coordinate,
                        "coordinate_is_in_frame": coordinate_is_in_frame,
                    }
                    for address, top_coordinate, coordinate_is_in_frame
                    in current_coordinates
                ],
                "neighbor_coordinates": [
                    {
                        "coordinate_address_sha256": address,
                        "top_coordinate_material_sha256": top_coordinate,
                    }
                    for address, top_coordinate in neighbor_coordinates
                ],
                "occurrences": sorted(occurrences_and_values),
                "occurrence_count": len(addressed_occurrences),
                "carried_by_every_measured_occurrence": (
                    len(addressed_occurrences) == occurrence_count
                ),
            }
        )
    findings.sort(
        key=lambda finding: (
            finding["direction"],
            finding["scalar_type"],
            repr(finding["current_coordinates"]),
            repr(finding["neighbor_coordinates"]),
        )
    )
    return findings


def main() -> int:
    process_started = time.monotonic()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--surfaces", type=Path, default=SURFACES)
    parser.add_argument("--frames", type=Path, default=FRAMES)
    parser.add_argument("--frame-number", type=int, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--coordinate-material-output",
        type=Path,
        default=COORDINATE_MATERIAL_OUTPUT,
    )
    parser.add_argument("--complete-output", type=Path, default=COMPLETE_OUTPUT)
    parser.add_argument("--reconstruct", action="store_true")
    arguments = parser.parse_args()

    surface_bytes = arguments.surfaces.read_bytes()
    frame_bytes = arguments.frames.read_bytes()
    surface_sha256 = _digest(surface_bytes)
    frame_sha256 = _digest(frame_bytes)
    if not arguments.reconstruct:
        existing = _complete_existing(
            output=arguments.output,
            coordinate_material_output=arguments.coordinate_material_output,
            complete_output=arguments.complete_output,
            surface_sha256=surface_sha256,
            frame_sha256=frame_sha256,
            frame_number=arguments.frame_number,
        )
        if existing is not None:
            encoded, coordinate_material_encoded = existing
            print(f"reused complete artifact: {arguments.output}")
            print(f"artifact bytes: {len(encoded)}")
            print(f"artifact sha256: {_digest(encoded)}")
            print(f"coordinate material: {arguments.coordinate_material_output}")
            print(
                "coordinate material sha256: "
                f"{_digest(coordinate_material_encoded)}"
            )
            print(f"elapsed seconds: {time.monotonic() - process_started:.6f}")
            return 0

    source_bytes = arguments.source.read_bytes()
    source_sha256 = _digest(source_bytes)
    source = json.loads(source_bytes)
    surfaces = json.loads(surface_bytes)
    frames = json.loads(frame_bytes)
    if any(
        artifact.get("known_loss") is not None
        for artifact in (source, surfaces, frames)
    ):
        raise ValueError("one inward artifact carries known loss")
    if surfaces.get("source_artifact_sha256") != source_sha256:
        raise ValueError("occurrence surfaces do not address the supplied source")
    if frames.get("occurrence_surface_artifact_sha256") != surface_sha256:
        raise ValueError("coordinate frames do not address the supplied surfaces")
    if arguments.frame_number < 0 or arguments.frame_number >= len(frames["frames"]):
        raise ValueError("frame number lies outside the frozen frame artifact")

    frame = frames["frames"][arguments.frame_number]
    frame_coordinates = frozenset(frame["coordinate_material_sha256s"])
    carrying_surfaces = frozenset(frame["coordinate_surface_sha256s"])
    surface_at = _surface_addresses(surfaces)

    coordinate_materials = {}
    address_materials = {}
    coordinate_sha256s = {}
    scalar_sha256s = {}
    source_materials = []
    for recorded_source in source["sources"]:
        materials = []
        for occurrence in recorded_source["occurrences"]:
            if occurrence["append_position"] != len(materials):
                raise ValueError("source occurrence addresses are not exact")
            materials.append(occurrence["material"])
        source_materials.append(materials)

    scalar_coordinates = {}

    def scalars_at(
        source_number: int,
        append_position: int,
        sought_scalars: frozenset[tuple[str, str]] | None = None,
    ):
        address = (source_number, append_position, sought_scalars)
        if address not in scalar_coordinates:
            scalar_coordinates[address] = _scalar_coordinates(
                source_materials[source_number][append_position],
                coordinate_materials,
                address_materials,
                sought_scalars,
                coordinate_sha256s,
                scalar_sha256s,
            )
        return scalar_coordinates[address]

    by_surface = {}
    observation_started = time.monotonic()
    for carrying_surface in sorted(carrying_surfaces):
        addressed_occurrences = []
        source_first_occurrences = []
        prior_equalities = defaultdict(list)
        later_equalities = defaultdict(list)
        prior_occurrence_count = 0
        for source_number, materials in enumerate(source_materials):
            for append_position in range(len(materials)):
                if surface_at[(source_number, append_position)] != carrying_surface:
                    continue
                address = [source_number, append_position]
                addressed_occurrences.append(address)
                current = scalars_at(source_number, append_position)
                sought_scalars = frozenset(current)
                if append_position == 0:
                    source_first_occurrences.append(address)
                else:
                    prior_occurrence_count += 1
                    prior = scalars_at(
                        source_number,
                        append_position - 1,
                        sought_scalars,
                    )
                    for equality in _same_scalar_groups(current, prior):
                        (
                            scalar_type,
                            value_sha256,
                            current_coordinates,
                            neighbor_coordinates,
                        ) = equality
                        key = (
                            "prior_to_current",
                            scalar_type,
                            tuple(
                                (
                                    address,
                                    top_coordinate,
                                    top_coordinate in frame_coordinates,
                                )
                                for address, top_coordinate in current_coordinates
                            ),
                            neighbor_coordinates,
                        )
                        prior_equalities[key].append(
                            [source_number, append_position, value_sha256]
                        )
                if append_position + 1 >= len(materials):
                    raise ValueError("one addressed frame occurrence has no later material")
                later = scalars_at(
                    source_number,
                    append_position + 1,
                    sought_scalars,
                )
                for equality in _same_scalar_groups(current, later):
                    (
                        scalar_type,
                        value_sha256,
                        current_coordinates,
                        neighbor_coordinates,
                    ) = equality
                    key = (
                        "current_to_later",
                        scalar_type,
                        tuple(
                            (
                                address,
                                top_coordinate,
                                top_coordinate in frame_coordinates,
                            )
                            for address, top_coordinate in current_coordinates
                        ),
                        neighbor_coordinates,
                    )
                    later_equalities[key].append(
                        [source_number, append_position, value_sha256]
                    )

        by_surface[carrying_surface] = {
            "coordinate_surface_sha256": carrying_surface,
            "addressed_occurrences": addressed_occurrences,
            "occurrence_count": len(addressed_occurrences),
            "source_first_occurrences": source_first_occurrences,
            "source_first_occurrence_count": len(source_first_occurrences),
            "prior_occurrence_count": prior_occurrence_count,
            "prior_to_current_equalities": _equality_findings(
                prior_equalities, prior_occurrence_count
            ),
            "current_to_later_equalities": _equality_findings(
                later_equalities, len(addressed_occurrences)
            ),
        }
        print(
            f"measured surface {len(by_surface)}/{len(carrying_surfaces)} "
            f"after {time.monotonic() - observation_started:.3f}s",
            flush=True,
        )

    result = {
        "measurement_identity": MEASUREMENT_IDENTITY,
        "source_artifact_sha256": source_sha256,
        "occurrence_surface_artifact_sha256": surface_sha256,
        "coordinate_frame_artifact_sha256": frame_sha256,
        "frame_number": arguments.frame_number,
        "frame_coordinate_material_sha256s": sorted(frame_coordinates),
        "operation": (
            "nested exact scalar sameness from one frozen frame occurrence to "
            "its immediate prior and later material, with source beginnings "
            "kept separate and frame coordinates distinguished from additional "
            "coordinates of each carrying surface"
        ),
        "carrying_surfaces": [by_surface[key] for key in sorted(by_surface)],
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)

    coordinate_material_finding = {
        "source_artifact_sha256": source_sha256,
        "occurrence_surface_artifact_sha256": surface_sha256,
        "coordinate_frame_artifact_sha256": frame_sha256,
        "frame_continuity_artifact_sha256": _digest(encoded),
        "coordinate_materials": coordinate_materials,
        "coordinate_address_materials": address_materials,
        "known_loss": None,
    }
    coordinate_material_encoded = _encoded(coordinate_material_finding)
    arguments.coordinate_material_output.write_bytes(coordinate_material_encoded)
    complete_finding = {
        "measurement_identity": MEASUREMENT_IDENTITY,
        "source_artifact_sha256": source_sha256,
        "occurrence_surface_artifact_sha256": surface_sha256,
        "coordinate_frame_artifact_sha256": frame_sha256,
        "frame_number": arguments.frame_number,
        "frame_continuity_artifact_sha256": _digest(encoded),
        "coordinate_material_artifact_sha256": _digest(
            coordinate_material_encoded
        ),
        "known_loss": None,
    }
    arguments.complete_output.write_bytes(_encoded(complete_finding))

    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"coordinate material: {arguments.coordinate_material_output}")
    print(
        "coordinate material sha256: "
        f"{_digest(coordinate_material_encoded)}"
    )
    print(f"frame occurrences: {sum(x['occurrence_count'] for x in by_surface.values())}")
    print(f"carrying surfaces: {len(by_surface)}")
    print(f"elapsed seconds: {time.monotonic() - process_started:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
