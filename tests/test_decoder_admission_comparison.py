"""Compare Admission results from distinct implementation functions."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import material_admission  # noqa: E402
from decoder_admission_comparison import (  # noqa: E402
    compare_admissions,
    final_admission,
)
from material_admission import preserves  # noqa: E402


def test_an_admission_preserves_itself_and_the_one_without_distinctions():
    fine = final_admission("utf-8")
    everything = frozenset({frozenset(range(256))})

    assert preserves(fine, fine)
    assert preserves(fine, everything)
    assert not preserves(everything, fine)


def test_one_admission_preserves_no_other():
    without_distinctions = frozenset({frozenset(range(256))})
    divided = frozenset({frozenset(range(128)), frozenset(range(128, 256))})

    assert preserves(divided, without_distinctions)
    assert not preserves(without_distinctions, divided)


def test_each_ordered_admission_pair_is_read_once(monkeypatch):
    found = {
        frozenset({frozenset({0, 1, 2})}): ["compiled-0"],
        frozenset({frozenset({0, 1}), frozenset({2})}): ["compiled-1"],
        frozenset({frozenset({0}), frozenset({1}), frozenset({2})}): [
            "compiled-2"
        ],
    }
    calls = []
    exact = material_admission.preserves

    def measured(first, second):
        calls.append((first, second))
        return exact(first, second)

    monkeypatch.setattr(material_admission, "preserves", measured)

    compare_admissions(found)

    assert len(calls) == 6
    assert len(set(calls)) == 6
