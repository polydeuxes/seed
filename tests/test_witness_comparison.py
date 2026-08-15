"""What comparing witnesses establishes, and what it shows they do not do.

Each decoding witness yields a material Locality over the same 256 bytes, so their results compare
without translation. The refinement relation between two of those results is
itself a relation the same climb rides, and its material is the earlier
climb's outputs.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import refinement_climb as rc  # noqa: E402
from witness_comparison_harness import (  # noqa: E402
    final_material_locality,
    order,
    material_localities,
    refines,
)


def test_a_material_locality_refines_itself_and_the_one_holding_everything():
    fine = final_material_locality("utf-8")
    everything = frozenset({frozenset(range(256))})

    assert refines(fine, fine)
    assert refines(fine, everything)
    assert not refines(everything, fine)


def test_many_witnesses_reach_the_same_resting_material_locality():
    found = material_localities()
    sizes = sorted((len(names) for names in found.values()), reverse=True)

    assert sum(sizes) > 100
    assert len(found) < sum(sizes)
    assert sizes[0] >= 40


def test_the_witnesses_do_not_converge():
    """Most pairs are incomparable: they cut the material differently.

    Not one finer than another. If witnesses were approaching some finest
    material Locality, comparable pairs would dominate; they are 7%.
    """

    counted = order(material_localities())

    assert counted["comparable"] * 4 < counted["pairs"]
    assert counted["finest"] > 20
    assert counted["coarsest"] == 1


def test_the_relation_over_results_is_itself_climbable():
    """Third level: material is the second level's outputs."""

    found = material_localities()
    keys = sorted(found, key=len)

    localities = rc.climb(rc.by(len, keys), refines)

    assert len(localities) > 1
    assert rc.heights(localities)[-1] == len(keys)
    assert rc.unseparated(localities) == []


def test_the_coarsest_is_the_one_that_separates_nothing():
    found = material_localities()
    coarsest = [key for key in found if len(key) == 1]

    assert len(coarsest) == 1
    assert all(refines(other, coarsest[0]) for other in found)
