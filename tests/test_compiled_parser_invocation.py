"""Exact invocation occurrences."""

from __future__ import annotations

import sys
from pathlib import Path
import shutil

import pytest




ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_parser_invocation import (  # noqa: E402
    COMPILED_PARSER_FUNCTIONS,
    python_parser_invocation,
    python_parser_invocations,
    compiled_parser_invocations,
    compiled_parser_invocation,
    one_byte_substitutions,
)
def test_equal_material_keeps_distinct_invocation_occurrences():
    first = python_parser_invocation(
        b"x=1\n", boundary_identity="equal-material", invocation_position=0
    )
    second = python_parser_invocation(
        b"x=1\n", boundary_identity="equal-material", invocation_position=1
    )

    assert first.exact_material == second.exact_material
    assert first.returned == second.returned
    assert first.result_material == second.result_material
    assert first.occurrence_identity != second.occurrence_identity


def test_nearby_accepted_material_has_distinct_exact_returned_material():
    results = python_parser_invocations(
        (b"a", b"b", b"c"), boundary_identity="distinct-material"
    )

    assert all(result.returned for result in results)
    returned = [result.result_material for result in results]
    assert len(set(returned)) == 3
    assert len({len(material) for material in returned if material is not None}) == 1


def test_one_byte_pressure_is_exact_complete_and_behaviorally_divided():
    source = b"x=1"
    candidates = one_byte_substitutions(source)
    results = python_parser_invocations(
        candidates, boundary_identity="one-byte-substitutions"
    )

    assert len(candidates) == len(source) * 255
    assert len(set(candidates)) == len(candidates)
    assert all(
        len(candidate) == len(source)
        and sum(left != right for left, right in zip(candidate, source)) == 1
        for candidate in candidates
    )
    assert {result.returned for result in results} == {False, True}


def test_non_utf8_source_bytes_reach_the_compiled_function_and_are_refused():
    result = python_parser_invocation(b"\xff", boundary_identity="non-utf8")

    assert result.exact_material == b"\xff"
    assert result.returned is False
    assert result.result_material is None
    assert type(result.refusal_material) is bytes
    assert result.refusal_material


def test_a_null_byte_is_also_a_refusal_result():
    result = python_parser_invocation(b"\x00", boundary_identity="null-byte")

    assert result.exact_material == b"\x00"
    assert result.returned is False
    assert result.result_material is None
    assert type(result.refusal_material) is bytes
    assert result.refusal_material


def test_a_non_byte_input_is_refused_before_invocation():
    with pytest.raises(TypeError, match="exact bytes"):
        python_parser_invocation("x", boundary_identity="non-byte")


def test_exact_bytes_reach_the_compiled_function_without_prior_decoding(monkeypatch):
    import compiled_parser_invocation as compiled_parser

    supplied = []
    compiled = compiled_parser.ast.parse

    def record(material):
        supplied.append(material)
        return compiled(material)

    monkeypatch.setattr(compiled_parser.ast, "parse", record)
    result = compiled_parser.python_parser_invocation(
        b"x=1", boundary_identity="exact-bytes"
    )

    assert result.returned is True
    assert supplied == [b"x=1"]


@pytest.mark.skipif(
    any(
        shutil.which(function.arguments[0]) is None
        for function in COMPILED_PARSER_FUNCTIONS
    ),
    reason="one compiled parser function is unavailable",
)
def test_distinct_compiled_parser_functions_receive_the_same_exact_material():
    material = b"x=1\n"

    results = tuple(
        compiled_parser_invocation(
            material,
            function,
            boundary_identity="distinct-functions",
        )
        for function in COMPILED_PARSER_FUNCTIONS
    )

    assert len({result.implementation_function_identity for result in results}) == 4
    assert len({result.occurrence_identity for result in results}) == 4
    assert all(result.exact_material == material for result in results)
    assert all(type(result.stdout_bytes) is bytes for result in results)
    assert all(type(result.stderr_bytes) is bytes for result in results)


@pytest.mark.skipif(
    any(
        shutil.which(function.arguments[0]) is None
        for function in COMPILED_PARSER_FUNCTIONS
    ),
    reason="one compiled parser function is unavailable",
)
def test_cross_parser_results_preserve_agreement_and_disagreement():
    materials = (b"", b"\x00", b"1", b"a", b"\xff")
    rows = compiled_parser_invocations(
        materials, boundary_identity="cross-parser-results"
    )
    returned = tuple(tuple(result.returned for result in row) for row in rows)

    assert len(rows) == 4
    assert all(tuple(result.exact_material for result in row) == materials for row in rows)
    assert all(len({result.occurrence_identity for result in row}) == len(materials) for row in rows)
    columns = tuple(zip(*returned))
    assert any(len(set(column)) == 1 for column in columns)
    assert any(len(set(column)) > 1 for column in columns)
