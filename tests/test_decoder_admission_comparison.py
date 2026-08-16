"""Compare Admission results from distinct implementation functions."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import material_admission  # noqa: E402
from decoder_admission_comparison import (  # noqa: E402
    admissions,
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


def test_many_decoder_functions_reach_the_same_admission():
    found = admissions()
    sizes = sorted((len(names) for names in found.values()), reverse=True)

    assert sum(sizes) > 100
    assert len(found) < sum(sizes)
    assert sizes[0] >= 40


def test_the_decoder_functions_do_not_share_one_admission():
    """Most Admission pairs preserve neither direction."""

    counted = compare_admissions(admissions())

    assert counted["preservation_pairs"] * 4 < counted["pair_count"]
    assert counted["not_preserved_by_another"] > 20
    assert counted["preserves_no_other"] == 1


def test_the_relation_over_results_is_itself_admitted():
    found = admissions()
    keys = tuple(found)

    found_admissions = material_admission.admit(
        material_admission.admission_by(len, keys), preserves
    )

    assert len(found_admissions) > 1
    assert material_admission.admission_counts(found_admissions)[-1] == len(keys)
    assert material_admission.not_distinguished(found_admissions) == []


def test_one_admission_preserves_no_other():
    found = admissions()
    without_distinctions = [key for key in found if len(key) == 1]

    assert len(without_distinctions) == 1
    assert all(preserves(other, without_distinctions[0]) for other in found)


def test_repeated_comparison_uses_the_exact_prior_admission():
    first = admissions()

    assert admissions() is first
    assert final_admission("utf-8") is final_admission("utf-8")


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


FIDELITY_SUBJECTS = {
    "admission_preservation_relation": (
        test_an_admission_preserves_itself_and_the_one_without_distinctions,
    ),
    "material_function_admission_equivalence": (
        test_many_decoder_functions_reach_the_same_admission,
    ),
    "material_function_admission_distinction": (
        test_the_decoder_functions_do_not_share_one_admission,
    ),
    "admission_result_relation": (
        test_the_relation_over_results_is_itself_admitted,
    ),
    "admission_preservation_boundary": (test_one_admission_preserves_no_other,),
    "prior_admission_identity": (
        test_repeated_comparison_uses_the_exact_prior_admission,
    ),
    "ordered_admission_pair_comparison": (
        test_each_ordered_admission_pair_is_read_once,
    ),
}
