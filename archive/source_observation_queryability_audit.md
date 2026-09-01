# Source Observation Queryability Audit

## Purpose

This audit examines whether Seed's current source-observation facts are usable as
an implementation navigation surface.

It is a documentation-only implementation audit.

It does not change code, schemas, projections, observations, facts, tests,
runtime behavior, source observation behavior, CLI behavior, or storage.

## Trigger

Recent repository self-observation expanded beyond import relationships to include
source definitions and entrypoints. The current architecture expects different
source relationships to answer different navigation questions:

```text
imports
    reveal dependency knowledge

defines
    reveals ownership knowledge

entrypoints
    reveal reachability knowledge

calls / registrations / reads / writes / emits
    reveal behavior knowledge
```

However, interactive operator checks showed that source observations are now
preserved but not yet easy to query for navigation.

Example commands and observations:

```text
seed --current-facts | grep -Ei "defines|entrypoint|imports|state-summary|impact|prometheus|observation|projection" | head -200
```

returned mostly import facts, making definitions and entrypoints difficult to
see near the top of the default fact stream.

```text
seed --current-facts | grep -F "state_summary_views defines"
```

confirmed definition facts exist, but each visible definition appeared duplicated
in rendered output.

```text
seed --why-fact seed_runtime/state_summary_views.py defines state_summary
```

returned no matching fact, despite visible facts such as:

```text
seed_runtime.state_summary_views defines seed_runtime.state_summary_views._entity_summary_row (path=seed_runtime/state_summary_views.py)
```

This shows that preservation exists, but operator lookup remains brittle.

## Central Finding

Source observations are being preserved, but the current operator-facing query
surfaces do not yet provide reliable implementation navigation.

The strongest boundary finding is:

```text
source observation preservation
        !=
source observation queryability
        !=
implementation navigation
```

Definitions and entrypoints may exist in projected state, but if an operator must
know the exact normalized subject/object shape before asking `--why-fact`, then
Seed has not yet made the source-observation layer sufficiently navigable.

## Evidence

### Definitions Exist

The operator observed definition facts such as:

```text
seed_runtime.state_summary_views defines seed_runtime.state_summary_views._canonical_entity_types
seed_runtime.state_summary_views defines seed_runtime.state_summary_views._classify_state_summary_entity
seed_runtime.state_summary_views defines seed_runtime.state_summary_views._entity_summary_row
seed_runtime.observation_sources defines seed_runtime.observation_sources.PrometheusObservationSource
```

This demonstrates that `defines` facts exist in current state.

### Evidence Links Exist

The operator ran:

```text
seed --unsupported-facts
```

and received:

```text
Unsupported Facts

(none)
```

This suggests the observed source facts are not unsupported. The problem is not
missing evidence support.

### Exact Fact Lookup Is Brittle

The operator attempted path-like and short-symbol fact explanation queries:

```text
seed --why-fact seed_runtime/state_summary_views.py defines state_summary
seed --why-fact scripts/seed_local.py defines main
```

Both returned no matching fact.

Visible facts use module-qualified subjects and fully qualified symbol objects,
not file-path subjects or short-symbol objects.

That mismatch means an operator can see that facts exist but cannot easily ask
for their evidence unless they already know the normalized fact shape.

### Rendered Facts Appear Duplicated

The operator-visible `--current-facts` output showed repeated adjacent facts, for
example each `defines` fact appeared twice in the sampled output.

This audit does not determine whether duplication is caused by duplicated state,
duplicate observation ingestion, alias/canonical rendering, or output formatting.
It records that duplication currently degrades navigability.

## Boundary Analysis

### Preservation Is Working

The system appears to preserve source definition observations and evidence.
This satisfies part of the source-observation goal.

### Queryability Is Weak

The operator-facing query surface currently requires exact normalized fact
shapes. The following equivalent human questions are not equivalent to the
current CLI:

```text
Where is state_summary defined?
What defines state_summary?
Why does Seed say state_summary_views defines state_summary?
Where is --state-build declared?
```

The operator must instead discover exact canonical values by grepping raw facts.

### Navigation Is Not Yet Achieved

Implementation navigation requires answering questions like:

```text
Where is this behavior owned?
Where is this behavior entered?
Which symbol should I inspect next?
Which source file owns the relevant definition?
```

The current source facts are closer to preserved observations than navigable
answers.

## Suspected Failure Modes

1. **Path versus module mismatch**

   Operators naturally ask with repository paths:

   ```text
   seed_runtime/state_summary_views.py
   ```

   but facts use module subjects:

   ```text
   seed_runtime.state_summary_views
   ```

2. **Short symbol versus fully qualified symbol mismatch**

   Operators naturally ask for:

   ```text
   state_summary
   main
   --state-build
   ```

   but facts may use fully qualified objects or entrypoint-specific normalized
   names.

3. **Raw fact stream flood**

   `--current-facts` mixes imports, definitions, entrypoints, runtime facts,
   host facts, repository facts, and other claims. Imports can dominate early
   output and obscure definitions or entrypoints.

4. **Duplicate rendered facts**

   Repeated adjacent facts reduce trust in the source-observation surface and
   make manual grep output harder to interpret.

5. **Definition existence without navigation projection**

   A definition fact answers ownership only if the operator can find it.
   Preservation alone does not provide a source map.

## What Is Correct

- Source definition facts should remain preserved.
- Entrypoint facts should remain preserved.
- Import facts should remain preserved.
- Evidence links should remain preserved.
- Exact fact explanation should remain possible.
- Source observations should remain read-only observations and must not imply
  runtime execution, capability authority, or behavioral reachability beyond the
  relationship they actually support.

## What Is Missing Or Suspect

- A source-focused query or projection surface for implementation navigation.
- Alias or normalization support for path-like versus module-like source
  subjects.
- Query support for short symbols resolving to fully qualified symbols.
- A dedicated entrypoint lookup by command/flag name.
- A duplicate diagnosis for repeated rendered `defines` and `imports` facts.
- A way to ask "where is this behavior?" without manually grepping all facts.

## Candidate Next Work

This audit does not implement changes, but it suggests several bounded follow-up
options.

### 1. Source Observation Query Surface

Add or design a read-only source navigation surface that can answer:

```text
seed --source-definitions state_summary
seed --source-entrypoints state-summary
seed --source-symbol state_summary
seed --source-file seed_runtime/state_summary_views.py
```

The exact CLI names are not prescribed by this audit.

The architectural requirement is that source facts become queryable by operator
terms, not only exact normalized fact triples.

### 2. Source Map Projection

Create a read-only projection over source observations that groups:

```text
file
    defines symbols
    declares entrypoints
    imports modules
```

This would make implementation navigation possible without changing preserved
facts.

### 3. Normalization/Alias Investigation

Audit whether source path subjects and module subjects should be linked by an
explicit source-identity relationship, or merely handled as query aliases.

This should not be implemented casually because path, module, package, script,
and importable name are related but not identical.

### 4. Duplicate Fact Diagnosis

Determine whether adjacent duplicate source facts are caused by:

```text
duplicate observations
duplicate fact promotion
duplicate rendering
canonical/alias expansion
multiple observation runs without dedupe
```

Do not delete preserved facts before understanding which layer owns the
repetition.

## Non-Goals

This audit does not recommend:

- deleting duplicate facts;
- changing fact identity semantics;
- changing source observation ingestion;
- collapsing path identity into module identity;
- making definitions imply reachability;
- making entrypoints imply capability authority;
- building a full call graph;
- building a universal code browser;
- adding runtime or ToolExecutor integration;
- treating source observation as proof of behavior correctness.

## Files And Surfaces Considered

- `docs/source_definitions_and_entrypoint_observation_reconciliation.md`
- `docs/architectural_status_and_next_frontier.md`
- live operator output from `seed --current-facts`
- live operator output from `seed --why-fact`
- live operator output from `seed --unsupported-facts`

## Invariants

```text
Source observation preservation is not source queryability.
```

```text
Source queryability is not implementation navigation by itself.
```

```text
Definitions reveal ownership only when the definition can be found.
```

```text
Entrypoints reveal reachability only when the entrypoint can be found by the
terms an operator has.
```

```text
Path identity, module identity, symbol identity, and entrypoint identity are
related but not interchangeable.
```

```text
Duplicate-looking source facts should be diagnosed before deletion or collapse.
```

## Conclusion

The source-observation layer has advanced beyond imports: definitions and likely
entrypoints are present and evidence-backed. The next problem is not whether Seed
can preserve source observations. The next problem is whether those observations
are queryable enough to support implementation navigation.

The immediate next audit or implementation task should focus on source
observation queryability and duplicate diagnosis before adding broader behavior
relationships such as call edges, reads, writes, emits, or promotes.
