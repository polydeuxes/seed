"""Discover source-addressed internal variation in recurrent exact extents.

This findings-only observer reads the frozen Unicode-scalar aperture artifact
only for its exact source-window addresses, then reads those exact windows as
unlabelled material.  It does not read the Book, machine grammar, Rosetta,
dictionaries, expected words, language roles, or a requested slot count.

Every adjacent scalar extent begins independently.  An extent grows one exact
source-order coordinate only while its complete internal same/different surface
recurs.  Within each recurrent surface, the observer asks every equality class
the same question:

    while every other exact class value remains fixed,
    does the source carry at least two different values here,
    each with more than one exact occurrence?

Thus the source, not the caller, establishes whether one recurrent extent has
zero, one, or several separately varying internal coordinate classes.

Usage:
    .venv/bin/python scripts/observe_open_world_internal_variation.py
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import time

import numpy as np

from observe_open_world_apertures import CORPUS, _window


INPUT = Path("/tmp/seed_open_world_scalar_apertures_blind.json")
OUTPUT = Path("/tmp/seed_open_world_internal_variation_manifest.json")
SOURCE_OUTPUT_DIRECTORY = Path(
    "/tmp/seed_open_world_internal_variation_sources"
)
OPERATION = (
    "incremental recurrent same/different extent surfaces with every "
    "source-addressed internal coordinate class independently tested "
    "against recurrent exact substitution while all other classes remain fixed"
)


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: object) -> str:
    material = value if isinstance(value, bytes) else _canonical(value)
    return sha256(material).hexdigest()


def _scalar_material_index(
    scalar_materials: list[dict[str, object]],
    indexes_by_value: dict[str, int],
    value: str,
) -> int:
    found_index = indexes_by_value.get(value)
    if found_index is not None:
        return found_index
    encoded = value.encode("utf-8")
    record = {
        "scalar_count": len(value),
        "byte_count": len(encoded),
        "utf8_hex": encoded.hex(),
    }
    index = len(scalar_materials)
    scalar_materials.append(record)
    indexes_by_value[value] = index
    return index


def _surface_classes(surface: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    classes: list[list[int]] = []
    class_at_position: list[int] = []
    for position, prior_position in enumerate(surface):
        if prior_position < 0:
            class_at_position.append(len(classes))
            classes.append([position])
            continue
        if prior_position >= position:
            raise ValueError("equality surface points outside its prior coordinates")
        class_number = class_at_position[prior_position]
        class_at_position.append(class_number)
        classes[class_number].append(position)
    return tuple(tuple(positions) for positions in classes)


def _surface_from_scalars(values: np.ndarray) -> tuple[int, ...]:
    latest: dict[int, int] = {}
    surface = []
    for position, scalar in enumerate(values.tolist()):
        surface.append(latest.get(scalar, -1))
        latest[scalar] = position
    return tuple(surface)


def _rolling_coordinates(scalars: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Provide fast candidate addresses; exact material rechecks every match."""

    mask = (1 << 64) - 1
    base = 1_000_003
    prefixes = np.empty(scalars.size + 1, dtype=np.uint64)
    powers = np.empty(scalars.size + 1, dtype=np.uint64)
    prefixes[0] = 0
    powers[0] = 1
    prefix = 0
    power = 1
    for position, scalar in enumerate(scalars.tolist(), start=1):
        prefix = (prefix * base + scalar + 1) & mask
        power = (power * base) & mask
        prefixes[position] = prefix
        powers[position] = power
    return prefixes, powers


def _variation_positions(
    *,
    surface: tuple[int, ...],
    starts: tuple[int, ...],
    recurrent_productions: tuple[tuple[str, tuple[int, ...]], ...],
    scalar_materials: list[dict[str, object]],
    scalar_indexes_by_value: dict[str, int],
) -> tuple[tuple[dict, ...], tuple[dict, ...]]:
    coordinate_classes = _surface_classes(surface)
    if len(recurrent_productions) < 2:
        return (), ()

    production_values: list[tuple[str, ...]] = []
    production_material_indexes = []
    for material, found_starts in recurrent_productions:
        values = tuple(
            material[positions[0]] for positions in coordinate_classes
        )
        if len(values) != len(set(values)):
            raise AssertionError("two equality classes carry the same source value")
        production_values.append(values)
        production_material_indexes.append(
            [
                _scalar_material_index(
                    scalar_materials, scalar_indexes_by_value, value
                )
                for value in values
            ]
        )

    variation_positions = []
    for class_number, source_positions in enumerate(coordinate_classes):
        exact_frames: dict[tuple[str, ...], list[int]] = defaultdict(list)
        for production_index, values in enumerate(production_values):
            fixed_values = values[:class_number] + values[class_number + 1 :]
            exact_frames[fixed_values].append(production_index)
        recurrent_frames = [
            {"production_indexes": production_indexes}
            for _fixed_values, production_indexes in sorted(exact_frames.items())
            if len(production_indexes) > 1
        ]
        if recurrent_frames:
            variation_positions.append(
                {
                    "coordinate_class_number": class_number,
                    "source_coordinate_positions": list(source_positions),
                    "recurrent_substitution_frame_count": len(recurrent_frames),
                    "recurrent_substitution_frames": recurrent_frames,
                }
            )
    if not variation_positions:
        return (), ()
    start_index = {start: index for index, start in enumerate(starts)}
    production_records = [
        {
            "coordinate_material_indexes": material_indexes,
            "support_start_indexes": [
                start_index[start] for start in found_starts
            ],
        }
        for material_indexes, (_material, found_starts) in zip(
            production_material_indexes, recurrent_productions
        )
    ]
    return tuple(variation_positions), tuple(production_records)


def _observe_source(
    source: dict,
    *,
    deadline: float,
    profile_slow_extents: bool = False,
) -> tuple[dict, bool]:
    source_begun = time.perf_counter()
    exact_bytes, _line_starts = _window(
        CORPUS.parent / source["source"], source["first_line"]
    )
    if _digest(exact_bytes) != source["material_sha256"]:
        raise ValueError("internal-variation source differs from frozen source")
    text = exact_bytes.decode("utf-8")
    scalar_materials: list[dict[str, object]] = []
    scalar_indexes_by_value: dict[str, int] = {}

    scalars = np.fromiter((ord(value) for value in text), dtype=np.uint32)
    rolling_prefixes, rolling_powers = _rolling_coordinates(scalars)
    active_starts = np.arange(len(text) - 1, dtype=np.int64)
    active_surface_ids = (scalars[:-1] != scalars[1:]).astype(np.int64)
    coordinate_count = 2
    recurrent_surface_count = 0
    recurrent_occurrence_count = 0
    varying_surface_count_by_position_count: Counter[int] = Counter()
    findings = []
    stopped_at_time_boundary = False

    while active_starts.size:
        if time.perf_counter() >= deadline:
            stopped_at_time_boundary = True
            break
        extent_begun = time.perf_counter()
        surface_ids, inverse, counts = np.unique(
            active_surface_ids,
            return_inverse=True,
            return_counts=True,
        )
        recurrent_id_mask = counts > 1
        recurrent_surface_ids = surface_ids[recurrent_id_mask]
        recurrent_surface_count += int(recurrent_surface_ids.size)
        recurrent_occurrence_count += int(
            counts[recurrent_id_mask].sum()
        )
        windows = np.lib.stride_tricks.sliding_window_view(
            scalars, coordinate_count
        )
        surface_occurrence_order = np.argsort(inverse, kind="stable")
        surface_occurrence_offsets = np.concatenate(
            (np.array([0], dtype=np.int64), np.cumsum(counts))
        )

        # Exact material recurrence is a stricter boundary than equality-
        # surface recurrence.  Use a rolling coordinate only to find candidate
        # groups, then recheck exact source material before it can participate.
        with np.errstate(over="ignore"):
            material_hashes = (
                rolling_prefixes[active_starts + coordinate_count]
                - rolling_prefixes[active_starts]
                * rolling_powers[coordinate_count]
            )
        _hash_values, hash_inverse, hash_counts = np.unique(
            material_hashes, return_inverse=True, return_counts=True
        )
        hash_occurrence_order = np.argsort(hash_inverse, kind="stable")
        hash_occurrence_offsets = np.concatenate(
            (np.array([0], dtype=np.int64), np.cumsum(hash_counts))
        )
        recurrent_productions_by_surface: dict[
            int, list[tuple[str, tuple[int, ...]]]
        ] = defaultdict(list)
        for hash_group in np.flatnonzero(hash_counts > 1).tolist():
            occurrence_indexes = hash_occurrence_order[
                hash_occurrence_offsets[hash_group] :
                hash_occurrence_offsets[hash_group + 1]
            ]
            exact_groups: dict[str, list[int]] = defaultdict(list)
            for occurrence_index in occurrence_indexes.tolist():
                start = int(active_starts[occurrence_index])
                exact_groups[text[start : start + coordinate_count]].append(start)
            for material, found_starts in exact_groups.items():
                if len(found_starts) < 2:
                    continue
                first_occurrence_index = int(
                    np.searchsorted(active_starts, found_starts[0])
                )
                surface_index = int(inverse[first_occurrence_index])
                recurrent_productions_by_surface[surface_index].append(
                    (material, tuple(found_starts))
                )

        finding_count_before = len(findings)
        for surface_id in recurrent_surface_ids.tolist():
            surface_index = int(np.searchsorted(surface_ids, surface_id))
            recurrent_productions = tuple(
                sorted(recurrent_productions_by_surface.get(surface_index, ()))
            )
            if len(recurrent_productions) < 2:
                varying_surface_count_by_position_count[0] += 1
                continue
            occurrence_indexes = surface_occurrence_order[
                surface_occurrence_offsets[surface_index] :
                surface_occurrence_offsets[surface_index + 1]
            ]
            group_starts_array = active_starts[occurrence_indexes]
            starts = tuple(int(value) for value in group_starts_array.tolist())
            surface = _surface_from_scalars(windows[group_starts_array[0]])
            variation_positions, productions = _variation_positions(
                surface=surface,
                starts=starts,
                recurrent_productions=recurrent_productions,
                scalar_materials=scalar_materials,
                scalar_indexes_by_value=scalar_indexes_by_value,
            )
            varying_position_count = len(variation_positions)
            varying_surface_count_by_position_count[varying_position_count] += 1
            if not variation_positions:
                continue
            coordinate_classes = _surface_classes(surface)
            finding_reference = _digest(
                {
                    "source": source["source"],
                    "coordinate_count": coordinate_count,
                    "surface": surface,
                    "starts": starts,
                }
            )
            findings.append(
                {
                    "finding_reference": finding_reference,
                    "coordinate_count": coordinate_count,
                    "complete_internal_same_difference_surface": list(surface),
                    "source_occurrence_count": len(starts),
                    "source_scalar_starts": list(starts),
                    "coordinate_classes": [
                        list(positions) for positions in coordinate_classes
                    ],
                    "recurrent_exact_productions": list(productions),
                    "source_addressed_varying_position_count": (
                        varying_position_count
                    ),
                    "variation_positions": list(variation_positions),
                }
            )

        variation_elapsed = time.perf_counter() - extent_begun
        if profile_slow_extents and variation_elapsed >= 1.0:
            print(
                f"  extent={coordinate_count:4} active={active_starts.size:7} "
                f"surfaces={recurrent_surface_ids.size:6} "
                f"findings={len(findings) - finding_count_before:5} "
                f"variation={variation_elapsed:.3f}s",
                flush=True,
            )

        keep = recurrent_id_mask[inverse]
        retained_starts = active_starts[keep]
        retained_parent_ids = active_surface_ids[keep]
        has_next_coordinate = retained_starts + coordinate_count < len(text)
        retained_starts = retained_starts[has_next_coordinate]
        retained_parent_ids = retained_parent_ids[has_next_coordinate]
        if not retained_starts.size:
            active_starts = retained_starts
            break
        next_windows = np.lib.stride_tricks.sliding_window_view(
            scalars, coordinate_count + 1
        )[retained_starts]
        matches = next_windows[:, :-1] == next_windows[:, -1, None]
        has_prior = matches.any(axis=1)
        reverse_distance = np.argmax(matches[:, ::-1], axis=1)
        prior_positions = np.where(
            has_prior,
            coordinate_count - 1 - reverse_distance,
            -1,
        )
        extension_coordinates = np.column_stack(
            (retained_parent_ids, prior_positions)
        )
        _extension_kinds, next_surface_ids = np.unique(
            extension_coordinates, axis=0, return_inverse=True
        )
        active_starts = retained_starts
        active_surface_ids = next_surface_ids.astype(np.int64, copy=False)
        coordinate_count += 1

    result = {
        "source": source["source"],
        "first_line": source["first_line"],
        "line_count": source["line_count"],
        "material_sha256": source["material_sha256"],
        "scalar_count": len(text),
        "maximum_recurrent_coordinate_count": coordinate_count - 1,
        "recurrent_surface_count": recurrent_surface_count,
        "recurrent_occurrence_count": recurrent_occurrence_count,
        "varying_surface_count_by_position_count": {
            str(key): value
            for key, value in sorted(varying_surface_count_by_position_count.items())
        },
        "varying_surface_findings": findings,
        "scalar_materials": scalar_materials,
        "wall_seconds": time.perf_counter() - source_begun,
    }
    return result, stopped_at_time_boundary


def _observe_source_with_limit(
    payload: tuple[dict, float, str, bool]
) -> tuple[dict, bool]:
    source, time_limit_seconds, output_directory, profile_slow_extents = payload
    observed, stopped = _observe_source(
        source,
        deadline=time.perf_counter() + time_limit_seconds,
        profile_slow_extents=profile_slow_extents,
    )
    wall_seconds = observed.pop("wall_seconds")
    source_finding = {
        "operation": OPERATION,
        "source": observed,
        "known_loss": (
            "time boundary reached with an unvisited recurrent extent frontier"
            if stopped
            else None
        ),
    }
    encoded = _canonical(source_finding)
    source_reference = _digest(source["source"].encode())
    artifact_sha256 = _digest(encoded)
    output = (
        Path(output_directory)
        / f"{source_reference}-{artifact_sha256}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded)
    return (
        {
            "source": source["source"],
            "first_line": source["first_line"],
            "line_count": source["line_count"],
            "material_sha256": source["material_sha256"],
            "artifact": str(output),
            "artifact_bytes": len(encoded),
            "artifact_sha256": artifact_sha256,
            "recurrent_surface_count": observed["recurrent_surface_count"],
            "varying_surface_finding_count": len(
                observed["varying_surface_findings"]
            ),
            "varying_surface_count_by_position_count": observed[
                "varying_surface_count_by_position_count"
            ],
            "maximum_recurrent_coordinate_count": observed[
                "maximum_recurrent_coordinate_count"
            ],
            "wall_seconds": wall_seconds,
        },
        stopped,
    )


def _reusable_source_artifacts(
    sources: list[dict], input_sha256: str, manifest_path: Path
) -> dict[str, dict]:
    if not manifest_path.exists():
        return {}
    try:
        manifest = json.loads(manifest_path.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    if (
        manifest.get("source_aperture_artifact_sha256") != input_sha256
        or manifest.get("operation") != OPERATION
        or manifest.get("known_loss") is not None
    ):
        return {}
    source_by_name = {source["source"]: source for source in sources}
    reusable = {}
    for entry in manifest.get("source_artifacts", []):
        source = source_by_name.get(entry.get("source"))
        if source is None or any(
            entry.get(key) != source[key]
            for key in ("first_line", "line_count", "material_sha256")
        ):
            continue
        artifact = Path(entry.get("artifact", ""))
        if not artifact.is_file():
            continue
        encoded = artifact.read_bytes()
        if (
            len(encoded) != entry.get("artifact_bytes")
            or _digest(encoded) != entry.get("artifact_sha256")
        ):
            continue
        reusable[source["source"]] = {
            **entry,
            "wall_seconds": 0.0,
            "reused_complete_artifact": True,
        }
    return reusable


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--source-output-directory",
        type=Path,
        default=SOURCE_OUTPUT_DIRECTORY,
    )
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--time-limit-seconds", type=float, default=55.0)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--profile-slow-extents", action="store_true")
    parser.add_argument("--no-reuse-complete-source-artifacts", action="store_true")
    parser.add_argument(
        "--complete-source-manifest",
        type=Path,
        default=OUTPUT,
    )
    arguments = parser.parse_args()

    begun = time.perf_counter()
    encoded_input = arguments.input.read_bytes()
    input_sha256 = _digest(encoded_input)
    aperture = json.loads(encoded_input)
    sources = []
    stopped_at_time_boundary = False
    selected_sources = [
        source
        for source in aperture["sources"]
        if not arguments.source or source["source"] in arguments.source
    ]
    # Larger exact windows generally carry the longest mechanics.  Starting
    # them first reduces parallel tail latency; manifest order remains the
    # frozen source order and findings do not depend on scheduling.
    execution_sources = sorted(
        selected_sources,
        key=lambda source: (-source["scalar_count"], source["source"]),
    )
    observed_by_source = {}
    reusable_by_source = {}
    if not arguments.no_reuse_complete_source_artifacts:
        reusable_by_source = _reusable_source_artifacts(
            execution_sources,
            input_sha256,
            arguments.complete_source_manifest,
        )
    pending_sources = []
    for source in execution_sources:
        reusable = reusable_by_source.get(source["source"])
        if reusable is None:
            pending_sources.append(source)
            continue
        observed_by_source[source["source"]] = (reusable, False)
        print(
            f"{source['source']:48} reused complete "
            f"{reusable['artifact_sha256'][:12]}",
            flush=True,
        )
    payloads = [
        (
            source,
            arguments.time_limit_seconds,
            str(arguments.source_output_directory),
            arguments.profile_slow_extents,
        )
        for source in pending_sources
    ]
    if arguments.jobs < 1:
        raise ValueError("jobs must be a positive exact process count")
    if arguments.jobs == 1:
        observed_sources = map(_observe_source_with_limit, payloads)
    else:
        executor = ProcessPoolExecutor(max_workers=arguments.jobs)
        observed_sources = executor.map(_observe_source_with_limit, payloads)

    try:
        for source, (source_artifact, stopped) in zip(
            pending_sources, observed_sources
        ):
            observed_by_source[source["source"]] = (source_artifact, stopped)
            print(
                f"{source['source']:48} "
                f"surfaces={source_artifact['recurrent_surface_count']:7} "
                f"findings={source_artifact['varying_surface_finding_count']:6} "
                f"positions={source_artifact['varying_surface_count_by_position_count']} "
                f"max={source_artifact['maximum_recurrent_coordinate_count']:4} "
                f"bytes={source_artifact['artifact_bytes']:8} "
                f"{source_artifact['wall_seconds']:.3f}s",
                flush=True,
            )
            stopped_at_time_boundary |= stopped
        sources = [
            {
                key: value
                for key, value in observed_by_source[source["source"]][0].items()
                if key not in {"wall_seconds", "reused_complete_artifact"}
            }
            for source in selected_sources
        ]
    finally:
        if arguments.jobs != 1:
            executor.shutdown()

    finding = {
        "source_aperture_artifact_sha256": input_sha256,
        "operation": OPERATION,
        "source_artifacts": sources,
        "known_loss": (
            "time boundary reached with an unvisited recurrent extent frontier"
            if stopped_at_time_boundary
            else None
        ),
    }
    encoded = _canonical(finding)
    arguments.output.write_bytes(encoded)
    print(f"\nartifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    print(f"complete wall seconds: {time.perf_counter() - begun:.3f}")
    print(f"known loss: {finding['known_loss']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
