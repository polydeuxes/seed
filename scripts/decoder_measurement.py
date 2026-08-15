#!/usr/bin/env python3
"""Invoke decoder implementation functions with exact bytes."""

from __future__ import annotations

import argparse
import codecs
import warnings
from functools import lru_cache

import material_admission

# See `accepts`: a warning is not a refusal.
warnings.filterwarnings("ignore", category=DeprecationWarning, module=__name__)
warnings.filterwarnings("ignore", category=SyntaxWarning)

CONTINUATION_PROBE = tuple(range(0x80, 0xC0))


def accepts(codec: str, sequence: tuple[int, ...]) -> bool:
    """Whether the implementation function returns for these exact bytes.

    Some implementation functions emit warnings while returning -- `unicode_escape` reports
    invalid escape sequences for most of the 256 single bytes. A warning is not
    a refusal and does not revise what the implementation function returned, so it is filtered
    at import rather than read as a result. Filtering per call costs 14x,
    measured, and this runs millions of times.
    """

    try:
        bytes(sequence).decode(codec)
    except (UnicodeDecodeError, LookupError):
        return False
    return True


@lru_cache(maxsize=None)
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


@lru_cache(maxsize=None)
def first_admission(codec: str, max_byte_count: int = 4) -> dict[object, list[int]]:
    """Material admitted by equal implementation-function results."""

    same_result: dict[object, list[int]] = {}
    for first in range(256):
        byte_count = shortest_accepted_byte_count(codec, first, max_byte_count)
        followers = admissible_followers(codec, first) if byte_count == 2 else []
        key = (byte_count, (followers[0], followers[-1]) if followers else None)
        same_result.setdefault(key, []).append(first)
    return same_result


ALL = "all"
NONE = "none"
MIXED = "mixed"


def measure_material_pairs(
    codec: str, admission: dict[object, list[int]]
) -> dict[tuple[object, object], str]:
    """Whether every, no, or some exact material pair is accepted.

    The Admission is supplied, not recomputed. This Measurement stands on the
    earlier one and cannot run without it: given another Admission it reports
    ordered pairs among those, and given none it reports nothing.

    Every material pair is probed, not one representative each. A representative
    testifies only for itself: `0x80` and `0xff` have one equal result under the
    earlier measurement and behave differently here, so one material occurrence
    reporting for both would have stated `all` where the truth is `mixed`.

    `mixed` is not a failure. It is this measurement finding the earlier
    Admission insufficient for its own purpose, which is what
    :func:`admit_pairs` then acts on.
    """

    results_by_pair: dict[tuple[object, object], str] = {}
    for first_key, firsts in admission.items():
        for second_key, seconds in admission.items():
            results = {
                accepts(codec, (first, second))
                for first in firsts
                for second in seconds
            }
            results_by_pair[(first_key, second_key)] = (
                ALL if results == {True} else NONE if results == {False} else MIXED
            )
    return results_by_pair


def admit_pairs(
    codec: str, admission: dict[object, list[int]]
) -> dict[object, list[int]]:
    material = [
        byte
        for bytes_at_one_coordinate in admission.values()
        for byte in bytes_at_one_coordinate
    ]
    observed = {
        (first, second): accepts(codec, (first, second))
        for first in material
        for second in material
    }
    admitted: dict[object, list[int]] = {}
    for key, bytes_at_one_coordinate in admission.items():
        same_result: dict[object, list[int]] = {}
        for byte in bytes_at_one_coordinate:
            signature = (
                tuple(observed[byte, other] for other in material),
                tuple(observed[other, byte] for other in material),
            )
            same_result.setdefault(signature, []).append(byte)
        for index, found in enumerate(same_result.values()):
            admitted[(key, index) if len(same_result) > 1 else key] = found
    return admitted


def admit(codec: str) -> list[dict[object, list[int]]]:
    """Each Admission established by the implementation function.

    `material_admission` knows nothing of codecs. This supplies the first
    Admission and the implementation function.
    """

    admissions = material_admission.admit(
        [
            tuple(bytes_at_one_coordinate)
            for bytes_at_one_coordinate in first_admission(codec, 4).values()
        ],
        lambda first, second: accepts(codec, (first, second)),
    )
    return [
        {index: list(material) for index, material in enumerate(admission)}
        for admission in admissions
    ]


def decoding_implementation_functions() -> list[str]:
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
    """Admission counts for each decoder implementation function."""

    rows = []
    for name in decoding_implementation_functions():
        try:
            admissions = admit(name)
        except Exception:
            continue
        rows.append(
            (name, len(admissions[0]), len(admissions[-1]), len(admissions))
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
        admission_counts: dict[int, int] = {}
        for _, _, _, many in rows:
            admission_counts[many] = admission_counts.get(many, 0) + 1
        print(f"  {len(rows)} implementation functions")
        print(f"  {'count':>6}{'functions':>11}   example, first Admission to last")
        for admission_count, many in sorted(admission_counts.items()):
            name, first, last, _ = next(
                row for row in rows if row[3] == admission_count
            )
            print(
                f"  {admission_count:>6}{many:>11}   {name:<18} {first} -> {last}"
            )
        return 0

    admitted = first_admission(args.codec, args.max_byte_count)
    print(f"  implementation function: the codec named {args.codec!r}")
    print(f"  {'bytes':14}{'count':>7}{'shortest accepted':>19}   followers")
    total = 0
    for (byte_count, followers), material in sorted(
        admitted.items(), key=lambda item: (item[0][0] is None, item[0][0])
    ):
        total += len(material)
        span = (
            f"{material[0]:#04x}-{material[-1]:#04x}"
            if len(material) > 1
            else f"{material[0]:#04x}"
        )
        shown = f"{followers[0]:#04x}-{followers[1]:#04x}" if followers else "-"
        print(f"  {span:14}{len(material):>7}{str(byte_count):>19}   {shown}")
    print(f"  {'':14}{total:>7}   distinct results: {len(admitted)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
