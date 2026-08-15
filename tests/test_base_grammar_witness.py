"""What separates the declared relations, and what does not.

Their stated requirements are identical, so
anything read only those cannot tell them apart. What differs is where each
runs from and to, and that is sparse.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import refinement_climb as rc  # noqa: E402
from base_grammar_witness import (  # noqa: E402
    compositions,
    relations,
    endpoints,
    links,
    shared_requirements,
)


def test_the_relations_state_identical_requirements():
    """So requirements cannot be what tells one from another."""

    declared = relations()

    assert set(declared) == {"locality", "participation", "yield", "locality"}
    assert shared_requirements(declared)
    assert {tuple(spec["requires"]) for spec in declared.values()} == {
        ("exact_relation", "occurrence_witness", "intact_evidence")
    }


def test_the_endpoint_space_is_almost_empty():
    declared = relations()
    ends = endpoints(declared)

    assert len(ends) == 5
    assert len(links(declared)) == 3
    assert len(links(declared)) * 8 < len(ends) ** 2


def test_exactly_one_pair_of_relations_composes():
    declared = relations()
    found = compositions(declared)

    assert found == [("participation", "yield")]
    assert declared["participation"]["to"] == declared["yield"]["from"] == "Act_occurrence"


def test_locality_keeps_its_subject_kinds_open():
    """Content-to-Event locality does not bound every Locality endpoint kind."""

    declared = relations()

    assert declared["locality"]["from"] == "first_subject"
    assert declared["locality"]["to"] == "second_subject"
    assert "Act_occurrence" in endpoints(declared)


def test_composition_separates_every_relation():
    declared = relations()
    rungs = rc.climb(
        rc.one_class(sorted(declared)),
        lambda a, b: declared[a]["to"] == declared[b]["from"],
    )

    assert rc.heights(rungs) == [1, 3]
    assert rc.unseparated(rungs) == []


def test_linkage_separates_every_endpoint():
    """The distinctions live in the endpoints."""

    declared = relations()
    ends = endpoints(declared)
    rungs = rc.climb(
        rc.one_class(ends),
        lambda x, y: any(
            spec["from"] == x and spec["to"] == y for spec in declared.values()
        ),
    )

    assert rc.heights(rungs)[-1] == len(ends)
    assert rc.unseparated(rungs) == []
