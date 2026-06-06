"""Read-only inventory of Seed's current deterministic rule metadata."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from typing import Any, Iterable

from seed_runtime.base import SeedModel
from seed_runtime.capability_catalog import CapabilityCatalog
from seed_runtime.entity_type_catalog import EntityTypeCatalog
from seed_runtime.inference_catalog import InferenceCatalog
from seed_runtime.predicate_catalog import PredicateCatalog
from seed_runtime.relationship_catalog import RelationshipCatalog

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field


class RuleInventoryEntry(SeedModel):
    """One source-attributed deterministic rule or rule-like catalog entry."""

    id: str
    category: str
    source: str
    summary: str
    if_conditions: list[str]
    then_effects: list[str]
    metadata: dict[str, Any] = Field(default_factory=dict)


class RuleInventoryBuilder:
    """Collect rule metadata from existing read-only catalogs.

    The builder does not inspect live hosts, execute tools, append events, project
    state, or introduce a rule engine. It only translates existing catalog and
    static validation metadata into stable inventory entries.
    """

    def __init__(
        self,
        *,
        predicate_catalog: PredicateCatalog | None = None,
        relationship_catalog: RelationshipCatalog | None = None,
        entity_type_catalog: EntityTypeCatalog | None = None,
        inference_catalog: InferenceCatalog | None = None,
        capability_catalog: CapabilityCatalog | None = None,
    ) -> None:
        self.predicate_catalog = predicate_catalog or PredicateCatalog.load()
        self.relationship_catalog = relationship_catalog or RelationshipCatalog.load()
        self.entity_type_catalog = entity_type_catalog or EntityTypeCatalog.load()
        self.inference_catalog = inference_catalog or InferenceCatalog.load()
        self.capability_catalog = capability_catalog or CapabilityCatalog.load()

    def collect(self) -> list[RuleInventoryEntry]:
        """Return all known deterministic inventory entries in stable order."""

        return _sort_entries(
            [
                *self._predicate_entries(),
                *self._predicate_mapping_entries(),
                *self._relationship_entries(),
                *self._entity_type_entries(),
                *self._inference_entries(),
                *self._graph_validation_entries(),
                *self._capability_resolution_entries(),
            ]
        )

    def _predicate_entries(self) -> list[RuleInventoryEntry]:
        entries: list[RuleInventoryEntry] = []
        for predicate in self.predicate_catalog.list_predicates():
            allowed = [str(value) for value in predicate.allowed_values]
            conditions = [f"fact predicate is {predicate.predicate!r}"]
            if allowed:
                conditions.append("value is one of: " + ", ".join(allowed))
            effects = [
                f"predicate is treated as a {predicate.kind}",
                f"value type is {predicate.value_type}",
                f"current fact cardinality is {predicate.cardinality}",
            ]
            entries.append(
                RuleInventoryEntry(
                    id=f"predicate.{predicate.predicate}",
                    category="predicate_catalog",
                    source=_source("predicate_catalog/core.json"),
                    summary=f"Canonical predicate {predicate.predicate}.",
                    if_conditions=conditions,
                    then_effects=effects,
                    metadata={
                        "predicate": predicate.predicate,
                        "kind": predicate.kind,
                        "value_type": predicate.value_type,
                        "cardinality": predicate.cardinality,
                        "allowed_values": list(predicate.allowed_values),
                    },
                )
            )
        return entries

    def _predicate_mapping_entries(self) -> list[RuleInventoryEntry]:
        entries: list[RuleInventoryEntry] = []
        for mapping in self.predicate_catalog.list_mappings():
            source_name = mapping.source_name or "*"
            entries.append(
                RuleInventoryEntry(
                    id=f"predicate_mapping.{source_name}.{mapping.predicate}",
                    category="predicate_mapping",
                    source=_source("predicate_catalog/core.json"),
                    summary=(
                        f"Map provider predicate {mapping.predicate} to "
                        f"{mapping.canonical_predicate}."
                    ),
                    if_conditions=[
                        f"observation source is {source_name!r}",
                        f"observation predicate is {mapping.predicate!r}",
                    ],
                    then_effects=[
                        f"canonical predicate becomes {mapping.canonical_predicate!r}",
                        "value map is applied when a matching value is declared",
                    ],
                    metadata={
                        "source_name": mapping.source_name,
                        "predicate": mapping.predicate,
                        "canonical_predicate": mapping.canonical_predicate,
                        "value_map": dict(mapping.value_map),
                    },
                )
            )
        return entries

    def _relationship_entries(self) -> list[RuleInventoryEntry]:
        entries: list[RuleInventoryEntry] = []
        for relationship in self.relationship_catalog.list_relationships():
            object_effect = (
                f"object is fixed to {relationship.object!r}"
                if relationship.object is not None
                else "object is taken from the source fact value"
            )
            entries.append(
                RuleInventoryEntry(
                    id=f"relationship.{relationship.relationship}",
                    category="relationship_catalog",
                    source=_source("relationship_catalog/core.json"),
                    summary=f"Project {relationship.relationship} relationships.",
                    if_conditions=[
                        "fact predicate is one of: "
                        + ", ".join(relationship.derived_from_predicates),
                    ],
                    then_effects=[
                        f"project relationship {relationship.relationship!r}",
                        f"relationship kind is {relationship.relationship_kind}",
                        f"subject type expectation is {relationship.subject_type}",
                        f"object type expectation is {relationship.object_type}",
                        object_effect,
                    ],
                    metadata={
                        "relationship": relationship.relationship,
                        "relationship_kind": relationship.relationship_kind,
                        "subject_type": relationship.subject_type,
                        "object_type": relationship.object_type,
                        "derived_from_predicates": list(
                            relationship.derived_from_predicates
                        ),
                        "object": relationship.object,
                    },
                )
            )
        return entries

    def _entity_type_entries(self) -> list[RuleInventoryEntry]:
        return [
            RuleInventoryEntry(
                id=f"entity_type.{entry.entity_type}",
                category="entity_type_catalog",
                source=_source("entity_type_catalog/core.json"),
                summary=entry.description or f"Entity type {entry.entity_type}.",
                if_conditions=[f"entity is classified as {entry.entity_type!r}"],
                then_effects=["entity type is available for projection and graph validation"],
                metadata={
                    "entity_type": entry.entity_type,
                    "description": entry.description,
                },
            )
            for entry in self.entity_type_catalog.list_entity_types()
        ]

    def _inference_entries(self) -> list[RuleInventoryEntry]:
        entries: list[RuleInventoryEntry] = []
        for rule in self.inference_catalog.list_rules():
            when_value = "any value" if rule.when_value is None else repr(rule.when_value)
            entries.append(
                RuleInventoryEntry(
                    id=f"inference.{rule.id}",
                    category="inference_catalog",
                    source=_source("inference_catalog/core.json"),
                    summary=rule.name,
                    if_conditions=[
                        f"fact predicate is {rule.when_predicate!r}",
                        f"fact value is {when_value}",
                    ],
                    then_effects=[
                        f"infer predicate {rule.then_predicate!r}",
                        f"infer value {rule.then_value!r}",
                        f"inferred confidence is {rule.confidence}",
                    ],
                    metadata={
                        "rule_id": rule.id,
                        "name": rule.name,
                        "when_predicate": rule.when_predicate,
                        "when_value": rule.when_value,
                        "then_predicate": rule.then_predicate,
                        "then_value": rule.then_value,
                        "confidence": rule.confidence,
                        "reason": rule.reason,
                    },
                )
            )
        return entries

    def _graph_validation_entries(self) -> list[RuleInventoryEntry]:
        source = "seed_runtime/state.py:GraphValidator"
        return [
            RuleInventoryEntry(
                id="graph_validation.skip_identity_relationships",
                category="graph_validation",
                source=source,
                summary="Identity relationships are not type-validated as graph issues.",
                if_conditions=["relationship kind is identity"],
                then_effects=["graph validation skips subject/object type checks for that edge"],
                metadata={"owner": "GraphValidator"},
            ),
            RuleInventoryEntry(
                id="graph_validation.unknown_expected_type",
                category="graph_validation",
                source=source,
                summary="Unknown catalog type expectations produce warnings.",
                if_conditions=["relationship expected type is not present in EntityTypeCatalog"],
                then_effects=["graph validation reports a warning"],
                metadata={"owner": "GraphValidator"},
            ),
            RuleInventoryEntry(
                id="graph_validation.unknown_actual_type",
                category="graph_validation",
                source=source,
                summary="Unknown actual entity types produce warnings when a specific type is expected.",
                if_conditions=["relationship expects a specific entity type", "actual entity type is unknown"],
                then_effects=["graph validation reports a warning"],
                metadata={"owner": "GraphValidator"},
            ),
            RuleInventoryEntry(
                id="graph_validation.ambiguous_actual_type",
                category="graph_validation",
                source=source,
                summary="Ambiguous actual entity types produce warnings unless independent evidence proves a mismatch.",
                if_conditions=["relationship expects a specific entity type", "actual entity type has multiple current values"],
                then_effects=["graph validation reports a warning or an error for independent mismatch evidence"],
                metadata={"owner": "GraphValidator"},
            ),
            RuleInventoryEntry(
                id="graph_validation.type_mismatch",
                category="graph_validation",
                source=source,
                summary="Concrete subject/object type mismatches produce graph errors.",
                if_conditions=["relationship expects a specific entity type", "actual entity type differs from expected type"],
                then_effects=["graph validation reports an error"],
                metadata={"owner": "GraphValidator"},
            ),
        ]

    def _capability_resolution_entries(self) -> list[RuleInventoryEntry]:
        entries = [
            RuleInventoryEntry(
                id="capability_resolution.registered_operation_candidates",
                category="capability_resolution",
                source="seed_runtime/tool_needs.py:ToolNeedService.resolve_capability",
                summary="Matching registered operations are reported as candidates only.",
                if_conditions=["ToolNeed.capability matches a registered ToolSpec capability"],
                then_effects=["registered operation candidate metadata is reported", "no tool is executed"],
                metadata={"executable": False},
            )
        ]
        for entry in self.capability_catalog.list_entries():
            entries.append(
                RuleInventoryEntry(
                    id=f"capability_resolution.{entry.capability}",
                    category="capability_resolution",
                    source=_source("capability_catalog/*.yml"),
                    summary=f"Recommend providers for capability {entry.capability}.",
                    if_conditions=[
                        f"ToolNeed.capability is {entry.capability!r}",
                    ],
                    then_effects=[
                        "provider and handoff recommendations may be reported as metadata",
                        "CapabilityRecommendation.operation remains metadata only",
                        "no provider, host, network, shell, or tool execution occurs",
                    ],
                    metadata={
                        "capability": entry.capability,
                        "recommendation_count": len(entry.recommendations),
                        "providers": [rec.provider for rec in entry.recommendations],
                        "operations": [
                            rec.operation for rec in entry.recommendations if rec.operation
                        ],
                    },
                )
            )
        return entries


def collect_rule_inventory() -> list[RuleInventoryEntry]:
    """Collect Seed's deterministic rule inventory from built-in catalogs."""

    return RuleInventoryBuilder().collect()


def _sort_entries(entries: Iterable[RuleInventoryEntry]) -> list[RuleInventoryEntry]:
    return sorted(entries, key=lambda entry: (entry.category, entry.id))


def _source(path: str) -> str:
    return str(Path(path).as_posix())
