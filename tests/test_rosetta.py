import importlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "book_of_seed/grammar.json"
ROSETTA = ROOT / "rosetta"
ROSETTA_ROOTS = ROSETTA / "roots.md"
ROSETTA_LEXICON = ROSETTA / "admitted-lexicon.txt"


def _rosetta_admission() -> set[str]:
    return {
        line.split("#", 1)[0].strip()
        for line in ROSETTA_LEXICON.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def _rosetta_words(material: str) -> set[str]:
    without_links = re.sub(r"\]\([^)]*\)", "]()", material)
    scanned = re.sub(r"[_-]+", " ", without_links).lower()
    return set(re.findall(r"[A-Za-z]+", scanned))


def _unadmitted_rosetta_words(material: str) -> set[str]:
    return _rosetta_words(material) - _rosetta_admission()


def _relation_line(name: str, coordinates: dict[str, object]) -> str:
    source = str(coordinates["from"]).replace("_", " ")
    target = str(coordinates["to"]).replace("_", " ")
    relation = name.capitalize()
    if coordinate := coordinates.get("coordinate"):
        relation = f"{relation}({coordinate})"
    return f"{source} ── {relation}"


def _assert_rosetta_relation_order(grammar: dict, rosetta: str) -> None:
    for name, coordinates in grammar["relations"].items():
        line_start = _relation_line(name, coordinates)
        matching = [
            line.strip()
            for line in rosetta.splitlines()
            if line.strip().startswith(line_start)
        ]
        assert len(matching) == 1
        assert matching[0].endswith(
            f"→ {str(coordinates['to']).replace('_', ' ')}"
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


def test_rosetta_follows_machine_grammar_relation_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    rosetta = ROSETTA_ROOTS.read_text(encoding="utf-8")

    _assert_rosetta_relation_order(grammar, rosetta)


def test_rosetta_reversed_relation_is_detected():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    rosetta = ROSETTA_ROOTS.read_text(encoding="utf-8")
    altered = rosetta.replace(
        "Act occurrence ── Yield → result",
        "result ── Yield → Act occurrence",
        1,
    )

    try:
        _assert_rosetta_relation_order(grammar, altered)
    except AssertionError:
        pass
    else:
        raise AssertionError("a reversed Rosetta relation escaped comparison")


def test_rosetta_implementation_references_resolve():
    rosetta = ROSETTA_ROOTS.read_text(encoding="utf-8")
    references = _implementation_references(rosetta)

    assert references
    for reference in references:
        _assert_live_reference(reference)


def test_rosetta_missing_implementation_reference_is_detected():
    try:
        _assert_live_reference("seed_runtime.yield_evidence::_missing")
    except AssertionError:
        pass
    else:
        raise AssertionError("a missing Rosetta implementation reference escaped")


def test_rosetta_prose_has_lexical_admission():
    violations = {
        path.relative_to(ROOT).as_posix(): _unadmitted_rosetta_words(
            path.read_text(encoding="utf-8")
        )
        for path in sorted(ROSETTA.glob("*.md"))
    }
    violations = {path: words for path, words in violations.items() if words}

    assert violations == {}, "\n" + "\n".join(
        f"{path}: {', '.join(sorted(words))}"
        for path, words in violations.items()
    )


def test_rosetta_admission_detects_an_unadmitted_word_without_naming_it():
    assert _unadmitted_rosetta_words("unadmittedword") == {"unadmittedword"}
