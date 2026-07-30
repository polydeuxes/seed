"""One-attempt bounded operator-ingress common-grammar interaction for unknown operator common grammar."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import BinaryIO, TextIO

from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    ClosedChoiceSelectionBindingError,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
    bind_closed_choice_selection,
)
from seed_runtime.bounded_operator_goal_establishment import (
    examine_meaning_relation_applicability,
)
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_ingress_representation import (
    CapturedOperatorMaterial,
    capture_stdin_material,
    examine_text_representation,
)
from seed_runtime.state import StateProjector

CHOICE_SET_REF = "operator-ingress-common-grammar:v1:two-alternative"
PROMPT = "Select one alternative by its exact token:"
OPTIONS = (
    ClosedChoiceOption(
        "1",
        "common-grammar-acquisition",
        "Select bounded common-grammar acquisition alternative.",
    ),
    ClosedChoiceOption("2", "local-stop", "Select local stopping alternative."),
)

SOURCE_PROPOSITIONS = {
    "source:operator-common-grammar-potential-goal:v1": (
        "potential-goal candidate",
        "establish richer shared grammar with the operator",
    ),
    "source:operator-common-grammar-local-stop:v1": (
        "local-stop",
        "establish no such goal and stop locally",
    ),
}
ALTERNATIVE_SOURCES = {
    "common-grammar-acquisition": "source:operator-common-grammar-potential-goal:v1",
    "local-stop": "source:operator-common-grammar-local-stop:v1",
}
RENDERING_KNOWN_LOSS = (
    "rendered label is a compressed presentation and does not carry the complete source proposition",
)

MEANING_CONVENTION_PURPOSE = "operator-ingress common-grammar source meaning"
MEANING_CONVENTION_SCOPE = "operator-ingress-common-grammar:v1"

POTENTIAL_GOAL_SOURCE_REF = "source:operator-common-grammar-potential-goal:v1"


@dataclass(frozen=True)
class ApplicationSourceMeaningTestimony:
    testimony_id: str
    source_ref: str
    source_role: str
    proposition: str
    relation_assertion: str = "expresses"
    attributed_supplier: str = "Seed application developer declaration"
    producer_declaration_ref: str = (
        "seed_runtime.operator_ingress_common_grammar:source-declaration:v1"
    )
    declared_application_purpose: str = MEANING_CONVENTION_PURPOSE
    scope: str = MEANING_CONVENTION_SCOPE
    provenance: tuple[str, ...] = (
        "application-owned operator-ingress common-grammar declaration",
    )
    known_loss: tuple[str, ...] = RENDERING_KNOWN_LOSS
    conflicts: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    authority_limits: tuple[str, ...] = (
        "testimony asserts only the exact expresses relation and does not warrant itself",
        "no truth, applicability, admission, goal, stopping, acquisition, authority, or movement",
    )


@dataclass(frozen=True)
class ApplicationSourceMeaningConvention:
    convention_id: str = "convention:operator-common-grammar:source-meaning:v2"
    attribution: str = "Seed application developer declaration"
    permitted_testimony_kind: str = "ApplicationSourceMeaningTestimony"
    permitted_relation_form: str = "expresses"
    purpose: str = MEANING_CONVENTION_PURPOSE
    scope: str = MEANING_CONVENTION_SCOPE
    applicable_authority: tuple[str, ...] = (
        "bounded application convention for examining eligible testimony as warrant basis",
    )
    required_provenance: bool = True
    required_coordinates: tuple[str, ...] = (
        "testimony_id",
        "source_ref",
        "source_role",
        "proposition",
        "relation_assertion",
        "attributed_supplier",
        "producer_declaration_ref",
        "declared_application_purpose",
        "scope",
        "provenance",
    )
    known_limitations: tuple[str, ...] = (
        "does not declare any source-to-proposition relation",
        "is neither constitutional authority nor a universal meaning-warrant topology",
    )
    conflicts: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()


SOURCE_MEANING_TESTIMONIES = {
    source_ref: ApplicationSourceMeaningTestimony(
        f"testimony:operator-common-grammar:{source_ref.rsplit(':', 2)[-2]}:v1",
        source_ref,
        role,
        proposition,
    )
    for source_ref, (role, proposition) in SOURCE_PROPOSITIONS.items()
}
APPLICATION_SOURCE_MEANING_CONVENTION = ApplicationSourceMeaningConvention()
# Applicability maps exact local identity only; the convention contains no G or M assertion.
SOURCE_MEANING_CONVENTIONS = {
    source_ref: APPLICATION_SOURCE_MEANING_CONVENTION
    for source_ref in SOURCE_PROPOSITIONS
}


def _representation_fingerprint(representations: object) -> str:
    encoded = json.dumps(
        representations, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return "operator-ingress-representations:" + hashlib.sha256(encoded).hexdigest()


def _recordable_binding_testimony(binding) -> dict[str, object]:
    """Serialize the complete binding without using ledger-reserved secret keys."""
    testimony = binding.to_json_dict()
    testimony["presented_options"] = [
        {
            "presented_token": option.token,
            "presented_alternative_ref": option.presented_alternative_ref,
            "presented_label": option.presented_label,
            "presented_detail": option.presented_detail,
        }
        for option in binding.presented_options
    ]
    return testimony


def _recordable_presented_options(choice_set) -> list[dict[str, str]]:
    return [
        {
            "presented_token": option.token,
            "presented_alternative_ref": option.presented_alternative_ref,
            "presented_label": option.presented_label,
            "presented_detail": option.presented_detail,
        }
        for option in choice_set.options
    ]


@dataclass(frozen=True)
class AlternativeSourceRepresentation:
    presented_alternative_ref: str
    represented_source_ref: str
    represented_source_role: str
    representation_purpose: str
    choice_set_ref: str
    exact_choice_set_fingerprint: str
    presentation_ref: str
    rendered_label: str
    rendered_detail: str
    proposition_assertion: str
    representation_relation: str
    exact_set_participation: str
    source_attribution: str
    producer_occurrence_ref: str
    authority_limits: tuple[str, ...]
    provenance: tuple[str, ...]
    scope: str
    known_loss: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


@dataclass(frozen=True)
class RecoveredRepresentedSource:
    presented_alternative_ref: str
    represented_source_ref: str
    represented_source_role: str
    proposition_assertion: str
    representation_provenance: tuple[str, ...]
    representation_scope: str
    representation_known_loss: tuple[str, ...]
    representation_occurrence_id: str
    binding_occurrence_id: str


def _warrant_source_meaning_relation(
    *,
    ledger,
    workspace_id,
    session_id,
    attempt_ref,
    source_recovery,
    testimony,
    convention,
):
    """Warrant one local relation from distinct recovery, testimony, and convention."""
    recoveries = [
        event
        for event in ledger.list_events(workspace_id)
        if event.payload.get("attempt_ref") == attempt_ref
        and event.kind
        in {
            "operator.ingress.common_grammar.source_recovered",
            "operator.ingress.common_grammar.source_recovery_refused",
        }
    ]
    recorded = recoveries[0] if len(recoveries) == 1 else None
    representation = (
        ledger.get(source_recovery.payload.get("representation_occurrence_id", ""))
        if source_recovery is not None
        else None
    )
    expected_testimony = (
        SOURCE_MEANING_TESTIMONIES.get(testimony.source_ref)
        if testimony is not None
        else None
    )
    required_missing = (
        [
            name
            for name in convention.required_coordinates
            if testimony is None or not getattr(testimony, name, None)
        ]
        if convention is not None
        else []
    )
    checks = (
        (not recoveries, "no_exact_recorded_source_recovery_occurrence"),
        (len(recoveries) > 1, "multiple_source_recovery_occurrences"),
        (
            recorded is None
            or source_recovery is None
            or recorded.model_dump() != source_recovery.model_dump(),
            "supplied_source_recovery_is_not_recorded_occurrence",
        ),
        (
            recorded is not None and recorded.kind.endswith("source_recovery_refused"),
            "source_recovery_reports_refusal",
        ),
        (testimony is None, "missing_meaning_testimony"),
        (
            testimony is not None
            and (
                expected_testimony is None
                or testimony.testimony_id != expected_testimony.testimony_id
            ),
            "meaning_testimony_identity_mismatch",
        ),
        (
            testimony is not None and testimony.relation_assertion != "expresses",
            "meaning_testimony_relation_not_expresses",
        ),
        (
            testimony is not None
            and testimony.attributed_supplier
            != "Seed application developer declaration",
            "meaning_testimony_attribution_absent_or_mismatched",
        ),
        (
            testimony is not None and not testimony.producer_declaration_ref,
            "meaning_testimony_declaration_reference_absent",
        ),
        (
            testimony is not None and not testimony.provenance,
            "meaning_testimony_provenance_absent",
        ),
        (
            testimony is not None
            and testimony.declared_application_purpose != MEANING_CONVENTION_PURPOSE,
            "meaning_testimony_purpose_mismatch",
        ),
        (
            testimony is not None and testimony.scope != MEANING_CONVENTION_SCOPE,
            "meaning_testimony_scope_mismatch",
        ),
        (
            testimony is not None and bool(testimony.unknowns),
            "meaning_testimony_unknown",
        ),
        (
            testimony is not None and bool(testimony.conflicts),
            "meaning_testimony_conflicting",
        ),
        (convention is None, "missing_constitutive_convention"),
        (
            convention is not None
            and convention.convention_id
            != APPLICATION_SOURCE_MEANING_CONVENTION.convention_id,
            "constitutive_convention_identity_mismatch",
        ),
        (
            convention is not None
            and convention.attribution != "Seed application developer declaration",
            "constitutive_convention_attribution_absent_or_mismatched",
        ),
        (
            convention is not None and not convention.applicable_authority,
            "constitutive_convention_authority_absent",
        ),
        (
            convention is not None
            and convention.permitted_testimony_kind
            != "ApplicationSourceMeaningTestimony",
            "constitutive_convention_testimony_form_not_permitted",
        ),
        (
            convention is not None
            and convention.permitted_relation_form != "expresses",
            "constitutive_convention_does_not_permit_expresses",
        ),
        (
            convention is not None and convention.purpose != MEANING_CONVENTION_PURPOSE,
            "constitutive_convention_purpose_mismatch",
        ),
        (
            convention is not None and convention.scope != MEANING_CONVENTION_SCOPE,
            "constitutive_convention_scope_mismatch",
        ),
        (bool(required_missing), "constitutive_convention_required_coordinate_absent"),
        (
            convention is not None
            and convention.required_provenance
            and testimony is not None
            and not testimony.provenance,
            "constitutive_convention_required_provenance_absent",
        ),
        (
            convention is not None and bool(convention.unknowns),
            "constitutive_convention_unknown",
        ),
        (
            convention is not None and bool(convention.conflicts),
            "constitutive_convention_conflicting",
        ),
        (
            convention is not None
            and convention != APPLICATION_SOURCE_MEANING_CONVENTION,
            "forged_constitutive_convention",
        ),
        (
            recorded is not None
            and testimony is not None
            and recorded.payload.get("recovered_source_ref") != testimony.source_ref,
            "source_identity_mismatch",
        ),
        (
            recorded is not None
            and testimony is not None
            and recorded.payload.get("recovered_source_role") != testimony.source_role,
            "source_role_mismatch",
        ),
        (
            recorded is not None
            and testimony is not None
            and recorded.payload.get("recovered_source_proposition")
            != testimony.proposition,
            "proposition_mismatch",
        ),
        (
            testimony is not None
            and expected_testimony is not None
            and testimony != expected_testimony,
            "forged_meaning_testimony",
        ),
        (representation is None, "upstream_representation_occurrence_missing"),
        (
            representation is not None and bool(representation.payload.get("unknowns")),
            "upstream_representation_unknown",
        ),
        (
            representation is not None
            and bool(representation.payload.get("conflicts")),
            "upstream_representation_conflicting",
        ),
    )
    reason = next((reason for failed, reason in checks if failed), None)
    if reason:
        return _record(
            ledger,
            "operator.ingress.common_grammar.meaning_relation_refused",
            workspace_id,
            session_id,
            attempt_ref,
            _dimensions(
                identity=f"meaning-relation-refusal:{source_recovery.id if source_recovery else attempt_ref}",
                content=reason,
                standing="refused",
                source=source_recovery.id if source_recovery else "Unknown",
                responsibility="application-source-meaning-relation-warrant",
                authority="refusal only; does not establish negation or a competing relation",
                scope=f"attempt:{attempt_ref}",
                occurrence="exact bounded refusal durably recorded",
            ),
            refusal_reason=reason,
            unknowns=["whether the source expresses the proposition remains Unknown"],
            lineage=[source_recovery.id] if source_recovery else [],
        )
    relation_ref = f"meaning-relation:{testimony.source_ref}:expresses"
    return _record(
        ledger,
        "operator.ingress.common_grammar.meaning_relation_warranted",
        workspace_id,
        session_id,
        attempt_ref,
        _dimensions(
            identity=relation_ref,
            content=testimony.proposition,
            standing="warranted",
            source=f"{testimony.testimony_id};{convention.convention_id}",
            responsibility="application-source-meaning-relation-warrant",
            authority="developer-attributed application testimony under a bounded local constitutive convention",
            scope=f"attempt:{attempt_ref};{testimony.scope}",
            occurrence="separate responsible meaning-relation warrant recorded",
        ),
        relation_ref=relation_ref,
        relation_assertion=testimony.relation_assertion,
        source_ref=testimony.source_ref,
        source_role=testimony.source_role,
        proposition=testimony.proposition,
        meaning_testimony=asdict(testimony),
        meaning_testimony_ref=testimony.testimony_id,
        constitutive_convention=asdict(convention),
        constitutive_convention_ref=convention.convention_id,
        source_recovery_occurrence_id=source_recovery.id,
        representation_occurrence_id=source_recovery.payload[
            "representation_occurrence_id"
        ],
        binding_occurrence_id=source_recovery.payload["binding_occurrence_id"],
        selected_presented_alternative_ref=source_recovery.payload[
            "selected_presented_alternative_ref"
        ],
        purpose=testimony.declared_application_purpose,
        scope=testimony.scope,
        provenance=list(testimony.provenance),
        known_loss=list(
            dict.fromkeys(
                (*source_recovery.payload.get("known_loss", ()), *testimony.known_loss)
            )
        ),
        conflicts=[],
        unknowns=[],
        warrant_basis_kind="developer-attributed application testimony under a bounded local constitutive convention",
        lineage=[
            source_recovery.payload["representation_occurrence_id"],
            source_recovery.payload["binding_occurrence_id"],
            *source_recovery.payload["lineage"][-1:],
            source_recovery.id,
        ],
    )


def _examine_meaning_relation_for_bounded_operator_goal_establishment(
    *, ledger, workspace_id, session_id, attempt_ref, meaning_relation
):
    """Deliver one exact recorded warrant to its consumer-owned boundary."""
    recorded = [
        event
        for event in ledger.list_events(workspace_id)
        if event.payload.get("attempt_ref") == attempt_ref
        and event.kind == "operator.ingress.common_grammar.meaning_relation_warranted"
    ]
    exact = recorded[0] if len(recorded) == 1 else None
    if (
        exact is None
        or meaning_relation is None
        or exact.model_dump() != meaning_relation.model_dump()
    ):
        return _record(
            ledger,
            "operator.ingress.common_grammar.bounded_operator_goal_establishment_applicability_refused",
            workspace_id,
            session_id,
            attempt_ref,
            _dimensions(
                identity=f"bounded-operator-goal-establishment-applicability-refusal:{attempt_ref}",
                content="supplied_meaning_relation_is_not_exact_recorded_warrant",
                standing="refused",
                source=meaning_relation.id if meaning_relation else "unknown",
                responsibility="bounded-operator-goal-establishment applicability examination",
                authority="refusal only; no applicability, admission, or goal establishment",
                scope=f"attempt:{attempt_ref}",
                occurrence="bounded refusal durably recorded",
            ),
            refusal_reason="supplied_meaning_relation_is_not_exact_recorded_warrant",
            applicability="unknown",
            conflicts=[],
            unknowns=["applicability evidence is unavailable"],
            lineage=[meaning_relation.id] if meaning_relation else [],
        )

    examination = examine_meaning_relation_applicability(exact.model_dump(mode="json"))
    return _record(
        ledger,
        "operator.ingress.common_grammar.bounded_operator_goal_establishment_applicability_examined",
        workspace_id,
        session_id,
        attempt_ref,
        _dimensions(
            identity=f"bounded-operator-goal-establishment-applicability:{exact.id}",
            content=examination.reason,
            standing=examination.applicability,
            source=exact.id,
            responsibility="bounded-operator-goal-establishment applicability examination",
            authority="exact consumer and purpose only; no admission or goal establishment",
            scope=f"attempt:{attempt_ref};consumer:{examination.consumer_ref};purpose:{examination.purpose_ref}",
            occurrence="consumer-owned applicability examination durably recorded",
        ),
        meaning_relation_warrant_occurrence=examination.evidence[
            "meaning_relation_warrant_occurrence"
        ],
        meaning_relation_warrant_occurrence_id=exact.id,
        relation_ref=exact.payload["relation_ref"],
        consumer_ref=examination.consumer_ref,
        purpose_ref=examination.purpose_ref,
        condition_examined=examination.condition_examined,
        condition_evidence=examination.evidence["condition_evidence"],
        applicability=examination.applicability,
        applicability_reason=examination.reason,
        scope=exact.payload["scope"],
        provenance=list(exact.payload["provenance"]),
        known_loss=list(exact.payload.get("known_loss", ())),
        conflicts=list(examination.conflicts),
        unknowns=list(examination.unknowns),
        lineage=[*exact.payload.get("lineage", ()), exact.id],
    )


def common_grammar_representation_lineages(
    choice_set: PresentedClosedChoiceSet,
    producer_occurrence_ref: str,
) -> tuple[AlternativeSourceRepresentation, ...]:
    """Preserve the application-owned row-to-source assertions for this probe."""
    return tuple(
        AlternativeSourceRepresentation(
            option.presented_alternative_ref,
            ALTERNATIVE_SOURCES[option.presented_alternative_ref],
            SOURCE_PROPOSITIONS[ALTERNATIVE_SOURCES[option.presented_alternative_ref]][
                0
            ],
            "represent an application-owned bounded common-grammar source",
            choice_set.choice_set_ref,
            choice_set.exact_choice_set_fingerprint,
            choice_set.presentation_ref,
            option.presented_label,
            option.presented_detail,
            SOURCE_PROPOSITIONS[ALTERNATIVE_SOURCES[option.presented_alternative_ref]][
                1
            ],
            "presented_alternative_represents_application_owned_source",
            "participates_in_exact_presented_choice_set_for_declared_purpose",
            "application-owned common-grammar prerequisite source",
            producer_occurrence_ref,
            (
                "no meaning warrant",
                "no goal, stopping, acquisition, or action authority",
            ),
            (
                "seed_runtime.operator_ingress_common_grammar:alternative-source-lineage:v1",
            ),
            f"presentation:{choice_set.presentation_ref};choice-set:{choice_set.choice_set_ref}",
            RENDERING_KNOWN_LOSS,
        )
        for option in choice_set.options
    )


def _recover_represented_source(
    binding,
    choice_set,
    occurrence,
    *,
    ledger,
    workspace_id,
    attempt_ref,
    presentation_occurrence,
    selection_occurrence,
):
    """Recover from one earlier durable representation occurrence, never constants."""
    selected = binding.selected_presented_alternative_ref
    attempt_events = [
        event
        for event in ledger.list_events(workspace_id)
        if event.payload.get("attempt_ref") == attempt_ref
    ]
    binding_occurrences = [
        event
        for event in attempt_events
        if event.kind == "operator.ingress.common_grammar.binding_completed"
    ]
    recorded_binding = binding_occurrences[0] if len(binding_occurrences) == 1 else None
    response_occurrences = [
        event
        for event in attempt_events
        if event.kind == "operator.ingress.common_grammar.response_captured"
    ]
    recorded_response = (
        response_occurrences[0] if len(response_occurrences) == 1 else None
    )
    presentation_occurrences = [
        event
        for event in attempt_events
        if event.kind == "operator.ingress.common_grammar.presentation_occurred"
    ]
    recorded_presentation = (
        presentation_occurrences[0] if len(presentation_occurrences) == 1 else None
    )
    checks = (
        (occurrence is None, "no_recorded_representation_occurrence"),
        (
            occurrence is not None
            and occurrence.payload.get("attempt_ref") != attempt_ref,
            "wrong_attempt",
        ),
        (
            occurrence is not None
            and occurrence.payload.get("presentation_ref")
            != choice_set.presentation_ref,
            "wrong_presentation",
        ),
        (
            occurrence is not None
            and occurrence.payload.get("choice_set_ref") != choice_set.choice_set_ref,
            "wrong_choice_set",
        ),
        (
            occurrence is not None
            and occurrence.payload.get("choice_set_fingerprint")
            != choice_set.exact_choice_set_fingerprint,
            "wrong_set_fingerprint",
        ),
        (presentation_occurrence is None, "no_recorded_presentation_occurrence"),
        (
            recorded_presentation is None
            or presentation_occurrence is None
            or recorded_presentation.id != presentation_occurrence.id,
            "recorded_presentation_occurrence_mismatch",
        ),
        (
            presentation_occurrence is not None
            and presentation_occurrence.payload.get("attempt_ref") != attempt_ref,
            "wrong_presentation_attempt",
        ),
        (
            presentation_occurrence is not None
            and presentation_occurrence.payload.get("presentation_ref")
            != choice_set.presentation_ref,
            "wrong_presentation_occurrence",
        ),
        (
            presentation_occurrence is not None
            and presentation_occurrence.payload.get("choice_set_fingerprint")
            != choice_set.exact_choice_set_fingerprint,
            "presentation_fingerprint_mismatch",
        ),
        (not binding_occurrences, "no_recorded_binding_occurrence"),
        (len(binding_occurrences) > 1, "multiple_recorded_binding_occurrences"),
        (
            recorded_binding is not None
            and recorded_binding.payload.get("binding_id") != binding.binding_id,
            "binding_id_mismatch",
        ),
        (
            recorded_binding is not None
            and recorded_binding.payload.get("choice_set_ref")
            != binding.choice_set_ref,
            "binding_choice_set_mismatch",
        ),
        (
            recorded_binding is not None
            and recorded_binding.payload.get("choice_set_fingerprint")
            != binding.exact_choice_set_fingerprint,
            "binding_set_fingerprint_mismatch",
        ),
        (
            recorded_binding is not None
            and recorded_binding.payload.get("presented_options")
            != _recordable_presented_options(choice_set),
            "binding_presented_options_mismatch",
        ),
        (
            recorded_binding is not None
            and recorded_binding.payload.get("selected_presented_alternative_ref")
            != selected,
            "binding_selected_alternative_mismatch",
        ),
        (
            recorded_binding is not None
            and recorded_binding.payload.get("binding_testimony")
            != _recordable_binding_testimony(binding),
            "recorded_binding_payload_mismatch",
        ),
        (
            recorded_response is None
            or presentation_occurrence is None
            or recorded_binding is None
            or recorded_response.id not in recorded_binding.payload.get("lineage", ())
            or presentation_occurrence.id
            not in recorded_binding.payload.get("lineage", ())
            or presentation_occurrence.id
            not in recorded_response.payload.get("lineage", ()),
            "binding_lineage_mismatch",
        ),
        (
            selection_occurrence is None
            or recorded_binding is None
            or selection_occurrence.payload.get("binding_id") != binding.binding_id
            or selection_occurrence.payload.get("selected_presented_alternative_ref")
            != selected
            or recorded_binding.id
            not in selection_occurrence.payload.get("lineage", ()),
            "selected_alternative_occurrence_mismatch",
        ),
        (
            binding.binding_state != "bound" or not selected,
            "no_selected_presented_alternative",
        ),
        (bool(binding.unknown_selection_evidence), "selection_evidence_unknown"),
        (
            bool(binding.conflicting_selection_evidence),
            "selection_evidence_conflicting",
        ),
    )
    for failed, reason in checks:
        if failed:
            return None, reason
    lineage = occurrence.payload.get("representations", ())
    if occurrence.payload.get(
        "representation_evidence_fingerprint"
    ) != _representation_fingerprint(lineage):
        return None, "forged_relation_payload"
    matches = [
        item for item in lineage if item.get("presented_alternative_ref") == selected
    ]
    if len(matches) != 1:
        return None, "selected_alternative_not_preserved"
    item = matches[0]
    required = {
        "represented_source_ref",
        "represented_source_role",
        "proposition_assertion",
        "representation_relation",
        "exact_set_participation",
        "rendered_label",
        "rendered_detail",
        "source_attribution",
        "producer_occurrence_ref",
        "provenance",
        "scope",
        "authority_limits",
        "known_loss",
        "unknowns",
        "conflicts",
    }
    if not required.issubset(item):
        return None, "representation_evidence_missing"
    if item["producer_occurrence_ref"] != occurrence.payload["dimensions"]["identity"]:
        return None, "forged_relation_payload"
    if (
        item["representation_relation"]
        != "presented_alternative_represents_application_owned_source"
    ):
        return None, "representation_relation_missing_or_conflicting"
    if (
        item["exact_set_participation"]
        != "participates_in_exact_presented_choice_set_for_declared_purpose"
    ):
        return None, "exact_set_participation_missing_or_conflicting"
    if item["unknowns"]:
        return None, "representation_evidence_unknown"
    if item["conflicts"]:
        return None, "representation_evidence_conflicting"
    option = next(
        (o for o in choice_set.options if o.presented_alternative_ref == selected), None
    )
    if option is None:
        return None, "wrong_alternative_identity"
    if (
        item["rendered_label"] != option.presented_label
        or item["rendered_detail"] != option.presented_detail
    ):
        return None, "rendered_content_mismatch"
    return (
        RecoveredRepresentedSource(
            selected,
            item["represented_source_ref"],
            item["represented_source_role"],
            item["proposition_assertion"],
            tuple(item["provenance"]),
            item["scope"],
            tuple(item["known_loss"]),
            occurrence.id,
            recorded_binding.id,
        ),
        None,
    )


def common_grammar_choice_set(presentation_ref: str) -> PresentedClosedChoiceSet:
    """Return the application-owned probe; callers can supply identity, not semantics."""
    return PresentedClosedChoiceSet(
        choice_set_ref=CHOICE_SET_REF,
        prompt=PROMPT,
        options=OPTIONS,
        presentation_ref=presentation_ref,
        provenance=("seed_runtime.operator_ingress_common_grammar:v1",),
    )


def render_probe(choice_set: PresentedClosedChoiceSet) -> str:
    return "\n".join(
        (
            choice_set.prompt,
            *(f"{o.token}. {o.presented_label}" for o in choice_set.options),
        )
    )


def _dimensions(
    *, identity, content, standing, source, responsibility, authority, scope, occurrence
):
    return {
        "identity": identity,
        "content": content,
        "standing": standing,
        "source_provenance": source,
        "responsibility": responsibility,
        "authority_warrant": authority,
        "scope_locality": scope,
        "occurrence_preservation": occurrence,
    }


def _record(ledger, kind, workspace, session, attempt, dimensions, **extra):
    return ledger.append(
        kind,
        workspace,
        {
            "attempt_ref": attempt,
            "dimensions": dimensions,
            "mutates_cluster": False,
            **extra,
        },
        session_id=session,
    )


def project_operator_ingress_common_grammar_events(state, event) -> None:
    """Dispatch one operator-ingress common-grammar event into the dedicated current view."""
    if not event.kind.startswith("operator.ingress.common_grammar."):
        return
    attempt = event.payload["attempt_ref"]
    view = state.operator_ingress_common_grammar_attempts.setdefault(
        attempt,
        {
            "event_ids": [],
            "dimensional_standing": {},
            "current_standing": {
                subject: None
                for subject in (
                    "raw_initial_material",
                    "raw_response_material",
                    "preserved_ingress",
                    "produced_probe",
                    "alternative_representations",
                    "presentation",
                    "response",
                    "binding_finding",
                    "alternative_selection",
                    "source_recovery",
                    "source_role_testimony",
                    "potential_goal_standing",
                    "presentation_eligibility",
                    "meaning_relation",
                    "bounded_operator_goal_establishment_applicability",
                    "interaction_closure",
                )
            },
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "representation_examinations": {},
        },
    )
    view["event_ids"].append(event.id)
    # Occurrences are evidence in their own right.  Keep each complete
    # eight-dimensional description rather than replacing it with the tail event.
    view["dimensional_standing"][event.id] = {
        "event_kind": event.kind,
        "subject_ref": event.payload["dimensions"]["identity"],
        "dimensions": event.payload["dimensions"],
        "lineage": list(event.payload.get("lineage", ())),
    }
    if event.kind == "operator.ingress.common_grammar.representation_examined":
        view["representation_examinations"][event.payload["material_role"]] = {
            "examination_event_id": event.id,
            "capture_event_id": event.payload["capture_event_id"],
            "encoding_testimony": event.payload["encoding_testimony"],
            "decoder_mechanism": event.payload["decoder_mechanism"],
            "decoder_mechanism_selection": event.payload["decoder_mechanism_selection"],
            "decoder_outcome": event.payload["decoder_outcome"],
            "decoder_succeeded": event.payload["decoder_succeeded"],
            "decoder_failure": event.payload["decoder_failure"],
        }
        view["last_event_kind"] = event.kind
        return
    subject_by_kind = {
        "operator.ingress.common_grammar.ingress_occurred": "preserved_ingress",
        "operator.ingress.common_grammar.initial_eof_occurred": "preserved_ingress",
        "operator.ingress.common_grammar.probe_produced": "produced_probe",
        "operator.ingress.common_grammar.alternatives_represented": "alternative_representations",
        "operator.ingress.common_grammar.presentation_occurred": "presentation",
        "operator.ingress.common_grammar.response_captured": "response",
        "operator.ingress.common_grammar.response_eof_occurred": "response",
        "operator.ingress.common_grammar.binding_completed": "binding_finding",
        "operator.ingress.common_grammar.unsupported_finding": "binding_finding",
        "operator.ingress.common_grammar.alternative_selected": "alternative_selection",
        "operator.ingress.common_grammar.source_recovered": "source_recovery",
        "operator.ingress.common_grammar.source_recovery_refused": "source_recovery",
        "operator.ingress.common_grammar.potential_goal_standing_examined": "potential_goal_standing",
        "operator.ingress.common_grammar.presentation_eligibility_examined": "presentation_eligibility",
        "operator.ingress.common_grammar.meaning_relation_warranted": "meaning_relation",
        "operator.ingress.common_grammar.meaning_relation_refused": "meaning_relation",
        "operator.ingress.common_grammar.bounded_operator_goal_establishment_applicability_examined": "bounded_operator_goal_establishment_applicability",
        "operator.ingress.common_grammar.bounded_operator_goal_establishment_applicability_refused": "bounded_operator_goal_establishment_applicability",
        "operator.ingress.common_grammar.stopping_occurred": "interaction_closure",
    }
    subject = (
        "raw_initial_material"
        if event.kind == "operator.ingress.common_grammar.raw_material_captured"
        and event.payload["material_role"] == "initial_ingress"
        else (
            "raw_response_material"
            if event.kind == "operator.ingress.common_grammar.raw_material_captured"
            else subject_by_kind[event.kind]
        )
    )
    dimensions = dict(event.payload["dimensions"])
    if subject == "preserved_ingress":
        dimensions["standing"] = "preserved"
    view["current_standing"][subject] = {
        "subject_ref": dimensions["identity"],
        "dimensions": dimensions,
        "evidence_event_id": event.id,
    }
    if subject == "response" and view["current_standing"]["presentation"]:
        view["current_standing"]["presentation"]["dimensions"]["standing"] = "consumed"
    if subject == "binding_finding" and view["current_standing"]["response"]:
        view["current_standing"]["response"]["dimensions"]["standing"] = "consumed"
    view["last_event_kind"] = event.kind
    for key in ("known_loss", "unknowns", "conflicts"):
        view[key] = sorted(set((*view[key], *event.payload.get(key, ()))))
    for key in (
        "choice_set_ref",
        "presentation_ref",
        "capture_ref",
        "binding_id",
        "selected_presented_alternative_ref",
        "recovered_source_ref",
        "recovered_source_role",
        "recovered_source_proposition",
        "source_role_testimony_ref",
        "standing_subject",
        "standing_relation",
        "standing_result",
        "upstream_standing_occurrence_id",
        "presentation_purpose_id",
        "eligibility_relation",
        "eligibility_result",
        "relation_ref",
        "relation_assertion",
        "meaning_testimony_ref",
        "constitutive_convention_ref",
        "meaning_relation_warrant_occurrence_id",
        "consumer_ref",
        "purpose_ref",
        "condition_examined",
        "condition_evidence",
        "applicability",
        "applicability_reason",
        "closed",
        "response_kind",
    ):
        if key in event.payload:
            view[key] = event.payload[key]
    if event.kind == "operator.ingress.common_grammar.potential_goal_standing_examined":
        view["current_standing"]["source_role_testimony"] = {
            "subject_ref": event.payload.get("source_role_testimony_ref"),
            "testimony": event.payload.get("source_role_testimony"),
            "evidence_event_id": event.id,
        }


def _capture_representation(
    *,
    ledger,
    workspace,
    session,
    attempt,
    material_role,
    captured_material=None,
    input_stream=None,
    lineage=(),
):
    if (captured_material is None) == (input_stream is None):
        raise ValueError("supply exactly one of captured_material or input_stream")
    capture = (
        captured_material
        if captured_material is not None
        else capture_stdin_material(input_stream)
    )
    capture_ref = new_id("operator_material")
    captured = _record(
        ledger,
        "operator.ingress.common_grammar.raw_material_captured",
        workspace,
        session,
        attempt,
        _dimensions(
            identity=capture_ref,
            content=capture.exact_bytes.hex(),
            standing="captured",
            source=capture.capture_boundary,
            responsibility="competent-raw-material-capture",
            authority="occurrence evidence only",
            scope=f"workspace:{workspace};session:{session};role:{material_role}",
            occurrence="exact boundary bytes durably preserved as hexadecimal",
        ),
        material_role=material_role,
        exact_bytes_hex=capture.exact_bytes.hex(),
        byte_count=len(capture.exact_bytes),
        eof=capture.eof,
        delimiter_hex=capture.delimiter_hex,
        encoding_testimony=capture.encoding_testimony,
        capture_boundary=capture.capture_boundary,
        byte_material_origin=capture.byte_material_origin,
        known_loss=list(capture.known_loss),
        lineage=list(lineage),
    )
    examination = examine_text_representation(capture)
    if examination is None:
        return capture, None, captured, None
    examination_event = _record(
        ledger,
        "operator.ingress.common_grammar.representation_examined",
        workspace,
        session,
        attempt,
        _dimensions(
            identity=f"representation-examination:{captured.id}",
            content="strict decoder examination",
            # Preserve the particular decoder occurrence here as well as in the
            # examination payload.  A shared ``not-decodable`` standing would
            # collapse an unavailable mechanism and bytes rejected by an
            # available mechanism back into the Boolean boundary this record is
            # intended to repair.
            standing=examination.outcome,
            source=captured.id,
            responsibility="bounded-representation-evidence-production",
            authority="decoder outcome evidence only",
            scope=f"captured-occurrence:{capture_ref}",
            occurrence="decoder examination durably recorded",
        ),
        material_role=material_role,
        capture_event_id=captured.id,
        encoding_testimony=capture.encoding_testimony,
        decoder_mechanism=examination.mechanism,
        decoder_mechanism_selection=examination.mechanism_selection,
        decoder_outcome=examination.outcome,
        decoder_succeeded=examination.succeeded,
        decoder_failure=examination.failure,
        known_loss=list(capture.known_loss),
        unknowns=["true source-relative encoding Unknown"],
        lineage=[captured.id],
    )
    return capture, examination, captured, examination_event


def run_operator_ingress_common_grammar_probe_attempt(
    *,
    ledger: EventLedger,
    workspace_id: str,
    session_id: str,
    captured_ingress: CapturedOperatorMaterial,
    response_input_stream: TextIO | BinaryIO,
    output_stream: TextIO,
) -> dict[str, object]:
    """Run exactly one ingress/common-grammar-probe/response attempt and return."""
    attempt = new_id("operator_ingress_common_grammar_attempt")
    (
        captured_ingress,
        ingress_examination,
        ingress_capture,
        ingress_examination_event,
    ) = _capture_representation(
        ledger=ledger,
        workspace=workspace_id,
        session=session_id,
        attempt=attempt,
        captured_material=captured_ingress,
        material_role="initial_ingress",
    )
    raw_ingress = (
        ingress_examination.represented_text or "" if ingress_examination else ""
    )
    ingress_kind = (
        "eof"
        if captured_ingress.eof
        else "empty" if raw_ingress in {"\n", "\r\n"} else "text"
    )
    ingress_content = (
        None
        if ingress_kind == "eof"
        else raw_ingress.removesuffix("\n").removesuffix("\r")
    )
    if ingress_examination is not None and not ingress_examination.succeeded:
        _record(
            ledger,
            "operator.ingress.common_grammar.stopping_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=f"stop:{ingress_examination_event.id}",
                content="representation insufficiency",
                standing="closed",
                source=ingress_examination_event.id,
                responsibility="competent-local-stopping",
                authority="closes only this interaction",
                scope=f"attempt:{attempt}",
                occurrence="separate stopping act recorded",
            ),
            closed=True,
            response_kind="representation_insufficient",
            lineage=[ingress_examination_event.id],
        )
        state = StateProjector(ledger).project(workspace_id)
        output_stream.write(
            "Representation insufficient: captured material did not decode under the selected decoder mechanism.\n"
        )
        output_stream.flush()
        return state.operator_ingress_common_grammar_attempts[attempt]
    ingress = _record(
        ledger,
        (
            "operator.ingress.common_grammar.initial_eof_occurred"
            if ingress_kind == "eof"
            else "operator.ingress.common_grammar.ingress_occurred"
        ),
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=attempt,
            content=ingress_content,
            standing="occurred",
            source=(
                ingress_capture.id
                if ingress_examination_event is None
                else ingress_examination_event.id
            ),
            responsibility="operator-ingress",
            authority="occurrence-only; meaning Unknown",
            scope=f"workspace:{workspace_id};session:{session_id}",
            occurrence=(
                "EOF occurrence preserves raw-capture lineage"
                if ingress_kind == "eof"
                else "strictly decoded text preserves capture/examination lineage"
            ),
        ),
        raw_input=raw_ingress,
        ingress_kind=ingress_kind,
        decoded_text=(
            ingress_examination.represented_text if ingress_examination else None
        ),
        raw_material_event_id=ingress_capture.id,
        **(
            {"representation_examination_event_id": ingress_examination_event.id}
            if ingress_examination_event is not None
            else {}
        ),
        known_loss=list(captured_ingress.known_loss),
        lineage=[
            ingress_capture.id,
            *([ingress_examination_event.id] if ingress_examination_event else []),
        ],
    )
    state = StateProjector(ledger).project(workspace_id)
    if ingress_kind == "eof":
        _record(
            ledger,
            "operator.ingress.common_grammar.stopping_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=f"stop:{ingress.id}",
                content="initial EOF",
                standing="closed",
                source=ingress.id,
                responsibility="competent-local-stopping",
                authority="closes only this interaction",
                scope=f"attempt:{attempt}",
                occurrence="separate stopping act recorded",
            ),
            closed=True,
            response_kind="initial_eof",
            lineage=[ingress.id],
        )
        state = StateProjector(ledger).project(workspace_id)
        output_stream.write(
            "Operator-ingress common-grammar interaction stopped locally.\n"
        )
        output_stream.flush()
        return state.operator_ingress_common_grammar_attempts[attempt]

    return state.operator_ingress_common_grammar_attempts[attempt]


def validate_capture_for_probe(
    *,
    ledger: EventLedger,
    workspace_id: str,
    attempt_ref: str,
    choice_set: PresentedClosedChoiceSet,
    capture: OperatorSelectionTokenCapture,
    unsupported_selection_evidence: tuple[str, ...] = (),
):
    """Validate production identity/currentness and consume one recorded capture."""
    events = [
        event
        for event in ledger.list_events(workspace_id)
        if event.payload.get("attempt_ref") == attempt_ref
    ]
    presentations = [
        event
        for event in events
        if event.kind == "operator.ingress.common_grammar.presentation_occurred"
    ]
    captures = [
        event
        for event in events
        if event.kind == "operator.ingress.common_grammar.response_captured"
    ]
    if not presentations or not captures:
        raise ClosedChoiceSelectionBindingError(
            "communication probe lacks recorded presentation or capture evidence"
        )
    presentation = presentations[-1]
    recorded_capture = captures[-1]
    fingerprint = choice_set.exact_choice_set_fingerprint
    if (
        choice_set.choice_set_ref != CHOICE_SET_REF
        or choice_set.presentation_ref != presentation.payload.get("presentation_ref")
        or capture.choice_set_ref != presentation.payload.get("choice_set_ref")
        or fingerprint != presentation.payload.get("choice_set_fingerprint")
    ):
        raise ClosedChoiceSelectionBindingError(
            "communication probe presentation/set identity or fingerprint mismatch"
        )
    if (
        capture.capture_ref != recorded_capture.payload.get("capture_ref")
        or capture.choice_set_ref != recorded_capture.payload.get("choice_set_ref")
        or capture.captured_token
        != (
            ""
            if recorded_capture.payload.get("response_kind") == "eof"
            else recorded_capture.payload.get("raw_input", "")
            .removesuffix("\n")
            .removesuffix("\r")
        )
    ):
        raise ClosedChoiceSelectionBindingError(
            "communication probe capture is not the current recorded occurrence"
        )
    if any(
        event.kind
        in {
            "operator.ingress.common_grammar.binding_completed",
            "operator.ingress.common_grammar.unsupported_finding",
        }
        and event.payload.get("capture_ref") == capture.capture_ref
        for event in events
    ):
        raise ClosedChoiceSelectionBindingError(
            "communication probe response capture was already consumed"
        )
    return bind_closed_choice_selection(
        choice_set,
        capture,
        unsupported_selection_evidence=unsupported_selection_evidence,
    )
