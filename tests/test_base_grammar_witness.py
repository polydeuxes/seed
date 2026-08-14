"""What separates the three structural edges, and what does not.

`grammar.json` declares three. Their stated requirements are identical, so
anything reading only those cannot tell them apart. What differs is where each
runs from and to, and that is sparse.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import refinement_climb as rc  # noqa: E402
from base_grammar_witness import (  # noqa: E402
    compositions,
    edges,
    endpoints,
    links,
    shared_requirements,
)


def test_the_three_edges_state_identical_requirements():
    """So requirements cannot be what tells one from another."""

    declared = edges()

    assert len(declared) == 3
    assert shared_requirements(declared)
    assert {tuple(spec["requires"]) for spec in declared.values()} == {
        ("exact_relation", "occurrence_witness", "intact_evidence")
    }


def test_the_endpoint_space_is_almost_empty():
    declared = edges()
    ends = endpoints(declared)

    assert len(ends) == 5
    assert len(links(declared)) == 3
    assert len(links(declared)) * 8 < len(ends) ** 2


def test_exactly_one_pair_of_edges_composes():
    declared = edges()
    found = compositions(declared)

    assert found == [("participation", "yield")]
    assert declared["participation"]["to"] == declared["yield"]["from"] == "Act_occurrence"


def test_carriage_reaches_a_place_no_edge_leaves():
    """It ends at `occurrence`; every edge begins somewhere else.

    The Book's prose reads an Act occurrence as one kind of occurrence, and
    holds `act occurrence` apart from `recording occurrence`. `grammar.json`
    states no relation between the two names, so nothing reading it can join
    what the prose joins.
    """

    declared = edges()

    assert declared["carriage"]["to"] == "occurrence"
    assert not [
        name for name, spec in declared.items() if spec["from"] == "occurrence"
    ]
    assert "Act_occurrence" in endpoints(declared)
    assert "occurrence" != "Act_occurrence"


def test_composition_separates_none_of_the_edges():
    """A witness that answers False for nearly every pair separates nothing."""

    declared = edges()
    rungs = rc.climb(
        rc.one_class(sorted(declared)),
        lambda a, b: declared[a]["to"] == declared[b]["from"],
    )

    assert rc.heights(rungs) == [1]


def test_linkage_separates_every_endpoint():
    """The structure such as it is lives in the endpoints."""

    declared = edges()
    ends = endpoints(declared)
    rungs = rc.climb(
        rc.one_class(ends),
        lambda x, y: any(
            spec["from"] == x and spec["to"] == y for spec in declared.values()
        ),
    )

    assert rc.heights(rungs)[-1] == len(ends)
    assert rc.unseparated(rungs) == []
