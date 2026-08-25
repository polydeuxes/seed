#!/usr/bin/env python3
"""Measure decoder read and write return distinctions."""

from __future__ import annotations

import argparse

from decoder_measurement import decoding_implementation_functions

NOT_DECODABLE = None
SAME = "same"
DIFFERENT = "different"
REFUSED = "refused"


def round_trip(codec: str, sequence: tuple[int, ...]) -> str | None:
    """Return one exact decoder read/write result."""

    given = bytes(sequence)
    try:
        read = given.decode(codec)
    except Exception:
        return NOT_DECODABLE
    try:
        written = read.encode(codec)
    except Exception:
        return REFUSED
    return SAME if written == given else DIFFERENT


def disagreements(codec: str, boundary: int = 256) -> list[tuple[int, str, str]]:
    """Return single-byte results not written back preserved."""

    found = []
    for value in range(boundary):
        result = round_trip(codec, (value,))
        if result in (SAME, NOT_DECODABLE):
            continue
        read = bytes([value]).decode(codec)
        try:
            written = read.encode(codec).hex()
        except Exception:
            written = "nothing"
        found.append((value, f"U+{ord(read):04X}" if len(read) == 1 else repr(read), written))
    return found


def survey() -> list[tuple[str, dict[str, int]]]:
    """Return each decoder function's measured results."""

    rows = []
    for name in decoding_implementation_functions():
        results: dict[str, int] = {}
        for value in range(256):
            result = round_trip(name, (value,))
            if result is not NOT_DECODABLE:
                results[result] = results.get(result, 0) + 1
        for high in range(0xC0, 0x100, 8):
            for low in range(0x80, 0x100, 8):
                result = round_trip(name, (high, low))
                if result is not NOT_DECODABLE:
                    results[result] = results.get(result, 0) + 1
        rows.append((name, results))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codec")
    parser.add_argument("--show", type=int, default=8)
    args = parser.parse_args()

    if args.codec:
        found = disagreements(args.codec)
        print(f"  {args.codec}: {len(found)} single bytes not written back preserved")
        for value, read, written in found[: args.show]:
            print(f"    {value:#04x}  reads as {read:>10}  writes {written}")
        return 0

    rows = survey()
    uneven = [(name, out) for name, out in rows if out.keys() - {SAME}]
    print(
        f"  {len(rows)} decoder functions, "
        f"{len(uneven)} of which do not write back"
    )
    print(f"  {'function':20}{'same':>7}{'different':>11}{'refused':>9}")
    for name, out in uneven:
        print(
            f"  {name:20}{out[SAME]:>7}{out[DIFFERENT]:>11}{out[REFUSED]:>9}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
