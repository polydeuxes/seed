"""Explicit represented-material fixture around the byte-native live acts."""

from __future__ import annotations

from io import BytesIO

from seed_runtime.operator_console import _advance_over
from seed_runtime.operator_ingest import run_operator_ingest
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation import (
    emit_operator_representation,
    record_operator_representation,
)
from tests.binary_input import BinaryFixtureInput


def run_material_fixture_console(
    *, ledger, locality_identity, input_stream, output_stream
) -> None:
    """Supply represented material explicitly; infer nothing from raw bytes."""

    if (
        not isinstance(input_stream, BinaryFixtureInput)
        or input_stream.supplied_material is None
    ):
        raise ValueError("developer-written represented material is required")
    locality_standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=locality_standing,
    )
    representation = emit_operator_representation(
        ledger, representation=representation, output_stream=output_stream
    )
    locality_standing = _advance_over(
        ledger,
        locality_standing,
        (
            representation["representation_event_identity"],
            representation["emission_attempt_event_identity"],
            representation["emitted_event_identity"],
        ),
        locality_identity=locality_identity,
    )
    for supplied_line in input_stream.supplied_material.splitlines(keepends=True):
        boundary_material = operator_boundary_material(
            BytesIO(supplied_line.encode("utf-8"))
        )
        with ledger.batched():
            attempt = run_operator_ingest(
                ledger=ledger,
                locality_identity=locality_identity,
                boundary_material=boundary_material,
                locality_standing=(
                    locality_standing if locality_standing["event_count"] else None
                ),
                supplied_material_representation=supplied_line,
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                attempt["event_identities"],
                locality_identity=locality_identity,
            )
            representation = record_operator_representation(
                ledger,
                locality_identity=locality_identity,
                locality_standing=locality_standing,
            )
            representation = emit_operator_representation(
                ledger, representation=representation, output_stream=output_stream
            )
            locality_standing = _advance_over(
                ledger,
                locality_standing,
                (
                    representation["representation_event_identity"],
                    representation["emission_attempt_event_identity"],
                    representation["emitted_event_identity"],
                ),
                locality_identity=locality_identity,
            )
