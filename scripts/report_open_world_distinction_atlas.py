"""Report a frozen open-world aperture artifact against later testimony.

The blind artifact is produced by ``observe_open_world_apertures.py`` without
reading any expected word or Seed coordinate.  This reporter runs afterward.
It may therefore ask where ordinary external words and current Seed spellings
occur, but a spelling match never counts as a physiology match.

Usage:
    .venv/bin/python scripts/report_open_world_distinction_atlas.py
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re

from observe_open_world_apertures import _window


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = Path("/tmp/seed_open_world_apertures_blind.json")
GRAMMAR = ROOT / "book_of_seed" / "witness_grammar.json"
# These words are queried only after the blind artifact has a fixed digest.
# They are testimony proposed by the operator/curator, not discovery targets.
POSTHOC_FAMILIES = {
    "established-place vocabulary": (
        "standing", "root", "head", "origin", "anchor",
    ),
    "relation-expression vocabulary": (
        "is", "has", "becomes", "contains", "precedes", "resembles",
    ),
    "presentation vocabulary": (
        "emission", "projection", "representation", "express",
        "presentation", "rendering",
    ),
    "modification vocabulary": (
        "adjective", "adverb", "modifier", "attribute",
    ),
}


def _render(value: bytes, boundary: int = 56) -> str:
    rendered = value.decode("utf-8", "backslashreplace")
    if len(rendered) > boundary:
        rendered = rendered[: boundary - 1] + "…"
    return repr(rendered)


def _material(source: dict, reference: str) -> bytes:
    return bytes.fromhex(source["materials"][reference]["hex"])


def _walk_words(value, found: Counter[str]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            found.update(word.lower() for word in re.findall(r"[A-Za-z]+", key))
            _walk_words(nested, found)
    elif isinstance(value, list):
        for nested in value:
            _walk_words(nested, found)
    elif isinstance(value, str):
        found.update(word.lower() for word in re.findall(r"[A-Za-z]+", value))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=ARTIFACT)
    parser.add_argument("--atlas-size", type=int, default=24)
    arguments = parser.parse_args()

    encoded = arguments.artifact.read_bytes()
    artifact = json.loads(encoded)
    artifact_digest = sha256(encoded).hexdigest()
    print(f"  frozen blind artifact: {arguments.artifact}")
    print(f"  sha256: {artifact_digest}")
    print(f"  blind wall seconds: {artifact['wall_seconds']:.3f}\n")

    frames: dict[tuple[int, bytes, bytes], list[dict]] = defaultdict(list)
    role_occurrences: dict[bytes, Counter[str]] = defaultdict(Counter)
    role_sources: dict[bytes, set[str]] = defaultdict(set)
    for source in artifact["sources"]:
        for deboundaryer in source["deboundaryers"]:
            for frame in deboundaryer["substitution_frames"]:
                left = _material(source, frame["left_material"])
                right = _material(source, frame["right_material"])
                key = (deboundaryer["separator_byte"], left, right)
                occupants = tuple(
                    _material(source, occupant["material"])
                    for occupant in frame["occupants"]
                )
                frames[key].append(
                    {
                        "source": source["source"],
                        "population": source["population"],
                        "occupants": occupants,
                    }
                )
                for role, values in (("left", (left,)), ("right", (right,)), ("occupant", occupants)):
                    for value in values:
                        role_occurrences[value][role] += 1
                        role_sources[value].add(source["source"])

    cross_source = [
        (key, occurrences)
        for key, occurrences in frames.items()
        if len({occurrence["source"] for occurrence in occurrences}) > 1
    ]
    cross_population = [
        (key, occurrences)
        for key, occurrences in cross_source
        if len({occurrence["population"] for occurrence in occurrences}) > 1
    ]
    print(f"  exact substitution-frame shapes: {len(frames)}")
    print(f"  carried by more than one source: {len(cross_source)}")
    print(f"  carried by more than one testimony population: {len(cross_population)}\n")

    ordered = sorted(
        cross_source,
        key=lambda item: (
            -len({occurrence["population"] for occurrence in item[1]}),
            -len({occurrence["source"] for occurrence in item[1]}),
            -len({occupant for occurrence in item[1] for occupant in occurrence["occupants"]}),
            item[0],
        ),
    )
    print("  small blind atlas (ordered only by population/source coverage):\n")
    for position, ((separator, left, right), occurrences) in enumerate(
        ordered[: arguments.atlas_size], start=1
    ):
        populations = sorted({occurrence["population"] for occurrence in occurrences})
        sources = sorted({occurrence["source"] for occurrence in occurrences})
        occupants = {occupant for occurrence in occurrences for occupant in occurrence["occupants"]}
        print(f"  A{position:03}")
        print(
            f"    exact frame: {_render(left)}  <{_render(bytes((separator,)))}>  "
            f"_  <{_render(bytes((separator,)))}>  {_render(right)}"
        )
        print(f"    source count: {len(sources)}")
        print(f"    testimony populations: {', '.join(populations)}")
        print(f"    distinct exact occupants: {len(occupants)}")
        rendered_occupants = ", ".join(_render(value, 28) for value in sorted(occupants)[:12])
        print(f"    occupants (first 12 by byte order): {rendered_occupants}\n")

    grammar_words: Counter[str] = Counter()
    _walk_words(json.loads(GRAMMAR.read_text(encoding="utf-8")), grammar_words)
    posthoc_words = tuple(
        word.encode()
        for words in POSTHOC_FAMILIES.values()
        for word in words
    )
    testimony_pattern = re.compile(
        rb"(?<![A-Za-z])(" + rb"|".join(map(re.escape, posthoc_words))
        + rb")(?![A-Za-z])",
        re.IGNORECASE,
    )
    testimony_counts: Counter[bytes] = Counter()
    testimony_sources = [
        source
        for source in artifact["sources"]
        if source["population"] in {"labeled_grammar", "lexical_testimony"}
    ]
    for source in testimony_sources:
        path = ROOT / source["source"]
        material, _line_starts = _window(path, source["first_line"])
        testimony_counts.update(
            match.group(1).lower()
            for match in testimony_pattern.finditer(material)
        )

    print("  post-hoc vocabulary testimony:\n")
    for family, words in POSTHOC_FAMILIES.items():
        print(f"  {family}")
        for word in words:
            exact = word.encode()
            roles = dict(role_occurrences.get(exact, {}))
            sources = len(role_sources.get(exact, set()))
            external = testimony_counts[exact]
            print(
                f"    {word:16} blind_roles={roles or '{}'}  "
                f"blind_sources={sources}  bounded_testimony_occurrences={external}  "
                f"current_spelling_occurrences={grammar_words[word]}"
            )
        print()

    print(
        "  The atlas rows are exact source-derived aperture physiologies: one\n"
        "  separator, two exact neighboring spans, and the complete varying\n"
        "  middle-material population observed at that bounded frame.  They are\n"
        "  not words, grammar roles, relations, or importance rankings.\n\n"
        "  The vocabulary table was evaluated only after the blind artifact's\n"
        "  digest was printed.  A spelling in the artifact, external testimony,\n"
        "  or witness grammar establishes no match between physiologies.  It\n"
        "  exposes where later testimony exists and where it does not."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
