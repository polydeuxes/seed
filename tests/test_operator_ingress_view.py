from copy import deepcopy
from io import BytesIO, StringIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_ingress_view import format_operator_ingress_view
from seed_runtime.state import StateProjector
from scripts import seed_local


def _successful_projection(text="exact material\n", *, ledger=None, workspace="w"):
    ledger = ledger or EventLedger()
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id=workspace,
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO(text)),
        output_stream=StringIO(),
    )
    return ledger, projection


def test_rendering_is_deterministic_and_preserves_supported_testimony():
    _, projection = _successful_projection()

    first = format_operator_ingress_view(projection)
    second = format_operator_ingress_view(projection)

    assert first == second
    ingress = projection["current_standing"]["preserved_ingress"]
    material = projection["addressable_operator_material"]
    assert 'Represented material: "exact material\\n"' in first
    assert ingress["subject_ref"] in first
    assert ingress["evidence_event_id"] in first
    assert "workspace:w" in first
    assert "session:s" in first
    assert all(reference in first for reference in material["provenance"])
    assert all(limit in first for limit in material["known_loss"])
    assert all(unknown in first for unknown in material["unknowns"])
    assert "Communicative meaning: unresolved (Unknown)." in first
    assert projection["event_ids"][-1] in first
    assert projection["last_event_kind"] in first


def test_view_formation_is_read_only_and_does_not_perform_semantic_compare():
    ledger, projection = _successful_projection()
    projection_before = deepcopy(projection)
    events_before = ledger.list_events("w")
    state_before = StateProjector(ledger).project("w")

    rendered = format_operator_ingress_view(projection)

    assert projection == projection_before
    assert ledger.list_events("w") == events_before
    assert StateProjector(ledger).project("w") == state_before
    assert "compare" not in rendered.lower()
    assert "intent=" not in rendered.lower()
    assert "goal=" not in rendered.lower()


def test_console_consumes_returned_projection_then_writes_formed_view(monkeypatch):
    _, projection = _successful_projection()
    calls = []

    def attempt(**kwargs):
        calls.append(("attempt", kwargs["output_stream"].getvalue()))
        return projection

    def form(supplied):
        calls.append(("formation", supplied))
        return "formed View\n"

    class Output(StringIO):
        def write(self, text):
            calls.append(("write", text))
            return super().write(text)

    monkeypatch.setattr(seed_local, "run_operator_ingress_attempt", attempt)
    monkeypatch.setattr(seed_local, "format_operator_ingress_view", form)
    output = Output()
    seed_local.run_persistent_operator_console(
        ledger=EventLedger(),
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("material\n"),
        output_stream=output,
    )

    assert calls[0] == ("write", "Seed console: `exit` exits.\n")
    assert calls[1][0] == "attempt"
    assert calls[2] == ("formation", projection)
    assert calls[3] == ("write", "formed View\n")
    assert output.getvalue().endswith("formed View\n")


def test_decoder_failure_output_and_lack_of_successful_view_are_unchanged():
    class RawInput:
        buffer = BytesIO(b"\xff\n")
        encoding = "utf-8"

    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=RawInput(),
        output_stream=output,
    )

    assert "Operator ingress View" not in output.getvalue()
    assert output.getvalue().endswith(
        "Representation insufficient: captured material did not decode under "
        "the selected decoder mechanism.\n"
    )


def test_later_event_boundary_makes_prior_view_stale_without_extra_claims():
    _, earlier = _successful_projection("earlier\n")
    _, later = _successful_projection("later\n")
    earlier_text = format_operator_ingress_view(earlier)
    later_text = format_operator_ingress_view(later)

    assert earlier["event_ids"][-1] in earlier_text
    assert later["event_ids"][-1] in later_text
    assert 'Represented material: "earlier\\n"' in earlier_text
    assert 'Represented material: "later\\n"' in later_text
    unsupported = ("incomplete", "rece" + "ipt", "acknowledg" + "ment")
    assert not any(term in earlier_text.lower() for term in unsupported)
