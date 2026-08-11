import json
import subprocess

import scripts.seed_local as seed_local
from seed_runtime.repository_observation import (
    GitRepositoryObservationProvider,
    observe_repository,
)
from seed_runtime.snapshot_policy_audit import (
    build_snapshot_policy_audit,
    format_snapshot_policy_audit,
)


def _git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=True
    )


def _repo(tmp_path, name="repo"):
    repo = tmp_path / name
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "seed@example.invalid")
    _git(repo, "config", "user.name", "Seed Test")
    (repo / "file.txt").write_text("clean\n", encoding="utf-8")
    _git(repo, "add", "file.txt")
    _git(repo, "commit", "-m", "initial")
    return repo


def test_repository_state_observation_clean_git_repo_branch_and_commit(tmp_path):
    repo = _repo(tmp_path)

    observation = observe_repository(repo)

    assert observation.repository_path == str(repo.resolve())
    assert observation.repository_vcs == "git"
    assert observation.repository_status_available is True
    assert observation.repository_head_commit
    assert observation.repository_branch in {"main", "master"}
    assert observation.repository_dirty is False
    assert observation.repository_staged_count == 0
    assert observation.repository_modified_count == 0
    assert observation.repository_untracked_count == 0


def test_repository_state_path_is_not_hardcoded_to_seed_and_dirty_is_represented(tmp_path):
    repo = _repo(tmp_path, "other-repository")
    (repo / "file.txt").write_text("dirty\n", encoding="utf-8")
    (repo / "new.txt").write_text("new\n", encoding="utf-8")

    observation = observe_repository(repo)

    assert observation.repository_path.endswith("other-repository")
    assert observation.repository_dirty is True
    assert observation.repository_modified_count == 1
    assert observation.repository_untracked_count == 1


def test_repository_state_git_unavailable_is_explicit_and_non_fatal(tmp_path, monkeypatch):
    repo = _repo(tmp_path)
    monkeypatch.setattr(
        "seed_runtime.repository_observation.shutil.which", lambda _: None
    )

    observation = GitRepositoryObservationProvider().observe(repo)

    assert observation.repository_status_available is False
    assert observation.reason == "git executable is unavailable"
    assert observation.repository_head_commit is None


def test_observe_repository_cli_json_is_read_only(tmp_path, capsys):
    repo = _repo(tmp_path)
    before = _git(repo, "rev-parse", "HEAD").stdout.strip()

    code = seed_local.main(["--observe-repository", str(repo), "--json"])
    payload = json.loads(capsys.readouterr().out)
    after = _git(repo, "rev-parse", "HEAD").stdout.strip()

    assert code == 0
    assert payload["repository_head_commit"] == before
    assert after == before
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False


def test_snapshot_policy_reports_repository_context_health_and_distinguishes_comparison(
    tmp_path,
):
    repo = _repo(tmp_path)
    from tests.test_snapshot_policy_audit import _ownership_snapshot
    _ownership_snapshot(repo, "2026-06-20T160000Z")
    _ownership_snapshot(repo, "2026-06-20T170000Z")
    _git(repo, "add", ".audit")
    _git(repo, "commit", "-m", "snapshots")

    audit = build_snapshot_policy_audit(repo)
    rendered = format_snapshot_policy_audit(audit)

    assert audit.repository_context_health == "healthy"
    assert any(row.comparison_available for row in audit.snapshot_kinds)
    assert "Repository Context:" in rendered
    assert "health: healthy" in rendered
    assert "comparison available: yes" in rendered


def test_snapshot_policy_can_have_comparison_available_with_missing_repository_context(
    tmp_path, monkeypatch
):
    from tests.test_snapshot_policy_audit import _ownership_snapshot
    _ownership_snapshot(tmp_path, "2026-06-20T160000Z")
    _ownership_snapshot(tmp_path, "2026-06-20T170000Z")
    monkeypatch.setattr(
        "seed_runtime.repository_observation.shutil.which", lambda _: None
    )

    audit = build_snapshot_policy_audit(tmp_path)

    assert any(row.comparison_available for row in audit.snapshot_kinds)
    assert audit.repository_context_health == "missing"
    assert audit.repository_context.repository_status_available is False
