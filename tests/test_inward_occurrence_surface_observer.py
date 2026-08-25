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
from observe_inward_frame_walks import (  # noqa: E402
    _aligned_coordinate_intersections,
    _frame_walks,
    _maximum_common_adjacent,
    _repeated_walks,
    _shared_ends,
)
from observe_inward_walk_continuities import _walk_transitions  # noqa: E402


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


def test_frozen_frame_bounds_every_walk_without_a_requested_length():
    walks = _frame_walks(
        [
            ["frame", "act", "result", "frame", "act", "yield", "result"],
            ["frame", "act", "result"],
        ],
        frozenset({"frame"}),
    )

    assert [walk["coordinate_surface_sha256s"] for walk in walks] == [
        ["frame", "act", "result"],
        ["frame", "act", "yield", "result"],
        ["frame", "act", "result"],
    ]


def test_aligned_walk_positions_retain_only_shared_coordinates():
    intersections = _aligned_coordinate_intersections(
        [
            {"coordinate_surface_sha256s": ["assignment-a", "act-a"]},
            {"coordinate_surface_sha256s": ["assignment-b", "act-b"]},
        ],
        {
            "assignment-a": frozenset({"assignment", "first-extra"}),
            "assignment-b": frozenset({"assignment", "second-extra"}),
            "act-a": frozenset({"act", "first-extra"}),
            "act-b": frozenset({"act", "second-extra"}),
        },
    )

    assert [finding["coordinate_material_sha256s"] for finding in intersections] == [
        ["assignment"],
        ["act"],
    ]


def test_walk_sequences_expose_shared_ends_and_varying_middle():
    first, last, middles = _shared_ends(
        [
            ["a", "b", "x", "y", "c"],
            ["a", "b", "x", "y", "x", "y", "c"],
            ["a", "b", "x", "y", "x", "y", "x", "y", "c"],
        ]
    )

    assert first == ["a", "b", "x", "y"]
    assert last == ["c"]
    assert middles == [[], ["x", "y"], ["x", "y", "x", "y"]]


def test_maximum_common_adjacent_walk_is_source_selected():
    length, findings = _maximum_common_adjacent(
        [
            ["a", "b", "c", "d"],
            ["x", "a", "b", "c", "d", "y"],
            ["a", "b", "c", "d", "z"],
        ]
    )

    assert length == 4
    assert findings == [["a", "b", "c", "d"]]


def test_walk_repetition_is_recovered_across_empty_and_varying_middles():
    first, repeated, counts = _repeated_walks(
        ["a", "b", "x", "y", "x", "y"],
        [[], ["x", "y"], ["x", "y", "x", "y"]],
    )

    assert first == ["a", "b"]
    assert repeated == ["x", "y"]
    assert counts == [2, 3, 4]


def test_walk_transitions_join_exact_later_and_prior_boundaries():
    transitions = _walk_transitions(
        [
            {
                "source_number": 0,
                "walk_identity_sha256s": ["a", "b", "c"],
                "walk_addresses": [[0, 4], [4, 11], [11, 15]],
            }
        ]
    )

    assert transitions == [
        {
            "source_number": 0,
            "first_walk_identity_sha256": "a",
            "later_walk_identity_sha256": "b",
            "first_walk_start_append_position": 0,
            "first_walk_last_append_position": 3,
            "later_walk_first_append_position": 4,
            "later_walk_end_append_position": 11,
        },
        {
            "source_number": 0,
            "first_walk_identity_sha256": "b",
            "later_walk_identity_sha256": "c",
            "first_walk_start_append_position": 4,
            "first_walk_last_append_position": 10,
            "later_walk_first_append_position": 11,
            "later_walk_end_append_position": 15,
        },
    ]


PYTEST_ADMISSION = (
    test_scalar_values_do_not_choose_an_occurrence_coordinate_surface,
    test_immediate_container_count_does_not_change_coordinate_surface,
    test_coordinate_material_changes_the_surface,
    test_nested_scalar_coordinates_have_exact_separate_addresses,
    test_nested_coordinate_lookup_is_separate_from_blind_addresses,
    test_plaintext_coordinate_material_is_outside_blind_surface_artifact,
    test_complete_nested_scalar_finding_is_reused_only_while_exact,
    test_frozen_frame_bounds_every_walk_without_a_requested_length,
    test_aligned_walk_positions_retain_only_shared_coordinates,
    test_walk_sequences_expose_shared_ends_and_varying_middle,
    test_maximum_common_adjacent_walk_is_source_selected,
    test_walk_repetition_is_recovered_across_empty_and_varying_middles,
    test_walk_transitions_join_exact_later_and_prior_boundaries,
)
