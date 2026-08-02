from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md"


def _clause() -> str:
    text = BOOK.read_text(encoding="utf-8")
    return text.split("### 01.Standing.E.1", 1)[1].split("### 01.Standing.F", 1)[0]


def test_book_preserves_rebuttable_input_applicability_owner():
    clause = _clause()

    assert "responsibility assigned to perform an exact constitutional act" in clause
    assert "responsible for ensuring that applicability is determined for every proposed input" in clause
    assert "before that input participates in, is consumed by, or is relied upon" in clause
    assert "Unless the Book explicitly assigns otherwise" in clause
    assert "explicit Book assignment therefore overrides the ordinary owner" in clause
    assert "assigned responsible occurrence for that exact downstream act" in clause


def test_book_distinguishes_input_exclusion_from_whole_act_nonperformance():
    clause = _clause()

    assert "upstream applicability is not downstream admission" in clause
    assert "admission remains required only where its exact local road requires it" in clause
    assert "It does not by itself establish admission" in clause
    assert "may not participate in, be consumed by, or be relied upon in that act" in clause
    assert "no act result may claim reliance on, support from, consumption of, or participation by the excluded input" in clause
    assert "Exclusion of one proposed input does not by itself establish whether the exact act is performed or not performed" in clause
    assert "That determination remains with the responsibility assigned to perform the exact act" in clause
    assert "under the conditions, relations, evidence, authority, scope, and other boundaries assigned to that responsibility" in clause


def test_book_preserves_required_input_and_alternative_input_boundary():
    clause = _clause()

    assert "An alternative proposed input does not participate by virtue of availability, similarity, equal proposition text or content" in clause
    assert "the act-owning responsibility must determine or consume applicability standing for that exact input-to-act relation" in clause
    assert "whatever standing, warrant, admission, authority, scope, provenance, or other relation that exact proposed use requires" in clause
    assert "Required coordinates are local to the exact act and proposed use" in clause
    assert "no coordinate is universally required merely because a subject is proposed as an input" in clause
    assert "No unassigned input-set sufficiency, substitution, readiness, or act-permission standing is created" in clause
    assert "One rejected candidate is not all candidates rejected" in clause


def test_book_preserves_composite_occurrence_as_independent_claims():
    clause = _clause()

    assert "One bounded responsible occurrence may determine applicability for proposed inputs" in clause
    assert "perform or not perform the exact act within the act-owning responsibility's assigned boundaries" in clause
    assert "These remain independently recoverable claims" in clause
    assert "applicability success is not act performance" in clause
    assert "one input excluded is neither act prohibited nor act permitted" in clause
    assert "act performance is not output standing" in clause
    assert "output standing is not downstream applicability" in clause


def test_book_does_not_turn_persistent_standing_into_production_demand():
    clause = _clause()

    assert "lawfully persistent result standing is not current production demand" in clause
    assert "does not lose its standing merely because a later consumer does not consume it" in clause
    assert "does not permit a producer to be implemented or invoked without a current responsibility" in clause
    assert "does not by itself establish producer demand, candidate-formation demand" in clause
