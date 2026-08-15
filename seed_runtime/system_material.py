"""System material entering the shared Ingest boundary."""

from __future__ import annotations

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


def preserve_system_material(
    ledger: EventLedger,
    *,
    locality_identity: str,
    exact_bytes: bytes,
    observed_boundary: str,
    represented_material: str | None = None,
) -> Event:
    return ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=exact_bytes,
        source_role="system",
        source_boundary=observed_boundary,
        represented_material=represented_material,
        known_loss=(
            "material before the supplied system boundary is not available here",
        ),
    )
