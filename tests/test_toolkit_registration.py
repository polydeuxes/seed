from seed_builder.generator import CandidateStore, ToolkitGenerator
from seed_builder.registration import ToolkitRegistrationService
from seed_builder.validator import ToolkitValidator
from seed_runtime.events import EventLedger
from seed_runtime.models import ToolNeed
from seed_runtime.registry import ToolRegistry


def test_registers_validated_candidate_and_emits_events(tmp_path):
    need = ToolNeed(id="need_1", workspace_id="ws", name="host_notes", summary="Record notes about hosts", capability="host_notes", reason="safe demo", desired_inputs=["host"], desired_outputs=["stored"])
    candidate = ToolkitGenerator(CandidateStore(tmp_path)).generate(need)
    report = ToolkitValidator().validate(candidate.id, candidate.artifact_path)
    ledger = EventLedger()
    registry = ToolRegistry()

    registered = ToolkitRegistrationService(ledger, registry).register("ws", candidate.artifact_path, report)

    assert registered == ["host_notes"]
    assert registry.require("host_notes").name == "host_notes"
    assert ledger.list_events("ws")[-1].kind == "tool.registered"
