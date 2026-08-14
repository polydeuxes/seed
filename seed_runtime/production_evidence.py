"""Private physiology for Evidence concerning one exact produced result.

This does not establish Responsibility. It preserves, from inside
an act after that act has fixed its result, Evidence committing to the exact
coordinates produced. The resulting Event is Evidence concerning the
production occurrence; it is not that occurrence by identity.

The helper is private implementation plumbing, not the guarantee. The result's
carried relation to this Evidence distinguishes a produced result from an
identical caller-constructed representation. Exposing a public operation that
accepts arbitrary result content would instead create a second recorder able to
manufacture that relation.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import EventLedger

PRODUCTION_EVIDENCE_KIND = "operator.production.evidence_recorded"
_PRODUCTION_COMMITMENT_DOMAIN = b"seed.production-evidence.v1\0"


def _commit_part(digest: "hashlib._Hash", value: str) -> None:
    """Commit one exact representation without borrowing another domain."""

    if not isinstance(value, str):
        raise TypeError(
            "a production commitment part is an exact representation, not "
            f"{type(value).__name__}"
        )
    encoded = value.encode("utf-8")
    digest.update(len(encoded).to_bytes(8, "big"))
    digest.update(encoded)


def production_commitment(convention: str, content: dict[str, Any]) -> str:
    """Commit to every coordinate under the production-evidence domain."""

    digest = hashlib.sha256(_PRODUCTION_COMMITMENT_DOMAIN)
    _commit_part(digest, convention)
    _commit_part(
        digest, json.dumps(content, sort_keys=True, separators=(",", ":"))
    )
    return digest.hexdigest()


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
    responsibility: str,
    responsible_boundary: str = "unrecovered",
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
                "production_occurrence_evidence": (
                    "preserved at the producing boundary after this exact "
                    "result was fixed; the result carries the relation to this"
                ),
                "responsibility": responsibility,
                "responsible_boundary": responsible_boundary,
                "authority": (
                    "establishes production of this exact result at this "
                    "producing boundary; establishes no responsibility, "
                    "authorization, or successful return from "
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
