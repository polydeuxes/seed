"""The first opaque interrogation of Python's compiled parser."""

from __future__ import annotations

import sys
from pathlib import Path
import shutil

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_parser_witness_harness import (  # noqa: E402
    COMPILED_PARSER_WITNESSES,
    first_probe_family,
    interrogate,
    interrogate_many,
    interrogate_across_compiled_parsers,
    interrogate_compiled_parser,
    one_byte_substitutions,
)


def test_the_first_family_preserves_only_exact_answers():
    outcomes = interrogate_many(first_probe_family())

    assert tuple(outcome.exact_material for outcome in outcomes) == (
        b"x",
        b"x=",
        b"x=1",
        b"x=1\n",
        b"def",
        b"def ",
        b"def x",
        b"def x(",
        b"def x():",
        b"def x():\n",
        b"def x():\n pass",
    )
    assert tuple(outcome.accepted for outcome in outcomes) == (
        True,
        False,
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
    )
    for outcome in outcomes:
        if outcome.accepted:
            assert type(outcome.result_material) is bytes
            assert outcome.result_material
            assert outcome.refusal_material is None
        else:
            assert outcome.result_material is None
            assert type(outcome.refusal_material) is bytes
            assert outcome.refusal_material


def test_the_same_exact_material_gets_the_same_exact_answer():
    first = interrogate(b"x=1\n")
    second = interrogate(b"x=1\n")

    assert first == second


def test_nearby_accepted_material_has_distinct_exact_returned_material():
    outcomes = interrogate_many((b"a", b"b", b"c"))

    assert all(outcome.accepted for outcome in outcomes)
    returned = [outcome.result_material for outcome in outcomes]
    assert len(set(returned)) == 3
    assert len({len(material) for material in returned if material is not None}) == 1


def test_one_byte_pressure_is_exact_complete_and_behaviorally_divided():
    source = b"x=1"
    candidates = one_byte_substitutions(source)
    outcomes = interrogate_many(candidates)

    assert len(candidates) == len(source) * 255
    assert len(set(candidates)) == len(candidates)
    assert all(
        len(candidate) == len(source)
        and sum(left != right for left, right in zip(candidate, source)) == 1
        for candidate in candidates
    )
    assert {outcome.accepted for outcome in outcomes} == {False, True}


def test_non_utf8_source_bytes_reach_the_witness_and_are_refused():
    outcome = interrogate(b"\xff")

    assert outcome.exact_material == b"\xff"
    assert outcome.accepted is False
    assert outcome.result_material is None
    assert type(outcome.refusal_material) is bytes
    assert outcome.refusal_material


def test_a_null_byte_is_also_a_refusal_outcome():
    outcome = interrogate(b"\x00")

    assert outcome.exact_material == b"\x00"
    assert outcome.accepted is False
    assert outcome.result_material is None
    assert type(outcome.refusal_material) is bytes
    assert outcome.refusal_material


def test_a_non_byte_input_is_refused_before_interrogation():
    with pytest.raises(TypeError, match="exact bytes"):
        interrogate("x")


def test_exact_bytes_reach_the_compiled_witness_without_prior_decoding(monkeypatch):
    import compiled_parser_witness_harness as harness

    supplied = []
    compiled = harness.ast.parse

    def record(material):
        supplied.append(material)
        return compiled(material)

    monkeypatch.setattr(harness.ast, "parse", record)
    outcome = harness.interrogate(b"x=1")

    assert outcome.accepted is True
    assert supplied == [b"x=1"]


@pytest.mark.skipif(
    any(shutil.which(witness.arguments[0]) is None for witness in COMPILED_PARSER_WITNESSES),
    reason="one compiled parser witness is unavailable",
)
def test_distinct_compiled_parsers_receive_the_same_exact_material():
    material = b"x=1\n"

    answers = tuple(
        interrogate_compiled_parser(material, witness)
        for witness in COMPILED_PARSER_WITNESSES
    )

    assert len({answer.witness for answer in answers}) == 4
    assert all(answer.exact_material == material for answer in answers)
    assert all(type(answer.stdout_bytes) is bytes for answer in answers)
    assert all(type(answer.stderr_bytes) is bytes for answer in answers)


@pytest.mark.skipif(
    any(shutil.which(witness.arguments[0]) is None for witness in COMPILED_PARSER_WITNESSES),
    reason="one compiled parser witness is unavailable",
)
def test_cross_parser_answers_preserve_agreement_and_disagreement():
    materials = first_probe_family()
    rows = interrogate_across_compiled_parsers(materials)
    acceptance = tuple(tuple(answer.accepted for answer in row) for row in rows)

    assert len(rows) == 4
    assert all(tuple(answer.exact_material for answer in row) == materials for row in rows)
    columns = tuple(zip(*acceptance))
    assert any(len(set(column)) == 1 for column in columns)
    assert any(len(set(column)) > 1 for column in columns)
