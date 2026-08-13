"""Private physiology for Evidence concerning one exact produced result.

This does not recover a Producer or Responsibility. It preserves, from inside
an act after that act has fixed its result, Evidence committing to the exact
coordinates produced. The resulting Event is Evidence concerning the
production occurrence; it is not that occurrence by identity.

The helper stays private. Exposing an operation that accepts arbitrary result
content would create a second recorder able to manufacture production standing
for caller-constructed objects.
"""

from __future__ import annotations

import json
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.support_basis import support_commitment

PRODUCTION_EVIDENCE_KIND = "operator.production.evidence_recorded"


def production_commitment(convention: str, content: dict[str, Any]) -> str:
    """Commit to every coordinate the producing act established."""

    return support_commitment(
        convention,
        (json.dumps(content, sort_keys=True, separators=(",", ":")),),
    )


def _record_production_evidence(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str | None,
    convention: str,
    producing_act: str,
    produced_result_kind: str,
    result_identity: str,
    produced_content: dict[str, Any],
    producer: str,
    responsibility: str,
) -> Event:
    """Preserve Evidence from inside an act for its already-fixed result."""

    return ledger.append(
        PRODUCTION_EVIDENCE_KIND,
        workspace_id,
        {
            "dimensions": {
                "identity": f"production-evidence:{result_identity}",
                "content": (
                    f"evidence that {producing_act} produced this exact "
                    f"{produced_result_kind} at its producing boundary"
                ),
                "standing": "produced",
                "producing_act": producing_act,
                "producer_evidence": (
                    "preserved at the producing boundary after this exact "
                    "result was fixed; the result carries the relation to this"
                ),
                "producer": producer,
                "responsibility": responsibility,
                "authority_warrant": (
                    "establishes production of this exact result at this "
                    "producing boundary; establishes no producer identity, "
                    "responsibility, authorization, or successful return from "
                    "an enclosing call"
                ),
                "occurrence_preservation": (
                    "evidence concerning a production occurrence, durably "
                    "recorded; not that occurrence by identity"
                ),
            },
            "production_convention": convention,
            "production_commitment": production_commitment(
                convention, produced_content
            ),
            "production_coordinates": sorted(produced_content),
            "produced_result_kind": produced_result_kind,
        },
        session_id=session_id,
    )
