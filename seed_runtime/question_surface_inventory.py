"""Static inventory of question families and answering Seed surfaces."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import IMPLEMENTATION_SPECS

BOUNDED_ASK_DISPATCH_SURFACES: dict[str, str] = {
    "operational pressure": "ops_brief",
    "current operational explanation": "operational_story",
    "knowledge reachability": "knowledge_reachability_audit",
    "capability pressure": "capability_needs",
    "ownership ambiguity": "ownership_discrepancies",
    "observation domain coverage": "observation_domains",
    "observation permission state": "observation_permission",
    "authority-constrained container ownership": "container_ownership_authority",
    "authority-constrained service ownership": "service_ownership_authority",
    "listener endpoint reachability": "listener_endpoint_authority",
    "projection shape visibility": "projection_shape",
    "derivation explanation": "reasoning_path",
    "selection explanation": "selection_path",
}

BOUNDED_ASK_REQUIRED_SURFACE_ARGS: dict[str, tuple[str, ...]] = {
    "derivation explanation": ("domain", "subject"),
    "selection explanation": ("target",),
}

BOUNDED_ASK_DIAGNOSTIC_ONLY_FAMILIES: frozenset[str] = frozenset(
    {
        "surface inventory",
        "surface shape validation",
    }
)

BOUNDED_ASK_ARG_VALUES: dict[str, object] = {
    "observation domain coverage": "__all__",
    "observation permission state": "__all__",
}

CANONICAL_DIAGNOSTIC_SURFACE_ALIASES: dict[str, str] = {
    "knowledge_reachability_audit": "knowledge_reachability",
}


def canonical_diagnostic_surface(surface: str) -> str:
    """Return implementation-backed diagnostic surface name for a dispatch surface."""

    return CANONICAL_DIAGNOSTIC_SURFACE_ALIASES.get(surface, surface)


def bounded_status_for_question_family(question_family: str) -> str:
    """Derive bounded ask status from executable dispatch maps."""

    if question_family in BOUNDED_ASK_REQUIRED_SURFACE_ARGS:
        return "eligible_with_parameters"
    if question_family in BOUNDED_ASK_DISPATCH_SURFACES:
        return "eligible_now"
    if question_family in BOUNDED_ASK_DIAGNOSTIC_ONLY_FAMILIES:
        return "diagnostic_only"
    return "not_dispatchable"


def bounded_ask_inventory_findings(
    rows: tuple["QuestionSurfaceInventoryRow", ...] | None = None,
) -> tuple[str, ...]:
    """Validate inventory rows against bounded ask implementation maps."""

    inventory = rows or build_question_surface_inventory()
    families = [row.question_family for row in inventory]
    findings: list[str] = []
    duplicates = sorted({family for family in families if families.count(family) > 1})
    if duplicates:
        findings.append("duplicate_question_families=" + ",".join(duplicates))
    row_families = set(families)
    dispatch_families = set(BOUNDED_ASK_DISPATCH_SURFACES)
    missing_rows = sorted(dispatch_families - row_families)
    if missing_rows:
        findings.append("orphaned_bounded_mappings=" + ",".join(missing_rows))
    missing_mappings = sorted(
        family
        for family in row_families
        if bounded_status_for_question_family(family)
        not in {
            "eligible_now",
            "eligible_with_parameters",
            "diagnostic_only",
            "not_dispatchable",
        }
    )
    if missing_mappings:
        findings.append(
            "question_families_missing_bounded_visibility=" + ",".join(missing_mappings)
        )
    return tuple(findings)


@dataclass(frozen=True)
class QuestionFamilyDefinition:
    question_family: str
    question_family_definition: dict[str, object]

    def to_json_dict(self) -> dict[str, object]:
        return {
            "question_family": self.question_family,
            "question_family_definition": self.question_family_definition,
        }


@dataclass(frozen=True)
class QuestionSurfaceInventoryRow:
    question_family: str
    example_questions: tuple[str, ...]
    surface: str
    surface_flag: str
    answer_responsibility: str
    authority_boundary: str
    notes: str
    bounded_status: str = ""
    dispatch_surface: str = ""
    required_surface_args: tuple[str, ...] = ()
    json_support: bool = True
    human_formatter: str = ""
    implementation_reason: str = ""
    canonical_diagnostic_surface: str = ""
    diagnostic_inventory_name: str = ""
    diagnostic_shape_spec_name: str = ""
    relationship_status: str = ""

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["example_questions"] = list(self.example_questions)
        data["required_surface_args"] = list(self.required_surface_args)
        return data


def build_question_surface_inventory() -> tuple[QuestionSurfaceInventoryRow, ...]:
    """Return deterministic, read-only question-family inventory rows."""

    rows = (
        QuestionSurfaceInventoryRow(
            question_family="operational pressure",
            example_questions=(
                "What should I care about right now?",
                "What operational pressure exists?",
            ),
            surface="ops_brief",
            surface_flag="--ops-brief",
            answer_responsibility="compact operational pressure and visibility summary",
            authority_boundary="read-only summary assembled from existing audits; no recording; no mutation",
            notes="Inventory row only; does not route operator questions.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="current operational explanation",
            example_questions=(
                "What is happening operationally?",
                "Why is capability pressure currently active?",
            ),
            surface="operational_story",
            surface_flag="--operational-story",
            answer_responsibility="broad operational explanation from existing evidence, pressure, constraints, outcomes, and investigation path",
            authority_boundary="read-only view; no recording; no event-ledger writes; no cluster mutation",
            notes="Composes existing surfaces; does not provide implementation advice.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="derivation explanation",
            example_questions=(
                "Where did this operational conclusion come from?",
                "Which evidence supports this conclusion?",
            ),
            surface="reasoning_path",
            surface_flag="--reasoning-path",
            answer_responsibility="evidence-backed derivation path from source evidence through conclusions and consumers",
            authority_boundary="read-only audit; no recording; no event-ledger writes; no cluster mutation",
            notes="Requires explicit domain and subject arguments; this inventory does not infer them.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="selection explanation",
            example_questions=(
                "Why was this operational conclusion selected?",
                "Which candidates or alternatives were considered?",
            ),
            surface="selection_path",
            surface_flag="--selection-path",
            answer_responsibility="implementation-backed selection path with candidates, factors, alternatives, and outcome",
            authority_boundary="read-only audit; no recording; no event-ledger writes; no cluster mutation",
            notes="Requires an explicit target argument; this inventory does not infer targets.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="knowledge reachability",
            example_questions=(
                "Can Seed reach this knowledge from preserved or projected evidence?",
                "Where is knowledge visible or missing?",
            ),
            surface="knowledge_reachability",
            surface_flag="--knowledge-reachability-audit",
            answer_responsibility="audits reachability across preserved, projected, read-model, inquiry, and rendered surfaces",
            authority_boundary="read-only audit over projected and repository evidence; no recording; no mutation",
            notes="Use implementation evidence before promoting presentation vocabulary into knowledge.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="capability pressure",
            example_questions=(
                "Which capabilities are needed?",
                "What diagnostic capability needs have been recorded?",
            ),
            surface="capability_needs",
            surface_flag="--capability-needs",
            answer_responsibility="reports recorded diagnostic capability needs by subject",
            authority_boundary="read-only diagnostic-fact reader; no recording; no event-ledger writes; no cluster mutation",
            notes="Reports existing diagnostic facts; does not acquire capabilities.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="ownership ambiguity",
            example_questions=(
                "Where is ownership ambiguous or conflicting?",
                "Which ownership candidates exist?",
            ),
            surface="ownership_discrepancies",
            surface_flag="--ownership-discrepancies",
            answer_responsibility="reports storage/service ownership candidates, conflicts, ambiguity, and capability needs",
            authority_boundary="read-only unless --record is supplied; default inventory row describes non-recording use",
            notes="This inventory does not invoke recording.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="observation domain coverage",
            example_questions=(
                "What observation domains are covered?",
                "Which observation-domain gaps are visible?",
            ),
            surface="observation_domains",
            surface_flag="--observation-domains",
            answer_responsibility="shows observation-domain coverage and gap visibility derived from existing evidence",
            authority_boundary="read-only surface; no recording; no event-ledger writes; no cluster mutation",
            notes="Accepts an explicit domain argument or renders all domains.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="observation permission state",
            example_questions=(
                "What permission state exists for an observation domain?",
                "Is observation blocked by missing authority?",
            ),
            surface="observation_permission",
            surface_flag="--observation-permission",
            answer_responsibility="shows observation-domain permission classes, authority evidence, unknowns, and manual-invocation reasoning",
            authority_boundary="read-only visibility; no enforcement; no approval storage; no autonomous runtime behavior",
            notes="Accepts an explicit domain argument or renders all domains.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="authority-constrained container ownership",
            example_questions=(
                "Can Seed determine container ownership without Docker or root?",
                "Why is container ownership blocked?",
            ),
            surface="container_ownership_authority",
            surface_flag="--container-ownership-authority",
            answer_responsibility="evaluates container ownership reachability under the constrained authority profile",
            authority_boundary="read-only evaluator; no provider acquisition; no permission creation; no execution; no mutation",
            notes="Uses existing projected and diagnostic evidence only.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="authority-constrained service ownership",
            example_questions=(
                "Can Seed determine service ownership under current authority?",
                "Why is service ownership blocked?",
            ),
            surface="service_ownership_authority",
            surface_flag="--service-ownership-authority",
            answer_responsibility="evaluates service ownership reachability under constrained authority and implementation inventory evidence",
            authority_boundary="read-only evaluator; no provider acquisition; no execution; no event-ledger writes; no mutation",
            notes="Uses projected state and implementation inventory evidence.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="listener endpoint reachability",
            example_questions=(
                "Can Seed see local listener endpoints?",
                "Why is endpoint ownership or process context unavailable?",
            ),
            surface="listener_endpoint_authority",
            surface_flag="--listener-endpoint-authority",
            answer_responsibility="evaluates local TCP/UDP listener endpoint authority and reachability",
            authority_boundary="read-only evaluator; no provider acquisition; no execution; no event-ledger writes; no mutation",
            notes="Uses projected state and implementation inventory evidence.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="surface inventory",
            example_questions=(
                "Which operational diagnostics are declared?",
                "What shape does each diagnostic surface declare?",
            ),
            surface="diagnostic_inventory",
            surface_flag="--diagnostic-inventory",
            answer_responsibility="lists diagnostic/test-like operational surfaces and declared behavior shape",
            authority_boundary="read-only static registry; no recording; no event-ledger writes; no cluster mutation",
            notes="This row points to the diagnostic registry, not to this question-family inventory itself.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="surface shape validation",
            example_questions=(
                "Do diagnostic declarations match implementation shape?",
                "Which operational surfaces have shape mismatches?",
            ),
            surface="diagnostic_shape_audit",
            surface_flag="--diagnostic-shape-audit",
            answer_responsibility="compares diagnostic registry declarations with static implementation shape",
            authority_boundary="read-only static implementation audit; no recording; no event-ledger writes; no cluster mutation",
            notes="Checks declarations; does not execute target surfaces.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="source definition/import lookup",
            example_questions=(
                "Where is this symbol defined?",
                "Which preserved imports mention this query?",
            ),
            surface="source_navigation",
            surface_flag="--source-navigation",
            answer_responsibility="looks up preserved imports and definitions from projected facts",
            authority_boundary="read-only projected-fact view; does not inspect repository files, parse source, or append events",
            notes="Requires an explicit query argument; this inventory does not infer queries.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="inquiry orientation",
            example_questions=(
                "What bounded orientation exists for this inquiry note?",
                "Which existing navigation clues relate to a recorded inquiry note?",
            ),
            surface="inquiry_orientation",
            surface_flag="--inquiry-orientation",
            answer_responsibility="renders a bounded read-only orientation view for an inquiry note",
            authority_boundary="read-only orientation over existing inquiry note and projected state; no routing; no execution",
            notes="Requires an explicit note id or latest note; this inventory does not classify intent.",
        ),
        QuestionSurfaceInventoryRow(
            question_family="projection shape visibility",
            example_questions=(
                "What shape does the projection build expose?",
                "Which projection stages are visible?",
            ),
            surface="projection_shape",
            surface_flag="--projection-shape",
            answer_responsibility="shows implementation-backed projection stage shape",
            authority_boundary="read-only implementation-backed view; no recording; no event-ledger writes; no cluster mutation",
            notes="Does not build projected state.",
        ),
    )
    diagnostic_names = {entry.name for entry in DIAGNOSTIC_INVENTORY}
    shape_spec_names = set(IMPLEMENTATION_SPECS)
    enriched = []
    for row in rows:
        status = bounded_status_for_question_family(row.question_family)
        surface = BOUNDED_ASK_DISPATCH_SURFACES.get(row.question_family, "")
        dispatch_or_declared_surface = surface or row.surface
        canonical_surface = canonical_diagnostic_surface(dispatch_or_declared_surface)
        diagnostic_inventory_name = (
            canonical_surface if canonical_surface in diagnostic_names else ""
        )
        diagnostic_shape_spec_name = (
            canonical_surface if canonical_surface in shape_spec_names else ""
        )
        if diagnostic_inventory_name and diagnostic_shape_spec_name:
            relationship_status = "connected"
        elif not canonical_surface:
            relationship_status = "not_dispatchable"
        elif not diagnostic_inventory_name:
            relationship_status = "missing_diagnostic_inventory"
        else:
            relationship_status = "missing_diagnostic_shape_spec"
        required_args = BOUNDED_ASK_REQUIRED_SURFACE_ARGS.get(row.question_family, ())
        reason = (
            "present in bounded ask dispatch map"
            if status == "eligible_now"
            else (
                "present in bounded ask dispatch map with required surface args"
                if status == "eligible_with_parameters"
                else (
                    "question family points at diagnostic inventory/audit surface, not bounded ask dispatch"
                    if status == "diagnostic_only"
                    else "no bounded ask dispatch mapping in current implementation"
                )
            )
        )
        if canonical_surface != dispatch_or_declared_surface:
            reason += (
                f"; canonical diagnostic surface alias: "
                f"{dispatch_or_declared_surface} -> {canonical_surface}"
            )
        enriched.append(
            QuestionSurfaceInventoryRow(
                **{
                    **row.to_json_dict(),
                    "example_questions": tuple(row.example_questions),
                    "required_surface_args": required_args,
                    "bounded_status": status,
                    "dispatch_surface": surface,
                    "json_support": True,
                    "human_formatter": f"format_{row.surface}",
                    "implementation_reason": reason,
                    "canonical_diagnostic_surface": canonical_surface,
                    "diagnostic_inventory_name": diagnostic_inventory_name,
                    "diagnostic_shape_spec_name": diagnostic_shape_spec_name,
                    "relationship_status": relationship_status,
                }
            )
        )
    return tuple(enriched)


def question_surface_inventory_json(
    rows: tuple[QuestionSurfaceInventoryRow, ...] | None = None,
) -> list[dict[str, object]]:
    return [row.to_json_dict() for row in (rows or build_question_surface_inventory())]


def format_question_surface_inventory(
    rows: tuple[QuestionSurfaceInventoryRow, ...] | None = None,
) -> str:
    inventory = rows or build_question_surface_inventory()
    lines = ["Known question families and answering Seed surfaces:"]
    for row in inventory:
        lines.append("")
        lines.append(f"- {row.question_family}: {row.surface} ({row.surface_flag})")
        lines.append(f"  bounded_status: {row.bounded_status}")
        lines.append(f"  dispatch_surface: {row.dispatch_surface or 'none'}")
        lines.append(
            "  canonical_diagnostic_surface: "
            + (row.canonical_diagnostic_surface or "none")
        )
        lines.append(
            "  diagnostic_inventory_name: " + (row.diagnostic_inventory_name or "none")
        )
        lines.append(
            "  diagnostic_shape_spec_name: "
            + (row.diagnostic_shape_spec_name or "none")
        )
        lines.append(f"  relationship_status: {row.relationship_status}")
        lines.append(
            "  required_surface_args: "
            + (
                ", ".join(row.required_surface_args)
                if row.required_surface_args
                else "none"
            )
        )
        lines.append(f"  json_support: {str(row.json_support).lower()}")
        lines.append(f"  human_formatter: {row.human_formatter}")
        lines.append(f"  implementation_reason: {row.implementation_reason}")
        lines.append(f"  responsibility: {row.answer_responsibility}")
        lines.append(f"  boundary: {row.authority_boundary}")
    findings = bounded_ask_inventory_findings(inventory)
    lines.append("")
    lines.append(
        "Implementation findings: " + ("none" if not findings else "; ".join(findings))
    )
    return "\n".join(lines)


def build_question_family_definition(
    question_family: str,
    rows: tuple[QuestionSurfaceInventoryRow, ...] | None = None,
) -> QuestionFamilyDefinition:
    """Return the read-only identity explanation for one QuestionFamily."""

    inventory = rows or build_question_surface_inventory()
    matches = [row for row in inventory if row.question_family == question_family]
    if not matches:
        return QuestionFamilyDefinition(
            question_family=question_family,
            question_family_definition={
                "status": "unknown",
                "question_family": question_family,
                "display_name": question_family,
                "bounded": "unknown",
                "bounded_status": "unknown",
                "dispatch_surface": "unknown",
                "answer_responsibility": "unknown",
                "question_family_answer_responsibility": {
                    "status": "unknown",
                    "answer_responsibility": "unknown",
                    "responsible_answering_surface": "unknown",
                    "dispatch_surface": "unknown",
                    "implementation_reason": "unknown question family; no question-surface inventory row exists",
                    "relationship_status": "unknown",
                    "evidence_source": "question_surface_inventory",
                },
                "question_family_boundary": "unknown question family; no implementation-backed authority boundary exists",
                "implementation_reason": "unknown question family; no question-surface inventory row exists",
                "evidence_source": "question_surface_inventory",
            },
        )

    row = matches[0]
    return QuestionFamilyDefinition(
        question_family=row.question_family,
        question_family_definition={
            "status": "known",
            "question_family": row.question_family,
            "display_name": row.question_family,
            "bounded": row.bounded_status != "not_dispatchable",
            "bounded_status": row.bounded_status,
            "surface": row.surface,
            "surface_flag": row.surface_flag,
            "dispatch_surface": row.dispatch_surface or "none",
            "answer_responsibility": row.answer_responsibility,
            "question_family_answer_responsibility": {
                "status": "known",
                "answer_responsibility": row.answer_responsibility,
                "responsible_answering_surface": row.surface,
                "surface_flag": row.surface_flag,
                "dispatch_surface": row.dispatch_surface or "none",
                "implementation_reason": row.implementation_reason,
                "relationship_status": row.relationship_status,
                "evidence_source": "question_surface_inventory",
            },
            "question_family_boundary": row.authority_boundary,
            "implementation_reason": row.implementation_reason,
            "relationship_status": row.relationship_status,
            "evidence_source": "question_surface_inventory",
        },
    )


def question_family_definition_json(
    question_family: str,
    rows: tuple[QuestionSurfaceInventoryRow, ...] | None = None,
) -> dict[str, object]:
    return build_question_family_definition(question_family, rows).to_json_dict()


def format_question_family_definition(
    question_family: str,
    rows: tuple[QuestionSurfaceInventoryRow, ...] | None = None,
) -> str:
    explanation = build_question_family_definition(question_family, rows)
    definition = explanation.question_family_definition
    lines = [
        f"QuestionFamily definition: {definition['question_family']}",
        f"  status: {definition['status']}",
        f"  display_name: {definition['display_name']}",
        f"  bounded_status: {definition['bounded_status']}",
        f"  dispatch_surface: {definition['dispatch_surface']}",
        "  question_family_answer_responsibility:",
        f"    answer_responsibility: {definition['question_family_answer_responsibility']['answer_responsibility']}",
        f"    responsible_answering_surface: {definition['question_family_answer_responsibility']['responsible_answering_surface']}",
        f"    dispatch_surface: {definition['question_family_answer_responsibility']['dispatch_surface']}",
        f"    implementation_reason: {definition['question_family_answer_responsibility']['implementation_reason']}",
        f"    relationship_status: {definition['question_family_answer_responsibility']['relationship_status']}",
        f"  question_family_boundary: {definition['question_family_boundary']}",
        f"  implementation_reason: {definition['implementation_reason']}",
        f"  evidence_source: {definition['evidence_source']}",
    ]
    if definition["status"] == "known":
        lines.insert(
            5, f"  surface: {definition['surface']} ({definition['surface_flag']})"
        )
    return "\n".join(lines)
