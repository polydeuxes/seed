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


@dataclass(frozen=True)
class ExactQuestionFamilyLookupResult:
    """Inventory-backed exact QuestionFamily lookup for selection surfaces.

    This private handoff owns only the lookup result needed before bounded
    eligibility. It does not own eligibility classification, dispatch surface
    selection, required-argument handling, diagnostics, presentation, rendering,
    or mutation.
    """

    question_family: str


def _lookup_exact_question_family(
    question_family: str,
    rows: tuple["QuestionSurfaceInventoryRow", ...] | None = None,
) -> ExactQuestionFamilyLookupResult:
    """Return an inventory-backed exact QuestionFamily or reject the text."""

    inventory = rows or build_question_surface_inventory()
    for row in inventory:
        if row.question_family == question_family:
            return ExactQuestionFamilyLookupResult(question_family=row.question_family)
    raise ValueError(f"unknown Question Family: {question_family}")


@dataclass(frozen=True)
class _QuestionFamilyEligibilityInput:
    """Prepared exact QuestionFamily text for bounded work eligibility only.

    This private handoff carries externally supplied question-family text after
    exact inventory admission. It does not own dispatch selection, presentation,
    rendering, surface arguments, or public result shape.
    """

    question_family: str


def _prepare_question_family_eligibility_input(
    question_family: str,
    rows: tuple["QuestionSurfaceInventoryRow", ...] | None = None,
) -> _QuestionFamilyEligibilityInput:
    """Prepare exact QuestionFamily text for bounded eligibility evaluation.

    The preparation boundary is intentionally narrow: it admits only an exact
    inventory-backed question family and returns the text needed by bounded
    eligibility. It does not classify free text, select a dispatch surface,
    validate surface arguments, compose presentation, render output, or mutate
    runtime state.
    """

    lookup_result = _lookup_exact_question_family(question_family, rows)
    return _QuestionFamilyEligibilityInput(
        question_family=lookup_result.question_family
    )


@dataclass(frozen=True)
class BoundedWorkEligibilityResult:
    """Implementation-backed permission result for exact QuestionFamily invocation."""

    question_family: str
    bounded_status: str
    permitted: bool
    required_surface_args: tuple[str, ...] = ()
    reason: str = ""


def _bounded_work_eligibility_for_prepared_question_family(
    prepared_input: _QuestionFamilyEligibilityInput,
) -> BoundedWorkEligibilityResult:
    """Return bounded work eligibility for prepared exact QuestionFamily text."""

    question_family = prepared_input.question_family
    bounded_status = bounded_status_for_question_family(question_family)
    required_surface_args = BOUNDED_ASK_REQUIRED_SURFACE_ARGS.get(question_family, ())
    permitted = bounded_status in {"eligible_now", "eligible_with_parameters"}
    if bounded_status == "eligible_now":
        reason = "bounded work may execute without additional surface args"
    elif bounded_status == "eligible_with_parameters":
        reason = "bounded work may execute after required surface args are provided"
    elif bounded_status == "diagnostic_only":
        reason = "diagnostic-only question family is not an inquiry-answer surface"
    else:
        reason = "no bounded ask dispatch mapping in current implementation"
    return BoundedWorkEligibilityResult(
        question_family=question_family,
        bounded_status=bounded_status,
        permitted=permitted,
        required_surface_args=required_surface_args,
        reason=reason,
    )


def bounded_work_eligibility_for_question_family(
    question_family: str,
) -> BoundedWorkEligibilityResult:
    """Return whether bounded work may execute for an exact QuestionFamily."""

    prepared_input = _prepare_question_family_eligibility_input(question_family)
    return _bounded_work_eligibility_for_prepared_question_family(prepared_input)


@dataclass(frozen=True)
class BoundedWorkSurfaceArgsResult:
    """Validated operator surface args for eligible bounded work."""

    question_family: str
    surface_args: tuple[str, ...]
    required_surface_args: tuple[str, ...] = ()
    reason: str = ""


def bounded_work_surface_args_for_eligibility(
    question_family: str,
    eligibility: BoundedWorkEligibilityResult,
    surface_args: tuple[str, ...] | None = None,
) -> BoundedWorkSurfaceArgsResult:
    """Validate surface args for already eligible bounded work.

    This recovers only the argument-satisfaction boundary used before bounded
    work selection. It does not decide exact lookup, eligibility, selected
    dispatch surface, CLI mutation, presentation, rendering, or semantic routing.
    """

    if eligibility.question_family != question_family:
        raise ValueError("eligibility result question family does not match surface args")
    if eligibility.bounded_status == "eligible_now":
        if surface_args is not None:
            raise ValueError(
                f"Question Family '{question_family}' does not accept --surface-args by "
                "current implementation-backed eligibility"
            )
        return BoundedWorkSurfaceArgsResult(
            question_family=question_family,
            surface_args=(),
            required_surface_args=(),
            reason="bounded work does not require operator surface args",
        )
    if eligibility.bounded_status == "eligible_with_parameters":
        required_count = len(eligibility.required_surface_args)
        if surface_args is None:
            raise ValueError(
                f"Question Family '{question_family}' requires --surface-args with "
                f"exactly {required_count} explicit operator-provided value(s)"
            )
        if len(surface_args) != required_count:
            raise ValueError(
                f"Question Family '{question_family}' requires exactly {required_count} "
                f"--surface-args value(s); received {len(surface_args)}"
            )
        return BoundedWorkSurfaceArgsResult(
            question_family=question_family,
            surface_args=surface_args,
            required_surface_args=eligibility.required_surface_args,
            reason="bounded work required operator surface args are satisfied",
        )
    raise ValueError("surface args require permitted bounded work eligibility")


@dataclass(frozen=True)
class BoundedWorkSelectionResult:
    """Implementation-backed selected bounded work for an eligible QuestionFamily."""

    question_family: str
    dispatch_surface: str
    surface_value: object
    required_surface_args: tuple[str, ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class BoundedWorkDispatchRequest:
    """Implementation-backed invocation request for already selected bounded work."""

    question_family: str
    dispatch_surface: str
    surface_value: object
    reason: str = ""


def bounded_work_dispatch_request_for_selection(
    selection: BoundedWorkSelectionResult,
) -> BoundedWorkDispatchRequest:
    """Describe how selected bounded work is invoked by the existing CLI surface.

    This recovers only the dispatch invocation already used by bounded ask; it
    does not decide QuestionFamily lookup, eligibility, bounded work selection,
    evidence interpretation, answer composition, rendering, or semantic routing.
    """

    return BoundedWorkDispatchRequest(
        question_family=selection.question_family,
        dispatch_surface=selection.dispatch_surface,
        surface_value=selection.surface_value,
        reason="dispatch selected bounded work through existing CLI namespace",
    )


@dataclass(frozen=True)
class BoundedWorkDispatchResult:
    """Implementation-backed result of executing a bounded work dispatch request."""

    question_family: str
    dispatch_surface: str
    surface_value: object
    reason: str = ""


def execute_bounded_work_dispatch(
    args: object,
    dispatch_request: BoundedWorkDispatchRequest,
) -> BoundedWorkDispatchResult:
    """Perform the existing bounded work invocation on the CLI namespace.

    This recovers only the dispatch execution already used by bounded ask; it
    does not decide QuestionFamily lookup, eligibility, bounded work selection,
    dispatch request construction, answer composition, rendering, evidence
    interpretation, or semantic routing.
    """

    setattr(
        args,
        dispatch_request.dispatch_surface,
        dispatch_request.surface_value,
    )
    return BoundedWorkDispatchResult(
        question_family=dispatch_request.question_family,
        dispatch_surface=dispatch_request.dispatch_surface,
        surface_value=dispatch_request.surface_value,
        reason="performed bounded work dispatch through existing CLI namespace",
    )


def bounded_work_selection_for_question_family(
    question_family: str,
    eligibility: BoundedWorkEligibilityResult,
    surface_args_result: BoundedWorkSurfaceArgsResult | None = None,
) -> BoundedWorkSelectionResult:
    """Select existing bounded work for an eligible exact QuestionFamily.

    This recovers only the map-backed selection already used by bounded ask; it
    does not decide eligibility, dispatch execution, argument mutation, answer
    composition, rendering, or evidence semantics.
    """

    if eligibility.question_family != question_family:
        raise ValueError("eligibility result question family does not match selection")
    if not eligibility.permitted:
        raise ValueError("bounded work selection requires permitted eligibility")
    dispatch_surface = BOUNDED_ASK_DISPATCH_SURFACES[question_family]
    required_surface_args = eligibility.required_surface_args
    if required_surface_args:
        if surface_args_result is None:
            surface_args_result = bounded_work_surface_args_for_eligibility(
                question_family, eligibility
            )
        provided_surface_args = surface_args_result.surface_args
        surface_value = (
            provided_surface_args[0]
            if len(provided_surface_args) == 1
            else provided_surface_args
        )
        reason = "selected parameterized bounded ask dispatch surface"
    else:
        surface_value = BOUNDED_ASK_ARG_VALUES.get(question_family, True)
        reason = "selected bounded ask dispatch surface"
    return BoundedWorkSelectionResult(
        question_family=question_family,
        dispatch_surface=dispatch_surface,
        surface_value=surface_value,
        required_surface_args=required_surface_args,
        reason=reason,
    )


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
class ComposedQuestionFamilyExplanation:
    question_family: str
    composed_question_family_explanation: dict[str, object]

    def to_json_dict(self) -> dict[str, object]:
        return {
            "question_family": self.question_family,
            "composed_question_family_explanation": self.composed_question_family_explanation,
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
                "question_family_diagnostic_relationship": {
                    "status": "unknown",
                    "canonical_diagnostic_surface": "unknown",
                    "dispatch_surface": "unknown",
                    "diagnostic_inventory_name": "unknown",
                    "diagnostic_shape_spec_name": "unknown",
                    "relationship_status": "unknown",
                    "implementation_reason": "unknown question family; no question-surface inventory row exists",
                    "evidence_source": "question_surface_inventory",
                },
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
            "question_family_diagnostic_relationship": {
                "status": "known",
                "canonical_diagnostic_surface": row.canonical_diagnostic_surface
                or "none",
                "dispatch_surface": row.dispatch_surface or "none",
                "diagnostic_inventory_name": row.diagnostic_inventory_name or "none",
                "diagnostic_shape_spec_name": row.diagnostic_shape_spec_name or "none",
                "relationship_status": row.relationship_status,
                "implementation_reason": row.implementation_reason,
                "evidence_source": "question_surface_inventory",
            },
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
        "  question_family_diagnostic_relationship:",
        f"    canonical_diagnostic_surface: {definition['question_family_diagnostic_relationship']['canonical_diagnostic_surface']}",
        f"    dispatch_surface: {definition['question_family_diagnostic_relationship']['dispatch_surface']}",
        f"    diagnostic_inventory_name: {definition['question_family_diagnostic_relationship']['diagnostic_inventory_name']}",
        f"    diagnostic_shape_spec_name: {definition['question_family_diagnostic_relationship']['diagnostic_shape_spec_name']}",
        f"    relationship_status: {definition['question_family_diagnostic_relationship']['relationship_status']}",
        f"    implementation_reason: {definition['question_family_diagnostic_relationship']['implementation_reason']}",
        f"    evidence_source: {definition['question_family_diagnostic_relationship']['evidence_source']}",
        f"  implementation_reason: {definition['implementation_reason']}",
        f"  evidence_source: {definition['evidence_source']}",
    ]
    if definition["status"] == "known":
        lines.insert(
            5, f"  surface: {definition['surface']} ({definition['surface_flag']})"
        )
    return "\n".join(lines)


def build_composed_question_family_explanation(
    question_family: str,
    rows: tuple[QuestionSurfaceInventoryRow, ...] | None = None,
) -> ComposedQuestionFamilyExplanation:
    """Compose existing QuestionFamily explanation fields for presentation only."""

    explanation = build_question_family_definition(question_family, rows)
    definition = explanation.question_family_definition
    composed = {
        "status": definition["status"],
        "question_family": definition["question_family"],
        "evidence_source": definition["evidence_source"],
        "composition_source": "question_family_definition",
        "sections": [
            {
                "label": "Definition",
                "field": "question_family_definition",
                "value": {
                    "question_family": definition["question_family"],
                    "display_name": definition["display_name"],
                    "status": definition["status"],
                    "bounded_status": definition["bounded_status"],
                    "dispatch_surface": definition["dispatch_surface"],
                },
            },
            {
                "label": "Answer responsibility",
                "field": "question_family_answer_responsibility",
                "value": definition["question_family_answer_responsibility"],
            },
            {
                "label": "Boundary",
                "field": "question_family_boundary",
                "value": definition["question_family_boundary"],
            },
            {
                "label": "Diagnostic relationship",
                "field": "question_family_diagnostic_relationship",
                "value": definition["question_family_diagnostic_relationship"],
            },
        ],
    }
    return ComposedQuestionFamilyExplanation(
        question_family=explanation.question_family,
        composed_question_family_explanation=composed,
    )


def composed_question_family_explanation_json(
    question_family: str,
    rows: tuple[QuestionSurfaceInventoryRow, ...] | None = None,
) -> dict[str, object]:
    return build_composed_question_family_explanation(question_family, rows).to_json_dict()


def format_composed_question_family_explanation(
    question_family: str,
    rows: tuple[QuestionSurfaceInventoryRow, ...] | None = None,
) -> str:
    explanation = build_composed_question_family_explanation(question_family, rows)
    composed = explanation.composed_question_family_explanation
    sections = composed["sections"]
    definition_section = sections[0]["value"]
    answer_section = sections[1]["value"]
    boundary = sections[2]["value"]
    diagnostic_section = sections[3]["value"]
    lines = [
        f"QuestionFamily explanation: {composed['question_family']}",
        f"  status: {composed['status']}",
        f"  evidence_source: {composed['evidence_source']}",
        "",
        "Definition:",
        f"  display_name: {definition_section['display_name']}",
        f"  bounded_status: {definition_section['bounded_status']}",
        f"  dispatch_surface: {definition_section['dispatch_surface']}",
        "",
        "Answer responsibility:",
        f"  answer_responsibility: {answer_section['answer_responsibility']}",
        f"  responsible_answering_surface: {answer_section['responsible_answering_surface']}",
        f"  implementation_reason: {answer_section['implementation_reason']}",
        "",
        "Boundary:",
        f"  {boundary}",
        "",
        "Diagnostic relationship:",
        f"  canonical_diagnostic_surface: {diagnostic_section['canonical_diagnostic_surface']}",
        f"  diagnostic_inventory_name: {diagnostic_section['diagnostic_inventory_name']}",
        f"  diagnostic_shape_spec_name: {diagnostic_section['diagnostic_shape_spec_name']}",
        f"  relationship_status: {diagnostic_section['relationship_status']}",
    ]
    return "\n".join(lines)
