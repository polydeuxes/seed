from pathlib import Path


BOOK = (
    Path(__file__).resolve().parents[1]
    / "book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md"
)


def _assertion_clause() -> str:
    text = BOOK.read_text()
    return text.split(
        "### 01.Standing.D.1 — An Assertion owns fidelity of its Standing", 1
    )[1].split("### 01.Standing.E", 1)[0]


def test_assertion_owns_only_fidelity_of_its_standing():
    clause = _assertion_clause()
    assert "exact asserted content as its own subject" in clause
    assert "owns the Responsibility for fidelity of its Standing" in clause
    assert "Producer != Assertion owner" in clause
    assert "producing Act != Assertion Responsibility" in clause


def test_assertion_ownership_creates_no_automatic_movement():
    clause = _assertion_clause()
    assert "does not require another Act merely because it exists" in clause
    assert "does not automatically revise its content or Standing" in clause
    assert "an **Unknown** does not create a demand to eliminate it" in clause
    assert "not an inferred constitutional Stop" in clause
