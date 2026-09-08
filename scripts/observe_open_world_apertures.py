"""Recover source-selected substitution apertures from external material.

This observer does not read the Book, the witness grammar, a dictionary, or a
list of expected words.  For each independently bounded 300-line source
window it:

1. divides the exact line population into four consecutive scopes;
2. enumerates every byte value occurring in every scope;
3. lets each enumerated byte value deboundary exact source spans;
4. groups a middle span by its exact preceding and following spans; and
5. preserves every frame carrying more than one middle span; and
6. separately preserves the subset in which at least two middle spans recur.

The four-scope division and the one-byte aperture resolution are observer
choices.  The separator, frame, occupants, and their source positions are not.
The output is a blind artifact beneath /tmp.  A separate reporter may compare
it with human vocabulary or Seed's current grammar only after its digest is
fixed.

Usage:
    .venv/bin/python scripts/observe_open_world_apertures.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import time


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
OUTPUT = Path("/tmp/seed_open_world_apertures_blind.json")
LINE_COUNT = 300
SCOPE_COUNT = 4

# These are independently bounded testimony populations.  The names classify
# sources for the later reporter; they do not affect blind measurement.
SOURCES = (
    ("prose_austen_pride.txt", 6000, "unlabeled_natural"),
    ("prose_dickens_copperfield.txt", 6000, "unlabeled_natural"),
    ("prose_franklin_autobiog.txt", 6000, "unlabeled_natural"),
    ("prose_emerson_essays.txt", 6000, "unlabeled_natural"),
    ("prose_hume_enquiry.txt", 6000, "unlabeled_natural"),
    ("grammar_goold_brown.txt", 6000, "labeled_grammar"),
    ("grammar_kittredge.txt", 6000, "labeled_grammar"),
    ("webster_dictionary.txt", 6000, "lexical_testimony"),
    ("roget_thesaurus.txt", 6000, "lexical_testimony"),
    ("french_les_miserables.txt", 6000, "external_language_french"),
    ("german_goethe_faust.txt", 6000, "external_language_german"),
    ("german_grimm_maerchen.txt", 6000, "external_language_german"),
    ("spanish_don_quijote.txt", 6000, "external_language_spanish"),
    ("latin_vulgate.txt", 6000, "external_language_latin"),
    ("greek_xenophon_anabasis.txt", 6000, "external_language_greek"),
    ("russian_mental_arithmetic.txt", 1800, "external_language_russian"),
    ("chinese_shanhaijing.txt", 1800, "external_language_chinese"),
)


def _digest(value: bytes) -> str:
    return sha256(value).hexdigest()


def _window(path: Path, first_line: int) -> tuple[bytes, tuple[int, ...]]:
    selected = []
    with path.open("rb") as source:
        for line_number, line in enumerate(source):
            if line_number < first_line:
                continue
            if line_number >= first_line + LINE_COUNT:
                break
            selected.append(line)
    if len(selected) != LINE_COUNT:
        raise ValueError(f"{path.name} does not carry the exact 300-line window")
    starts = []
    position = 0
    for line in selected:
        starts.append(position)
        position += len(line)
    return b"".join(selected), tuple(starts)


def _scope_materials(material: bytes, line_starts: tuple[int, ...]) -> tuple[bytes, ...]:
    scope_size = LINE_COUNT // SCOPE_COUNT
    boundaries = tuple(line_starts[position] for position in range(0, LINE_COUNT, scope_size))
    return tuple(
        material[start : boundaries[index + 1] if index + 1 < len(boundaries) else len(material)]
        for index, start in enumerate(boundaries)
    )


def _spans(material: bytes, separator: int) -> tuple[tuple[int, int, bytes], ...]:
    # ``bytes.find`` performs the same exact scan in bounded C code.  Iterating
    # the complete material once in Python for every possible separator made
    # the aperture inventory, rather than its surviving findings, dominate the
    # experiment.
    needle = bytes((separator,))
    found = []
    position = material.find(needle)
    while position >= 0:
        found.append(position)
        position = material.find(needle, position + 1)
    positions = (-1, *found, len(material))
    return tuple(
        (positions[index] + 1, positions[index + 1], material[positions[index] + 1 : positions[index + 1]])
        for index in range(len(positions) - 1)
    )


def _material_reference(
    materials: dict[str, dict[str, object]], value: bytes
) -> str:
    identity = _digest(value)
    found = materials.get(identity)
    rendered = {
        "byte_count": len(value),
        "hex": value.hex(),
    }
    if found is not None and found != rendered:
        raise AssertionError("material digest collision")
    materials[identity] = rendered
    return identity


def _observe_source(path: Path, first_line: int, population: str) -> dict[str, object]:
    begun = time.perf_counter()
    material, line_starts = _window(path, first_line)
    scopes = _scope_materials(material, line_starts)
    separators = sorted(set.intersection(*(set(scope) for scope in scopes)))
    materials: dict[str, dict[str, object]] = {}
    deboundaryer_results = []

    for separator in separators:
        deboundaryer_begun = time.perf_counter()
        spans = _spans(material, separator)
        frames: dict[tuple[bytes, bytes], dict[bytes, list[tuple[int, int]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for position in range(1, len(spans) - 1):
            left = spans[position - 1][2]
            start, end, occupant = spans[position]
            right = spans[position + 1][2]
            frames[(left, right)][occupant].append((start, end))

        distinct_substitution_frames = 0
        substitution_frames = []
        recurrent_frames = []
        maximum_distinct_occupants = 0
        maximum_recurrent_occupants = 0
        for (left, right), occupants in frames.items():
            if len(occupants) > 1:
                distinct_substitution_frames += 1
                maximum_distinct_occupants = max(maximum_distinct_occupants, len(occupants))
                substitution_frames.append(
                    {
                        "left_material": _material_reference(materials, left),
                        "right_material": _material_reference(materials, right),
                        "occupants": [
                            {
                                "material": _material_reference(materials, occupant),
                                "source_ranges": [list(found) for found in positions],
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
                            "source_ranges": [list(found) for found in positions],
                        }
                        for occupant, positions in sorted(recurrent.items())
                    ],
                }
            )

        deboundaryer_results.append(
            {
                "separator_byte": separator,
                "separator_hex": bytes((separator,)).hex(),
                "occurrence_count": material.count(bytes((separator,))),
                "span_count": len(spans),
                "distinct_span_count": len({span[2] for span in spans}),
                "substitution_frame_count": distinct_substitution_frames,
                "recurrent_substitution_frame_count": len(recurrent_frames),
                "maximum_distinct_occupants": maximum_distinct_occupants,
                "maximum_recurrent_occupants": maximum_recurrent_occupants,
                "wall_seconds": time.perf_counter() - deboundaryer_begun,
                "substitution_frames": substitution_frames,
                "recurrent_substitution_frames": recurrent_frames,
            }
        )

    return {
        "source": path.relative_to(ROOT).as_posix(),
        "population": population,
        "first_line": first_line,
        "line_count": LINE_COUNT,
        "byte_count": len(material),
        "material_sha256": _digest(material),
        "scope_count": SCOPE_COUNT,
        "enumerated_separator_count": len(separators),
        "materials": materials,
        "deboundaryers": deboundaryer_results,
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
        slowest = max(observed["deboundaryers"], key=lambda item: item["wall_seconds"])
        print(
            f"{name:38} {observed['byte_count']:7} bytes  "
            f"{observed['enumerated_separator_count']:3} apertures  "
            f"{sum(item['recurrent_substitution_frame_count'] for item in observed['deboundaryers']):5} recurrent frames  "
            f"{observed['wall_seconds']:.3f}s"
        )
        print(
            f"  slowest aperture: byte {slowest['separator_byte']:3}  "
            f"{slowest['wall_seconds']:.3f}s  "
            f"{slowest['span_count']} spans  "
            f"{slowest['recurrent_substitution_frame_count']} recurrent frames"
        )

    artifact = {
        "observer": "source-selected one-byte apertures and recurrent substitution frames",
        "observer_choices": {
            "source_windows": "the established exact 300-line windows beginning at the recorded line",
            "scope_division": "four equal consecutive 75-line scopes",
            "aperture_resolution": "each one-byte value recurring in every scope",
            "substitution": "one exact neighboring-span frame carries at least two distinct middle materials",
            "recurrent_substitution": "at least two of one frame's distinct middle materials each recur",
        },
        "sources": sources,
        "wall_seconds": time.perf_counter() - begun,
    }
    encoded = json.dumps(artifact, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    arguments.output.write_bytes(encoded)
    print(f"\nartifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"complete wall seconds: {artifact['wall_seconds']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
