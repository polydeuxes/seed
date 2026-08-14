# Constitutional Conservation Characterization

## Evidence reviewed

This report treats "conservation" as a question, not as architecture. The reviewed evidence was:

- `constitutional_transition_artifact_delta_characterization.md`, especially its family-by-family account of artifacts that changed and did not change.
- `constitutional_transition_family_characterization.md`, especially its refusal to collapse multiple transition families into one transition engine.
- `constitutional_interpretation_characterization.md`, especially its boundary around bounded local competence.
- `constitutional_promotion_authority_characterization.md`, especially its distinction between pressure, support, candidate state, and authority.
- `implementation_readiness_characterization.md`, especially its distinction between implementation pressure and implementation readiness.
- `competency_interrogation_methodology_reconciliation.md`, especially its evidence, authority, boundary, negative authority, locality, lawful termination, and confidence questions.
- Implementation evidence in `seed_runtime/inquiry_orientation.py`, `seed_runtime/capability_candidates.py`, `seed_runtime/verification_evidence.py`, `seed_runtime/capability_verification.py`, `seed_runtime/pressure_audit.py`, `seed_runtime/tool_needs.py`, `seed_runtime/projection_shape.py`, and associated tests.

Repository authority wins over the candidate label. This document therefore does not stabilize `conservation` as an architecture term. It characterizes a recurring boundary pattern: some transitions remain lawful only because adjacent artifacts retain their prior authority class, evidential status, subject boundary, ownership boundary, or operational force.

## Small answer

Yes, recurring constitutional transitions often require some artifacts or distinctions to remain unchanged.

The unchanged artifacts that matter are not every untouched file or record. The recurring constitutional unchanged set is narrower:

```text
The authority-bearing source and the negative boundary around the produced artifact must remain unchanged unless repository evidence explicitly moves them.
```

Examples:

- An inquiry note may be recorded, and an orientation view may be rendered, but the note must remain operator prose rather than projected truth, command, plan, authorization, or runtime instruction.
- A package fact may become candidate support, but the candidate must remain candidate support rather than verified capability, permission, policy approval, or execution authority.
- A binary path may become acquired verification evidence, but it must remain support rather than a `capability_verified` fact.
- A pressure audit may rank pressure and name a recommended inspection, but the pressure item must remain inspection guidance rather than implementation priority or command.
- A diagnostic or projection-shape report may expose read-only status, but that visibility must remain non-mutating and must not become cluster truth.

That is conservation-like only in the weak, characterization sense. The repository does not show one global conservation framework. It shows repeated local guards preserving distinctions while a transition creates a new view, support row, inspection row, projected read model, report, or document.

## Candidate conservation families

### Authority conservation

**What appears to change.** A surface emits an answer, report, inventory row, verification status, orientation view, or recommended inspection.

**What must not change.** The source of authority must not move from the implementation-backed source to the presentation artifact. Orientation must not become truth or command. Verification inspection must not create verification authority. Diagnostic visibility must not become mutation authority.

**Evidence.** `inquiry_orientation.py` states that rendering reads projected state but never mutates it, appends events, executes tools, or creates facts, goals, decisions, proposals, or plans. Its authority boundary says an inquiry note is not a fact, claim, requirement, authorization, command, or runtime instruction. `capability_verification.py` states verification status comes only from existing capability inventory backed by projected `capability_verified` facts. `projection_shape.py` declares its boundary as read-only, with no event-ledger writes and no cluster mutation.

**Mistake if changed silently.** Presentation output would impersonate repository authority: orientation would become command, candidate inspection would become admission, and diagnostic visibility would become operational permission.

**Enforced today or characterized only.** Partly implementation- and test-backed for the reviewed surfaces; report-only as a cross-family generalization.

### Evidence conservation

**What appears to change.** Evidence is reformatted into candidate rows, acquired verification evidence rows, verification inspections, fact support summaries, diagnostic report rows, or methodology citations.

**What must not change.** Support evidence must remain support evidence until an admitted fact or implementation-backed authority changes its status.

**Evidence.** `capability_candidates.py` builds candidates from projected `package_installed` facts and says candidates are not capability proof, permission, selection, planning, or execution. `verification_evidence.py` acquires local filesystem metadata and explicitly says it never runs binaries and never promotes evidence into `capability_verified` facts. Tests assert verification evidence boundary notes and candidate support preservation.

**Mistake if changed silently.** A support item would be treated as admission: package evidence or binary-path observation would become verified capability without a projected `capability_verified` fact.

**Enforced today or characterized only.** Implementation- and test-backed for capability candidates, verification evidence, and capability verification. Characterized more generally for methodology and reports.

### Boundary conservation

**What appears to change.** A bounded surface gains a rendered output, JSON shape, answer family, or diagnostic row.

**What must not change.** The subject boundary, mutation boundary, event-ledger boundary, and scope of the worker must remain intact unless implementation changes them and tests preserve the new behavior.

**Evidence.** `inquiry_artifacts.py` gives a read-only boundary with no recording, event-ledger writes, cluster mutation, inquiry graph creation, pressure transformation inference, workflow, or planning behavior. `projection_shape.py` similarly records `read_only`, `writes_event_ledger=false`, and `mutates_cluster=false`. The repository `AGENTS.md` requires new diagnostic surfaces to update inventory, shape-audit specs, and tests, and to prove diagnostic recording scope and non-mutation boundaries when applicable.

**Mistake if changed silently.** A diagnostic could become invisible or mutable without inventory/audit coverage; diagnostic-only findings could become cluster truth.

**Enforced today or characterized only.** Implementation- and test-backed for registered diagnostic/read-only surfaces. The cross-family boundary rule is methodological, with AGENTS.md operational instructions for diagnostic changes.

### Ownership conservation

**What appears to change.** A surface observes structure, source navigation, capability candidates, pressure, or responsibility-like evidence.

**What must not change.** Observation must not become ownership. Definition/import/source-navigation evidence must not become runtime ownership, behavior, or responsibility assignment unless separately evidenced.

**Evidence.** The transition artifact delta report characterizes implementation recovery as read-only recovery of implementation-backed facts that does not automatically become responsibility, ownership, or constitutional vocabulary. The competency reconciliation says locality and boundaries prevent local competencies from becoming universal planners, registries, gateways, or governance owners.

**Mistake if changed silently.** A visibility or structure artifact would assign responsibility or authority without implementation evidence.

**Enforced today or characterized only.** Partly implementation-backed in source/navigation and structure-observation surfaces; partly report-only in broader constitutional characterization.

### Fact conservation

**What appears to change.** Event replay produces projected state, read models, fact supports, relationships, aliases, graph issues, and current facts.

**What must not change.** Ledger history remains the source input; projection is the current read model over events, not an arbitrary source of new truth. Diagnostic-only and note-only outputs must not attach directly to hosts, services, filesystems, or runtime entities as truth unless the event/fact pipeline admits them.

**Evidence.** The artifact delta report says projection finalization creates current read models while source events remain append-only inputs. The AGENTS.md diagnostic recording boundary instructs diagnostic records to prefer `diagnostic_run:<id>` scoped subjects and not attach diagnostic-only findings directly to runtime entities unless explicitly changing that boundary.

**Mistake if changed silently.** Projection or diagnostic findings would be mistaken for source truth, and diagnostic findings could silently become cluster truth.

**Enforced today or characterized only.** Projection behavior is implementation-backed. The diagnostic recording boundary is an operational instruction and test obligation when surfaces are changed. The general phrase “fact conservation” remains only a characterization.

### Candidate conservation

**What appears to change.** Candidate rows are created from package facts; verification inspection can add a verification status column.

**What must not change.** A candidate must remain a candidate unless a projected verification fact exists. Candidate support, acquired evidence, and inspection status must not become selection, permission, or execution.

**Evidence.** `capability_candidates.py` marks candidate inspection as preservation only and includes boundary notes such as candidate-not-capability, not execution authority, not execution decision, no policy evaluation, and no tool execution. `capability_verification.py` says a package-observed candidate without a `capability_verified` fact remains unverified because candidate evidence is not verification authority. Tests assert candidate read-only behavior, verification inspection boundaries, and candidate-not-verified notes.

**Mistake if changed silently.** A candidate would be treated as verified or executable merely because it is visible or locally supported.

**Enforced today or characterized only.** Implementation- and test-backed.

### Orientation conservation

**What appears to change.** Raw operator prose is preserved as an inquiry note and may produce a related-material orientation view.

**What must not change.** The prose must remain a probe-local note, not a projected fact, goal, tool need, decision, proposal, plan, authorization, command, runtime instruction, ownership assertion, importance assertion, or next safe move.

**Evidence.** `inquiry_orientation.py` stores notes outside the event ledger and its boundary excludes facts, claims, requirements, capabilities, decisions, proposals, plans, authorizations, commands, runtime instructions, importance, ownership, intent, concern, recommended action, and next safe move. Tests prove recording an inquiry note does not change facts, observed/inferred facts, goals, tool needs, execution authorizations, proposals, pending actions, plans, handoff plans, or tools.

**Mistake if changed silently.** Operator prose would become repository truth or operational direction without admission.

**Enforced today or characterized only.** Implementation- and test-backed.

### Visibility conservation

**What appears to change.** A diagnostic, inventory, shape audit, projection shape, source-navigation match, candidate row, or orientation row becomes visible.

**What must not change.** Visibility must remain read-only unless the implementation and tests explicitly make it recordable or mutating. Visibility must not create authority, fact, permission, ownership, or priority.

**Evidence.** The diagnostic and projection-shape surfaces repeatedly carry `read_only`, `writes_event_ledger=false`, and `mutates_cluster=false`. The artifact delta report says diagnostic rows, inquiry-artifact rows, orientation related material, candidate rows, and source-navigation matches can become visible without creating projected facts or admitted authority.

**Mistake if changed silently.** A report row would be treated as law, truth, priority, or permission.

**Enforced today or characterized only.** Implementation- and test-backed for many individual surfaces; report-only as a cross-family wording.

### Operator testimony conservation

**What appears to change.** Operator-supplied prose can be preserved and investigated.

**What must not change.** Operator testimony must remain testimony, pressure, or orientation unless repository evidence admits it as a fact or authority-bearing artifact.

**Evidence.** Inquiry orientation preserves operator prose as a note but explicitly excludes fact, claim, command, plan, authorization, and runtime instruction. The implementation readiness characterization says operator pressure may start readiness investigation but cannot finish it.

**Mistake if changed silently.** Human testimony would become repository truth or command without evidence.

**Enforced today or characterized only.** Implementation- and test-backed for inquiry notes. Broader operator-testimony treatment remains methodology/report-only.

## Required distinctions

| Distinction | Preserved by | Evidence and current status |
| --- | --- | --- |
| Orientation != Truth | Implementation and tests | Inquiry notes are stored outside the event ledger and the orientation boundary excludes facts and claims; tests prove no projected-state change after note recording. |
| Visibility != Authority | Implementation, tests, diagnostics, and reports | Diagnostic/projection surfaces declare read-only/non-mutating boundaries; transition reports repeatedly characterize visibility as not knowledge or authority. |
| Support != Admission | Implementation and tests | Candidate and verification-evidence support is separate from `capability_verified` facts; verification status comes only from inventory/projected facts. |
| Candidate != Verified | Implementation and tests | Capability verification inspection keeps candidates unverified without inventory entries backed by projected verification facts. |
| Projection != Fact | Implementation and reports | Projection is a current read model over append-only events; reports characterize projection publication as visibility over replay/finalization, not arbitrary truth creation. |
| Pressure != Priority | Implementation and reports | Pressure audit ranks operational pressure and recommended inspections, while implementation readiness says pressure can start but not finish readiness. No global priority engine is evidenced. |
| Verification != Permission | Implementation and tests | Verification boundary notes say verified capability is not selection, execution authority, execution decision, tool invocation, or permission. |
| Recommendation != Command | Implementation and reports | Pressure audit emits `recommended_command`/`Recommended inspection`; tool resolution treats provider recommendations as catalog-derived advisory metadata. These are not commands or registered operations. |
| Operator testimony != Repository truth | Implementation, tests, and reports | Inquiry note preservation keeps raw prose outside projected runtime state; tests prove no facts/goals/actions are created. Broader treatment remains methodology/report-only. |

None of these distinctions is preserved only by operator memory in the reviewed core examples. Some are stronger than others: candidate/verification/orientation boundaries are test-backed; pressure/priority and recommendation/command are partly implementation-backed but more report-local as constitutional distinctions.

## Artifact delta review by transition family

### Communication to orientation

**Changed artifacts.** A probe-local `InquiryNoteRecord` can be appended to an isolated JSONL store, and an `InquiryOrientationView` can be rendered.

**Explicitly unchanged artifacts.** Event ledger, projected facts, observed/inferred facts, goals, tool needs, execution authorizations, execution proposals, pending actions, action plans, handoff plans, tools, authority, ownership, importance, recommended action, and next safe move.

**Was the unchanged set necessary?** Yes. Without it, the transition from communication to orientation would become admission, planning, or command.

### Visibility / diagnostics

**Changed artifacts.** Inventory rows, audit rows, JSON/text diagnostic output, and sometimes a diagnostic run record when explicitly supported.

**Explicitly unchanged artifacts.** Cluster mutation, event-ledger writes for read-only diagnostics, and source domain truth. Recordable diagnostics must preserve diagnostic-run scope unless intentionally different.

**Was the unchanged set necessary?** Yes. It prevents visibility from creating authority or cluster truth.

### Evidence acquisition

**Changed artifacts.** Transient verification-evidence rows may be produced from filesystem metadata.

**Explicitly unchanged artifacts.** Binaries are not invoked; `capability_verified` facts are not created; policy, execution, permission, proposals, and ledger event count remain unchanged.

**Was the unchanged set necessary?** Yes. Otherwise local support would become verification or permission.

### Candidate/support

**Changed artifacts.** Candidate records and support summaries are derived from package facts.

**Explicitly unchanged artifacts.** Package facts remain source support; candidates are not capability proof, permission, selection, planning, or execution.

**Was the unchanged set necessary?** Yes. It preserves support/admission and candidate/verified distinctions.

### Candidate to verified inspection

**Changed artifacts.** Verification inspection rows combine candidate support, acquired evidence, and inventory-derived status.

**Explicitly unchanged artifacts.** Candidate evidence remains candidate evidence; acquired evidence remains support; verification authority remains with existing inventory/projected `capability_verified` facts.

**Was the unchanged set necessary?** Yes. Otherwise inspection would manufacture authority.

### Admission

**Changed artifacts.** When a `capability_verified` fact exists in projected state, inventory can present admitted capability state.

**Explicitly unchanged artifacts.** Requests, tool contracts, candidates, acquired support, and inventory presentation do not become admission sources.

**Was the unchanged set necessary?** Yes. It keeps admission tied to projected fact authority.

### Fact projection

**Changed artifacts.** Projection creates current read models, fact supports, inferred partitions, relationships, aliases, conflicts, and graph issues.

**Explicitly unchanged artifacts.** Source ledger events remain the replay input; diagnostic-only and note-only findings remain outside cluster truth unless separately admitted.

**Was the unchanged set necessary?** Yes. It keeps projection from masquerading as source event creation.

### Implementation recovery

**Changed artifacts.** Source/navigation/structure rows may expose implementation facts or matches.

**Explicitly unchanged artifacts.** Source files, runtime behavior, ownership, responsibility, and authority remain unchanged unless separately evidenced.

**Was the unchanged set necessary?** Yes. It prevents observed structure from becoming ownership or capability authority.

### Methodology promotion / characterization

**Changed artifacts.** A repository document may preserve a characterization with evidence, unknowns, confidence, and lawful stop conditions.

**Explicitly unchanged artifacts.** Runtime behavior, state mutation boundaries, implementation ownership, diagnostic surfaces, and architectural vocabulary remain unchanged unless implementation evidence changes them.

**Was the unchanged set necessary?** Yes. Otherwise a report would create architecture.

## Negative analysis

The reviewed evidence supports these recurring failure modes if unchanged artifacts are silently treated as changed:

- Inquiry note treated as fact: directly contradicted by orientation implementation and tests.
- Inquiry note treated as command, authorization, plan, proposal, or next safe move: directly contradicted by the orientation authority boundary.
- Candidate treated as verified: directly contradicted by candidate and verification implementations.
- Candidate support or binary-path evidence treated as `capability_verified`: directly contradicted by verification-evidence implementation.
- Verification status treated as permission or execution authority: directly contradicted by verification boundary notes.
- Visibility row treated as authority or cluster mutation: contradicted by diagnostic/projection read-only boundaries.
- Pressure score treated as implementation priority: not supported by the pressure audit; implementation readiness keeps pressure separate from readiness.
- Recommended inspection treated as command: not supported by pressure audit or tool resolution; recommendation appears as advisory/inspection metadata.
- Projection treated as source truth: contradicted by the event-replay/read-model distinction in the transition delta report.
- Operator testimony treated as repository truth: contradicted by inquiry-note storage outside the ledger and no-state-change tests.

No additional failure is asserted here unless the reviewed files or tests supported it.

## Locality

The repository evidence does not earn a global constitutional law named conservation.

The current locality is:

- **Test-backed implementation boundaries:** inquiry orientation, capability candidates, verification evidence, capability verification, diagnostic/projection read-only surfaces, and some recommendation/handoff boundaries.
- **Family-local guards:** orientation/truth, candidate/verified, support/admission, visibility/authority, verification/permission, pressure/readiness.
- **Report-only methodology:** the cross-family phrasing that these are conservation-like constraints.
- **Operator memory:** not sufficient for the reviewed core distinctions. Where only memory would preserve a distinction, the repository instructions and prior methodology reports treat that as a weakness, not as authority.

Therefore the lawful formulation is:

```text
Conservation-like constraints are local boundary guards, not a single global conservation framework.
```

## Typed unknowns

These remain unknown and should not be resolved by metaphor:

| Unknown | Preserved uncertainty |
| --- | --- |
| Conservation conflict | No implementation evidence shows what happens when two preserved boundaries conflict. |
| Authority transfer | No generic rule shows when authority can transfer from one artifact class to another. Current examples require explicit projected facts, implementation evidence, or tests. |
| Evidence transformation | Support can be reformatted, but the repository has no general transformation calculus for when support becomes admission. |
| Boundary migration | A boundary can move only through implementation-backed change; no general migration rule is characterized here. |
| Ownership reassignment | Observation does not assign ownership, and no generic reassignment process is evidenced. |
| Fact supersession | Projection can rebuild current read models, but this report does not characterize a general fact-supersession law. |
| Rollback | No reviewed transition family establishes a general rollback rule for authority, facts, or admission. |
| Conservation label | The label itself remains a characterization aid, not stabilized repository vocabulary. |

## Smallest truthful answer

The smallest recurring constitutional thing that must remain unchanged is:

```text
the difference between the produced artifact and the authority-bearing artifact.
```

Even smaller:

```text
output is not authority.
```

That phrase is too broad if used as architecture, so the precise version is:

```text
A transition may produce a new output, view, support row, report, or characterization only if the repository evidence that grants truth, admission, permission, ownership, or command authority remains where implementation says it is.
```

If that unchanged authority location is not preserved, the transition is no longer lawful under the reviewed repository evidence.

## Lawful termination

This investigation stops at characterization. It does not create a conservation framework, runtime check, diagnostic surface, implementation recommendation, or new stable architecture vocabulary. It does not claim every unchanged artifact has constitutional meaning. It identifies only recurring unchanged distinctions already supported by implementation evidence, tests, diagnostics, reports, or repository instructions.

## Remaining questions

- Is there an implementation-backed need for a registry of preserved negative boundaries, or are existing local tests sufficient?
- Are pressure/recommendation boundaries strong enough in implementation, or mostly report-local?
- Should future diagnostic recording tests explicitly assert diagnostic-only subjects remain under `diagnostic_run:<id>` for every recordable read-only surface?
- Can projection/fact/supersession boundaries be characterized more precisely without creating a new framework?
- Are there transition families where an unchanged artifact is incidental rather than constitutional, and what evidence would distinguish that?

## Confidence

Confidence is **high** that the repository repeatedly preserves orientation/truth, support/admission, candidate/verified, visibility/authority, verification/permission, and operator-testimony/repository-truth distinctions in the reviewed surfaces.

Confidence is **medium** that pressure/priority and recommendation/command are preserved as constitutional distinctions, because implementation supports advisory and inspection wording but the broader distinction is more report-local.

Confidence is **low** that `conservation` should become stabilized architecture. The evidence supports local unchanged-boundary characterization, not a global conservation model.
