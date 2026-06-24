"""Static inventory of question families and answering Seed surfaces."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class QuestionSurfaceInventoryRow:
    question_family: str
    example_questions: tuple[str, ...]
    surface: str
    surface_flag: str
    answer_responsibility: str
    authority_boundary: str
    notes: str

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["example_questions"] = list(self.example_questions)
        return data


def build_question_surface_inventory() -> tuple[QuestionSurfaceInventoryRow, ...]:
    """Return deterministic, read-only question-family inventory rows."""

    return (
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
        lines.append(f"  responsibility: {row.answer_responsibility}")
        lines.append(f"  boundary: {row.authority_boundary}")
    return "\n".join(lines)
