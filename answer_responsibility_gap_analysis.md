# Answer Responsibility Gap Analysis

## Question

Which existing surfaces are missing implementation-shape elements associated
with strong answer responsibility?

This report is implementation characterization only. It does not propose an
`AnswerInventory`, an answer-contract schema, metadata registry, runtime
registration, new visibility system, or answer framework. Repository authority
wins: prior investigation terms are used only where current implementation
supports them.

## Method

The analysis reviewed prior characterization and current implementation for
these surfaces:

- Operational Story
- Inquiry Orientation
- Projection Integrity Summary
- Source Navigation
- Reasoning Path Audit
- Selection Path Audit
- Diagnostic Inventory
- Diagnostic Shape Audit
- Projection Shape

Each surface was evaluated against the strongest currently observed
implementation shape:

```text
answer-responsible surface
    = bounded view
    + builder over existing authorities
    + answer-shaping logic
    + uncertainty preservation
    + authority boundary
```

These elements are reading aids, not proposed metadata. A missing element below
means missing or weak implementation shape, not missing registration.

## Surface assessment matrix

Strength scale:

- **Strong**: element is backed by data shape plus builder/formatter behavior or
  explicit boundary/caveat/unknown logic.
- **Medium**: element is implemented, but narrow, formatter-heavy, delegated, or
  implicit.
- **Weak**: element exists mostly as prose, generic mechanics, or negative-result
  text.
- **Absent**: no implementation evidence for this element in answer-responsible
  form.

| Surface | Classification | Bounded view | Builder over authorities | Answer-shaping logic | Uncertainty preservation | Authority boundary | Main gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Operational Story | Strong | Strong | Strong | Strong | Strong | Strong | Authority provenance is named by consumed-surface family rather than item-level source lineage. |
| Inquiry Orientation | Strong narrow | Strong | Strong | Strong | Strong | Strong | Semantic scope is intentionally only lexical related-material orientation. |
| Projection Integrity Summary | Strong narrow | Strong | Strong | Strong | Strong | Medium | No first-class `boundary` field; boundary is split between docstring and caveats. |
| Source Navigation | Nearly complete / strong narrow | Strong | Medium | Strong | Weak | Medium | Uncertainty is mostly a no-match formatter branch; boundary is distributed rather than structured. |
| Reasoning Path Audit | Strong partial / nearly complete | Strong | Strong | Strong | Medium | Strong | Depends on broad string matching and composed surfaces; answer target is implementation-specific, not a universal reasoning model. |
| Selection Path Audit | Nearly complete / partial-to-strong | Strong | Strong | Strong | Strong | Strong | Strong only for implemented focus/pressure selection families; broader selection targets return unknown. |
| Diagnostic Inventory | Mechanical-only | Medium mechanical | Weak mechanical | Absent semantic | Absent semantic | Strong mechanical | Mechanical surface contracts are not semantic answer shaping. |
| Diagnostic Shape Audit | Mechanical-only | Strong mechanical | Strong mechanical | Strong mechanical | Weak mechanical | Strong mechanical | Its `unknown` status concerns implementation-marker classification, not semantic answer uncertainty. |
| Projection Shape | Mechanical / structural | Strong structural | Medium structural | Absent semantic | Weak | Strong structural | Stage visibility is projection-structure self-knowledge, not bounded semantic answer composition. |

## Strong surfaces

### Operational Story

Operational Story is the strongest current answer-responsible surface. Its view
object is answer-shaped: focus, pressure, supporting evidence, capabilities,
constraints, correlation gaps, impact, recent changes, observed outcomes,
investigation path, unknowns, and boundary are first-class fields. Its builder
consumes pressure, capability, privilege, correlation, impact, investigation-path,
and projected-state authorities, then shapes them into a current operational
story. It preserves unknowns for missing pressure, missing capability needs, and
unknown impact. Its returned boundary is explicit: read-only view, no fact
recording, no event-ledger writes, and no cluster mutation.

Classification: **strong**.

Gap characterization:

- Not missing the core shape.
- The remaining limitation is not missing metadata. It is that consumed authority
  visibility is mostly surface-level: it names the composing surfaces and renders
  derived fields, but does not expose item-level provenance for every story
  sentence.
- This is still strong bounded answer responsibility because the surface owns a
  narrow composition question, not full truth of every consumed diagnostic.

### Inquiry Orientation

Inquiry Orientation is strong for its intentionally narrow question: which
already-projected material is deterministically related to a preserved inquiry
note? Its module refuses to mutate projected state, append events, call
providers, execute tools, or create facts, goals, needs, decisions, proposals, or
plans. The view carries the note, related material, uncertainty, and authority
boundary. The builder tokenizes note prose, computes overlap against projected
fact supports and source-navigation matches, deduplicates results, and caps
related material. It preserves both match and no-match uncertainty and gives a
strong negative authority boundary: the note is not promoted into a fact, goal,
plan, authorization, command, runtime instruction, intent, or recommended next
move.

Classification: **strong narrow**.

Gap characterization:

- Not missing the core shape.
- Its narrowness is not a weakness. A narrow surface can be strong when it names
  and enforces its limits.
- The most important limitation is semantic: it is lexical orientation, not
  intent understanding. That is an intentional boundary, not an implementation
  gap.

### Projection Integrity Summary

Projection Integrity Summary is strong for aggregate integrity counts and
caveats. Its dataclass carries explicit integrity counts, caveats, projection
version, and last event id. The builder consumes existing integrity authorities:
evidence summary, fact conflicts, contradictions, graph issues, stale facts,
refresh recommendations, capability inventory, and projected-state versioning. It
aggregates counts deterministically and preserves caveats as returned data,
including the distinction between integrity signals and truth/correctness
judgments.

Classification: **strong narrow**.

Gap characterization:

- The weakest element is authority boundary shape, not boundary existence.
- Unlike Operational Story and the path audits, Projection Integrity Summary has
  no separate `boundary` dict. Its no-truth/no-repair/no-execution boundary is
  split between the module docstring and caveats.
- This is not evidence that it is partial; it is evidence that strong answer
  responsibility does not require one uniform boundary-object schema.

## Nearly complete and partial surfaces

### Source Navigation

Source Navigation is nearly complete and strong within a very narrow navigation
scope. It exposes a bounded view for one query with definition and import rows.
It consumes projected fact supports and restricts authority to preserved
`defines` and `imports` predicates. Its builder normalizes a query, converts
supports to source rows, rejects non-source predicates, matches syntactically by
subject, path, qualified symbol, or final segment, then sorts and formats the
result. Its module boundary refuses file inspection, source parsing, observation
ingestion, behavioral inference, reachability inference, and ownership inference.

Classification: **nearly complete / strong narrow**.

Missing or weak elements:

- **Weak uncertainty preservation**: no-match output says no source facts matched,
  but there is no structured uncertainty field comparable to `unknowns` or
  `caveats`.
- **Distributed authority boundary**: boundary is implemented through docstring,
  predicate constants, matching logic, bounded row limit, and formatter behavior,
  not a first-class boundary field.
- **Authority visibility is support-row local**: rows expose representative fact
  and support ids, but the surface does not preserve broader authority caveats in
  the returned view object.

Potentially small characterization-relevant improvement, without proposing an
implementation: it appears close to strong because the missing pieces are not
selection or authority consumption. They are mostly structured uncertainty and
structured boundary visibility.

### Reasoning Path Audit

Reasoning Path Audit is strong but partial in a precise way: it explains
implemented derivation paths for operational conclusions, not reasoning in
general. Its dataclass includes domain, subject, evidence, intermediate
conclusions, derived conclusions, consumers, story impact, unknowns, and a
read-only boundary. The builder consumes ownership discrepancies, capability
needs, pressure audit, privilege discovery, Operational Story, projected State,
and repository context. It shapes a response by matching the requested
subject/domain, constructing evidence rows, deriving intermediate and capability
conclusions, identifying consumers, attaching story impact, deduplicating
consumers, and returning an incomplete path when no evidence is found.

Classification: **strong partial / nearly complete**.

Missing or weak elements:

- **Weak precision of answer shaping**: subject/domain matching is broad string
  matching over implemented diagnostic output rather than a typed derivation
  graph.
- **Composed-authority opacity**: it tells which surfaces contributed to the
  path, but some authority is delegated to consumed surfaces rather than fully
  expanded.
- **Boundary is strong operationally but narrow semantically**: it preserves
  read-only/no-record/no-mutation boundaries; it does not prove a universal
  reasoning-chain model.

This is a limitation of implementation shape, not a metadata gap. Adding a
registry would not by itself make the derivation matching more precise.

### Selection Path Audit

Selection Path Audit is nearly complete for implemented current-focus and
primary-pressure selection. Its dataclass carries target, selected value,
candidates, selection factors, non-selected candidates, evidence, outcome,
unknowns, and boundary. The builder consumes pressure audit and Operational
Story, normalizes targets, recognizes current-focus/primary-pressure selection,
preserves candidate ordering, explains selected and non-selected candidates, and
returns explicit unknowns when the requested target is not an implemented
selection surface.

Classification: **nearly complete / partial-to-strong**.

Missing or weak elements:

- **Broadness gap, not strength gap**: it is strong for pressure/focus selection
  but intentionally partial for unsupported target families.
- **Delegated authority**: candidate ordering comes from Pressure Audit and focus
  comes from Operational Story; Selection Path Audit explains that implemented
  selection rather than owning independent selection correctness.
- **Answer boundary depends on target recognition**: unsupported targets are
  handled safely as unknown, which is both a strength and the evidence of its
  bounded scope.

This surface is a counterexample to treating "partial" as weak. Its partiality is
mostly coverage boundary, not failure to preserve uncertainty or authority.

## Mechanical-only and structural surfaces

### Diagnostic Inventory

Diagnostic Inventory is appropriately mechanical. Its entry shape records CLI
flags, projected-state use, repository-file use, JSON support, record support,
record scope, diagnostic-fact emission, cluster-fact emission, event-ledger
writes, cluster mutation, diagnostic-fact reads, and description. That is strong
operational surface self-knowledge.

Classification: **mechanical-only**.

Why it is not answer-responsible in the same sense:

- Its bounded view is mechanical inventory, not a semantic answer view.
- Its consumed authorities are registry entries, not domain authorities selected
  for an operator question.
- It does not perform semantic answer shaping such as composition, orientation,
  aggregation, navigation, derivation, or selection.
- It preserves mutation and recording boundaries, but not semantic unknowns or
  answer caveats.

It is not misclassified. It can answer mechanical questions like whether a
surface supports JSON or recording, but that is mechanical responsibility.

### Diagnostic Shape Audit

Diagnostic Shape Audit is also appropriately mechanical. Its implementation
specs bind diagnostic names to module paths, functions, CLI flags, JSON flags,
repo-file markers, diagnostic-fact read markers, and mutation markers. The audit
rows compare declared inventory fields to observed implementation evidence and
assign statuses such as consistent, warning, mismatch, and unknown.

Classification: **mechanical-only**.

Why it is not answer-responsible in the same semantic sense:

- Its bounded question is registry-to-implementation consistency.
- Its shaping logic is mechanical field comparison, not semantic answer shaping.
- Its unknown status means implementation-marker uncertainty, not unresolved
  semantic evidence.
- Its authority boundary concerns record/mutation/read mechanics, not the truth,
  intent, planning, repair, or inference limits of an answer.

This surface is a useful precedent for implementation-backed auditing, but it is
not evidence that every diagnostic is answer-responsible.

### Projection Shape

Projection Shape is structural self-knowledge. It exposes projection stages,
what they consume, produce, influence, do not influence, their authority-boundary
labels, implementation-backed confidence, and a read-only/no-event/no-mutation
boundary.

Classification: **mechanical / structural**.

Why it is not a broad answer-responsible surface:

- Its bounded view is projection-stage structure, not a semantic operator answer.
- Its consumes/produces/influences tuples are structural facts about the
  projection pipeline, not consumed answer authorities.
- It renders declared stage shape; it does not build a semantic answer over live
  authorities.
- Its confidence is uniform implementation backing, not uncertainty preservation
  about evidence absence or semantic caveats.

Projection Shape is accidentally close to answer responsibility for the narrow
question "what is the implementation-backed projection shape?" It should remain
classified as structural unless implementation adds semantic answer shaping over
projection evidence.

## Weakest implementation-shape elements

Across reviewed surfaces, the weakest elements are:

1. **Uncertainty preservation**
   - Strong in Operational Story, Inquiry Orientation, Projection Integrity
     Summary, Reasoning Path Audit, and Selection Path Audit.
   - Weak in Source Navigation because no-match text is present but not a
     structured uncertainty field.
   - Mechanical-only in Diagnostic Shape Audit because `unknown` means audit
     marker uncertainty, not semantic answer uncertainty.

2. **Authority boundary shape**
   - Strong where a `boundary` field exists or where the authority boundary is a
     first-class returned string.
   - Medium where boundary is distributed through docstrings, caveats,
     constants, predicate restrictions, or formatter sections.
   - Mechanical-only where boundary covers mutation/recording but not semantic
     non-authority.

3. **Authority visibility**
   - Strong enough to identify consumed surfaces in composition surfaces.
   - Weaker at item-level provenance: Operational Story and Reasoning Path Audit
     name surfaces and include evidence snippets, but do not fully expand every
     consumed authority path.
   - Opaque in mechanical inventory for semantic purposes because inventory flags
     do not describe answer authorities.

4. **Answer-shaping precision**
   - Strong where shaping is deterministic and local: aggregation, lexical
     overlap, predicate-limited navigation, pressure candidate ordering.
   - Weaker where matching is broad string matching or delegated composition,
     as in Reasoning Path Audit.

5. **Bounded view specificity**
   - Generally strong in the reviewed answer-responsible surfaces.
   - Only weak when the surface is structural/mechanical and therefore bounded
     around mechanics rather than an operator answer.

## Recurring partial patterns

### Authority boundary present, uncertainty weak

Source Navigation has a clear source-fact boundary, but uncertainty is mostly a
formatter no-match statement. Projection Shape has read-only and influence
boundaries, but not semantic unknown/caveat handling. This pattern suggests that
boundary implementation can be strong while answer uncertainty remains weak.

### Answer shaping present, consumed authorities partly opaque

Operational Story, Reasoning Path Audit, and Selection Path Audit shape answers
from multiple surfaces. They expose the consumed surface family and selected
fields, but do not always expand item-level provenance. This is not fatal: their
answer responsibility is composition/explanation, not the underlying truth of all
inputs. The gap is authority visibility depth.

### Bounded view present, boundary implicit or distributed

Projection Integrity Summary and Source Navigation both have strong bounded
views. Projection Integrity Summary places boundary in docstring and caveats;
Source Navigation places boundary in docstring, predicate constants, match logic,
and formatter output. This confirms that boundary should be characterized as an
implementation shape, not as one required field.

### Mechanical boundary mistaken for semantic boundary

Diagnostic Inventory, Diagnostic Shape Audit, and Projection Shape all provide
strong read/write/mutation boundaries. Those boundaries are real but mechanical.
They do not automatically preserve semantic uncertainty or negative authority
for an answer target.

### Partial because narrow, not because incomplete

Inquiry Orientation, Source Navigation, and Selection Path Audit all demonstrate
that narrowness and partiality must be separated. Inquiry Orientation is strong
because it is deliberately lexical. Source Navigation is nearly complete for
source-fact navigation but weak for structured uncertainty. Selection Path Audit
is strong for focus/pressure selection and partial for unsupported target
families.

## Counterexamples reviewed

### Strong surfaces relying on formatter prose

- **Source Navigation** is the closest caution case. The no-match uncertainty is
  formatter text, but the source-only boundary is also enforced by
  `SOURCE_PREDICATES` and `_matches`, so it is not formatter-only.
- **Projection Integrity Summary** has no boundary dict, but caveats are
  first-class returned data and builder aggregation is real.
- **Operational Story**, **Reasoning Path Audit**, and **Selection Path Audit**
  do not rely only on formatter prose; unknowns and boundary are data fields.

No reviewed strong surface is supported only by investigation interpretation or
formatter vocabulary.

### Partial surfaces already satisfying all criteria

Selection Path Audit nearly satisfies all implementation-shape criteria for its
implemented target family. Its "partial" label is mostly about breadth: it does
not claim all selection behavior. Source Navigation also satisfies most criteria
for its narrow source-fact lookup, but structured uncertainty remains weak.

### Are strong, partial, and mechanical meaningful distinctions?

Implementation evidence supports the distinctions:

- Strong surfaces combine bounded view, authority consumption, answer shaping,
  uncertainty, and authority boundary.
- Partial/nearly-complete surfaces show the same shape but with narrow coverage,
  formatter-heavy uncertainty, distributed boundary, delegated authority, or
  broad matching.
- Mechanical surfaces answer real mechanical questions but lack semantic answer
  shaping and semantic uncertainty preservation.

The distinctions are meaningful if treated as implementation characterization,
not architecture status.

## Missing implementation shape vs missing metadata

The gaps found here are mostly not missing metadata.

- Source Navigation's gap is not that it lacks registry metadata; it lacks
  structured uncertainty comparable to caveats/unknowns.
- Reasoning Path Audit's gap is not that it lacks an answer declaration; it uses
  broad matching and delegated surfaces for derivation evidence.
- Projection Integrity Summary's gap is not that it lacks registration; its
  boundary is real but split across docstring and caveats.
- Diagnostic Inventory does not become answer-responsible by adding answer labels;
  it would still need semantic authorities, answer shaping, and semantic
  uncertainty preservation.

## Mechanical limitation vs answer-responsibility limitation

Mechanical limitations concern whether a surface supports JSON, record scope,
reads repository files, writes the event ledger, mutates cluster state, or
matches implementation markers. Answer-responsibility limitations concern
whether a surface owns a bounded semantic question, consumes authorities for that
question, shapes an answer, preserves uncertainty, and states negative authority.

Diagnostic Inventory and Diagnostic Shape Audit have mechanical strength, not
semantic weakness. Source Navigation and Selection Path Audit have
answer-responsibility limitations, not mechanical inventory failures.

## Strong answer responsibility vs broad answer responsibility

Implementation evidence rejects the assumption that broad responsibility is
stronger. Inquiry Orientation is strong because it is narrow and refuses semantic
promotion. Source Navigation is nearly complete because it confines itself to
preserved source facts. Projection Integrity Summary is strong because it answers
aggregate integrity counts, not truth or repair. Selection Path Audit is strong
for implemented pressure/focus selection and appropriately unknown elsewhere.

Strong answer responsibility is therefore about enforced boundedness, not breadth.

## Supported conclusions

1. **Strongly answer-responsible surfaces**: Operational Story, Inquiry
   Orientation, and Projection Integrity Summary. Reasoning Path Audit is strong
   for implemented derivation visibility but should be described as strong
   partial because of broad matching and composed authority.
2. **Nearly complete / partial surfaces**: Source Navigation and Selection Path
   Audit. Source Navigation is nearly complete for source-fact navigation but has
   weak structured uncertainty. Selection Path Audit is nearly complete for
   focus/pressure selection and intentionally unknown outside supported target
   families.
3. **Mechanical-only or structural surfaces**: Diagnostic Inventory, Diagnostic
   Shape Audit, and Projection Shape. They are appropriately mechanical or
   structural, not misclassified as incomplete answer-responsible surfaces.
4. **Weakest elements**: uncertainty preservation, structured authority boundary,
   item-level authority visibility, and answer-shaping precision.
5. **Recurring gaps**: boundary without uncertainty, shaping with opaque consumed
   authorities, bounded views with distributed boundaries, and mechanical
   boundaries mistaken for semantic answer boundaries.
6. **Nearly-complete candidates**: Source Navigation and Selection Path Audit are
   closest to moving from partial/nearly-complete to unambiguously strong within
   their narrow families, because their missing elements are localized.
7. **Implementation-backed future characterization work** is obvious around
   structured uncertainty, authority-boundary visibility, and provenance depth;
   no new registry, schema, or runtime proposal is required to characterize those
   gaps.

## Unsupported conclusions

The reviewed implementation does not support these claims:

- Answer responsibility is a runtime concept, declaration, registry, metadata
  system, or schema.
- Mechanical inventory fields are enough to classify semantic answer
  responsibility.
- Broad surfaces are more answer-responsible than narrow surfaces.
- Source Navigation answers behavior, ownership, runtime reachability, or current
  source contents.
- Inquiry Orientation extracts operator intent or requirements.
- Projection Integrity Summary decides truth, correctness, health, repair, or
  provider availability.
- Reasoning Path Audit exposes a universal reasoning chain model.
- Selection Path Audit explains all selection behavior in the repository.
- Projection Shape is a general answer-responsibility surface rather than
  projection-structure visibility.

## Recommended next step

Perform a focused characterization pass on **structured uncertainty and boundary
visibility** across the nearly-complete surfaces, especially Source Navigation
and Selection Path Audit. The pass should remain descriptive: identify exactly
where uncertainty and boundary are data fields, formatter text, docstring text,
predicate restrictions, caveats, or mechanical flags. Do not introduce a new
registry, schema, metadata layer, runtime registration mechanism, or answer
framework.
