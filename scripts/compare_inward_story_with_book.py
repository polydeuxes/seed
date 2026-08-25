"""Place the frozen enforced inward story beside the active Book testimony.

The story and its enforced edges are already frozen without the Book.  This
post-freeze operation resolves each opaque walk to its current occurrence
material, preserves the Book clauses named by those occurrences, and records
the active Book and machine-grammar material separately.  Neither witness is
used to alter the other.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import time


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.book_admission import book_proper_files  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"
SOURCE = Path("/tmp/seed_inward_occurrence_material.json")
WALKS = Path("/tmp/seed_inward_frame_walks_blind.json")
REFUSALS = Path("/tmp/seed_inward_walk_binding_refusals.json")
GRAMMAR = BOOK / "witness_grammar.json"
OUTPUT = Path("/tmp/seed_inward_story_book_comparison.json")

CLAUSE = re.compile(
    r"^###\s+([0-9]+\.[A-Za-z][A-Za-z0-9.]*)\s+—\s*(.+)$", re.M
)
SECTION = re.compile(r"^##\s+(.+)$", re.M)
YIELD_EVENT_LABEL = "operator.yield_relation_recorded"


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _without_duplicates(values) -> list:
    found = {}
    for value in values:
        found[value] = None
    return list(found)


def _coordinate_names(material: object) -> list[str]:
    names = {}

    def visit(value: object) -> None:
        if type(value) is dict:
            for coordinate, carried in value.items():
                names[coordinate] = None
                visit(carried)
        elif type(value) is list:
            for carried in value:
                visit(carried)

    visit(material)
    return sorted(names)


def _values_at_coordinate(material: object, coordinate: str) -> list[object]:
    values = []

    def visit(value: object) -> None:
        if type(value) is dict:
            for name, carried in value.items():
                if name == coordinate:
                    values.append(carried)
                visit(carried)
        elif type(value) is list:
            for carried in value:
                visit(carried)

    visit(material)
    return values


def _relation_material(material: object, relation: str) -> list[dict]:
    findings = []

    def visit(value: object) -> None:
        if type(value) is dict:
            if value.get("relation") == relation:
                findings.append(value)
            for carried in value.values():
                visit(carried)
        elif type(value) is list:
            for carried in value:
                visit(carried)

    visit(material)
    return findings


def _carried_dicts_at_coordinates(
    material: object, coordinates: tuple[str, ...]
) -> list[dict]:
    findings = []
    for coordinate in coordinates:
        for carried in _values_at_coordinate(material, coordinate):
            if type(carried) is dict:
                findings.append(carried)
            elif type(carried) is list:
                findings.extend(item for item in carried if type(item) is dict)
    return findings


def _identified_clauses() -> dict[str, dict[str, str]]:
    identified = {}
    for path in sorted((BOOK / "chapters").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        matches = list(CLAUSE.finditer(text))
        for number, match in enumerate(matches):
            end = matches[number + 1].start() if number + 1 < len(matches) else len(text)
            body = text[match.end() : end]
            references = body.find("\n## References")
            if references >= 0:
                body = body[:references]
            identified[match.group(1)] = {
                "chapter": path.relative_to(ROOT).as_posix(),
                "heading": match.group(2).strip(),
                "text": body.strip(),
            }
    return identified


def _readme_sections() -> dict[str, str]:
    path = BOOK / "README.md"
    text = path.read_text(encoding="utf-8")
    matches = list(SECTION.finditer(text))
    sections = {}
    for number, match in enumerate(matches):
        end = matches[number + 1].start() if number + 1 < len(matches) else len(text)
        sections[match.group(1).strip()] = text[match.end() : end].strip()
    return sections


def _bound_walk_identities(refusals: dict) -> list[str]:
    identities = {}
    for finding in refusals["coordinate_control_findings"]:
        identities[finding["first_walk_identity_sha256"]] = None
        identities[finding["later_walk_identity_sha256"]] = None
    unbound_later = {
        transition["later_walk_identity_sha256"]: None
        for transition in refusals["unbound_transitions"]
    }
    for identity in unbound_later:
        identities.pop(identity, None)
    return sorted(identities)


def _walk_finding(exact_walk: dict, sources: list[dict]) -> dict[str, object]:
    label_sequences = []
    event_occurrences = []
    for source_number, start, end in exact_walk["addresses"]:
        occurrences = sources[source_number]["occurrences"]
        addressed = occurrences[start:end]
        if len(addressed) != end - start:
            raise ValueError("one exact walk address exceeds its source")
        if any(
            occurrence["append_position"] != start + position
            for position, occurrence in enumerate(addressed)
        ):
            raise ValueError("one exact walk address does not match append positions")
        label_sequences.append(tuple(item["event_label"] for item in addressed))
        event_occurrences.extend((source_number, item) for item in addressed)
    one_sequence = _without_duplicates(label_sequences)
    if len(one_sequence) != 1:
        raise ValueError("one opaque walk identity resolves to different event labels")

    coordinate_names = {}
    clause_identities = {}
    participation_relations = 0
    carriage_relations = 0
    participation_identities = {}
    carriage_identities = {}
    for source_number, occurrence in event_occurrences:
        material = occurrence["material"]
        for name in _coordinate_names(material):
            coordinate_names[name] = None
        for clause in _values_at_coordinate(material, "book_clause_identity"):
            if type(clause) is str:
                clause_identities[clause] = None
        related_participation = _relation_material(material, "participation")
        related_carriage = _relation_material(material, "carriage")
        participation_relations += len(related_participation)
        carriage_relations += len(related_carriage)
        carried_participation = _carried_dicts_at_coordinates(
            material, ("participation", "participation_of_input_in_compare")
        )
        for carried in carried_participation:
            identity = carried.get("relation_occurrence_identity", carried.get("identity"))
            if type(identity) is str:
                participation_identities[(source_number, identity)] = None
        for carried in related_carriage:
            identity = carried.get("relation_occurrence_identity", carried.get("identity"))
            if type(identity) is str:
                carriage_identities[(source_number, identity)] = None

    labels = one_sequence[0]
    return {
        "walk_identity_sha256": exact_walk["walk_identity_sha256"],
        "walk_length": exact_walk["walk_length"],
        "walk_occurrence_count": exact_walk["occurrence_count"],
        "event_labels": list(labels),
        "book_clause_identities": sorted(clause_identities),
        "coordinate_names": sorted(coordinate_names),
        "responsibility_assignment_occurrence_count": sum(
            label.endswith("responsibility_assignment_recorded") for label in labels
        )
        * exact_walk["occurrence_count"],
        "yield_occurrence_count": labels.count(YIELD_EVENT_LABEL)
        * exact_walk["occurrence_count"],
        "nested_participation_relation_count": participation_relations,
        "nested_carriage_relation_count": carriage_relations,
        "exact_participation_relation_identity_count": len(participation_identities),
        "exact_carriage_relation_identity_count": len(carriage_identities),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--walks", type=Path, default=WALKS)
    parser.add_argument("--refusals", type=Path, default=REFUSALS)
    parser.add_argument("--grammar", type=Path, default=GRAMMAR)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    begun = time.perf_counter()
    source_bytes = arguments.source.read_bytes()
    walk_bytes = arguments.walks.read_bytes()
    refusal_bytes = arguments.refusals.read_bytes()
    grammar_bytes = arguments.grammar.read_bytes()
    source = json.loads(source_bytes)
    walks = json.loads(walk_bytes)
    refusals = json.loads(refusal_bytes)
    grammar = json.loads(grammar_bytes)
    if any(
        finding.get("known_loss") is not None
        for finding in (source, walks, refusals)
    ):
        raise ValueError("one supplied inward finding carries known loss")
    if refusals.get("source_artifact_sha256") != _digest(source_bytes):
        raise ValueError("refusal finding does not address the supplied source")
    if refusals.get("walk_artifact_sha256") != _digest(walk_bytes):
        raise ValueError("refusal finding does not address the supplied walks")

    bound_identities = _bound_walk_identities(refusals)
    exact_walk_by_identity = {
        walk["walk_identity_sha256"]: walk for walk in walks["exact_walks"]
    }
    if any(identity not in exact_walk_by_identity for identity in bound_identities):
        raise ValueError("one bound walk identity is absent from the walk finding")
    story_walks = [
        _walk_finding(exact_walk_by_identity[identity], source["sources"])
        for identity in bound_identities
    ]
    story_occurrence_count = sum(
        walk["walk_length"] * walk["walk_occurrence_count"]
        for walk in story_walks
    )

    story_clause_identities = sorted(
        {
            clause: None
            for walk in story_walks
            for clause in walk["book_clause_identities"]
        }
    )
    governing_clause_identities = (
        "01.Current.A",
        "01.Current.A.1",
        "01.Current.E.1",
        "02.Acts.A",
        "08.Support.A",
        "08.Scope.A",
    )
    clauses = _identified_clauses()
    compared_clause_identities = _without_duplicates(
        [*governing_clause_identities, *story_clause_identities]
    )
    if any(identity not in clauses for identity in compared_clause_identities):
        raise ValueError("one compared Book clause is absent from active chapters")

    book_files = []
    for path in sorted(book_proper_files()):
        material = path.read_bytes()
        book_files.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "byte_count": len(material),
                "sha256": _digest(material),
            }
        )

    relevant_grammar = {
        "standing": grammar["standing"],
        "responsibility": grammar["responsibility"],
        "participation": grammar["relations"]["participation"],
        "carriage": grammar["relations"]["carriage"],
        "yield": grammar["relations"]["yield"],
        "book_coordinates": {
            identity: grammar["book_coordinates"].get(identity)
            for identity in compared_clause_identities
        },
    }
    result = {
        "source_artifact_sha256": _digest(source_bytes),
        "walk_artifact_sha256": _digest(walk_bytes),
        "binding_refusal_artifact_sha256": _digest(refusal_bytes),
        "machine_grammar_sha256": _digest(grammar_bytes),
        "operation": (
            "resolve only the already frozen enforced walk identities to their "
            "current occurrence material, then place their exact forms beside "
            "the separately read active Book and machine grammar"
        ),
        "book_files": book_files,
        "bound_walk_identity_sha256s": bound_identities,
        "story_walks": story_walks,
        "story_walk_form_count": len(story_walks),
        "story_walk_occurrence_count": sum(
            walk["walk_occurrence_count"] for walk in story_walks
        ),
        "story_occurrence_count": story_occurrence_count,
        "story_responsibility_assignment_occurrence_count": sum(
            walk["responsibility_assignment_occurrence_count"]
            for walk in story_walks
        ),
        "story_yield_occurrence_count": sum(
            walk["yield_occurrence_count"] for walk in story_walks
        ),
        "story_nested_participation_relation_count": sum(
            walk["nested_participation_relation_count"] for walk in story_walks
        ),
        "story_nested_carriage_relation_count": sum(
            walk["nested_carriage_relation_count"] for walk in story_walks
        ),
        "story_exact_participation_relation_identity_count": sum(
            walk["exact_participation_relation_identity_count"]
            for walk in story_walks
        ),
        "story_exact_carriage_relation_identity_count": sum(
            walk["exact_carriage_relation_identity_count"]
            for walk in story_walks
        ),
        "story_clause_identities": story_clause_identities,
        "compared_book_clauses": {
            identity: clauses[identity] for identity in compared_clause_identities
        },
        "readme_sections": {
            name: text
            for name, text in _readme_sections().items()
            if name in ("Standing", "Responsibility", "Act and occurrence")
        },
        "machine_grammar": relevant_grammar,
        "known_loss": None,
    }
    encoded = _encoded(result)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"story walk forms: {result['story_walk_form_count']}")
    print(f"story occurrences: {result['story_occurrence_count']}")
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
