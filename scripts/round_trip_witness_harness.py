#!/usr/bin/env python3
"""Ask a witness to take back what it gave, and record whether it can.

A codec returns results for two different probes. Handed bytes it says what it makes of
them; handed that back it says which bytes it would write. Those are two
testimonies, and this records where they disagree. Neither is corrected by the
other here: a disagreement is a finding about the pair, not a fault in either.

Four results, and the last three are all things a decoder alone cannot say:

```text
  not decodable   the witness refused the bytes; nothing was asked of it
  same            it wrote back the bytes it was given
  different       it wrote back other bytes for what it read
  refused         it read the bytes and will not write anything for them
```

Measured across the codecs on one machine, 10 of 104 return something other
than `same` for some input they accept:

```text
  mac_arabic   0x20 and 0xa0 both read as U+0020; it writes 0xa0
  cp875        0x3f, 0xdc and 0xe1 all read as U+001A; it writes 0xfd,
               which is none of them
  idna         0x2e reads as U+002E, and it writes nothing for U+002E
```

So being readable and being written back the same way are separate
properties, and a witness may hold the first without the second.

Usage:

    round_trip_witness_harness.py
    round_trip_witness_harness.py --codec mac_arabic --show 6
"""

from __future__ import annotations

import argparse
import collections

from decoder_witness_harness import decoding_witnesses

NOT_DECODABLE = None
SAME = "same"
DIFFERENT = "different"
REFUSED = "refused"


def round_trip(codec: str, sequence: tuple[int, ...]) -> str | None:
    """What the witness writes back for what it read, or nothing if it refused."""

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


def disagreements(codec: str, limit: int = 256) -> list[tuple[int, str, str]]:
    """Each single byte the witness reads but does not write back preserved."""

    found = []
    for value in range(limit):
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


def survey() -> list[tuple[str, collections.Counter]]:
    """Every witness and its results for single bytes and some pairs."""

    rows = []
    for name in decoding_witnesses():
        results: collections.Counter = collections.Counter()
        for value in range(256):
            result = round_trip(name, (value,))
            if result is not NOT_DECODABLE:
                results[result] += 1
        for high in range(0xC0, 0x100, 8):
            for low in range(0x80, 0x100, 8):
                result = round_trip(name, (high, low))
                if result is not NOT_DECODABLE:
                    results[result] += 1
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
    print(f"  {len(rows)} witnesses, {len(uneven)} of which do not write back")
    print(f"  {'witness':20}{'same':>7}{'different':>11}{'refused':>9}")
    for name, out in uneven:
        print(
            f"  {name:20}{out[SAME]:>7}{out[DIFFERENT]:>11}{out[REFUSED]:>9}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
