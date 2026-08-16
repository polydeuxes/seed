#!/usr/bin/env python3
"""Compare Admission results from distinct implementation functions."""

from __future__ import annotations

import argparse
from functools import lru_cache

import material_admission
from decoder_measurement import accepts, first_admission, decoding_implementation_functions

Admission = frozenset


@lru_cache(maxsize=None)
def final_admission(codec: str) -> Admission:
    """The final Admission for one implementation function."""

    read = first_admission(codec, 4)
    admissions = material_admission.admit(
        [tuple(material) for material in read.values()],
        lambda first, second: accepts(codec, (first, second)),
    )
    return frozenset(frozenset(material) for material in admissions[-1])


@lru_cache(maxsize=1)
def admissions() -> dict[Admission, list[str]]:
    """Each distinct final Admission and its implementation functions."""

    same_result: dict[Admission, list[str]] = {}
    for name in decoding_implementation_functions():
        try:
            same_result.setdefault(final_admission(name), []).append(name)
        except Exception:
            continue
    return same_result


def compare_admissions(found: dict[Admission, list[str]]) -> dict[str, int]:

    keys = list(found)
    above: dict[int, int] = {}
    below: dict[int, int] = {}
    preservation_pairs = 0
    for i, first in enumerate(keys):
        for j in range(i + 1, len(keys)):
            second = keys[j]
            first_preserves_second = material_admission.preserves(first, second)
            second_preserves_first = material_admission.preserves(second, first)
            if first_preserves_second:
                below[i] = below.get(i, 0) + 1
                above[j] = above.get(j, 0) + 1
            if second_preserves_first:
                below[j] = below.get(j, 0) + 1
                above[i] = above.get(i, 0) + 1
            preservation_pairs += first_preserves_second or second_preserves_first
    return {
        "admissions": len(keys),
        "not_preserved_by_another": sum(
            1 for i in range(len(keys)) if above.get(i, 0) == 0
        ),
        "preserves_no_other": sum(
            1 for i in range(len(keys)) if below.get(i, 0) == 0
        ),
        "preservation_pairs": preservation_pairs,
        "pair_count": len(keys) * (len(keys) - 1) // 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    found = admissions()
    counted = compare_admissions(found)
    implementation_functions = sum(len(names) for names in found.values())

    print(
        f"  {implementation_functions} implementation functions -> "
        f"{counted['admissions']} distinct material admissions"
    )
    print(
        "  material admissions not preserved by another: "
        f"{counted['not_preserved_by_another']}"
    )
    print(
        "  material admissions preserving no other: "
        f"{counted['preserves_no_other']}"
    )
    print(
        f"  preservation pairs: {counted['preservation_pairs']} of "
        f"{counted['pair_count']}"
        f"  ({counted['preservation_pairs'] / counted['pair_count'] * 100:.0f}%)"
    )

    keys = tuple(found)
    admissions = material_admission.admit(
        material_admission.admission_by(len, keys), preserves
    )
    print(
        "\n  Admission results under complete comparison: "
        f"{len(admissions)}"
    )
    print(
        f"  counts {material_admission.admission_counts(admissions)[:6]} ... {material_admission.admission_counts(admissions)[-1]}"
    )
    print(
        "  material not distinguished: "
        f"{len(material_admission.not_distinguished(admissions))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
