#!/usr/bin/env python3
"""Interrogate a decoder and record what it refuses.

A decoder is a witness. Asked whether it accepts an exact byte sequence it
answers, and the answer is attributed testimony about that decoder, not a fact
about the bytes. What it accepts and refuses is measurable without reading it
and without adopting its vocabulary.

**Nothing is copied.** This runs a decoder and records outcomes. No
implementation is read, transcribed, or derived from, so no implementation's
licence is engaged by what this produces. The witness here is Python's own
codec, and any other decoder answers the same questions the same way.

**Its words are not taken with its answers.** A decoder's source and
documentation carry `code point`, `continuation byte`, `leader`, `overlong`,
`scalar`. Those name why its author believes the boundaries fall where they
do. This records where they fall.

What one interrogation yields, for the codec ordinarily called UTF-8:

```text
  0x00-0x7f   128   accepted alone
  0xc2-0xdf    30   refused alone; accepted before one byte of 0x80-0xbf
  0xe0-0xef    16   refused alone and in pairs; accepted at length three
  0xf0-0xf4     5   accepted at length four
  remaining    77   refused as a first byte at every length tried
```

Five classes with exact boundaries, summing to 256. `0xc0`, `0xc1` and
`0xf5`-`0xff` fall in the refused class though a bit-pattern reading would
admit them, so the witness refuses more than a leading-bit rule predicts, and
that surplus is itself recorded rather than explained.

Usage:

    decoder_witness_harness.py --codec utf-8
    decoder_witness_harness.py --codec ascii --max-length 2
"""

from __future__ import annotations

import argparse
import codecs
import collections
from functools import lru_cache

CONTINUATION_PROBE = tuple(range(0x80, 0xC0))


def accepts(codec: str, sequence: tuple[int, ...]) -> bool:
    """Whether the witness accepts these exact bytes. Its answer, not a fact."""

    try:
        bytes(sequence).decode(codec)
    except (UnicodeDecodeError, LookupError):
        return False
    return True


def admissible_followers(codec: str, first: int) -> list[int]:
    """Every single byte this one is accepted before."""

    return [second for second in range(256) if accepts(codec, (first, second))]


def shortest_accepted_length(codec: str, first: int, max_length: int) -> int | None:
    """The shortest length at which this byte begins something accepted.

    Lengths beyond two are probed with followers drawn from the range the
    length-two probe found admissible, which is a choice this harness makes to
    keep the probe finite. A byte reported as refused was refused under that
    probe, not under every sequence.
    """

    if accepts(codec, (first,)):
        return 1
    if admissible_followers(codec, first):
        return 2
    for length in range(3, max_length + 1):
        for tail in _tails(length - 1):
            if accepts(codec, (first, *tail)):
                return length
    return None


def _tails(count: int) -> list[tuple[int, ...]]:
    """Tails probed at lengths beyond two.

    Each position is probed at both ends of the admissible range and once
    inside it rather than across all 64 values. A byte accepted only for some
    tail outside this probe is reported refused, which is a bound on the probe
    and is stated rather than hidden: an exhaustive probe at length four is
    64^3 tails for every byte it must refuse.
    """

    probe = (CONTINUATION_PROBE[0], CONTINUATION_PROBE[32], CONTINUATION_PROBE[-1])
    if count == 1:
        return [(value,) for value in probe]
    return [(value, *rest) for value in probe for rest in _tails(count - 1)]


@lru_cache(maxsize=16)
def classes(codec: str, max_length: int = 4) -> dict[object, list[int]]:
    """Bytes grouped by the outcomes the witness gave them."""

    grouped: dict[object, list[int]] = collections.defaultdict(list)
    for first in range(256):
        length = shortest_accepted_length(codec, first, max_length)
        followers = admissible_followers(codec, first) if length == 2 else []
        key = (length, (followers[0], followers[-1]) if followers else None)
        grouped[key].append(first)
    return dict(grouped)


def class_adjacency(
    codec: str, recovered: dict[object, list[int]]
) -> dict[tuple[object, object], bool]:
    """Which recovered class may be followed by which, under this witness.

    The classes are supplied, not recomputed. This measurement stands on the
    earlier one and cannot be run without it: given other classes it reports
    adjacency among those, and given none it reports nothing.

    One representative is probed per class. Two bytes the earlier measurement
    did not separate are not separated here either, which is what makes this
    a measurement over classes rather than over bytes.
    """

    representatives = {key: members[0] for key, members in recovered.items()}
    return {
        (first_key, second_key): accepts(codec, (first, second))
        for first_key, first in representatives.items()
        for second_key, second in representatives.items()
    }


def decoding_witnesses() -> list[str]:
    """Every codec on this machine that answers when handed bytes."""

    import encodings
    import pkgutil

    found = []
    for module in pkgutil.iter_modules(encodings.__path__):
        try:
            codecs.lookup(module.name)
            b"A".decode(module.name)
        except Exception:
            continue
        found.append(module.name)
    return sorted(found)


def survey() -> list[tuple[str, int, int]]:
    """Each witness, its class count, and its admissible class pairs."""

    rows = []
    for name in decoding_witnesses():
        try:
            recovered = classes(name, 4)
            adjacency = class_adjacency(name, recovered)
        except Exception:
            continue
        rows.append((name, len(recovered), sum(adjacency.values())))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codec", default="utf-8")
    parser.add_argument("--max-length", type=int, default=4)
    parser.add_argument("--survey", action="store_true")
    args = parser.parse_args()

    if args.survey:
        rows = survey()
        shapes = collections.Counter((count, pairs) for _, count, pairs in rows)
        print(f"  {len(rows)} witnesses measured at both ladders")
        print(f"  {'classes':>8}{'admissible pairs':>18}{'witnesses':>11}   example")
        for (count, pairs), many in sorted(
            shapes.items(), key=lambda item: (-item[1], item[0])
        ):
            example = next(n for n, c, p in rows if (c, p) == (count, pairs))
            print(f"  {count:>8}{pairs:>18}{many:>11}   {example}")
        return 0

    grouped = classes(args.codec, args.max_length)
    print(f"  witness: the codec named {args.codec!r}")
    print(f"  {'bytes':14}{'count':>7}{'shortest accepted':>19}   followers")
    total = 0
    for (length, followers), members in sorted(
        grouped.items(), key=lambda item: (item[0][0] is None, item[0][0])
    ):
        total += len(members)
        span = (
            f"{members[0]:#04x}-{members[-1]:#04x}"
            if len(members) > 1
            else f"{members[0]:#04x}"
        )
        shown = f"{followers[0]:#04x}-{followers[1]:#04x}" if followers else "-"
        print(f"  {span:14}{len(members):>7}{str(length):>19}   {shown}")
    print(f"  {'':14}{total:>7}   classes: {len(grouped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
