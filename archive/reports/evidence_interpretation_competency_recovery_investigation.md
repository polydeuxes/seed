# Evidence Interpretation Competency Recovery Investigation

Repository authority wins. This investigation does not redesign the competency, add runtime behavior, change schemas, change CLI surfaces, migrate vocabulary, or create a new abstraction. It recovers the bounded implementation work already present in the repository that the competency roadmap calls **Evidence Interpretation**.

## Executive answer

**Evidence Interpretation is currently one competency expressed as several implementation families, not one single runtime owner.**

The implementation-backed definition is:

> Evidence Interpretation is the bounded work that consumes visible evidence already present in projected state, local inspection, catalogs, diagnostics, or preserved operator notes, applies repository-owned deterministic rules to classify or qualify that evidence, and emits an interpreted read model, explanation, audit, readiness status, relationship definition, or answer payload while preserving explicit authority and non-promotion boundaries.

The repository does not implement a generic `EvidenceInterpretation` service. Instead, interpretation is distributed across owners that already transform evidence into bounded meaning:

- `FactSupport` / state support projection interprets facts as aggregate durable support, current measurement samples, expiration-aware support groups, conflicts, and unambiguous best support.
- `ExplanationBuilder` interprets projected support as current, ambiguous, competing, or absent beliefs with recursive provenance.
- `CapabilityInventory` interprets `capability_verified` fact support into verified, provider-reported, unverified, stale, or unknown capability states.
- `VerificationEvidence`, `CapabilityVerification`, and `CapabilityPromotionReadiness` interpret candidate evidence and local PATH observations without selecting, authorizing, executing, or promoting capabilities.
- `RelationshipCatalog` interprets fact predicates through read-only relationship vocabulary.
- `ReasoningPathAudit` and `SelectionPathAudit` interpret existing diagnostic surfaces into derivation paths and selection traces.
- `InquiryOrientation` intentionally performs only lexical related-material interpretation and explicitly forbids semantic intent interpretation.
- `OperationalStory` interprets multiple visibility surfaces into bounded answer, reasoning, support, boundary, and limitation payloads.

A new implementation responsibility family naturally emerges as a **candidate**, but not as an implemented owner: **Evidence Interpretation** can name the cross-cutting competency and review discipline. Repository authority does not currently support adding a generic implementation family without a concrete compression point, shared API, or compatibility surface.

## Method and source scope

Reviewed implementation and existing recovery artifacts around:

- `FactSupport`, state support selection, fact conflicts, and explanation building.
- `VerificationEvidence`, `CapabilityVerification`, `CapabilityInventory`, and promotion readiness.
- `RelationshipCatalog` and predicate-derived relationship vocabulary.
- `ReasoningPathAudit`, `SelectionPathAudit`, `InquiryOrientation`, and `OperationalStory`.
- Recent investigations on architectural invariants, implicit observation workflow, explainability, slice readiness, observation-derived capability, answer composition, execution visibility, and responsibility recovery.

This report treats source code and tests as stronger authority than architectural documents. Prior reports are used only where they describe existing implementation evidence or recurring invariants.

## Implementation-backed definition

Evidence Interpretation is not raw observation, not arbitrary semantic understanding, not evaluation, not promotion, and not answer composition by itself.

Implementation-backed Evidence Interpretation consists of six repeated moves:

1. **Consume visible evidence**: projected facts, evidence IDs, source types, candidate records, local filesystem metadata, registered tool metadata, diagnostic rows, pressure audit items, source-navigation matches, or catalog entries.
2. **Apply deterministic repository rules**: predicate semantics, support ranking, fact expiry, value normalization, source/candidate joins, catalog mappings, lexical overlap, diagnostic matching, pressure ordering, or read-only boundary construction.
3. **Emit interpreted evidence**: support groups, current/competing belief status, capability state, verification status, promotion-readiness status, relationship definitions, derivation paths, selection traces, related material, or story payloads.
4. **Preserve provenance and support**: supporting fact IDs, evidence IDs, source types, rationale, support notes, reason fields, intermediate/derived conclusions, supporting evidence strings, and investigation paths.
5. **Declare authority boundaries**: read-only mode, no event-ledger writes, no cluster mutation, no tool execution, no policy approval, no promotion, no capability selection, no semantic intent recovery, or no repository-truth creation.
6. **Terminate before downstream authority**: interpretation may inform explanation, inspection, presentation, readiness, or audit output; it does not become cluster mutation, operational execution, durable promotion, or final answer authority unless a separate owner performs that work.

## Bounded work by implementation owner

### 1. Fact support and state support selection

**Owner:** `FactSupport` plus state support helpers.

**Input evidence:** `Fact` records with subject, predicate, value, dimensions, evidence IDs, source type, confidence, observation time, inference metadata, and optional expiry.

**Interpreted output:** Support groups for one subject/predicate/value claim; durable aggregate support; measurement current samples; expired support markers; current facts; unambiguous best support or ambiguity.

**Interpretation rules:**

- Predicate metadata and legacy measurement predicate sets distinguish durable support from volatile measurements.
- `FactSupport` preserves supporting fact IDs, source types, confidence, first/latest observation timestamps, expiration metadata, predicate semantics, and support kind.
- `State.get_fact_supports(...)` resolves aliases except for endpoint-scoped predicates, filters by predicate/dimensions, and projects support groups.
- `State.get_fact_support(...)` returns only the unambiguous strongest support; ties or unresolved conflicts terminate as no best support rather than forcing a winner.
- Current fact selection uses support groups and representative fact ranking by confidence, observed-vs-inferred status, observation time, and fact ID.

**Authority boundary:** Projection/support interpretation is derived from projected facts. It is not the event ledger, not source acquisition, not cluster mutation, and not operational execution.

**Non-interpretation boundary:** Fact support does not evaluate arbitrary truth, decide promotion, execute acquisition, or compose a final answer. It also treats measurement predicates differently from durable predicates rather than aggregating repeated volatile samples into stronger truth.

**Termination:** Support interpretation terminates at `FactSupport`, current fact selection, conflict records, and optional explanations that consume those structures.

### 2. ExplanationBuilder

**Owner:** `ExplanationBuilder`.

**Input evidence:** Projected `State`, `FactSupport`, `FactConflict`, facts, evidence IDs, source fact links, inference rule IDs, and entity aliases.

**Interpreted output:** `Explanation` with `status` of `current`, `ambiguous`, or `no_current_belief`; current beliefs; competing beliefs; conflict metadata; recursive fact provenance.

**Interpretation rules:**

- Multi-cardinality predicates expose all support groups as current beliefs.
- Single-cardinality predicates ask state for the unambiguous best support.
- Absence of a best support with existing supports becomes `ambiguous`; absence of supports becomes `no_current_belief`.
- Competing beliefs are support groups whose value differs from the selected best value.
- Recursive source-fact traversal preserves inference lineage and confidence cap visibility without inventing additional reasoning.

**Authority boundary:** The builder is explicitly deterministic and entirely projected-state based.

**Non-interpretation boundary:** It does not acquire evidence, mutate state, change fact confidence, resolve truth outside projection rules, or perform arbitrary natural-language reasoning.

**Termination:** Explanation terminates at an explanation object; formatting/presentation is downstream.

### 3. Capability inventory

**Owner:** `capability_inventory`.

**Input evidence:** Projected `capability_verified` facts and their `FactSupport`; registered `ToolSpec` capability labels; unresolved `ToolNeed` capability names; evidence graph views for supporting evidence.

**Interpreted output:** `CapabilityInventoryEntry` with state `verified`, `provider_reported`, `unverified`, `stale`, or `unknown`; support summary; evidence summary; age; reason.

**Interpretation rules:**

- Inventory universe is the union of admitted projected capability subjects, executable operation contract metadata, and requested capabilities.
- Operation contract labels widen presentation but do not admit repository capability knowledge.
- Current active support maps normalized support values to verification states.
- Expired support maps to `stale`.
- Missing `capability_verified` support maps to `unverified`.
- Supporting facts are joined to evidence graph summaries; evidence summaries preserve evidence ID, type, summary, confidence, and observation time.

**Authority boundary:** Capability inventory is read-only and interprets already-projected state only.

**Non-interpretation boundary:** It does not execute tools, call providers, append events, schedule work, select capabilities, authorize execution, evaluate policy, or create `capability_verified` facts. Registered tool metadata is not interpreted as proof of availability or verification.

**Termination:** Interpretation terminates at inventory entries and summaries.

### 4. Verification evidence acquisition

**Owner:** `verification_evidence`.

**Input evidence:** Evidence-derived capability candidates and local PATH filesystem metadata.

**Interpreted output:** `VerificationEvidence` records such as `binary_path_observed`, with rationale, support notes, and boundary notes.

**Interpretation rules:**

- Only repository-justified candidate-to-binary mappings are checked.
- Evidence is acquired by checking whether binary names exist as executable files in PATH directories.
- Observed executable files support later verification inspection but do not verify capability existence by themselves.

**Authority boundary:** Read-only local inspection only.

**Non-interpretation boundary:** It never invokes binaries, promotes evidence into `capability_verified`, selects capabilities, grants permission, approves policy, or executes tools.

**Termination:** Interpretation terminates at evidence records and inspection output.

### 5. Capability verification inspection

**Owner:** `capability_verification`.

**Input evidence:** Capability candidates, candidate supporting evidence, acquired verification evidence, and capability inventory entries.

**Interpreted output:** `CapabilityVerification` status, preserved candidate evidence, verification-supporting facts/evidence, acquired evidence, rationale, and boundary notes.

**Interpretation rules:**

- Candidate evidence is preserved separately from verification status.
- Verification status comes only from capability inventory semantics backed by projected `capability_verified` facts.
- If no inventory entry exists, candidate remains `unverified` even when candidate evidence exists.

**Authority boundary:** Read-only candidate-to-verification inspection.

**Non-interpretation boundary:** Candidate preservation is not verification, selection, permission, policy approval, execution authority, or tool invocation.

**Termination:** Interpretation terminates at verification inspection status.

### 6. Capability promotion readiness

**Owner:** `capability_promotion_readiness`.

**Input evidence:** Evidence-derived capability candidates and acquired verification evidence.

**Interpreted output:** `CapabilityPromotionReadiness` with `supported` or `unsupported`, rationale, candidate support, verification support, and boundary notes.

**Interpretation rules:**

- `_CapabilityVerificationPayload` separates candidate support from verification support before readiness interpretation.
- Promotion readiness is `supported` only when both candidate support and verification support are present.
- Missing verification support keeps readiness `unsupported`.

**Authority boundary:** Read-only future-promotion support inspection.

**Non-interpretation boundary:** Readiness is not promotion. The module does not create `capability_verified` facts, modify inventory, select capabilities, authorize execution, evaluate policy, or invoke tools.

**Termination:** Interpretation terminates at readiness status and rationale.

### 7. Relationship catalog

**Owner:** `RelationshipCatalog`.

**Input evidence:** Catalog JSON relationship definitions and fact predicates.

**Interpreted output:** Relationship definitions grouped by relationship name or derived-from predicate.

**Interpretation rules:**

- Catalog entries define relationship kind, subject/object types, derived predicates, and optional fixed object.
- `for_predicate(...)` maps a fact predicate to relationship definitions in stable name order.
- Duplicate relationship names are rejected.

**Authority boundary:** Read-only vocabulary for how entities connect to each other.

**Non-interpretation boundary:** Catalog mapping does not prove runtime behavior, calls, ownership, reachability, execution authority, or environmental truth. It only supplies vocabulary and mapping rules for projection/validation consumers.

**Termination:** Interpretation terminates at relationship definitions and mapping lists.

### 8. Reasoning path audit

**Owner:** `reasoning_path_audit`.

**Input evidence:** Ownership discrepancy rows, capability needs, pressure audit output, privilege discovery output, operational story output, and subject/domain filters.

**Interpreted output:** `ReasoningPathAudit` with observed evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and read-only boundary.

**Interpretation rules:**

- Relevant ownership discrepancy rows become observed evidence.
- Conflict-bearing rows can become intermediate conclusions such as ownership attribution incomplete.
- Diagnostic capability need records become derived capability-need conclusions.
- Capability needs, pressure, privilege, and operational story outputs become consumers or story impact when subject/domain matching supports the join.
- If nothing matches, an unknown derivation reason is emitted instead of inventing a chain.

**Authority boundary:** Read-only reasoning audit; records no facts, writes no event ledger entries, and mutates no cluster state.

**Non-interpretation boundary:** It composes existing diagnostic surfaces only; it does not create the underlying diagnostics, prove external truth, or execute remediation.

**Termination:** Interpretation terminates at a derivation path audit.

### 9. Selection path audit

**Owner:** `selection_path_audit`.

**Input evidence:** Pressure audit candidates, operational story focus, and target string.

**Interpreted output:** `SelectionPathAudit` with selected item, candidate set, selection factors, non-selected candidates, evidence, outcome, unknowns, and read-only boundary.

**Interpretation rules:**

- Recognized current-focus or primary-pressure targets consume pressure ordering and story focus.
- Pressure candidates are ranked by pressure audit ordering.
- Non-selected candidates preserve reason and evidence.
- Unknown target yields an explicit unknown selection result instead of asserting an unsupported selection surface.

**Authority boundary:** Read-only selection trace.

**Non-interpretation boundary:** It does not change selection behavior, schedule actions, mutate facts, or authorize operational work.

**Termination:** Interpretation terminates at a selection trace audit.

### 10. Inquiry orientation

**Owner:** `inquiry_orientation`.

**Input evidence:** Preserved raw inquiry note, projected fact supports, source-navigation matches, deterministic tokens.

**Interpreted output:** `InquiryOrientationView` containing potentially related material, support/why-related text, uncertainty, and authority boundary.

**Interpretation rules:**

- Raw note text is tokenized deterministically.
- Related material is selected by lexical overlap against projected fact supports and source-navigation matches.
- Related material is deduped and capped.
- Matches produce uncertainty text that warns the relation may be incomplete or incidental; absence of matches does not prove unrelatedness.

**Authority boundary:** Inquiry orientation is read-only and treats operator prose as preserved evidence for the probe only.

**Non-interpretation boundary:** It explicitly rejects semantic interpretation, operator intent, ownership, importance, recommended action, next safe move, facts, goals, tool needs, decisions, proposals, plans, authorization, commands, and runtime instructions.

**Termination:** Interpretation terminates at orientation view material; rendering is separate.

### 11. Operational story

**Owner:** `operational_story`.

**Input evidence:** Pressure audit, capability needs, privilege discovery, correlation audit, impact audit, investigation path audit, and absence/presence of pressures.

**Interpreted output:** `OperationalStory` with focus, pressure, supporting evidence, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes, investigation path, unknowns, and boundary.

**Interpretation rules:**

- Primary pressure supplies focus and pressure payload when present.
- Capability needs become missing-capability answer material.
- Privilege discovery becomes constraints.
- Correlation findings become correlation gaps.
- Impact metrics become impact, recent changes, and observed outcomes.
- Missing pressure/capability/impact evidence becomes explicit unknowns.
- Internally, answer, reasoning, supporting evidence, boundary, and limitations are separated before compatibility handoff into the public story object.

**Authority boundary:** Read-only view; no recording, no event-ledger writes, no cluster mutation.

**Non-interpretation boundary:** It does not plan, execute, record facts, or mutate operational state. It composes existing visibility surfaces.

**Termination:** Interpretation terminates at a bounded story answer object and formatter input.

## Interpretation families recovered

The following families are implementation-backed, but they are families of work rather than a shared class hierarchy.

| Family | Implementation evidence | Interpreted output | Boundary |
| --- | --- | --- | --- |
| Provenance/support interpretation | `FactSupport`, `ExplanationBuilder`, evidence graph joins | support groups, belief explanations, evidence IDs, source facts | no acquisition, no mutation, no truth beyond projected support |
| Current-belief interpretation | `State.get_fact_support`, `ExplanationBuilder.why` | current / ambiguous / no-current / competing beliefs | no forced winner when support is ambiguous |
| Authority interpretation | boundary fields and notes in audits, verification, inquiry, story | read-only, no-record, no-ledger-write, no-mutation, no-execution limits | authority is exposed, not expanded |
| Compatibility / handoff interpretation | answer payloads and public view handoffs in inquiry and operational story | public compatibility objects from private payloads | no schema/CLI behavior change implied |
| Verification interpretation | capability inventory and verification inspection | capability states and verification statuses | candidate evidence is not verification authority |
| Promotion-readiness interpretation | capability promotion readiness | supported / unsupported readiness | readiness is not promotion |
| Projection interpretation | state support projection and relationship predicate mapping | support indexes and relationship definitions | projection/read-only mapping is not durable event truth |
| Relationship interpretation | `RelationshipCatalog` | relationship definitions by predicate | vocabulary mapping is not behavior/ownership proof |
| Selection/derivation interpretation | reasoning and selection path audits | derivation path and selection trace | audit output is not execution or mutation |
| Lexical orientation interpretation | inquiry orientation | related material and uncertainty | lexical overlap is not semantic intent |
| Answer-material interpretation | operational story | answer/reason/support/boundary/limitations payloads | answer composition is not truth creation or action |

## Counterexamples and negative evidence

### Visible evidence returned or preserved without stronger interpretation

- `VerificationEvidence` preserves PATH-observed executable file metadata as support but explicitly says observed binary path is not verification, permission, approval, or execution authority.
- `CapabilityVerification` preserves candidate support separately from verification status; candidate evidence remains unverified without projected `capability_verified` inventory support.
- `InquiryOrientation` preserves operator prose and lexical overlaps but refuses semantic intent interpretation.
- `ReasoningPathAudit` emits unknowns when no derivation evidence is available instead of fabricating a chain.
- `SelectionPathAudit` emits `selected="unknown"` for unsupported target surfaces instead of generalizing selection logic.

### Interpretation intentionally forbidden

- Documentation structure and code relationship observation reports explicitly reject prose interpretation, grammar interpretation, responsibility recovery, authority inference, runtime behavior inference, ownership inference, and mutation.
- Inquiry orientation forbids interpreting raw notes as facts, claims, goals, capabilities, plans, commands, authorization, intent, concern, recommended action, or safe next move.
- Capability verification and promotion readiness forbid treating candidates, binary metadata, or readiness as selection, permission, policy approval, execution, or promotion.

### Multiple interpretation responsibilities compressed together

- `CapabilityInventory` still interprets the inventory universe, verification state, staleness, supporting facts, supporting evidence, and age in one module, while comments preserve local handoffs between admitted capability state and executable operation contract metadata.
- `ReasoningPathAudit` combines relevance matching, observed evidence preservation, intermediate conclusions, derived conclusions, consumer discovery, story impact, and unknowns. Internal payloads split derived conclusions from lineage, but no separate generic derivation interpreter exists.
- `OperationalStory` composes answer material, reasoning, support, limitations, and authority boundary from several surfaces. Internal payloads make the split visible but preserve one public compatibility object.
- `ExplanationBuilder` combines current-belief status interpretation, support explanation, recursive provenance traversal, confidence cap visibility, conflict attachment, and alias-resolution path exposure.

### Interpretation terminates before evaluation

- `FactSupport` produces support groups and unambiguous support selection but does not evaluate responsibility sufficiency or promote facts.
- Capability promotion readiness says a future promotion would be supportable or unsupported but does not perform promotion.
- Verification inspection reports status from inventory but does not select, authorize, or execute.
- Inquiry orientation reports potentially related material but does not decide operator intent or recommended action.
- Selection path audit reports why a current surface selected an item, but does not evaluate whether that selection is correct.

## Recurring invariants

The implementation supports these invariants as recovered evidence, not architectural preference:

1. **Visible evidence != interpreted evidence.** Raw facts, evidence IDs, PATH files, candidate records, operator notes, and diagnostic rows are repeatedly transformed into support groups, states, statuses, reasons, related material, or paths.
2. **Interpreted evidence != evaluation.** Support groups, verification status, readiness, derivation paths, and orientation results do not by themselves evaluate responsibility sufficiency or correctness.
3. **Evaluation != promotion.** Promotion readiness may be supported, but no `capability_verified` fact is created.
4. **Promotion != answer.** Capability admission facts can feed inventory, but answer composition remains a separate consumer.
5. **Candidate != verified.** Capability candidates and local binary observations are preserved but remain non-authoritative without projected verification facts.
6. **Lexical relation != semantic intent.** Inquiry orientation deliberately stops at deterministic overlap.
7. **Projection/read model != event truth.** Fact support, inventory, relationship mapping, and story outputs are derived views, not event-ledger authority.
8. **Read-only interpretation != mutation.** Audits and views repeatedly declare no fact recording, no event-ledger writes, and no cluster mutation.
9. **Authority boundary is part of the interpreted output.** Rationale, boundary notes, and boundary objects are not incidental prose; they prevent overclaiming by downstream consumers.
10. **Unknown is a valid interpreted output.** Ambiguity, no-current-belief, unknown verification state, unknown selection target, and no derivation evidence are first-class stopping points.

## Supported conclusions

1. Evidence Interpretation is already present in implementation as bounded deterministic transformations from visible evidence into interpreted read models, statuses, reasons, paths, and answer payloads.
2. It is **one competency** in the roadmap sense because the recurring bounded work is consistent: interpret evidence under repository authority while preserving boundaries and stopping before unsupported promotion/evaluation/action.
3. It is **several implementation families** in code because no generic owner, interface, registry, or compatibility surface currently unifies support interpretation, capability verification interpretation, relationship interpretation, lexical orientation, derivation-path interpretation, selection interpretation, and story composition.
4. The strongest implementation owners are `FactSupport`/state support projection, `ExplanationBuilder`, `CapabilityInventory`, `CapabilityVerification`, `CapabilityPromotionReadiness`, `RelationshipCatalog`, `ReasoningPathAudit`, `SelectionPathAudit`, `InquiryOrientation`, and `OperationalStory`.
5. The repository supports a recurring boundary grammar: evidence is preserved, interpreted, qualified, and handed off; interpretation does not silently become evaluation, promotion, answer, execution, or mutation.
6. The competency roadmap's **Evidence Interpretation** slot is implementation-backed, but the roadmap's earlier label **Authority Interpretation** is too narrow for the implementation evidence now reviewed. Authority interpretation is one strong subfamily, not the whole recovered competency.

## Unsupported conclusions

1. Unsupported: the repository has a generic `EvidenceInterpretation` runtime abstraction.
2. Unsupported: all interpretation should be centralized. Current evidence shows bounded local owners and public compatibility surfaces, not a shared API requirement.
3. Unsupported: candidate evidence, lexical overlap, relationship vocabulary, pressure ordering, or local binary presence is enough to promote repository truth.
4. Unsupported: Evidence Interpretation includes arbitrary semantic understanding of operator prose or architectural documents.
5. Unsupported: Verification evidence acquisition verifies capabilities. It only observes support for later inspection.
6. Unsupported: Promotion readiness performs promotion. It explicitly stops before fact creation.
7. Unsupported: Relationship catalog mapping proves behavior, ownership, reachability, or runtime execution.
8. Unsupported: Operational story or inquiry orientation owns planning, scheduling, execution, or mutation.
9. Unsupported: Existing answer composition surfaces should be retrofitted into an Evidence Interpretation abstraction without a concrete implementation compression point.

## Does a new implementation responsibility family naturally emerge?

**Yes, as a recovery candidate; no, as an implementation mandate.**

A candidate family naturally emerges because many owners perform the same bounded move:

```text
visible evidence
  -> deterministic repository rule
  -> interpreted evidence/status/path/reason
  -> explicit boundary
  -> termination before downstream authority
```

However, repository authority does not support implementing a new shared family now. There is no current failing command, compatibility gap, duplicated public schema, or shared runtime interface that requires extraction. The family is best treated as a recovered competency and review lens until a concrete compression point appears.

## Recommended next implementation family

The recommended next implementation family is **Inquiry Navigation**, not a new generic Evidence Interpretation abstraction.

Reasoning:

- The prompt context says a parallel branch is already recovering Inquiry Navigation through bounded question dispatch.
- Evidence Interpretation appears sufficiently recovered as a competency and distributed implementation pattern.
- The repository already has question-surface inventory, bounded ask dispatch, inquiry orientation, selection path audit, and reasoning path audit surfaces that can inform navigation.
- A generic Evidence Interpretation owner would risk redesigning rather than recovering.

If future implementation work is justified, it should be driven by a concrete compression point such as repeated boundary-note construction, repeated unknown/status schemas, repeated evidence-to-status adapters, or duplicated diagnostic inventory assertions. Until then, preserve local owners.

## Acceptance answers

### What bounded work constitutes Evidence Interpretation inside the repository?

Evidence Interpretation is the deterministic transformation of visible evidence into interpreted support, status, relationship, readiness, derivation, selection, orientation, or answer-material outputs with provenance and authority boundaries preserved. It consumes projected state, local inspection evidence, catalogs, diagnostics, and preserved notes; it emits bounded read models and audits; it stops before evaluation, promotion, execution, mutation, or arbitrary semantic understanding.

### Is Evidence Interpretation one competency or several implementation families?

It is one competency expressed through several implementation families. The competency is unified by the repeated evidence-to-interpreted-output move and the recurring boundary discipline. The implementation is distributed across support projection, explanations, capability inventory/verification/readiness, relationship catalog mapping, reasoning/selection audits, inquiry orientation, and operational story composition.

### What implementation evidence supports that answer?

Support comes from source owners that encode deterministic interpretation rules and boundaries: `FactSupport`, state support helpers, `ExplanationBuilder`, `capability_inventory`, `verification_evidence`, `capability_verification`, `capability_promotion_readiness`, `RelationshipCatalog`, `reasoning_path_audit`, `selection_path_audit`, `inquiry_orientation`, and `operational_story`. Existing recovery reports reinforce the same invariants around authority boundaries, non-promotion, answer composition, observation-derived capability, and responsibility evaluation.

### Does a new implementation responsibility family naturally emerge?

A candidate family emerges conceptually, but it should not be implemented now. The repository supports **Evidence Interpretation** as a recovered competency and cross-cutting implementation pattern, not as a new runtime owner. The next implementation-backed frontier should remain Inquiry Navigation unless concrete implementation compression proves otherwise.
