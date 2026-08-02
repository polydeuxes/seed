from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md"


def _clause() -> str:
    text = BOOK.read_text(encoding="utf-8")
    return text.split("### 01.Standing.E.1", 1)[1].split("### 01.Standing.F", 1)[0]


def test_exact_act_owner_is_rebuttable_default_applicability_owner():
    clause = _clause()

    assert "responsibility assigned to perform an exact constitutional act" in clause
    assert "responsible for ensuring that every proposed input is applicable" in clause
    assert "Unless the Book explicitly assigns otherwise" in clause
    assert "explicit Book assignment therefore overrides the ordinary owner" in clause
    assert "assigned responsible occurrence for that exact downstream act" in clause


def test_applicability_does_not_collapse_admission_or_performance():
    clause = _clause()

    assert "upstream applicability is not downstream admission" in clause
    assert "admission remains required only where its exact local road requires it" in clause
    assert "It does not by itself establish admission" in clause
    assert "Inapplicable**, **conflicting**, or **Unknown** does not permit a supported downstream act result" in clause
    assert "no supported or unsupported act result is fabricated" in clause


def test_composite_occurrence_preserves_independent_claims():
    clause = _clause()

    assert "One bounded responsible occurrence may determine input applicability" in clause
    assert "These remain independently recoverable claims" in clause
    assert "applicability success is not act success" in clause
    assert "act success is not output standing" in clause
    assert "output standing is not downstream applicability" in clause


def test_persistent_standing_does_not_create_production_demand():
    clause = _clause()

    assert "lawfully persistent result standing create current production demand" in clause
    assert "no current candidate-formation demand is established" in clause
    assert "does not establish a producer, proposed input, responsible occurrence, Demand" in clause
