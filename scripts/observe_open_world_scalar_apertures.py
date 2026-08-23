"""Repeat the blind aperture observer at exact Unicode-scalar resolution.

The byte observer is exact about transport material but can place an aperture
inside a multibyte UTF-8 representation.  This independent control decodes each
exact source window as UTF-8 without normalization or case folding, enumerates
every scalar recurring in all four scopes, and performs the same neighboring-
span substitution measurement.

Usage:
    .venv/bin/python scripts/observe_open_world_scalar_apertures.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import time

from observe_open_world_apertures import (
    CORPUS,
    LINE_COUNT,
    SCOPE_COUNT,
    SOURCES,
    _window,
)


OUTPUT = Path("/tmp/seed_open_world_scalar_apertures_blind.json")


def _digest(value: bytes) -> str:
    return sha256(value).hexdigest()


def _scope_materials(lines: tuple[str, ...]) -> tuple[str, ...]:
    scope_size = LINE_COUNT // SCOPE_COUNT
    return tuple(
        "".join(lines[start : start + scope_size])
        for start in range(0, LINE_COUNT, scope_size)
    )


def _spans(material: str, separator: str) -> tuple[tuple[int, int, str], ...]:
    found = []
    position = material.find(separator)
    while position >= 0:
        found.append(position)
        position = material.find(separator, position + 1)
    positions = (-1, *found, len(material))
    return tuple(
        (
            positions[index] + 1,
            positions[index + 1],
            material[positions[index] + 1 : positions[index + 1]],
        )
        for index in range(len(positions) - 1)
    )


def _material_reference(
    materials: dict[str, dict[str, object]], value: str
) -> str:
    encoded = value.encode("utf-8")
    identity = _digest(encoded)
    found = materials.get(identity)
    rendered = {
        "scalar_count": len(value),
        "byte_count": len(encoded),
        "utf8_hex": encoded.hex(),
    }
    if found is not None and found != rendered:
        raise AssertionError("material digest collision")
    materials[identity] = rendered
    return identity


def _observe_source(path: Path, first_line: int, population: str) -> dict[str, object]:
    begun = time.perf_counter()
    exact_bytes, _byte_line_starts = _window(path, first_line)
    exact_lines = tuple(
        line.decode("utf-8") for line in exact_bytes.splitlines(keepends=True)
    )
    if len(exact_lines) != LINE_COUNT:
        raise ValueError(f"{path.name} does not preserve 300 decoded lines")
    material = "".join(exact_lines)
    scopes = _scope_materials(exact_lines)
    separators = sorted(set.intersection(*(set(scope) for scope in scopes)))
    materials: dict[str, dict[str, object]] = {}
    delimiter_results = []

    for separator in separators:
        delimiter_begun = time.perf_counter()
        spans = _spans(material, separator)
        frames: dict[tuple[str, str], dict[str, list[tuple[int, int]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for position in range(1, len(spans) - 1):
            left = spans[position - 1][2]
            start, end, occupant = spans[position]
            right = spans[position + 1][2]
            frames[(left, right)][occupant].append((start, end))

        substitution_frames = []
        recurrent_frames = []
        maximum_distinct_occupants = 0
        maximum_recurrent_occupants = 0
        for (left, right), occupants in frames.items():
            if len(occupants) > 1:
                maximum_distinct_occupants = max(maximum_distinct_occupants, len(occupants))
                substitution_frames.append(
                    {
                        "left_material": _material_reference(materials, left),
                        "right_material": _material_reference(materials, right),
                        "occupants": [
                            {
                                "material": _material_reference(materials, occupant),
                                "source_scalar_ranges": [list(found) for found in positions],
                            }
                            for occupant, positions in sorted(occupants.items())
                        ],
                    }
                )
            recurrent = {
                occupant: tuple(positions)
                for occupant, positions in occupants.items()
                if len(positions) > 1
            }
            if len(recurrent) < 2:
                continue
            maximum_recurrent_occupants = max(maximum_recurrent_occupants, len(recurrent))
            recurrent_frames.append(
                {
                    "left_material": _material_reference(materials, left),
                    "right_material": _material_reference(materials, right),
                    "occupants": [
                        {
                            "material": _material_reference(materials, occupant),
                            "source_scalar_ranges": [list(found) for found in positions],
                        }
                        for occupant, positions in sorted(recurrent.items())
                    ],
                }
            )

        delimiter_results.append(
            {
                "separator_scalar": separator,
                "separator_codepoint": ord(separator),
                "separator_utf8_hex": separator.encode("utf-8").hex(),
                "occurrence_count": material.count(separator),
                "span_count": len(spans),
                "distinct_span_count": len({span[2] for span in spans}),
                "substitution_frame_count": len(substitution_frames),
                "recurrent_substitution_frame_count": len(recurrent_frames),
                "maximum_distinct_occupants": maximum_distinct_occupants,
                "maximum_recurrent_occupants": maximum_recurrent_occupants,
                "wall_seconds": time.perf_counter() - delimiter_begun,
                "substitution_frames": substitution_frames,
                "recurrent_substitution_frames": recurrent_frames,
            }
        )

    return {
        "source": path.relative_to(CORPUS.parent).as_posix(),
        "population": population,
        "first_line": first_line,
        "line_count": LINE_COUNT,
        "byte_count": len(exact_bytes),
        "scalar_count": len(material),
        "material_sha256": _digest(exact_bytes),
        "scope_count": SCOPE_COUNT,
        "enumerated_separator_count": len(separators),
        "materials": materials,
        "delimiters": delimiter_results,
        "wall_seconds": time.perf_counter() - begun,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    begun = time.perf_counter()
    sources = []
    for name, first_line, population in SOURCES:
        observed = _observe_source(CORPUS / name, first_line, population)
        sources.append(observed)
        slowest = max(observed["delimiters"], key=lambda item: item["wall_seconds"])
        print(
            f"{name:38} {observed['scalar_count']:7} scalars  "
            f"{observed['enumerated_separator_count']:3} apertures  "
            f"{sum(item['recurrent_substitution_frame_count'] for item in observed['delimiters']):5} recurrent frames  "
            f"{observed['wall_seconds']:.3f}s"
        )
        print(
            f"  slowest aperture: U+{slowest['separator_codepoint']:04X}  "
            f"{slowest['wall_seconds']:.3f}s  {slowest['span_count']} spans  "
            f"{slowest['recurrent_substitution_frame_count']} recurrent frames"
        )

    artifact = {
        "observer": "source-selected Unicode-scalar apertures and substitution frames",
        "observer_choices": {
            "source_windows": "the established exact 300-line windows beginning at the recorded line",
            "scope_division": "four equal consecutive 75-line scopes",
            "aperture_resolution": "each exact Unicode scalar recurring in every scope after strict UTF-8 decoding",
            "normalization": "none",
            "case_folding": "none",
            "substitution": "one exact neighboring-span frame carries at least two distinct middle materials",
            "recurrent_substitution": "at least two of one frame's distinct middle materials each recur",
        },
        "sources": sources,
        "wall_seconds": time.perf_counter() - begun,
    }
    encoded = json.dumps(
        artifact, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    arguments.output.write_bytes(encoded)
    print(f"\nartifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"complete wall seconds: {artifact['wall_seconds']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
