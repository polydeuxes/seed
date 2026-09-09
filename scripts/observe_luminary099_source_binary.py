#!/usr/bin/env python3
"""Observe one exact Luminary 099 source/listing/binary correspondence."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from typing import Any


PINNED_REVISION = "ebd8695d23bde6eb9f26933ddf244b8d18987f21"
PROGRAM_DIRECTORY = "Luminary099"
SOURCE_PATH = "CONTROLLED_CONSTANTS.agc"
SOURCE_FIRST_LINE = 40
SOURCE_LAST_LINE = 45
LISTING_PATH = "Luminary099.lst"
REFERENCE_BINARY_PATH = "Luminary099.bin"
ASSEMBLED_BINARY_PATH = "MAIN.agc.bin"
BANK = 0o36
FIRST_ADDRESS = 0o2000
WORDS_PER_BANK = 0o2000
BYTES_PER_WORD = 2

_LISTING_ROW = re.compile(
    r"^(?P<global_line>[0-9]{6}),(?P<source_line>[0-9]{6}):\s+"
    r"(?P<bank>[0-7]{2}),(?P<address>[0-7]{4})\s+"
    r"(?P<first>[0-7]{5})\s+(?P<second>[0-7]{5})\s+"
    r"(?P<label>\S+)\s+2DEC\b"
)


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def agc_words_to_bytes(words: tuple[int, ...]) -> bytes:
    """Encode right-aligned 15-bit words in the rope-image byte format."""
    encoded = bytearray()
    for word in words:
        if type(word) is not int or not 0 <= word <= 0o77777:
            raise ValueError("AGC word must be a 15-bit integer")
        encoded.extend((word << 1).to_bytes(BYTES_PER_WORD, "big"))
    return bytes(encoded)


def binary_bank_position(bank: int) -> int:
    """Return the bank's zero-based position in a Block II rope image."""
    if type(bank) is not int or not 0 <= bank < 0o44:
        raise ValueError("Block II bank must be in the exact range 00 through 43")
    return {0o2: 0, 0o3: 1, 0o0: 2, 0o1: 3}.get(bank, bank)


def _source_lines(source: Path) -> tuple[str, ...]:
    lines = source.read_text(encoding="utf-8").splitlines()
    if len(lines) < SOURCE_LAST_LINE:
        raise ValueError("Luminary source does not contain the addressed lines")
    if not any(
        "Copyright:" in line and "Public domain" in line for line in lines[:12]
    ):
        raise ValueError("Luminary source lacks its public-domain declaration")
    selected = tuple(lines[SOURCE_FIRST_LINE - 1 : SOURCE_LAST_LINE])
    if any(not line or line[0].isspace() for line in selected):
        raise ValueError("addressed Luminary source statement is malformed")
    return selected


def _listing_rows(listing: Path, source_lines: tuple[str, ...]) -> tuple[dict[str, Any], ...]:
    labels = tuple(line.split()[0] for line in source_lines)
    expected_source_lines = range(SOURCE_FIRST_LINE, SOURCE_LAST_LINE + 1)
    matches: dict[tuple[int, str], re.Match[str]] = {}
    for line in listing.read_text(encoding="utf-8").splitlines():
        match = _LISTING_ROW.match(line)
        if match is None or int(match.group("bank"), 8) != BANK:
            continue
        key = (int(match.group("source_line")), match.group("label"))
        if key in zip(expected_source_lines, labels, strict=True):
            if key in matches:
                raise ValueError("listing repeats an addressed source statement")
            matches[key] = match

    rows = []
    for source_line, label in zip(expected_source_lines, labels, strict=True):
        match = matches.get((source_line, label))
        if match is None:
            raise ValueError("listing omits an addressed source statement")
        rows.append(
            {
                "global_line": int(match.group("global_line")),
                "source_line": source_line,
                "bank_octal": match.group("bank"),
                "address_octal": match.group("address"),
                "words_octal": [match.group("first"), match.group("second")],
                "label": label,
            }
        )

    expected_addresses = tuple(FIRST_ADDRESS + position for position in range(0, 12, 2))
    actual_addresses = tuple(int(row["address_octal"], 8) for row in rows)
    if actual_addresses != expected_addresses:
        raise ValueError("listing addresses are not the exact contiguous source range")
    return tuple(rows)


def _revision(root: Path) -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def observe_luminary099(
    root: Path,
    *,
    revision: str | None = None,
) -> dict[str, Any]:
    """Read exact source, listing, and binary coordinates from a built checkout."""
    root = root.resolve()
    observed_revision = revision if revision is not None else _revision(root)
    if observed_revision != PINNED_REVISION:
        raise ValueError(
            f"Virtual AGC revision {observed_revision!r} is not {PINNED_REVISION!r}"
        )

    program = root / PROGRAM_DIRECTORY
    source_lines = _source_lines(program / SOURCE_PATH)
    listing_rows = _listing_rows(program / LISTING_PATH, source_lines)
    words = tuple(
        int(word, 8)
        for row in listing_rows
        for word in row["words_octal"]
    )
    listing_bytes = agc_words_to_bytes(words)

    reference = (program / REFERENCE_BINARY_PATH).read_bytes()
    assembled = (program / ASSEMBLED_BINARY_PATH).read_bytes()
    expected_binary_size = 0o44 * WORDS_PER_BANK * BYTES_PER_WORD
    if len(reference) != expected_binary_size or len(assembled) != expected_binary_size:
        raise ValueError("Luminary binary does not have the exact Block II rope size")
    if reference != assembled:
        raise ValueError("source-assembled and independently entered binaries differ")

    bank_position = binary_bank_position(BANK)
    bank_byte_offset = bank_position * WORDS_PER_BANK * BYTES_PER_WORD
    window_byte_offset = bank_byte_offset + (FIRST_ADDRESS - 0o2000) * BYTES_PER_WORD
    window_end = window_byte_offset + len(listing_bytes)
    reference_window = reference[window_byte_offset:window_end]
    assembled_window = assembled[window_byte_offset:window_end]
    if listing_bytes != reference_window or listing_bytes != assembled_window:
        raise ValueError("listing words and addressed binary bytes differ")

    return {
        "upstream": {
            "repository": "https://github.com/virtualagc/virtualagc",
            "revision": observed_revision,
            "program": PROGRAM_DIRECTORY,
        },
        "source": {
            "path": f"{PROGRAM_DIRECTORY}/{SOURCE_PATH}",
            "first_line": SOURCE_FIRST_LINE,
            "last_line": SOURCE_LAST_LINE,
            "lines": list(source_lines),
        },
        "listing": {
            "path": f"{PROGRAM_DIRECTORY}/{LISTING_PATH}",
            "rows": list(listing_rows),
            "word_count": len(words),
            "words_octal": [f"{word:05o}" for word in words],
        },
        "binary_coordinates": {
            "bank_octal": f"{BANK:02o}",
            "first_address_octal": f"{FIRST_ADDRESS:04o}",
            "last_address_octal": f"{FIRST_ADDRESS + len(words) - 1:04o}",
            "bank_position": bank_position,
            "bank_byte_offset": bank_byte_offset,
            "window_byte_offset": window_byte_offset,
            "window_byte_count": len(listing_bytes),
        },
        "reference_binary": {
            "path": f"{PROGRAM_DIRECTORY}/{REFERENCE_BINARY_PATH}",
            "byte_count": len(reference),
            "sha256": _digest(reference),
            "window_hex": reference_window.hex(),
        },
        "assembled_binary": {
            "path": f"{PROGRAM_DIRECTORY}/{ASSEMBLED_BINARY_PATH}",
            "byte_count": len(assembled),
            "sha256": _digest(assembled),
            "window_hex": assembled_window.hex(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("virtualagc_root", type=Path)
    parser.add_argument(
        "--expected",
        type=Path,
        help="refuse unless the observation equals this committed JSON reading",
    )
    args = parser.parse_args()

    observation = observe_luminary099(args.virtualagc_root)
    if args.expected is not None:
        expected = json.loads(args.expected.read_text(encoding="utf-8"))
        if observation != expected:
            raise SystemExit("exact Luminary observation differs from expected reading")
    print(json.dumps(observation, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
