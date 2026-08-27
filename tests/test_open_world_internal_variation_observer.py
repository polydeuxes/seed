"""Position distinctions are established by exact source material."""

from pathlib import Path
import json
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from observe_open_world_internal_variation import (  # noqa: E402
    OPERATION,
    _canonical,
    _digest,
    _reusable_source_artifacts,
    _surface_classes,
    _variation_positions,
)


def _variation(materials: tuple[str, ...]):
    starts = tuple(range(len(materials) * 2))
    productions = tuple(
        (material, (2 * position, 2 * position + 1))
        for position, material in enumerate(materials)
    )
    scalar_materials = []
    variation_positions, recorded_productions = _variation_positions(
        surface=(-1, -1),
        starts=starts,
        recurrent_productions=productions,
        scalar_materials=scalar_materials,
        scalar_indexes_by_value={},
    )
    return variation_positions, recorded_productions, scalar_materials


def test_source_population_establishes_zero_one_or_many_varying_positions():
    no_variation, productions, _materials = _variation(("ab", "cd"))
    assert no_variation == ()
    assert productions == ()

    one_variation, _productions, _materials = _variation(("ab", "ac"))
    assert tuple(
        finding["coordinate_class_number"] for finding in one_variation
    ) == (1,)

    two_variations, productions, scalar_materials = _variation(
        ("ab", "ac", "db", "dc")
    )
    assert tuple(
        finding["coordinate_class_number"] for finding in two_variations
    ) == (0, 1)
    assert tuple(
        finding["source_coordinate_positions"] for finding in two_variations
    ) == ([0], [1])
    assert tuple(
        finding["recurrent_substitution_frame_count"]
        for finding in two_variations
    ) == (2, 2)
    assert len(productions) == 4
    assert len(scalar_materials) == 4


def test_repeated_coordinate_is_one_exact_coordinate_class():
    assert _surface_classes((-1, -1, 0)) == ((0, 2), (1,))


def test_complete_source_artifact_is_reused_only_while_its_bytes_match(tmp_path):
    source = {
        "source": "opaque-source",
        "first_line": 7,
        "line_count": 11,
        "material_sha256": "material-digest",
        "scalar_count": 13,
    }
    artifact_material = _canonical({"exact": "finding"})
    artifact = tmp_path / "source.json"
    artifact.write_bytes(artifact_material)
    entry = {
        "source": source["source"],
        "first_line": source["first_line"],
        "line_count": source["line_count"],
        "material_sha256": source["material_sha256"],
        "artifact": str(artifact),
        "artifact_bytes": len(artifact_material),
        "artifact_sha256": _digest(artifact_material),
        "recurrent_surface_count": 2,
        "varying_surface_finding_count": 1,
        "varying_surface_count_by_position_count": {"1": 1},
        "maximum_recurrent_coordinate_count": 3,
    }
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "source_aperture_artifact_sha256": "input-digest",
                "operation": OPERATION,
                "source_artifacts": [entry],
                "known_loss": None,
            }
        ),
        encoding="utf-8",
    )

    found = _reusable_source_artifacts([source], "input-digest", manifest)
    assert found[source["source"]]["artifact_sha256"] == entry["artifact_sha256"]

    artifact.write_bytes(artifact_material + b"changed")
    assert _reusable_source_artifacts([source], "input-digest", manifest) == {}


def test_complete_source_manifest_must_address_the_current_input(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "source_aperture_artifact_sha256": "other-input",
                "operation": OPERATION,
                "source_artifacts": [],
                "known_loss": None,
            }
        ),
        encoding="utf-8",
    )
    assert _reusable_source_artifacts([], "current-input", manifest) == {}
