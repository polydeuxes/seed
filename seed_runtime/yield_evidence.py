"""Private physiology for Evidence concerning one exact yielded result.

This does not establish Responsibility. It preserves, from inside
an act after that act has fixed its result, Evidence committing to the exact
coordinates yielded. The resulting Event is Evidence concerning the
yield occurrence; it is not that occurrence by identity.

The helper is private implementation plumbing, not the guarantee. The result's
carried relation to this Evidence distinguishes a yielded result from an
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

YIELD_EVIDENCE_KIND = "operator.yield.evidence_recorded"
_YIELD_COMMITMENT_DOMAIN = b"seed.yield-evidence.v1\0"


def _commit_part(digest: "hashlib._Hash", value: str) -> None:
    """Commit one declared string representation in this mechanical domain."""

    if not isinstance(value, str):
        raise TypeError(
            "a yield commitment part is an exact representation, not "
            f"{type(value).__name__}"
        )
    encoded = value.encode("utf-8")
    digest.update(len(encoded).to_bytes(8, "big"))
    digest.update(encoded)


def yield_commitment(convention: str, content: dict[str, Any]) -> str:
    """Commit to canonical JSON of declared coordinates in this domain.

    The digest does not identify literal carriage bytes. Distinct JSON texts
    that decode to the same coordinate values receive the same commitment.
    """

    digest = hashlib.sha256(_YIELD_COMMITMENT_DOMAIN)
    _commit_part(digest, convention)
    _commit_part(
        digest, json.dumps(content, sort_keys=True, separators=(",", ":"))
    )
    return digest.hexdigest()


def _record_yield_evidence(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str | None,
    convention: str,
    yielding_act: str,
    yielded_result_kind: str,
    result_identity: str,
    yielded_content: dict[str, Any],
    responsibility: str,
    responsible_boundary: str = "unestablished",
) -> Event:
    """Preserve Evidence from inside an act for its already-fixed result."""

    return ledger.append(
        YIELD_EVIDENCE_KIND,
        workspace_id,
        {
            "dimensions": {
                "identity": f"yield-evidence:{result_identity}",
                "content": (
                    f"evidence that {yielding_act} yielded this exact "
                    f"{yielded_result_kind} at its exact Act boundary"
                ),
                "standing": "yielded",
                "yielding_act": yielding_act,
                "yield_occurrence_evidence": (
                    "preserved at the exact Act boundary after this exact "
                    "result was fixed; the result carries the relation to this"
                ),
                "responsibility": responsibility,
                "responsible_boundary": responsible_boundary,
                "authority": (
                    "establishes the exact occurrence-to-result edge at this "
                    "Act boundary; establishes no responsibility, "
                    "authorization, or successful return from "
                    "an enclosing call"
                ),
                "occurrence_preservation": (
                    "evidence concerning a yield occurrence, durably "
                    "recorded; not that occurrence by identity"
                ),
            },
            "yield_convention": convention,
            "yield_commitment": yield_commitment(
                convention, yielded_content
            ),
            "yield_coordinates": sorted(yielded_content),
            "yielded_result_kind": yielded_result_kind,
        },
        session_id=session_id,
    )
