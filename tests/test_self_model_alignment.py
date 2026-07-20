from __future__ import annotations

from seed_runtime.knowledge.self_model_alignment import (
    DocumentationClaim,
    RepositoryArtifactFact,
    reconcile_claims,
)


def _claim(claim: str, family: str) -> DocumentationClaim:
    return DocumentationClaim(
        claim=claim,
        claim_family=family,
        source_path="docs/fixture.md",
    )


def _fact(
    fact: str,
    artifact_kind: str = "module_defines_class",
    path: str = "seed_runtime/fixture.py",
    symbol: str | None = None,
) -> RepositoryArtifactFact:
    return RepositoryArtifactFact(
        fact=fact,
        artifact_kind=artifact_kind,
        path=path,
        symbol=symbol,
    )


def _single_outcome(
    claim: DocumentationClaim, facts: list[RepositoryArtifactFact]
) -> str:
    return reconcile_claims([claim], facts)[0].outcome


def test_projection_store_ownership_with_projection_store_artifact_is_supported():
    claim = _claim("ProjectionStore owns cached projected state.", "ownership")
    facts = [_fact("ProjectionStore class exists.", symbol="ProjectionStore")]

    assert _single_outcome(claim, facts) == "supported"


def test_projection_store_ownership_without_matching_artifact_is_missing_support():
    claim = _claim("ProjectionStore owns cached projected state.", "ownership")
    facts = [_fact("Runtime class exists.", symbol="Runtime")]

    assert _single_outcome(claim, facts) == "missing_support"


def test_component_ownership_with_matching_artifact_is_supported():
    claim = _claim("ProjectionStore owns cached projected-state snapshots.", "ownership")
    facts = [_fact("ExampleComponent class exists.", symbol="ProjectionStore")]

    assert _single_outcome(claim, facts) == "supported"


def test_response_engine_rejected_without_response_engine_artifact_is_supported():
    claim = _claim("ResponseEngine is rejected.", "rejected_concept")
    facts = [_fact("Runtime class exists.", symbol="Runtime")]

    assert _single_outcome(claim, facts) == "supported"


def test_response_engine_rejected_with_response_engine_artifact_is_potential_conflict():
    claim = _claim("ResponseEngine is rejected.", "rejected_concept")
    facts = [_fact("ResponseEngine class exists.", symbol="ResponseEngine")]

    assert _single_outcome(claim, facts) == "potential_conflict"


def test_users_observation_frontier_without_users_observation_artifact_is_supported():
    claim = _claim("Users Observation is a current frontier.", "frontier")
    facts = [_fact("Repository Observation class exists.", symbol="RepositoryObservation")]

    assert _single_outcome(claim, facts) == "supported"


def test_users_observation_frontier_with_users_observation_artifact_is_potential_conflict():
    claim = _claim("Users Observation is a current frontier.", "frontier")
    facts = [
        _fact(
            "UsersObservation class exists.",
            path="seed_runtime/users_observation.py",
            symbol="UsersObservation",
        )
    ]

    assert _single_outcome(claim, facts) == "potential_conflict"


def test_unrelated_status_philosophy_claim_is_not_evaluable():
    claim = _claim("Seed should preserve architectural humility.", "philosophy")
    facts = [_fact("Runtime class exists.", symbol="Runtime")]

    assert _single_outcome(claim, facts) == "not_evaluable"
