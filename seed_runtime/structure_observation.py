"""Implementation-local owner for substrate-independent structure observation.

Structure Observation owns the shared boundary for read-only structural
extraction. Substrate adapters (Markdown documentation, Python repository/code,
relationship extraction, and repository-state observers) keep ownership of their
parsing, record schemas, traversal, and compatibility surfaces.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StructureObservationBoundary:
    """Substrate-independent ownership boundary for structural observation."""

    read_only: bool = True
    structural_extraction: bool = True
    preserves_evidence: bool = True
    interprets_content: bool = False
    owns_substrate_parsing: bool = False
    owns_grammar: bool = False
    owns_responsibility_recovery: bool = False
    owns_lexicon: bool = False
    writes_event_ledger: bool = False
    mutates_repository: bool = False
    mutates_cluster: bool = False

    def as_documentation_boundary(self) -> dict[str, bool]:
        """Return the existing Documentation Structure compatibility boundary."""

        return {
            "read_only": self.read_only,
            "interprets_prose": self.interprets_content,
            "infers_claims": False,
            "infers_authority": False,
            "infers_shapes": False,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_repository": self.mutates_repository,
        }


STRUCTURE_OBSERVATION_BOUNDARY = StructureObservationBoundary()

STRUCTURE_OBSERVATION_BOUNDARY_TEXT = (
    "read only; structural extraction; evidence preservation; "
    "non-interpretation; substrate adapter boundary; no substrate parsing; "
    "no grammar interpretation; no responsibility recovery; no lexicon stabilization; "
    "no event ledger writes; no repository mutation; no cluster mutation"
)

STRUCTURE_OBSERVATION_OWNER = "Structure Observation"
