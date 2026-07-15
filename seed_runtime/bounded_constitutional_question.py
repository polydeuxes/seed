"""Deterministic bounded constitutional question production.

This module owns only the Operator Inquiry -> BoundedConstitutionalQuestion
boundary. It preserves explicit caller inputs as evidence/testimony without
projecting views, discovering capabilities, selecting authority, writing ledgers,
or mutating cluster state.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.serialization import to_plain


FORMULATION_CONVENTION = "bounded_constitutional_question_formulation_v1"


class BoundedConstitutionalQuestionFormulationError(ValueError):
    """Deterministic validation failure for bounded-question formulation."""


@dataclass(frozen=True)
class BoundedConstitutionalQuestion:
    """Immutable provenance-preserving bounded constitutional question artifact."""

    bounded_question_id: str
    operator_inquiry: str
    inquiry_provenance: str
    bounded_question: str
    constitutional_intent: str
    scope_status: str
    uncertainty: tuple[str, ...]
    unknowns: tuple[str, ...]
    caller_supplied_fields: tuple[tuple[str, str], ...] = ()
    testimony_status: str = "operator testimony preserved as evidence, not established fact"
    read_only_boundaries: tuple[str, ...] = (
        "operator inquiry preserved as received",
        "explicit caller-supplied bounded fields only",
        "no natural-language classification",
        "no established fact promotion",
        "no verified claim promotion",
        "no constitutional authority creation",
        "no repository truth creation",
        "no durable knowledge creation",
        "no authoritative capability creation",
        "no constitutional view selection",
        "no QuestionProjection production",
        "no event-ledger writes",
        "no cluster mutation",
    )
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False


def _tuple_of_strings(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(str(value) for value in values)


def _field_items(fields: dict[str, Any] | None) -> tuple[tuple[str, str], ...]:
    if not fields:
        return ()
    return tuple((str(key), str(value)) for key, value in sorted(fields.items()))


def _stable_question_id(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "bounded-constitutional-question:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def produce_bounded_constitutional_question(
    *,
    operator_inquiry: str,
    inquiry_provenance: str,
    bounded_question: str,
    constitutional_intent: str,
    scope_status: str,
    uncertainty: Iterable[str] = (),
    unknowns: Iterable[str] = (),
    bounded_question_id: str | None = None,
    caller_supplied_fields: dict[str, Any] | None = None,
) -> BoundedConstitutionalQuestion:
    """Produce one deterministic bounded question from explicit caller inputs only."""

    uncertainty_tuple = _tuple_of_strings(uncertainty)
    unknowns_tuple = _tuple_of_strings(unknowns)
    caller_fields_tuple = _field_items(caller_supplied_fields)

    identity_payload = {
        "operator_inquiry": operator_inquiry,
        "inquiry_provenance": inquiry_provenance,
        "bounded_question": bounded_question,
        "constitutional_intent": constitutional_intent,
        "scope_status": scope_status,
        "uncertainty": uncertainty_tuple,
        "unknowns": unknowns_tuple,
        "caller_supplied_fields": caller_fields_tuple,
    }

    return BoundedConstitutionalQuestion(
        bounded_question_id=bounded_question_id or _stable_question_id(identity_payload),
        operator_inquiry=operator_inquiry,
        inquiry_provenance=inquiry_provenance,
        bounded_question=bounded_question,
        constitutional_intent=constitutional_intent,
        scope_status=scope_status,
        uncertainty=uncertainty_tuple,
        unknowns=unknowns_tuple,
        caller_supplied_fields=caller_fields_tuple,
    )


def _sorted_unique(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values if value}))


def _csv(values: Iterable[str], fallback: str = "unspecified") -> str:
    vals = tuple(str(value) for value in values if value)
    return ", ".join(vals) if vals else fallback


def _focus(interpretation: OperatorExpressionInterpretationProjection) -> str:
    parts = (
        *interpretation.relation_or_focus_expressions,
        *interpretation.subject_expressions,
        *interpretation.object_expressions,
    )
    return _csv(parts, "requested focus")


def _constitutional_intent(kind: str, activity: str) -> str:
    if activity == "constitutional_read":
        if kind == "explain":
            return "examine current constitutional State limitations and Unknowns"
        if kind == "support":
            return "examine current constitutional support and provenance boundaries"
        if kind == "unknowns":
            return "examine current constitutional Unknowns"
        if kind == "limitations":
            return "examine current constitutional limitations"
        return "examine current constitutional State"
    if activity in {
        "local_passive_observation",
        "network_active_observation",
        "local_privileged_observation",
        "external_effectful_movement",
    }:
        return "determine lawful constitutional movement without authorization or execution"
    return "formulate bounded constitutional inquiry without downstream selection"


def _formulated_question(
    kind: str,
    activity: str,
    focus: str,
    bound_scope: tuple[str, ...],
    constraints: tuple[str, ...],
) -> str:
    scope = _csv(bound_scope, "the permitted bound scope")
    constraint_text = (
        f" under operator-stated constraints {_csv(constraints)}" if constraints else ""
    )
    if activity == "network_active_observation":
        return (
            "determine the lawful constitutional road, if any, for the permitted "
            f"network-active observation request within bound scope {scope}{constraint_text}"
        )
    if activity == "local_passive_observation":
        return (
            "determine the next lawful movement, if any, for local-passive "
            f"observation of the bound scope {scope}{constraint_text}"
        )
    if activity == "local_privileged_observation":
        return (
            "determine the next lawful movement, if any, for privileged inspection "
            f"of the bound scope {scope}{constraint_text}"
        )
    if activity == "external_effectful_movement":
        return (
            "determine whether and through what bounded constitutional road the "
            f"permitted movement request may advance within bound scope {scope}{constraint_text}, "
            "without authorizing it"
        )
    if kind == "explain":
        return (
            "explain the current constitutional limitations, support boundaries, "
            f"and Unknowns concerning {focus} within bound scope {scope}"
        )
    if kind == "support":
        return (
            f"identify the bounded support and provenance relevant to {focus} "
            f"within bound scope {scope}"
        )
    if kind == "unknowns":
        return (
            f"identify unresolved constitutional material concerning {focus} "
            f"within bound scope {scope}"
        )
    if kind == "limitations":
        return (
            "identify the constraints preventing the requested stronger conclusion "
            f"or movement concerning {focus} within bound scope {scope}"
        )
    return (
        f"identify the bounded relation or state requested for {focus} "
        f"within bound scope {scope}"
    )


def _validate_formulation_inputs(
    expression: Any,
    interpretation: Any,
    binding: Any,
    handoff: Any,
) -> None:
    if binding.binding_state != "permitted":
        raise BoundedConstitutionalQuestionFormulationError("authority/scope binding is not permitted")
    if binding.future_bounded_question_handoff != handoff:
        raise BoundedConstitutionalQuestionFormulationError("future bounded-question handoff mismatch")
    checks = (
        (handoff.authority_scope_binding_ref, binding.binding_projection_id, "binding identity mismatch"),
        (handoff.interpretation_projection_ref, binding.interpretation_projection_ref, "handoff interpretation mismatch"),
        (handoff.interpretation_projection_ref, interpretation.interpretation_projection_id, "interpretation identity mismatch"),
        (handoff.attributed_expression_ref, binding.attributed_expression_ref, "handoff attributed expression mismatch"),
        (handoff.attributed_expression_ref, expression.expression_id, "attributed expression identity mismatch"),
        (interpretation.attributed_expression_ref, expression.expression_id, "interpretation attributed expression mismatch"),
        (handoff.operator_identity_ref, binding.operator_identity_ref, "operator identity mismatch"),
        (expression.operator_ref, binding.operator_identity_ref.removeprefix("operator:verified:"), "operator identity mismatch"),
        (handoff.workspace_ref, binding.workspace_ref, "workspace identity mismatch"),
        (expression.workspace_ref, binding.workspace_ref, "workspace identity mismatch"),
        (handoff.session_ref, binding.session_ref, "session identity mismatch"),
        (expression.session_ref, binding.session_ref, "session identity mismatch"),
        (handoff.inquiry_or_request_kind, binding.inquiry_or_request_kind, "request/inquiry kind mismatch"),
        (handoff.inquiry_or_request_kind, interpretation.inquiry_or_request_kind, "interpretation request/inquiry kind mismatch"),
        (handoff.requested_activity_class, binding.requested_activity_class, "requested activity class mismatch"),
        (tuple(handoff.requested_scope_expressions), tuple(binding.requested_scope_expressions), "requested scope expressions mismatch"),
        (tuple(handoff.bound_scope_refs), tuple(binding.permitted_scope_refs), "bound/permitted scope mismatch"),
        (tuple(handoff.excluded_scope_refs), tuple(binding.excluded_scope_refs), "excluded scope mismatch"),
        (tuple(handoff.operator_stated_effect_constraints), tuple(binding.operator_stated_effect_constraints), "operator-stated constraints mismatch"),
        (handoff.presentation_preference, binding.presentation_preference, "presentation preference mismatch"),
    )
    for left, right, message in checks:
        if left != right:
            raise BoundedConstitutionalQuestionFormulationError(message)
    if tuple(handoff.provenance) != tuple(_sorted_unique((*binding.provenance, *interpretation.provenance))):
        # Binding handoffs intentionally carry the applicable interpretation/scope
        # provenance subset; require it to remain present without reconstructing it.
        if not set(handoff.provenance).issubset(set((*binding.provenance, *interpretation.provenance))):
            raise BoundedConstitutionalQuestionFormulationError("provenance references mismatch")


def formulate_bounded_constitutional_question(
    *,
    expression: Any,
    interpretation: Any,
    binding: Any,
    handoff: Any | None = None,
    formulation_convention: str = FORMULATION_CONVENTION,
    formulation_unknowns: Iterable[str] = (),
) -> BoundedConstitutionalQuestion:
    """Formulate one canonical bounded question from one permitted ingress binding."""

    actual_handoff = handoff or binding.future_bounded_question_handoff
    if actual_handoff is None:
        raise BoundedConstitutionalQuestionFormulationError("future bounded-question handoff is absent")
    _validate_formulation_inputs(expression, interpretation, binding, actual_handoff)
    focus = _focus(interpretation)
    constraints = _sorted_unique(binding.operator_stated_effect_constraints)
    question = _formulated_question(
        binding.inquiry_or_request_kind,
        binding.requested_activity_class,
        focus,
        binding.permitted_scope_refs,
        constraints,
    )
    intent = _constitutional_intent(binding.inquiry_or_request_kind, binding.requested_activity_class)
    scope_status = (
        f"permitted_scope={_csv(binding.permitted_scope_refs, 'none')}; "
        f"requested_scope={_csv(binding.requested_scope_expressions, 'none')}; "
        f"excluded_scope={_csv(binding.excluded_scope_refs, 'none')}; "
        f"unresolved_scope={_csv(binding.unresolved_scope_expressions, 'none')}"
    )
    provenance = _csv(
        _sorted_unique(
            (
                *expression.provenance,
                interpretation.interpretation_projection_id,
                binding.binding_projection_id,
                *actual_handoff.provenance,
                f"formulation_convention:{formulation_convention}",
            )
        )
    )
    uncertainty = _sorted_unique(
        (
            *expression.uncertainty,
            *interpretation.unresolved_lexical_bindings,
            *interpretation.unresolved_references,
            *interpretation.known_loss,
            *binding.unresolved_scope_expressions,
            *binding.excluded_scope_refs,
            *actual_handoff.known_loss,
            *actual_handoff.conflicts,
            *binding.conflicts,
            *formulation_unknowns,
        )
    )
    unknowns = _sorted_unique(
        (*expression.unknowns, *interpretation.unknowns, *binding.unknowns, *actual_handoff.unknowns)
    )
    caller_fields = {
        "exact_operator_expression": expression.exact_text,
        "requested_scope_expressions": _csv(binding.requested_scope_expressions, "none"),
    }
    if constraints:
        caller_fields["operator_stated_effect_constraints"] = _csv(constraints)
    if binding.presentation_preference:
        caller_fields["presentation_preference"] = binding.presentation_preference
    if binding.excluded_scope_refs:
        caller_fields["excluded_original_scope"] = _csv(binding.excluded_scope_refs)
    return produce_bounded_constitutional_question(
        operator_inquiry=expression.exact_text,
        inquiry_provenance=provenance,
        bounded_question=question,
        constitutional_intent=intent,
        scope_status=scope_status,
        uncertainty=uncertainty,
        unknowns=unknowns,
        caller_supplied_fields=caller_fields,
    )


def bounded_constitutional_question_json(
    artifact: BoundedConstitutionalQuestion,
) -> dict[str, Any]:
    """Return deterministic JSON-ready bounded-question data."""

    return to_plain(artifact)


def format_bounded_constitutional_question(
    artifact: BoundedConstitutionalQuestion,
) -> str:
    """Return a stable human-readable bounded-question rendering."""

    lines = [
        "Bounded Constitutional Question",
        f"bounded_question_id: {artifact.bounded_question_id}",
        f"operator_inquiry: {artifact.operator_inquiry}",
        f"bounded_question: {artifact.bounded_question}",
        f"constitutional_intent: {artifact.constitutional_intent}",
        f"scope_status: {artifact.scope_status}",
        f"inquiry_provenance: {artifact.inquiry_provenance}",
        f"testimony_status: {artifact.testimony_status}",
        f"read_only: {str(artifact.read_only).lower()}",
        f"writes_event_ledger: {str(artifact.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(artifact.mutates_cluster).lower()}",
    ]
    for label, values in (
        ("uncertainty", artifact.uncertainty),
        ("unknowns", artifact.unknowns),
        ("caller_supplied_fields", tuple(f"{k}={v}" for k, v in artifact.caller_supplied_fields)),
        ("read_only_boundaries", artifact.read_only_boundaries),
    ):
        lines.append(label + ":")
        lines += [f"- {value}" for value in values] or ["- none"]
    return "\n".join(lines)
