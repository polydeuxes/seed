# Implementation Promotion Grammar Recovery Investigation

## Scope and method

This is a recovery report only. It does not propose a knowledge framework, ontology, promotion engine, learning engine, runtime redesign, or new grammar. It asks whether the repository already demonstrates recurring promotion boundaries in implementation.

Commands used:

```bash
rg -n "class ObservationIngestor|def ingest|Fact|CapabilityCandidate|VerificationEvidence|register|project|candidate|promot" seed_runtime tests docs/*.md *investigation.md
sed -n '1,240p' seed_runtime/observations.py
sed -n '1,240p' seed_runtime/facts.py
sed -n '1,220p' seed_runtime/capability_candidates.py
sed -n '1,220p' seed_runtime/capability_verification.py
sed -n '1,260p' seed_runtime/capability_inventory.py
sed -n '1,220p' seed_runtime/registry.py
sed -n '715,985p' seed_runtime/state.py
sed -n '1275,1365p' seed_runtime/state.py
sed -n '1819,1858p' seed_runtime/state.py
sed -n '1,180p' seed_runtime/explanations.py
sed -n '1,220p' seed_runtime/knowledge/relationship_observation.py
sed -n '1,180p' seed_runtime/diagnostic_inventory.py
sed -n '1,160p' seed_runtime/diagnostic_shape_audit.py
sed -n '1,140p' operation_capability_observation_recovery_investigation.md
sed -n '1,120p' docs/implementation_relationship_grammar_investigation.md
sed -n '1,110p' docs/implementation_artifact_explanation_grammar_investigation.md
sed -n '1,100p' docs/documentation_structure_phase_3_investigation.md
```

Implementation evidence always overrides terminology in this report.

## Executive answer

Yes, the repository already possesses a recurring promotion grammar, but it is not implemented as one universal `PromotionGrammar` object or one linear lifecycle. The implementation-backed recurrence is distributed across observation ingestion, fact projection, capability inspection, registered operation execution, relationship projection, explanation rendering, diagnostic registries, and documentation-structure observation.

The strongest recurring pattern is:

```text
bounded observation / declaration / event
  -> provenance or support preservation
  -> candidate or derived projection
  -> validation / registry / catalog / support check
  -> durable projected belief, registered operation, or bounded rendered surface
```

The equally important counter-pattern is:

```text
observation / candidate / recommendation / projection / diagnostic output
  -> intentionally not promoted when ownership or evidence is insufficient
```

So the repository does not demonstrate a single runtime learning pipeline. It demonstrates several independent promotion grammars that share boundaries: observation is weaker than fact support; candidate is weaker than verification; recommendation is weaker than registered operation; projection is weaker than event history; presentation vocabulary is weaker than reachable knowledge; diagnostic recording is weaker than cluster mutation.

## Promotion stages already present

| Stage | Accepted? | Implementation evidence | Boundary |
| --- | --- | --- | --- |
| `observed` | Accepted. | `ObservationIngestor` emits `observation.observed` and `evidence.observed` events before any optional fact event. `StateProjector.apply()` stores observations and evidence separately from facts. | Observation is source/provenance input, not automatically all durable knowledge in every case. |
| `evidence` / `support` | Accepted. | `observation_to_evidence()` preserves source, subject, predicate, value, dimensions, expiry, and confidence. `FactSupport` aggregates or selects current support depending on predicate semantics. | Evidence supports claims; it is not itself registration, execution permission, or selected truth. |
| `fact` / `observed fact` | Accepted with boundaries. | `observation_to_fact()` converts an observation and evidence into a `Fact`; `_should_suppress_fact_promotion()` proves at least one implementation-backed observation may remain unpromoted. | A fact requires an ingestion owner and can be suppressed for specific source/predicate boundaries. |
| `inferred` / `derived` | Accepted. | `StateProjector.finalize()` projects inferred facts, fact supports, relationships, entity types, graph issues, aliases, and conflicts after replaying events. | Derived projection is rebuilt from event history and catalogs; it does not rewrite event authority. |
| `candidate` | Accepted. | `CapabilityCandidate` is built from `package_installed` facts and carries explicit notes that it is not proof, selection, policy, or execution authority. | Candidate preservation is intentionally weaker than verified capability or operation authority. |
| `verification evidence` | Accepted. | Capability verification inspection joins candidates to capability inventory; missing `capability_verified` facts leave a candidate unverified. | Verification status is separate from candidate evidence and remains read-only. |
| `verified` | Accepted only where projected verification facts exist. | `build_capability_inventory()` derives states from projected `capability_verified` `FactSupport`, with stale/unverified handling. | Verification is a projected read-model state, not operation selection or permission. |
| `registered` | Accepted. | `ToolRegistry` owns registered operation catalog behavior and only lists model-visible tools when status is `registered` and visibility is `model_visible`. | Registration is manifest/catalog ownership, not inferred from package or binary observation. |
| `projected` | Accepted. | `StateProjector.project()` replays ledger events and `finalize()` rebuilds derived indexes. | Projection is inspectable state built from ledger authority, not independent truth creation. |
| `promoted` | Accepted as a recurring interpretation, not a single API. | Observation-to-fact, fact-to-support, fact-to-relationship, candidate-to-verification-inspection, manifest-to-registered-operation, diagnostic-spec-to-audited-surface all show promotion-like transitions. | The term is not uniformly implemented; each family owns its own transition. |

## Promotion ownership by implementation family

| Family | Promotion owner | Promoted output | Evidence required | Explicit non-promotion boundary |
| --- | --- | --- | --- | --- |
| Observation to fact | `ObservationIngestor` | `Fact` event with evidence IDs | `Observation` plus generated `Evidence` | Prometheus `node_uname_info` `os` observations can suppress fact promotion. |
| Event history to projected state | `StateProjector` | `State`, fact supports, relationships, aliases, conflicts, graph issues | Append-only events plus catalogs and inference rules | Projection diagnostics are non-authoritative; projected state is rebuilt, not ledger authority. |
| Fact support / current belief | `State` support helpers and `_project_fact_supports()` | `FactSupport`, current sample or aggregate support | Non-expired facts, predicate semantics, source confidence | Measurements keep current sample semantics instead of durable aggregation. |
| Capability candidate recovery | `build_capability_candidates()` | `CapabilityCandidateInspection` | Projected `package_installed` facts | Candidate notes reject proof, permission, policy evaluation, selection, and execution. |
| Capability verification | `build_capability_inventory()` and `build_capability_verification_inspection()` | `CapabilityInventoryEntry` / `CapabilityVerification` | Projected `capability_verified` facts and support | Candidate evidence without verification fact remains unverified. |
| Registered operation | `ToolRegistry` and manifest loader | `ToolSpec` registered operation | Toolkit manifest fields, normalized capabilities, status, visibility | Provider recommendations and capability candidates are not registered operations. |
| Runtime execution | `Runtime` routes; `ToolExecutor` owns registered-operation execution | Tool call result and ledger events | Validated model decision, registered `ToolSpec`, policy validation | `request_tool` creates/resolves a need; it does not execute or register. |
| Relationship projection | Relationship observation adapter and `StateProjector` catalog projection | `RelationshipFact` / `EntityRelationship` | Static syntax or explicit document metadata; catalog mapping from facts | Import/definition relationships do not prove behavior, calls, ownership, or reachability. |
| Explanation fields | `ExplanationBuilder` | Current/ambiguous/no-current-belief explanation | Projected `FactSupport`, facts, evidence IDs, conflicts | Explanation renders projected support; it does not create facts or resolve missing belief. |
| Diagnostic surfaces | `DIAGNOSTIC_INVENTORY` and `diagnostic_shape_audit` | Visible/auditable diagnostic surface | Registry row plus implementation spec checks | Recordable diagnostics use `record_scope=diagnostic_run` and `mutates_cluster=false` unless declared otherwise. |
| Documentation structure | `documentation_structure` diagnostic family | Structural metrics and recurrence visibility | Repo file structure, headings, front matter, code fences, links | No prose interpretation, claim extraction, authority inference, ontology promotion, ledger writes, or repo mutation. |

## Shared promotion boundaries across architectural families

### Observation family

The observation pipeline separates `Observation`, `Evidence`, and `Fact`. The ingestor always records observation and evidence events, but fact production is optional. This is direct implementation evidence that observed data is not identical to promoted fact.

### Capability family

Capability recovery has a strict ladder:

```text
package_installed fact
  -> capability candidate
  -> verification evidence / capability inventory lookup
  -> verified / stale / provider_reported / unverified read-model status
```

The implementation repeatedly states that candidates and verification inspections do not grant permission, selection, policy approval, tool invocation, or execution authority.

### Execution / operation family

Execution grammar separates capability gaps, recommendations, registered operation candidates, and actual calls. `ToolRegistry` owns registered operation catalog state, while `ToolExecutor` owns registered-operation execution only. A provider operation string or recommendation is not a registered operation.

### Relationship family

Relationship recovery promotes only bounded evidence. Static Python imports become import relationships, static definitions become definition relationships, and documentation front matter becomes document relationships. The adapter explicitly rejects behavior, reachability, ownership, and runtime authority claims.

### Explanation / presentation family

Explanation surfaces are read models over projected support. They expose current belief, ambiguity, competing beliefs, and conflict without creating new truth. Prior explanation recovery also found recurring fields of identity, responsibility, input/output, consumers, preservation/cache, authority boundary, and unknowns rather than a single explanation ontology.

### Repository artifact and documentation family

Documentation structure follows a safe progression from prose to observable structure to recurrence visibility. It intentionally refuses meaning extraction, claim extraction, authority inference, shape inference, ontology promotion, event writes, and repository mutation.

### Diagnostic family

Diagnostic promotion is registry-governed rather than inference-governed. A diagnostic surface becomes operationally visible only when declared in `DIAGNOSTIC_INVENTORY` and checked by `diagnostic_shape_audit` implementation specs. If recordable, it remains diagnostic-scoped rather than cluster truth unless explicitly declared otherwise.

### Projection family

Projection is promoted inspectability, not original authority. `StateProjector` reads event history, applies events, and finalizes derived indexes. This makes projection a durable read model, but not a substitute for append-only event authority.

## Does promotion require stronger evidence than observation?

Mostly yes, but the kind of stronger evidence differs by family.

| Driver | Accepted / rejected | Implementation-backed assessment |
| --- | --- | --- |
| Observation | Accepted as entry condition, rejected as sufficient universal condition. | Observation can become evidence and sometimes fact, but candidates, diagnostics, relationship adapters, and documentation structure preserve observation without promoting broader claims. |
| Recurrence | Accepted for documentation structure and prior architectural recovery, rejected as universal promotion authority. | Documentation structure can show recurrence histograms and skeletons while still rejecting claim/ontology promotion. Recurrence alone does not register operations or verify capabilities. |
| Validation | Accepted as a major promotion driver. | Decision validation gates runtime routing; policy/registry validation gates tool execution; shape audit validates diagnostic declarations; graph validation checks projected relationships. |
| Implementation ownership | Accepted as a major promotion driver. | Each family has a specific owner: ingestor, projector, registry, inventory, adapter, diagnostic registry, explanation builder. Cross-family promotion is not ownerless. |
| Relationship evidence | Accepted in relationship and graph projection families. | Relationships require static syntax, explicit front matter, or catalog-backed fact projection. They do not prove behavior or ownership without additional evidence. |
| Operator testimony | Partially accepted. | User/source facts can carry high-confidence source types, and runtime decisions can record answers/questions/refusals, but operator language does not automatically promote presentation vocabulary into repository knowledge. |
| Event history | Accepted for projected state. | Event ledger replay is the authority for projected `State`; projection cache and diagnostics remain subordinate to event history. |

## Recurring transition types recovered

The implementation supports these recurring transition forms:

```text
observe -> evidence -> fact
```

Implemented by `ObservationIngestor`, with a suppression counterexample.

```text
fact -> support -> current belief / conflict / explanation
```

Implemented by fact support projection, conflict projection, and `ExplanationBuilder`.

```text
fact -> candidate -> verification inspection -> verified/stale/unverified status
```

Implemented by capability candidates, verification evidence, verification inspection, and capability inventory.

```text
declared manifest -> registered operation -> validated/policy-checked execution
```

Implemented by toolkit manifest loading, `ToolRegistry`, runtime routing, and `ToolExecutor`.

```text
explicit syntax/metadata/fact -> bounded relationship -> graph validation / relationship view
```

Implemented by relationship observation and catalog relationship projection.

```text
repo file structure -> structural observation -> recurrence visibility -> no semantic promotion
```

Implemented by documentation structure investigation and diagnostic boundaries.

```text
diagnostic registry row -> implementation shape audit -> operational visibility
```

Implemented by diagnostic inventory and diagnostic shape audit specs.

These transitions share a grammar of bounded input, preservation, owner-specific validation/derivation, promoted output, and boundary notes. They do not collapse into one lifecycle or one authority source.

## Counterexamples and intentional non-promotion

1. **Suppressed fact promotion:** Prometheus `node_uname_info` `os` observations with suppression metadata become observation/evidence events but no fact.
2. **Capability candidates:** Package evidence can create a capability candidate, but the module states this is not capability proof, permission, selection, policy evaluation, or tool execution.
3. **Unverified candidates:** Verification inspection leaves candidates unverified when no projected `capability_verified` fact exists.
4. **Provider recommendations:** Capability catalog recommendations and provider operation strings are recommendation metadata, not registered operations.
5. **Relationship observation:** Imports and definitions are syntax evidence only; they do not prove calls, behavior, boundaries, reachability, or ownership.
6. **Documentation structure:** Structural recurrence visibility intentionally refuses prose interpretation, claim extraction, authority inference, shape inference, ontology promotion, ledger writes, and repo mutation.
7. **Diagnostics:** Recordable diagnostics write diagnostic-scoped facts and declare `mutates_cluster=false`; they do not silently become cluster facts.
8. **Projection diagnostics/cache:** Projection timings, cache status, and rendered state-build information are non-authoritative visibility, not new truth authority.
9. **Explanation rendering:** Current/ambiguous/no-current-belief explanation statuses describe projected support and conflict; they do not create missing support.

## Lexical, structural, operational, and knowledge promotion

The repository distinguishes these in implementation, though not under one formal taxonomy.

| Promotion class | Implementation evidence | Current status |
| --- | --- | --- |
| Lexical promotion | Documentation structure can observe labels and recurrence; tool vocabulary and explanation investigations recover vocabulary boundaries. | Weakest. Vocabulary recurrence is not knowledge without reachability or implementation evidence. |
| Structural promotion | Documentation structure observes headings, front matter, links, code fences, skeletons, and recurrence; relationship adapters observe syntax/front-matter relationships. | Supported as read-only structure and recurrence visibility, not semantic authority. |
| Operational promotion | Toolkit manifests become registered operations; runtime decisions can call registered tools after validation and policy; diagnostics become visible through inventory and shape audit. | Strong where registry/validation owners exist. Not derived from package/binary observation alone. |
| Knowledge promotion | Observations can become facts; facts become supports/current beliefs; facts project relationships; capability verification uses `capability_verified` facts. | Evidence-backed and projection-owned; not all observations become durable facts. |

## Supported conclusions

1. The repository already demonstrates recurring promotion boundaries across multiple architectural families.
2. Observation is preserved separately from evidence and fact in the ingestion/projection pipeline.
3. Promotion is owner-specific: ingestor, projector, registry, verification inventory, relationship adapter, diagnostic registry, and explanation builder each own different transitions.
4. Candidate status is intentionally weaker than verification, registration, execution, and durable knowledge.
5. Registered operation authority is manifest/registry/policy backed, not inferred from observed package or binary evidence.
6. Projection is a durable inspectable read model, but event history remains the authority behind it.
7. Documentation and lexical recurrence are intentionally kept below semantic/ontology promotion.
8. Diagnostic visibility is registry/audit governed and explicitly separated from cluster mutation.
9. A shared promotion shape exists: bounded observation/declaration, preserved support, owner validation/derivation, promoted output, and explicit boundary.

## Unsupported conclusions

1. Unsupported: Seed has one implemented universal promotion engine.
2. Unsupported: recurrence alone promotes vocabulary into repository knowledge.
3. Unsupported: observation immediately becomes durable knowledge in all cases.
4. Unsupported: package/binary evidence creates registered operations.
5. Unsupported: provider recommendations are registered executable tools.
6. Unsupported: projection, cache status, diagnostics, or presentation surfaces create truth authority by rendering it.
7. Unsupported: relationship evidence proves behavior, call paths, ownership, or runtime reachability without additional implementation evidence.
8. Unsupported: current implementation defines a complete `observed -> candidate -> validated -> promoted` lifecycle for every concept.

## Recommended next investigation

Investigate the exact boundary between `FactSupport`, `current belief`, `FactConflict`, and explanation statuses:

```text
fact support selection
  -> current / ambiguous / no_current_belief
  -> conflict projection
  -> explanation rendering
```

This is the narrowest next step because it tests promotion from supported facts into operator-facing belief without proposing new ontology or runtime design.
