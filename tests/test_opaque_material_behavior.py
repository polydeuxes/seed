"""Exact source material and Measurement result coordinates."""

from io import BytesIO
from pathlib import Path
import base64
import gzip
import tarfile

from seed_runtime.byte_measurement import BYTE_PAIR_MEASUREMENT_RECORDED_KIND
from seed_runtime.events import EventLedger
from seed_runtime.material_source import exact_material_result_bytes
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
)


ANONYMOUS_GZIP = base64.b64decode(
    "H4sIAAAAAAACA+3SQQ6CMBCF4a49RdMDmCKIwmWaIo3BQEloWRAub2Fj4toYE/9v8yZvFrOZfh46b6dFV5WZnG07fzdZeT0+wujFh+ikLIo9k/fU+py/5q3Pcn26CKnFF8wh2imdF/9pPUipbAhuaHrXmmZ/BlXLrU+bZonO3MbZR1ULAAAAAAAAAAAAAAAAAMDveAIhSo4CACgAAA=="
)


def _contained_material_and_tar() -> tuple[bytes, bytes]:
    contained = Path("tests/public_domain/luminary099_reading.json").read_bytes()[:43]
    buffer = BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        entry = tarfile.TarInfo("luminary099_reading_168.json")
        entry.size = len(contained)
        entry.mtime = 0
        entry.uid = 0
        entry.gid = 0
        entry.uname = ""
        entry.gname = ""
        archive.addfile(entry, BytesIO(contained))
    return contained, buffer.getvalue()


def test_anonymous_gzip_material_does_not_imply_inner_material_or_host_invocation():
    contained, tar_material = _contained_material_and_tar()
    assert len(ANONYMOUS_GZIP) == 157
    assert b"\n" not in ANONYMOUS_GZIP
    assert gzip.decompress(ANONYMOUS_GZIP) == tar_material

    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="opaque-material",
        input_stream=BytesIO(ANONYMOUS_GZIP),
    )

    events = ledger.list()
    material_results = [
        event
        for event in events
        if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
    ]
    assert [exact_material_result_bytes(event) for event in material_results] == [
        ANONYMOUS_GZIP
    ]
    assert [
        event.exact_material
        for event in events
        if type(event.exact_material) is bytes
    ] == [ANONYMOUS_GZIP]
    assert tar_material not in [event.exact_material for event in events]
    assert contained not in [event.exact_material for event in events]

    pair_result = next(
        event
        for event in events
        if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
    )
    result_kinds = [
        position["result"] for position in pair_result.material["result_positions"]
    ]
    assert result_kinds.count("count") == 140
    assert result_kinds.count("recurrence") == 1
