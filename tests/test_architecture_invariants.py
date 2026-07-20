from __future__ import annotations

from pathlib import Path

from seed_runtime.capability_catalog import (
    CapabilityCatalog,
    CapabilityCatalogEntry,
    CapabilityRecommendation,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.models import Decision, RuntimeResponse, ToolNeed
from seed_runtime.projection_store import ProjectionStore
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import Runtime
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService




def test_runtime_loop_module_is_absent_from_seed_runtime():
    assert not Path("seed_runtime/runtime_loop.py").exists()
    assert not list(Path("seed_runtime").glob("**/runtime_loop.py"))




def test_capability_recommendation_operation_is_handoff_metadata_not_registered_operation():
    catalog = CapabilityCatalog(
        [
            CapabilityCatalogEntry(
                capability="ssh_access",
                summary="SSH access metadata",
                recommendations=[
                    CapabilityRecommendation(
                        provider="ops_handoff",
                        summary="Ask an operator to verify SSH reachability.",
                        backend_type="manual",
                        operation="verify_ssh_access",
                    )
                ],
            )
        ]
    )
    registry = ToolRegistry()
    ledger = EventLedger()
    service = ToolNeedService(ledger, StateProjector(ledger))
    need = ToolNeed(
        id="need_ssh",
        name="ssh_access",
        summary="Need SSH access",
        capability="ssh_access",
        reason="connectivity is unknown",
    )

    resolution = service.resolve_capability(
        need,
        capability_catalog=catalog,
        tool_registry=registry,
    )

    assert resolution["known_capability"] is True
    assert resolution["registered_operations"] == []
    assert resolution["handoff_candidates"] == [
        {
            "provider": "ops_handoff",
            "backend_type": "manual",
            "operation": "verify_ssh_access",
        }
    ]


def test_projection_store_protocol_does_not_own_event_methods():
    assert "append" not in ProjectionStore.__dict__
    assert "extend" not in ProjectionStore.__dict__
    assert "list" not in ProjectionStore.__dict__
    assert "list_events" not in ProjectionStore.__dict__
    assert "get" not in ProjectionStore.__dict__


def test_event_ledgers_do_not_own_projection_snapshot_methods():
    snapshot_methods = {"load_snapshot", "save_snapshot", "clear_snapshot"}

    assert snapshot_methods.isdisjoint(EventLedger.__dict__)
    assert snapshot_methods.isdisjoint(SQLiteEventLedger.__dict__)
