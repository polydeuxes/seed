"""Interrogate terminal content and presentation as distinct exact results.

One isolated tmux server renders each exact source at one fixed geometry.  The
plain cell capture and style-preserving capture remain external testimony.  No
Seed Measurement identifies presentation controls or forms new styled output.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import time

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


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
    function = ingest_material(
        ledger,
        locality_identity="terminal-style-material-witness-source",
        exact_bytes=FUNCTION_MATERIAL,
        source_role="operator supplied material",
        source_boundary="terminal style external function reference",
    )
    sources = tuple(
        ingest_material(
            ledger,
            locality_identity="terminal-style-material-witness-source",
            exact_bytes=material,
            source_role="operator supplied material",
            source_boundary=f"terminal style source occurrence {position}",
        )
        for position, material in enumerate(EXACT_MATERIAL)
    )
    plain_results = tuple(
        ingest_material(
            ledger,
            locality_identity="terminal-style-material-witness-result",
            exact_bytes=capture[0],
            source_role="system",
            source_boundary=f"external terminal plain result {position}",
            provenance_occurrence_references=(
                function.identity,
                sources[position].identity,
            ),
        )
        for position, capture in enumerate(captures)
    )
    styled_results = tuple(
        ingest_material(
            ledger,
            locality_identity="terminal-style-material-witness-result",
            exact_bytes=capture[1],
            source_role="system",
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
