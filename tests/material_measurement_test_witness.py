from __future__ import annotations

from pathlib import Path
import sys

from seed_runtime.byte_measurement import (
    record_byte_measurement_responsibility_assignment,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
)
from seed_runtime.events import EventLedger
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition
from seed_runtime.operator_locality_standing import read_operator_locality_standing


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import exact_byte_material_references  # noqa: E402


def measured_one_byte_material():
    ledger = EventLedger()
    record_witness_material_acquisition(
        ledger,
        locality_identity="one-byte-material",
        exact_bytes=bytes(range(256)),
        source_boundary="one-byte material test boundary",
    )
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("one-byte-material",),
        recording_locality_identity="one-byte-measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="one-byte-measurement"
        ),
    )
    act_evidence = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="one-byte-measurement"
        ),
    )
    measurement = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    return ledger, exact_byte_material_references(ledger, measurement.identity)
