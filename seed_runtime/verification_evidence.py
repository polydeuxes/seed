"""Read-only verification-evidence acquisition for capability candidates.

Verification evidence is observable local evidence that may support later
capability verification inspection. It is not a verified capability, capability
selection, execution authority, policy approval, planning, or tool invocation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os

from seed_runtime.capability_candidates import build_capability_candidates
from seed_runtime.state import State

_VERIFICATION_EVIDENCE_BOUNDARY_NOTES = (
    "verification_evidence_not_capability_verification",
    "verification_evidence_not_capability_selection",
    "verification_evidence_not_execution_authority",
    "verification_evidence_not_tool_invocation",
    "observed_binary_not_permission",
    "observed_path_not_approval",
    "no_capability_selection",
    "no_policy_evaluation",
    "no_tool_execution",
    "read_only_inspection",
)

_CAPABILITY_BINARY_CANDIDATES: dict[str, tuple[str, ...]] = {
    "ssh_client": ("ssh",),
    "python_runtime": ("python3", "python"),
    "docker_client": ("docker",),
    "git_client": ("git",),
    "http_client": ("curl",),
}


@dataclass(frozen=True)
class VerificationEvidence:
    """One locally observed support item for a capability candidate."""

    candidate: str
    evidence_type: str
    observation_source: str
    value: str
    rationale: str
    support_notes: list[str] = field(default_factory=list)
    boundary_notes: list[str] = field(
        default_factory=lambda: list(_VERIFICATION_EVIDENCE_BOUNDARY_NOTES)
    )


@dataclass(frozen=True)
class VerificationEvidenceInspection:
    """Read-only verification-evidence acquisition result."""

    evidence: list[VerificationEvidence] = field(default_factory=list)
    filter: str | None = None
    boundary: str = "verification_evidence_acquisition_only"
    notes: list[str] = field(default_factory=lambda: list(_VERIFICATION_EVIDENCE_BOUNDARY_NOTES))


def build_verification_evidence(
    state: State,
    *,
    filter_text: str | None = None,
    path_env: str | None = None,
) -> VerificationEvidenceInspection:
    """Acquire local read-only verification evidence for observed candidates.

    The candidate universe remains the evidence-derived capability candidates.
    Acquisition only checks whether repository-justified binary names are present
    as executable files in PATH directories. It never runs those binaries and
    never promotes evidence into ``capability_verified`` facts.
    """

    candidate_inspection = build_capability_candidates(state, filter_text=filter_text)
    path_entries = _path_entries(os.environ.get("PATH", "") if path_env is None else path_env)
    evidence: list[VerificationEvidence] = []
    for candidate in candidate_inspection.candidates:
        for binary in _CAPABILITY_BINARY_CANDIDATES.get(candidate.candidate, ()):  # noqa: SIM118
            binary_path = _find_binary(binary, path_entries)
            if binary_path is None:
                continue
            evidence.append(
                VerificationEvidence(
                    candidate=candidate.candidate,
                    evidence_type="binary_path_observed",
                    observation_source="local_path_inspection",
                    value=str(binary_path),
                    rationale=(
                        f"binary {binary!r} was observed as an executable file in PATH; "
                        "this can support verification inspection but is not verification, "
                        "selection, permission, policy approval, or execution authority"
                    ),
                    support_notes=[
                        f"binary_name:{binary}",
                        "filesystem_metadata_only",
                        "binary_not_invoked",
                    ],
                )
            )
    return VerificationEvidenceInspection(evidence=evidence, filter=filter_text)


def _path_entries(path_env: str) -> list[Path]:
    return [Path(entry or ".") for entry in path_env.split(os.pathsep) if entry or entry == ""]


def _find_binary(binary: str, path_entries: list[Path]) -> Path | None:
    for directory in path_entries:
        candidate = directory / binary
        try:
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return candidate
        except OSError:
            continue
    return None
