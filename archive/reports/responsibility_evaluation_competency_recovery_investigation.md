# Responsibility Evaluation Competency Recovery Investigation

Repository authority wins. This investigation does not redesign the competency, add runtime behavior, change schemas, change CLI surfaces, migrate vocabulary, or create a new abstraction. It recovers the bounded implementation work already present in the repository that the competency roadmap calls **Responsibility Evaluation**.

## Executive conclusion

**Responsibility Evaluation is currently one competency expressed through several implementation owners, not one implemented runtime responsibility family.**

Implementation-backed definition:

> Responsibility Evaluation is the bounded work that consumes ownership, authority, verification, selection, reasoning, or diagnostic evidence and emits a constrained conclusion about whether a responsibility or ownership claim is supported, unsupported, ambiguous, incomplete, blocked by authority, outside current implementation authority, or merely a candidate. It preserves evidence, confidence or status, reasons, unknowns, and non-promotion boundaries, and it terminates before assignment, promotion, execution, mutation, or answer synthesis changes repository truth.

The central implementation pattern is not "who owns this work?" The pattern is:

1. gather repository-visible candidate or support evidence,
2. evaluate the evidence under local deterministic rules,
3. emit a classified conclusion with reasons and boundaries,
4. expose missing evidence or blocked authority when the conclusion is incomplete, and
5. stop before downstream authority such as promotion, execution, recording, cluster mutation, generic review judgment, or architectural redesign.

The strongest owners are:

- `ownership_discrepancies`: candidate ownership, ambiguity, missing owner, insufficient evidence, and diagnostic-only capability needs.
- `service_ownership_authority`: service ownership authority reachability, blocked observations, uncertainty, and read-only boundaries.
- `container_ownership_authority`: container ownership authority blockage under constrained authority, remaining observations, and boundary preservation.
- `capability_verification`: candidate-vs-verified responsibility separation and verification sufficiency against existing admitted inventory.
- `capability_promotion_readiness`: future promotion sufficiency without promotion.
- `capability_inventory`: admitted capability knowledge versus executable operation metadata and requested capability presentation.
- `reasoning_path_audit`: derivation sufficiency and downstream consumer visibility for operational conclusions.
- `selection_path_audit`: candidate selection sufficiency and unknown-selection termination.
- `diagnostic_inventory` and `diagnostic_shape_audit`: diagnostic authority and visibility evaluation for recordability, event-ledger writes, mutation, and implementation shape.
- Current recovery investigations: responsibility-family and competency reports evaluate whether evidence supports a family, a competency, a candidate family, or no current owner.

A new implementation responsibility family does **not** naturally emerge yet. The evidence supports a competency and review discipline. It does not support adding a generic evaluator, registry, command, schema, or family because evaluation rules are intentionally local to their owning surfaces and no shared compatibility surface or compression point is implemented.

## Repository evidence reviewed

Implementation and investigation evidence reviewed includes:

- `seed_runtime/ownership_discrepancies.py`.
- `seed_runtime/service_ownership_authority.py`.
- `seed_runtime/container_ownership_authority.py`.
- `seed_runtime/capability_verification.py`.
- `seed_runtime/capability_promotion_readiness.py`.
- `seed_runtime/capability_inventory.py`.
- `seed_runtime/reasoning_path_audit.py`.
- `seed_runtime/selection_path_audit.py`.
- Diagnostic inventory and diagnostic shape-audit governance through existing repository instructions and tests.
- `seed_competency_roadmap_v2.md`.
- `evidence_interpretation_competency_recovery_investigation.md`.
- `responsibility_family_vs_competency_recovery_investigation.md`.
- Recent family recovery materials for Operational Responsibility, Observation-Derived Capability, Answer Composition, authority investigations, ownership investigations, and Inquiry Navigation context.

## What bounded work constitutes Responsibility Evaluation?

Responsibility Evaluation is the repository's repeated evidence-to-conclusion discipline for responsibility-like claims. It evaluates whether a claim has enough support to be treated as:

- a provisional candidate,
- a supported responsibility within a local surface,
- an ambiguous or conflicted attribution,
- an unsupported responsibility due to missing evidence,
- an incomplete responsibility due to verification or promotion gaps,
- an authority-blocked responsibility due to unavailable observation authority,
- a diagnostic-only finding that must not become cluster truth, or
- an out-of-authority conclusion that the current implementation must not make.

The competency is not the same as Evidence Interpretation. Evidence Interpretation asks what visible evidence means inside provenance, shape, authority, and non-promotion boundaries. Responsibility Evaluation uses interpreted evidence to judge sufficiency for a responsibility, ownership, authority, verification, readiness, selection, or diagnostic claim. It therefore depends on Evidence Interpretation but adds the sufficiency question: **is this enough to justify the responsibility conclusion, and where must evaluation stop?**

The competency is also not the same as Bounded Answer Composition. Evaluation may produce support, conflict, unknowns, and boundaries. Answer Composition later presents that material as an answer. `operational_story`, `reasoning_path_audit`, and `selection_path_audit` show that evaluation material can feed answer-like views, but the evaluation boundary remains separate from composing a complete operator response.

## Implementation owners

### 1. Ownership discrepancies

**Owner:** `seed_runtime/ownership_discrepancies.py`.

**Input evidence:** projected facts for storage and service subjects: host predicates, mount source predicates, storage owner candidates, listener endpoints, process/container host facts, Prometheus targets, service configuration host facts, matching local listener facts, matching listener-process facts, and fact support IDs.

**Evaluated output:** `OwnershipDiscrepancyRow` with `candidate_owner`, `confidence`, `evidence_count`, `conflict`, `reason`, evidence refs, and `label="candidate"`.

**Evaluation rules:**

- Missing candidate evidence becomes `missing_owner`.
- Endpoint-only service evidence becomes `insufficient_evidence`.
- Local listener evidence can confirm socket presence while still producing `owner_not_observed` when process/container/service ownership remains unverified.
- Remote mount source evidence can support a candidate while still producing `remote_export_attribution_missing`.
- Multiple plausible candidates above the confidence threshold become `multiple_candidate_owners` or `mount_source_conflict`.
- Local mount visibility can be treated as consumer evidence rather than ownership, producing `consumer_mistaken_as_owner` under storage conditions.
- Conflict rows drive diagnostic-only capability need records rather than ownership assignment.

**Authority boundary:** the module is read-only. It consumes projected facts and emits diagnostic rows and diagnostic-only capability needs. It does not mutate state, assign owners, promote facts, execute observations, or resolve conflicts.

**Non-evaluation boundary:** it does not decide actual service/container/storage ownership. A row label remains `candidate`; even a high-confidence candidate remains provisional when conflict or missing verification is present.

**Termination:** evaluation terminates at a discrepancy row and optional diagnostic capability need records. Downstream capability acquisition, observation execution, and ownership assignment are separate.

### 2. Service ownership authority

**Owner:** `seed_runtime/service_ownership_authority.py`.

**Input evidence:** constrained authority profile, required service observations, capability needs derived from `ownership_discrepancies`, observation-domain data, observation-permission guidance, privilege discovery explanations, and discrepancy summaries keyed by needed capability.

**Evaluated output:** `ServiceOwnershipAuthoritySlice` with required observations, required authority, available authority, reachable observations, blocked observations, blocked details, outcome, strategy status, remaining observations, uncertainty, blocking boundary, and read-only boundary fields.

**Evaluation rules:**

- Required observations are built from current discrepancy-owned capability needs plus known service observation classes.
- TCP listener and systemd observations are reachable through local passive authority.
- Listener-process inventory can be reachable through partial non-root/local passive conditions.
- Container inventory and container port mapping remain blocked when Docker/root authority is unavailable.
- Mixed reachable and blocked observations produce `partially_reachable`; only reachable produces `reachable`; only blocked produces `blocked`; absence of both produces `unknown`.
- Docker/root unavailable for container runtime observations produces the named blocking boundary.

**Authority boundary:** the supplied authority profile is authoritative for the constrained scenario. The surface is explicitly read-only: no records, event-ledger writes, provider acquisition, permission creation, observation execution, or cluster mutation.

**Non-evaluation boundary:** it does not acquire Docker/root authority, execute observations, ask providers, or promote service ownership. It evaluates reachability of evidence required to justify service ownership, not ownership itself.

**Termination:** evaluation terminates at strategy status, blocked observations, uncertainty, and blocking boundary.

### 3. Container ownership authority

**Owner:** `seed_runtime/container_ownership_authority.py`.

**Input evidence:** constrained authority profile, container runtime observation requirements, observation-domain capability mapping, observation-permission recognition of Docker socket access, privilege guidance, and subject-specific pressure from ownership discrepancy capability needs.

**Evaluated output:** `ContainerOwnershipAuthoritySlice` with required observations, required authority, available authority, outcome, current strategy, remaining observations, uncertainty, blocking boundary, and read-only boundary fields.

**Evaluation rules:**

- The slice is scoped to container ownership and the container runtime domain.
- Container inventory and port mapping require Docker group or root authority.
- If all required observations require Docker/root and both are unavailable, the outcome is `blocked`.
- Local passive authority is explicitly not sufficient for Docker/root container runtime evidence.
- Subject-specific pressure may exist from ownership discrepancies, but pressure does not override authority.

**Authority boundary:** the constrained profile remains authoritative. The surface is read-only and does not record, write events, mutate cluster state, acquire providers, create permissions, or execute observations.

**Non-evaluation boundary:** it does not decide container ownership and does not generalize container runtime authority to all service ownership. It evaluates only whether the required observation evidence can be reached under the profile.

**Termination:** evaluation terminates at `blocked`, `unknown`, remaining observations, uncertainty, and blocking boundary.

### 4. Capability verification

**Owner:** `seed_runtime/capability_verification.py`.

**Input evidence:** evidence-derived capability candidates, acquired verification evidence, capability inventory entries derived from projected `capability_verified` facts, and optional fact index.

**Evaluated output:** `CapabilityVerificationInspection` and per-candidate `CapabilityVerification` records with verification status, supporting evidence, verification-supporting facts, acquired verification evidence, rationale, and boundary notes.

**Evaluation rules:**

- The candidate universe comes from evidence-derived capability candidates.
- Verification status comes from existing capability inventory semantics backed by projected `capability_verified` facts.
- Candidate evidence without a projected verification fact remains `unverified`.
- Inventory-backed status and support produce the verification status and rationale.

**Authority boundary:** verification inspection is read-only and explicitly not capability selection, execution authority, execution decision, tool invocation, permission, policy evaluation, or tool execution.

**Non-evaluation boundary:** it does not perform policy evaluation, select capabilities, invoke tools, or create verification facts.

**Termination:** evaluation terminates at verification status and rationale.

### 5. Capability promotion readiness

**Owner:** `seed_runtime/capability_promotion_readiness.py`.

**Input evidence:** evidence-derived capability candidates, candidate support, read-only verification evidence such as local PATH metadata, and optional fact index.

**Evaluated output:** `CapabilityPromotionReadinessInspection` and per-candidate `CapabilityPromotionReadiness` records with candidate support, verification support, `promotion_readiness` of `supported` or `unsupported`, rationale, and boundary notes.

**Evaluation rules:**

- A future capability verification promotion is `supported` only when both candidate support and verification support are present.
- Missing verification support makes promotion readiness `unsupported` even if candidate support exists.
- Supported readiness means a future promotion would be supportable by inspected evidence; it is not promotion.

**Authority boundary:** the surface does not create `capability_verified` facts, modify inventory, select capabilities, evaluate policy, invoke tools, plan, or execute.

**Non-evaluation boundary:** it does not decide that a capability is verified and does not perform admission into repository truth.

**Termination:** evaluation terminates at supported/unsupported readiness.

### 6. Capability inventory

**Owner:** `seed_runtime/capability_inventory.py`.

**Input evidence:** projected `capability_verified` facts and fact support, registered `ToolSpec` executable operation contracts, requested capabilities from unresolved needs, predicate catalog, and expiry semantics.

**Evaluated output:** deterministic `CapabilityInventoryEntry` records with verification state, supporting facts/evidence, support summary, observed timestamps, age, and reason.

**Evaluation rules:**

- Inventory universe is the union of registered tool capabilities, requested tool needs, and verification fact subjects.
- Admitted repository capability knowledge is separate from executable operation contract metadata.
- Registered executable operation contracts can widen presentation but do not verify capability existence.
- Missing verification facts produce `unverified`; expired verification facts produce `stale`; value semantics can produce `verified`, `provider_reported`, or `unverified` states.

**Authority boundary:** inventory interprets already-projected state only. It does not execute tools, call providers, append events, schedule work, route runtime behavior, perform promotion, create facts, decide execution authority, or admit operation metadata as knowledge.

**Non-evaluation boundary:** inventory presentation is not promotion/admission and not an execution contract authorizer.

**Termination:** evaluation terminates at inventory state and reason.

### 7. Reasoning path audit

**Owner:** `seed_runtime/reasoning_path_audit.py`.

**Input evidence:** ownership discrepancies, diagnostic capability need records, capability needs, pressure audit, privilege discovery, and operational story.

**Evaluated output:** `ReasoningPathAudit` with evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and read-only boundary.

**Evaluation rules:**

- Relevant ownership discrepancy rows become evidence records.
- Conflicts become intermediate conclusions such as ownership attribution incomplete.
- Diagnostic capability need records become derived capability-need conclusions.
- Capability needs, pressure audit, privilege discovery, and operational story are recorded as consumers when they match the subject/domain.
- If no derivation evidence is available, the audit emits an unknown rather than inventing a path.

**Authority boundary:** the audit is a read-only reasoning audit. It records no facts, writes no event ledger entries, and mutates no cluster state.

**Non-evaluation boundary:** it explains derivation and consumers; it does not create new conclusions beyond implemented diagnostic surfaces and does not repair or execute anything.

**Termination:** evaluation terminates at evidence, intermediate/derived conclusions, consumers, story impact, or unknowns.

### 8. Selection path audit

**Owner:** `seed_runtime/selection_path_audit.py`.

**Input evidence:** pressure audit, operational story, requested target, current focus, and pressure candidates.

**Evaluated output:** `SelectionPathAudit` with selected item, candidate set, selection factors, non-selected candidates, evidence, outcome, unknowns, and read-only boundary.

**Evaluation rules:**

- Current focus/primary pressure targets are evaluated from operational story focus and pressure ordering.
- Pressure candidates are ordered by descending score, then category name.
- Non-selected candidates are exposed with reasons rather than hidden.
- Unknown targets produce `selected="unknown"`, an outcome reason, and an unknown-selection entry rather than fabricated selection evidence.

**Authority boundary:** the audit is read-only and records no facts, writes no event ledger entries, and mutates no cluster state.

**Non-evaluation boundary:** it explains an implemented selection path. It does not change pressure ordering, alter story focus, select operational work, or implement a planner.

**Termination:** evaluation terminates at selected/unknown and candidate lineage.

### 9. Diagnostic inventory and diagnostic shape audit

**Owner:** diagnostic visibility governance across registry, shape audit, and tests.

**Input evidence:** diagnostic surface declarations and implementation shape for read-only status, recording scope, event-ledger writes, cluster mutation, and output fields.

**Evaluated output:** inventory and shape-audit findings that say whether a surface is visible, recordability is declared, record scope is correct, event-ledger behavior is declared, mutation is declared, and the implementation shape matches expectations.

**Evaluation rules:**

- A new diagnostic, audit, probe, view, operational CLI flag, or recordable output must be registered.
- Shape-audit specs and tests must prove the surface appears in diagnostic inventory and is checked by diagnostic shape audit.
- If a diagnostic supports `--record`, `record_scope=diagnostic_run` must be proved unless intentionally different.
- If it writes the event ledger, `mutates_cluster=false` must be proved unless intentionally operational.

**Authority boundary:** diagnostic findings must not silently become cluster truth. Diagnostic-only findings should prefer `diagnostic_run:<id>` scoped subjects and preserve `mutates_cluster=false` for read-only diagnostics.

**Non-evaluation boundary:** diagnostic inventory and shape audit evaluate operational visibility and authority declarations, not the domain truth of every diagnostic finding.

**Termination:** evaluation terminates at visibility/shape conformance or mismatch. It does not promote diagnostic findings into operational truth.

### 10. Current recovery investigations

**Owner:** repository investigations such as Evidence Interpretation recovery, Responsibility Family vs Competency recovery, operational responsibility slices, observation-derived capability completion, answer composition completion, authority investigations, ownership investigations, and Inquiry Navigation work.

**Input evidence:** implementation slices, tests, modules, CLI surfaces, diagnostic surfaces, previous reports, and explicit counterexamples.

**Evaluated output:** supported conclusions, unsupported conclusions, confidence, natural completion points, candidate families, family-vs-competency classification, recommended next family, and stop criteria.

**Evaluation rules:**

- Responsibility families are recovered from implementation ownership chains, not labels.
- Competencies are recurring disciplines that may span multiple owners.
- Candidate abstractions require a concrete compression point, shared API, compatibility surface, or tests before becoming implementation families.
- Presentation vocabulary is not knowledge without implementation evidence.
- Evaluation stops when the next conclusion would require hidden intent, semantic reasoning, unsupported promotion, mutation, or authority beyond evidence.

**Authority boundary:** investigations may classify support and recommend next work, but they do not implement runtime behavior or create repository truth by vocabulary alone.

**Non-evaluation boundary:** investigation output is not schema, not CLI behavior, not runtime execution, and not automatic ownership recovery.

**Termination:** evaluation terminates at implementation-backed conclusion, unsupported conclusion, or recommended next family.

## Recovered evaluation disciplines

The following disciplines are implementation-backed. They are not proposed stages; they are recurring local work found in existing owners.

| Discipline | Implementation evidence | Output |
| --- | --- | --- |
| Ownership sufficiency | `ownership_discrepancies` candidate rules | provisional owner, missing owner, insufficient evidence, conflict |
| Ownership ambiguity | multiple candidates, mount-source conflict, consumer-vs-source checks | ambiguity exposed rather than resolved |
| Authority evaluation | service/container ownership authority slices | reachable, partially reachable, blocked, unknown, blocking boundary |
| Verification sufficiency | capability verification inspection | verified/unverified/stale/provider-reported/unknown status from admitted inventory |
| Promotion sufficiency | capability promotion readiness | supported/unsupported future promotion readiness |
| Support sufficiency | capability inventory, fact support, reasoning path audit | support reason, missing support, unknown derivation |
| Responsibility confidence | ownership candidates and evidence counts | confidence and evidence count without assignment |
| Responsibility exclusion | boundary notes, read-only flags, no mutation/recording clauses | explicit refusal to promote, execute, mutate, or assign |
| Selection sufficiency | selection path audit | selected/unknown with candidate lineage |
| Diagnostic authority sufficiency | diagnostic inventory/shape audit governance | visibility and mutation/recording conformance |
| Family/competency sufficiency | recovery investigations | family, competency, candidate family, unsupported abstraction |

## Recurring invariants

The strongest recurring invariants are:

1. **Candidate != supported responsibility.** Ownership candidates and capability candidates are preserved, but additional evidence or authority is required before verification, promotion, assignment, or execution.
2. **Supported responsibility != assigned responsibility.** `ownership_discrepancies` can support provisional ownership while still labeling rows as candidates and preserving conflicts.
3. **Evaluation != promotion.** Capability promotion readiness explicitly evaluates whether promotion would be supportable while refusing to create `capability_verified` facts.
4. **Evaluation != execution.** Verification, readiness, inventory, service authority, container authority, reasoning path, and selection path all terminate before tool invocation or observation execution.
5. **Evaluation != mutation.** Read-only boundaries recur across authority slices, reasoning path, selection path, diagnostic governance, and capability inspections.
6. **Diagnostic output != cluster truth.** Diagnostic-only capability needs and diagnostic recording boundaries prevent findings from becoming cluster facts or runtime entities.
7. **Authority availability gates responsibility conclusions.** Service and container ownership authority surfaces expose blocked observations and uncertainty rather than claiming ownership from unreachable evidence.
8. **Ambiguity is an output, not an exception.** Multiple ownership candidates, unknown selection targets, missing derivation evidence, and unsupported promotion readiness are first-class outputs.
9. **Evidence source ownership is preserved.** Capability inventory separates admitted capability facts, executable operation metadata, and requested capabilities; ownership authority slices preserve discrepancy-owned summaries rather than absorbing their ownership.
10. **Evaluation stops before downstream answer or action authority.** Reasoning path and selection path expose lineage; operational story can consume them, but evaluation does not itself become action planning or truth creation.

## Counterexamples and stopping evidence

### Ownership is preserved without evaluation

`capability_inventory` preserves executable operation contract capability labels as presentation-universe inputs without treating them as admitted capability knowledge or verification. This is preservation and presentation, not ownership evaluation. Similarly, diagnostic inventory preserves metadata about surfaces without evaluating every domain finding as true.

### Evaluation intentionally stops

`capability_promotion_readiness` stops at supported/unsupported readiness and refuses to create `capability_verified` facts. `service_ownership_authority` and `container_ownership_authority` stop at reachability/blockage and do not execute observations. `selection_path_audit` stops with `unknown` for unsupported targets.

### Multiple evaluation responsibilities are compressed locally

`ownership_discrepancies` compresses candidate extraction, confidence selection, ambiguity detection, conflict classification, and diagnostic capability need derivation. That compression is local and tested by its surface; it does not prove a generic evaluator.

`reasoning_path_audit` compresses evidence gathering, intermediate conclusion generation, derived conclusion generation, consumer mapping, story impact, and unknown production. Again, this is a local audit shape, not a generic Responsibility Evaluation service.

### Evaluation terminates before downstream authority

Service/container authority evaluation terminates before provider acquisition or observation execution. Capability verification terminates before selection and execution. Promotion readiness terminates before promotion. Diagnostic governance terminates before cluster mutation. Recovery investigations terminate before runtime implementation.

## Supported conclusions

1. Responsibility Evaluation is implementation-backed as a competency.
2. It is not currently backed as one generic runtime owner or responsibility family.
3. The competency consumes interpreted evidence and produces sufficiency classifications for responsibility-like claims.
4. Existing implementation owners already evaluate ownership support, ambiguity, authority reachability, verification support, promotion readiness, selection support, derivation support, and diagnostic authority.
5. The repository repeatedly separates candidate/support/readiness from assignment/promotion/execution/mutation.
6. Authority boundaries and unknowns are part of the evaluated output, not afterthoughts.
7. Existing recovery investigations are themselves examples of Responsibility Evaluation at the architectural-review layer.
8. Current evidence supports keeping Responsibility Evaluation as a review competency until an actual compression point emerges.

## Unsupported conclusions

1. Unsupported: Responsibility Evaluation is already a single implemented service, registry, command, schema, or API.
2. Unsupported: ownership candidate rows assign owners.
3. Unsupported: verified or readiness-supported capabilities authorize execution.
4. Unsupported: promotion readiness promotes facts.
5. Unsupported: authority slices can infer ownership when required observations are blocked.
6. Unsupported: diagnostic findings can silently become cluster truth.
7. Unsupported: answer composition or operational story is itself responsibility evaluation.
8. Unsupported: Evidence Interpretation and Responsibility Evaluation are the same competency.
9. Unsupported: a new implementation responsibility family should be created now.
10. Unsupported: absent visibility alone proves a responsibility mismatch; several surfaces emit unknown/blocked/incomplete instead.

## Is Responsibility Evaluation one competency or several implementation families?

Responsibility Evaluation is one competency expressed through several implementation families and local owners.

It is one competency because the same bounded work recurs: evidence is compared to a responsibility-like claim, sufficiency is evaluated, the conclusion is classified, authority boundaries are preserved, and evaluation stops before promotion/action. It is several implementation families because each owner has local evidence types and rules:

- ownership discrepancies evaluate ownership candidates and conflicts;
- authority slices evaluate observation reachability;
- capability verification evaluates admitted verification support;
- promotion readiness evaluates future supportability;
- inventory evaluates admitted state versus operation metadata;
- reasoning/selection audits evaluate lineage and selection sufficiency;
- diagnostic governance evaluates surface visibility and mutation/recording authority;
- recovery investigations evaluate architectural responsibility and competency claims.

No implementation evidence shows a shared evaluator interface, registry, result schema, CLI, or compatibility-preserving abstraction that would justify unifying them now.

## Does a new implementation responsibility family naturally emerge?

No implemented responsibility family naturally emerges yet.

A **candidate future family** is visible only if future work finds a real compression point around review result schemas, common sufficiency classifications, shared boundary-note generation, or diagnostic inventory assertions. Current repository authority does not support creating that family now because:

- the roadmap says Responsibility Evaluation is ready as investigation discipline, not as an implemented review evaluator;
- existing evaluation rules are owner-specific;
- no generalized evaluator over arbitrary target evidence exists;
- no test-backed review result schema exists;
- no target-specific compatibility-break evaluator exists; and
- adding one now would redesign rather than recover.

## Recommended next implementation family

The recommended next implementation family remains **Inquiry Navigation**, not a new generic Responsibility Evaluation abstraction.

Reasoning:

1. Evidence Interpretation has already been recovered as a competency and not one generic implementation owner.
2. Responsibility Evaluation is now recoverable as the next competency-level discipline, also distributed across owners.
3. The prompt context says a parallel branch is recovering Inquiry Navigation through bounded question dispatch.
4. Responsibility Evaluation depends on being able to find the right evidence-bearing surfaces; Inquiry Navigation is the natural next implementation family because it can make that dispatch explicit without inventing a generic evaluator.
5. A generic Responsibility Evaluation family should wait until inquiry/navigation work exposes repeated concrete evaluator compression points with tests.

## Acceptance answers

### What bounded work constitutes Responsibility Evaluation inside the repository?

Responsibility Evaluation is the bounded evidence-to-sufficiency work that determines whether responsibility-like claims are supported, unsupported, ambiguous, incomplete, blocked by authority, diagnostic-only, or outside current authority. It is implemented through local owners such as ownership discrepancies, ownership authority slices, capability verification/readiness/inventory, reasoning and selection audits, diagnostic governance, and recovery investigations.

### Is Responsibility Evaluation one competency or several implementation families?

It is one competency expressed through several implementation owners and families. It is not one implemented runtime responsibility family.

### What implementation evidence supports that answer?

The evidence is the repeated local pattern across ownership discrepancy rows, authority slice outcomes, verification statuses, promotion-readiness statuses, capability inventory states, reasoning/selection audit unknowns and conclusions, diagnostic inventory/shape governance, and prior investigations that distinguish supported families from unsupported abstractions.

### Does a new implementation responsibility family naturally emerge?

No. A candidate future family may eventually emerge around review result schemas or shared sufficiency/boundary mechanics, but current implementation evidence supports only a competency and review discipline. The next implementation family should remain Inquiry Navigation unless future implementation evidence provides a concrete compression point.
