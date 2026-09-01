"""Observe repeated runtime handoffs that have no recorded relation witness.

This pytest plugin records exact append-order occurrence references.  It does
not infer a relation from a reference, shared material, a name, a directory, or
source wording.  After the run it separates references already carried inside
an explicit relation coordinate from repeated bare handoffs.  The latter are
observer questions, not established Seed relations.

Set ``SEED_RELATION_HOLE_OBSERVATION`` to an output path when invoking pytest.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from contextvars import ContextVar
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
from typing import Any, Iterable

import pytest

from seed_runtime.event import Event
from seed_runtime.events import EventLedger, SQLiteEventLedger


OUTPUT_ENVIRONMENT_COORDINATE = "SEED_RELATION_HOLE_OBSERVATION"
CONSEQUENCE_RUNG_COUNT_BOUNDARY = 8
OBSERVER_STATEMENT = (
    "exact append-order occurrence references; a reference carries no "
    "relation unless a recorded relation carries both occurrences as "
    "its first and second subjects"
)

_current_test: ContextVar[str | None] = ContextVar(
    "relation_hole_test", default=None
)
_ledger_ordinals: dict[object, int] = {}
_ledger_positions: Counter[int] = Counter()
_seen_occurrences: set[tuple[int, str]] = set()
_captured: list[dict[str, Any]] = []
_originals: list[tuple[type, str, object]] = []


def _digest(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
    ).hexdigest()


def _ledger_ordinal(ledger: object) -> int:
    ordinal = _ledger_ordinals.get(ledger)
    if ordinal is None:
        ordinal = len(_ledger_ordinals)
        _ledger_ordinals[ledger] = ordinal
    return ordinal


def _capture(ledger: object, events: Iterable[Event]) -> None:
    test = _current_test.get()
    if test is None:
        return
    ordinal = _ledger_ordinal(ledger)
    for event in events:
        key = (ordinal, event.identity)
        if key in _seen_occurrences:
            continue
        _seen_occurrences.add(key)
        copied = deepcopy(event)
        position = _ledger_positions[ordinal]
        _ledger_positions[ordinal] += 1
        _captured.append(
            {
                "test": test,
                "ledger": ordinal,
                "append_position": position,
                "identity": copied.identity,
                "kind": copied.kind,
                "material": copied.material,
                "material_digest": _digest(copied.material),
                "exact_material_byte_count": (
                    None
                    if copied.exact_material is None
                    else len(copied.exact_material)
                ),
                "exact_material_digest": (
                    None
                    if copied.exact_material is None
                    else sha256(copied.exact_material).hexdigest()
                ),
                "locality_identity": copied.locality_identity,
            }
        )


def _install_capture(cls: type, method_name: str) -> None:
    original = getattr(cls, method_name)
    _originals.append((cls, method_name, original))

    if method_name == "append":

        def wrapped(ledger, *args, **kwargs):
            event = original(ledger, *args, **kwargs)
            _capture(ledger, (event,))
            return event

    else:

        def wrapped(ledger, *args, **kwargs):
            events = original(ledger, *args, **kwargs)
            _capture(ledger, events)
            return events

    setattr(cls, method_name, wrapped)


def pytest_configure(config: object) -> None:
    del config
    for cls in (EventLedger, SQLiteEventLedger):
        for method_name in ("append", "append_many"):
            _install_capture(cls, method_name)


def pytest_unconfigure(config: object) -> None:
    del config
    while _originals:
        cls, method_name, original = _originals.pop()
        setattr(cls, method_name, original)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item: object, nextitem: object):
    del nextitem
    token = _current_test.set(item.nodeid)
    try:
        yield
    finally:
        _current_test.reset(token)


def _coordinate(material: dict[str, Any], name: str) -> object:
    direct = material.get(name)
    if direct is not None:
        return direct
    dimensions = material.get("dimensions")
    if isinstance(dimensions, dict):
        direct = dimensions.get(name)
        if direct is not None:
            return direct
    coordinates = material.get("coordinates")
    if isinstance(coordinates, dict):
        return coordinates.get(name)
    return None


def _normalize_path(path: tuple[object, ...]) -> tuple[object, ...]:
    return tuple("#" if isinstance(part, int) else part for part in path)


def _string_paths(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield from _string_paths(nested, path + (key,))
    elif isinstance(value, (list, tuple)):
        for position, nested in enumerate(value):
            yield from _string_paths(nested, path + (position,))
    elif isinstance(value, str):
        yield path, value


def _key_value_paths(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield path + (key,), key, nested
            yield from _key_value_paths(nested, path + (key,))
    elif isinstance(value, (list, tuple)):
        for position, nested in enumerate(value):
            yield from _key_value_paths(nested, path + (position,))


def _relation_coordinates(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        if (
            {"first_subject", "second_subject"} <= set(value)
            and (
                "relation" in value
                or "relation_occurrence_identity" in value
            )
        ):
            yield {
                "path": path,
                "relation": value.get("relation"),
                "relation_content_present": "relation" in value,
                "first_subject": value["first_subject"],
                "second_subject": value["second_subject"],
            }
        for key, nested in value.items():
            yield from _relation_coordinates(nested, path + (key,))
    elif isinstance(value, (list, tuple)):
        for position, nested in enumerate(value):
            yield from _relation_coordinates(nested, path + (position,))


def _path_within(path: tuple[object, ...], parent: tuple[object, ...]) -> bool:
    return len(path) >= len(parent) and path[: len(parent)] == parent


def _subject_occurrences(value: object, known: set[str]) -> set[str]:
    """Exact recorded occurrences a relation subject carries.

    A subject is not always the occurrence itself.  Observed material carries a
    coordinate whose value is the exact occurrence, so the occurrence is
    collected wherever it is recorded within the subject.  A string that is not
    a captured occurrence is not an occurrence and is not collected.
    """

    return {
        carried
        for _path, carried in _string_paths(value)
        if carried in known
    } | ({value} if isinstance(value, str) and value in known else set())


def _recorded_relations(
    events: list[dict[str, Any]],
    known: set[str],
) -> list[dict[str, Any]]:
    """Every relation coordinate recorded anywhere in this ledger population."""

    population = []
    for index, event in enumerate(events):
        for relation in _relation_coordinates(event["material"]):
            first = _subject_occurrences(relation["first_subject"], known)
            second = _subject_occurrences(relation["second_subject"], known)
            population.append(
                {
                    "recorded_by_index": index,
                    "recorded_by_occurrence": event["identity"],
                    "path": relation["path"],
                    "relation": relation["relation"],
                    "relation_content_present": relation[
                        "relation_content_present"
                    ],
                    "first_subject_occurrences": first,
                    "second_subject_occurrences": second,
                    "first_subject_occurrence_count": len(first),
                    "second_subject_occurrence_count": len(second),
                }
            )
    return population


def _relation_subject_positions(
    population: list[dict[str, Any]],
) -> tuple[dict[str, list[int]], dict[str, list[int]]]:
    first_index: dict[str, list[int]] = defaultdict(list)
    second_index: dict[str, list[int]] = defaultdict(list)
    for position, relation in enumerate(population):
        for identity in relation["first_subject_occurrences"]:
            first_index[identity].append(position)
        for identity in relation["second_subject_occurrences"]:
            second_index[identity].append(position)
    return first_index, second_index


def _recorded_relation_record(
    relation: dict[str, Any],
    subject_order: str,
    destination_index: int,
) -> dict[str, Any]:
    rendered = relation["recorded_by_index"]
    if rendered == destination_index:
        position = "same_recorded_occurrence"
    elif rendered < destination_index:
        position = "earlier_recorded_occurrence"
    else:
        position = "later_recorded_occurrence"
    return {
        "subject_order": subject_order,
        "relation": relation["relation"],
        "relation_content_present": relation["relation_content_present"],
        "recorded_by_occurrence": relation["recorded_by_occurrence"],
        "recorded_position": position,
        "relation_path": [str(part) for part in relation["path"]],
    }


RECORDED_RELATION_ORDER = (
    "no_recorded_relation",
    "second_and_first_subject",
    "first_and_second_subject",
)


def _relation_for_occurrence_pair(values: Iterable[str]) -> str:
    """The strongest relation recorded for any reference joining one pair.

    Several reference paths can join the same two occurrences.  One recorded
    relation whose subjects are that pair covers the pair, so the pair carries
    no recorded relation only when every one of its references carries none.
    """

    return max(
        values,
        key=RECORDED_RELATION_ORDER.index,
        default="no_recorded_relation",
    )


def _recorded_relation_for_pair(
    source_identity: str,
    destination_identity: str,
    destination_index: int,
    population: list[dict[str, Any]],
    first_index: dict[str, list[int]],
    second_index: dict[str, list[int]],
) -> tuple[str, list[dict[str, Any]], bool]:
    """Whether a recorded relation carries these two occurrences as subjects.

    The question is only whether the two occurrences are the first and second
    subjects of some recorded relation.  Being carried within a relation
    coordinate is not the same, and a relation recorded in a third occurrence
    carries the pair just as well as one recorded beside the reference.  Both
    subject orders are searched separately because the grammar orders its
    subjects.

    Both occurrences carried inside one subject is reported separately and is
    not a weaker carriage of the pair.  A subject that carries two occurrences
    is one compound coordinate, so neither occurrence is established as the
    other's counterpart.
    """

    records: list[dict[str, Any]] = []
    forward = set(first_index.get(source_identity, ())) & set(
        second_index.get(destination_identity, ())
    )
    reverse = set(first_index.get(destination_identity, ())) & set(
        second_index.get(source_identity, ())
    )
    for position in sorted(forward):
        records.append(
            _recorded_relation_record(
                population[position], "first_and_second", destination_index
            )
        )
    for position in sorted(reverse):
        records.append(
            _recorded_relation_record(
                population[position], "second_and_first", destination_index
            )
        )
    within_one_subject = bool(
        (
            set(first_index.get(source_identity, ()))
            & set(first_index.get(destination_identity, ()))
        )
        or (
            set(second_index.get(source_identity, ()))
            & set(second_index.get(destination_identity, ()))
        )
    )
    if forward:
        return "first_and_second_subject", records, within_one_subject
    if reverse:
        return "second_and_first_subject", records, within_one_subject
    return "no_recorded_relation", records, within_one_subject


def _event_shape(event: dict[str, Any]) -> dict[str, Any]:
    material = event["material"]
    relations = list(_relation_coordinates(material))
    return {
        "kind": event["kind"],
        "responsibility": _coordinate(material, "responsibility"),
        "exact_act": _coordinate(material, "exact_act"),
        "book_reference": _coordinate(material, "book_reference"),
        "material_keys": sorted(material),
        "relation_coordinate_count": len(relations),
        "relation_coordinate_missing_content_count": sum(
            not relation["relation_content_present"] for relation in relations
        ),
        "relation_contents": sorted(
            {
                str(relation["relation"])
                for relation in relations
                if relation["relation_content_present"]
            }
        ),
    }


def _consequence_traces(
    edges_from: dict[int, list[dict[str, Any]]],
    event_shapes: list[dict[str, Any]],
) -> list[list[dict[str, Any]]]:
    """Hash every later consequence once per depth.

    Append order makes the reference graph acyclic.  Reusing the prior-depth
    digest of each later occurrence avoids walking the same growing history
    separately for every edge.
    """

    traces: list[list[dict[str, Any]]] = [[] for _ in event_shapes]
    prior_depth_digest: list[str | None] = [None for _ in event_shapes]
    for depth in range(1, CONSEQUENCE_RUNG_COUNT_BOUNDARY + 1):
        current_depth_digest: list[str | None] = [None for _ in event_shapes]
        for source in range(len(event_shapes) - 1, -1, -1):
            branches = []
            for edge in edges_from.get(source, ()):
                destination = edge["destination_index"]
                branch = {
                    "reference_path": edge["reference_path"],
                    "recorded_relation": edge["recorded_relation"],
                    "destination_shape": event_shapes[destination],
                }
                if prior_depth_digest[destination] is not None:
                    branch["later_digest"] = prior_depth_digest[destination]
                branches.append(branch)
            if not branches:
                continue
            branches.sort(key=_digest)
            digest = _digest(branches)
            current_depth_digest[source] = digest
            traces[source].append(
                {
                    "depth": depth,
                    "immediate_reference_count": len(branches),
                    "shape_digest": digest,
                }
            )
        prior_depth_digest = current_depth_digest
    return traces


def _analyze() -> dict[str, Any]:
    by_ledger: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for event in _captured:
        by_ledger[event["ledger"]].append(event)

    all_edges: list[dict[str, Any]] = []
    missing_relation_content: dict[
        tuple[object, ...], list[dict[str, Any]]
    ] = defaultdict(list)
    unrendered_relation_occurrences: dict[
        tuple[object, ...], list[dict[str, Any]]
    ] = defaultdict(list)
    family_members: dict[tuple[object, ...], list[dict[str, Any]]] = defaultdict(
        list
    )
    transition_members: dict[
        tuple[object, ...], list[dict[str, Any]]
    ] = defaultdict(list)
    for ledger, events in sorted(by_ledger.items()):
        event_shapes = [_event_shape(event) for event in events]
        for index, event in enumerate(events):
            relations = list(_relation_coordinates(event["material"]))
            rendered_occurrence_identities = {
                nested.get("relation_occurrence_identity")
                for _path, _key, nested in _key_value_paths(event["material"])
                if isinstance(nested, dict)
                and {"first_subject", "second_subject"} <= set(nested)
                and isinstance(nested.get("relation_occurrence_identity"), str)
            }
            for relation in relations:
                if relation["relation_content_present"]:
                    continue
                key = (
                    event["kind"],
                    str(event_shapes[index]["book_reference"]),
                    _normalize_path(relation["path"]),
                )
                missing_relation_content[key].append(
                    {
                        "test": event["test"],
                        "ledger": ledger,
                        "event_identity": event["identity"],
                        "first_subject_type": type(
                            relation["first_subject"]
                        ).__name__,
                        "second_subject_type": type(
                            relation["second_subject"]
                        ).__name__,
                    }
                )
            for path, key_name, nested in _key_value_paths(event["material"]):
                if (
                    not isinstance(key_name, str)
                    or not key_name.endswith("relation_occurrence_identity")
                    or not isinstance(nested, str)
                    or nested in rendered_occurrence_identities
                ):
                    continue
                key = (
                    event["kind"],
                    str(event_shapes[index]["book_reference"]),
                    _normalize_path(path),
                )
                unrendered_relation_occurrences[key].append(
                    {
                        "test": event["test"],
                        "ledger": ledger,
                        "event_identity": event["identity"],
                    }
                )
        known_identities = {event["identity"] for event in events}
        relation_population = _recorded_relations(
            events, known_identities
        )
        first_index, second_index = _relation_subject_positions(relation_population)
        by_identity: dict[str, int] = {}
        edges_from: dict[int, list[dict[str, Any]]] = defaultdict(list)
        pending: list[dict[str, Any]] = []
        for destination, event in enumerate(events):
            relations = list(_relation_coordinates(event["material"]))
            for path, value in _string_paths(event["material"]):
                source = by_identity.get(value)
                if source is None:
                    continue
                reference_within_relation = any(
                    _path_within(path, relation["path"])
                    for relation in relations
                )
                (
                    recorded_relation,
                    records,
                    within_one_subject,
                ) = _recorded_relation_for_pair(
                    events[source]["identity"],
                    event["identity"],
                    destination,
                    relation_population,
                    first_index,
                    second_index,
                )
                source_shape = event_shapes[source]
                destination_shape = event_shapes[destination]
                normalized_path = _normalize_path(path)
                family_key = (
                    source_shape["kind"],
                    destination_shape["kind"],
                    normalized_path,
                    str(source_shape["book_reference"]),
                    str(destination_shape["book_reference"]),
                    recorded_relation,
                )
                edge = {
                    "ledger": ledger,
                    "test": event["test"],
                    "source_index": source,
                    "destination_index": destination,
                    "source_identity": events[source]["identity"],
                    "destination_identity": event["identity"],
                    "reference_path": list(normalized_path),
                    "recorded_relation": recorded_relation,
                    "recorded_relations": records,
                    "reference_within_relation_coordinate": reference_within_relation,
                    "both_occurrences_within_one_subject": within_one_subject,
                    "source_shape": source_shape,
                    "destination_shape": destination_shape,
                    "source_material_digest": events[source]["material_digest"],
                    "destination_material_digest": event["material_digest"],
                }
                pending.append(edge)
                edges_from[source].append(edge)
                family_members[family_key].append(edge)
                all_edges.append(edge)
            by_identity[event["identity"]] = destination
        consequence_traces = _consequence_traces(edges_from, event_shapes)
        for edge in pending:
            edge["later_consequences"] = consequence_traces[
                edge["destination_index"]
            ]
        occurrence_pairs: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(
            list
        )
        for edge in pending:
            occurrence_pairs[
                (edge["source_index"], edge["destination_index"])
            ].append(edge)
        for (_source, _destination), pair_edges in occurrence_pairs.items():
            first = pair_edges[0]
            source_shape = first["source_shape"]
            destination_shape = first["destination_shape"]
            recorded_relation = _relation_for_occurrence_pair(
                edge["recorded_relation"] for edge in pair_edges
            )
            transition_key = (
                source_shape["kind"],
                destination_shape["kind"],
                str(source_shape["book_reference"]),
                str(destination_shape["book_reference"]),
                recorded_relation,
            )
            transition_members[transition_key].append(
                {
                    "ledger": ledger,
                    "test": first["test"],
                    "source_identity": first["source_identity"],
                    "destination_identity": first["destination_identity"],
                    "reference_paths": sorted(
                        {
                            tuple(map(str, edge["reference_path"]))
                            for edge in pair_edges
                        }
                    ),
                    "recorded_relation": recorded_relation,
                    "source_shape": source_shape,
                    "destination_shape": destination_shape,
                    "source_material_digest": first["source_material_digest"],
                    "destination_material_digest": first[
                        "destination_material_digest"
                    ],
                    "later_consequences": first["later_consequences"],
                }
            )

    families = []
    for key, members in family_members.items():
        (
            source_kind,
            destination_kind,
            path,
            source_book,
            destination_book,
            recorded_relation,
        ) = key
        consequence_vectors = {
            tuple(
                (rung["immediate_reference_count"], rung["shape_digest"])
                for rung in member["later_consequences"]
            )
            for member in members
        }
        source_materials = {member["source_material_digest"] for member in members}
        destination_materials = {
            member["destination_material_digest"] for member in members
        }
        families.append(
            {
                "source_kind": source_kind,
                "destination_kind": destination_kind,
                "reference_path": list(path),
                "source_book_reference": None if source_book == "None" else source_book,
                "destination_book_reference": (
                    None if destination_book == "None" else destination_book
                ),
                "recorded_relation": recorded_relation,
                "occurrence_count": len(members),
                "test_count": len({member["test"] for member in members}),
                "ledger_count": len({member["ledger"] for member in members}),
                "distinct_source_material_count": len(source_materials),
                "distinct_destination_material_count": len(destination_materials),
                "distinct_consequence_count": len(consequence_vectors),
                "maximum_later_rungs": max(
                    (len(member["later_consequences"]) for member in members),
                    default=0,
                ),
                "samples": [
                    {
                        "test": member["test"],
                        "source_identity": member["source_identity"],
                        "destination_identity": member["destination_identity"],
                        "source_shape": member["source_shape"],
                        "destination_shape": member["destination_shape"],
                        "later_consequences": member["later_consequences"],
                    }
                    for member in members[:3]
                ],
            }
        )
    families.sort(
        key=lambda item: (
            RECORDED_RELATION_ORDER.index(item["recorded_relation"]),
            -item["test_count"],
            -item["occurrence_count"],
            item["source_kind"],
            item["destination_kind"],
            tuple(map(str, item["reference_path"])),
        )
    )

    repeated_bare = [
        family
        for family in families
        if family["recorded_relation"] == "no_recorded_relation"
        and family["occurrence_count"] > 1
        and family["distinct_source_material_count"] > 1
    ]

    transition_families = []
    for key, members in transition_members.items():
        (
            source_kind,
            destination_kind,
            source_book,
            destination_book,
            recorded_relation,
        ) = key
        transition_families.append(
            {
                "source_kind": source_kind,
                "destination_kind": destination_kind,
                "source_book_reference": (
                    None if source_book == "None" else source_book
                ),
                "destination_book_reference": (
                    None if destination_book == "None" else destination_book
                ),
                "recorded_relation": recorded_relation,
                "occurrence_pair_count": len(members),
                "test_count": len({member["test"] for member in members}),
                "ledger_count": len({member["ledger"] for member in members}),
                "distinct_source_material_count": len(
                    {member["source_material_digest"] for member in members}
                ),
                "distinct_destination_material_count": len(
                    {member["destination_material_digest"] for member in members}
                ),
                "distinct_reference_path_population_count": len(
                    {tuple(member["reference_paths"]) for member in members}
                ),
                "maximum_later_rungs": max(
                    (len(member["later_consequences"]) for member in members),
                    default=0,
                ),
                "samples": members[:3],
            }
        )
    transition_families.sort(
        key=lambda item: (
            RECORDED_RELATION_ORDER.index(item["recorded_relation"]),
            -item["test_count"],
            -item["occurrence_pair_count"],
            item["source_kind"],
            item["destination_kind"],
        )
    )
    repeated_bare_transitions = [
        family
        for family in transition_families
        if family["recorded_relation"] == "no_recorded_relation"
        and family["occurrence_pair_count"] > 1
        and family["distinct_source_material_count"] > 1
    ]

    def vacancy_rows(population):
        rows = []
        for (kind, book_reference, path), members in population.items():
            rows.append(
                {
                    "event_kind": kind,
                    "book_reference": (
                        None if book_reference == "None" else book_reference
                    ),
                    "coordinate_path": list(path),
                    "occurrence_count": len(members),
                    "test_count": len({member["test"] for member in members}),
                    "ledger_count": len({member["ledger"] for member in members}),
                    "samples": members[:3],
                }
            )
        rows.sort(
            key=lambda item: (
                -item["test_count"],
                -item["occurrence_count"],
                item["event_kind"],
                tuple(map(str, item["coordinate_path"])),
            )
        )
        return rows

    missing_content_rows = vacancy_rows(missing_relation_content)
    unrendered_rows = vacancy_rows(unrendered_relation_occurrences)
    recorded_relation_counts = Counter(
        edge["recorded_relation"] for edge in all_edges
    )
    carried_within_only = sum(
        edge["reference_within_relation_coordinate"]
        and edge["recorded_relation"] == "no_recorded_relation"
        for edge in all_edges
    )
    subjects_without_carriage = sum(
        not edge["reference_within_relation_coordinate"]
        and edge["recorded_relation"]
        in ("first_and_second_subject", "second_and_first_subject")
        for edge in all_edges
    )
    return {
        "observer": OBSERVER_STATEMENT,
        "captured_test_count": len({event["test"] for event in _captured}),
        "ledger_count": len(by_ledger),
        "event_count": len(_captured),
        "reference_edge_count": len(all_edges),
        "recorded_relation_counts": dict(sorted(recorded_relation_counts.items())),
        "reference_carried_within_relation_coordinate_only_count": (
            carried_within_only
        ),
        "relation_subjects_without_carriage_count": subjects_without_carriage,
        "reference_family_count": len(families),
        "reference_transition_family_count": len(transition_families),
        "repeated_bare_handoff_family_count": len(repeated_bare),
        "repeated_bare_transition_family_count": len(
            repeated_bare_transitions
        ),
        "relation_coordinate_missing_content_family_count": len(
            missing_content_rows
        ),
        "unrendered_relation_occurrence_family_count": len(unrendered_rows),
        "relation_coordinate_missing_content_families": missing_content_rows,
        "unrendered_relation_occurrence_families": unrendered_rows,
        "repeated_bare_handoff_families": repeated_bare,
        "repeated_bare_transition_families": repeated_bare_transitions,
        "reference_transition_families": transition_families,
        "all_reference_families": families,
    }


def pytest_sessionfinish(session: object, exitstatus: int) -> None:
    del session
    output = os.environ.get(OUTPUT_ENVIRONMENT_COORDINATE)
    if not output:
        return
    result = _analyze()
    result["pytest_exit_status"] = exitstatus
    result["structural_digest"] = _digest(result)
    path = Path(output)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(
        f"\nRELATION HOLES {path} events={result['event_count']} "
        f"edges={result['reference_edge_count']} "
        f"bare_families={result['repeated_bare_handoff_family_count']} "
        f"digest={result['structural_digest']}"
    )
