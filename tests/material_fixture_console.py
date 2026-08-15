"""Explicit represented-material fixture around the byte-native live acts."""

from __future__ import annotations

from io import BytesIO

from seed_runtime.operator_console import _advance_over
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation import (
    emit_operator_representation,
    record_operator_representation,
)
from tests.binary_input import BinaryFixtureInput


def run_material_fixture_console(
    *, ledger, workspace_id, locality_id, input_stream, output_stream
) -> None:
    """Supply represented material explicitly; infer nothing from raw bytes."""

    if (
        not isinstance(input_stream, BinaryFixtureInput)
        or input_stream.supplied_material is None
    ):
        raise ValueError("developer-written represented material is required")
    locality_standing = read_operator_locality_standing(
        ledger, workspace_id=workspace_id, locality_id=locality_id
    )
    representation = record_operator_representation(
        ledger,
        workspace_id=workspace_id,
        locality_id=locality_id,
        locality_standing=locality_standing,
    )
    representation = emit_operator_representation(
        ledger, representation=representation, output_stream=output_stream
    )
    locality_standing = _advance_over(
        ledger,
        locality_standing,
        (
            representation["representation_event_id"],
            representation["emission_attempt_event_id"],
            representation["emitted_event_id"],
        ),
        workspace_id=workspace_id,
        locality_id=locality_id,
    )
    for supplied_line in input_stream.supplied_material.splitlines(keepends=True):
        captured = capture_stdin_material(BytesIO(supplied_line.encode("utf-8")))
        with ledger.batched():
            attempt = run_operator_ingress_attempt(
                ledger=ledger,
                workspace_id=workspace_id,
                locality_id=locality_id,
                captured_ingress=captured,
                locality_standing=(
                    locality_standing if locality_standing["event_count"] else None
                ),
                supplied_material_representation=supplied_line,
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                attempt["event_ids"],
                workspace_id=workspace_id,
                locality_id=locality_id,
            )
            representation = record_operator_representation(
                ledger,
                workspace_id=workspace_id,
                locality_id=locality_id,
                locality_standing=locality_standing,
            )
            representation = emit_operator_representation(
                ledger, representation=representation, output_stream=output_stream
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                (
                    representation["representation_event_id"],
                    representation["emission_attempt_event_id"],
                    representation["emitted_event_id"],
                ),
                workspace_id=workspace_id,
                locality_id=locality_id,
            )
