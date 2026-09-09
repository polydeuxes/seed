"""Exact source material and result coordinates."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re

import pytest

from scripts.observe_luminary099_source_binary import (
    ASSEMBLED_BINARY_PATH,
    BANK,
    BYTES_PER_WORD,
    LISTING_PATH,
    PINNED_REVISION,
    PROGRAM_DIRECTORY,
    REFERENCE_BINARY_PATH,
    SOURCE_PATH,
    WORDS_PER_BANK,
    agc_words_to_bytes,
    binary_bank_position,
    observe_luminary099,
    require_expected_reading,
)


READING_PATH = Path(__file__).parent / "public_domain" / "luminary099_reading.json"


def _reading() -> dict:
    return json.loads(READING_PATH.read_text(encoding="utf-8"))


def _fixture_checkout(tmp_path: Path, reading: dict) -> Path:
    program = tmp_path / PROGRAM_DIRECTORY
    program.mkdir()

    source = reading["source"]
    source_lines = ["## Copyright:\tPublic domain."]
    source_lines.extend("" for _ in range(source["first_line"] - 2))
    source_lines.extend(source["lines"])
    (program / SOURCE_PATH).write_text("\n".join(source_lines) + "\n", encoding="utf-8")

    listing_lines = []
    for row in reading["listing"]["rows"]:
        listing_lines.append(
            f'{row["global_line"]:06d},{row["source_line"]:06d}: '
            f'{row["bank_octal"]},{row["address_octal"]}           '
            f'{row["words_octal"][0]} {row["words_octal"][1]}  '
            f'{row["label"]}               2DEC     '
            f'{row["operand"]}     {row["scale"]}'
        )
    (program / LISTING_PATH).write_text("\n".join(listing_lines) + "\n", encoding="utf-8")

    binary_coordinates = reading["binary_coordinates"]
    binary = bytearray(0o44 * WORDS_PER_BANK * BYTES_PER_WORD)
    window = bytes.fromhex(reading["reference_binary"]["window_hex"])
    offset = binary_coordinates["window_byte_offset"]
    binary[offset : offset + len(window)] = window
    for name in (REFERENCE_BINARY_PATH, ASSEMBLED_BINARY_PATH):
        (program / name).write_bytes(binary)
    return tmp_path


def test_committed_reading_keeps_source_listing_and_binary_coordinates_separate():
    reading = _reading()

    assert reading["upstream"]["revision"] == PINNED_REVISION
    assert reading["source"]["first_line"] == 40
    assert reading["source"]["last_line"] == 45
    assert reading["listing"]["word_count"] == 12
    assert reading["binary_coordinates"] == {
        "bank_byte_offset": 61440,
        "bank_octal": "36",
        "bank_position": 30,
        "first_address_octal": "2000",
        "last_address_octal": "2013",
        "window_byte_count": 24,
        "window_byte_offset": 61440,
    }
    assert reading["reference_binary"]["path"] != reading["assembled_binary"]["path"]
    assert reading["reference_binary"]["sha256"] == reading["assembled_binary"]["sha256"]
    assert reading["reference_binary"]["window_hex"] == reading["assembled_binary"]["window_hex"]


def test_listing_words_encode_the_committed_binary_window():
    reading = _reading()
    words = tuple(int(word, 8) for word in reading["listing"]["words_octal"])

    assert agc_words_to_bytes(words).hex() == reading["reference_binary"]["window_hex"]
    assert binary_bank_position(BANK) == 30


def test_observer_reconstructs_the_committed_coordinate_shape(tmp_path):
    reading = _reading()
    root = _fixture_checkout(tmp_path, reading)

    observed = observe_luminary099(root, revision=PINNED_REVISION)

    assert observed["source"] == reading["source"]
    assert observed["listing"] == reading["listing"]
    assert observed["binary_coordinates"] == reading["binary_coordinates"]
    assert observed["reference_binary"]["window_hex"] == reading["reference_binary"]["window_hex"]
    assert observed["assembled_binary"]["window_hex"] == reading["assembled_binary"]["window_hex"]


def test_observer_refuses_different_proofread_reference_binary(tmp_path):
    reading = _reading()
    root = _fixture_checkout(tmp_path, reading)
    reference = root / PROGRAM_DIRECTORY / REFERENCE_BINARY_PATH
    material = bytearray(reference.read_bytes())
    material[-1] ^= 1
    reference.write_bytes(material)

    with pytest.raises(
        ValueError,
        match="source-assembled and proofread-reference binaries differ",
    ):
        observe_luminary099(root, revision=PINNED_REVISION)


def test_observer_refuses_changed_binary_placement(tmp_path):
    reading = _reading()
    root = _fixture_checkout(tmp_path, reading)
    for name in (REFERENCE_BINARY_PATH, ASSEMBLED_BINARY_PATH):
        path = root / PROGRAM_DIRECTORY / name
        material = bytearray(path.read_bytes())
        offset = reading["binary_coordinates"]["window_byte_offset"]
        material[offset : offset + 2] = b"\x00\x00"
        path.write_bytes(material)

    with pytest.raises(ValueError, match="listing words and addressed binary bytes differ"):
        observe_luminary099(root, revision=PINNED_REVISION)


def test_observer_refuses_source_listing_nonidentity(tmp_path):
    reading = _reading()
    root = _fixture_checkout(tmp_path, reading)
    source = root / PROGRAM_DIRECTORY / SOURCE_PATH
    source.write_text(source.read_text().replace("FDPS", "OTHER", 1), encoding="utf-8")

    with pytest.raises(ValueError, match="listing omits an addressed source statement"):
        observe_luminary099(root, revision=PINNED_REVISION)


@pytest.mark.parametrize(
    "changed_statement",
    (
        "FDPS               2DEC     4.3671     B-7",
        "FDPS               2DEC     4.3670     B-6",
        "FDPS               2DEC",
    ),
)
def test_observer_refuses_changed_listing_statement(tmp_path, changed_statement):
    reading = _reading()
    root = _fixture_checkout(tmp_path, reading)
    listing = root / PROGRAM_DIRECTORY / LISTING_PATH
    lines = listing.read_text(encoding="utf-8").splitlines()
    lines[0] = re.sub(r"FDPS\s+2DEC.*$", changed_statement, lines[0])
    listing.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="source statement"):
        observe_luminary099(root, revision=PINNED_REVISION)


def test_expected_reading_refuses_equal_off_window_binary_changes(tmp_path):
    reading = _reading()
    root = _fixture_checkout(tmp_path, reading)
    for name in (REFERENCE_BINARY_PATH, ASSEMBLED_BINARY_PATH):
        path = root / PROGRAM_DIRECTORY / name
        material = bytearray(path.read_bytes())
        material[-1] ^= 1
        path.write_bytes(material)

    observed = observe_luminary099(root, revision=PINNED_REVISION)

    assert observed["reference_binary"]["sha256"] == observed["assembled_binary"]["sha256"]
    assert observed["reference_binary"]["sha256"] != reading["reference_binary"]["sha256"]
    with pytest.raises(ValueError, match="expected reading"):
        require_expected_reading(observed, reading)


def test_observer_refuses_unpinned_revision(tmp_path):
    reading = deepcopy(_reading())
    root = _fixture_checkout(tmp_path, reading)

    with pytest.raises(ValueError, match="is not"):
        observe_luminary099(root, revision="different")
