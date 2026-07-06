"""Registry-backed visibility for operational diagnostic CLI surfaces."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Literal, Union

RecordScope = Literal["none", "diagnostic_run"]


@dataclass(frozen=True)
class DiagnosticInventoryEntry:
    """Operational shape declaration for one diagnostic/test-like CLI surface."""

    name: str
    cli_flags: tuple[str, ...]
    uses_projected_state: bool
    uses_repo_files: bool
    supports_json: bool
    supports_record: bool
    record_scope: RecordScope
    emits_diagnostic_facts: bool
    emits_cluster_facts: bool
    writes_event_ledger: bool
    mutates_cluster: bool
    reads_diagnostic_facts: bool
    description: str

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["cli_flags"] = list(self.cli_flags)
        return data


@dataclass(frozen=True)
class _DiagnosticInventoryCompositionInput:
    """Prepared diagnostic declarations for inventory composition only."""

    entries: tuple[DiagnosticInventoryEntry, ...]


@dataclass(frozen=True)
class _DiagnosticSurfaceReadOnlyEvaluation:
    """Implementation-local read-only evaluation before boundary identification."""

    read_only: bool


@dataclass(frozen=True)
class _DiagnosticSurfaceBoundaryStatementSet:
    """Implementation-local ordered boundary statements before identification."""

    statements: tuple[str, ...]


@dataclass(frozen=True)
class _DiagnosticSurfaceBoundaryIdentification:
    """Implementation-local boundary facts before report presentation."""

    statements: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        return {
            "status": "known",
            "statements": list(self.statements),
            "evidence_source": "diagnostic_inventory",
            "implementation_reason": (
                "boundary recovered from declared diagnostic inventory fields"
            ),
        }


@dataclass(frozen=True)
class _KnownDiagnosticSurfaceDefinition:
    """Implementation-local known DiagnosticSurface fact before wrapping."""

    entry: DiagnosticInventoryEntry
    boundary: _DiagnosticSurfaceBoundaryIdentification
    consumption: _DiagnosticSurfaceConsumptionIdentification
    shape_registration: _DiagnosticSurfaceShapeRegistrationIdentification

    def to_json_dict(self) -> dict[str, object]:
        return {
            "status": "known",
            "diagnostic_name": self.entry.name,
            "cli_flags": list(self.entry.cli_flags),
            "description": self.entry.description,
            "supports_json": self.entry.supports_json,
            "supports_record": self.entry.supports_record,
            "record_scope": self.entry.record_scope,
            "diagnostic_surface_boundary": _diagnostic_surface_boundary(self.boundary),
            "diagnostic_surface_consumption": _diagnostic_surface_consumption(
                self.consumption
            ),
            "diagnostic_inventory_registration": "present",
            "shape_registration_status": _diagnostic_surface_shape_registration_status(
                self.shape_registration
            ),
            "evidence_source": "diagnostic_inventory + diagnostic_shape_audit",
            "implementation_reason": "identity recovered from the diagnostic inventory entry and static shape-audit registration",
        }


@dataclass(frozen=True)
class _UnknownDiagnosticSurfaceDefinition:
    """Implementation-local unknown DiagnosticSurface fact before wrapping."""

    diagnostic_name: str

    def to_json_dict(self) -> dict[str, object]:
        return {
            "status": "unknown",
            "diagnostic_name": self.diagnostic_name,
            "cli_flags": [],
            "description": "unknown",
            "supports_json": "unknown",
            "supports_record": "unknown",
            "record_scope": "unknown",
            "diagnostic_surface_boundary": {
                "status": "unknown",
                "statements": [],
                "evidence_source": "diagnostic_inventory",
                "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
            },
            "diagnostic_surface_consumption": {
                "status": "unknown",
                "declared_consumption": {},
                "evidence_source": "diagnostic_inventory",
                "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
            },
            "diagnostic_inventory_registration": "absent",
            "shape_registration_status": "unknown",
            "evidence_source": "diagnostic_inventory",
            "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
        }


@dataclass(frozen=True)
class _DiagnosticSurfaceExplanationComposition:
    """Implementation-local DiagnosticSurface explanation before wrapping."""

    definition: dict[str, object]

    def to_json_dict(self) -> dict[str, object]:
        return {
            "diagnostic_surface_definition": self.definition,
            "diagnostic_surface_boundary": self.definition[
                "diagnostic_surface_boundary"
            ],
            "diagnostic_surface_consumption": self.definition[
                "diagnostic_surface_consumption"
            ],
        }


@dataclass(frozen=True)
class _DiagnosticSurfaceDefinitionLineSet:
    """Implementation-local definition lines before human rendering."""

    lines: tuple[str, ...]


@dataclass(frozen=True)
class _DiagnosticSurfaceExplanationLineSet:
    """Implementation-local explanation lines before human rendering."""

    lines: tuple[str, ...]


@dataclass(frozen=True)
class _DiagnosticSurfaceCliFlagDisplay:
    """Implementation-local CLI flag display text before human rendering."""

    text: str


@dataclass(frozen=True)
class _DiagnosticSurfaceBoundaryStatementSequence:
    """Implementation-local boundary statements before text rendering."""

    statements: tuple[str, ...]


@dataclass(frozen=True)
class _DiagnosticSurfaceBoundaryText:
    """Implementation-local boundary statement text before line rendering."""

    text: str


@dataclass(frozen=True)
class _DiagnosticSurfaceConsumptionText:
    """Implementation-local consumption declaration text before line rendering."""

    text: str


@dataclass(frozen=True)
class _DiagnosticSurfaceShapeRegistrationLookup:
    """Implementation-local shape registration lookup before status identification."""

    present: bool


@dataclass(frozen=True)
class _DiagnosticSurfaceShapeRegistrationIdentification:
    """Implementation-local shape registration fact before definition composition."""

    status: str


@dataclass(frozen=True)
class _DiagnosticSurfaceConsumptionDeclarationSet:
    """Implementation-local declared consumption facts before identification."""

    uses_projected_state: bool
    uses_repo_files: bool
    reads_diagnostic_facts: bool


@dataclass(frozen=True)
class _DiagnosticSurfaceConsumptionIdentification:
    """Implementation-local consumption facts before report presentation."""

    uses_projected_state: bool
    uses_repo_files: bool
    reads_diagnostic_facts: bool

    def to_json_dict(self) -> dict[str, object]:
        return {
            "status": "known",
            "declared_consumption": {
                "uses_projected_state": self.uses_projected_state,
                "uses_repo_files": self.uses_repo_files,
                "reads_diagnostic_facts": self.reads_diagnostic_facts,
            },
            "evidence_source": "diagnostic_inventory",
            "implementation_reason": (
                "consumption recovered from declared diagnostic inventory fields"
            ),
        }


DIAGNOSTIC_INVENTORY: tuple[DiagnosticInventoryEntry, ...] = (
    DiagnosticInventoryEntry(
        name="classification_coverage",
        cli_flags=("--classification-coverage",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=False,
        supports_record=True,
        record_scope="diagnostic_run",
        emits_diagnostic_facts=True,
        emits_cluster_facts=False,
        writes_event_ledger=True,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Reports projected entity classification coverage and unknown contributors.",
    ),
    DiagnosticInventoryEntry(
        name="graph_issue_summary",
        cli_flags=("--graph-issue-summary",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=False,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Reports grouped projected graph validation issues.",
    ),
    DiagnosticInventoryEntry(
        name="knowledge_reachability",
        cli_flags=(
            "--knowledge-reachability-audit",
            "--knowledge-reachability-audit-json",
        ),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Audits knowledge reachability across projected, repository, inquiry, and rendered surfaces.",
    ),
    DiagnosticInventoryEntry(
        name="documentation_structure",
        cli_flags=(
            "--documentation-structure",
            "--document",
            "--missing-front-matter",
            "--missing-trailing-newline",
            "--empty-sections",
            "--sections",
            "--links",
            "--code-fences",
            "--architectural-relations",
            "--recurrence",
            "--rare",
            "--missing-common-sections",
            "--outliers",
            "--skeletons",
            "--where",
            "--membership",
            "--limit",
            "--top",
            "--summary-only",
            "--min-count",
            "--max-count",
        ),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Observes mechanical document metrics, front matter, heading outline metadata, section inventory boundaries, structural Markdown link targets, and fenced code block structure, explicit architectural relation forms, and corpus-level structural recurrence, exact section-label structural drilldown, exact section-label structural membership, compact human skeleton signature rendering, and raw JSON skeleton signature metrics for top-level repository docs without parsing code contents, interpreting prose, link text, grammar, responsibility, lexicon, extracting claims, inferring authority, inferring shapes, promoting ontology, writing events, or mutating the repository.",
    ),
    DiagnosticInventoryEntry(
        name="container_ownership_authority",
        cli_flags=("--container-ownership-authority",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Shows bounded read-only container ownership authority reasoning from projected state without recording, provider acquisition, execution, event-ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="service_ownership_authority",
        cli_flags=("--service-ownership-authority",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Shows bounded read-only service ownership authority reasoning from projected state and implementation inventory evidence without recording, provider acquisition, execution, event-ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="listener_endpoint_authority",
        cli_flags=("--listener-endpoint-authority",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Shows bounded read-only local TCP/UDP listener endpoint authority reasoning from projected state and implementation inventory evidence without recording, provider acquisition, execution, event-ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="ownership_discrepancies",
        cli_flags=("--ownership-discrepancies",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=True,
        record_scope="diagnostic_run",
        emits_diagnostic_facts=True,
        emits_cluster_facts=False,
        writes_event_ledger=True,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Reports storage/service ownership candidates, conflicts, and capability needs.",
    ),
    DiagnosticInventoryEntry(
        name="audit_snapshot",
        cli_flags=("--audit-snapshot",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=False,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Saves local operational audit output and best-effort git metadata under .audit/seed/ without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="audit_snapshots",
        cli_flags=("--audit-snapshots",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=False,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Lists local operational audit snapshot artifacts from .audit/seed/.",
    ),
    DiagnosticInventoryEntry(
        name="audit_compare",
        cli_flags=("--audit-compare",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Compares two local operational audit snapshots without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="operational_surface_inventory",
        cli_flags=("--operational-surface-inventory",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Discovers operational CLI surfaces from argparse implementation evidence without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="visibility_coverage_audit",
        cli_flags=("--visibility-coverage-audit",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Compares implementation-discovered operational surfaces with diagnostic inventory visibility without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="operational_surface_classification_audit",
        cli_flags=("--operational-surface-classification-audit",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Classifies discovered CLI elements into primary surfaces, filters, modifiers, debug, manual-input, legacy, or unknown without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="consumer_audit",
        cli_flags=("--consumer-audit",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Audits implementation-backed consumers of observation predicates and diagnostic surfaces without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="emitter_consumer_audit",
        cli_flags=("--emitter-consumer-audit", "--include-rendered"),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Audits implementation-backed emitted outputs and their visible consumers without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="emitter_attribution_audit",
        cli_flags=("--emitter-attribution-audit", "--include-rendered"),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Explains attributed, dynamic, indirect, discovery-gap, missing, or unknown emitter attribution without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="component_audit",
        cli_flags=("--component-audit",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Summarizes a named component role from repository, graph, consumer, test, and architecture evidence without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="architecture_conformance_audit",
        cli_flags=("--architecture-conformance-audit",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Compares architecture evidence with observed operational structure, significance breakdowns, and concept realizations without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="operational_graph",
        cli_flags=("--operational-graph",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Builds a read-only implementation-backed operational relationship graph with evidence and confidence without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="operational_graph_taxonomy",
        cli_flags=("--operational-graph-taxonomy",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Summarizes operational graph node classifications and aggregate connectivity without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="operational_graph_confidence",
        cli_flags=("--operational-graph-confidence", "--exclude-aggregate"),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Analyzes operational graph edge confidence reasons, evidence categories, representative examples, and important weak relationships without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="observation_utilization",
        cli_flags=("--observation-utilization",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description=(
            "Audits implementation source participation of observation predicates "
            "across projection, read-model, and diagnostic surfaces without "
            "loading projected state."
        ),
    ),
    DiagnosticInventoryEntry(
        name="observation_domains",
        cli_flags=("--observation-domains",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Shows read-only observation-domain coverage and gap classification from existing observation, capability, and operational evidence without recording or mutation.",
    ),
    DiagnosticInventoryEntry(
        name="observation_permission",
        cli_flags=("--observation-permission",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Shows read-only observation-domain permission visibility with conservative classes, authority evidence, unknowns, and manual-invocation reasoning without recording, event ledger writes, cluster mutation, enforcement, approval storage, or autonomous runtime behavior.",
    ),
    DiagnosticInventoryEntry(
        name="capability_needs",
        cli_flags=("--capability-needs",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Reads recorded diagnostic facts and reports capability needs by subject.",
    ),
    DiagnosticInventoryEntry(
        name="capability_relationship",
        cli_flags=("--capability-relationship",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Explains read-only capability relationship context across access, benefit, pressure, attainability, expectation, and unknowns without acquisition, policy, planning, recording, event ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="investigation_path",
        cli_flags=("--investigation-path",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Exposes evidence-backed read-only investigation paths across existing diagnostic surfaces without planning, recording, event ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="reasoning_path",
        cli_flags=("--reasoning-path",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Exposes evidence-backed derivation paths from source evidence through conclusions, consumers, and story impact without recording facts, event ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="selection_path",
        cli_flags=("--selection-path",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Exposes read-only implementation-backed selection paths showing candidates, factors, non-selected alternatives, and outcome without recording facts, event ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="operational_story",
        cli_flags=("--operational-story",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Composes existing operational evidence into a read-only story view without recording facts, event ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="ops_brief",
        cli_flags=("--ops-brief",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Aggregates existing operational visibility surfaces into a read-only triage brief.",
    ),
    DiagnosticInventoryEntry(
        name="current_facts_cache_debug",
        cli_flags=("--current-facts-cache-debug",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=False,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Reports read-only current-facts cache and timing phases without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="impact_audit",
        cli_flags=("--impact-audit",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Compares existing operational audit snapshots, reports snapshot coverage, and classifies observable outcome impact without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="history_brief",
        cli_flags=("--history-brief",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Synthesizes existing impact, snapshot-policy, and repository-state visibility into a read-only historical brief without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="reference_selection",
        cli_flags=("--reference-selection",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Exposes read-only implementation-selected comparison-reference visibility for a question domain without recording facts, event ledger writes, baseline creation, expectations, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="repository_state_observation",
        cli_flags=("--observe-repository",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Observes read-only repository state for an arbitrary local repository path without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="snapshot_policy_audit",
        cli_flags=("--snapshot-policy-audit",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Audits snapshot readiness, comparison availability, and visibility recommendations without creating snapshots, writing events, or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="pressure_audit",
        cli_flags=("--pressure-audit",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Ranks operational pressure from existing visibility surfaces without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="correlation_audit",
        cli_flags=("--correlation-audit",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Correlates existing evidence, consumers, and pressure surfaces to expose suspected operational disconnects without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="projection_shape",
        cli_flags=("--projection-shape",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Shows read-only implementation-backed projection stage shape without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="projection_stage_definition",
        cli_flags=("--projection-stage-definition",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Explains the implementation-backed identity and boundary of one projection stage from projection shape declarations without runtime execution, projection execution, planning, interpretation, inference, recording, event-ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="projection_stage_explanation",
        cli_flags=("--projection-stage-explanation",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Composes existing projection stage definition, boundary, and implementation-backed relationship explanation fields without runtime execution, projection execution, projection ordering, planning, semantic interpretation, relationship inference, recording, event-ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="question_surface_inventory",
        cli_flags=(
            "--question-surface-inventory",
            "ask --question-families",
            "--question-family-definition",
            "--question-family-explanation",
        ),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Lists known question families and explains their existing diagnostic-surface relationships without routing, recommendations, recording, event-ledger writes, projected state, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="inquiry_artifacts",
        cli_flags=("--inquiry-artifacts",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Shows read-only repository-visible inquiry artifact classifications without recording, event-ledger writes, cluster mutation, inquiry graph creation, pressure transformation inference, workflow, or planning behavior.",
    ),
    DiagnosticInventoryEntry(
        name="diagnostic_surface_definition",
        cli_flags=("--diagnostic-surface-definition",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Explains the implementation-backed identity of one diagnostic surface from diagnostic inventory and shape-audit declarations without execution, planning, interpretation, inference, recording, event-ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="diagnostic_surface_explanation",
        cli_flags=("--diagnostic-surface-explanation",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Composes existing DiagnosticSurface definition, boundary, and consumption explanation fields without discovering, inferring, reasoning, recording, event-ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="diagnostic_inventory",
        cli_flags=("--diagnostic-inventory",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Lists registry-declared diagnostic and operational surfaces without recording or mutation.",
    ),
    DiagnosticInventoryEntry(
        name="diagnostic_shape_audit",
        cli_flags=("--diagnostic-shape-audit",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Compares diagnostic registry declarations with static implementation shape without recording or mutation.",
    ),
    DiagnosticInventoryEntry(
        name="projected_state_consumers",
        cli_flags=("--projected-state-consumers",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Lists implementation-backed evidence source classes consumed by known diagnostic and operational surfaces without recording or mutation.",
    ),
    DiagnosticInventoryEntry(
        name="implementation_trait_characterization",
        cli_flags=("--implementation-trait-characterization",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Classifies traits exposed by current visibility inventories into implementation-backed recurring concerns without recording, observation execution, event-ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="privilege_discovery",
        cli_flags=("--privilege-discovery",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Explains privilege boundaries and bounded guidance/evidence blockers for current capability needs without privileged actions, fact recording, or cluster mutation.",
    ),
)


def build_diagnostic_surface_definition(
    diagnostic_surface: str,
    entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> dict[str, object]:
    """Return a read-only identity explanation for one DiagnosticSurface."""

    entry = next((item for item in entries if item.name == diagnostic_surface), None)
    if entry is None:
        return _diagnostic_surface_definition_wrapper(
            _produce_unknown_diagnostic_surface_definition(diagnostic_surface)
        )

    return _diagnostic_surface_definition_wrapper(
        _produce_known_diagnostic_surface_definition(entry)
    )


def _produce_known_diagnostic_surface_definition(
    entry: DiagnosticInventoryEntry,
) -> _KnownDiagnosticSurfaceDefinition:
    return _KnownDiagnosticSurfaceDefinition(
        entry=entry,
        boundary=_identify_diagnostic_surface_boundary(entry),
        consumption=_identify_diagnostic_surface_consumption(entry),
        shape_registration=_identify_diagnostic_surface_shape_registration(entry.name),
    )


def _produce_unknown_diagnostic_surface_definition(
    diagnostic_surface: str,
) -> _UnknownDiagnosticSurfaceDefinition:
    return _UnknownDiagnosticSurfaceDefinition(diagnostic_name=diagnostic_surface)


def _diagnostic_surface_definition_wrapper(
    definition: Union[
        _KnownDiagnosticSurfaceDefinition, _UnknownDiagnosticSurfaceDefinition
    ],
) -> dict[str, object]:
    return {"diagnostic_surface_definition": definition.to_json_dict()}


def build_diagnostic_surface_explanation(
    diagnostic_surface: str,
    entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> dict[str, object]:
    """Compose existing DiagnosticSurface explanation fields for presentation."""

    definition = build_diagnostic_surface_definition(diagnostic_surface, entries)[
        "diagnostic_surface_definition"
    ]
    return _diagnostic_surface_explanation_wrapper(
        _compose_diagnostic_surface_explanation(definition)
    )


def _compose_diagnostic_surface_explanation(
    definition: dict[str, object],
) -> _DiagnosticSurfaceExplanationComposition:
    return _DiagnosticSurfaceExplanationComposition(definition=definition)


def _diagnostic_surface_explanation_wrapper(
    explanation: _DiagnosticSurfaceExplanationComposition,
) -> dict[str, object]:
    return {"diagnostic_surface_explanation": explanation.to_json_dict()}


def diagnostic_surface_explanation_json(diagnostic_surface: str) -> dict[str, object]:
    return build_diagnostic_surface_explanation(diagnostic_surface)


def format_diagnostic_surface_explanation(diagnostic_surface: str) -> str:
    explanation = build_diagnostic_surface_explanation(diagnostic_surface)[
        "diagnostic_surface_explanation"
    ]
    line_set = _assemble_diagnostic_surface_explanation_line_set(explanation)
    return "\n".join(line_set.lines)


def _assemble_diagnostic_surface_explanation_line_set(
    explanation: dict[str, object],
) -> _DiagnosticSurfaceExplanationLineSet:
    definition = explanation["diagnostic_surface_definition"]
    flag_display = _prepare_diagnostic_surface_cli_flag_display(definition["cli_flags"])
    return _DiagnosticSurfaceExplanationLineSet(
        lines=(
            f"DiagnosticSurface explanation: {definition['diagnostic_name']}",
            "  definition:",
            f"    status: {definition['status']}",
            f"    cli_flags: {flag_display.text}",
            f"    description: {definition['description']}",
            f"    supports_json: {str(definition['supports_json']).lower()}",
            f"    supports_record: {str(definition['supports_record']).lower()}",
            f"    record_scope: {definition['record_scope']}",
            _format_diagnostic_surface_boundary(
                explanation["diagnostic_surface_boundary"], indent="    "
            ),
            _format_diagnostic_surface_consumption(
                explanation["diagnostic_surface_consumption"], indent="    "
            ),
        )
    )


def diagnostic_surface_definition_json(diagnostic_surface: str) -> dict[str, object]:
    return build_diagnostic_surface_definition(diagnostic_surface)


def format_diagnostic_surface_definition(diagnostic_surface: str) -> str:
    definition = build_diagnostic_surface_definition(diagnostic_surface)[
        "diagnostic_surface_definition"
    ]
    line_set = _assemble_diagnostic_surface_definition_line_set(definition)
    return "\n".join(line_set.lines)


def _assemble_diagnostic_surface_definition_line_set(
    definition: dict[str, object],
) -> _DiagnosticSurfaceDefinitionLineSet:
    flag_display = _prepare_diagnostic_surface_cli_flag_display(definition["cli_flags"])
    return _DiagnosticSurfaceDefinitionLineSet(
        lines=(
            f"DiagnosticSurface definition: {definition['diagnostic_name']}",
            f"  status: {definition['status']}",
            f"  cli_flags: {flag_display.text}",
            f"  description: {definition['description']}",
            f"  supports_json: {str(definition['supports_json']).lower()}",
            f"  supports_record: {str(definition['supports_record']).lower()}",
            f"  record_scope: {definition['record_scope']}",
            _format_diagnostic_surface_boundary(
                definition["diagnostic_surface_boundary"]
            ),
            _format_diagnostic_surface_consumption(
                definition["diagnostic_surface_consumption"]
            ),
            f"  diagnostic_inventory_registration: {definition['diagnostic_inventory_registration']}",
            f"  shape_registration_status: {definition['shape_registration_status']}",
            f"  implementation_reason: {definition['implementation_reason']}",
            f"  evidence_source: {definition['evidence_source']}",
        )
    )


def _prepare_diagnostic_surface_cli_flag_display(
    cli_flags: object,
) -> _DiagnosticSurfaceCliFlagDisplay:
    if isinstance(cli_flags, list) and cli_flags:
        return _DiagnosticSurfaceCliFlagDisplay(
            text=", ".join(str(flag) for flag in cli_flags)
        )
    return _DiagnosticSurfaceCliFlagDisplay(text="none")


def _identify_diagnostic_surface_boundary(
    entry: DiagnosticInventoryEntry,
) -> _DiagnosticSurfaceBoundaryIdentification:
    read_only = _evaluate_diagnostic_surface_read_only_boundary(entry)
    statement_set = _assemble_diagnostic_surface_boundary_statement_set(entry)
    statements = list(statement_set.statements)
    if read_only.read_only:
        statements.insert(0, "read-only")
    return _DiagnosticSurfaceBoundaryIdentification(statements=tuple(statements))


def _assemble_diagnostic_surface_boundary_statement_set(
    entry: DiagnosticInventoryEntry,
) -> _DiagnosticSurfaceBoundaryStatementSet:
    return _DiagnosticSurfaceBoundaryStatementSet(
        statements=(
            "records" if entry.supports_record else "does not record",
            f"record_scope={entry.record_scope}",
            (
                "writes event ledger"
                if entry.writes_event_ledger
                else "does not write event ledger"
            ),
            "mutates cluster" if entry.mutates_cluster else "does not mutate cluster",
            (
                "uses projected state"
                if entry.uses_projected_state
                else "does not use projected state"
            ),
            (
                "uses repository files"
                if entry.uses_repo_files
                else "does not use repository files"
            ),
            (
                "emits diagnostic facts"
                if entry.emits_diagnostic_facts
                else "does not emit diagnostic facts"
            ),
            (
                "emits cluster facts"
                if entry.emits_cluster_facts
                else "does not emit cluster facts"
            ),
            (
                "reads diagnostic facts"
                if entry.reads_diagnostic_facts
                else "does not read diagnostic facts"
            ),
        )
    )


def _evaluate_diagnostic_surface_read_only_boundary(
    entry: DiagnosticInventoryEntry,
) -> _DiagnosticSurfaceReadOnlyEvaluation:
    return _DiagnosticSurfaceReadOnlyEvaluation(
        read_only=(
            not entry.supports_record
            and not entry.writes_event_ledger
            and not entry.mutates_cluster
            and not entry.emits_diagnostic_facts
            and not entry.emits_cluster_facts
        )
    )


def _diagnostic_surface_boundary(
    identification: _DiagnosticSurfaceBoundaryIdentification,
) -> dict[str, object]:
    return identification.to_json_dict()


def _identify_diagnostic_surface_consumption(
    entry: DiagnosticInventoryEntry,
) -> _DiagnosticSurfaceConsumptionIdentification:
    declaration_set = _assemble_diagnostic_surface_consumption_declaration_set(entry)
    return _DiagnosticSurfaceConsumptionIdentification(
        uses_projected_state=declaration_set.uses_projected_state,
        uses_repo_files=declaration_set.uses_repo_files,
        reads_diagnostic_facts=declaration_set.reads_diagnostic_facts,
    )


def _assemble_diagnostic_surface_consumption_declaration_set(
    entry: DiagnosticInventoryEntry,
) -> _DiagnosticSurfaceConsumptionDeclarationSet:
    return _DiagnosticSurfaceConsumptionDeclarationSet(
        uses_projected_state=entry.uses_projected_state,
        uses_repo_files=entry.uses_repo_files,
        reads_diagnostic_facts=entry.reads_diagnostic_facts,
    )


def _diagnostic_surface_consumption(
    identification: _DiagnosticSurfaceConsumptionIdentification,
) -> dict[str, object]:
    return identification.to_json_dict()


def _format_diagnostic_surface_boundary(boundary: object, indent: str = "  ") -> str:
    boundary_text = _prepare_diagnostic_surface_boundary_text(boundary)
    return f"{indent}diagnostic_surface_boundary: {boundary_text.text}"


def _prepare_diagnostic_surface_boundary_text(
    boundary: object,
) -> _DiagnosticSurfaceBoundaryText:
    sequence = _extract_diagnostic_surface_boundary_statement_sequence(boundary)
    if not sequence.statements:
        return _DiagnosticSurfaceBoundaryText(text="unknown")
    return _DiagnosticSurfaceBoundaryText(
        text="; ".join(str(statement) for statement in sequence.statements)
    )


def _extract_diagnostic_surface_boundary_statement_sequence(
    boundary: object,
) -> _DiagnosticSurfaceBoundaryStatementSequence:
    if not isinstance(boundary, dict):
        return _DiagnosticSurfaceBoundaryStatementSequence(statements=())
    statements = boundary.get("statements")
    if not isinstance(statements, list) or not statements:
        return _DiagnosticSurfaceBoundaryStatementSequence(statements=())
    return _DiagnosticSurfaceBoundaryStatementSequence(
        statements=tuple(str(statement) for statement in statements)
    )


def _format_diagnostic_surface_consumption(
    consumption: object, indent: str = "  "
) -> str:
    consumption_text = _prepare_diagnostic_surface_consumption_text(consumption)
    return f"{indent}diagnostic_surface_consumption: {consumption_text.text}"


def _prepare_diagnostic_surface_consumption_text(
    consumption: object,
) -> _DiagnosticSurfaceConsumptionText:
    if not isinstance(consumption, dict):
        return _DiagnosticSurfaceConsumptionText(text="unknown")
    declared = consumption.get("declared_consumption")
    if not isinstance(declared, dict) or not declared:
        return _DiagnosticSurfaceConsumptionText(text="unknown")
    items = [f"{key}={str(value).lower()}" for key, value in declared.items()]
    return _DiagnosticSurfaceConsumptionText(text="; ".join(items))


def _identify_diagnostic_surface_shape_registration(
    diagnostic_name: str,
) -> _DiagnosticSurfaceShapeRegistrationIdentification:
    lookup = _lookup_diagnostic_surface_shape_registration(diagnostic_name)
    status = "present" if lookup.present else "absent"
    return _DiagnosticSurfaceShapeRegistrationIdentification(status=status)


def _lookup_diagnostic_surface_shape_registration(
    diagnostic_name: str,
) -> _DiagnosticSurfaceShapeRegistrationLookup:
    from seed_runtime.diagnostic_shape_audit import IMPLEMENTATION_SPECS

    return _DiagnosticSurfaceShapeRegistrationLookup(
        present=diagnostic_name in IMPLEMENTATION_SPECS
    )


def _diagnostic_surface_shape_registration_status(
    identification: _DiagnosticSurfaceShapeRegistrationIdentification,
) -> str:
    return identification.status


def _prepare_diagnostic_inventory_composition(
    entries: Iterable[DiagnosticInventoryEntry],
) -> _DiagnosticInventoryCompositionInput:
    return _DiagnosticInventoryCompositionInput(entries=tuple(entries))


def diagnostic_inventory_json(
    entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> list[dict[str, object]]:
    composition_input = _prepare_diagnostic_inventory_composition(entries)
    return _compose_diagnostic_inventory_json(composition_input)


def _compose_diagnostic_inventory_json(
    composition_input: _DiagnosticInventoryCompositionInput,
) -> list[dict[str, object]]:
    return [entry.to_json_dict() for entry in composition_input.entries]


def format_diagnostic_inventory(
    entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> str:
    composition_input = _prepare_diagnostic_inventory_composition(entries)
    return _compose_diagnostic_inventory(composition_input)


def _compose_diagnostic_inventory(
    composition_input: _DiagnosticInventoryCompositionInput,
) -> str:
    headers = [
        "Diagnostic",
        "CLI Flag",
        "Uses State",
        "Uses Repo Files",
        "JSON",
        "Record",
        "Record Scope",
        "Emits Facts",
        "Mutates Cluster",
        "Notes",
    ]
    rows = [
        [
            entry.name,
            ", ".join(entry.cli_flags),
            _yes_no(entry.uses_projected_state),
            _yes_no(entry.uses_repo_files),
            _yes_no(entry.supports_json),
            _yes_no(entry.supports_record),
            entry.record_scope,
            _emits_facts_label(entry),
            _yes_no(entry.mutates_cluster),
            _notes(entry),
        ]
        for entry in composition_input.entries
    ]
    widths = [
        max(len(row[index]) for row in [headers, *rows])
        for index in range(len(headers))
    ]
    rendered = [_render_row(headers, widths)]
    rendered.extend(_render_row(row, widths) for row in rows)
    return "\n".join(rendered)


def _render_row(row: list[str], widths: list[int]) -> str:
    return " | ".join(value.ljust(widths[index]) for index, value in enumerate(row))


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _emits_facts_label(entry: DiagnosticInventoryEntry) -> str:
    if entry.emits_diagnostic_facts and entry.emits_cluster_facts:
        return "diagnostic and cluster facts"
    if entry.emits_diagnostic_facts:
        return "diagnostic facts"
    if entry.emits_cluster_facts:
        return "cluster facts"
    return "no"


def _notes(entry: DiagnosticInventoryEntry) -> str:
    notes = [entry.description]
    if entry.supports_record:
        notes.append("recorded subjects use diagnostic_run:<id>")
    if entry.writes_event_ledger:
        notes.append("writes_event_ledger=true")
    if entry.reads_diagnostic_facts:
        notes.append("reads_diagnostic_facts=true")
    return " ".join(notes)
