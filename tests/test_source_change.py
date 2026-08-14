from __future__ import annotations

import os
from pathlib import Path
import sys

import pytest

from seed_runtime.source_change import (
    SourceChangeError,
    SourceEdit,
    apply_source_edits,
    observe_source_files,
    render_source_diff,
    run_source_check,
)


def _repository(tmp_path: Path) -> Path:
    root = tmp_path / "other-repository"
    root.mkdir()
    (root / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "check.py").write_text(
        "from app import VALUE\nraise SystemExit(0 if VALUE == 2 else 7)\n",
        encoding="utf-8",
    )
    return root


def test_exact_observation_can_be_changed_and_checked(tmp_path):
    root = _repository(tmp_path)
    observation = observe_source_files(root, ("app.py",))[0]
    replacement = b"VALUE = 2\n"

    diff = render_source_diff(observation, replacement)
    applied = apply_source_edits(
        root, (SourceEdit.from_observation(observation, replacement),)
    )
    checked = run_source_check(root, (sys.executable, "check.py"))

    assert "-VALUE = 1" in diff
    assert "+VALUE = 2" in diff
    assert (root / "app.py").read_bytes() == replacement
    assert applied[0].before == observation.identity
    assert applied[0].after.byte_count == len(replacement)
    assert checked.passed is True
    assert checked.argv == (sys.executable, "check.py")
    assert checked.stdout_complete is True
    assert checked.stderr_complete is True


def test_stale_observation_refuses_before_any_file_changes(tmp_path):
    root = _repository(tmp_path)
    app, check = observe_source_files(root, ("app.py", "check.py"))
    (root / "check.py").write_text("raise SystemExit(9)\n", encoding="utf-8")

    with pytest.raises(SourceChangeError, match="changed after observation"):
        apply_source_edits(
            root,
            (
                SourceEdit.from_observation(app, b"VALUE = 2\n"),
                SourceEdit.from_observation(check, b"raise SystemExit(0)\n"),
            ),
        )

    assert (root / "app.py").read_bytes() == app.material
    assert (root / "check.py").read_text(encoding="utf-8") == "raise SystemExit(9)\n"


def test_paths_cannot_escape_or_cross_a_symbolic_link(tmp_path):
    root = _repository(tmp_path)
    outside = tmp_path / "outside.py"
    outside.write_text("SECRET = True\n", encoding="utf-8")
    (root / "linked.py").symlink_to(outside)
    nested = root / "nested"
    nested.mkdir()
    (nested / "inside.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "linked-directory").symlink_to(nested, target_is_directory=True)

    for path in (
        "../outside.py",
        "/etc/passwd",
        "linked.py",
        "linked-directory/inside.py",
    ):
        with pytest.raises(SourceChangeError):
            observe_source_files(root, (path,))


def test_duplicate_paths_are_refused_before_change(tmp_path):
    root = _repository(tmp_path)
    observation = observe_source_files(root, ("app.py",))[0]
    edit = SourceEdit.from_observation(observation, b"VALUE = 2\n")

    with pytest.raises(SourceChangeError, match="only once"):
        apply_source_edits(root, (edit, edit))
    assert (root / "app.py").read_bytes() == observation.material


def test_equivalent_path_spellings_cannot_bypass_duplicate_refusal(tmp_path):
    root = _repository(tmp_path)
    observation = observe_source_files(root, ("app.py",))[0]
    first = SourceEdit.from_observation(observation, b"VALUE = 2\n")
    second = SourceEdit("./app.py", observation.identity, b"VALUE = 3\n")

    with pytest.raises(SourceChangeError):
        apply_source_edits(root, (first, second))
    assert (root / "app.py").read_bytes() == observation.material


def test_check_failure_is_returned_as_material_not_a_write_rollback(tmp_path):
    root = _repository(tmp_path)
    observation = observe_source_files(root, ("app.py",))[0]
    apply_source_edits(
        root,
        (SourceEdit.from_observation(observation, b"VALUE = 3\n"),),
    )

    checked = run_source_check(root, (sys.executable, "check.py"))

    assert checked.passed is False
    assert checked.returncode == 7
    assert (root / "app.py").read_text(encoding="utf-8") == "VALUE = 3\n"


def test_source_check_does_not_invoke_a_shell(tmp_path):
    root = _repository(tmp_path)
    marker = root / "shell-ran"
    checked = run_source_check(
        root,
        (
            sys.executable,
            "-c",
            "import sys; print(sys.argv[1])",
            f"hello; touch {marker}",
        ),
    )

    assert checked.passed is True
    assert f"hello; touch {marker}" in checked.stdout.decode("utf-8")
    assert marker.exists() is False


def test_source_check_output_is_bounded_without_hiding_its_extent(tmp_path):
    root = _repository(tmp_path)
    checked = run_source_check(
        root,
        (
            sys.executable,
            "-c",
            "import sys; sys.stdout.write('o' * 2048); sys.stderr.write('e' * 1024)",
        ),
        max_output_bytes=64,
    )

    assert checked.passed is True
    assert checked.stdout == b"o" * 64
    assert checked.stderr == b"e" * 64
    assert checked.stdout_total_bytes == 2048
    assert checked.stderr_total_bytes == 1024
    assert checked.stdout_complete is False
    assert checked.stderr_complete is False


def test_replacement_keeps_existing_permission_bits(tmp_path):
    root = _repository(tmp_path)
    path = root / "app.py"
    os.chmod(path, 0o744)
    observation = observe_source_files(root, ("app.py",))[0]

    apply_source_edits(
        root,
        (SourceEdit.from_observation(observation, b"VALUE = 2\n"),),
    )

    assert path.stat().st_mode & 0o777 == 0o744
