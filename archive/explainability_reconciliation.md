# Executive Summary

Explainability Reconciliation finds that Seed already has a broad, read-only
explainability foundation. The prior explainability architecture audit,
inventory audit, and contract characterization all converged on the same core
finding: Seed's explanation-producing surfaces already expose most of the data
needed to answer operator-facing explanation questions, but that data is split
across facts, support, evidence, contradictions, capability verification, rule
inventory, temporal metadata, stale-fact views, graph issues, and current-state
views.

The correct reconciliation status is therefore **partially implemented**, not
missing. Fact-level explanations, evidence explanations, support explanations,
contradiction explanations, capability explanations, rule explanations,
temporal/stale explanations, graph issue explanations, and current-state
explanations all have existing building blocks. The missing piece is not a new
reasoning system. It is a small documentation/schema/vocabulary layer that names
how existing fields line up when a caller wants a common explanation shape.

A unified explanation contract is **partially implemented as data and vocabulary**
and **missing as a stable contract document/schema**. It should primarily be a
read-only **vocabulary and schema** over existing projection-backed,
evidence-backed, and inventory-backed surfaces. It should not be a Runtime
feature, ToolExecutor feature, projection feature, explanation engine, reasoning
engine, provider-calling path, or LLM-generated explanation system.

Smallest safe next step: document an **Explanation Contract Vocabulary v1** that
maps existing surfaces into common fields (`subject`, `claim`, `status`,
`supporting_facts`, `supporting_evidence`, `competing_facts`, `conflicts`,
`rules`, `temporal_metadata`, `provenance`, `notes`, and optional `extensions`)
without adding behavior. Characterization tests may follow later, but this
reconciliation intentionally does not implement them.

# Audit Convergence

## Consistent conclusions

The three audits remained consistent on the most important architectural points:

- Explainability already exists implicitly through deterministic read models, not
  through a separate explanation engine.
- `ExplanationBuilder` is the clearest explicit explanation surface for current
  fact/belief explanations.
- `FactSupport` is the central support-level explanation primitive.
- `Evidence` and the Evidence Graph provide provenance and evidence joins.
- `FactConflict`, contradiction reporting, and graph validation issues already
  expose conflict/issue facts, reasons, and supporting identifiers.
- Capability explanation must remain separate from capability execution and must
  use `capability_verified` facts/support/evidence for verification claims.
- Rule explanation should reuse the Rule Inventory and catalog metadata; it must
  not introduce a rule engine.
- Temporal and stale explanation already has expiry, observation time, current
  sample, stale fact, and refresh recommendation data, but not a single stale
  rationale object.
- Explainability must be read-only and derived from projected state, evidence,
  inventories, and static catalogs.
- LLM-generated explanations, runtime orchestration, execution behavior,
  projection mutation, and truth arbitration are non-goals.

## Findings that changed

The wording shifted across the audit sequence:

- The architecture audit emphasized that Seed had an **implicit and unevenly
  surfaced explainability stack**. It focused on concrete current capabilities
  and noted gaps such as why-stale, why-current, selection rationale, why-not
  verified, and exact rule attribution.
- The inventory audit reframed the same landscape as **many explanation-producing
  surfaces** and found that a common contract was feasible as an inventory/schema
  exercise rather than an engine.
- The contract characterization went further and showed that fact, contradiction,
  capability, rule, temporal, stale, graph, and state-view outputs can fit a
  shared field set, provided surface-specific fields remain in `extensions`.

The main change was not the discovery of a new subsystem. It was a stronger
recognition that the common shape already exists in pieces and should be named
rather than built as behavior.

## Findings that converged

The audits converged on these reconciliation findings:

| Area | Converged finding |
| --- | --- |
| Fact explanation | Implemented for subject/predicate current beliefs; partial for arbitrary fact ID, stale, and selection rationale. |
| Evidence explanation | Implemented as Evidence Graph / fact evidence views; partial when joined with current belief/support semantics. |
| Support explanation | Implemented as `FactSupport`; partial as operator-facing rationale prose/schema. |
| Contradiction explanation | Implemented/partial through `FactConflict`, contradiction reporting, and graph issues; no automatic truth resolution should be added. |
| Capability explanation | Implemented/partial through Capability Verification Inventory; capability why-not remains partial. |
| Rule explanation | Implemented as Rule Inventory; missing exact rule-to-projection attribution for every output. |
| Temporal/stale explanation | Partial: expiry/current-sample/observation data exists, but rationale vocabulary is incomplete. |
| Unified contract | Partial as fields/data; missing as a small vocabulary/schema document. |

# Existing Explainability Capabilities

| Capability | Status | Reconciliation |
| --- | --- | --- |
| Fact explanation | Already implemented, with partial gaps | `ExplanationBuilder.why(subject, predicate)` exposes current/ambiguous/no-current status, current and competing beliefs, support confidence, evidence IDs, source types, observation times, recursive source facts, inference rule IDs, confidence cap visibility, and entity resolution. It does not explain arbitrary fact IDs, stale/replacement rationale, or full support-selection rationale in a dedicated object. |
| Evidence explanation | Already implemented, with partial gaps | Evidence Graph exposes evidence nodes, links, fact evidence views, supporting event IDs, evidence summaries, and unsupported fact views. It is partial only because it is not merged into every fact/current-belief explanation object. |
| Support explanation | Already implemented, with partial gaps | `FactSupport` exposes subject, predicate, value, dimensions, supporting fact IDs, source types, confidence, observed/latest times, expiry, predicate semantics, and support kind. It is not a prose explanation and does not inline competing support or rule attribution. |
| Contradiction explanation | Partially implemented | `FactConflict` explains single-cardinality disagreements with values, winning value/best fact when available, conflicting facts, and reason. `Contradiction` adds severity, evidence by fact, and supporting event IDs for conservative exclusive-predicate conflicts. Graph issues add relationship/type issue explanations. The surfaces are not unified and do not arbitrate truth. |
| Capability explanation | Partially implemented | Capability Verification Inventory explains `verified`, `provider_reported`, `stale`, `unverified`, and `unknown` states from `capability_verified` facts/support/evidence and inventory universe membership. It does not execute verifiers or prove absence beyond projected verification facts. |
| Rule explanation | Partially implemented | Rule Inventory exposes deterministic catalog/static rule metadata with source, summary, conditions, effects, and metadata. Exact attribution from every projected output back to a rule inventory entry is not consistently represented. |
| Temporal explanation | Partially implemented | Observation times, latest observation times, expiry, age, measurement current samples, projection version, and event IDs exist. Missing pieces are as-of/timeline answers and explicit replacement/selection/staleness rationale. |
| Stale explanation | Partially implemented | Stale fact reporting and stale refresh recommendations expose expired facts, `expires_at`, and deterministic refresh capability reasons. A single stale explanation contract is missing. |
| Graph issue explanation | Already implemented, with partial gaps | `GraphValidationIssue` exposes severity, subject, relationship, object, relationship IDs, source fact IDs, reason, hint, and expected/actual subject/object types. It is partial only in the sense that it is not normalized into the common explanation fields. |
| Current-state explanation | Already implemented, with partial gaps | State views expose current facts, observations, requirements, capabilities, issues, summaries, supporting event IDs, projection version, and last event ID. They explain what is current but not always why the current selection won unless callers join `FactSupport`/`ExplanationBuilder`. |

# Unified Explanation Contract Status

A unified explanation contract is **partially implemented**.

It is already implemented in substance because current surfaces repeatedly expose
these common fields:

- `subject`
- `claim`
- `status`
- `supporting_facts`
- `supporting_evidence`
- `competing_facts`
- `conflicts`
- `rules`
- `temporal_metadata`
- `provenance`
- `notes`

It is missing as a stable, named contract because no single document or schema
currently tells callers how to map each existing surface into those fields, which
statuses are allowed for each explanation family, or which surface-specific data
belongs in `extensions`.

The unified explanation contract should primarily be:

1. **Vocabulary**: define shared meanings for status terms such as `current`,
   `ambiguous`, `no_current_belief`, `unsupported`, `expired`, `stale`,
   `verified`, `provider_reported`, `unverified`, `conflicted`, and graph issue
   severities.
2. **Schema**: define a read-only common shape that references existing facts,
   evidence, conflicts, rules, temporal metadata, and provenance without
   changing their owners.
3. **Not an adapter yet**: an adapter may be a future smallest implementation if
   callers need one, but the immediate missing item is smaller: document the
   vocabulary/schema mapping first.
4. **Not a runtime feature**: Runtime should not generate, route, or own
   explanations.
5. **Not a projection feature**: projection already produces the state that
   explanations read. Projection semantics should not change to satisfy the
   contract.

# Missing Concepts

| Concept | Status | Reconciliation |
| --- | --- | --- |
| Why-not explanation | Missing / partially represented | `ExplanationBuilder` has `no_current_belief`, unsupported facts exist, and capability inventory reports missing verification facts, but there is no general why-not explanation contract. |
| Selection rationale | Partially implemented | Current selection rules exist in `State` support selection and representative fact selection, and `FactConflict` can record winners. There is no dedicated rationale object that explains confidence/count/time/tie behavior. |
| Replacement rationale | Missing / partially represented | Measurement current-sample behavior and stale filtering exist, but Seed does not expose why an older sample was replaced or pruned as a named explanation. |
| Stale rationale | Partially implemented | Expiry and stale refresh recommendation reasons exist. A unified stale rationale object with current time vs. `expires_at` and stale/non-current distinctions is missing. |
| Capability why-not | Partially implemented | Inventory can say no `capability_verified` fact is present or a value maps to `unverified`, but it cannot prove absence, inspect providers, execute checks, or explain missing evidence beyond projected state. |
| Contradiction rationale | Partially implemented | `FactConflict.reason`, `Contradiction.reason`, severity, competing values, fact IDs, and graph issue reasons exist. The rationale is not unified across conflict surfaces and does not include automatic resolution. |
| Rule attribution | Partially implemented | Inferred facts can carry `inference_rule_id`, and Rule Inventory exists. Most current-state/projection outputs do not carry a direct Rule Inventory entry reference. |
| Evidence provenance | Already implemented | `Evidence`, Evidence Graph nodes, fact evidence views, supporting event IDs, fact evidence IDs, source types, observed times, source run IDs, and payloads exist. |
| Explanation inventory | Partially implemented | The inventory audit listed explanation-producing surfaces. A durable inventory/status table can be kept as documentation; no new runtime inventory is needed. |

# Reuse Analysis

## What should be reused

- **FactSupport** should remain the canonical support-level object for supported
  subject/predicate/value claims, including confidence, source types, observation
  times, expiry, predicate semantics, and support kind.
- **Evidence** should remain the canonical provenance payload model.
- **Evidence Graph** should remain the read-only join surface for evidence nodes,
  links, fact evidence views, summaries, and unsupported facts.
- **FactConflict** should remain the projected current-support conflict object
  for single-cardinality durable disagreements.
- **Contradictions** should remain the standalone conservative read-only detector
  for exact-subject exclusive-predicate conflicts and evidence-by-side views.
- **Capability Inventory** should remain the read-only capability verification
  explanation surface for `capability_verified` facts/support/evidence.
- **Rule Inventory** should remain the read-only inventory for deterministic
  rule/catalog metadata.
- **Temporal metadata** on facts/support/evidence/state summaries should be
  reused for observation, age, expiry, current sample, stale, and projection
  context.
- **ExplanationBuilder** should remain the explicit fact/belief explanation
  builder for subject/predicate why queries.
- **State Views** should remain the lightweight current-state/summary views for
  facts, observations, requirements, capabilities, issues, last event ID, and
  projection version.

## What should never be duplicated

- Do not duplicate fact truth or support aggregation outside `FactSupport` and
  `State` current-support semantics.
- Do not duplicate evidence storage outside `Evidence` and Evidence Graph.
- Do not duplicate contradiction/conflict classification in a new explanation
  subsystem.
- Do not duplicate capability verification state outside the Capability
  Verification Inventory and future scoped verification read models, if any.
- Do not duplicate deterministic catalog/rule metadata outside Rule Inventory and
  the owning catalogs.
- Do not duplicate temporal truth in an explanation layer.
- Do not create parallel current-state models, parallel truth systems, or a
  separate explanation persistence store.

# Architectural Boundaries

Explainability should remain:

- **Read-only**: explanations interpret existing projected state, evidence,
  inventories, and catalogs.
- **Projection-backed**: current belief/status answers should come from projected
  `State`, `FactSupport`, conflicts, graph issues, and state views.
- **Evidence-backed**: support and provenance should reuse `Evidence` and the
  Evidence Graph.
- **Inventory-backed**: rule and capability explanations should reuse Rule
  Inventory and Capability Verification Inventory.

Explainability should **not** own:

| Responsibility | Should explainability own it? | Answer |
| --- | --- | --- |
| Truth selection | No | `State`/support projection already owns current support selection; explanations may report it but must not select differently. |
| Verification | No | Capability verification is fact/evidence/read-model territory; explanations must not verify by themselves. |
| Execution | No | ToolExecutor owns registered-operation execution. Explainability must not execute tools. |
| Runtime decisions | No | Runtime remains canonical for runtime behavior. Explainability must not become a runtime decision path. |
| Provider calls | No | Provider/catalog recommendations are metadata unless executed elsewhere under the proper boundaries. Explanations must not call providers. |
| LLM reasoning | No | Explanations should be deterministic and state-derived, not generated as a reasoning authority by an LLM. |

# Complexity Traps

The following architecture risks should be avoided:

- **ExplanationEngine**: would likely duplicate `ExplanationBuilder`, Evidence
  Graph, FactSupport, contradiction reporting, and inventories.
- **ReasoningEngine**: would blur the accepted boundary between read-only
  explanation and behavior-changing reasoning/orchestration.
- **WhySubsystem**: would create a parallel owner for support, evidence,
  contradiction, rule, capability, and temporal concepts that already have owners.
- **LLM explanation generation**: risks hallucinated provenance, unverifiable
  rationales, and a second source of truth for why Seed believes something.
- **Duplicate explanation models**: new models that restate facts, evidence,
  conflicts, rules, and temporal metadata would drift from canonical owners.
- **Parallel truth systems**: any explanation path that selects winners,
  suppresses conflicts, or verifies capabilities differently from `State` and
  inventories would undermine projection semantics.
- **Runtime explanation paths**: explanations should not require Runtime calls or
  introduce new Runtime behavior.
- **Projection mutation**: explanations must not append events, change projected
  facts, update support, alter conflicts, or rewrite state views.
- **ToolExecutor explanation hooks**: ToolExecutor should not be instrumented to
  produce explanation truth; execution results may become evidence through
  existing projection paths.
- **Provider-backed why-not checks**: a why-not answer must not silently become a
  network/provider availability check.
- **Rule-engine backfill**: Rule Inventory describes existing deterministic
  metadata; it must not become an executable rule engine.

# Recommended Smallest Next Step

The smallest safe next step is **documentation only**:

1. Create an **Explanation Contract Vocabulary v1** document.
2. Define the common fields and allowed status vocabulary by explanation family.
3. Map each existing surface to those fields:
   - `ExplanationBuilder` / `Explanation`
   - `FactSupport`
   - `Evidence` / Evidence Graph
   - `FactConflict`
   - `Contradiction`
   - `CapabilityInventoryEntry`
   - `RuleInventoryEntry`
   - stale fact reporting / refresh recommendations
   - `GraphValidationIssue`
   - State Views
4. Explicitly require surface-specific details to remain in `extensions` rather
   than being flattened or duplicated.
5. Re-state non-goals: no explanation engine, no reasoning engine, no Runtime or
   ToolExecutor changes, no projection changes, no execution behavior, no
   orchestration, and no LLM-generated explanations.

Characterization tests that assert the vocabulary mapping can be a later step,
but they should still avoid behavior changes.

# Updated Roadmap Status

Explainability is **functionally near-complete as a foundation**, but **not
complete as a contract**.

Updated status:

- **Foundation status**: mostly implemented through existing read-only surfaces.
- **Contract status**: partially implemented; missing a stable vocabulary/schema
  document.
- **Behavior status**: no new behavior recommended.
- **Architecture status**: keep explainability read-only, projection-backed,
  evidence-backed, and inventory-backed.
- **Roadmap recommendation**: add a documentation-only Explanation Contract
  Vocabulary v1 as the smallest remaining item. Do not prioritize engines,
  adapters, runtime paths, projection changes, ToolExecutor behavior, execution
  behavior, orchestration, provider calls, or LLM explanations.
