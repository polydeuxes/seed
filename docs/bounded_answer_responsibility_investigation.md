# Bounded Answer Responsibility Investigation

## Scope

This is an implementation-backed investigation only. It does not propose a new registry, schema, runtime layer, metadata framework, answer engine, router, or planner.

The question is narrow:

> What is the minimum implementation-backed evidence that a surface owns a bounded answer responsibility?

Repository authority wins. Existing implementation, tests, and prior investigations are treated as evidence only where they identify behavior that is actually present in code.

## Working distinction

A surface owns **mechanical responsibility** when implementation evidence says what it can consume, emit, record, mutate, format, or expose operationally.

A surface owns **bounded answer responsibility** when implementation evidence additionally shows that the surface takes responsibility for a specific operator question or semantic conclusion while preserving the limits of that answer.

The difference is not a new object boundary. It is a responsibility boundary:

```text
mechanical responsibility
  = what the surface does and what it may affect

bounded answer responsibility
  = what question the surface answers, from which authorities,
    with which uncertainty and negative authority preserved
```

## Vocabulary distinctions

### View

A view is a read-oriented presentation of existing data. A view may be answer-responsible, but only if implementation evidence shows bounded question ownership. `SourceNavigationView` is a view that can answer a narrow source-location question because its builder selects preserved `defines` and `imports` facts for a query and its module explicitly refuses file inspection, parsing, ingestion, behavior inference, reachability inference, and ownership inference.

### Lookup

A lookup returns matching material for a key or query. A lookup does not become answer-responsible merely because it finds rows. It becomes answer-responsible only when the match semantics and non-authority are implementation-bounded. Source Navigation is a lookup-like surface with bounded answer responsibility for source-fact navigation, but not for behavioral explanation.

### Inventory

An inventory enumerates surfaces or capabilities. Diagnostic Inventory is primarily mechanical self-knowledge: CLI flags, projected-state use, repository-file use, JSON support, record support, record scope, diagnostic-fact emission, cluster-fact emission, event-ledger writes, cluster mutation, diagnostic-fact reads, and a description. Its descriptions can approximate answer responsibility, but the implemented dataclass is a mechanical surface contract rather than an answer contract.

### Summary

A summary aggregates existing signals into a compact representation. A summary can be purely mechanical aggregation or answer-responsible composition. Projection Integrity Summary is answer-responsible because it aggregates existing integrity signals and carries explicit caveats that those counts are integrity signals rather than truth, correctness, health, execution, repair, or provider-availability decisions.

### Audit

An audit checks or traces a bounded concern. Diagnostic Shape Audit is mechanical: it compares declared diagnostic fields against implementation markers. Reasoning Path Audit and Selection Path Audit are semantic audits: they expose derivation or selection evidence, unknowns, consumers, outcomes, and read-only boundaries.

### Diagnostic

A diagnostic is an operational visibility surface. It may be mechanical-only, answer-responsible, or both. Diagnostic status alone does not imply answer responsibility. The relevant evidence is whether the diagnostic implements a question, authorities, selection/composition logic, uncertainty, and negative authority.

### Navigation surface

A navigation surface helps an operator move from a question to repository-backed material. Navigation alone is not answer composition. Source Navigation owns a bounded answer only for source-fact navigation because its selection rules and refusal boundaries are implemented.

### Answer composition

Answer composition is a surface behavior in which existing authorities are selected, joined, derived, or organized into an answer with preserved boundaries. It is not currently proven as a separate architectural object. Operational Story is the clearest implemented answer composition because it composes multiple existing visibility surfaces into current focus, pressure, evidence, capabilities, constraints, gaps, impact, investigation path, unknowns, and boundary.

## Minimum evidence requirement

A surface owns bounded answer responsibility only when implementation evidence shows all of the following:

1. **A bounded answer target.** The code shape, formatter, CLI behavior, or tests identify what kind of question the surface answers. The target may be implicit in field names and formatting, but it must be narrower than "render some data".
2. **Consumed authorities.** The builder must reveal which projected state, repository files, diagnostics, inventories, or preserved records are consumed.
3. **Selection, aggregation, composition, or derivation logic.** The surface must do more than pass through data; it must choose, group, order, join, derive, or otherwise shape material in service of the answer target.
4. **Preserved uncertainty or incompleteness.** The output shape or formatter must expose unknowns, caveats, absence semantics, incomplete status, or equivalent uncertainty preservation when evidence is missing or limited.
5. **Negative authority.** The surface must explicitly state what it does not do or does not prove, especially around truth, intent, planning, recording, event-ledger writes, cluster mutation, behavioral inference, or source-of-truth promotion.
6. **Testable or inspectable boundary.** The responsibility must be traceable to implementation artifacts such as dataclasses, builder functions, formatter text, diagnostic inventory entries, shape-audit specs, or tests.

These conditions are jointly sufficient for the local investigation label "bounded answer responsibility." None is individually sufficient.

They are not proposed as a new schema. They are a reading discipline for existing implementation evidence.

## Candidate answer-responsible surfaces

### Operational Story

Operational Story is the strongest candidate.

Implementation evidence:

- Its module docstring identifies it as a read-only operational story view composed from existing visibility surfaces.
- `build_operational_story` consumes Pressure Audit, Capability Needs, Privilege Discovery, Correlation Audit, Impact Audit, and Investigation Path Audit.
- The returned dataclass carries focus, pressure, supporting evidence, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes, investigation path, unknowns, and boundary.
- Unknowns are explicitly populated for missing pressure, missing capability needs, and unknown impact.
- Boundary fields state read-only view, no fact recording, no event-ledger writes, and no cluster mutation.
- The formatter states that it provides no recording, event-ledger writes, cluster mutation, plans, or implementation advice.

Determination: **bounded answer responsibility**.

Bounded question:

```text
What current operational story is supported by existing visibility surfaces?
```

It remains bounded because it does not claim operational truth, plan action, execute tools, record facts, or mutate the cluster.

### Projection Integrity Summary

Projection Integrity Summary is a bounded answer-responsible summary.

Implementation evidence:

- Its module docstring says it is a read-only composition over existing projected State integrity signals.
- The builder consumes evidence summaries, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, and capability inventory.
- The dataclass aggregates integrity counts and caveats.
- Default caveats explicitly say integrity signals are not truth or correctness judgments, that unsupported/unverified/stale/contradicted/missing evidence does not mean false, and that refresh recommendations execute no refresh or verification.

Determination: **bounded answer responsibility**.

Bounded question:

```text
What aggregate integrity caveats and counts are visible in projected State?
```

It remains bounded because it does not verify, refresh, repair, resolve contradictions, call providers, create facts, create evidence, or mutate projected State.

### Inquiry Orientation

Inquiry Orientation is a bounded answer-responsible orientation surface.

Implementation evidence:

- Inquiry notes are preserved outside the event ledger and are evidence for the probe only.
- The builder tokenizes a preserved inquiry note, performs deterministic lexical overlap against fact supports and Source Navigation matches, limits related material, and returns uncertainty plus authority boundary.
- It preserves uncertainty both when matches exist and when no matches exist.
- Its authority boundary says the inquiry note is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction; matches do not assert importance, ownership, intent, concern, recommended action, or next safe move.

Determination: **bounded answer responsibility**.

Bounded question:

```text
What already-projected material is deterministically related to this preserved inquiry note?
```

It remains bounded because lexical overlap is not semantic interpretation and absence of overlap is not proof of unrelatedness.

### Source Navigation

Source Navigation is a narrow answer-responsible navigation/lookup surface.

Implementation evidence:

- Its module docstring states that it projects only existing `imports` and `defines` facts from State.
- `SOURCE_PREDICATES` restricts the authority to `defines` and `imports`.
- `build_source_navigation` matches a query syntactically against support subjects, paths, qualified definition values, and final dotted segments.
- The formatter reports no matches rather than implying absence of source reality.
- The module explicitly refuses file inspection, source parsing, observation ingestion, and behavior/reachability/ownership inference.

Determination: **bounded answer responsibility, but very narrow**.

Bounded question:

```text
Which preserved source facts define or import the queried symbol, module, or path?
```

It remains bounded because it does not answer ownership, behavior, reachability, runtime status, or whether source files currently contain the symbol.

### Reasoning Path Audit

Reasoning Path Audit is answer-responsible for implemented derivation visibility.

Implementation evidence:

- Its module docstring identifies read-only evidence-backed derivation paths for operational conclusions.
- The builder consumes ownership discrepancies, capability needs, pressure audit, privilege discovery, and Operational Story.
- It separates observed evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and boundary.
- It emits an explicit incomplete title when unknowns exist.
- Its boundary states no recording, no event-ledger writes, and no cluster mutation.

Determination: **bounded answer responsibility**.

Bounded question:

```text
What implemented evidence path connects this subject/domain to operational conclusions and consumers?
```

It remains bounded because it only uses implemented diagnostic surfaces and reports unknown derivation when no evidence is available.

### Selection Path Audit

Selection Path Audit is answer-responsible for implemented selection visibility.

Implementation evidence:

- Its module docstring identifies read-only selection trace visibility for operational conclusions.
- The builder consumes Pressure Audit and Operational Story.
- For implemented targets, it exposes selected item, candidate set, selection factors, non-selected alternatives, evidence, outcome, unknowns, and boundary.
- For unknown targets, it explicitly reports `selected="unknown"` and says the target is not an implemented selection surface.
- Its boundary states no recording, no event-ledger writes, and no cluster mutation.

Determination: **bounded answer responsibility**.

Bounded question:

```text
Why was this implemented operational candidate selected over other candidates?
```

It remains bounded because it does not generalize to arbitrary selection surfaces and reports unknown selection logic when the target lacks implemented evidence.

## Candidate mechanical-only or primarily mechanical surfaces

### Diagnostic Inventory

Diagnostic Inventory is primarily mechanical self-knowledge.

It owns mechanical responsibility because its entry shape declares CLI flags, input classes, JSON support, record support, record scope, diagnostic-fact behavior, cluster-fact behavior, event-ledger behavior, mutation behavior, diagnostic-fact reads, and descriptions.

It does not consistently own bounded answer responsibility because the implemented fields do not require question family, uncertainty preservation, consumed semantic authority, negative authority, or adjacent unanswered questions. Some descriptions approximate answer responsibility, but descriptions are not enough unless supported by surface-specific implementation.

Determination: **mechanical responsibility only as a registry; individual registered surfaces may be answer-responsible**.

### Diagnostic Shape Audit

Diagnostic Shape Audit is primarily mechanical audit responsibility.

It owns a bounded mechanical question:

```text
Do diagnostic inventory declarations match implementation markers?
```

However, its implemented field set is about support for record, JSON, record scope, diagnostic-fact emission, event-ledger writes, repo-file use, projected-state use, and mutation markers. It does not determine what semantic question each surface answers.

Determination: **mechanical responsibility, not semantic answer responsibility for the audited surfaces**.

The audit itself answers a bounded mechanical question, but it is not evidence that every audited diagnostic owns a bounded answer.

### Projection Shape

Projection Shape sits between mechanical self-knowledge and bounded answer responsibility.

It exposes consumes, produces, influences, does-not-influence, authority boundary, confidence, and read-only/event-ledger/cluster boundary. This is more than a simple inventory because it answers how projection stages relate mechanically and authoritatively.

However, it does not preserve per-question uncertainty or derived semantic conclusions. Its answer is structural rather than semantic.

Determination: **strong mechanical/projection responsibility; limited bounded structural answer responsibility**.

Bounded structural question:

```text
What are the implementation-backed projection stages, consumed/produced artifacts, influence boundaries, and authority boundaries?
```

It should not be treated as an answer composition about operational meaning.

## Counterexamples

### Aggregation without clear answer ownership

Diagnostic Inventory aggregates operational surface declarations, but the registry shape is mechanical. It can tell whether a diagnostic supports JSON or mutates cluster state; it cannot by itself tell what uncertainty the diagnostic preserves or what adjacent questions it refuses.

### Mechanical audit without semantic responsibility

Diagnostic Shape Audit aggregates registry entries and implementation specs. It owns a bounded mechanical audit question, but the audited fields are not answer-family fields. It proves mechanical surface self-knowledge, not semantic answer contracts.

### Structural rendering without semantic composition

Projection Shape renders stage consumes/produces/influences boundaries. It is implementation-backed and authority-aware, but it does not compose an answer about current operational pressure, source meaning, inquiry intent, or truth. It is answer-like only for projection structure.

### Bounded answer without explicit answer-contract object

Source Navigation answers a bounded question without an explicit answer-contract schema. Its contract is distributed across module docstring, predicate restriction, match logic, formatter behavior, and tests. This shows that answer responsibility can exist in practice without a new architectural object.

### Semantic responsibility inferred by prose but not implementation

Prior investigation prose sometimes calls surfaces answer compositions. That label is unsupported unless the implementation shows the minimum evidence above. For example, a document phrase like "answer composition visibility" is not enough to promote a surface into an answer-responsible surface without builder logic, boundaries, uncertainty, and authority evidence.

## Necessary and sufficient conditions

### Question family

Necessary: **yes**, but it may be implicit in code shape and formatter output rather than a named field.

Sufficient: **no**. A CLI description may imply a question without preserving authorities, uncertainty, or negative authority.

### Consumed knowledge / consumed authorities

Necessary: **yes** for implementation-backed responsibility. Without consumed authorities, the answer cannot be bounded to repository evidence.

Sufficient: **no**. Diagnostic Inventory consumes registry entries, but that alone does not make it semantically answer-responsible for each surface.

### Uncertainty preservation

Necessary: **yes** for semantic answer responsibility. A surface that answers a bounded question must expose what remains unknown, incomplete, caveated, absent, or not proven.

Sufficient: **no**. A warning or caveat alone does not show question ownership.

### Negative authority

Necessary: **yes** where overclaiming is possible. In this repository, nearly every candidate answer-responsible surface needs explicit non-authority because diagnostics, projections, inquiry notes, and navigation rows can otherwise be mistaken for cluster truth, operator intent, or operational action.

Sufficient: **no**. A no-mutation statement is mechanical unless paired with a bounded answer and authority/uncertainty logic.

## Surface rendering vs aggregation vs composition vs answer responsibility

Rendering is formatting existing data for an operator. It is not answer responsibility by itself.

Aggregation collects multiple records or counts. It becomes answer-relevant only if the aggregation is in service of a bounded question and preserves caveats.

Composition joins multiple authorities or surfaces into a structured result. It becomes answer-responsible only when it exposes why those authorities are relevant, what conclusion or orientation is produced, and what remains outside authority.

Answer responsibility is the combination of bounded question ownership, implementation-backed authorities, shaping logic, uncertainty preservation, and negative authority.

## Can a surface answer a bounded question without becoming an answer composition?

Yes.

Source Navigation answers a bounded question by constrained lookup over preserved source facts. It is not a broad answer composition because it does not join multiple semantic surfaces into a conclusion; it selects from a narrow fact family. Projection Shape answers a bounded structural question by rendering declared stage boundaries. Diagnostic Shape Audit answers a bounded mechanical consistency question.

Therefore:

```text
bounded answer responsibility
  does not imply
answer composition
```

Answer composition is one way to own bounded answer responsibility, not the only way.

## Does the repository already contain answer contracts in practice?

Yes, locally and unevenly.

The repository does not appear to contain a uniform `AnswerContract` architectural object. But several surfaces already implement answer-contract-like behavior in practice:

- Operational Story: strongest multi-surface operational answer contract.
- Projection Integrity Summary: integrity-count answer contract with caveats.
- Inquiry Orientation: preserved-prose orientation contract with uncertainty and negative authority.
- Source Navigation: narrow source-fact navigation contract.
- Reasoning Path Audit: derivation-path answer contract.
- Selection Path Audit: selection-trace answer contract.

Diagnostic Inventory and Diagnostic Shape Audit provide mechanical contracts that make those surfaces visible and checkable, but they do not themselves provide semantic answer contracts for every surface.

## Supported conclusions

1. The minimum evidence for bounded answer responsibility is not a new registry field. It is implementation evidence of bounded question target, consumed authorities, answer-shaping logic, uncertainty preservation, negative authority, and inspectable/testable boundary.
2. Mechanical responsibility and answer responsibility are different but compatible. Mechanical responsibility governs what a surface can do; answer responsibility governs what bounded question it answers and what it refuses to answer.
3. Answer responsibility can remain implementation-backed. Existing module docstrings, dataclasses, builder logic, formatter text, diagnostic inventory entries, shape-audit specs, and tests already provide enough evidence for several surfaces.
4. Answer responsibility does not require answer composition. Lookups and structural audits can answer bounded questions when their authority and non-authority are implemented.
5. The repository already contains answer contracts in practice, but they are distributed and uneven rather than centralized.

## Unsupported conclusions

1. It is not supported that Seed needs a new answer registry, schema, router, planner, runtime layer, or metadata framework.
2. It is not supported that every diagnostic, view, lookup, inventory, summary, audit, or navigation surface owns semantic answer responsibility.
3. It is not supported that presentation vocabulary such as "answer composition visibility" is itself repository knowledge without implementation evidence.
4. It is not supported that aggregation alone implies answer responsibility.
5. It is not supported that a read-only or no-mutation boundary alone implies an answer contract.

## Recommended next step

Do not implement a new system.

The smallest implementation-backed next step, if future operational work needs it, is to choose one existing answer-responsible surface and improve tests or documentation around its already-implemented answer boundary. Operational Story is the best candidate because it has the strongest composition evidence and already appears in Diagnostic Inventory and Diagnostic Shape Audit.

For this investigation, no code change is recommended.
