from __future__ import annotations

from pathlib import Path
import sys

from seed_runtime.byte_measurement import record_byte_count_layer
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import exact_byte_material_references  # noqa: E402


def measured_one_byte_material():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="one-byte-material",
        exact_bytes=bytes(range(256)),
        source_role="fixture material",
        source_boundary="fixture-0",
    )
    measurement = record_byte_count_layer(
        ledger,
        source_localities=("one-byte-material",),
        recording_locality_identity="one-byte-measurement",
    )
    return ledger, exact_byte_material_references(ledger, measurement.identity)
