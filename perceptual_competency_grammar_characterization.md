# Perceptual Competency Grammar Characterization

## Executive answer

Yes, the repository demonstrates a recurring, implementation-backed perceptual competency grammar often enough to characterize it as a methodology pattern used by several independently recovered competencies:

```text
Observation -> Evidence -> Classification -> Authority -> Stop
```

The pattern is real, but bounded. It is not implemented as a universal runtime pipeline, not owned by a shared base class, and not consistently present in every family. The strongest support comes from Pressure Visibility, Selection / Reference Visibility, Capability Verification, diagnostic surfaces, and responsibility / completion inquiry reports. Provider Language Translation supports the front half strongly and authority/stop unevenly. Answer Composition supports a neighboring composition grammar around answer / reason / supporting evidence / boundary, but it is not itself a full perceptual grammar. Negative investigations support the methodology by preserving unsupported conclusions, counterexamples, and insufficient-evidence stops.

The repository does **not** provide sufficient implementation evidence to recover a shared ownership family for this grammar.

```text
Insufficient implementation evidence.
```

## Methodology reviewed

The review treated implementation and tests as primary authority, and prose reports as secondary only where they summarize implementation-backed recovery. The investigation looked for five narrow stages:

| Stage | Narrow meaning used in this report |
| --- | --- |
| Observation | What was perceived by an implementation surface, audit, provider, or inquiry. |
| Evidence | What preserves that perception separately from the conclusion. |
| Classification | What conclusion, status, rank, selection, or category is permitted from the evidence. |
| Authority | What the surface is allowed to do, including negative authority. |
| Stop | Where the surface terminates instead of mutating, executing, promoting, planning, or inferring beyond evidence. |

Counterexamples were searched for explicitly: classification without evidence, authority not explicit, observation immediately mutating implementation, and absence of meaningful stop conditions.

## Families examined

Representative implementation-backed families reviewed:

- Answer Composition.
- Pressure Visibility.
- Reference Selection and Selection Path visibility.
- Capability Verification / Observation-Derived Capability.
- Inquiry and responsibility-family completion inquiry reports.
- Provider Language Translation.
- Completion audits.
- Negative investigations.
- Diagnostic surfaces, including diagnostic inventory and diagnostic shape audit.

## Recurring grammar by family

### 1. Pressure Visibility

Pressure Visibility is the strongest direct example of the full grammar.

- **Observation:** `build_pressure_audit(...)` observes existing diagnostic-shape, ownership, capability, predicate-consumer, and fragile-predicate surfaces.
- **Evidence:** Each `PressureItem` preserves `evidence` as its own field, and the formatter renders an explicit `Evidence:` section.
- **Classification:** Pressure rows are classified by `category` and ranked by `score`; output is sorted by descending score and category.
- **Authority:** The builder docstring bounds the work to ranking operational pressure without planning, recording, or mutation.
- **Stop:** The output recommends an inspection command, but does not execute the command, record facts, or mutate state.

This is implementation, not just vocabulary: the dataclass carries evidence and reason separately, and the builder produces sorted pressure items from existing inputs rather than owning downstream remediation.

### 2. Selection Path / Reference Selection

Selection Path and Reference Selection support the grammar as read-only selection explanation.

- **Observation:** Selection Path observes already-implemented pressure and operational-story outputs for a requested target. Reference Selection observes impact-audit and snapshot-policy outputs for history-domain comparison.
- **Evidence:** Selection Path preserves `candidates`, `selection_factors`, `non_selected`, `evidence`, `outcome`, and `unknowns` separately. Reference Selection preserves `selected_reference`, `selection_rationale`, and `alternative_references` separately.
- **Classification:** Selection Path classifies a selected target or returns `selected="unknown"` for unsupported target logic. Reference Selection selects the previous comparable snapshot when comparable pairs exist, or classifies the reference as unavailable.
- **Authority:** Both expose explicit read-only authority boundaries. Selection Path has a `boundary` stating no fact recording, event-ledger writes, or cluster mutation. Reference Selection has an `authority_boundary` that denies accepted-reference and expectation-bearing authority.
- **Stop:** Unsupported Selection Path targets terminate with an explicit unknown instead of fabricating selection evidence. Reference Selection stops at visibility and does not create baselines, expectations, lifecycle policy, persistence, runtime behavior, or storage.

This family demonstrates the recurring grammar in a selection/answer-adjacent competency, while also showing that the grammar is local and target-specific rather than a general inquiry selector.

### 3. Capability Verification / Observation-Derived Capability

Capability Verification strongly supports Evidence -> Classification -> Authority -> Stop, and begins with evidence-derived observations.

- **Observation:** Candidate universe comes from evidence-derived capability candidates.
- **Evidence:** `_ObservedCapabilityEvidence` preserves candidate supporting evidence and acquired verification evidence before verification status is interpreted.
- **Classification:** `_CapabilityVerificationStatus` classifies each candidate as unverified or as the inventory-derived verification state.
- **Authority:** Boundary notes explicitly state that verified capability is not capability selection, execution authority, execution decision, tool invocation, permission, or policy evaluation.
- **Stop:** The module is read-only inspection; it does not select capabilities, evaluate policy, invoke tools, plan, or execute.

The strongest counterexample inside this family is also valuable: candidate evidence without a projected `capability_verified` fact remains `unverified`. That proves classification is not allowed to jump directly from observation evidence to execution authority.

### 4. Diagnostic surfaces

Diagnostic Inventory and Diagnostic Shape Audit support the grammar as operational surface governance.

- **Observation:** Diagnostic Inventory observes declared CLI diagnostic surfaces and their operational shape. Diagnostic Shape Audit statically observes implementation slices for build, format, JSON, record, state, repo-file, event-ledger, diagnostic-fact, and mutation markers.
- **Evidence:** Inventory entries preserve per-surface flags such as `supports_record`, `record_scope`, `emits_diagnostic_facts`, `writes_event_ledger`, and `mutates_cluster`. Shape Audit returns observed implementation shape, including record scope and mutation/event indicators.
- **Classification:** Shape Audit classifies consistency between registry and implementation authority; tests assert expected statuses such as `consistent`.
- **Authority:** The registry distinguishes diagnostic facts from cluster facts and event-ledger writes from cluster mutation.
- **Stop:** Read-only surfaces declare `mutates_cluster=False`; recordable diagnostics must use `record_scope="diagnostic_run"` unless intentionally different.

Diagnostic surfaces show the grammar most operationally: observations about implementation shape are preserved separately and used to classify consistency without silently becoming cluster truth.

### 5. Provider Language Translation

Provider Language Translation supports the front half of the grammar strongly and the authority/stop stages unevenly.

- **Observation:** Providers observe external or repository-specific languages: dpkg status text, Python AST, Prometheus vector samples, systemd JSON rows, local-host files/APIs, and git command output.
- **Evidence:** Mature paths preserve intermediate evidence records, such as `PackageRecord`, `RelationshipFact`, or `RepositoryObservation`; compressed paths preserve provider labels, timestamps, metadata, dimensions, and predicate assignments inside direct observation construction.
- **Classification:** Providers classify accepted package records, relationship kinds, Prometheus metric branches, systemd unit states, filesystem dimensions, or repository dirty/status counts.
- **Authority:** Some paths carry strong negative authority, especially static Python relationship extraction and repository observation. Other paths rely on local source boundaries and tests rather than a common authority record.
- **Stop:** Some providers stop cleanly at provider records before observation construction; others perform translation and observation construction in the same method.

This is a counterexample to overclaiming implementation consistency. Provider Language Translation recurs as methodology, but not as a uniform implementation pattern. Prometheus, systemd, and local-host direct observations demonstrate compressed translation where observation, evidence preservation, classification, and observation construction are close together.

### 6. Answer Composition

Answer Composition supports a related composition grammar, but only partially supports the perceptual competency grammar.

- **Observation:** The reviewed slice is about `SelectionPathAudit`, an already implemented inquiry surface.
- **Evidence:** The slice separated `_SelectionSupportingEvidencePayload` from lineage, while preserving the public `Evidence:` and `Outcome:` sections.
- **Classification:** The composition boundary distinguishes reason/outcome from supporting evidence, but does not itself classify repository state.
- **Authority:** Compatibility and read-only boundaries are preserved by the unchanged public audit object and diagnostic behavior.
- **Stop:** The slice stops after one implementation-local ownership transition and explicitly leaves remaining compression points for future evidence.

Answer Composition therefore supports the broader methodology: preserve selected answer, reason, supporting evidence, lineage, unknowns, and boundary. It does not prove a full Observation -> Evidence -> Classification -> Authority -> Stop pipeline on its own.

### 7. Inquiry and completion audits

Inquiry and completion audits support the grammar as review methodology rather than runtime implementation.

- **Observation:** Family completion inquiry observes slice reports and implementation surfaces.
- **Evidence:** It uses implementation evidence, changed files, tests, generated architecture evidence, compatibility preservation, and remaining compressed boundaries.
- **Classification:** It classifies families as boundedly complete, incomplete, or future-family candidates.
- **Authority:** It states that implementation and tests outrank architectural prose, and that completion is not a manual flag.
- **Stop:** It stops at read-only inquiry and explicitly says no stable Seed command exists yet for automatic family completion inquiry.

This is evidence for a methodology pattern, not a consolidated competency implementation.

### 8. Negative investigations

Negative investigations strongly support the Stop stage and the discipline around unsupported classification.

- They preserve unsupported domains, unknown targets, insufficient evidence, absence, ambiguity, and negative ownership as evidence about what the repository can and cannot support.
- They prevent classification without sufficient evidence.
- They frequently terminate with `insufficient evidence`, `unknown`, or `future family` instead of recommending redesign or ownership recovery.

Negative investigations are central to the grammar because they prove `Stop` is not merely the absence of work; it is often a positive methodology result.

## Stage-by-stage findings

### Which competencies begin with Observation?

Strong evidence:

- Pressure Visibility observes existing audits and visibility surfaces.
- Diagnostic surfaces observe declared and implemented CLI diagnostic shapes.
- Provider Language Translation observes external/provider languages.
- Capability Verification begins from evidence-derived capability candidates.
- Selection Path observes existing pressure/story selection evidence.

Partial evidence:

- Answer Composition observes already-constructed inquiry artifacts rather than raw operational state.
- Completion inquiry observes prior slice evidence and reports rather than a first-class runtime data source.

### Which preserve Evidence separately?

Strong evidence:

- Pressure Visibility preserves `PressureItem.evidence` separately from `reason` and `recommended_command`.
- Selection Path preserves separate supporting evidence payload and public `evidence` field.
- Reference Selection preserves selected reference, rationale, alternatives, limitations, and authority boundary separately.
- Capability Verification preserves candidate supporting evidence separately from verification status.
- Diagnostic Inventory preserves surface declarations separately from diagnostic shape-audit observed implementation results.

Partial or uneven evidence:

- Provider Language Translation preserves evidence records in dpkg, Python relationships, and repository observation, but compressed providers do not uniformly materialize an intermediate evidence object.

### Which perform Classification?

Strong evidence:

- Pressure Visibility scores and ranks pressure categories.
- Selection Path selects, ranks candidates, and returns unknown for unsupported selection targets.
- Reference Selection selects or marks unavailable history references.
- Capability Verification classifies candidates as unverified or inventory-derived verified states.
- Diagnostic Shape Audit classifies registry/implementation shape consistency.

Partial evidence:

- Provider Language Translation classifies provider grammar elements into accepted records, predicates, relationship kinds, statuses, and dimensions, but the classification is provider-local rather than shared.
- Answer Composition classifies composition roles more than operational state.

### Which expose Authority boundaries?

Strong evidence:

- Capability Verification has explicit negative boundary notes denying execution, selection, permission, policy, and invocation authority.
- Selection Path and Reference Selection expose read-only/no-recording/no-mutation boundaries.
- Diagnostic Inventory distinguishes diagnostic fact emission, cluster fact emission, event-ledger writes, record scope, and mutation.

Partial evidence:

- Provider Language Translation exposes authority boundaries unevenly: some paths state negative semantics explicitly, while compressed provider paths rely on local collection boundaries.
- Completion inquiry exposes methodology authority, not a runtime authority surface.

### Which own explicit Stop conditions?

Strong evidence:

- Capability Verification stops at read-only inspection.
- Pressure Visibility stops at recommended inspection command rather than executing remediation.
- Selection Path stops at unknown when target selection evidence is unavailable.
- Reference Selection stops at visibility and no baseline/expectation creation.
- Diagnostic surfaces stop at diagnostic-run records or read-only output without cluster mutation.
- Negative investigations stop at unsupported / insufficient evidence.

Partial evidence:

- Provider Language Translation has local stops at provider records or observation construction boundaries, but not a consistent shared stop record.
- Answer Composition stops per-slice after a single recovered boundary, but the stop condition belongs to recovery methodology rather than the composed answer object itself.

## Counterexamples and limits

### Classification without sufficient evidence

The repository actively prevents this in several places:

- Capability Verification keeps candidate evidence unverified when no projected `capability_verified` fact exists.
- Selection Path returns `selected="unknown"` for unsupported targets rather than inventing selection evidence.
- Reference Selection returns unsupported-domain or unavailable-reference output instead of treating latest snapshots as accepted baselines.

No strong implementation-backed example was found where a mature recovered competency intentionally classifies beyond its preserved evidence. The counterexample is mostly negative: compressed provider paths perform local classification close to observation construction, so their evidence/classification separation is weaker.

### Authority not explicit

Provider Language Translation is the main uneven case. Some providers and reports have explicit negative authority; others have provider-local code boundaries but no shared authority record. This contradicts any claim of a consistent implementation pattern across all providers.

### Observation immediately mutates implementation

The reviewed diagnostic, pressure, selection, reference, and capability-verification surfaces are explicitly read-only or diagnostic-run scoped. No reviewed implementation-backed competency showed observation immediately mutating cluster truth. However, diagnostic recording can write the event ledger, so the boundary matters: the inventory and shape audit preserve `record_scope="diagnostic_run"` and `mutates_cluster=False` to prevent diagnostic findings from becoming cluster facts.

### No meaningful stop condition

The strongest weak spots are compressed provider translation paths where stop is implicit in local method boundaries rather than exposed as a public stop condition. This is not enough to reject the recurring methodology, but it rejects a claim of uniform implementation ownership.

## Supported conclusions

1. The repository demonstrates a recurring `Observation -> Evidence -> Classification -> Authority -> Stop` grammar often enough to characterize it as a **recurring perceptual competency grammar**.
2. The recurring grammar is strongest in Pressure Visibility, Selection Path / Reference Selection, Capability Verification, Diagnostic Inventory / Diagnostic Shape Audit, and negative-investigation methodology.
3. Provider Language Translation supports the grammar unevenly: it clearly observes provider language and preserves/uses evidence, but implementation separation varies by provider.
4. Answer Composition supports adjacent composition boundaries and evidence preservation, but does not independently prove the full perceptual grammar.
5. The recurring identity is a **methodology pattern** first, a **competency pattern** in several read-only visibility competencies second, and **not** a shared implementation ownership pattern.

## Unsupported conclusions

The repository evidence does **not** support the following conclusions:

- A universal cognition framework exists or should be introduced.
- A universal runtime pipeline exists or should be built.
- All competencies implement every stage.
- Provider Language Translation has a uniform intermediate-record architecture.
- Answer Composition is itself the same thing as perceptual classification.
- The grammar justifies recovering a shared ownership family.
- The grammar should be promoted into schema changes, base classes, runtime redesign, or pipeline consolidation.

## Confidence

- **High** confidence that the grammar recurs as methodology across recovered work.
- **Medium-high** confidence that it recurs as a competency pattern in read-only visibility/diagnostic/evaluation surfaces.
- **Low** confidence that it recurs as a shared implementation pattern across all families.
- **Very low** confidence that it supports ownership recovery.

## Recommendation on methodology, competency, or ownership

This should be characterized as:

```text
methodology pattern, with recurring competency expression in read-only perceptual/visibility surfaces
```

It should **not** be characterized as:

```text
shared implementation ownership family
```

Final ownership recommendation:

```text
Insufficient implementation evidence.
```
