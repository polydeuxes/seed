"""Interrogate terminal content and presentation as distinct exact results.

One isolated tmux server renders each exact source at one fixed geometry.  The
plain cell capture and style-preserving capture remain external testimony.  No
Seed Measurement establishes presentation controls or forms new styled output.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path
import re
import subprocess
import tempfile
import time

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    get_recorded_pair_measurement_comparison,
)
from seed_runtime.witness_material_acquisition import WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND, record_witness_material_acquisition
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation import (
    REPRESENTATION_RECORDED_KIND,
    read_operator_representation,
)
from seed_runtime.operator_representation_admission import (
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND,
    REPRESENTATION_CANDIDATE_RECORDED_KIND,
    get_recorded_exact_material_representation_admission,
)
from seed_runtime.operator_invocation_locality import OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
from seed_runtime.supplied_invocation_material import SuppliedWitnessMaterialOccurrence
from tests.binary_input import binary_input


TMUX = Path("/usr/bin/tmux")
TAIL = Path("/usr/bin/tail")
SGR = re.compile(rb"\x1b\[[0-9;:]*m")
EXACT_MATERIAL = (
    b"Seed material witness\n",
    (
        b"\x1b[38;2;205;214;244mSeed "
        b"\x1b[1mmaterial witness\x1b[0m\n"
    ),
)
FUNCTION_MATERIAL = (
    b"tmux isolated terminal capture; width 40; height 8; "
    b"plain cells and style-preserving cells"
)


def _capture_terminal_material(source: Path, socket: Path) -> tuple[bytes, bytes]:
    target = "witness:0.0"
    command = f"{TAIL} -f {source}"
    subprocess.run(
        (
            str(TMUX),
            "-S",
            str(socket),
            "new-session",
            "-d",
            "-x",
            "40",
            "-y",
            "8",
            "-s",
            "witness",
            command,
        ),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=2.0,
    )
    try:
        plain = b""
        for _ in range(100):
            plain = subprocess.run(
                (
                    str(TMUX),
                    "-S",
                    str(socket),
                    "capture-pane",
                    "-p",
                    "-J",
                    "-t",
                    target,
                ),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2.0,
            ).stdout
            if b"Seed material witness" in plain:
                break
            time.sleep(0.01)
        else:
            raise AssertionError("external terminal did not expose exact cells")
        styled = subprocess.run(
            (
                str(TMUX),
                "-S",
                str(socket),
                "capture-pane",
                "-p",
                "-e",
                "-J",
                "-t",
                target,
            ),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2.0,
        ).stdout
        return plain, styled
    finally:
        subprocess.run(
            (str(TMUX), "-S", str(socket), "kill-server"),
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2.0,
        )


@pytest.fixture(scope="module")
def terminal_style_witness_observation(tmp_path_factory):
    if not TMUX.is_file() or not TAIL.is_file():
        pytest.skip("the external terminal implementation function is unavailable")

    directory = tmp_path_factory.mktemp("terminal-style-witness")
    captures = []
    for position, material in enumerate(EXACT_MATERIAL):
        source = directory / f"source-{position}"
        source.write_bytes(material)
        captures.append(
            _capture_terminal_material(
                source,
                directory / f"tmux-{position}.sock",
            )
        )

    ledger = EventLedger()
    function = record_witness_material_acquisition(
        ledger,
        locality_identity="terminal-style-material-witness-source",
        exact_bytes=FUNCTION_MATERIAL,
        source_boundary="terminal style external function reference",
    )
    sources = tuple(
        record_witness_material_acquisition(
            ledger,
            locality_identity="terminal-style-material-witness-source",
            exact_bytes=material,
            source_boundary=f"terminal style source occurrence {position}",
        )
        for position, material in enumerate(EXACT_MATERIAL)
    )
    plain_results = tuple(
        record_witness_material_acquisition(
            ledger,
            locality_identity="terminal-style-material-witness-result",
            exact_bytes=capture[0],
            source_boundary=f"external terminal plain result {position}",
            provenance_occurrence_references=(
                function.identity,
                sources[position].identity,
            ),
        )
        for position, capture in enumerate(captures)
    )
    styled_results = tuple(
        record_witness_material_acquisition(
            ledger,
            locality_identity="terminal-style-material-witness-result",
            exact_bytes=capture[1],
            source_boundary=f"external terminal styled result {position}",
            provenance_occurrence_references=(
                function.identity,
                sources[position].identity,
            ),
        )
        for position, capture in enumerate(captures)
    )
    return ledger, function, sources, plain_results, styled_results


def test_style_does_not_change_the_plain_terminal_cells(
    terminal_style_witness_observation,
):
    _, _, _, plain_results, _ = terminal_style_witness_observation

    assert plain_results[0].exact_material == plain_results[1].exact_material
    assert b"Seed material witness" in plain_results[0].exact_material
    assert b"\x1b" not in plain_results[0].exact_material


def test_style_preserving_capture_keeps_a_distinct_exact_result(
    terminal_style_witness_observation,
):
    _, _, _, plain_results, styled_results = terminal_style_witness_observation

    assert styled_results[0].exact_material != styled_results[1].exact_material
    assert SGR.findall(styled_results[0].exact_material) == []
    assert SGR.findall(styled_results[1].exact_material)
    assert tuple(
        SGR.sub(b"", result.exact_material) for result in styled_results
    ) == tuple(result.exact_material for result in plain_results)


def test_each_terminal_result_preserves_source_and_function_provenance(
    terminal_style_witness_observation,
):
    _, function, sources, plain_results, styled_results = (
        terminal_style_witness_observation
    )
    expected = tuple(
        [function.identity, source.identity] for source in sources
    )

    for results in (plain_results, styled_results):
        assert tuple(
            result.material["provenance_occurrence_references"]
            for result in results
        ) == expected
        assert len({result.identity for result in results}) == len(results)


def test_terminal_views_cross_compare_and_only_exact_styled_material_egresses(
    terminal_style_witness_observation,
):
    _, _, _, plain_results, styled_results = terminal_style_witness_observation
    ledger = EventLedger()
    command = b"!witness terminal style\n"
    supplied = (
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=FUNCTION_MATERIAL,
            source_boundary="terminal style external function reference",
            egress=False,
        ),
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=EXACT_MATERIAL[0],
            source_boundary="plain terminal source occurrence",
            egress=False,
        ),
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=plain_results[0].exact_material,
            source_boundary="plain terminal cell result",
            egress=False,
            provenance_occurrence_positions=(0, 1),
        ),
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=EXACT_MATERIAL[1],
            source_boundary="styled terminal source occurrence",
            egress=False,
        ),
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=plain_results[1].exact_material,
            source_boundary="styled source plain terminal cell result",
            egress=False,
            provenance_occurrence_positions=(0, 3),
        ),
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=styled_results[1].exact_material,
            source_boundary="styled source style preserving terminal result",
            egress=True,
            provenance_occurrence_positions=(0, 3, 4),
        ),
    )

    def provider(exact_command, supply):
        assert exact_command == command
        for occurrence in supplied:
            supply(occurrence)

    with tempfile.TemporaryFile(mode="w+b") as raw_output:
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="terminal-style-operator-locality",
            input_stream=binary_input(command),
            output_stream=StringIO(),
            raw_output_stream=raw_output,
            operator_invocation_provider=provider,
        )
        raw_output.seek(0)
        emitted = raw_output.read()

    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    )
    invocation_locality = relation.material["destination_locality_identity"]
    events = ledger.list_locality(invocation_locality)
    acquisition_results = tuple(
        event for event in events if event.kind == WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
    )
    comparisons = tuple(
        event
        for event in events
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )

    assert tuple(event.exact_material for event in acquisition_results) == tuple(
        occurrence.exact_bytes for occurrence in supplied
    )
    assert emitted == styled_results[1].exact_material
    assert len(comparisons) == 3

    terminal_view_comparison = get_recorded_pair_measurement_comparison(
        ledger, comparisons[-1].identity
    )
    assignment = ledger.get(
        terminal_view_comparison["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    assert assignment is not None
    assert assignment.material["added_occurrence_reference"] == acquisition_results[5].identity
    assert assignment.material["added_occurrence_provenance_references"][-3:] == [
        acquisition_results[0].identity,
        acquisition_results[3].identity,
        acquisition_results[4].identity,
    ]
    assert terminal_view_comparison["findings"]["conflicting_findings"]
    assert terminal_view_comparison["findings"]["unknown_findings"] == []

    comparison_identities = {event.identity for event in comparisons}
    comparison_representations = tuple(
        read_operator_representation(ledger, event.identity)
        for event in events
        if event.kind == REPRESENTATION_RECORDED_KIND
        and event.material["source_occurrence_reference"] in comparison_identities
    )
    assert len(comparison_representations) == len(comparisons)
    assert all(
        representation["exact_material"] is None
        and "representation_rule" not in representation
        for representation in comparison_representations
    )

    comparison_representation_identities = {
        representation["representation_event_identity"]
        for representation in comparison_representations
    }
    comparison_candidate_identities = {
        event.identity
        for event in events
        if event.kind == REPRESENTATION_CANDIDATE_RECORDED_KIND
        and event.material["representation_reference"][
            "representation_event_identity"
        ]
        in comparison_representation_identities
    }
    admitted_candidate_identities = {
        get_recorded_exact_material_representation_admission(ledger, event.identity)[
            "candidate_reference"
        ]["recorded_occurrence_identity"]
        for event in events
        if event.kind == EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND
    }
    assert len(comparison_candidate_identities) == len(comparisons)
    assert comparison_candidate_identities.isdisjoint(admitted_candidate_identities)

    standing = read_operator_locality_standing(
        ledger, locality_identity=invocation_locality
    )
    assert set(standing["comparison_result_occurrences"]) == comparison_identities
