#!/usr/bin/env python3
"""Measure exact relations between frozen enforced inward stories.

The walk and refusal findings are already frozen. This operation reads only
opaque walk identities, exact walk addresses, refusal booleans, and the frozen
unbound transitions. It receives no event labels, Book material, coordinate
names, Root, or desired larger flow.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import factorial
from pathlib import Path
import time


WALKS = Path("/tmp/seed_inward_frame_walks_blind.json")
REFUSALS = Path("/tmp/seed_inward_walk_binding_refusals.json")
OUTPUT = Path("/tmp/seed_inward_story_flows_blind.json")


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _read_artifacts(walk_path: Path, refusal_path: Path) -> tuple[dict, dict, bytes, bytes]:
    walk_bytes = walk_path.read_bytes()
    refusal_bytes = refusal_path.read_bytes()
    walks = json.loads(walk_bytes)
    refusals = json.loads(refusal_bytes)
    if walks.get("known_loss") is not None or refusals.get("known_loss") is not None:
        raise ValueError("one frozen inward finding carries known loss")
    if refusals.get("walk_artifact_sha256") != _digest(walk_bytes):
        raise ValueError("refusals do not address the supplied walks")
    return walks, refusals, walk_bytes, refusal_bytes


def _edge_forms(refusals: dict) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    enforced = {
        (
            finding["first_walk_identity_sha256"],
            finding["later_walk_identity_sha256"],
        )
        for finding in refusals["coordinate_control_findings"]
        if finding["refused"]
    }
    unbound = {
        (
            finding["first_walk_identity_sha256"],
            finding["later_walk_identity_sha256"],
        )
        for finding in refusals["unbound_transitions"]
    }
    overlap = enforced & unbound
    if overlap:
        raise ValueError("one walk edge is both enforced and unbound")
    return enforced, unbound


def _story_occurrences(
    source_walk_sequences: list[dict], enforced: set[tuple[str, str]]
) -> list[dict]:
    stories = []
    for source in source_walk_sequences:
        source_number = source["source_number"]
        identities = source["walk_identity_sha256s"]
        addresses = source["walk_addresses"]
        if len(identities) != len(addresses):
            raise ValueError("walk identities and addresses differ in count")
        for number, address in enumerate(addresses):
            if len(address) != 2 or address[0] >= address[1]:
                raise ValueError("one walk address is not exact")
            if number and addresses[number - 1][1] != address[0]:
                raise ValueError("one source walk sequence is not consecutive")

        start = 0
        for first_position in range(len(identities) - 1):
            pair = (identities[first_position], identities[first_position + 1])
            if pair in enforced:
                continue
            end = first_position + 1
            if end - start > 1:
                stories.append(
                    _story_occurrence(source_number, identities, addresses, start, end)
                )
            start = end
        if len(identities) - start > 1:
            stories.append(
                _story_occurrence(
                    source_number, identities, addresses, start, len(identities)
                )
            )
    return stories


def _story_occurrence(
    source_number: int,
    identities: list[str],
    addresses: list[list[int]],
    start: int,
    end: int,
) -> dict:
    carried_identities = identities[start:end]
    carried_addresses = addresses[start:end]
    material = {
        "source_number": source_number,
        "first_walk_position": start,
        "later_walk_position": end,
        "walk_identity_sha256s": carried_identities,
        "walk_addresses": carried_addresses,
    }
    return {
        **material,
        "story_identity_sha256": _digest(_encoded(material)),
        "first_append_position": carried_addresses[0][0],
        "later_append_position": carried_addresses[-1][1],
    }


def _story_neighbors(stories: list[dict], source_walk_sequences: list[dict]) -> list[dict]:
    sources = {source["source_number"]: source for source in source_walk_sequences}
    findings = []
    for story in stories:
        source = sources[story["source_number"]]
        identities = source["walk_identity_sha256s"]
        addresses = source["walk_addresses"]
        first = story["first_walk_position"]
        later = story["later_walk_position"]
        finding = {
            "source_number": story["source_number"],
            "story_identity_sha256": story["story_identity_sha256"],
            "preceding_walk": None,
            "later_walk": None,
        }
        if first:
            finding["preceding_walk"] = {
                "walk_identity_sha256": identities[first - 1],
                "walk_address": addresses[first - 1],
            }
        if later < len(identities):
            finding["later_walk"] = {
                "walk_identity_sha256": identities[later],
                "walk_address": addresses[later],
            }
        findings.append(finding)
    return findings


def _adjacent_story_pairs(stories: list[dict]) -> list[dict]:
    by_source: dict[int, list[dict]] = {}
    for story in stories:
        by_source.setdefault(story["source_number"], []).append(story)
    findings = []
    for source_number, addressed in sorted(by_source.items()):
        ordered = sorted(addressed, key=lambda story: story["first_walk_position"])
        for first, later in zip(ordered, ordered[1:]):
            if first["later_walk_position"] == later["first_walk_position"]:
                findings.append(
                    {
                        "source_number": source_number,
                        "first_story_identity_sha256": first["story_identity_sha256"],
                        "later_story_identity_sha256": later["story_identity_sha256"],
                    }
                )
    return findings


def _shared_internal_edge_forms(stories: list[dict]) -> set[tuple[str, str]]:
    edge_forms = [
        set(zip(story["walk_identity_sha256s"], story["walk_identity_sha256s"][1:]))
        for story in stories
    ]
    if not edge_forms:
        return set()
    return set.intersection(*edge_forms)


def _artifact_order_controls(stories: list[dict]) -> dict:
    return {
        "artifact_story_order_count": factorial(len(stories)),
        "artifact_order_creates_source_transition": False,
        "reversed_artifact_order_creates_source_transition": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--walks", type=Path, default=WALKS)
    parser.add_argument("--refusals", type=Path, default=REFUSALS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    begun = time.perf_counter()
    walks, refusals, walk_bytes, refusal_bytes = _read_artifacts(
        arguments.walks, arguments.refusals
    )
    enforced, unbound = _edge_forms(refusals)
    stories = _story_occurrences(walks["source_walk_sequences"], enforced)
    neighbors = _story_neighbors(stories, walks["source_walk_sequences"])
    adjacent_story_pairs = _adjacent_story_pairs(stories)
    shared_internal_edges = _shared_internal_edge_forms(stories)
    if adjacent_story_pairs:
        raise ValueError(
            "story-to-story adjacency requires an exact continuity measurement"
        )
    story_by_identity = {
        story["story_identity_sha256"]: story for story in stories
    }
    unbound_later_neighbors = [
        finding
        for finding in neighbors
        if finding["later_walk"] is not None
        and (
            story_by_identity[finding["story_identity_sha256"]][
                "walk_identity_sha256s"
            ][-1],
            finding["later_walk"]["walk_identity_sha256"],
        )
        in unbound
    ]

    result = {
        "operation": (
            "opaque exact story occurrences from maximal consecutive enforced "
            "walk edges; exact story neighbors and story-to-story adjacency"
        ),
        "walk_artifact_sha256": _digest(walk_bytes),
        "binding_refusal_artifact_sha256": _digest(refusal_bytes),
        "enforced_edge_forms": [list(pair) for pair in sorted(enforced)],
        "unbound_edge_forms": [list(pair) for pair in sorted(unbound)],
        "story_occurrence_count": len(stories),
        "exact_story_identity_count": len(
            {story["story_identity_sha256"] for story in stories}
        ),
        "shared_internal_edge_form_count": len(shared_internal_edges),
        "shared_internal_edge_forms": [
            list(pair) for pair in sorted(shared_internal_edges)
        ],
        "every_enforced_edge_form_occurs_in_every_story": (
            shared_internal_edges == enforced
        ),
        "story_occurrences": stories,
        "story_neighbors": neighbors,
        "adjacent_story_pair_count": len(adjacent_story_pairs),
        "adjacent_story_pairs": adjacent_story_pairs,
        "unbound_later_neighbor_count": len(unbound_later_neighbors),
        "unbound_later_neighbors": unbound_later_neighbors,
        "inter_story_carried_coordinate_count": 0,
        "inter_story_reader_control_count": 0,
        "artifact_order_controls": _artifact_order_controls(stories),
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"stories: {len(stories)}")
    print(f"adjacent story pairs: {len(adjacent_story_pairs)}")
    print(f"unbound later neighbors: {len(unbound_later_neighbors)}")
    print(f"reader controls: {result['inter_story_reader_control_count']}")
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
