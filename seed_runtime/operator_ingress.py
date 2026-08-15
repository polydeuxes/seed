"""One-attempt bounded operator-ingress representation handling and attempt_standing."""

from __future__ import annotations

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_ingress_representation import (
    CapturedOperatorMaterial,
)


# Who supplied the material an occurrence preserves. Not the responsible boundary
# or Act occurrence that recorded it, and not authorship
# — an operator who supplies a book did not write it. `#2490` records why this
# has to exist before Seed preserves what it emitted: without it a later
# measurement over "preserved material" cannot decline to have as input Seed's own
# output, and Seed's account of a fire becomes material saying a fire occurred.
OPERATOR_ORIGIN = "operator"
SEED_ORIGIN = "this Seed"


def _dimensions(
    *,
    identity,
    content,
    standing,
    source,
    responsibility,
    authority,
    scope,
    occurrence,
    evidence_scope=None,
):
    dimensions = {
        "identity": identity,
        "content": content,
        "standing": standing,
        "source_provenance": source,
        "responsibility": responsibility,
        "authority": authority,
        "scope_locality": scope,
        "occurrence_preservation": occurrence,
    }
    if evidence_scope is not None:
        dimensions["evidence_scope"] = evidence_scope
    return dimensions


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
        locality_id=session,
    )


def update_operator_ingress_standing(attempts, event, *, ledger=None) -> None:
    """Dispatch one operator-ingress event into the dedicated current standing.

    ``attempts`` is the per-attempt attempt_standing mapping and is the whole of what
    this read has as input. It reads no entity, normalized Assertion, alias, relationship, or
    result condition, so nothing here requires a whole-workspace attempt_standing to exist.
    """
    if not event.kind.startswith("operator.material."):
        return
    subject_by_kind = {
        "operator.material.raw_captured": "raw_initial_material",
        "operator.material.occurred": "preserved_ingress",
        "operator.material.stopping_occurred": "interaction_closure",
    }
    supported_kinds = set(subject_by_kind)
    if event.kind not in supported_kinds:
        raise ValueError(f"unsupported operator-ingress event: {event.kind}")
    attempt = event.payload["attempt_ref"]
    standing = attempts.setdefault(
        attempt,
        {
            "event_ids": [],
            "dimensional_standing": {},
            "current_standing": {
                subject: None
                for subject in (
                    "raw_initial_material",
                    "preserved_ingress",
                    "interaction_closure",
                )
            },
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
        },
    )
    standing["event_ids"].append(event.id)
    # Occurrences are evidence in their own right.  Keep each complete
    # eight-dimensional description rather than replacing it with the tail event.
    standing["dimensional_standing"][event.id] = {
        "event_kind": event.kind,
        "subject_ref": event.payload["dimensions"]["identity"],
        "dimensions": event.payload["dimensions"],
        "provenance_occurrence_refs": list(
            event.payload.get("provenance_occurrence_refs", ())
        ),
    }
    subject = subject_by_kind[event.kind]
    dimensions = dict(event.payload["dimensions"])
    if subject == "preserved_ingress":
        dimensions["standing"] = "preserved"
    standing["current_standing"][subject] = {
        "subject_ref": dimensions["identity"],
        "dimensions": dimensions,
        "evidence_event_id": event.id,
    }
    if event.kind == "operator.material.occurred" and "raw_material_event_id" in event.payload:
        from seed_runtime.operator_ingress_addressable_material import (
            form_operator_ingress_addressable_material,
        )

        if ledger is not None:
            standing["addressable_operator_material"] = (
                form_operator_ingress_addressable_material(
                    ingress_occurrence=event, ledger=ledger
                ).to_json_dict()
            )
    standing["last_event_kind"] = event.kind
    for key in ("known_loss", "unknowns", "conflicts"):
        standing[key] = sorted(set((*standing[key], *event.payload.get(key, ()))))
    for key in ("closed", "response_kind"):
        if key in event.payload:
            standing[key] = event.payload[key]


def _capture_representation(
    *,
    ledger,
    workspace,
    session,
    attempt,
    material_role,
    captured_material: CapturedOperatorMaterial,
    provenance_occurrence_refs=(),
):
    capture = captured_material
    capture_ref = new_id("operator_material")
    captured = _record(
        ledger,
        "operator.material.raw_captured",
        workspace,
        session,
        attempt,
        _dimensions(
            identity=capture_ref,
            content=capture.exact_bytes.hex(),
            standing="captured",
            source=capture.capture_boundary,
            responsibility="competent-raw-material-capture",
            authority="unestablished",
            evidence_scope="occurrence Evidence only",
            scope=f"workspace:{workspace};locality:{session};role:{material_role}",
            occurrence="exact boundary bytes durably preserved as hexadecimal",
        ),
        material_role=material_role,
        exact_bytes_hex=capture.exact_bytes.hex(),
        byte_count=len(capture.exact_bytes),
        eof=capture.eof,
        delimiter_hex=capture.delimiter_hex,
        capture_boundary=capture.capture_boundary,
        byte_material_origin=capture.byte_material_origin,
        known_loss=list(capture.known_loss),
        provenance_occurrence_refs=list(provenance_occurrence_refs),
    )
    return capture, captured


def _attempt_standing(*, events, ledger, attempt):
    """Read one attempt from exactly the occurrences it recorded.

    The whole-workspace replay this replaces rebuilt every entity, normalized Assertion,
    alias, relationship, and index in order to return one bounded attempt, and
    it did so once per attempt, so occurrence *j* was replayed by every later
    attempt. The cost here is constant in the number of earlier attempts.

    The addressable material is formed through
    `form_operator_ingress_addressable_material`, which consults the ledger for
    this attempt's exact raw occurrence and refuses foreign, incomplete, or
    unrecorded material. What is not performed is replay of unrelated historical
    events.
    """

    attempts: dict[str, dict] = {}
    for event in events:
        update_operator_ingress_standing(attempts, event, ledger=ledger)
    return attempts[attempt]


def run_operator_ingress_attempt(
    *,
    ledger: EventLedger,
    workspace_id: str,
    locality_id: str,
    captured_ingress: CapturedOperatorMaterial,
    locality_standing: dict[str, object] | None = None,
    supplied_material_representation: str | None = None,
) -> dict[str, object]:
    """Capture, examine, and project one bounded non-EOF ingress attempt.

    ``locality_standing`` is already-projected Standing from this session's
    earlier recorded events.  It is carried on the returned attempt_standing for
    the Representation to expose; it is not recorded, interpreted, or used to
    alter this attempt's own occurrence handling.

    The occurrence names no Representation.  A relation between this preserved
    material and any preserved Representation is its own bounded Assertion with
    its own participants, roles, occurrence, and Evidence; it does not live
    inside one participant's record, and no such relation is established
    here.
    """
    if captured_ingress.eof:
        raise ValueError("captured_ingress must be non-EOF")
    if supplied_material_representation is not None and type(
        supplied_material_representation
    ) is not str:
        raise ValueError("supplied_material_representation must be exact material")

    attempt = new_id("operator_ingress_attempt")
    captured_ingress, ingress_capture = _capture_representation(
        ledger=ledger,
        workspace=workspace_id,
        session=locality_id,
        attempt=attempt,
        captured_material=captured_ingress,
        material_role="initial_ingress",
    )
    ingress_kind = (
        "empty" if captured_ingress.exact_bytes in {b"\n", b"\r\n"} else "bytes"
    )
    representation_payload = {}
    if supplied_material_representation is not None:
        representation_payload = {
            "represented_material": supplied_material_representation,
            "material_representation": {
                "available": True,
                "source": "explicitly supplied representation",
            },
        }
    ingress_event = _record(
        ledger,
        "operator.material.occurred",
        workspace_id,
        locality_id,
        attempt,
        _dimensions(
            identity=attempt,
            content=captured_ingress.exact_bytes.hex(),
            standing="occurred",
            source=ingress_capture.id,
            responsibility="operator-ingress",
            authority="unestablished",
            evidence_scope="occurrence only; represented relation Unknown",
            scope=f"workspace:{workspace_id};locality:{locality_id}",
            occurrence="exact bytes preserve raw-capture provenance",
        ),
        material_origin=OPERATOR_ORIGIN,
        ingress_kind=ingress_kind,
        byte_count=len(captured_ingress.exact_bytes),
        raw_material_event_id=ingress_capture.id,
        **representation_payload,
        known_loss=list(captured_ingress.known_loss),
        unknowns=["what these bytes represent remains Unknown"],
        provenance_occurrence_refs=[ingress_capture.id],
    )
    attempt_standing = _attempt_standing(
        events=(ingress_capture, ingress_event),
        ledger=ledger,
        attempt=attempt,
    )
    if locality_standing is not None:
        attempt_standing["locality_standing"] = locality_standing
    return attempt_standing
