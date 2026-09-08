"""Ask whether frozen inward-walk continuities are required by live readers.

The preceding blind work found exact scalar material carried from the final
occurrence of one walk into the first occurrence of the later walk.  This
post-freeze observer changes only those later coordinates before they are
recorded, then lets the existing runtime decide whether work may continue.

It also tests the strongest repeated edge separately: a later assignment that
normally addresses the immediately prior result is given an intact result
reference from an earlier iteration.  No runtime or Book rule is added here.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
import time


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger  # noqa: E402
from seed_runtime.operator_console import run_persistent_operator_console  # noqa: E402

from record_inward_occurrence_material import SOURCE_MATERIALS  # noqa: E402


SOURCE = Path("/tmp/seed_inward_occurrence_material.json")
SURFACES = Path("/tmp/seed_inward_occurrence_surfaces_blind.json")
WALKS = Path("/tmp/seed_inward_frame_walks_blind.json")
CONTINUITIES = Path("/tmp/seed_inward_walk_continuities_blind.json")
COORDINATE_MATERIALS = Path(
    "/tmp/seed_inward_walk_continuity_coordinate_materials.json"
)
OUTPUT = Path("/tmp/seed_inward_walk_binding_refusals.json")

RESPONSIBLE_BOUNDARY = "responsible_boundary"
DETERMINATION_RESULT_REFERENCE = (
    "addressed_byte_occurrence_reference_determination_result_reference"
)


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _read_artifacts(
    source_path: Path,
    surface_path: Path,
    walk_path: Path,
    continuity_path: Path,
    coordinate_material_path: Path,
) -> tuple[dict, dict, dict, dict, dict, dict[str, bytes]]:
    material_by_path = {}
    decoded = []
    for path in (
        source_path,
        surface_path,
        walk_path,
        continuity_path,
        coordinate_material_path,
    ):
        material = path.read_bytes()
        material_by_path[str(path)] = material
        decoded.append(json.loads(material))
    source, surfaces, walks, continuities, coordinate_materials = decoded
    if any(
        artifact.get("known_loss") is not None
        for artifact in decoded
    ):
        raise ValueError("one supplied inward finding carries known loss")
    if surfaces.get("source_artifact_sha256") != _digest(
        material_by_path[str(source_path)]
    ):
        raise ValueError("occurrence surfaces do not address the supplied source")
    if walks.get("occurrence_surface_artifact_sha256") != _digest(
        material_by_path[str(surface_path)]
    ):
        raise ValueError("walks do not address the supplied surfaces")
    if continuities.get("source_artifact_sha256") != _digest(
        material_by_path[str(source_path)]
    ):
        raise ValueError("continuities do not address the supplied source")
    if continuities.get("occurrence_surface_artifact_sha256") != _digest(
        material_by_path[str(surface_path)]
    ):
        raise ValueError("continuities do not address the supplied surfaces")
    if continuities.get("walk_artifact_sha256") != _digest(
        material_by_path[str(walk_path)]
    ):
        raise ValueError("continuities do not address the supplied walks")
    if coordinate_materials.get("walk_continuity_artifact_sha256") != _digest(
        material_by_path[str(continuity_path)]
    ):
        raise ValueError("coordinate material does not address the continuities")
    if len(source["sources"]) != len(SOURCE_MATERIALS):
        raise ValueError("source material count changed")
    for source_number, (recorded, exact_material) in enumerate(
        zip(source["sources"], SOURCE_MATERIALS, strict=True)
    ):
        if recorded["source_number"] != source_number:
            raise ValueError("one source address changed")
        if recorded["input_sha256"] != _digest(exact_material):
            raise ValueError("one source material changed")
    return (
        source,
        surfaces,
        walks,
        continuities,
        coordinate_materials,
        material_by_path,
    )


def _complete_later_paths(
    pair: dict, coordinate_materials: dict
) -> list[tuple[tuple[str, object], ...]]:
    names = coordinate_materials["coordinate_materials"]
    addresses = coordinate_materials["coordinate_address_materials"]
    paths = {}
    for finding in pair["same_scalar_findings"]:
        if not finding["carried_by_every_exact_transition"]:
            continue
        for coordinate in finding["later_walk_first_coordinates"]:
            address_sha256 = coordinate["coordinate_address_sha256"]
            path = tuple(tuple(part) for part in addresses[address_sha256])
            if not path or path[0][0] != "coordinate":
                raise ValueError("one carried scalar has no exact top coordinate")
            expected_top = names[
                coordinate["top_coordinate_material_sha256"]
            ]
            if path[0][1] != expected_top:
                raise ValueError("one carried scalar has a changed top coordinate")
            if expected_top != RESPONSIBLE_BOUNDARY:
                paths[path] = None
    return sorted(paths, key=repr)


def _changed_scalar(value: object) -> object:
    if type(value) is str:
        return value + "-changed"
    if type(value) is int:
        return value + 1_000_000
    if type(value) is bool:
        return not value
    if type(value) is float:
        return value + 1_000_000.0
    if value is None:
        return "changed"
    raise ValueError("one addressed coordinate does not carry scalar material")


def _change_at_path(material: dict, path: tuple[tuple[str, object], ...]) -> None:
    current: object = material
    for part_type, part_value in path[:-1]:
        if part_type == "coordinate" and type(current) is dict:
            if part_value not in current:
                raise ValueError("one addressed coordinate is absent")
            current = current[part_value]
        elif part_type == "list_position" and type(current) is list:
            if type(part_value) is not int or not 0 <= part_value < len(current):
                raise ValueError("one addressed list position is absent")
            current = current[part_value]
        else:
            raise ValueError("one coordinate address does not match its material")
    part_type, part_value = path[-1]
    if part_type == "coordinate" and type(current) is dict:
        if part_value not in current:
            raise ValueError("one addressed coordinate is absent")
        current[part_value] = _changed_scalar(current[part_value])
    elif part_type == "list_position" and type(current) is list:
        if type(part_value) is not int or not 0 <= part_value < len(current):
            raise ValueError("one addressed list position is absent")
        current[part_value] = _changed_scalar(current[part_value])
    else:
        raise ValueError("one final coordinate address does not match its material")


def _result_reference(event) -> dict[str, str]:
    material = event.material
    required = {
        "act_occurrence_event_identity",
        "determination_act_occurrence_identity",
        "result_identity",
        "yield_relation_identity",
    }
    if not required.issubset(material):
        raise ValueError("an earlier occurrence is not an addressed result")
    return {
        "act_occurrence_event_identity": material[
            "act_occurrence_event_identity"
        ],
        "act_occurrence_identity": material[
            "determination_act_occurrence_identity"
        ],
        "recorded_occurrence_identity": event.identity,
        "result_identity": material["result_identity"],
        "yield_relation_identity": material["yield_relation_identity"],
    }


def _wrong_iteration_reference(ledger: EventLedger, material: dict) -> dict:
    current_reference = material.get(DETERMINATION_RESULT_REFERENCE)
    if type(current_reference) is not dict:
        raise ValueError("the later assignment lacks its addressed result reference")
    prior_occurrences = ledger.list()
    current_event = next(
        (
            event
            for event in prior_occurrences
            if event.identity == current_reference.get("recorded_occurrence_identity")
        ),
        None,
    )
    if current_event is None or _result_reference(current_event) != current_reference:
        raise ValueError("the later assignment does not address its exact prior result")
    same_surface = [
        event
        for event in prior_occurrences
        if event.identity != current_event.identity
        and event.material.keys() == current_event.material.keys()
    ]
    if not same_surface:
        raise ValueError("no earlier complete result is available for substitution")
    return _result_reference(same_surface[-1])


class _ChangedAssignmentLedger(EventLedger):
    def __init__(
        self,
        *,
        target_append_position: int,
        paths: list[tuple[tuple[str, object], ...]] = (),
        operation: str = "change",
        top_coordinate: str | None = None,
    ) -> None:
        super().__init__()
        self.target_append_position = target_append_position
        self.paths = paths
        self.operation = operation
        self.top_coordinate = top_coordinate
        self.changed = False

    def append(
        self,
        event_label: str,
        material: dict | None = None,
        *,
        exact_material: bytes | None = None,
        locality_identity: str | None = None,
    ):
        current_position = len(self.list())
        changed_material = deepcopy(material or {})
        if current_position == self.target_append_position:
            if self.changed:
                raise ValueError("one target append position was reached twice")
            if self.operation == "change":
                if not self.paths:
                    raise ValueError("changed assignment requires exact coordinates")
                for path in self.paths:
                    _change_at_path(changed_material, path)
            elif self.operation == "remove_top_coordinate":
                if (
                    type(self.top_coordinate) is not str
                    or self.top_coordinate not in changed_material
                ):
                    raise ValueError("the exact top coordinate is absent")
                del changed_material[self.top_coordinate]
            elif self.operation == "wrong_iteration":
                changed_material[DETERMINATION_RESULT_REFERENCE] = (
                    _wrong_iteration_reference(self, changed_material)
                )
            else:
                raise ValueError("unknown assignment change operation")
            self.changed = True
        return super().append(
            event_label,
            changed_material,
            exact_material=exact_material,
            locality_identity=locality_identity,
        )


def _exercise(
    *,
    source_number: int,
    target_append_position: int,
    paths: list[tuple[tuple[str, object], ...]] = (),
    operation: str = "change",
    top_coordinate: str | None = None,
) -> dict[str, object]:
    ledger = _ChangedAssignmentLedger(
        target_append_position=target_append_position,
        paths=paths,
        operation=operation,
        top_coordinate=top_coordinate,
    )
    refusal = None
    try:
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity=f"inward-source-{source_number}",
            input_stream=BytesIO(SOURCE_MATERIALS[source_number]),
        )
    except Exception as error:
        refusal = {"error_type": type(error).__name__, "message": str(error)}
    if not ledger.changed:
        raise ValueError("the exact later assignment was not reached")
    return {
        "source_number": source_number,
        "later_walk_first_append_position": target_append_position,
        "changed_coordinate_count": len(paths),
        "operation": operation,
        "refused": refusal is not None,
        "refusal": refusal,
        "recorded_occurrence_count": len(ledger.list()),
    }


def _exercise_payload(payload: dict[str, object]) -> dict[str, object]:
    return _exercise(**payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--surfaces", type=Path, default=SURFACES)
    parser.add_argument("--walks", type=Path, default=WALKS)
    parser.add_argument("--continuities", type=Path, default=CONTINUITIES)
    parser.add_argument(
        "--coordinate-materials", type=Path, default=COORDINATE_MATERIALS
    )
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--jobs", type=int, default=4)
    arguments = parser.parse_args()
    if arguments.jobs < 1:
        raise ValueError("jobs must be positive")

    begun = time.perf_counter()
    (
        _source,
        _surfaces,
        _walks,
        continuities,
        coordinate_materials,
        artifact_materials,
    ) = _read_artifacts(
        arguments.source,
        arguments.surfaces,
        arguments.walks,
        arguments.continuities,
        arguments.coordinate_materials,
    )

    control_payloads = []
    control_coordinates = []
    unbound_transitions = []
    direct_pair = None
    name_sha256s = {
        name: identity
        for identity, name in coordinate_materials["coordinate_materials"].items()
    }
    for pair in continuities["walk_identity_pairs"]:
        paths = _complete_later_paths(pair, coordinate_materials)
        if any(path[0][1] == DETERMINATION_RESULT_REFERENCE for path in paths):
            if direct_pair is not None:
                raise ValueError("more than one walk pair carries the direct result")
            direct_pair = pair
        for transition in pair["transitions"]:
            if not paths:
                unbound_transitions.append(transition)
                continue
            paths_by_top = {}
            for path in paths:
                paths_by_top.setdefault(path[0][1], []).append(path)
            for top_coordinate, top_paths in sorted(paths_by_top.items()):
                for operation in ("change", "remove_top_coordinate"):
                    control_payloads.append(
                        {
                            "source_number": transition["source_number"],
                            "target_append_position": transition[
                                "later_walk_first_append_position"
                            ],
                            "paths": top_paths,
                            "operation": operation,
                            "top_coordinate": top_coordinate,
                        }
                    )
                    control_coordinates.append(
                        {
                            "first_walk_identity_sha256": pair[
                                "first_walk_identity_sha256"
                            ],
                            "later_walk_identity_sha256": pair[
                                "later_walk_identity_sha256"
                            ],
                            "first_walk_last_append_position": transition[
                                "first_walk_last_append_position"
                            ],
                            "top_coordinate_material_sha256": name_sha256s[
                                top_coordinate
                            ],
                            "changed_coordinate_address_sha256s": sorted(
                                _digest(_encoded(path)) for path in top_paths
                            ),
                        }
                    )

    if direct_pair is None:
        raise ValueError("no walk pair carries the direct result reference")
    direct_payloads = []
    direct_coordinates = []
    for transition in direct_pair["transitions"]:
        direct_payloads.append(
            {
                "source_number": transition["source_number"],
                "target_append_position": transition[
                    "later_walk_first_append_position"
                ],
                "operation": "wrong_iteration",
            }
        )
        direct_coordinates.append(
            {
                "first_walk_identity_sha256": direct_pair[
                    "first_walk_identity_sha256"
                ],
                "later_walk_identity_sha256": direct_pair[
                    "later_walk_identity_sha256"
                ],
                "first_walk_last_append_position": transition[
                    "first_walk_last_append_position"
                ],
            }
        )

    with ProcessPoolExecutor(max_workers=arguments.jobs) as executor:
        control_findings = list(executor.map(_exercise_payload, control_payloads))
        direct_refusals = list(executor.map(_exercise_payload, direct_payloads))
    for finding, coordinates in zip(
        control_findings, control_coordinates, strict=True
    ):
        finding.update(coordinates)
    for finding, coordinates in zip(
        direct_refusals, direct_coordinates, strict=True
    ):
        finding.update(coordinates)

    result = {
        "source_artifact_sha256": _digest(
            artifact_materials[str(arguments.source)]
        ),
        "occurrence_surface_artifact_sha256": _digest(
            artifact_materials[str(arguments.surfaces)]
        ),
        "walk_artifact_sha256": _digest(
            artifact_materials[str(arguments.walks)]
        ),
        "walk_continuity_artifact_sha256": _digest(
            artifact_materials[str(arguments.continuities)]
        ),
        "coordinate_material_artifact_sha256": _digest(
            artifact_materials[str(arguments.coordinate_materials)]
        ),
        "operation": (
            "change or remove each exact non-boundary top coordinate carried "
            "into each later assignment, one top coordinate at a time, then "
            "retain the existing runtime decision; separately substitute one "
            "intact addressed result reference from an earlier iteration"
        ),
        "coordinate_control_findings": control_findings,
        "coordinate_control_count": len(control_findings),
        "coordinate_control_refusal_count": sum(
            finding["refused"] for finding in control_findings
        ),
        "coordinate_control_acceptance_count": sum(
            not finding["refused"] for finding in control_findings
        ),
        "unbound_transitions": unbound_transitions,
        "unbound_transition_count": len(unbound_transitions),
        "direct_result_findings": direct_refusals,
        "direct_result_finding_count": len(direct_refusals),
        "direct_result_refusal_count": sum(
            finding["refused"] for finding in direct_refusals
        ),
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(
        "coordinate controls: "
        f"{result['coordinate_control_count']} "
        f"refused={result['coordinate_control_refusal_count']} "
        f"accepted={result['coordinate_control_acceptance_count']}"
    )
    print(
        "direct result controls: "
        f"{result['direct_result_finding_count']} "
        f"refused={result['direct_result_refusal_count']}"
    )
    print(f"unbound transitions: {result['unbound_transition_count']}")
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
