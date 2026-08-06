"""Recorded Compare and Identification over one bounded Presentation exchange."""

from __future__ import annotations

from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id

RESPONSE_COMPARISON_KIND = "operator.exchange.comparison_occurred"
IDENTIFICATION_KIND = "operator.exchange.identification_occurred"

# Unknowns the Book positively establishes at this exact position: the
# external fact is only that the operator produced material after emission.
_MATCH_UNKNOWNS = (
    "operator intent Unknown",
    "operator selection occurrence Unknown",
)
_NO_MATCH_UNKNOWNS = (
    "response meaning Unknown",
    "operator intent Unknown",
    "operator selection occurrence Unknown",
    "requested treatment Unknown",
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


def _require(condition: bool, failure: str) -> None:
    if not condition:
        raise ValueError(f"response comparison preconditions unmet: {failure}")


def run_operator_response_comparison_and_identification(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    presentation: dict[str, Any],
    response_ingress_event_id: str,
) -> dict[str, Any]:
    """Compare captured operator material with C's exact response coordinates,
    then identify the corresponding presented alternative, as two distinct
    recorded results of one responsible occurrence.

    The compared representation is the ingress occurrence's recorded content
    dimension -- the strictly decoded text with the single trailing line
    delimiter removed by the ingress boundary -- matched exactly against C's
    recorded coordinates.  No further trimming, normalization, case folding,
    or interpretation occurs here.

    A match establishes correspondence within C only.  It establishes no
    operator intent, understanding, selection, authorization, source
    recovery, meaning, or treatment.  No coordinate match establishes none
    of: that the material was not a response, candidate nonparticipation,
    or negative operator intent.
    """
    _require(presentation is not None, "no presentation supplied")
    presentation_ref = presentation["presentation_id"]
    formed_event_id = presentation["formed_event_id"]
    emitted_event_id = presentation["emitted_event_id"]
    _require(formed_event_id is not None, "presentation has no formation evidence")
    _require(emitted_event_id is not None, "presentation has no emission evidence")
    scope = f"workspace:{workspace_id};session:{session_id}"

    # The recorded formation payload is the sole source of C's alternatives,
    # coordinate bindings, and scope.  The supplied projection identifies
    # which C to retrieve; it must not redefine C, so a projection that
    # disagrees with the recorded testimony is structurally refused.
    formed_event = ledger.get(formed_event_id)
    _require(formed_event is not None, "formation event not recorded in this ledger")
    _require(
        formed_event.kind == "operator.presentation.formed",
        "formation evidence is not a presentation formation event",
    )
    _require(
        formed_event.workspace_id == workspace_id
        and formed_event.session_id == session_id,
        "formation event belongs to another workspace or session",
    )
    _require(
        formed_event.payload["presentation_ref"] == presentation_ref,
        "formation event does not record this exact presentation",
    )
    _require(
        formed_event.payload["dimensions"]["scope_locality"] == scope,
        "presentation scope does not match this workspace and session",
    )
    alternatives = formed_event.payload["alternatives"]
    coordinate_bindings = formed_event.payload["coordinate_bindings"]
    _require(bool(alternatives), "recorded presentation has no alternatives")
    _require(bool(coordinate_bindings), "recorded presentation has no bindings")
    for key in ("alternatives", "coordinate_bindings"):
        supplied = presentation.get(key)
        _require(
            supplied is None or supplied == formed_event.payload[key],
            f"supplied projection disagrees with recorded {key}",
        )

    emitted_event = ledger.get(emitted_event_id)
    _require(emitted_event is not None, "emission event not recorded in this ledger")
    _require(
        emitted_event.kind == "operator.presentation.emitted",
        "emission evidence is not a presentation emission event",
    )
    _require(
        emitted_event.workspace_id == workspace_id
        and emitted_event.session_id == session_id,
        "emission event belongs to another workspace or session",
    )
    _require(
        emitted_event.payload["presentation_ref"] == presentation_ref,
        "emission event does not record this exact presentation",
    )
    _require(
        emitted_event.payload["formed_event_id"] == formed_event_id,
        "emission event does not record this exact formation occurrence",
    )

    ingress_event = ledger.get(response_ingress_event_id)
    _require(ingress_event is not None, "response ingress event not recorded")
    _require(
        ingress_event.kind == "operator.ingress.ingress_occurred",
        "response evidence is not an ingress occurrence",
    )
    _require(
        ingress_event.workspace_id == workspace_id
        and ingress_event.session_id == session_id,
        "response ingress belongs to another workspace or session",
    )
    # The exact recorded C -> R reference chain; append order alone is not
    # relied on, and every named reference must agree.
    _require(
        ingress_event.payload.get("produced_after_presentation_ref")
        == presentation_ref,
        "ingress does not record production after this exact presentation",
    )
    _require(
        ingress_event.payload.get("produced_after_presentation_formed_event_id")
        == formed_event_id,
        "ingress does not record this exact formation occurrence",
    )
    _require(
        ingress_event.payload.get("produced_after_presentation_emitted_event_id")
        == emitted_event_id,
        "ingress does not record this exact emission occurrence",
    )

    response_attempt_ref = ingress_event.payload["attempt_ref"]
    response_capture_event_id = ingress_event.payload["raw_material_event_id"]
    capture_event = ledger.get(response_capture_event_id)
    _require(capture_event is not None, "response capture event not recorded")
    _require(
        capture_event.kind == "operator.ingress.raw_material_captured",
        "capture evidence is not a raw-material capture event",
    )
    _require(
        capture_event.workspace_id == workspace_id
        and capture_event.session_id == session_id,
        "capture event belongs to another workspace or session",
    )
    _require(
        capture_event.payload["attempt_ref"] == response_attempt_ref,
        "capture and ingress belong to different attempts",
    )

    compared_representation = ingress_event.payload["dimensions"]["content"]
    # C's exact response coordinates are the recorded alternatives' own
    # coordinates; the binding relation is consumed separately below, so a
    # recorded coordinate whose binding is absent stays distinguishable.
    coordinate_set = sorted(
        alternative["response_coordinate"] for alternative in alternatives
    )
    matched_coordinate = (
        compared_representation
        if compared_representation in set(coordinate_set)
        else None
    )
    comparison_outcome = (
        f"match:{matched_coordinate}"
        if matched_coordinate is not None
        else "no-coordinate-match"
    )
    comparison_ref = new_id("operator_response_comparison")
    exchange_lineage = [
        formed_event_id,
        emitted_event_id,
        response_capture_event_id,
        response_ingress_event_id,
    ]
    comparison_event = ledger.append(
        RESPONSE_COMPARISON_KIND,
        workspace_id,
        {
            "attempt_ref": response_attempt_ref,
            "comparison_ref": comparison_ref,
            "presentation_ref": presentation_ref,
            "presentation_formed_event_id": formed_event_id,
            "presentation_emitted_event_id": emitted_event_id,
            "response_attempt_ref": response_attempt_ref,
            "response_capture_event_id": response_capture_event_id,
            "response_ingress_event_id": response_ingress_event_id,
            "compared_representation": compared_representation,
            "coordinate_set": coordinate_set,
            "matched_coordinate": matched_coordinate,
            "outcome": comparison_outcome,
            "purpose": (
                "compare captured operator material with the emitted "
                "presentation's exact response coordinates"
            ),
            "dimensions": _dimensions(
                identity=comparison_ref,
                content=comparison_outcome,
                standing=comparison_outcome,
                source=response_ingress_event_id,
                responsibility="bounded-response-comparison",
                authority=(
                    "bounded by this exchange: captured material against this "
                    "presentation's exact response coordinates; result bounded "
                    "to match or no coordinate match; establishes no intent, "
                    "understanding, selection, authorization, or treatment"
                ),
                scope=f"{scope};exchange:{presentation_ref}->{response_attempt_ref}",
                occurrence="comparison occurrence durably recorded",
            ),
            "known_loss": [],
            "unknowns": list(
                _MATCH_UNKNOWNS if matched_coordinate else _NO_MATCH_UNKNOWNS
            ),
            "conflicts": [],
            "lineage": exchange_lineage,
            "mutates_cluster": False,
        },
        session_id=session_id,
    )

    # Distinct Identification: consumes the comparison finding, exact C, and
    # the recorded coordinate-to-alternative binding.  The formation event is
    # the Evidence for the binding and the preserved A -> G representation
    # relations; each alternative's empty upstream evidence_event_ids means
    # only that no separately recorded developer-source event exists.
    identified_alternative = None
    if matched_coordinate is None:
        basis = "no-coordinate-match"
    else:
        bound_alternative_id = coordinate_bindings.get(matched_coordinate)
        alternatives_by_id = {
            alternative["alternative_id"]: alternative
            for alternative in alternatives
        }
        if bound_alternative_id is None:
            basis = "binding-absent"
        elif bound_alternative_id not in alternatives_by_id:
            basis = "binding-inapplicable"
        else:
            basis = "identified"
            alternative = alternatives_by_id[bound_alternative_id]
            identified_alternative = {
                "alternative_id": alternative["alternative_id"],
                "role": alternative["role"],
                "response_coordinate": alternative["response_coordinate"],
                "rendered_label": alternative["rendered_label"],
            }
    identification_outcome = (
        "alternative-identified"
        if identified_alternative is not None
        else "no-presented-alternative-identified"
    )
    identification_ref = new_id("operator_alternative_identification")
    identification_event = ledger.append(
        IDENTIFICATION_KIND,
        workspace_id,
        {
            "attempt_ref": response_attempt_ref,
            "identification_ref": identification_ref,
            "comparison_ref": comparison_ref,
            "comparison_event_id": comparison_event.id,
            "presentation_ref": presentation_ref,
            "presentation_formed_event_id": formed_event_id,
            "response_attempt_ref": response_attempt_ref,
            "identified_alternative": identified_alternative,
            "basis": basis,
            "outcome": identification_outcome,
            "purpose": (
                "identify which presented alternative corresponds to the "
                "captured material within the exact presentation"
            ),
            "dimensions": _dimensions(
                identity=identification_ref,
                content=identification_outcome,
                standing=identification_outcome,
                source=comparison_event.id,
                responsibility="bounded-alternative-identification",
                authority=(
                    "identifies a presented alternative within this exact "
                    "presentation only; establishes no source recovery, "
                    "meaning, intent, selection, authorization, goal, or "
                    "treatment occurrence"
                ),
                scope=f"{scope};exchange:{presentation_ref}->{response_attempt_ref}",
                occurrence="identification occurrence durably recorded",
            ),
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "lineage": [comparison_event.id, formed_event_id],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )
    return {
        "comparison": {
            "comparison_ref": comparison_ref,
            "event_id": comparison_event.id,
            "outcome": comparison_outcome,
            "matched_coordinate": matched_coordinate,
            "compared_representation": compared_representation,
            "coordinate_set": coordinate_set,
        },
        "identification": {
            "identification_ref": identification_ref,
            "event_id": identification_event.id,
            "outcome": identification_outcome,
            "basis": basis,
            "identified_alternative": identified_alternative,
        },
    }
