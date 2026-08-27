import importlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "book_of_seed/witness_grammar.json"
ROSETTA = ROOT / "rosetta"
ROSETTA_STANDING_RESPONSIBILITY = ROSETTA / "standing_and_responsibility.md"
ROSETTA_ADMISSION = ROSETTA / "rosetta_admission.txt"


def _rosetta_admission() -> set[str]:
    return {
        line.split("#", 1)[0].strip()
        for line in ROSETTA_ADMISSION.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def _rosetta_words(material: str) -> set[str]:
    without_links = re.sub(r"\]\([^)]*\)", "]()", material)
    scanned = re.sub(r"[_-]+", " ", without_links).lower()
    return set(re.findall(r"[A-Za-z]+", scanned))


def _rosetta_proper_words() -> dict[str, list[tuple[str, int]]]:
    found: dict[str, list[tuple[str, int]]] = {}
    for path in sorted(ROSETTA.glob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(
            path.read_text(encoding="utf-8").split("\n"), start=1
        ):
            for word in _rosetta_words(line):
                found.setdefault(word, []).append((relative, number))
    return found


def _unadmitted_rosetta_words(material: str) -> set[str]:
    return _rosetta_words(material) - _rosetta_admission()


def _relation_coordinate_identity(coordinate: object) -> str:
    if type(coordinate) is str and coordinate:
        return coordinate
    if type(coordinate) is dict:
        identity = coordinate.get("identity")
        if type(identity) is str and identity:
            return identity
    raise TypeError("one exact relation-coordinate identity is required")


def _relation_line(name: str, coordinates: dict[str, object]) -> str:
    source = _relation_coordinate_identity(coordinates["first_subject"]).replace(
        "_", " "
    )
    relation = name.capitalize()
    return f"{source} ── {relation}"


def _exact_relation_coordinates(grammar: dict) -> dict[str, dict[str, object]]:
    coordinates = grammar["book_coordinates"]
    return {
        "yield": coordinates["02.Acts.A"]["Yield"],
        "locality": coordinates["06.Locality.A"]["Locality"],
    }


def _assert_rosetta_relation_order(grammar: dict, rosetta: str) -> None:
    for name, coordinates in _exact_relation_coordinates(grammar).items():
        line_start = _relation_line(name, coordinates)
        matching = [
            line.strip()
            for line in rosetta.splitlines()
            if line.strip().startswith(line_start)
        ]
        assert len(matching) == 1
        assert matching[0].endswith(
            "→ "
            + _relation_coordinate_identity(coordinates["second_subject"]).replace(
                "_", " "
            )
        )


def _implementation_references(rosetta: str) -> tuple[str, ...]:
    return tuple(
        match.group(1)
        for line in rosetta.splitlines()
        if (match := re.fullmatch(r"\s+(seed_runtime\.[\w.]+::\w+)", line))
    )


def _assert_live_reference(reference: str) -> None:
    module_name, symbol = reference.split("::", 1)
    module = importlib.import_module(module_name)
    assert hasattr(module, symbol), reference


def test_rosetta_follows_witness_grammar_relation_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")

    _assert_rosetta_relation_order(grammar, rosetta)


def test_rosetta_reversed_relation_is_detected():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")
    altered = rosetta.replace(
        "exact Act occurrence ── Yield → exact result",
        "exact result ── Yield → exact Act occurrence",
        1,
    )

    try:
        _assert_rosetta_relation_order(grammar, altered)
    except AssertionError:
        pass
    else:
        raise AssertionError("a reversed Rosetta relation escaped comparison")


def test_rosetta_implementation_references_resolve():
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")
    references = _implementation_references(rosetta)

    assert references
    for reference in references:
        _assert_live_reference(reference)


def test_rosetta_participant_decompresses_to_act_occurrence_coordinates():
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")

    assert "participant" in _rosetta_admission()
    assert (
        "Participant    subject carried by one exact Act occurrence under one "
        "role; not Candidate by identity"
    ) in rosetta


def test_rosetta_role_decompresses_to_exact_structural_positions():
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")

    assert {"role", "roles"} <= _rosetta_admission()
    assert (
        "Role / roles   ordinary shorthand for exact subject position "
        "coordinates; the words establish no additional coordinate, identity, "
        "object, or occurrence"
    ) in rosetta


def test_rosetta_unknown_decompresses_to_open_world_absence():
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")

    assert "unknown" in _rosetta_admission()
    assert (
        "Unknown        ordinary shorthand for no exact positive or negative "
        "result established through one exact boundary; absence is not false, "
        "and the word establishes no additional coordinate, identity, object, "
        "occurrence, or result"
    ) in rosetta


def test_rosetta_conflict_decompresses_to_exact_results_and_findings():
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")

    assert "conflict" in _rosetta_admission()
    assert (
        "Conflict       ordinary shorthand for an exact Compare finding whose "
        "exact subject carries different earlier and later contents; current "
        "Seed establishes no conflicting Applicability result, absence of "
        "agreement establishes no conflict by identity, and the word "
        "establishes no additional collection or object"
    ) in rosetta


def test_rosetta_book_decompresses_to_language_clauses_and_lexicon():
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")

    assert {"book", "language", "lexicon"} <= _rosetta_admission()
    assert (
        "Book           this constitutional language + ordered clause "
        "coordinates + this Book's admitted lexicon; Book != lexicon by identity"
    ) in rosetta


def test_rosetta_admission_does_not_establish_a_clause():
    rosetta = ROSETTA_STANDING_RESPONSIBILITY.read_text(encoding="utf-8")

    assert (
        "Lexicon        admitted words only; admission of a word establishes "
        "no clause, coordinate, relation, or currentness"
    ) in rosetta


def test_rosetta_missing_implementation_reference_is_detected():
    try:
        _assert_live_reference("seed_runtime.yield_relation::_missing")
    except AssertionError:
        pass
    else:
        raise AssertionError("a missing Rosetta implementation reference escaped")


def test_rosetta_proper_is_within_rosetta_admission():
    unadmitted = {
        word: places
        for word, places in _rosetta_proper_words().items()
        if word not in _rosetta_admission()
    }
    report = "\n".join(
        f"  {word} -- {places[0][0]}:{places[0][1]}"
        + (f" and {len(places) - 1} more" if len(places) > 1 else "")
        for word, places in sorted(unadmitted.items())
    )
    assert not unadmitted, (
        "\nRosetta proper carries words absent from Rosetta admission:\n"
        + report
    )


def test_rosetta_admission_carries_no_unused_words():
    unused = sorted(_rosetta_admission() - set(_rosetta_proper_words()))
    assert not unused, (
        "\nRosetta admission carries words absent from Rosetta proper: "
        + ", ".join(unused)
    )


def test_rosetta_admission_detects_an_unadmitted_word_without_naming_it():
    assert _unadmitted_rosetta_words("unadmittedword") == {"unadmittedword"}
