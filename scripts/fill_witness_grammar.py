"""Fill exact Book-to-witness-grammar coordinates without sorting them."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"
GRAMMAR = BOOK / "grammar.json"
ADMISSION = BOOK / "book_admission.txt"
CHAPTERS = BOOK / "chapters"

BOOK_MATERIALS = (
    CHAPTERS / "01_source_coordinates_and_grammar.md",
    CHAPTERS / "02_constitutional_standing.md",
    CHAPTERS / "03_acts_and_occurrences.md",
    CHAPTERS / "06_movement_coordinates.md",
    CHAPTERS / "07_result_boundaries_and_movement.md",
    CHAPTERS / "09_assertion_source_coordinates.md",
    CHAPTERS / "10_evidence_and_provenance.md",
    CHAPTERS / "11_recording_and_preserved_assertions.md",
    CHAPTERS / "12_locality_relations.md",
    CHAPTERS / "13_authority_scope.md",
    CHAPTERS / "14_representation_emission_and_locality.md",
    CHAPTERS / "15_stopping_and_completion.md",
    BOOK / "README.md",
    BOOK / "concordance.md",
)

EMPTY_KIND = b'      "recorded_occurrence_kind": [],'
FIDELITY_KIND = b'      "recorded_occurrence_kind": ["Fidelity_occurrence"],'
VOCABULARY_MARKER = b'  "book_vocabulary": {'
NEXT_SECTION_MARKER = b'  "completeness": {'


def _words(material: str) -> tuple[str, ...]:
    without_targets = re.sub(r"\]\([^)]*\)", "]()", material)
    divided = re.sub(r"[_-]+", " ", without_targets)
    return tuple(re.findall(r"[A-Za-z]+", divided.lower()))


def _admission() -> set[str]:
    return {
        line.split("#", 1)[0].strip()
        for line in ADMISSION.read_text(encoding="utf-8").splitlines()
        if line.split("#", 1)[0].strip()
    }


def expected_book_vocabulary(grammar_bytes: bytes) -> dict:
    grammar = json.loads(grammar_bytes)
    grammar.pop("book_vocabulary", None)
    base_words = set(_words(json.dumps(grammar, ensure_ascii=False)))
    missing = _admission() - base_words

    first_positions: dict[str, int] = {}
    position = 0
    for path in BOOK_MATERIALS:
        if not path.is_file():
            raise ValueError("declared Book material is absent")
        for word in _words(path.read_text(encoding="utf-8")):
            first_positions.setdefault(word, position)
            position += 1
    if missing - set(first_positions):
        raise ValueError("Book admission carries material absent from this Book")

    return {
        "subject": "this_Book",
        "coordinates": ["entry", "first_occurrence_position"],
        "ordered_entries": [
            [word, first_position]
            for word, first_position in first_positions.items()
            if word in missing
        ],
    }


def _render_vocabulary(section: dict) -> bytes:
    entries = section["ordered_entries"]
    lines = [
        '  "book_vocabulary": {',
        f'    "subject": {json.dumps(section["subject"])},',
        '    "coordinates": ["entry", "first_occurrence_position"],',
        '    "ordered_entries": [',
    ]
    lines.extend(
        "      "
        + json.dumps(entry, ensure_ascii=False)
        + ("," if position + 1 < len(entries) else "")
        for position, entry in enumerate(entries)
    )
    lines.extend(("    ]", "  },"))
    return ("\n".join(lines) + "\n").encode()


def _carry_vocabulary(grammar_bytes: bytes, section: dict) -> bytes:
    block = _render_vocabulary(section)
    next_position = grammar_bytes.find(NEXT_SECTION_MARKER)
    if next_position < 0:
        raise ValueError("witness grammar completeness boundary is absent")
    start = grammar_bytes.find(VOCABULARY_MARKER)
    if start < 0:
        return grammar_bytes[:next_position] + block + grammar_bytes[next_position:]
    if start >= next_position:
        raise ValueError("Book vocabulary is outside its declared position")
    return grammar_bytes[:start] + block + grammar_bytes[next_position:]


def fill_fidelity_occurrence_kinds(
    grammar_bytes: bytes,
) -> tuple[bytes, tuple[str, ...]]:
    grammar = json.loads(grammar_bytes)
    missing = tuple(
        identity
        for identity, clause in grammar["clauses"].items()
        if clause["recorded_occurrence_kind"] == []
    )
    if grammar_bytes.count(EMPTY_KIND) != len(missing):
        raise ValueError("empty occurrence-kind coordinates are not exact")

    book = b"\n".join(path.read_bytes() for path in BOOK_MATERIALS)
    for identity in missing:
        if book.count(f"### {identity} ".encode()) != 1:
            raise ValueError("witness grammar clause has no exact Book clause")

    filled = grammar_bytes.replace(EMPTY_KIND, FIDELITY_KIND)
    parsed = json.loads(filled)
    allowed = {
        ("event_occurrence",),
        ("Assertion_occurrence",),
        ("Fidelity_occurrence",),
    }
    if any(
        tuple(clause["recorded_occurrence_kind"]) not in allowed
        for clause in parsed["clauses"].values()
    ):
        raise ValueError("witness grammar clause occurrence family is incomplete")
    return filled, missing


def fill_witness_grammar(
    grammar_bytes: bytes,
) -> tuple[bytes, tuple[str, ...]]:
    carried, filled_kinds = fill_fidelity_occurrence_kinds(grammar_bytes)
    vocabulary = expected_book_vocabulary(carried)
    return _carry_vocabulary(carried, vocabulary), filled_kinds


def main() -> None:
    before = GRAMMAR.read_bytes()
    after, filled = fill_witness_grammar(before)
    if after != before:
        GRAMMAR.write_bytes(after)
    print(
        f"filled {len(filled)} Fidelity occurrence kinds and "
        f"{len(expected_book_vocabulary(after)['ordered_entries'])} Book vocabulary entries"
    )


if __name__ == "__main__":
    main()
