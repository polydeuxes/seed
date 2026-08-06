"""Read-only formation of the successful operator-ingress View."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any


def _value(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def format_operator_ingress_view(projection: Mapping[str, Any]) -> str:
    """Expose only standing and limits present in a successful projection."""
    current = projection["current_standing"]
    preserved = current["preserved_ingress"]
    if preserved is None:
        raise ValueError("operator-ingress View requires a successful projection")

    material = projection["addressable_operator_material"]
    final_event_id = projection["event_ids"][-1]
    final_event = projection["dimensional_standing"][final_event_id]
    lines = [
        "Operator ingress View",
        f"Ingress occurrence: {_value(preserved['subject_ref'])}",
        "Represented material: "
        f"{_value(material['exact_operator_material']['exact_text'])}",
        "Current Standing:",
    ]
    for coordinate in (
        "raw_initial_material",
        "preserved_ingress",
        "interaction_closure",
    ):
        standing = current[coordinate]
        if standing is None:
            lines.append(f"  {coordinate}: null")
            continue
        lines.append(
            f"  {coordinate}: subject={_value(standing['subject_ref'])}; "
            f"standing={_value(standing['dimensions']['standing'])}; "
            f"evidence={_value(standing['evidence_event_id'])}"
        )
    lines.extend(
        (
            f"Provenance: {_value(material['provenance'])}",
            f"Source references: {_value(material['scope'])}",
            f"Known loss: {_value(material['known_loss'])}",
            f"Conflicts: {_value(projection['conflicts'])}",
            f"Unknowns: {_value(material['unknowns'])}",
            "Authority: "
            f"{_value(preserved['dimensions']['authority_warrant'])}",
            "Communicative meaning: unresolved (Unknown).",
            "Exact final event: "
            f"{_value(final_event_id)} ({_value(final_event['event_kind'])})",
            f"View accounts for events through: {_value(final_event_id)}",
        )
    )
    session_standing = projection.get("session_standing")
    if session_standing is not None:
        lines.extend(_session_standing_lines(session_standing))
    return "\n".join(lines) + "\n"


def _session_standing_lines(standing: Mapping[str, Any]) -> list[str]:
    """Expose earlier session Standing exactly as its events carried it.

    Every line is inherited from recorded session events; nothing is
    interpreted, and no meaning candidate is produced.  An empty coordinate
    is rendered as absence of record, not negative standing and not Unknown.
    """
    lines = [
        "Session Standing "
        f"(session {_value(standing['session_id'])}, "
        f"as of event {_value(standing['as_of_event_id'])}):",
        f"  Prior preserved ingress occurrences: {len(standing['preserved_ingress_occurrences'])}",
    ]
    for occurrence in standing["preserved_ingress_occurrences"]:
        lines.append(
            f"    {_value(occurrence['subject_ref'])}: "
            f"standing={_value(occurrence['standing'])}; "
            f"authority={_value(occurrence['authority_warrant'])}; "
            f"evidence={_value(occurrence['evidence_event_id'])}"
        )
    lines.append(
        f"  Prior interaction closures: {len(standing['interaction_closures'])}"
    )
    for closure in standing["interaction_closures"]:
        lines.append(
            f"    {_value(closure['attempt_ref'])}: "
            f"response_kind={_value(closure['response_kind'])}; "
            f"evidence={_value(closure['evidence_event_id'])}"
        )
    if standing["recorded_relation_standings"]:
        lines.append(
            f"  Recorded relation standings: {_value(standing['recorded_relation_standings'])}"
        )
    else:
        lines.append(
            "  Recorded relation standings: none recorded"
            " (absence of record; not negative standing; not Unknown)"
        )
    lines.extend(
        (
            f"  Session known loss: {_value(standing['known_loss'])}",
            f"  Session unknowns: {_value(standing['unknowns'])}",
            f"  Session conflicts: {_value(standing['conflicts'])}",
        )
    )
    return lines
