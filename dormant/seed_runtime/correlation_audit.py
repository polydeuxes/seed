"""Read-only correlation audit for operational evidence disconnects."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from seed_runtime.capability_needs import build_capability_needs
from seed_runtime.consumer_dependency_audit import build_consumer_audit
from seed_runtime.ownership_discrepancies import build_ownership_discrepancies
from seed_runtime.state import State

_LISTENER_PROCESS_PREDICATES = {
    "listening_process_name",
    "listening_process_id",
}


@dataclass(frozen=True)
class CorrelationFinding:
    area: str
    evidence_present: dict[str, Any]
    consumer: str
    observed_result: dict[str, Any]
    assessment: str
    candidate_boundary: str
    inference_guardrails: tuple[str, ...] = field(
        default=(
            "diagnostic_only",
            "does_not_infer_ownership",
            "does_not_write_facts",
            "does_not_mutate_cluster",
        )
    )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "area": self.area,
            "evidence_present": dict(self.evidence_present),
            "consumer": self.consumer,
            "observed_result": dict(self.observed_result),
            "assessment": self.assessment,
            "candidate_boundary": self.candidate_boundary,
            "inference_guardrails": list(self.inference_guardrails),
        }


@dataclass(frozen=True)
class CorrelationAudit:
    findings: tuple[CorrelationFinding, ...]
    metadata: dict[str, Any]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "findings": [finding.to_json_dict() for finding in self.findings],
            "metadata": dict(self.metadata),
        }


def build_correlation_audit(
    state: State, *, repo_root: str | Path | None = None
) -> CorrelationAudit:
    """Build a read-only audit of evidence that appears disconnected from consumers."""

    root = (
        Path(repo_root)
        if repo_root is not None
        else Path(__file__).resolve().parents[1]
    )
    findings: list[CorrelationFinding] = []
    ownership_rows = build_ownership_discrepancies(state)
    facts = list(state.facts.values())

    listener_process_facts = [
        fact for fact in facts if fact.predicate in _LISTENER_PROCESS_PREDICATES
    ]
    process_observed_statuses = [
        fact
        for fact in facts
        if fact.predicate == "listener_attribution_status"
        and str(fact.value) == "process_observed"
    ]
    owner_not_observed_rows = [
        row
        for row in ownership_rows
        if row.kind == "service" and row.conflict == "owner_not_observed"
    ]
    if listener_process_facts or process_observed_statuses or owner_not_observed_rows:
        if listener_process_facts and owner_not_observed_rows:
            assessment = (
                "process attribution exists but does not appear sufficient to resolve "
                "all ownership rows"
            )
            boundary = "service identity correlation"
        elif listener_process_facts:
            assessment = (
                "process attribution exists and no unresolved service ownership rows "
                "are currently observed"
            )
            boundary = "no suspected boundary from current projection"
        else:
            assessment = (
                "ownership remains unresolved and listener process attribution is not "
                "present in the current projection"
            )
            boundary = "listener process attribution"
        findings.append(
            CorrelationFinding(
                area="Listener Attribution",
                evidence_present={
                    "listener_process_facts": len(listener_process_facts),
                    "process_observed_statuses": len(process_observed_statuses),
                },
                consumer="ownership discrepancies",
                observed_result={
                    "owner_not_observed_rows": len(owner_not_observed_rows)
                },
                assessment=assessment,
                candidate_boundary=boundary,
            )
        )

    capability_needs = build_capability_needs(state)
    if capability_needs:
        diagnostics = sorted(
            {d for need in capability_needs for d in need.diagnostics}
        )
        findings.append(
            CorrelationFinding(
                area="Capability Pressure",
                evidence_present={
                    "capability_needs": len(capability_needs),
                    "capabilities": [need.capability for need in capability_needs],
                },
                consumer="pressure audit and privilege discovery",
                observed_result={"diagnostics": diagnostics},
                assessment="capability needs are surfaced for downstream pressure and privilege views",
                candidate_boundary="no suspected boundary from current projection",
            )
        )

    consumer_audit = build_consumer_audit(root)
    orphaned = [item for item in consumer_audit.items if item.orphaned]
    consumed = [item for item in consumer_audit.items if not item.orphaned]
    if consumer_audit.items:
        findings.append(
            CorrelationFinding(
                area="Consumer Audit",
                evidence_present={"items_scanned": len(consumer_audit.items)},
                consumer="consumer audit",
                observed_result={
                    "consumed_items": len(consumed),
                    "orphaned_items": len(orphaned),
                },
                assessment=(
                    "predicates or diagnostics without implementation consumers remain explanatory only"
                    if orphaned
                    else "predicates and diagnostics scanned by the consumer audit have implementation consumers"
                ),
                candidate_boundary=(
                    "predicate-to-consumer wiring"
                    if orphaned
                    else "no suspected boundary from current repository"
                ),
            )
        )

    return CorrelationAudit(
        findings=tuple(findings),
        metadata={
            "mode": "read_only",
            "records_facts": False,
            "mutates_cluster": False,
            "scope": "current_projection_and_repository_surfaces",
        },
    )


def correlation_audit_json(audit: CorrelationAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_correlation_audit(audit: CorrelationAudit) -> str:
    lines = ["Correlation Audit", ""]
    if not audit.findings:
        lines.append("(none)")
        lines.append("No correlation gaps were identified from the current projection.")
        return "\n".join(lines)
    for finding in audit.findings:
        lines.append("Finding:")
        lines.append(f"  {finding.area}")
        lines.append("")
        lines.append("Evidence Present:")
        for key, value in finding.evidence_present.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        lines.append("Consumer:")
        lines.append(f"  {finding.consumer}")
        lines.append("")
        lines.append("Observed Result:")
        for key, value in finding.observed_result.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        lines.append("Assessment:")
        lines.append(f"  {finding.assessment}")
        lines.append("")
        lines.append("Candidate Boundary:")
        lines.append(f"  {finding.candidate_boundary}")
        lines.append("")
    lines.append("Guardrail: diagnostic only; no ownership facts are inferred or written.")
    return "\n".join(lines).rstrip()
