"""Exact source material and Measurement result coordinates."""

from io import BytesIO
from pathlib import Path
import base64
import gzip
import shutil
import subprocess
import tarfile

from scripts.operator_host_provider import invoke_operator_host
from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    result_positions_of_recorded_byte_measurement,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    get_recorded_pair_measurement_comparison,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_source import (
    exact_material_result_bytes,
    iter_exact_material_results,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates
from seed_runtime.operator_destination_locality import (
    OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND,
)
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialOccurrence,
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


def test_anonymous_gzip_material_does_not_invoke_an_unaddressed_host_callback():
    contained, tar_material = _contained_material_and_tar()
    assert len(ANONYMOUS_GZIP) == 157
    assert b"\n" not in ANONYMOUS_GZIP
    assert gzip.decompress(ANONYMOUS_GZIP) == tar_material
    gzip_executable = shutil.which("gzip")
    assert gzip_executable is not None
    assert subprocess.run(
        (gzip_executable, "-dc"),
        input=ANONYMOUS_GZIP,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout == tar_material

    provider_calls = []

    def provided_gzip(exact_command, supply):
        provider_calls.append(exact_command)
        completed = subprocess.run(
            (gzip_executable, "-dc"),
            input=ANONYMOUS_GZIP,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                exact_bytes=completed.stdout,
                source_boundary="provided gzip output",
            )
        )

    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="opaque-material",
        input_stream=BytesIO(ANONYMOUS_GZIP),
        operator_invocation_provider=provided_gzip,
    )

    assert provider_calls == []
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


def test_gzip_path_result_at_prior_boundary_enters_later_measurement_comparison():
    gzip_executable = shutil.which("gzip")
    assert gzip_executable is not None
    contained_material = b"A"
    anonymous_gzip = gzip.compress(contained_material, compresslevel=9, mtime=0)
    assert b"\n" not in anonymous_gzip

    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="operator",
        input_stream=BytesIO(b"!ls " + gzip_executable.encode() + b"\n"),
        operator_invocation_provider=invoke_operator_host,
    )
    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND
    )
    gzip_locality = relation.locality_identity
    prior_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=gzip_locality
    )
    prior_pair_measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        and event.locality_identity == gzip_locality
    )
    assert prior_pair_measurements
    prior_material_results = tuple(
        iter_exact_material_results(ledger, gzip_locality)
    )
    prior_pair_source_reference = prior_pair_measurements[-1].material[
        "source_result_position_reference"
    ]
    prior_byte_positions = result_positions_of_recorded_byte_measurement(
        ledger,
        prior_pair_source_reference["recorded_occurrence_identity"],
    )
    assert prior_byte_positions is not None
    prior_pair_source = next(
        position
        for position in prior_byte_positions
        if position["dimensions"]["position"]
        == prior_pair_source_reference["result_position"]
    )
    assert prior_pair_source["dimensions"]["content"]["source_material"] == [
        {"material_result_occurrence_identity": result.identity}
        for result in prior_material_results
    ]

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=gzip_locality,
        input_stream=BytesIO(anonymous_gzip),
        operator_invocation_provider=invoke_operator_host,
    )

    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=gzip_locality
    )
    assert (
        prior_coordinates["through_event_occurrence_identity"]
        != current_coordinates["through_event_occurrence_identity"]
    )
    material_results = tuple(iter_exact_material_results(ledger, gzip_locality))
    assert [event.exact_material for event in material_results] == [
        gzip_executable.encode() + b"\n",
        b"",
        b"",
        anonymous_gzip,
    ]
    assert all(
        event.exact_material != contained_material for event in material_results
    )

    pair_measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        and event.locality_identity == gzip_locality
    )
    comparisons = tuple(
        event
        for event in ledger.list()
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
        and event.locality_identity == gzip_locality
    )
    assert len(comparisons) == 1
    subjects = get_recorded_pair_measurement_comparison(
        ledger, comparisons[0].identity
    )["subject_reference"]
    assert subjects["earlier_measurement_reference"][
        "recorded_occurrence_identity"
    ] == prior_pair_measurements[-1].identity
    assert subjects["later_measurement_reference"][
        "recorded_occurrence_identity"
    ] == pair_measurements[-1].identity
