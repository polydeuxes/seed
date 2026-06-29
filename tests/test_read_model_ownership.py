from seed_runtime.projection_store import STATE_PROJECTION_VERSION
from seed_runtime.read_model_ownership import (
    read_model_construction_inputs,
    read_model_dependency_identity,
    read_model_dependency_identity_for_state_boundary,
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
