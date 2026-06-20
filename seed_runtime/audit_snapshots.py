"""Local audit snapshot files and before/after comparison helpers."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

SNAPSHOT_FORMAT_VERSION = 1
SUPPORTED_KINDS = {"observation_inventory", "ownership_discrepancies"}


@dataclass(frozen=True)
class AuditSnapshotResult:
    snapshot_id: str
    directory: Path
    kind: str
    metadata: dict[str, Any]
    git: dict[str, Any]


def snapshot_id_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


def audit_root(repo_root: Path) -> Path:
    return repo_root / ".audit" / "seed"


def create_audit_snapshot(
    *,
    repo_root: Path,
    kind: str,
    payload: Any,
    command: str,
    seed_db: str | None,
    events: list[Any],
    projection_version: str,
    snapshot_id: str | None = None,
) -> AuditSnapshotResult:
    if kind not in SUPPORTED_KINDS:
        raise ValueError(f"unsupported audit snapshot kind: {kind}")
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    sid = snapshot_id or snapshot_id_now()
    directory = _unique_snapshot_dir(audit_root(repo_root), sid)
    directory.mkdir(parents=True, exist_ok=False)
    latest_event_id = events[-1].id if events else None
    metadata = {
        "snapshot_id": directory.name,
        "created_at": created_at,
        "kind": kind,
        "command": command,
        "seed_db": seed_db,
        "latest_event_id": latest_event_id,
        "event_count": len(events),
        "projection_version": projection_version,
        "snapshot_format_version": SNAPSHOT_FORMAT_VERSION,
    }
    git = collect_git_metadata(repo_root)
    _write_json(directory / f"{kind}.json", payload)
    _write_json(directory / "metadata.json", metadata)
    _write_json(directory / "git.json", git)
    return AuditSnapshotResult(directory.name, directory, kind, metadata, git)


def _unique_snapshot_dir(root: Path, snapshot_id: str) -> Path:
    candidate = root / snapshot_id
    if not candidate.exists():
        return candidate
    suffix = 1
    while True:
        candidate = root / f"{snapshot_id}-{suffix:02d}"
        if not candidate.exists():
            return candidate
        suffix += 1


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def collect_git_metadata(repo_root: Path, *, runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> dict[str, Any]:
    def git(args: list[str]) -> str:
        completed = runner(["git", *args], cwd=repo_root, text=True, capture_output=True, check=True)
        return completed.stdout.strip()
    try:
        branch = git(["rev-parse", "--abbrev-ref", "HEAD"])
        commit = git(["rev-parse", "HEAD"])
        changed = [line for line in git(["status", "--porcelain"]).splitlines() if line]
        return {
            "available": True,
            "branch": branch,
            "commit": commit,
            "dirty": bool(changed),
            "changed_files": [line[3:] if len(line) > 3 else line for line in changed],
        }
    except Exception as exc:  # best effort only: git must never block snapshots
        return {"available": False, "reason": str(exc)}


def list_audit_snapshots(repo_root: Path) -> list[dict[str, Any]]:
    root = audit_root(repo_root)
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return rows
    for directory in sorted(p for p in root.iterdir() if p.is_dir()):
        metadata = _read_json(directory / "metadata.json") or {}
        git = _read_json(directory / "git.json") or {}
        rows.append({"snapshot_id": directory.name, "metadata": metadata, "git": git})
    return rows


def format_audit_snapshots(rows: list[dict[str, Any]]) -> str:
    headers = ["Snapshot ID", "Kind", "Commit", "Created", "Command"]
    rendered = [headers]
    for row in rows:
        meta = row.get("metadata", {})
        git = row.get("git", {})
        commit = git.get("commit", "-") if git.get("available", True) else "-"
        if isinstance(commit, str) and len(commit) > 7:
            commit = commit[:7]
        rendered.append([row["snapshot_id"], meta.get("kind", "-"), commit or "-", meta.get("created_at", "-"), meta.get("command", "-")])
    widths = [max(len(str(r[i])) for r in rendered) for i in range(len(headers))]
    return "\n".join("  ".join(str(v).ljust(widths[i]) for i, v in enumerate(r)) for r in rendered)


def compare_audit_snapshots(repo_root: Path, a: str, b: str, *, kind: str) -> dict[str, Any]:
    path_a = _resolve_snapshot(repo_root, a) / f"{kind}.json"
    path_b = _resolve_snapshot(repo_root, b) / f"{kind}.json"
    left = _read_json(path_a)
    right = _read_json(path_b)
    if left is None or right is None:
        raise FileNotFoundError(f"snapshot kind file missing for {kind}")
    if kind == "observation_inventory":
        return _compare_observation_inventory(left, right)
    if kind == "ownership_discrepancies":
        return _compare_ownership_discrepancies(left, right)
    raise ValueError(f"unsupported audit compare kind: {kind}")


def _resolve_snapshot(repo_root: Path, ref: str) -> Path:
    root = audit_root(repo_root)
    dirs = sorted([p for p in root.iterdir() if p.is_dir()]) if root.exists() else []
    if ref in {"latest", "previous"}:
        if len(dirs) < (1 if ref == "latest" else 2):
            raise FileNotFoundError(f"not enough snapshots for {ref}")
        return dirs[-1] if ref == "latest" else dirs[-2]
    path = root / ref
    if not path.exists():
        raise FileNotFoundError(f"snapshot not found: {ref}")
    return path


def _read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def _compare_observation_inventory(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    def names(payload: dict[str, Any], section: str, key: str) -> set[str]:
        return {str(item[key]) for item in payload.get(section, []) if key in item}
    out = {"kind": "observation_inventory"}
    for section, key in [("predicates", "predicate"), ("providers", "name"), ("families", "family")]:
        left, right = names(a, section, key), names(b, section, key)
        out[section] = {"added": sorted(right - left), "removed": sorted(left - right)}
    summary = {}
    for key in sorted(set(a.get("summary", {})) | set(b.get("summary", {}))):
        if a.get("summary", {}).get(key) != b.get("summary", {}).get(key):
            summary[key] = {"from": a.get("summary", {}).get(key), "to": b.get("summary", {}).get(key)}
    out["summary_changes"] = summary
    return out


def _compare_ownership_discrepancies(a: list[dict[str, Any]], b: list[dict[str, Any]]) -> dict[str, Any]:
    def key(row: dict[str, Any]) -> str:
        return f"{row.get('kind')}\t{row.get('subject')}"
    left, right = {key(r): r for r in a}, {key(r): r for r in b}
    common = sorted(set(left) & set(right))
    changed = {field: [] for field in ["conflict", "confidence", "candidate_owner", "capability_needs"]}
    for k in common:
        for field in ["conflict", "confidence", "candidate_owner"]:
            if left[k].get(field) != right[k].get(field):
                changed[field].append({"key": k, "from": left[k].get(field), "to": right[k].get(field)})
        ln, rn = _capability_needs(left[k]), _capability_needs(right[k])
        if ln != rn:
            changed["capability_needs"].append({"key": k, "added": sorted(rn - ln), "removed": sorted(ln - rn)})
    return {"kind": "ownership_discrepancies", "added_rows": [right[k] for k in sorted(set(right)-set(left))], "removed_rows": [left[k] for k in sorted(set(left)-set(right))], "changes": changed}


def _capability_needs(row: dict[str, Any]) -> set[str]:
    values = row.get("capability_needs") or row.get("capability_needs", [])
    return {str(v) for v in values} if isinstance(values, list) else set()


def format_audit_compare(diff: dict[str, Any]) -> str:
    if diff["kind"] == "observation_inventory":
        lines = ["Audit Compare: observation_inventory", ""]
        for title, section in [("Predicates", "predicates"), ("Providers", "providers"), ("Families", "families")]:
            lines += [f"{title}:", f"  added: {', '.join(diff[section]['added']) or 'none'}", f"  removed: {', '.join(diff[section]['removed']) or 'none'}", ""]
        lines.append("Summary:")
        for key, change in diff["summary_changes"].items():
            lines.append(f"  {key}: {change['from']} -> {change['to']}")
        if not diff["summary_changes"]:
            lines.append("  none")
        return "\n".join(lines)
    lines = ["Audit Compare: ownership_discrepancies", "", "Rows:", f"  added: {len(diff['added_rows'])}", f"  removed: {len(diff['removed_rows'])}", "", "Changes:"]
    any_change = False
    for field, changes in diff["changes"].items():
        if changes:
            any_change = True
            lines.append(f"  {field}: {len(changes)}")
    if not any_change:
        lines.append("  none")
    return "\n".join(lines)
