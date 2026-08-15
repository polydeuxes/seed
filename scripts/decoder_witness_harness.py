#!/usr/bin/env python3
"""Interrogate a decoder and record what it refuses.

A decoder is a witness. Asked whether it accepts an exact byte sequence it
returns a result, and the result is attributed testimony about that decoder, not a fact
about the bytes. What it accepts and refuses is measurable without read it
and without adopting its vocabulary.

**Nothing is copied.** This runs a decoder and records results. No
implementation is read, transcribed, or derived from, so no implementation's
licence is engaged by what this produces. The witness here is Python's own
codec, and any other decoder returns results for the same probes.

**Its words are not taken with its results.** A decoder's source and
documentation carry `code point`, `continuation byte`, `leader`, `overlong`,
`scalar`. Those name why its author believes the boundaries fall where they
do. This records where they fall.

What one interrogation yields, for the codec ordinarily called UTF-8:

```text
  0x00-0x7f   128   accepted alone
  0xc2-0xdf    30   refused alone; accepted before one byte of 0x80-0xbf
  0xe0-0xef    16   refused alone and in pairs; accepted at three bytes
  0xf0-0xf4     5   accepted at four bytes
  remaining    77   refused as a first byte at every byte count tried
```

Five exact material tuples, each sharing one equal result and together summing
to 256. `0xc0`, `0xc1` and `0xf5`-`0xff` share the refused result though a bit-pattern read would
admit them, so the witness refuses more than a leading-bit rule predicts, and
that surplus is itself recorded rather than explained.

Usage:

    decoder_witness_harness.py --codec utf-8
    decoder_witness_harness.py --codec ascii --max-byte-count 2
"""

from __future__ import annotations

import argparse
import codecs
import collections
import warnings
from functools import lru_cache

import refinement_climb

# See `accepts`: a warning is not a refusal.
warnings.filterwarnings("ignore", category=DeprecationWarning, module=__name__)
warnings.filterwarnings("ignore", category=SyntaxWarning)

CONTINUATION_PROBE = tuple(range(0x80, 0xC0))


def accepts(codec: str, sequence: tuple[int, ...]) -> bool:
    """Whether the witness accepts these exact bytes. Its result, not a fact.

    Some witnesses emit warnings while returning -- `unicode_escape` reports
    invalid escape sequences for most of the 256 single bytes. A warning is not
    a refusal and does not revision what the witness returned, so it is filtered
    at import rather than read as a result. Filtering per call costs 14x,
    measured, and this runs millions of times.
    """

    try:
        bytes(sequence).decode(codec)
    except (UnicodeDecodeError, LookupError):
        return False
    return True


def admissible_followers(codec: str, first: int) -> list[int]:
    """Every single byte this one is accepted before."""

    return [second for second in range(256) if accepts(codec, (first, second))]


def shortest_accepted_byte_count(
    codec: str, first: int, max_byte_count: int
) -> int | None:
    """The smallest byte count at which this byte begins something accepted.

    Byte counts beyond two are probed with followers drawn from the range the
    two-byte probe found admissible, which is a coordinate this harness fixes to
    keep the probe finite. A byte reported as refused was refused under that
    probe, not under every sequence.
    """

    if accepts(codec, (first,)):
        return 1
    if admissible_followers(codec, first):
        return 2
    for byte_count in range(3, max_byte_count + 1):
        for tail in _tails(byte_count - 1):
            if accepts(codec, (first, *tail)):
                return byte_count
    return None


def _tails(count: int) -> list[tuple[int, ...]]:
    """Tails probed beyond two bytes.

    Each position is probed at both ends of the admissible range and once
    inside it rather than across all 64 values. A byte accepted only for some
    tail outside this probe is reported refused, which is a bound on the probe
    and is stated rather than hidden: an exhaustive probe at four bytes is
    64^3 tails for every byte it must refuse.
    """

    probe = (CONTINUATION_PROBE[0], CONTINUATION_PROBE[32], CONTINUATION_PROBE[-1])
    if count == 1:
        return [(value,) for value in probe]
    return [(value, *rest) for value in probe for rest in _tails(count - 1)]


@lru_cache(maxsize=16)
def material_locality(codec: str, max_byte_count: int = 4) -> dict[object, list[int]]:
    """Bytes grouped by the results the witness gave them."""

    grouped: dict[object, list[int]] = collections.defaultdict(list)
    for first in range(256):
        byte_count = shortest_accepted_byte_count(codec, first, max_byte_count)
        followers = admissible_followers(codec, first) if byte_count == 2 else []
        key = (byte_count, (followers[0], followers[-1]) if followers else None)
        grouped[key].append(first)
    return dict(grouped)


ALL = "all"
NONE = "none"
MIXED = "mixed"


def measure_material_pairs(
    codec: str, read: dict[object, list[int]]
) -> dict[tuple[object, object], str]:
    """Whether every, no, or some exact material pair is accepted.

    The material Locality is supplied, not recomputed. This measurement stands on the
    earlier one and cannot run without it: given another material Locality it reports
    ordered pairs among those, and given none it reports nothing.

    Every material pair is probed, not one representative each. A representative
    testifies only for itself: `0x80` and `0xff` have one equal result under the
    earlier measurement and behave differently here, so one material occurrence
    reporting for both would have stated `all` where the truth is `mixed`.

    `mixed` is not a failure. It is this measurement finding the earlier
    material Locality insufficient for its own purpose, which is what
    :func:`refine` then acts on.
    """

    results_by_pair: dict[tuple[object, object], str] = {}
    for first_key, firsts in read.items():
        for second_key, seconds in read.items():
            results = {
                accepts(codec, (first, second))
                for first in firsts
                for second in seconds
            }
            results_by_pair[(first_key, second_key)] = (
                ALL if results == {True} else NONE if results == {False} else MIXED
            )
    return results_by_pair


def refine(codec: str, read: dict[object, list[int]]) -> dict[object, list[int]]:
    material = [
        byte
        for bytes_at_one_coordinate in read.values()
        for byte in bytes_at_one_coordinate
    ]
    observed = {
        (first, second): accepts(codec, (first, second))
        for first in material
        for second in material
    }
    refined: dict[object, list[int]] = {}
    for key, bytes_at_one_coordinate in read.items():
        grouped: dict[object, list[int]] = collections.defaultdict(list)
        for byte in bytes_at_one_coordinate:
            signature = (
                tuple(observed[byte, other] for other in material),
                tuple(observed[other, byte] for other in material),
            )
            grouped[signature].append(byte)
        for index, split in enumerate(grouped.values()):
            refined[(key, index) if len(grouped) > 1 else key] = split
    return refined


def climb(codec: str) -> list[dict[object, list[int]]]:
    """Each material Locality through the one that stops moving.

    The mechanism is `refinement_climb`, which knows nothing of codecs. What
    this supplies is the first material Locality and the witness.
    """

    localities = refinement_climb.climb(
        [
            tuple(bytes_at_one_coordinate)
            for bytes_at_one_coordinate in material_locality(codec, 4).values()
        ],
        lambda first, second: accepts(codec, (first, second)),
    )
    return [
        {index: list(material) for index, material in enumerate(locality)}
        for locality in localities
    ]


def decoding_witnesses() -> list[str]:
    """Every codec on this machine that returns when handed bytes."""

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


def survey() -> list[tuple[str, int, int, int]]:
    """Each witness: its first material Locality count, its last, and total.

    Grouping witnesses by counts is not grouping them by shape. Two witnesses
    with the same number of distinct results and admissible pairs may relate them
    differently, and nothing here compares those relations.
    """

    rows = []
    for name in decoding_witnesses():
        try:
            localities = climb(name)
        except Exception:
            continue
        rows.append(
            (name, len(localities[0]), len(localities[-1]), len(localities))
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codec", default="utf-8")
    parser.add_argument("--max-byte-count", type=int, default=4)
    parser.add_argument("--survey", action="store_true")
    args = parser.parse_args()

    if args.survey:
        rows = survey()
        heights = collections.Counter(many for _, _, _, many in rows)
        print(f"  {len(rows)} witnesses climbed")
        print(f"  {'count':>6}{'witnesses':>11}   example, first Locality to last")
        for locality_count, many in sorted(heights.items()):
            name, first, last, _ = next(
                row for row in rows if row[3] == locality_count
            )
            print(
                f"  {locality_count:>6}{many:>11}   {name:<18} {first} -> {last}"
            )
        return 0

    grouped = material_locality(args.codec, args.max_byte_count)
    print(f"  witness: the codec named {args.codec!r}")
    print(f"  {'bytes':14}{'count':>7}{'shortest accepted':>19}   followers")
    total = 0
    for (byte_count, followers), material in sorted(
        grouped.items(), key=lambda item: (item[0][0] is None, item[0][0])
    ):
        total += len(material)
        span = (
            f"{material[0]:#04x}-{material[-1]:#04x}"
            if len(material) > 1
            else f"{material[0]:#04x}"
        )
        shown = f"{followers[0]:#04x}-{followers[1]:#04x}" if followers else "-"
        print(f"  {span:14}{len(material):>7}{str(byte_count):>19}   {shown}")
    print(f"  {'':14}{total:>7}   distinct results: {len(grouped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
