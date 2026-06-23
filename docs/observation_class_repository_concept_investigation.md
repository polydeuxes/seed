# Observation Class Repository Concept Investigation

## Scope

This investigation asks what role observation classes play within current
repository reasoning. It is intentionally not a permission, policy,
inheritance, authorization, approval-propagation, or operator-preference
investigation.

Repository authority wins: conclusions below are limited to implementation and
existing documentation evidence.

## Commands and evidence reviewed

Implementation-backed checks used during this investigation:

```bash
rg -n "observation[_ -]?(domain|class)|Observation Class|neighbor_table_read|active_network_probe|docker_socket_read|diagnostic-inventory|shape-audit" -S .
sed -n '1,260p' seed_runtime/observation_permission.py
sed -n '1,220p' seed_runtime/observation_domains.py
sed -n '1,140p' tests/test_observation_permission.py
rg -n "entity type|relationship catalog|predicate catalog|capability class|classification|GraphIssue|surface classification|operational-surface-classification|classifies|Category|IssueCategory" seed_runtime docs tests -S
sed -n '1,220p' seed_runtime/entity_type_catalog.py
sed -n '1,180p' seed_runtime/relationship_catalog.py
sed -n '1,120p' seed_runtime/predicate_catalog.py
sed -n '1,230p' seed_runtime/operational_surface_inventory.py
sed -n '1,140p' seed_runtime/capability_relationship.py
python -m pytest -q tests/test_observation_permission.py
```

## Observation domains discovered

The current observation-permission implementation has one explicit domain to
class map:

| Observation domain | Observation class | Implementation source |
| --- | --- | --- |
| `neighbor_table_read` | `local_passive` | `SUPPORTED_OBSERVATION_CLASSES` |
| `traffic_capture` | `network_passive` | `SUPPORTED_OBSERVATION_CLASSES` |
| `active_network_probe` | `network_active` | `SUPPORTED_OBSERVATION_CLASSES` |
| `docker_socket_read` | `local_privileged` | `SUPPORTED_OBSERVATION_CLASSES` |
| `external_provider_query` | `external` | `SUPPORTED_OBSERVATION_CLASSES` |

The older observation-domain visibility surface discovers different domain
names from observation inventory, utilization, capability pressure, and
operational-story evidence. Current implementation-backed examples include
`local_listeners`, `container_runtime`, and generated family-derived names such
as `<family>_observations`.

This means there are currently at least two domain vocabularies:

1. **Observation-permission domains**, explicitly enumerated in
   `SUPPORTED_OBSERVATION_CLASSES`.
2. **Observation-domain visibility domains**, derived from observed predicate
   families and capability pressure.

Those two vocabularies are not unified by a shared catalog in current code.

## Observation classes discovered

The implementation defines this closed literal vocabulary for observation
permission entries:

- `local_passive`
- `network_passive`
- `network_active`
- `local_privileged`
- `external`
- `unknown`

Only five non-unknown classes are mapped from known domains today. `unknown` is
used when a requested domain is not recognized by the implementation evidence.

## Relationship between domains and classes

The current relationship is a direct many-domain-to-one-class-capable mapping in
shape, but the populated implementation is currently one domain per non-unknown
class.

Evidence:

- The map type is `dict[str, ObservationClass]`, so the implementation can map
  many domain strings to the same class without structural change.
- The current map contains only one domain for each non-unknown class.
- There is no reverse index, class catalog, class definition object, class
  metadata, class description, class-to-policy rule, class-to-collector rule, or
  class-to-visibility registry.

Therefore, current code supports reusable classes as values, but current data
does not yet prove that multiple domains share a class.

## Evidence supporting class significance

### 1. Classes are part of a typed runtime model

`ObservationClass` is a `Literal`, not an arbitrary display string. It is used
as the type of `ObservationPermissionDomain.observation_class`, serialized in
JSON, and rendered in human-readable CLI output. That makes observation class a
stable field in the observation-permission report shape, not merely incidental
text in a formatter.

### 2. Classes participate in known/unknown recognition

The permission entry builder uses whether the class is `unknown` to distinguish
recognized domains from unrecognized domains. Recognized domains receive
`requires_operator_expression`; unrecognized domains receive `unknown`. The
reasoning text also changes from "observation domain identified" to
"observation domain not recognized by implementation evidence" based on the
class lookup.

This is the strongest implementation evidence that classes do more than label
output: class lookup currently drives recognized-domain reasoning and the
unknown-domain permission state.

### 3. Classes are tested as output and model behavior

Tests assert that `neighbor_table_read` renders `Observation Class:` and
`local_passive`, that `traffic_capture` has class `network_passive`, and that an
unmapped domain has class `unknown` plus unknown reusable permission state.

This makes the field regression-protected as part of the implemented diagnostic
surface.

### 4. Classes are exposed through diagnostic-governed visibility

The observation-permission diagnostic is registered in diagnostic inventory and
shape audit. The tests assert JSON support, no record support, no event-ledger
writes, no cluster mutation, and shape-audit consistency. Because the class
field is part of the diagnostic JSON object, it is visible through a governed
operational surface.

## Evidence against class significance

### 1. No standalone observation-class catalog exists

Unlike entity types, relationships, and predicates, observation classes are not
loaded from a catalog file, represented by definition records, documented with
descriptions in code, or exposed via list/get APIs.

### 2. Classes do not currently drive collection or observation behavior

No evidence was found that `local_passive`, `network_passive`, `network_active`,
`local_privileged`, or `external` select collectors, change source ingestion,
modify observation normalization, alter projection, or determine what facts are
recorded.

### 3. Classes do not currently influence permission beyond knownness

Within the observation-permission builder, all recognized classes currently
receive the same default permission state when no approval is observed:
`requires_operator_expression`. The implementation does not distinguish
`network_active` from `local_passive` for permission behavior. This
investigation does not evaluate whether such behavior should exist; it only
notes that it does not exist today.

### 4. Classes do not appear in the older observation-domain visibility model

`observation_domains.py` has fields named `domain`, `classification`,
`gap_type`, `pressure`, and `evidence`; it does not include `observation_class`.
That surface reasons about observed/partially observed/unobserved domains and
gap types, not the passive/active/privileged/external class vocabulary.

### 5. No implementation-backed relationship preserves class membership

No current relationship catalog entry, predicate mapping, entity type assertion,
graph issue, capability relationship, or operational graph edge was found that
preserves "domain belongs to observation class" as repository knowledge outside
`observation_permission.py`.

## Do classes explain meaningful differences?

Partially, but only as conservative visibility labels today.

The class names encode meaningful distinctions:

- local versus network vantage point;
- passive versus active observation style;
- privileged local access;
- external-provider access;
- unknown/unrecognized domains.

However, current implementation evidence does not show these distinctions being
used to alter collection, projection, policy, authorization, recording, or
cluster mutation behavior. The meaningful difference currently preserved by
code is mostly **recognized class versus unknown class**.

## Do classes participate in reasoning?

Yes, narrowly.

They participate in reasoning inside `build_observation_permission` by deciding
whether a requested domain is recognized. That decision changes permission state,
reusable permission state, future autonomous invocation state, and reasoning
text for unknown domains.

They do not currently participate in broader repository reasoning such as graph
validation, predicate projection, relationship projection, capability pressure,
observation-domain coverage, or operational-surface classification.

## Do classes influence visibility?

Yes.

Observation classes are visible in both human-readable and JSON
observation-permission output. That output is a registered diagnostic surface.
Classes therefore influence what users can see about observation-domain
permission visibility.

No evidence shows that classes influence which visibility surfaces exist or
which observations are collected.

## Do classes appear reusable?

Architecturally, yes; evidentially, not yet proven by multiple populated domains
per class.

The `ObservationClass` literal and `SUPPORTED_OBSERVATION_CLASSES` map make the
classes reusable values. A future domain could be added to `local_passive` or
`network_active` without changing the report shape.

But current repository evidence maps only one explicit domain to each
non-unknown class. Therefore it is supported to say the implementation is
reusable-class-shaped. It is not supported to say current data demonstrates
class reuse across multiple domains.

## Comparison to existing repository classifications

### Entity types

Entity types are first-class repository concepts. They have a catalog with
`EntityTypeDefinition`, are loadable from built-in JSON, require an `unknown`
entry, and are consumed by projection/graph validation and classification
coverage diagnostics.

Observation classes are weaker: they are typed literals and output fields, but
have no definition catalog and no broad projection or validation role.

### Relationship catalogs

Relationships are first-class concepts. `RelationshipDefinition` records contain
relationship kind, subject type, object type, and source predicates. The catalog
builds a predicate-to-relationship index and exposes `get`, `for_predicate`, and
`list_relationships` APIs.

Observation classes do not have comparable definition records or derived-index
behavior. The only current index is direct domain-to-class lookup.

### Predicate catalogs

Predicates are first-class concepts. `PredicateDefinition` includes kind, value
type, cardinality, and allowed values. `PredicateMapping` connects provider
predicates to canonical predicates, and predicate catalog methods influence
currentness, measurement semantics, and mapping behavior.

Observation classes have no equivalent metadata such as vantage point, activity,
privilege requirement, mutability risk, source authority, or allowed domain
members.

### Capability classifications and capability relationships

Capability relationship visibility is read-only and explains current access,
operational benefit, pressure, attainability, expectation, reasoning, and known
limitations. Capability pressure also feeds `observation_domains.py` through
`CAPABILITY_TO_DOMAIN`.

Observation classes resemble capability classifications in being conservative
visibility language, but they are less integrated. They do not currently carry
pressure, benefit, attainability, or expectation fields.

### Graph issue categories

Graph issues are diagnostic outputs over projected relationships and entity
types. They participate in integrity and classification-coverage visibility but
are not truth themselves.

Observation classes are similar in one respect: they are diagnostic visibility,
not cluster truth. They differ because graph issues are produced by validation
over catalog-backed projections, while observation classes are assigned by a
small static map.

### Surface classifications

Operational-surface classification is close in shape. It assigns implementation
surfaces to classes such as primary surface, filter, modifier, debug surface, and
manual input using parser and registry evidence. It exposes counts and itemized
classification output.

Observation classes similarly classify operationally meaningful things, but
there is no dedicated observation-class audit, count view, or consistency check
beyond the observation-permission diagnostic itself.

## Supported conclusions

1. **Observation classes are real implementation-backed fields in the
   observation-permission diagnostic.** They are typed, serialized, rendered,
   and tested.

2. **Observation classes are more than formatter-only labels.** The class lookup
   determines whether a domain is recognized or unknown, and that affects
   permission-state and reasoning output.

3. **Observation classes are not currently first-class repository concepts in
   the same sense as entity types, predicates, or relationships.** They lack a
   catalog, definitions, metadata, projection integration, validation role,
   broad API, and cross-surface preservation.

4. **Observation classes are reusable-class-shaped but not yet reuse-proven.**
   The map can associate many domains with a class, but current populated data
   has one domain per non-unknown class.

5. **The safest current classification is: observation classes are
   implementation-backed reusable visibility classifications, not yet
   first-class repository concepts.**

## Unsupported conclusions

Current evidence does not support claiming that observation classes:

- define permission inheritance;
- define policy inheritance;
- grant or deny authorization by class;
- propagate approval;
- select observation collectors;
- change recording behavior;
- mutate cluster state;
- are preserved as graph relationships;
- are catalog-backed ontology objects;
- are currently reused by multiple domains per class.

## Open questions

1. Should observation classes get a catalog with definitions, descriptions, and
   explicit semantics, or remain local to observation-permission visibility?
2. Should `observation_domains.py` and `observation_permission.py` share a domain
   registry, or are they intentionally separate visibility vocabularies?
3. Should future observation-domain reasoning preserve class membership outside
   a permission-focused diagnostic?
4. If observation classes become first-class, what metadata is necessary:
   vantage point, passive/active mode, privilege boundary, source locality,
   expected mutability, or recordability?
5. Should class membership ever influence runtime behavior, or should it remain
   explanatory visibility only?
6. Should there be tests proving multiple domains can share one class if reuse
   becomes an intended property?

## Acceptance answers

### Are observation classes real repository concepts?

They are real implementation-backed concepts inside the observation-permission
visibility surface. They are not yet first-class repository concepts across the
repository architecture.

### Or are they merely implementation labels?

They are not merely output labels, because unknown versus recognized class
lookup affects report state and reasoning. But most non-unknown class
specificity is currently label-like: `local_passive`, `network_passive`,
`network_active`, `local_privileged`, and `external` do not yet drive distinct
behavior.

### Would future repository reasoning benefit from treating observation classes as first-class objects?

Probably yes, if future work needs to compare observation domains across vantage
point, activity, privilege, externality, collection risk, or diagnostic
visibility boundaries. First-class treatment would make class definitions,
reuse, and consistency auditable instead of embedded in a single map.

However, repository authority does not justify implementing that now. The
current evidence supports a conservative next step only if needed: define an
observation-class catalog or audit when more than one surface needs to reason
about class membership.

### What evidence supports that conclusion?

The supporting evidence is the combination of typed observation-class fields,
static domain-to-class mapping, JSON/rendered/tested diagnostic output,
recognized-vs-unknown reasoning behavior, and the absence of catalog/projection
integration comparable to established first-class concepts.
