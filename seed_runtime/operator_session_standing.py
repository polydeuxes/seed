"""Deterministic session-local Standing read over preserved ingress events."""

from __future__ import annotations


from bisect import bisect_left
from typing import Any, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.event import Event

_SUBJECT_BY_KIND = {
    "operator.ingress.raw_material_captured": "raw_initial_material",
    "operator.ingress.ingress_occurred": "preserved_ingress",
    "operator.ingress.stopping_occurred": "interaction_closure",
}
_REPRESENTATION_RECORDED_KIND = "operator.representation.recorded"
_REPRESENTATION_ACT_EVIDENCE_KIND = "operator.representation.act_evidenced"
_REPRESENTATION_CARRIAGE_EVIDENCE_KIND = (
    "operator.representation.carriage_evidenced"
)
_REPRESENTATION_EMISSION_ATTEMPTED_KIND = "operator.representation.emission_attempted"
_REPRESENTATION_EMITTED_KIND = "operator.representation.emitted"
_REPRESENTATION_EMISSION_OUTCOME_KIND = "operator.representation.emission_outcome_recorded"
_REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND = (
    "operator.representation.emission_act_evidenced"
)
_REPRESENTATION_EMISSION_CARRIAGE_EVIDENCE_KIND = (
    "operator.representation.emission_carriage_evidenced"
)
_COMPARISON_KIND = "operator.exchange.comparison_occurred"
_IDENTIFICATION_KIND = "operator.exchange.identification_occurred"
_SOURCE_VALIDATED_KIND = "operator.representation.source_validated"
_REPRESENTED_RELATION_KIND = "operator.representation.represented_relation_established"
_SUPPORTED_KINDS = {
    *_SUBJECT_BY_KIND,
    "operator.ingress.decoder_outcome_recorded",
    _REPRESENTATION_RECORDED_KIND,
    _REPRESENTATION_ACT_EVIDENCE_KIND,
    _REPRESENTATION_CARRIAGE_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_ATTEMPTED_KIND,
    _REPRESENTATION_EMITTED_KIND,
    _REPRESENTATION_EMISSION_OUTCOME_KIND,
    _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_CARRIAGE_EVIDENCE_KIND,
    _COMPARISON_KIND,
    _IDENTIFICATION_KIND,
    _SOURCE_VALIDATED_KIND,
    _REPRESENTED_RELATION_KIND,
}


def _record_distinct(collected: list[str], value: str) -> None:
    """Keep one sorted, distinct sequence in place.

    The returned coordinate is a sorted list of distinct strings, as it has
    always been.  Adding a value already present does nothing, so an advance
    that yields no new value costs nothing.
    """

    index = bisect_left(collected, value)
    if index == len(collected) or collected[index] != value:
        collected.insert(index, value)


def read_operator_session_standing(
    ledger: EventLedger, *, workspace_id: str, session_id: str
) -> dict[str, Any]:
    """Project bounded session-local Standing by replaying the whole session.

    Equivalent to advancing from no prior Standing over every recorded event.
    `#2376` established that advancing from a prior Standing over only the
    occurrences after its boundary yields the same result, so a caller that
    already holds its Standing and knows what it just recorded should use
    :func:`advance_operator_session_standing` instead of replaying.
    """

    return advance_operator_session_standing(
        ledger.list_session(workspace_id, session_id),
        workspace_id=workspace_id,
        session_id=session_id,
    )


def advance_operator_session_standing(
    events: Iterable[Event],
    *,
    workspace_id: str,
    session_id: str,
    prior: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Advance bounded session-local Standing over an exact sequence of events.

    With no `prior`, this reads from nothing and `events` must be the whole
    session. With a `prior`, `events` must be exactly the applicable
    occurrences recorded after `prior["as_of_event_id"]`, in append order; the
    prefix it already input is not revisited.

    The caller supplies those occurrences. Nothing here searches a ledger for
    them, because a responsible act that just recorded an occurrence already
    holds it.

    Every accumulator the live event kinds read is seeded from `prior`, and the
    per-event branches and refusals below are the same ones replay uses. Those
    refusals consult accumulated Standing rather than the ledger, which is why
    seeding preserves them (`#2376`).

    **The advance has as input `prior`.** Its accumulators are taken over rather
    than copied, and the returned Standing shares them. A caller that needs the
    earlier Standing to stay as it was must project it again; there is no
    snapshot here.

    That is not defensive weakness, it is the point. Standing grows with the
    session, so copying it per advance would cost the session length every
    time and reinstate the quadratic this replaced. The console holds one
    Standing, hands it forward, and keeps no earlier one.

    Accepts as input only ``operator.ingress.*`` and ``operator.representation.*``
    events stamped with this exact workspace and session, in append order.  The result is fully recomputable
    from the ledger and is not itself recorded: it exposes only standings,
    limits, and Unknowns the session's events already carry.  An empty
    coordinate is absence of record, not negative standing and not Unknown.
    Represented relation candidates are never yielded here; each preserved ingress keeps
    the authority its own event recorded.
    """
    scope = f"workspace:{workspace_id};session:{session_id}"
    attempts: dict[str, dict[str, Any]] = {}
    preserved_ingress_occurrences: list[dict[str, Any]] = []
    interaction_closures: list[dict[str, Any]] = []
    representations: dict[str, dict[str, Any]] = {}
    comparisons: dict[str, dict[str, Any]] = {}
    identifications: dict[str, dict[str, Any]] = {}
    latest_exchange_finding: dict[str, Any] | None = None
    source_validations: dict[str, dict[str, Any]] = {}
    represented_relations: dict[str, dict[str, Any]] = {}
    latest_source_validation: dict[str, Any] | None = None
    latest_represented_relation: dict[str, Any] | None = None
    # Kept sorted and distinct in place rather than as a set sorted on return.
    # A set would have to be rebuilt from the prior list and re-sorted on every
    # advance, which costs the accumulated size each time.  These coordinates
    # do not grow on the five live kinds today, but acquisition would make them
    # grow, and the prior-transfer rule has to hold for every accumulator that
    # can.
    known_loss: list[str] = []
    unknowns: list[str] = []
    conflicts: list[str] = []
    as_of_event_id: str | None = None
    event_count = 0

    if prior is not None:
        # Every accumulator the live event kinds read, taken over from the
        # Standing that already input the earlier occurrences.  Not copied:
        # see the shared-accumulator note above.
        attempts = prior["attempts"]
        preserved_ingress_occurrences = prior["preserved_ingress_occurrences"]
        interaction_closures = prior["interaction_closures"]
        representations = prior["representations"]
        comparisons = prior["comparisons"]
        identifications = prior["identifications"]
        latest_exchange_finding = prior["latest_exchange_finding"]
        source_validations = prior["source_validations"]
        represented_relations = prior["represented_relations"]
        latest_source_validation = prior["latest_source_validation"]
        latest_represented_relation = prior["latest_represented_relation"]
        known_loss = prior["known_loss"]
        unknowns = prior["unknowns"]
        conflicts = prior["conflicts"]
        as_of_event_id = prior["as_of_event_id"]
        event_count = prior["event_count"]

    for event in events:
        if event.session_id != session_id:
            continue
        if not (
            event.kind.startswith("operator.ingress.")
            or event.kind.startswith("operator.representation.")
            or event.kind.startswith("operator.exchange.")
            or event.kind.startswith("operator.interaction.")
        ):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported operator-ingress event: {event.kind}")
        event_count += 1
        as_of_event_id = event.id
        for key, collected in (
            ("known_loss", known_loss),
            ("unknowns", unknowns),
            ("conflicts", conflicts),
        ):
            for value in event.payload.get(key, ()):
                _record_distinct(collected, value)
        if event.kind in {
            _REPRESENTATION_ACT_EVIDENCE_KIND,
            _REPRESENTATION_CARRIAGE_EVIDENCE_KIND,
        }:
            continue
        if event.kind == _REPRESENTATION_RECORDED_KIND:
            payload = event.payload
            if payload["representation_ref"] in representations:
                raise ValueError(
                    "duplicate representation reference: "
                    f"{payload['representation_ref']}"
                )
            representations[payload["representation_ref"]] = {
                "representation_id": payload["representation_ref"],
                "representation_event_id": event.id,
                "emission_attempt_event_id": None,
                "emission_outcome_event_id": None,
                "emitted_event_id": None,
                "representation_result": payload["representation_result"],
                "alternatives": payload["alternatives"],
                "coordinate_bindings": payload["coordinate_bindings"],
                "session_standing_as_of_event_id": payload[
                    "session_standing_as_of_event_id"
                ],
                "prior_exchange_finding": payload.get("prior_exchange_finding"),
                "scope": payload["dimensions"]["scope_locality"],
                "provenance": payload["dimensions"]["source_provenance"],
                "known_loss": payload["known_loss"],
                "unknowns": payload["unknowns"],
                "conflicts": payload["conflicts"],
            }
            continue
        if event.kind in {
            _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
            _REPRESENTATION_EMISSION_CARRIAGE_EVIDENCE_KIND,
        }:
            # These Events preserve exact edge Evidence. They do not add or
            # revise session Standing by identity.
            continue
        if event.kind == _REPRESENTATION_EMISSION_ATTEMPTED_KIND:
            representation_ref = event.payload["representation_ref"]
            if representation_ref not in representations:
                raise ValueError(
                    "representation emission attempt without recorded representation event: "
                    f"{representation_ref}"
                )
            representations[representation_ref]["emission_attempt_event_id"] = event.id
            continue
        if event.kind == _REPRESENTATION_EMITTED_KIND:
            representation_ref = event.payload["representation_ref"]
            if representation_ref not in representations:
                raise ValueError(
                    "representation emission without recorded representation event: "
                    f"{representation_ref}"
                )
            if (
                event.payload["representation_event_id"]
                != representations[representation_ref]["representation_event_id"]
            ):
                raise ValueError(
                    "representation emission does not name its recorded "
                    "representation Act occurrence"
                )
            if (
                event.payload["attempt_ref"]
                != representations[representation_ref]["emission_attempt_event_id"]
            ):
                raise ValueError(
                    "representation emission does not name its recorded attempt"
                )
            representations[representation_ref]["emitted_event_id"] = event.id
            representations[representation_ref]["emission_outcome_event_id"] = event.id
            continue
        if event.kind == _REPRESENTATION_EMISSION_OUTCOME_KIND:
            representation_ref = event.payload["representation_ref"]
            if representation_ref not in representations:
                raise ValueError(
                    "representation emission outcome without recorded representation event: "
                    f"{representation_ref}"
                )
            if (
                event.payload["attempt_ref"]
                != representations[representation_ref]["emission_attempt_event_id"]
            ):
                raise ValueError(
                    "representation emission outcome does not name its recorded attempt"
                )
            representations[representation_ref]["emission_outcome_event_id"] = event.id
            continue
        if event.kind == _COMPARISON_KIND:
            payload = event.payload
            if payload["comparison_ref"] in comparisons:
                raise ValueError(
                    "duplicate comparison reference: "
                    f"{payload['comparison_ref']}"
                )
            # The comparison result is re-derived from recorded C and R;
            # a carried result that contradicts the recorded ingress
            # content or C's recorded coordinates is refused.
            representation = representations.get(payload["representation_ref"])
            if representation is None or (
                payload["representation_event_id"]
                != representation["representation_event_id"]
                or payload["representation_emitted_event_id"]
                != representation["emitted_event_id"]
                or representation["emitted_event_id"] is None
            ):
                raise ValueError(
                    "comparison does not carry the recorded representation "
                    "occurrence provenance"
                )
            response_attempt = attempts.get(payload["response_attempt_ref"])
            preserved_response = (
                response_attempt["preserved_ingress"] if response_attempt else None
            )
            if preserved_response is None or (
                preserved_response["evidence_event_id"]
                != payload["response_ingress_event_id"]
                or preserved_response["raw_material_event_id"]
                != payload["response_capture_event_id"]
            ):
                raise ValueError(
                    "comparison's response evidence does not agree with a "
                    "recorded ingress occurrence"
                )
            # The ingress records no Representation reference, so no check
            # here establishes that this Representation and this ingress
            # belong to one act.  That relation is unestablished.
            expected_representation = preserved_response["content"]
            expected_coordinate_set = sorted(
                alternative["response_coordinate"]
                for alternative in representation["alternatives"]
            )
            expected_match = (
                expected_representation
                if expected_representation in set(expected_coordinate_set)
                else None
            )
            expected_outcome = (
                f"match:{expected_match}"
                if expected_match is not None
                else "no-coordinate-match"
            )
            expected_unknowns = (
                [
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                ]
                if expected_match is not None
                else [
                    "response represented relation Unknown",
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                    "requested treatment Unknown",
                ]
            )
            for field, expected in (
                ("compared_representation", expected_representation),
                ("coordinate_set", expected_coordinate_set),
                ("matched_coordinate", expected_match),
                ("outcome", expected_outcome),
                ("unknowns", expected_unknowns),
            ):
                if payload[field] != expected:
                    raise ValueError(
                        "comparison does not agree with the result derived "
                        f"from recorded payload on {field}"
                    )
            comparisons[payload["comparison_ref"]] = {
                "comparison_ref": payload["comparison_ref"],
                "event_id": event.id,
                "representation_ref": payload["representation_ref"],
                "response_attempt_ref": payload["response_attempt_ref"],
                "response_ingress_event_id": payload["response_ingress_event_id"],
                "response_capture_event_id": payload["response_capture_event_id"],
                "compared_representation": expected_representation,
                "coordinate_set": expected_coordinate_set,
                "matched_coordinate": expected_match,
                "outcome": expected_outcome,
                "unknowns": expected_unknowns,
            }
            continue
        if event.kind == _IDENTIFICATION_KIND:
            payload = event.payload
            if payload["identification_ref"] in identifications:
                raise ValueError(
                    "duplicate identification reference: "
                    f"{payload['identification_ref']}"
                )
            identification = {
                "identification_ref": payload["identification_ref"],
                "event_id": event.id,
                "comparison_ref": payload["comparison_ref"],
                "comparison_event_id": payload["comparison_event_id"],
                "representation_ref": payload["representation_ref"],
                "response_attempt_ref": payload["response_attempt_ref"],
                "identified_alternative": payload["identified_alternative"],
                "basis": payload["basis"],
                "outcome": payload["outcome"],
            }
            identifications[payload["identification_ref"]] = identification
            comparison = comparisons.get(payload["comparison_ref"])
            if comparison is None:
                raise ValueError(
                    "identification without recorded comparison: "
                    f"{payload['comparison_ref']}"
                )
            # The joined pair must agree on every shared coordinate; a
            # mismatched pair is structurally refused rather than composed.
            for identification_key, comparison_key in (
                ("comparison_event_id", "event_id"),
                ("representation_ref", "representation_ref"),
                ("response_attempt_ref", "response_attempt_ref"),
            ):
                if (
                    identification[identification_key]
                    != comparison[comparison_key]
                ):
                    raise ValueError(
                        "identification does not agree with its recorded "
                        f"comparison on {identification_key}"
                    )
            # The only lawful identification result is re-derived from the
            # reconstructed comparison and C's recorded bindings; the
            # carried basis, outcome, and complete identified alternative
            # must equal that reconstruction.
            identification_representation = representations.get(
                identification["representation_ref"]
            )
            if identification_representation is None:
                raise ValueError(
                    "identification names an unrecorded representation: "
                    f"{identification['representation_ref']}"
                )
            matched = comparison["matched_coordinate"]
            expected_identified = None
            if matched is None:
                expected_basis = "no-coordinate-match"
            else:
                bound_alternative_id = identification_representation[
                    "coordinate_bindings"
                ].get(matched)
                recorded_by_id = {
                    alternative["alternative_id"]: alternative
                    for alternative in identification_representation["alternatives"]
                }
                if bound_alternative_id is None:
                    expected_basis = "binding-absent"
                elif bound_alternative_id not in recorded_by_id:
                    expected_basis = "binding-inapplicable"
                else:
                    expected_basis = "identified"
                    recorded = recorded_by_id[bound_alternative_id]
                    expected_identified = {
                        "alternative_id": recorded["alternative_id"],
                        "role": recorded["role"],
                        "response_coordinate": recorded["response_coordinate"],
                        "rendered_label": recorded["rendered_label"],
                    }
            expected_outcome = (
                "alternative-identified"
                if expected_identified is not None
                else "no-represented-alternative-identified"
            )
            if (
                identification["basis"] != expected_basis
                or identification["outcome"] != expected_outcome
                or identification["identified_alternative"] != expected_identified
            ):
                raise ValueError(
                    "identification does not agree with the result derived "
                    "from its recorded comparison and binding"
                )
            identification["identified_alternative"] = expected_identified
            # The most recent complete exchange finding, exactly as recorded.
            latest_exchange_finding = {
                "comparison": comparison,
                "identification": identification,
            }
            continue
        if event.kind == _SOURCE_VALIDATED_KIND:
            payload = event.payload
            # A reconstruction is admitted into Standing only where the recorded
            # representation payload and the recorded identification agree with
            # every coordinate it carries.
            representation = representations.get(payload["representation_ref"])
            if representation is None:
                raise ValueError(
                    "source reconstruction names an unrecorded representation: "
                    f"{payload['representation_ref']}"
                )
            recorded_alternative = next(
                (
                    alternative
                    for alternative in representation["alternatives"]
                    if alternative["alternative_id"]
                    == payload["alternative"]["alternative_id"]
                ),
                None,
            )
            if recorded_alternative is None:
                raise ValueError(
                    "source reconstruction names an alternative outside its "
                    "recorded representation"
                )
            recorded_source = recorded_alternative["represented_source"]
            for key in ("identity", "kind", "source_role", "reference"):
                if payload["source"][key] != recorded_source[key]:
                    raise ValueError(
                        "source reconstruction does not agree with recorded "
                        f"representation payload on source {key}"
                    )
            for key in ("role", "response_coordinate"):
                if payload["alternative"][key] != recorded_alternative[key]:
                    raise ValueError(
                        "source reconstruction does not agree with recorded "
                        f"representation payload on alternative {key}"
                    )
            if (
                payload["representation_event_id"]
                != representation["representation_event_id"]
                or payload["representation_emitted_event_id"]
                != representation["emitted_event_id"]
            ):
                raise ValueError(
                    "source reconstruction does not carry the recorded "
                    "representation occurrence provenance"
                )
            supporting_identification = next(
                (
                    identification
                    for identification in identifications.values()
                    if identification["event_id"]
                    == payload["identification_event_id"]
                ),
                None,
            )
            if supporting_identification is None or (
                supporting_identification["representation_ref"]
                != payload["representation_ref"]
                or supporting_identification["basis"] != "identified"
                or supporting_identification["outcome"]
                != "alternative-identified"
                or supporting_identification["identified_alternative"] is None
                or supporting_identification["identified_alternative"][
                    "alternative_id"
                ]
                != payload["alternative"]["alternative_id"]
                or supporting_identification["comparison_event_id"]
                != payload["comparison_event_id"]
                or supporting_identification["response_attempt_ref"]
                != payload["response_attempt_ref"]
            ):
                raise ValueError(
                    "source reconstruction does not agree with its recorded "
                    "identification"
                )
            # Re-prove Compare -> Identification -> A from the recorded
            # comparison: a match to the identified alternative's own
            # coordinate, bound to its identity by the recorded binding.
            supporting_comparison = comparisons.get(
                supporting_identification["comparison_ref"]
            )
            if supporting_comparison is None:
                raise ValueError(
                    "source reconstruction's identification has no recorded "
                    "comparison"
                )
            matched = supporting_comparison["matched_coordinate"]
            if (
                matched is None
                or supporting_comparison["outcome"] != f"match:{matched}"
                or recorded_alternative["response_coordinate"] != matched
                or representation["coordinate_bindings"].get(matched)
                != payload["alternative"]["alternative_id"]
            ):
                raise ValueError(
                    "source reconstruction is not supported by a recorded match "
                    "bound to the identified alternative"
                )
            if (
                payload["response_ingress_event_id"]
                != supporting_comparison["response_ingress_event_id"]
                or payload["response_capture_event_id"]
                != supporting_comparison["response_capture_event_id"]
            ):
                raise ValueError(
                    "source reconstruction does not carry its comparison's "
                    "recorded response evidence"
                )
            response_attempt = attempts.get(payload["response_attempt_ref"])
            preserved_response = (
                response_attempt["preserved_ingress"] if response_attempt else None
            )
            if preserved_response is None or (
                preserved_response["evidence_event_id"]
                != payload["response_ingress_event_id"]
                or preserved_response["raw_material_event_id"]
                != payload["response_capture_event_id"]
            ):
                raise ValueError(
                    "source reconstruction's response evidence does not agree "
                    "with the recorded ingress occurrence"
                )
            if payload["representation"] != recorded_alternative["representation"]:
                raise ValueError(
                    "source reconstruction does not agree with recorded representation Act "
                    "source coordinates on the representation boundary"
                )
            if payload["validation_ref"] in source_validations:
                raise ValueError(
                    f"duplicate reconstruction reference: {payload['validation_ref']}"
                )
            reconstruction = {
                "validation_ref": payload["validation_ref"],
                "event_id": event.id,
                "representation_ref": payload["representation_ref"],
                "representation_event_id": payload[
                    "representation_event_id"
                ],
                "representation_emitted_event_id": payload[
                    "representation_emitted_event_id"
                ],
                "comparison_event_id": payload["comparison_event_id"],
                "identification_event_id": payload["identification_event_id"],
                "response_attempt_ref": payload["response_attempt_ref"],
                "response_ingress_event_id": payload["response_ingress_event_id"],
                "response_capture_event_id": payload["response_capture_event_id"],
                "alternative": payload["alternative"],
                "source": payload["source"],
                # The complete representation boundary, reconstructed from
                # the recorded representation payload it was validated against.
                "representation": recorded_alternative["representation"],
            }
            source_validations[payload["validation_ref"]] = reconstruction
            latest_source_validation = reconstruction
            continue
        if event.kind == _REPRESENTED_RELATION_KIND:
            payload = event.payload
            validation_event_id = payload["source_validation_event_id"]
            reconstruction = source_validations.get(payload["validation_ref"])
            if reconstruction is None:
                raise ValueError(
                    "represented relation without recorded source reconstruction: "
                    f"{payload['validation_ref']}"
                )
            # The joined pair must agree on every shared coordinate; a
            # mismatched pair is structurally refused rather than composed.
            representation = representations.get(payload["representation_ref"])
            if representation is None:
                raise ValueError(
                    "represented relation names an unrecorded representation: "
                    f"{payload['representation_ref']}"
                )
            recorded_alternative = next(
                (
                    alternative
                    for alternative in representation["alternatives"]
                    if alternative["alternative_id"] == payload["alternative_id"]
                ),
                None,
            )
            if recorded_alternative is None:
                raise ValueError(
                    "represented relation names an alternative outside its "
                    "recorded representation"
                )
            recorded_source = recorded_alternative["represented_source"]
            recorded_representation = recorded_alternative["representation"]
            agreements = (
                (validation_event_id, reconstruction["event_id"], "source_validation_event_id"),
                (
                    payload["representation_ref"],
                    reconstruction["representation_ref"],
                    "representation_ref",
                ),
                (
                    payload["representation_event_id"],
                    reconstruction["representation_event_id"],
                    "representation_event_id",
                ),
                (
                    payload["identification_event_id"],
                    reconstruction["identification_event_id"],
                    "identification_event_id",
                ),
                (
                    payload["alternative_id"],
                    reconstruction["alternative"]["alternative_id"],
                    "alternative_id",
                ),
                (
                    payload["source_identity"],
                    reconstruction["source"]["identity"],
                    "source_identity",
                ),
                (
                    payload["source_reference"],
                    reconstruction["source"]["reference"],
                    "source_reference",
                ),
                # The proposition and its source role must equal the recorded
                # representation payload exactly; a forged M is refused here.
                (payload["proposition"], recorded_source["represented_result"], "proposition"),
                (
                    payload["source_role"],
                    recorded_source["source_role"],
                    "source_role",
                ),
                (
                    payload["representation_result_boundary"],
                    recorded_representation["representation_result"],
                    "representation_result_boundary",
                ),
                (
                    payload["representation_scope"],
                    recorded_representation["scope"],
                    "representation_scope",
                ),
            )
            for supplied, recorded, coordinate in agreements:
                if supplied != recorded:
                    raise ValueError(
                        "represented relation does not agree with its recorded "
                        f"source reconstruction on {coordinate}"
                    )
            # The structural Authority coordinates are reconstructed from
            # recorded payload, and the carried separation must equal the
            # reconstruction -- a forged standing, support, Evidence, or
            # Scope is refused rather than exposed to a later Act.
            reconstructed_separation = {
                "source_authority": {
                    "standing": "bounded",
                    "supports": ["source-supplied-with-relation-Assertion"],
                    "evidence_event_ids": [reconstruction["representation_event_id"]],
                    "scope": {
                        "source_identity": reconstruction["source"]["identity"],
                        "proposition": recorded_source["represented_result"],
                    },
                },
                "response_comparison_authority": {
                    "standing": "bounded",
                    "supports": ["response-matched-coordinate-within-representation"],
                    "evidence_event_ids": [reconstruction["comparison_event_id"]],
                    "scope": {
                        "representation_ref": reconstruction["representation_ref"],
                        "response_attempt_ref": reconstruction["response_attempt_ref"],
                    },
                },
                "support_relation_standing": {
                    "standing": "established",
                    "supports": ["source-expresses-proposition"],
                    "evidence_event_ids": [
                        reconstruction["representation_event_id"],
                        reconstruction["event_id"],
                    ],
                    "scope": {
                        "source_identity": reconstruction["source"]["identity"],
                        "proposition": recorded_source["represented_result"],
                    },
                },
                "operator_authority": {
                    "standing": "unresolved",
                    "supports": [],
                    "evidence_event_ids": [],
                    "scope": {"proposition": recorded_source["represented_result"]},
                },
            }
            carried_separation = payload["authority_separation"]
            if set(carried_separation) != set(reconstructed_separation):
                raise ValueError(
                    "represented relation does not carry the four Authority "
                    "coordinates"
                )
            authority_separation = {}
            for name, reconstructed in reconstructed_separation.items():
                carried = carried_separation[name]
                for field, value in reconstructed.items():
                    if carried.get(field) != value:
                        raise ValueError(
                            "represented relation does not agree with recorded "
                            f"source coordinates on {name}.{field}"
                        )
                authority_separation[name] = {
                    **reconstructed,
                    "source_role": carried.get("source_role"),
                }
            # The relation's remaining Standing coordinates are carried
            # invariants at this boundary; a forged loss, Unknown, or
            # conflicts are refused rather than exposed.
            reconstructed_relation_standing = {
                "support_relation_standing": (
                    "developer-supplied relation Assertion "
                    "preserved by the recorded Representation Act occurrence"
                ),
                "known_loss": [],
                "unknowns": [
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                ],
                    "conflicts": [],
            }
            for field, value in reconstructed_relation_standing.items():
                if payload[field] != value:
                    raise ValueError(
                        "represented relation does not agree with recorded "
                        f"source coordinates on {field}"
                    )
            if payload["relation_ref"] in represented_relations:
                raise ValueError(
                    f"duplicate relation reference: {payload['relation_ref']}"
                )
            relation = {
                "relation_ref": payload["relation_ref"],
                "event_id": event.id,
                "source_validation_event_id": validation_event_id,
                "validation_ref": payload["validation_ref"],
                "representation_ref": payload["representation_ref"],
                "representation_event_id": payload[
                    "representation_event_id"
                ],
                "identification_event_id": payload["identification_event_id"],
                "alternative_id": payload["alternative_id"],
                "source_identity": payload["source_identity"],
                "proposition": payload["proposition"],
                "source_role": payload["source_role"],
                "source_reference": payload["source_reference"],
                "representation_result_boundary": payload[
                    "representation_result_boundary"
                ],
                "representation_scope": payload["representation_scope"],
                "support_relation_standing": reconstructed_relation_standing[
                    "support_relation_standing"
                ],
                "authority_separation": authority_separation,
                "known_loss": reconstructed_relation_standing["known_loss"],
                "unknowns": reconstructed_relation_standing["unknowns"],
                "conflicts": reconstructed_relation_standing["conflicts"],
            }
            represented_relations[payload["relation_ref"]] = relation
            latest_represented_relation = relation
            continue
        attempt_ref = event.payload["attempt_ref"]
        attempt = attempts.setdefault(
            attempt_ref,
            {"event_ids": [], "preserved_ingress": None, "interaction_closure": None},
        )
        attempt["event_ids"].append(event.id)
        if event.kind == "operator.ingress.ingress_occurred":
            occurrence = {
                "attempt_ref": attempt_ref,
                "subject_ref": event.payload["dimensions"]["identity"],
                "standing": "preserved",
                "authority": event.payload["dimensions"]["authority"],
                "evidence_event_id": event.id,
                "raw_material_event_id": event.payload["raw_material_event_id"],
                "content": event.payload["dimensions"]["content"],
            }
            attempt["preserved_ingress"] = occurrence
            preserved_ingress_occurrences.append(occurrence)
        elif event.kind == "operator.ingress.stopping_occurred":
            closure = {
                "attempt_ref": attempt_ref,
                "response_kind": event.payload.get("response_kind"),
                "evidence_event_id": event.id,
            }
            attempt["interaction_closure"] = closure
            interaction_closures.append(closure)

    return {
        "workspace_id": workspace_id,
        "session_id": session_id,
        "as_of_event_id": as_of_event_id,
        "event_count": event_count,
        "attempts": attempts,
        "preserved_ingress_occurrences": preserved_ingress_occurrences,
        "interaction_closures": interaction_closures,
        "representations": representations,
        # No "current" Representation is projected.  Emission order is
        # reconstructible from `representations`, which preserves representation Act and
        # emission occurrences in append order; naming one of them current
        # would assert present relevance that no occurrence establishes.
        # Exactly the relation standings recorded by session events.  No
        # current event kind records one, so this stays empty until a
        # responsible occurrence does; emptiness is absence of record only.
        "comparisons": comparisons,
        "identifications": identifications,
        "latest_exchange_finding": latest_exchange_finding,
        "source_validations": source_validations,
        "represented_relations": represented_relations,
        "latest_source_validation": latest_source_validation,
        "latest_represented_relation": latest_represented_relation,
        "recorded_relation_standings": [],
        "known_loss": known_loss,
        "unknowns": unknowns,
        "conflicts": conflicts,
    }
