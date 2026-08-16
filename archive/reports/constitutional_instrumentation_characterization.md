# Constitutional Instrumentation Characterization

## Architectural question

Repository pressure currently looks less like scheduling and more like an instrument: it reports a bounded condition of the repository without deciding a next behavior. The question for this characterization is therefore:

> Has Seed independently recovered a broader family of constitutional instrumentation surfaces, or is pressure simply a particularly well-developed diagnostic?

This document treats repository implementation as authority. It does not investigate scheduling, planning, optimization, sensor frameworks, or behavioral selection.

## Method

Reviewed implementation and runtime evidence from:

- `seed --pressure-audit`
- `seed --diagnostic-inventory`
- `seed --diagnostic-shape-audit`
- `seed --integrity-summary`
- `seed --state-build`
- `seed --classification-coverage`
- `seed --graph-issue-summary`
- `seed --capability-needs`
- `seed --ownership-discrepancies`
- `seed --consumer-audit`
- `seed --knowledge-reachability-audit`
- diagnostic registry and pressure-audit implementation
- prior repository characterizations concerning pressure, purpose, diagnostics, responsibility, and runtime questions

The core test was whether a surface exposes a truthful bounded aspect of current condition while preserving read-only authority boundaries, rather than selecting behavior.

## Implementation evidence

### Diagnostic registry already encodes constitutional boundaries

`DiagnosticInventoryEntry` is not just a list of commands. It records whether a surface uses projected state, uses repository files, supports JSON, supports recording, emits diagnostic facts, emits cluster facts, writes the event ledger, mutates the cluster, or reads diagnostic facts. That shape is strong evidence that the repository treats diagnostic surfaces as bounded authority-bearing declarations, not merely formatter names.

The registry repeatedly declares `mutates_cluster=False` across diagnostic surfaces. Recordable surfaces distinguish diagnostic-run facts from cluster facts: `classification_coverage` supports recording, uses `record_scope="diagnostic_run"`, emits diagnostic facts, does not emit cluster facts, writes the event ledger, and still does not mutate the cluster.

This means the repository already separates:

```text
observation/reporting surface
from
cluster mutation / behavioral authority
```

### Diagnostic Shape Audit checks instruments against their declared shape

`seed --diagnostic-shape-audit` compares declared diagnostic properties with static implementation evidence. Its output is organized around fields such as record support, JSON support, record scope, diagnostic fact emission, event-ledger writes, projected-state use, repository-file use, and cluster mutation. In the current run, reviewed rows were consistent for these fields.

This is important because a diagnostic surface is not only output. It has a constitutional shape: what it may read, write, record, and mutate. The shape audit is itself an instrument about instrumentation health.

### Pressure Audit aggregates condition signals without command authority

`build_pressure_audit(...)` explicitly says it ranks operational pressure without planning, recording, or mutating state. The pressure implementation aggregates candidates from existing surfaces:

- diagnostic shape audit;
- ownership discrepancies;
- capability needs;
- consumer audit orphaned predicates;
- consumer audit fragile predicates.

The current pressure output reported orphaned predicates and fragile predicates. These are measurements about the repository's current architecture: unused observation predicates and single-consumer predicates. Pressure includes score and recommended inspection commands, but those commands route an operator to evidence. They are not execution plans.

The strongest counterweight is that the code sorts pressure items by score and category. That is prioritization-like presentation. However, the implementation stops at reporting and inspection. It does not select a slice, mutate state, invoke tools, open a plan, or decide runtime behavior.

### Recording boundary preserves diagnostic condition as diagnostic condition

The repository has explicit tests and registry fields around `record_scope="diagnostic_run"`, diagnostic facts, event-ledger writes, and `mutates_cluster=False`. This supports the user-provided boundary: diagnostic findings must not silently become cluster truth. A recorded diagnostic may become an event-ledger fact, but it remains scoped to a diagnostic run rather than attached directly to operational entities unless intentionally changed.

This is constitutional instrumentation evidence: the repository can preserve measurements without confusing them with the organism's truth or behavior.

### Other reviewed surfaces expose current condition

The reviewed surfaces mostly answer bounded condition questions:

- integrity summary: what projected-state support, contradictions, graph issues, and classification gaps exist now;
- state build: what current state summary and cache/build status exist now;
- classification coverage: which projected entities lack classification now;
- graph issue summary: what projected graph validation issues exist now;
- capability needs: which capabilities are missing for current diagnostics now;
- ownership discrepancies: where ownership attribution is ambiguous now;
- consumer audit: which predicates or surfaces lack consumers or have fragile consumption now;
- knowledge reachability: what knowledge is reachable across projected, repository, inquiry, and rendered surfaces now.

These surfaces can be operationally useful, but their implementation evidence primarily supports reporting condition. They do not themselves own behavior selection.

## Candidate instrumentation families

The repository does not equally support every candidate family. The following table characterizes current support.

| Candidate family | Support level | Implementation evidence | Characterization |
|---|---:|---|---|
| Repository Pressure | Strong | `pressure_audit` aggregates diagnostic shape, ownership, capability, orphaned predicate, and fragile predicate signals; read-only; no recording or mutation. | A well-developed condition instrument that reports architectural pressure and suggests inspection. |
| Repository Integrity | Strong | `integrity_summary`, graph issues, contradictions, unsupported facts, classification gaps. | Current-state integrity instrumentation is supported. |
| Capability Coverage | Strong | `capability_needs`, `classification_coverage`, capability status and candidates. | Exposes missing or insufficient current capabilities. |
| Architectural Drift | Medium | Diagnostic shape audit, architecture conformance audit, visibility coverage, operational surface classification audit. | Supported when drift means mismatch between declared/expected visibility shape and implementation. Not a general drift ontology. |
| Ownership Health | Strong | `ownership_discrepancies`, ownership authority surfaces, capability needs derived from ownership gaps. | Exposes ambiguous or unsupported ownership condition. |
| Consumer Health | Strong | `consumer_audit`, emitter-consumer audit, orphaned/fragile predicates consumed by pressure. | Exposes current consumption fragility. |
| Classification Health | Strong | `classification_coverage` and classification-related diagnostic facts. | Exposes current projected classification completeness. |
| Graph Health | Strong | `graph_issue_summary`, operational graph confidence/taxonomy surfaces. | Exposes projected graph validation and confidence condition. |
| Knowledge Reachability | Strong | `knowledge_reachability` reads projected state and repo files; audits reachability across surfaces. | Exposes what repository knowledge is reachable and where vocabulary may only be presentational. |
| Resource Usage | Medium-low | Environmental/runtime predicates such as process memory, thread count, runtime duration, SQLite database size appear, but current pressure reports some as orphaned. | Some measurements exist, but family support is not yet strongly consumed. |
| Environmental State | Medium | Local host, Prometheus, repository observation, current observations, listeners, mounts, systemd, users, groups. | Environmental observation exists; constitutional-instrumentation family status depends on consumer support. |
| Operator Activity | Medium-low | Inquiry notes, inquiry orientation, event history, audit snapshots, history brief. | The repository preserves operator-visible artifacts, but instrumentation family vocabulary is not fully earned. |

## Relationship to diagnostics

Instrumentation is not separate from diagnostics in the current implementation. It appears to be a characterization of a subset or role of diagnostics.

A diagnostic becomes instrument-like when it:

1. reports one bounded aspect of current condition;
2. declares and preserves read/write/mutation boundaries;
3. avoids behavioral selection;
4. can be checked against its declared shape;
5. can be recorded, if at all, as diagnostic-run scoped evidence rather than cluster truth;
6. may route the operator to further inspection without authorizing that inspection as a required next behavior.

Therefore, instrumentation is narrower than "all diagnostics" but not a new runtime layer. It is a constitutional interpretation of diagnostic surfaces whose authority is truthful bounded measurement.

## Relationship to pressure

Pressure is currently one of the strongest examples of instrumentation because it composes other condition surfaces into a bounded architectural pressure reading.

Pressure reports:

```text
current architecture has unresolved pressure here
because evidence says these boundaries or consumers are fragile, missing, ambiguous, or inconsistent
```

Pressure does not report:

```text
Seed must do this next
```

Pressure has recommended inspection commands. Those commands are bounded follow-up affordances, not behavioral authority. They are closer to a labeled knob or maintenance manual reference on an instrument panel than to an autopilot.

## Relationship to physiology

A useful separation is supported, but only as characterization:

```text
Instrumentation
  reports
Current Condition
  constrains and informs
Physiology
  reacts through existing lawful mechanisms
Behavior
  emerges
```

The repository supports this ordering only weakly-to-moderately as vocabulary. It strongly supports the first two links: instruments report condition. It also strongly supports that repository authority and implementation boundaries constrain behavior. It does not yet support a separate implementation layer called "constitutional instrumentation" or a formal physiology integration contract.

Instrumentation can legitimately influence physiology by changing what evidence is visible to existing mechanisms and operators. It should not direct physiology. Influence is lawful when it remains evidence, boundary, orientation, or inspection affordance.

## Relationship to behavior

Instrumentation is distinguished from behavior by authority.

Instrumentation:

- observes, audits, summarizes, compares, or explains;
- preserves provenance and scope;
- reports current condition;
- may expose confidence, unknowns, warnings, mismatches, and recommended inspection;
- does not mutate the cluster;
- does not select next work;
- does not execute remediation;
- does not transform diagnostic findings into cluster truth by default.

Behavior:

- changes state or environment;
- selects or executes an action;
- authorizes a transition;
- mutates cluster truth or operational reality;
- owns effects rather than only reporting evidence.

The repository repeatedly encodes this distinction with `mutates_cluster`, event-ledger, record-scope, and fact-emission fields.

## Required question answers

### 1. What distinguishes instrumentation from behavior?

Instrumentation reports bounded current condition under declared authority boundaries. Behavior selects, authorizes, executes, or mutates. The decisive distinction is not usefulness; it is authority over effects.

### 2. What distinguishes instrumentation from diagnostics?

Diagnostics are the current implementation category. Instrumentation is an architectural characterization of diagnostics that function as condition instruments. Not every diagnostic must be promoted to stable instrumentation vocabulary.

### 3. Does instrumentation merely expose current condition, or may it recommend bounded follow-up work?

It may recommend bounded follow-up inspection when the recommendation remains evidence-routing. Pressure's `recommended_command` is supported because it points to an inspection surface. It would cross the boundary if it selected implementation work, scheduled remediation, or treated the recommendation as command authority.

### 4. Should instrumentation ever possess authority?

Instrumentation should possess authority to report truthfully within its declared scope. It should not possess authority to decide behavior. Its authority is epistemic and constitutional, not executive.

### 5. Can instrumentation legitimately influence physiology without directing it?

Yes. Visibility can influence physiology by exposing condition, unknowns, mismatches, and boundaries that existing lawful mechanisms or operators may react to. The influence remains legitimate only while the instrument does not choose the reaction.

### 6. What relationship exists between Constitution, Current Condition, Instrumentation, Pressure, Physiology, and Behavior?

Supported characterization:

```text
Constitution
  defines lawful authority boundaries and repository values

Current Condition
  is the organism's present projected/repository/environmental state and architectural situation

Instrumentation
  truthfully reports bounded aspects of Current Condition under constitutional boundaries

Pressure
  is one strongly supported instrument reading about architectural strain or unresolved condition

Physiology
  is the organism's lawful internal machinery and constraints that may consume evidence

Behavior
  is the resulting selected or executed action/change, which instrumentation must not directly command
```

### 7. Does every instrument expose one bounded aspect of current reality?

That is the best supported characterization. Some instruments aggregate multiple inputs, as pressure does, but the output remains one bounded reading: current operational pressure. Aggregation does not make it behavior.

### 8. Has the repository earned instrumentation as stable architectural vocabulary, or is it still characterization?

The repository has earned **constitutional instrumentation** as a useful characterization, but not yet as a fully stabilized implementation vocabulary. The evidence supports saying that several diagnostic surfaces behave as instruments. It does not yet support introducing a new framework, registry, abstraction layer, or canonical ontology named instrumentation.

## Counterexamples and challenges

### Pressure might be prioritization

Evidence for: pressure items have scores and are sorted by descending score. The CLI help says it ranks current operational pressure.

Evidence against: the implementation does not plan, record, mutate, execute, or select work. It emits reasons and recommended inspection commands. Sorting is presentation of measurement severity, not behavioral selection.

Conclusion: pressure has prioritization-like presentation but not prioritization authority.

### Diagnostics might already completely explain the phenomenon

Evidence for: all reviewed surfaces already live in diagnostic/operational CLI architecture, and diagnostic inventory plus shape audit already provide the most concrete implementation vocabulary.

Evidence against: the recurring pattern is not merely "diagnostic exists"; it is "diagnostic reports bounded current condition under constitutional authority boundaries." That pattern is architecturally meaningful.

Conclusion: diagnostics remain the implementation category. Instrumentation is a higher-level characterization, not a replacement.

### Instrumentation might introduce unnecessary vocabulary

Evidence for: no `constitutional_instrumentation` implementation registry exists. Adding one would be premature.

Evidence against: pressure, integrity, ownership, graph, classification, consumer, capability, and reachability surfaces recur as condition readings rather than commands. The term names a real recurring shape.

Conclusion: vocabulary is useful in documents as characterization, but should not be stabilized into implementation without further evidence.

### Instrumentation might already perform behavioral selection

Evidence found: selection-path code can consume pressure candidates for selection explanation in its own surface, and pressure output is sorted.

Limiting evidence: pressure itself does not execute selection; selection-path is an audit/explanation surface, not an executor. The reviewed registry boundaries remain read-only.

Conclusion: no strong evidence was found that instrumentation itself performs behavioral selection.

### The altimeter analogy may overstate repository evidence

The analogy fits pressure's non-commanding report shape. It overstates the evidence if it implies a complete instrument panel architecture, an autopilot boundary, formal physiology coupling, or a stable instrumentation subsystem. The repository supports the analogy as explanation, not as architecture.

## Supported conclusions

1. Repository pressure does not tell Seed what to do.
2. Repository pressure truthfully reports one bounded aspect of current architectural condition.
3. Pressure is not isolated: many existing surfaces independently report bounded current condition under explicit authority boundaries.
4. The repository has recovered a broader family shape: constitutional instrumentation as condition-reporting diagnostics.
5. The family is strongest for pressure, integrity, capability coverage, ownership health, consumer health, classification health, graph health, and knowledge reachability.
6. Instrumentation may expose bounded follow-up inspection, but not command behavior.
7. Instrumentation has epistemic authority to report within scope, not executive authority to decide.
8. Diagnostics remain the concrete implementation vocabulary.
9. Constitutional instrumentation should remain a characterization until implementation evidence demands a new registry or abstraction.

## Unsupported interpretations

The repository does not support:

- pressure as scheduler;
- pressure as planner;
- pressure as optimizer;
- pressure as behavior selector;
- instrumentation as sensor framework;
- instrumentation as new implementation subsystem;
- instrumentation as authority to mutate cluster truth;
- recommended inspection as mandated next work;
- every diagnostic as automatically a constitutional instrument;
- every candidate family as equally earned;
- the aircraft panel analogy as more authoritative than repository evidence.

## Remaining unknowns

- Whether resource usage, environmental state, and operator activity will mature into strong instrumentation families or remain ordinary observations/audits.
- Whether future physiology-facing implementation will consume these condition readings in a way that requires formal contracts.
- Whether diagnostic inventory should eventually classify instrument-like surfaces, or whether that would introduce unnecessary vocabulary.
- Whether recommended inspection commands need a stricter boundary model if future surfaces add stronger guidance.
- Whether recorded diagnostic facts should gain richer lineage to preserve instrument readings over time without becoming cluster truth.

## Confidence

**Medium-high.**

Confidence is high that pressure itself is a read-only condition-reporting diagnostic rather than a behavioral selector. Confidence is also high that several diagnostic surfaces share this pattern. Confidence is lower that "constitutional instrumentation" should become stable repository vocabulary, because current implementation authority still names and enforces the concrete surfaces through diagnostic inventory, shape audit, and individual audit implementations rather than through an instrumentation subsystem.

The best current answer is:

> The repository has independently recovered a broader family shape of constitutional instrumentation, but only as an architectural characterization of condition-reporting diagnostics. Pressure is a particularly well-developed member of that family, not merely a one-off diagnostic; however, the family is not yet implementation-stabilized vocabulary.
