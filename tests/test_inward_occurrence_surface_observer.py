from pathlib import Path
from hashlib import sha256
import json
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from observe_inward_occurrence_surfaces import (  # noqa: E402
    _surface,
    main as observe_occurrence_surfaces,
)
from observe_inward_frame_coordinate_continuities import (  # noqa: E402
    MEASUREMENT_IDENTITY,
    _complete_existing,
    _scalar_coordinates,
)


def test_scalar_values_do_not_choose_an_occurrence_coordinate_surface():
    coordinate_materials = {}
    first_exact, first_surface, *_ = _surface(
        {"alpha": "first", "beta": 1}, coordinate_materials
    )
    second_exact, second_surface, *_ = _surface(
        {"alpha": "second", "beta": 2}, coordinate_materials
    )

    assert first_surface == second_surface
    assert first_exact == second_exact


def test_immediate_container_count_does_not_change_coordinate_surface():
    coordinate_materials = {}
    first_exact, first_surface, *_ = _surface(
        {"alpha": ["first"]}, coordinate_materials
    )
    second_exact, second_surface, *_ = _surface(
        {"alpha": ["first", "second"]}, coordinate_materials
    )

    assert first_surface == second_surface
    assert first_exact != second_exact


def test_coordinate_material_changes_the_surface():
    coordinate_materials = {}
    _first_exact, first_surface, *_ = _surface(
        {"alpha": "same"}, coordinate_materials
    )
    _second_exact, second_surface, *_ = _surface(
        {"beta": "same"}, coordinate_materials
    )

    assert first_surface != second_surface


def test_nested_scalar_coordinates_have_exact_separate_addresses():
    coordinate_materials = {}
    address_materials = {}

    found = _scalar_coordinates(
        {
            "alpha": {"value": "same"},
            "beta": [{"value": "same"}],
        },
        coordinate_materials,
        address_materials,
    )

    scalar = next(iter(found))
    assert len(found[scalar]) == 2
    assert found[scalar][0][0] != found[scalar][1][0]
    assert found[scalar][0][1] != found[scalar][1][1]
    assert len(address_materials) == 2


def test_nested_coordinate_lookup_is_separate_from_blind_addresses():
    coordinate_materials = {}
    address_materials = {}

    found = _scalar_coordinates(
        {"clear_coordinate": {"nested_coordinate": "material"}},
        coordinate_materials,
        address_materials,
    )

    encoded_blind_finding = repr(found)
    assert "clear_coordinate" not in encoded_blind_finding
    assert "nested_coordinate" not in encoded_blind_finding
    assert "clear_coordinate" in coordinate_materials.values()
    assert any(
        ["coordinate", "nested_coordinate"] in address
        for address in address_materials.values()
    )


def test_plaintext_coordinate_material_is_outside_blind_surface_artifact(
    tmp_path, monkeypatch
):
    source = tmp_path / "source.json"
    blind = tmp_path / "blind.json"
    coordinate_material = tmp_path / "coordinate-material.json"
    source.write_text(
        json.dumps(
            {
                "known_loss": None,
                "sources": [
                    {
                        "source_number": 0,
                        "known_loss": None,
                        "occurrences": [
                            {"append_position": 0, "material": {"alpha": "one"}},
                            {"append_position": 1, "material": {"beta": "two"}},
                        ],
                    },
                    {
                        "source_number": 1,
                        "known_loss": None,
                        "occurrences": [
                            {"append_position": 0, "material": {"alpha": "three"}},
                            {"append_position": 1, "material": {"beta": "four"}},
                        ],
                    },
                ],
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "observe_inward_occurrence_surfaces.py",
            "--input",
            str(source),
            "--output",
            str(blind),
            "--coordinate-material-output",
            str(coordinate_material),
        ],
    )

    assert observe_occurrence_surfaces() == 0

    blind_material = json.loads(blind.read_bytes())
    coordinate_material_finding = json.loads(coordinate_material.read_bytes())
    assert "coordinate_materials" not in blind_material
    assert sorted(coordinate_material_finding["coordinate_materials"].values()) == [
        "alpha",
        "beta",
    ]
    assert coordinate_material_finding[
        "occurrence_surface_artifact_sha256"
    ] == sha256(blind.read_bytes()).hexdigest()


def test_complete_nested_scalar_finding_is_reused_only_while_exact(tmp_path):
    output = tmp_path / "finding.json"
    coordinate_material = tmp_path / "coordinate-material.json"
    complete = tmp_path / "complete.json"
    output.write_bytes(b'{"finding":"exact"}')
    coordinate_material.write_bytes(b'{"coordinates":"separate"}')
    complete.write_text(
        json.dumps(
            {
                "measurement_identity": MEASUREMENT_IDENTITY,
                "source_artifact_sha256": "source",
                "occurrence_surface_artifact_sha256": "surfaces",
                "coordinate_frame_artifact_sha256": "frames",
                "frame_number": 52,
                "frame_continuity_artifact_sha256": sha256(
                    output.read_bytes()
                ).hexdigest(),
                "coordinate_material_artifact_sha256": sha256(
                    coordinate_material.read_bytes()
                ).hexdigest(),
                "known_loss": None,
            }
        )
    )

    assert _complete_existing(
        output=output,
        coordinate_material_output=coordinate_material,
        complete_output=complete,
        surface_sha256="surfaces",
        frame_sha256="frames",
        frame_number=52,
    ) == (output.read_bytes(), coordinate_material.read_bytes())

    output.write_bytes(b'{"finding":"changed"}')
    assert (
        _complete_existing(
            output=output,
            coordinate_material_output=coordinate_material,
            complete_output=complete,
            surface_sha256="surfaces",
            frame_sha256="frames",
            frame_number=52,
        )
        is None
    )
