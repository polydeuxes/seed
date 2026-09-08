"""Record current Seed occurrences from opaque acquired material.

This findings-only source producer does not read the Book or machine grammar.
Each source uses one fresh Locality and one exact input boundary so later blind
work can compare separately recorded occurrence sequences.  The event label is
preserved for later inspection but is not an input to the blind observer.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.operator_console import run_persistent_operator_console


OUTPUT = Path("/tmp/seed_inward_occurrence_material.json")
SOURCE_MATERIALS = (
    b"zafeqor\n",
    b"nivokasure\n",
    b"gudewalotyc\n",
    b"beximorufadyn\n",
)


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _record_source(payload: tuple[int, bytes]) -> dict:
    source_number, exact_material = payload
    begun = time.perf_counter()
    ledger = EventLedger()
    failure = None
    try:
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity=f"inward-source-{source_number}",
            input_stream=BytesIO(exact_material),
        )
    except Exception as error:  # Preserve a bounded failed source exactly.
        failure = f"{type(error).__name__}: {error}"
    occurrences = []
    for append_position, event in enumerate(ledger.list()):
        exact = event.exact_material
        occurrences.append(
            {
                "append_position": append_position,
                "identity": event.identity,
                "event_label": event.kind,
                "timestamp": event.timestamp.isoformat(),
                "locality_identity": event.locality_identity,
                "material": event.material,
                "exact_material_hex": None if exact is None else exact.hex(),
            }
        )
    return {
        "source_number": source_number,
        "input_sha256": _digest(exact_material),
        "input_byte_count": len(exact_material),
        "occurrence_count": len(occurrences),
        "occurrences": occurrences,
        "known_loss": failure,
        "wall_seconds": time.perf_counter() - begun,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--jobs", type=int, default=4)
    arguments = parser.parse_args()
    if arguments.jobs < 1:
        raise ValueError("jobs must be positive")

    begun = time.perf_counter()
    payloads = list(enumerate(SOURCE_MATERIALS))
    if arguments.jobs == 1:
        sources = [_record_source(payload) for payload in payloads]
    else:
        with ProcessPoolExecutor(max_workers=arguments.jobs) as executor:
            sources = list(executor.map(_record_source, payloads))
    for source in sources:
        print(
            f"source {source['source_number']} "
            f"bytes={source['input_byte_count']} "
            f"occurrences={source['occurrence_count']} "
            f"{source['wall_seconds']:.3f}s "
            f"known loss={source['known_loss']}",
            flush=True,
        )

    finding = {
        "operation": (
            "current operator acquisition and declared work from one exact "
            "opaque material boundary in each fresh Locality"
        ),
        "sources": [
            {key: value for key, value in source.items() if key != "wall_seconds"}
            for source in sources
        ],
        "known_loss": (
            None
            if all(source["known_loss"] is None for source in sources)
            else "one or more exact source recordings stopped at a runtime refusal"
        ),
    }
    encoded = _encoded(finding)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
