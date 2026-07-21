from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text()


def test_view_kind_depends_on_emitted_standing_not_input_artifact_alone():
    text = _read("book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md")

    assert "Input artifact kind and representation shape may supply evidence" in text
    assert "they do not automatically determine the View kind" in text
    assert "the standing of the assertion Seed is warranted to emit" in text
    assert "A View over Observation artifacts is not automatically an ObservationView" in text
    assert "FactSupport" in text and "not automatically a FactView" in text


def test_projection_chapter_distinguishes_current_implementation_from_true_fact_view():
    text = _read("book_of_seed/06-state-and-projection/projection-and-current-state.md")

    assert "A true FactView exposes a proposition with bounded Fact standing" in text
    assert "current implementation named `FactView` exposes projected normalized fact/support material" in text
    assert "PR 1890 was therefore correct" in text
    assert "overbroad if that phrase is treated as the constitutional definition" in text
    assert "A current-facing Fact View is a further standing-bearing emission" in text


def test_amendment_records_required_reliance_answers_and_surface_table():
    text = _read("book_of_seed/view_emission_warrant_and_reliance_amendment_001.md")

    assert "not independent constitutional authority" in text
    assert "Was PR 1890 correct to canonize `FactView`" in text
    assert "correct as implementation characterization" in text
    assert "not as the constitutional definition" in text
    assert "What standing does a true FactView warrant?" in text
    assert "What may an operator lawfully rely upon when presented with an `ObservationView`?" in text
    assert "occurrence and attribution of testimony" in text
    assert "What may an operator lawfully rely upon when presented with a `FactView`?" in text
    assert "| `ObservationView` |" in text
    assert "| `FactView` current implementation |" in text
    assert "| `FactSupport` |" in text
    assert "| current-fact getters |" in text
    assert "| evidence-facing Views |" in text
    assert "| explanation surfaces |" in text
    assert "| verification-facing Views |" in text


def test_unresolved_ledger_preserves_repair_question_not_answered_temporal_question():
    text = _read("book_of_seed/unresolved.md")

    assert "which temporal standings and relations govern Claim expression" not in text
    assert "Which current public and operator-facing View emissions fail" in text
    assert "amended warrant, reliance, and temporal disclosure contracts" in text
