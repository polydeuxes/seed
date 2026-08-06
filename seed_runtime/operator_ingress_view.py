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
    return "\n".join(lines) + "\n"
