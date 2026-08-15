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


def test_the_first_family_preserves_only_exact_results():
    results = interrogate_many(first_probe_family())

    assert tuple(result.exact_material for result in results) == (
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
    assert tuple(result.accepted for result in results) == (
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
    for result in results:
        if result.accepted:
            assert type(result.result_material) is bytes
            assert result.result_material
            assert result.refusal_material is None
        else:
            assert result.result_material is None
            assert type(result.refusal_material) is bytes
            assert result.refusal_material


def test_the_same_exact_material_gets_the_same_exact_result():
    first = interrogate(b"x=1\n")
    second = interrogate(b"x=1\n")

    assert first == second


def test_nearby_accepted_material_has_distinct_exact_returned_material():
    results = interrogate_many((b"a", b"b", b"c"))

    assert all(result.accepted for result in results)
    returned = [result.result_material for result in results]
    assert len(set(returned)) == 3
    assert len({len(material) for material in returned if material is not None}) == 1


def test_one_byte_pressure_is_exact_complete_and_behaviorally_divided():
    source = b"x=1"
    candidates = one_byte_substitutions(source)
    results = interrogate_many(candidates)

    assert len(candidates) == len(source) * 255
    assert len(set(candidates)) == len(candidates)
    assert all(
        len(candidate) == len(source)
        and sum(left != right for left, right in zip(candidate, source)) == 1
        for candidate in candidates
    )
    assert {result.accepted for result in results} == {False, True}


def test_non_utf8_source_bytes_reach_the_witness_and_are_refused():
    result = interrogate(b"\xff")

    assert result.exact_material == b"\xff"
    assert result.accepted is False
    assert result.result_material is None
    assert type(result.refusal_material) is bytes
    assert result.refusal_material


def test_a_null_byte_is_also_a_refusal_result():
    result = interrogate(b"\x00")

    assert result.exact_material == b"\x00"
    assert result.accepted is False
    assert result.result_material is None
    assert type(result.refusal_material) is bytes
    assert result.refusal_material


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
    result = harness.interrogate(b"x=1")

    assert result.accepted is True
    assert supplied == [b"x=1"]


@pytest.mark.skipif(
    any(shutil.which(witness.arguments[0]) is None for witness in COMPILED_PARSER_WITNESSES),
    reason="one compiled parser witness is unavailable",
)
def test_distinct_compiled_parsers_receive_the_same_exact_material():
    material = b"x=1\n"

    results = tuple(
        interrogate_compiled_parser(material, witness)
        for witness in COMPILED_PARSER_WITNESSES
    )

    assert len({result.witness for result in results}) == 4
    assert all(result.exact_material == material for result in results)
    assert all(type(result.stdout_bytes) is bytes for result in results)
    assert all(type(result.stderr_bytes) is bytes for result in results)


@pytest.mark.skipif(
    any(shutil.which(witness.arguments[0]) is None for witness in COMPILED_PARSER_WITNESSES),
    reason="one compiled parser witness is unavailable",
)
def test_cross_parser_results_preserve_agreement_and_disagreement():
    materials = first_probe_family()
    rows = interrogate_across_compiled_parsers(materials)
    acceptance = tuple(tuple(result.accepted for result in row) for row in rows)

    assert len(rows) == 4
    assert all(tuple(result.exact_material for result in row) == materials for row in rows)
    columns = tuple(zip(*acceptance))
    assert any(len(set(column)) == 1 for column in columns)
    assert any(len(set(column)) > 1 for column in columns)
