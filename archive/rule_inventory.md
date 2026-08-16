# Rule inventory

This document identifies current Seed systems that own deterministic rules or
rule-like catalog metadata. It does not invent new rules and does not define a
new rule engine.

Rule Inventory v1 is implemented as a read-only inventory over current
deterministic catalogs and static rule owners. It emits stable entries from
existing catalogs and rule-owning systems so Seed can answer: "What deterministic
rules does Seed currently know about?"

The v1 implementation lives in `seed_runtime/rule_inventory.py` and is exposed
through `python scripts/seed_local.py --rules` (also available as
`--explain-rules`). The CLI prints JSON by default. Collection loads catalog
metadata only; it does not project state, append ledger events, inspect live
hosts, call providers, execute tools, mutate host state, or introduce
LLM-driven reasoning.

## Inventory format

An inventory entry is deterministic and source-attributed. The v1 shape is:

```yaml
- id: predicate.availability_status
  category: predicate_catalog
  source: predicate_catalog/core.json
  summary: Canonical predicate availability_status.
  if_conditions:
    - fact predicate is 'availability_status'
    - "value is one of: up, down, unknown"
  then_effects:
    - predicate is treated as a measurement
    - value type is enum
    - current fact cardinality is single
  metadata:
    predicate: availability_status
    kind: measurement
```

Each entry identifies a stable id, category, source, summary, conditions,
effects, and metadata.

## PredicateCatalog rules

`PredicateCatalog` owns predicate metadata, including predicate names,
normalization expectations, and cardinality declarations represented in the
checked-in predicate catalog.

Example current rule shape represented by v1 entries:

```text
IF predicate cardinality is single
AND conflicting current values exist
THEN fact conflict is reported, not silently resolved.
```

## RelationshipCatalog rules

`RelationshipCatalog` owns relationship type metadata and relationship-level
validation expectations represented in the checked-in relationship catalog.

The implemented inventory lists each relationship type from the catalog with
its source metadata and validation-relevant subject/object type expectations.

## EntityTypeCatalog rules

`EntityTypeCatalog` owns entity type classification metadata represented in the
checked-in entity type catalog.

The implemented inventory lists classification metadata and the catalog source
for each entity type rule-like entry.

## InferenceCatalog rules

`InferenceCatalog` owns explicit inference metadata represented in the checked-in
inference catalog.

The implemented inventory lists inference rules exactly as represented by the
catalog and does not add inferred behavior that the catalog does not declare.

## Graph validation rules

Graph validation rules are owned by the graph validation system. The implemented
inventory lists the static validation checks that can report graph issues,
including deterministic type-warning and type-error conditions.

## Capability resolution rules

Capability resolution is read-only. The implemented inventory records the simple
static rules for reporting matching registered operation candidates and
capability catalog provider/handoff recommendations, but it does not execute,
authorize, mutate hosts, register tools, or turn catalog metadata into callable
operations.

Example current rule shapes:

```text
IF observation is accepted
THEN evidence is recorded.

IF evidence supports predicate/value
THEN fact is projected.

IF ToolNeed.capability matches ToolSpec.capabilities
THEN registered operation candidate is reported.

IF ToolNeed.capability matches CapabilityCatalogEntry.capability
THEN provider recommendations may be reported.
```

## Non-goals

- Do not build a new rule engine; v1 is inventory-only.
- Do not invent rules absent from current code or catalogs.
- Do not add planning orchestration or workflow execution.
- Do not add LLM-driven projection logic.
