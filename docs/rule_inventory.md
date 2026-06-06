# Rule inventory

This document identifies current Seed systems that own deterministic rules or
rule-like catalog metadata. It does not invent new rules and does not define a
new rule engine.

A future read-only rule inventory should emit stable entries from existing
catalogs and rule-owning systems so Seed can answer: "What deterministic rules
does Seed apply?"

## Expected future inventory format

A future inventory entry should be deterministic and source-attributed. A minimal
shape could be:

```yaml
- id: predicate.single_cardinality_conflict
  owner: PredicateCatalog / StateProjector
  source: predicate_catalog/core.json
  kind: predicate_rule
  if:
    - predicate cardinality is single
    - conflicting current values exist
  then:
    - fact conflict is reported
    - conflicting current values are not silently resolved
```

The exact schema can change, but each entry should identify the owner, source,
rule category, condition, and result.

## PredicateCatalog rules

`PredicateCatalog` owns predicate metadata, including predicate names,
normalization expectations, and cardinality declarations represented in the
checked-in predicate catalog.

Example current rule shape:

```text
IF predicate cardinality is single
AND conflicting current values exist
THEN fact conflict is reported, not silently resolved.
```

## RelationshipCatalog rules

`RelationshipCatalog` owns relationship type metadata and relationship-level
validation expectations represented in the checked-in relationship catalog.

A future inventory should list each relationship type from the catalog with its
source metadata and validation-relevant constraints.

## EntityTypeCatalog rules

`EntityTypeCatalog` owns entity type classification metadata represented in the
checked-in entity type catalog.

A future inventory should list classification rules and the catalog source for
each entity type rule.

## InferenceCatalog rules

`InferenceCatalog` owns explicit inference metadata represented in the checked-in
inference catalog.

A future inventory should list inference rules exactly as represented by the
catalog and should not add inferred behavior that the catalog does not declare.

## Graph validation rules

Graph validation rules are owned by the graph validation system. A future
inventory should list validation checks that can report graph issues, including
the deterministic condition that produces each issue.

## Capability resolution rules

Capability resolution is read-only. It can report matching registered operation
candidates and provider/handoff recommendations, but it does not execute,
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

- Do not build a new rule engine yet.
- Do not invent rules absent from current code or catalogs.
- Do not add planning orchestration or workflow execution.
- Do not add LLM-driven projection logic.
