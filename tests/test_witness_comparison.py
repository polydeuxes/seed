"""Compare Admission results from distinct implementation functions."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import material_admission  # noqa: E402
from witness_comparison_harness import (  # noqa: E402
    admissions,
    compare_admissions,
    final_admission,
    preserves,
)


def test_an_admission_preserves_itself_and_the_one_without_distinctions():
    fine = final_admission("utf-8")
    everything = frozenset({frozenset(range(256))})

    assert preserves(fine, fine)
    assert preserves(fine, everything)
    assert not preserves(everything, fine)


def test_many_witnesses_reach_the_same_resting_admission():
    found = admissions()
    sizes = sorted((len(names) for names in found.values()), reverse=True)

    assert sum(sizes) > 100
    assert len(found) < sum(sizes)
    assert sizes[0] >= 40


def test_the_witnesses_do_not_converge():
    """Most Admission pairs preserve neither direction."""

    counted = compare_admissions(admissions())

    assert counted["preservation_pairs"] * 4 < counted["pair_count"]
    assert counted["not_preserved_by_another"] > 20
    assert counted["preserves_no_other"] == 1


def test_the_relation_over_results_is_itself_admitted():
    found = admissions()
    keys = sorted(found, key=len)

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
