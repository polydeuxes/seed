from dataclasses import replace

from seed_runtime.bounded_constitutional_question import produce_bounded_constitutional_question
from seed_runtime.constitutional_view_selection import (
    ConstitutionalCapabilityProjection,
    project_constitutional_capabilities,
    project_constitutional_question,
    select_constitutional_views,
)
from seed_runtime.read_model_ownership import (
    CONSTITUTIONAL_READ_MODEL_CONTRACTS,
    constitutional_read_model_registration,
)


def test_projects_real_registered_constitutional_capability_sources():
    projections = project_constitutional_capabilities()

    assert [p.registered_view_name for p in projections] == [
        "constitutional_process",
        "constitutional_governance",
        "constitutional_fidelity",
    ]
    assert [p.capability_keys for p in projections] == [
        ("process",),
        ("governance",),
        ("fidelity",),
    ]
    assert all(p.compatibility_answer == "No." for p in projections)
    assert all(p.read_only for p in projections)
    assert not any(p.writes_event_ledger for p in projections)
    assert not any(p.mutates_cluster for p in projections)


def test_equivalent_sources_and_duplicate_contracts_are_deterministic():
    contracts = CONSTITUTIONAL_READ_MODEL_CONTRACTS + (
        CONSTITUTIONAL_READ_MODEL_CONTRACTS[0],
    )
    registrations = tuple(
        constitutional_read_model_registration(contract) for contract in contracts
    )

    first = project_constitutional_capabilities(contracts, registrations)
    second = project_constitutional_capabilities(tuple(reversed(contracts)), tuple(reversed(registrations)))

    assert first == project_constitutional_capabilities()
    assert second == (
        ConstitutionalCapabilityProjection("constitutional_process", ("process",)),
        ConstitutionalCapabilityProjection("constitutional_fidelity", ("fidelity",)),
        ConstitutionalCapabilityProjection("constitutional_governance", ("governance",)),
    )
    assert len(first) == 3


def test_projection_does_not_infer_from_display_names_or_missing_evidence():
    contract = replace(
        CONSTITUTIONAL_READ_MODEL_CONTRACTS[0],
        name="constitutional_display_only",
        cli_flag="--display-only",
    )
    registration = constitutional_read_model_registration(contract)

    projections = project_constitutional_capabilities(
        (contract,),
        (registration,),
        view_builders={},
    )

    assert projections == (
        ConstitutionalCapabilityProjection(
            registered_view_name="constitutional_display_only",
            capability_keys=(),
            compatibility_answer="Unknown.",
        ),
    )


def test_projection_does_not_mutate_contracts_or_registrations_or_produce_later_artifacts():
    contracts = CONSTITUTIONAL_READ_MODEL_CONTRACTS
    registrations = tuple(
        constitutional_read_model_registration(contract) for contract in contracts
    )
    before_contracts = contracts
    before_registrations = registrations

    projections = project_constitutional_capabilities(contracts, registrations)

    assert contracts == before_contracts
    assert registrations == before_registrations
    assert all(isinstance(p, ConstitutionalCapabilityProjection) for p in projections)
    assert not any(hasattr(p, "selection_keys") for p in projections)
    assert not any(hasattr(p, "selected_view_names") for p in projections)
    assert not any(hasattr(p, "requested_views") for p in projections)


def test_manual_projection_fixtures_still_work_with_selection():
    selected = select_constitutional_views(
        question_projection=project_constitutional_question(
            produce_bounded_constitutional_question(
                operator_inquiry="show governance",
                inquiry_provenance="test",
                bounded_question="governance",
                scope_status="bounded",
                constitutional_intent="selection fixture compatibility",
                caller_supplied_fields={"selection_key": "governance"},
            )
        ),
        capability_projections=(
            ConstitutionalCapabilityProjection("constitutional_governance", ("governance",)),
        ),
    )

    assert selected.selected_view_names == ("constitutional_governance",)


def test_real_capability_projection_pairs_with_real_question_projection_for_selection():
    question = project_constitutional_question(
        produce_bounded_constitutional_question(
            operator_inquiry="show constitutional fidelity",
            inquiry_provenance="test",
            bounded_question="fidelity",
            scope_status="bounded",
            constitutional_intent="select exact fidelity view",
            caller_supplied_fields={"selection_key:fidelity": ""},
        )
    )

    selected = select_constitutional_views(
        question_projection=question,
        capability_projections=project_constitutional_capabilities(),
    )

    assert selected.selected_view_names == ("constitutional_fidelity",)
    assert selected.read_only is True
    assert selected.writes_event_ledger is False
    assert selected.mutates_cluster is False
