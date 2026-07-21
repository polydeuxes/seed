from seed_runtime.projection_store import STATE_PROJECTION_VERSION
from seed_runtime.read_model_ownership import (
    read_model_cache_lookup_request,
    read_model_construction_inputs,
    read_model_construction_request,
    read_model_dependency_identity,
    read_model_dependency_identity_for_state_boundary,
    construct_read_model,
    resolve_read_model_cache_lookup,
)
from seed_runtime.state import State


def test_read_model_dependency_identity_preserves_existing_projected_state_identity():
    state = State(workspace_id="ws", last_event_id="evt_current")
    inputs = read_model_construction_inputs(state)

    identity = read_model_dependency_identity(
        inputs, state_projection_version=STATE_PROJECTION_VERSION
    )

    assert identity.state_projection_version == STATE_PROJECTION_VERSION
    assert identity.state_last_event_id == "evt_current"


def test_read_model_dependency_identity_can_use_known_state_boundary_for_cache_lookup():
    identity = read_model_dependency_identity_for_state_boundary(
        state_projection_version=STATE_PROJECTION_VERSION,
        state_last_event_id="evt_current",
    )

    assert identity.state_projection_version == STATE_PROJECTION_VERSION
    assert identity.state_last_event_id == "evt_current"


def test_read_model_cache_lookup_resolves_existing_exact_identity_lookup():
    identity = read_model_dependency_identity_for_state_boundary(
        state_projection_version=STATE_PROJECTION_VERSION,
        state_last_event_id="evt_current",
    )
    request = read_model_cache_lookup_request(identity)
    calls = []

    def load_snapshot(lookup_identity):
        calls.append(lookup_identity)
        return {"snapshot": "cached"} if lookup_identity == identity else None

    result = resolve_read_model_cache_lookup(request, load_snapshot)

    assert calls == [identity]
    assert result.request == request
    assert result.cache_hit is True
    assert result.snapshot == {"snapshot": "cached"}


def test_read_model_cache_lookup_preserves_existing_miss_decision():
    identity = read_model_dependency_identity_for_state_boundary(
        state_projection_version=STATE_PROJECTION_VERSION,
        state_last_event_id="evt_current",
    )

    result = resolve_read_model_cache_lookup(
        read_model_cache_lookup_request(identity),
        lambda _lookup_identity: None,
    )

    assert result.cache_hit is False
    assert result.snapshot is None


def test_read_model_construction_request_preserves_existing_builder_handoff():
    state = State(workspace_id="ws", last_event_id="evt_current")
    inputs = read_model_construction_inputs(state)
    identity = read_model_dependency_identity(
        inputs, state_projection_version=STATE_PROJECTION_VERSION
    )
    lookup = resolve_read_model_cache_lookup(
        read_model_cache_lookup_request(identity),
        lambda _lookup_identity: None,
    )
    request = read_model_construction_request(inputs, identity, cache_lookup=lookup)
    calls = []

    def build_read_model(construction_inputs):
        calls.append(construction_inputs)
        return {"workspace_id": construction_inputs.visible_state.workspace_id}

    result = construct_read_model(request, build_read_model)

    assert calls == [inputs]
    assert result.request == request
    assert result.read_model == {"workspace_id": "ws"}
    assert result.request.cache_lookup is lookup


def test_read_model_cache_publication_preserves_existing_snapshot_save_handoff():
    from seed_runtime.read_model_ownership import (
        publish_read_model_cache,
        read_model_cache_publication_request,
    )

    state = State(workspace_id="ws", last_event_id="evt_current")
    inputs = read_model_construction_inputs(state)
    identity = read_model_dependency_identity(
        inputs, state_projection_version=STATE_PROJECTION_VERSION
    )
    construction = construct_read_model(
        read_model_construction_request(inputs, identity),
        lambda construction_inputs: {
            "workspace_id": construction_inputs.visible_state.workspace_id,
            "last_event_id": construction_inputs.visible_state.last_event_id,
        },
    )
    saved_snapshots = []

    result = publish_read_model_cache(
        read_model_cache_publication_request(construction),
        lambda publication_construction: {
            "payload": publication_construction.read_model,
            "state_last_event_id": publication_construction.request.dependency_identity.state_last_event_id,
        },
        saved_snapshots.append,
    )

    assert result.request.construction_result is construction
    assert result.snapshot == {
        "payload": {"workspace_id": "ws", "last_event_id": "evt_current"},
        "state_last_event_id": "evt_current",
    }
    assert saved_snapshots == [result.snapshot]


def test_read_model_view_registration_preserves_registration_without_dispatch_or_rendering():
    from seed_runtime.read_model_ownership import (
        read_model_view_registration,
        register_read_model_view,
    )

    registration = read_model_view_registration(
        name="constitutional_placeholder",
        cli_flag="--constitutional-placeholder",
        builder="seed_runtime.example.build_placeholder",
        renderer="scripts.seed_local.format_placeholder",
    )

    result = register_read_model_view(registration)

    assert result.registration is registration
    assert result.registration.read_only is True
    assert result.registration.builder == "seed_runtime.example.build_placeholder"
    assert result.registration.renderer == "scripts.seed_local.format_placeholder"


def test_existing_read_model_view_registrations_expose_consumable_cli_flags():
    from seed_runtime.read_model_ownership import (
        READ_MODEL_VIEW_REGISTRATIONS,
        read_model_view_registration_flags,
    )

    flags = read_model_view_registration_flags(READ_MODEL_VIEW_REGISTRATIONS)

    assert "--current-observations" in flags
    assert "--current-requirements" in flags
    assert "--current-capabilities" in flags
    assert "--current-issues" in flags
    assert all(registration.read_only for registration in READ_MODEL_VIEW_REGISTRATIONS)


def test_constitutional_process_view_registration_exposes_consumable_cli_flag():
    from seed_runtime.read_model_ownership import READ_MODEL_VIEW_REGISTRATIONS

    registration = next(
        registration
        for registration in READ_MODEL_VIEW_REGISTRATIONS
        if registration.name == "constitutional_process"
    )

    assert registration.cli_flag == "--constitutional-process"
    assert (
        registration.builder
        == "seed_runtime.constitutional_process_view.build_constitutional_process_view"
    )
    assert registration.read_only is True


def test_constitutional_governance_view_registration_exposes_consumable_cli_flag():
    from seed_runtime.read_model_ownership import READ_MODEL_VIEW_REGISTRATIONS

    registration = next(
        registration
        for registration in READ_MODEL_VIEW_REGISTRATIONS
        if registration.name == "constitutional_governance"
    )

    assert registration.cli_flag == "--constitutional-governance"
    assert (
        registration.builder
        == "seed_runtime.constitutional_governance_view.build_constitutional_governance_view"
    )
    assert registration.read_only is True


def test_constitutional_fidelity_view_registration_exposes_consumable_cli_flag():
    from seed_runtime.read_model_ownership import READ_MODEL_VIEW_REGISTRATIONS

    registration = next(
        registration
        for registration in READ_MODEL_VIEW_REGISTRATIONS
        if registration.name == "constitutional_fidelity"
    )

    assert registration.cli_flag == "--constitutional-fidelity"
    assert (
        registration.builder
        == "seed_runtime.constitutional_fidelity_view.build_constitutional_fidelity_view"
    )
    assert registration.read_only is True


def test_constitutional_read_model_contracts_recover_recurring_obligations():
    from seed_runtime.read_model_ownership import CONSTITUTIONAL_READ_MODEL_CONTRACTS

    contracts = {
        contract.name: contract for contract in CONSTITUTIONAL_READ_MODEL_CONTRACTS
    }

    assert set(contracts) == {"constitutional_process", "constitutional_governance", "constitutional_fidelity"}
    for contract in contracts.values():
        assert contract.cli_flag.startswith("--constitutional-")
        assert contract.builder.startswith("seed_runtime.constitutional_")
        assert contract.renderer.startswith("seed_runtime.constitutional_")
        assert contract.json_renderer.startswith("seed_runtime.constitutional_")
        assert contract.inventory_name == contract.name
        assert contract.shape_audit_name == contract.name
        assert contract.read_only is True
        assert contract.supports_json is True
        assert contract.supports_record is False
        assert contract.record_scope == "none"
        assert contract.writes_event_ledger is False
        assert contract.mutates_cluster is False


def test_constitutional_read_model_contracts_match_inventory_and_shape_audit():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import IMPLEMENTATION_SPECS
    from seed_runtime.read_model_ownership import CONSTITUTIONAL_READ_MODEL_CONTRACTS

    inventory_by_name = {entry.name: entry for entry in DIAGNOSTIC_INVENTORY}

    for contract in CONSTITUTIONAL_READ_MODEL_CONTRACTS:
        inventory_entry = inventory_by_name[contract.inventory_name]
        shape_spec = IMPLEMENTATION_SPECS[contract.shape_audit_name]

        assert inventory_entry.cli_flags == (contract.cli_flag,)
        assert inventory_entry.supports_json is contract.supports_json
        assert inventory_entry.supports_record is contract.supports_record
        assert inventory_entry.record_scope == contract.record_scope
        assert inventory_entry.writes_event_ledger is contract.writes_event_ledger
        assert inventory_entry.mutates_cluster is contract.mutates_cluster
        assert shape_spec.cli_flags == (contract.cli_flag,)
        assert f"{shape_spec.build_function}" in contract.builder
        assert f"{shape_spec.format_function}" in contract.renderer
        assert f"{shape_spec.json_function}" in contract.json_renderer
