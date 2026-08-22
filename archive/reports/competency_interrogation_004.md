# Competency Interrogation 004

## Selected competency

**Pressure Audit**.

This interrogation selects Pressure Audit because it pressures the methodology more than Documentation Structure did: the implementation ranks operational pressure, is consumed by neighboring explanatory surfaces, and exposes recommended inspections while explicitly refusing planning, recording, and mutation. That makes it necessary to distinguish pressure from priority, selection, and authorization.

The selected competency is not a planner, scheduler, priority engine, or implementation authority. It is the read-only operational pressure audit implemented in `seed_runtime/pressure_audit.py` and registered as the `pressure_audit` diagnostic surface.

Smallest truthful answer:
Pressure Audit ranks implemented evidence of operational pressure from existing visibility surfaces; it does not command action.

## Implementation evidence reviewed

Implementation evidence reviewed in this interrogation:

- `seed_runtime/pressure_audit.py`
  - module purpose: read-only operational pressure audit aggregated from existing visibility surfaces;
  - `PressureItem`, `_PressureItemCandidate`, and `PressureAudit` record shapes;
  - `build_pressure_audit()` construction and score ordering;
  - pressure candidates for diagnostic shape, ownership attribution, capability needs, orphaned predicates, and fragile predicates;
  - `pressure_audit_json()` and `format_pressure_audit()` output;
  - recommended inspection commands attached to pressure rows.
- `seed_runtime/diagnostic_inventory.py`
  - `pressure_audit` diagnostic inventory entry;
  - `uses_projected_state=True` and `uses_repo_files=True`;
  - `supports_json=True`;
  - `supports_record=False`;
  - `record_scope="none"`;
  - `writes_event_ledger=False`;
  - `mutates_cluster=False`;
  - `reads_diagnostic_facts=True`.
- `seed_runtime/diagnostic_shape_audit.py`
  - `pressure_audit` implementation spec;
  - build, format, and JSON function names;
  - CLI flag coverage;
  - repository-file markers and diagnostic-fact read markers.
- `scripts/seed_local.py`
  - `--pressure-audit` CLI flag;
  - JSON and formatted output dispatch.
- `tests/test_pressure_audit.py`
  - public item shape preservation;
  - evidence-backed ranking;
  - CLI JSON and formatted rendering;
  - categories produced from existing surface evidence;
  - empty-state read-only behavior and event-ledger non-write proof.
- `seed_runtime/operational_story.py`
  - current operational story composes pressure evidence and may name a primary pressure without making Pressure Audit itself a planner.
- `seed_runtime/selection_path_audit.py`
  - selection-path explanation reads pressure ordering as selection evidence while documenting selection visibility separately from movement permission.
- App commands run for this interrogation:
  - `python scripts/seed_local.py --pressure-audit --json`
  - `python -m pytest -q tests/test_pressure_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

Smallest truthful answer:
The implementation evidence supports a registered diagnostic that reads state, repository files, and diagnostic-derived facts to produce scored pressure rows, JSON, and formatted output without recording or mutating.

## Interrogation matrix

Legend:

- ✓ Answered by implementation
- ? Partially supported / unanswered but meaningful
- ○ Not applicable at current maturity
- ✗ Unsupported / unknown

Question level legend:

- **Core** — needed for truthful bounded use of the competency now.
- **Advanced** — useful for mature public or multi-consumer governance, but not always required for this surface.
- **Evolutionary** — future split, simplification, or maturation question; absence is not automatically a failure.

### Identity

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What worker or implementation surface is being interrogated? | ✓ | The `pressure_audit` diagnostic surface is being interrogated: `build_pressure_audit()`, `pressure_audit_json()`, `format_pressure_audit()`, the `--pressure-audit` CLI flag, and the inventory/shape-audit registrations. |
| Core | What competency does that worker exercise? | ✓ | It exercises read-only operational pressure measurement and ordering from existing visibility surfaces. |
| Core | What constitutional role does this competency play in the organism? | ✓ | The smallest supported role is **current-condition orientation**: it orients Seed around observed operational pressure categories so a human or neighboring explanatory surface can inspect why pressure is visible. This wording is not stabilized vocabulary. |
| Core | What bounded responsibility does that competency own? | ✓ | It owns constructing scored `PressureItem` rows from diagnostic shape findings, ownership discrepancies, capability needs, orphaned predicates, and fragile predicates; sorting them by descending score and category; and rendering them as JSON or formatted diagnostic output. |
| Core | Does implementation distinguish worker, competency, and responsibility? | ✓ | Yes. The worker is the diagnostic implementation/CLI surface, the competency is pressure measurement and ordering, and the bounded responsibility is evidence-backed pressure-row construction and rendering. |
| Core | What is this competency incapable of doing? | ✓ | It cannot execute recommended inspections, repair mismatches, observe evidence outside its input audits, prove causal severity, persist diagnostic records, mutate cluster state, or independently decide work. |
| Core | What is this competency constitutionally forbidden from doing? | ✓ | It is forbidden from planning, recording facts, writing event-ledger entries, mutating cluster state, presenting pressure as implementation authorization, or treating score order as priority command. |
| Core | What does it explicitly refuse to own? | ✓ | The build function docstring refuses planning, recording, and state mutation. Inventory refuses record support, event-ledger writes, and cluster mutation. Tests prove empty-state invocation does not write events. |

Smallest truthful answer:
Pressure Audit is a current-condition orientation diagnostic for measuring and ordering operational pressure; it is incapable of acting and forbidden from authorizing action.

### Constitutional Authority

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Who may invoke this worker? | ✓ | Operators may invoke it through `seed --pressure-audit`; internal code and tests may invoke `build_pressure_audit()`, `pressure_audit_json()`, and `format_pressure_audit()`. |
| Core | Who may consume its artifacts? | ? | Operators, tests, JSON consumers, `operational_story`, `reasoning_path_audit`, and `selection_path_audit` consume or refer to pressure evidence. A complete consumer registry is not implemented. |
| Core | Who may trust this artifact? | ✓ | Operators and internal diagnostic/explanatory consumers may trust it only for pressure visibility derived from the audited inputs. |
| Core | What may be trusted? | ✓ | Category names, integer scores, evidence payloads, reasons, recommended inspection commands, sorted pressure ordering, empty-state reporting, JSON shape, and formatted rendering may be trusted as implemented diagnostic output. |
| Core | To what extent may it be trusted? | ✓ | It may be trusted as pressure measurement and pressure ordering only. Pressure is not priority. Pressure ordering is not selection authority. Recommended inspection is not movement permission. |
| Core | Under what assumptions does that trust remain lawful? | ✓ | Trust remains lawful only if the state and repository root are the intended inputs, the dependent audits are appropriate evidence sources, consumers preserve the read-only diagnostic boundary, and ranked pressure is used as inquiry orientation rather than command. |
| Core | What constitutional authority permits it to participate? | ✓ | Diagnostic inventory registers it as a JSON-capable diagnostic using projected state and repository files, reading diagnostic facts, not supporting record, not writing the event ledger, and not mutating the cluster. Shape audit names the implementation functions and markers. |
| Core | What constitutional constraints limit it? | ✓ | It is constrained to existing visibility surfaces, scored diagnostic rows, read-only output, no recording, no event-ledger writes, no cluster mutation, and no planning authority. |
| Advanced | What would be an unlawful expansion of responsibility? | ✓ | Treating top score as mandatory priority, automatically running recommended commands, creating action plans, recording cluster facts from pressure rows, mutating files/services, or selecting future work from pressure ordering alone would exceed authority. |

Smallest truthful answer:
Seed may trust Pressure Audit to expose pressure evidence and order it, but must refuse to treat that order as priority, selection, permission, or implementation authority.

### Preconditions

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What must already be true before this competency can answer honestly? | ✓ | A `State` must be supplied, a repository root must resolve or default, dependent visibility builders must be importable, and the question must be about pressure visible through implemented audits. |
| Core | Which preconditions are organism-level assumptions rather than observed evidence? | ✓ | The intended repository root, suitability of the state snapshot, operator choice to inspect pressure, and consumer discipline not to convert pressure into command are lawful-use assumptions, not observations emitted by Pressure Audit. |
| Core | Which preconditions are not guaranteed by the artifact itself? | ✓ | The artifact does not prove that the state is complete, that repository-file evidence is exhaustive, that scores represent severity, that recommended inspections will remain available, or that downstream consumers will preserve the boundary. |

Smallest truthful answer:
Pressure Audit assumes the selected state/root and dependent audit surfaces are the lawful evidence base; its output does not prove those assumptions.

### Evidence

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What evidence can this worker observe? | ✓ | It observes outputs from diagnostic shape audit, ownership discrepancies, capability needs, and consumer dependency audit. It can also observe the presence of `scripts/seed_local.py` to decide shape-audit root handling. |
| Core | What evidence can it preserve? | ✓ | It preserves category, score, evidence dictionary, reason, and recommended inspection command for each pressure item. JSON output preserves these fields directly. |
| Core | What evidence can it not observe? | ✓ | It cannot observe actual operator intent, future work priority, runtime effects of repairs, business impact, causal root cause, whether a recommended command should be run, or whether a pressure category should be selected for implementation. |
| Core | What evidence permits movement? | ✓ | Movement from dependent audit outputs to pressure rows is permitted by positive scores: mismatches/warnings/unknowns, conflict rows, capability need subject occurrences, orphaned predicates, and single-consumer predicates. |
| Core | What evidence causes lawful stop? | ✓ | Zero or absent evidence produces no pressure item. Formatting stops at summary and recommended inspection text. The competency does not execute commands, create plans, record facts, or mutate state. |

Smallest truthful answer:
Pressure Audit converts already-visible audit evidence into scored rows and stops before execution or promotion.

### Boundaries

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Where does this worker begin? | ✓ | It begins with a `State` and optional repository root, then calls implemented visibility builders. |
| Core | Where does it end? | ✓ | It ends at a `PressureAudit` record, JSON-compatible dictionary, or formatted diagnostic output. |
| Core | Which neighboring responsibilities does it deliberately avoid? | ✓ | It avoids repair, planning, selection authority, priority authority, execution, ledger recording, cluster mutation, repository mutation, causal analysis beyond reason text, and full consumer governance. |
| Core | How does implementation distinguish pressure, pressure measurement, pressure ordering, priority, and selection? | ? | Pressure is represented as a category with evidence. Pressure measurement is the integer score. Pressure ordering is sorting by descending score and category. Priority is not implemented. Selection is not owned by Pressure Audit, although selection/explanation surfaces may read the ordering as evidence. |
| Advanced | Which recurring implementation evidence supports those boundaries? | ✓ | The module docstring, build docstring, inventory entry, shape-audit spec, CLI dispatch, tests for read-only empty-state behavior, and neighboring selection/story surfaces repeat the diagnostic-read-only boundary. |

Smallest truthful answer:
Pressure Audit begins with implemented visibility inputs and ends with ordered pressure output; anything that acts on that output belongs elsewhere.

### Artifact Handoff

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What artifact leaves this worker? | ✓ | A `PressureAudit` containing ordered `PressureItem` records, formatted text, or JSON-compatible pressure rows leaves the worker. |
| Core | What minimum orientation survives? | ✓ | Each row preserves category, score, evidence, reason, and recommended inspection command. The overall output preserves order and pressure count. |
| Core | What provenance survives? | ? | Evidence values and command names survive. Full source-row provenance, timestamps, operator identity, dependent audit versions, and state snapshot identifiers do not survive in the pressure item shape. |
| Core | Who may consume the artifact? | ? | Operators, tests, JSON callers, operational story, reasoning path, and selection path surfaces may consume it. A complete downstream consumer registry is absent. |
| Core | What information is intentionally excluded? | ✓ | Action authorization, execution result, repair plan, priority status, selection mandate, cluster fact promotion, event-ledger record, and mutation effect are excluded. |

Smallest truthful answer:
The handoff artifact is an ordered diagnostic pressure report, not an executable plan.

### Unknown / Stop

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What can remain unknown? | ✓ | Whether the highest pressure is most urgent, whether a recommended inspection should run, whether a pressure item reflects root cause, whether a repair is safe, whether future work should select it, and whether consumers preserve the boundary can remain unknown. |
| Core | What unsupported conclusions are refused? | ✓ | A higher score does not prove priority. A recommended command does not authorize movement. A category does not prove root cause. A pressure row does not prove cluster truth. Empty output does not prove the organism has no problems. |
| Core | How does the competency stop honestly? | ✓ | It emits only pressure rows supported by current dependent evidence or a zero-pressure summary, then stops before planning, selection authority, recording, or mutation. |
| Advanced | Which unanswered questions reveal real gaps? | ? | Complete consumer mapping, richer provenance, score calibration semantics, downstream boundary enforcement, and whether recommended commands remain current are real gaps for automated reliance. |
| Evolutionary | Which unanswered questions are inappropriate for this maturity level? | ○ | Requiring business priority, repair execution, planner authority, or autonomous work selection from this diagnostic is maturity-inappropriate because those belong to different competencies. |

Smallest truthful answer:
Pressure Audit may lawfully stop at pressure visibility even when urgency, root cause, and next action remain unknown.

### Locality

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Why is this competency local? | ✓ | It is local because it aggregates a fixed set of implemented Seed visibility surfaces into pressure rows. |
| Core | Why has implementation rejected universal ownership? | ✓ | It delegates evidence to existing audits and exposes recommended inspections instead of owning their domains or repairs. Inventory and tests preserve non-recording/non-mutating limits. |
| Advanced | What would fail if this competency became universal? | ✓ | It would conflate evidence aggregation with planning, root-cause analysis, selection, priority, execution, and truth promotion. Scores would become overclaimed as authority rather than orientation. |

Smallest truthful answer:
Pressure Audit is local to implemented pressure categories and should not be generalized into universal prioritization.

### Continuity

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What public compatibility contract exists? | ✓ | The public contract includes `--pressure-audit`, JSON support, formatted output, `PressureItem` JSON shape, diagnostic inventory registration, and diagnostic shape-audit implementation spec. |
| Core | What internal implementation freedom remains? | ✓ | Internals may change if they preserve registered CLI/JSON/format behavior, evidence-backed row shape, read-only boundary, no record support, no event-ledger writes, no cluster mutation, and diagnostic-shape visibility. |
| Core | What identity survives implementation evolution? | ✓ | Read-only pressure measurement and ordering from existing visibility surfaces survives. Planning, priority, selection authority, execution, and mutation remain outside identity. |
| Advanced | How is compatibility drift detected today? | ✓ | Drift is detected by pressure-audit tests plus diagnostic inventory and shape-audit tests. |

Smallest truthful answer:
The stable contract is a visible read-only pressure diagnostic with JSON/format output and drift-audit registration.

### Self-Observation / Drift

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | How can this competency be audited? | ✓ | It can be audited through `seed --pressure-audit`, `seed --diagnostic-inventory`, `seed --diagnostic-shape-audit`, and the pressure-audit unit tests. |
| Advanced | How is drift detected today? | ✓ | Diagnostic inventory and shape-audit registrations check the operational surface, while unit tests check pressure item shape, ranking, category generation, rendering, JSON output, and read-only empty-state behavior. |
| Advanced | What diagnostic evidence already exists? | ✓ | Inventory registration, CLI flag, JSON support, `supports_record=False`, `record_scope=none`, `writes_event_ledger=False`, `mutates_cluster=False`, shape-audit function markers, repository-file markers, and diagnostic-fact read markers exist. |
| Advanced | What important self-observation remains absent? | ? | Full score calibration explanation, dependent row provenance, complete consumer registry, invocation timestamp, and proof that every consumer preserves non-selection authority remain absent. |

Smallest truthful answer:
Pressure Audit is self-visible as a diagnostic surface, but not fully provenance-rich or consumer-governed.

### Evolution

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Evolutionary | Why did this competency emerge? | ? | Current implementation shows a need to aggregate multiple visibility surfaces into a single pressure view, but code alone does not fully prove historical causality. |
| Evolutionary | What architectural pressure produced it? | ? | Implementation suggests pressure to orient inquiry across shape, ownership, capability, and predicate-consumer gaps without granting planning or mutation authority. This is partly implementation-backed and partly inferred from code structure. |
| Evolutionary | What future evidence could split it? | ✓ | Independent governance for score calibration, category-specific pressure builders, recommended-inspection validation, or consumer handoff could justify smaller competencies. |
| Evolutionary | What future evidence could simplify it? | ✓ | If consumers stop needing one or more categories, those pressure candidates could remain internal details or be removed without changing the core read-only pressure competency. |

Smallest truthful answer:
The evolutionary evidence supports aggregation pressure, not a mature theory of prioritization.

## Recurring implementation evidence

Recurring evidence supports the same bounded conclusion:

1. **The module declares read-only pressure aggregation.** Pressure Audit is expressly aggregated from existing visibility surfaces and its builder refuses planning, recording, and state mutation.
2. **The public shape is pressure-oriented, not action-oriented.** `PressureItem` contains category, score, evidence, reason, and recommended inspection, but no selected action, priority state, execution result, or mutation record.
3. **The ranking is mechanical.** Pressure rows are sorted by descending score and category. The sort creates presentation order; it does not create constitutional priority.
4. **The diagnostic inventory makes the operational boundary visible.** The entry allows JSON, reads state/repository/diagnostic facts, but refuses record support, event-ledger writes, and cluster mutation.
5. **The shape audit preserves implementation visibility.** The spec names the module, build/format/JSON functions, CLI flag, repository-file markers, and diagnostic-fact read markers.
6. **Tests prove visible behavior and read-only limits.** Tests cover row shape, ranking, categories, CLI rendering, JSON rendering, and no ledger writes in an empty-state diagnostic run.
7. **Neighboring surfaces consume pressure without making Pressure Audit a planner.** Operational Story and Selection Path can use pressure evidence to explain current focus or selection lineage, but their existence proves handoff pressure rather than Pressure Audit authority.
8. **Actual app output remains pressure-only.** The app command returned `Orphaned Predicates` and `Fragile Predicates` with scores, evidence, reasons, and recommended inspections; it did not select, execute, record, or mutate.

Smallest truthful answer:
Every recurring implementation signal supports pressure visibility and pressure ordering; none supports command authority.

## Constitutional observations

Pressure Audit can answer a bounded constitutional oral examination:

- **What worker/surface is being interrogated?** The registered `pressure_audit` diagnostic surface.
- **What competency does it exercise?** Read-only pressure measurement and ordering from existing visibility surfaces.
- **What constitutional role does it play?** Current-condition orientation, if that phrase remains a provisional label rather than stabilized vocabulary.
- **What bounded responsibility does it own?** Constructing and rendering ordered pressure rows from specific dependent audits.
- **What can Seed trust it for?** Seed can trust category, score, evidence, reason, recommendation text, and mechanical ordering as diagnostic pressure output.
- **What must Seed refuse to infer from it?** Seed must refuse priority, selection mandate, movement permission, implementation authorization, root-cause proof, cluster truth, event-ledger truth, and repair safety.
- **What assumptions must already hold?** The chosen state/root and dependent audits must be the intended evidence base, and consumers must keep pressure as orientation.
- **Which gaps are real?** Consumer completeness, provenance richness, score calibration semantics, recommendation-currentness, and downstream boundary enforcement are real gaps for stronger automated reliance.
- **Which gaps are maturity-inappropriate?** Planner authority, autonomous repair, business priority, and universal root-cause analysis are inappropriate demands for this diagnostic.

Smallest truthful answer:
Seed can truthfully explain Pressure Audit as read-only current-condition pressure orientation and must refuse all inference from pressure to command.

## Unsupported answers

The following answers remain unsupported or only partially supported:

- A complete list of all legitimate downstream consumers of Pressure Audit output.
- Proof that every downstream consumer preserves the distinction between pressure order and selection authority.
- Full row-level provenance from dependent audits into every pressure item.
- Timestamp, operator identity, state snapshot identity, or dependent audit version in the pressure artifact.
- Calibration proof that one score point in one category is commensurate with one score point in another category.
- Proof that a recommended inspection is the best next command.
- Proof that high score means high priority, high urgency, high impact, or root cause.
- Proof that empty pressure output means the repository has no operational problems.
- Full implementation-only history of why the diagnostic emerged.

Smallest truthful answer:
The unsupported answers mostly concern over-reliance: provenance, calibration, consumers, and conversion from pressure to action.

## Unanswered question classification

| Unanswered / partial question | Classification | Why |
| --- | --- | --- |
| Complete consumer map | consumer gap | Known consumers exist, but no exhaustive consumer registry was found. |
| Downstream preservation of pressure/priority/selection distinctions | handoff gap | Neighboring surfaces consume pressure evidence; implementation does not prove all consumers preserve the constitutional boundary. |
| Full dependent-row provenance | handoff gap | Pressure rows preserve summarized evidence, not complete source rows or derivation traces. |
| Invocation timestamp/operator/state snapshot identity | handoff gap | The artifact is pressure-oriented and omits full invocation provenance. |
| Score commensurability across categories | calibration gap | Scores are category-specific counts or sums; implementation does not prove cross-category severity equivalence. |
| Whether recommended inspection is the best next command | authority gap | Recommended command text identifies an inspection surface, not permission or priority. |
| Whether top pressure is urgent or highest impact | authority gap | Pressure ordering is implemented; urgency and impact authority are not. |
| Whether pressure should drive future work selection | frontier | Selection/explanation may read pressure, but Pressure Audit does not own work selection. |
| Whether historical emergence is fully known from code | implementation gap | Current code proves present boundary better than historical causality. |
| Whether pressure category labels are repository knowledge | presentation-only | Labels orient diagnostic output; they do not stabilize ontology or constitutional vocabulary by themselves. |

Smallest truthful answer:
The typed unknowns show real handoff/calibration gaps while rejecting planner demands as outside this competency.

## Constitutional oral examination

If Seed were asked to explain Pressure Audit, he could answer truthfully only in bounded terms.

| Answer class | Result |
| --- | --- |
| Unknown | Complete consumer map; score commensurability; full dependent-row provenance; invocation timestamp/operator/state identity; downstream boundary preservation; full historical emergence. |
| Unsupported | Any claim that pressure score equals priority, that pressure order equals selection, that a recommended inspection authorizes movement, that pressure proves root cause, or that the diagnostic records facts, writes events, mutates cluster state, repairs issues, or executes commands. |
| Operator-only | Choice to invoke Pressure Audit, the intended repository root, and intended state snapshot are lawful-use assumptions, not pressure findings. |
| Presentation vocabulary | Category labels, score labels, and `Recommended inspection` text orient output; they do not create stable constitutional vocabulary, priority, or command authority. |
| Implementation-backed | Read-only pressure aggregation; five implemented pressure candidate families; positive-score filtering; descending score/category ordering; JSON/formatted output; diagnostic inventory and shape-audit visibility; no record support; `record_scope=none`; no event-ledger writes; no cluster mutation. |

Smallest truthful answer:
The oral exam can preserve implementation-backed pressure facts only by refusing action, priority, and selection claims.

## Constitutional reliance

Seed may rely on this competency to:

- expose operational pressure visible through implemented audit inputs;
- produce category, score, evidence, reason, and recommended-inspection rows;
- mechanically order pressure rows by descending score and category;
- render pressure diagnostics as text or JSON;
- appear in diagnostic inventory and diagnostic shape audit;
- remain read-only, non-recording, non-event-writing, and non-cluster-mutating.

Seed may rely on it only to this extent:

- as inquiry orientation and pressure visibility;
- as evidence that a dependent audit reported countable findings;
- as a prompt to inspect, not as permission to act.

Seed must not rely on this competency to:

- establish priority;
- select future work;
- authorize movement;
- execute recommended inspections;
- prove causal root cause;
- prove business or operational impact;
- promote diagnostic-only pressure into cluster truth;
- write events or mutate the cluster;
- stabilize pressure category labels as repository knowledge.

Assumptions that must already hold:

- the supplied `State` is the intended state evidence;
- the repository root is the intended repository evidence;
- dependent audit builders are the intended visibility surfaces;
- consumers preserve the distinction between pressure, pressure measurement, pressure ordering, priority, and selection;
- recommended commands are treated as inspection references, not commands to run automatically.

Smallest truthful answer:
Seed may rely on Pressure Audit for bounded inquiry orientation from implemented pressure evidence, and must refuse to rely on it for priority or action.

## Methodology audit

**Which questions produced the most constitutional insight?**

The most useful questions were the new refusal split and the required pressure distinction. Separating incapability from prohibition showed that Pressure Audit is both unable to repair/execute and constitutionally forbidden from converting pressure into authorization. Distinguishing pressure, measurement, ordering, priority, and selection prevented the score sort from being overclaimed.

**Which questions produced weak, repetitive, or low-value answers?**

Several continuity and self-observation questions repeated inventory/shape-audit facts already established in implementation evidence. They remained useful as safeguards but produced less new insight than authority and handoff questions.

**Which questions may be asking two things at once?**

"Who may trust this artifact?" can mix consumer identity with trust extent. It is clearer when split into who may consume, what may be trusted, to what extent, and under what assumptions. "What evidence permits movement?" can also blur internal movement from input evidence to output rows with external movement toward action; Pressure Audit shows those must remain separate.

**Did any new constitutional question emerge?**

Yes: when a diagnostic emits a recommended command, the interrogation should ask whether the command is an inspection reference, a movement permission, or an execution request. For Pressure Audit, it is only an inspection reference.

**Should any existing question be reduced rather than expanded?**

Yes. For mature diagnostic surfaces, repeated inventory/shape-audit questions could be reduced to a single visibility-contract row unless the task concerns diagnostic registration itself. More attention should go to handoff authority and overclaim risk.

**Did the interrogation discipline change?**

**Meaningful refinement.**

The discipline changed by adding constitutional role, splitting incapability from prohibition, adding smallest-truthful-answer notes for every major section, and auditing the methodology before termination. The largest substantive refinement is the explicit separation between diagnostic orientation and action authority.

Smallest truthful answer:
This pass meaningfully refined the interrogation discipline by tightening refusal, role, and overclaim controls, not by stabilizing new vocabulary.

## Methodology honesty candidates

The following are preserved only as candidates. They are not stabilized repository knowledge.

- Competency Interrogation appears to recover constitutional trust boundaries.
- Typed unknowns preserve more honest uncertainty than generic unknowns.
- Some questions may be maturity-stage-specific rather than universally required.
- Lawful stops are becoming more precise than project-management statuses.
- Stable questions may matter more than stable vocabulary.
- Diagnostics that emit recommendations may require an explicit distinction between inspection reference, movement permission, and execution request.

Smallest truthful answer:
The recurring honesty candidates are methodological watchpoints, not claims promoted into Seed knowledge.

## Lawful termination

**Pressure boundary characterized; command boundary preserved.**

This interrogation can lawfully stop after characterizing Pressure Audit as a visible, tested, read-only pressure-orientation diagnostic. The repository supports trusting the surface for pressure measurement and ordering from implemented visibility inputs. It does not support trusting it for priority, selection, movement permission, repair, execution, event-ledger truth, repository mutation, or cluster mutation.

The lawful stop is not to reconcile Competency Interrogation 001, not to redesign pressure scoring, and not to turn recommended inspections into action. No operational surface was changed. The smallest lawful stop is to preserve the constitutional boundary and typed gaps for future work if repository authority later requires stronger provenance, score calibration, or consumer governance.

Smallest truthful answer:
Stop at boundary characterization: Pressure Audit can orient inquiry, not command behavior.

## Remaining questions

- Should pressure scores ever receive explicit calibration semantics, or should they remain local count-based measurements?
- Should recommended inspection commands carry machine-readable boundary metadata stating that they are not movement permission?
- Should pressure rows preserve source-row provenance from dependent audits?
- Should downstream consumers of pressure output be registered or audited for pressure/priority/selection overclaim?
- Should Operational Story and Selection Path carry explicit language distinguishing pressure order from action authority wherever they consume Pressure Audit?
- Should empty pressure output include a stronger caveat that no current pressure was found by the implemented inputs only?

Smallest truthful answer:
The remaining questions are handoff and calibration questions, not blockers to explaining the current competency truthfully.

## Confidence

**Moderate-high.**

Confidence is high that Pressure Audit is a read-only, visible, tested pressure diagnostic with no record, event-ledger, or cluster-mutation authority. Confidence is moderate rather than absolute because complete consumer mapping, provenance richness, score calibration, and downstream boundary preservation are not fully implemented.

Acceptance answers:

- **Can Seed truthfully explain this competency?** Yes, as read-only pressure measurement and ordering from implemented visibility surfaces.
- **What is the smallest truthful constitutional role of this competency?** Current-condition orientation.
- **What can Seed trust it for?** Category, score, evidence, reason, recommended inspection text, and mechanical ordering as diagnostic pressure output.
- **What must Seed refuse to infer from it?** Priority, selection, movement permission, implementation authorization, root cause, repair safety, event-ledger truth, cluster truth, or mutation authority.
- **What assumptions must already hold?** Intended state/root inputs, valid dependent visibility surfaces, and disciplined consumers that keep pressure as orientation.
- **Which unknowns are typed?** Consumer, handoff, calibration, authority, frontier, implementation, and presentation-only unknowns.
- **Which gaps are real?** Consumer mapping, provenance, calibration, recommendation-currentness, and downstream boundary enforcement.
- **Which gaps are maturity-inappropriate?** Planner authority, autonomous repair, universal prioritization, business impact proof, and work selection authority.
- **Did the interrogation methodology itself change?** Yes; meaningful refinement.
- **What lawful stop does the repository support?** Boundary characterized; pressure may orient inquiry, not command behavior.

Smallest truthful answer:
Confidence is sufficient for a bounded explanation and insufficient for converting pressure into autonomous priority or action.
