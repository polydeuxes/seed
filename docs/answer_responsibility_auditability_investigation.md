# Answer Responsibility Auditability Investigation

## Question

Can bounded answer responsibility be audited using implementation evidence alone,
without introducing an `AnswerInventory`, answer-contract schema, metadata
registry, runtime registration, or any new visibility system?

## Short answer

Yes, partially and usefully.

Implementation evidence can already distinguish many answer-responsible surfaces
from mechanical-only surfaces. The distinction is not a declared metadata field;
it is distributed across module boundaries, dataclasses, builder inputs,
selection logic, formatter sections, explicit unknown/caveat handling, negative
authority text, and tests.

The audit can detect three practical responsibility classes today:

1. **Strong answer responsibility**: bounded target, consumed authorities,
   answer-shaping logic, uncertainty/unknown preservation, negative authority,
   and inspectable boundary are all present in implementation.
2. **Partial answer responsibility**: most categories are present, but one or
   more are formatter-heavy, narrow, or only implicit in selection code.
3. **Mechanical-only responsibility**: the surface has strong mechanical
   self-knowledge or projection-boundary self-knowledge, but lacks semantic
   answer target, semantic uncertainty, or answer-shaped negative authority.

This conclusion does not require a new architectural object. It requires careful
reading of existing implementation evidence and preservation of the difference
between implementation evidence and investigation interpretation.

## Files inspected

Implementation evidence was reviewed in:

- `seed_runtime/operational_story.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`

Prior interpretive work was used only as context and checked against
implementation:

- `bounded_answer_responsibility_investigation.md`
- `docs/answer_composition_self_knowledge_investigation.md`
- `docs/repository_surface_inventory_observation.md`
- `docs/audit/projection_authority_provenance_audit.md`
- related characterization and observation documents found by repository search

Repository authority wins: implementation evidence below is treated as stronger
than investigation prose.

## Auditable evidence categories

The investigation used six evidence categories. These are not proposed metadata
fields. They are practical features that can be detected in current code.

| Category | Implementation evidence that can be audited today |
| --- | --- |
| Bounded answer target | Module docstring, dataclass name/fields, builder function name/signature, formatter title/sections, CLI tests. |
| Consumed authorities | Imports of existing builders, `State` inputs, repository path inputs, preserved fact/support inputs, optional prebuilt source views. |
| Answer-shaping logic | Filtering, sorting, aggregation, ranking, selection, deduplication, row limits, candidate/non-selected construction, caveat assembly. |
| Uncertainty preservation | `unknowns`, `caveats`, incomplete titles, default caveat constants, no-match branches, explicit unknown reasons. |
| Negative authority | Docstrings and formatter/boundary text saying what the surface does not infer, decide, mutate, record, execute, verify, or promote. |
| Inspectable boundary | JSON/dataclass boundary fields, rendered Boundary sections, read-only flags, `records_facts=False`, `writes_event_ledger=False`, `mutates_cluster=False`. |

The categories are most reliable when they appear in more than one location, for
example a dataclass field plus builder logic plus formatter text plus tests. They
are weakest when they appear only in investigation prose or only as explanatory
formatter text.

## Answer-responsible surfaces

### Operational Story: strong evidence

Operational Story is the strongest current example of bounded answer
responsibility.

| Evidence category | Implementation evidence |
| --- | --- |
| Bounded answer target | The module is a read-only operational story view. The dataclass has answer-shaped fields such as `focus`, `pressure`, `supporting_evidence`, `capabilities`, `constraints`, `correlation_gaps`, `impact`, `recent_changes`, `observed_outcomes`, `investigation_path`, `unknowns`, and `boundary`. |
| Consumed authorities | The builder consumes implemented surfaces: pressure audit, capability needs, privilege discovery, correlation audit, impact audit, investigation path audit, and projected `State`. |
| Answer-shaping logic | It chooses a primary pressure, derives focus from that pressure, extracts supporting evidence, maps capability/constraint/correlation/impact data into story fields, and builds an investigation path from the primary domain. |
| Uncertainty preservation | It appends unknowns when no pressure is identified, no capability needs are identified, or impact is unknown. |
| Negative authority | The builder docstring says it composes current operational evidence without planning, recording, or mutation. The rendered boundary says no recording, event-ledger writes, cluster mutation, plans, or implementation advice. |
| Inspectable boundary | The dataclass carries a `boundary` dict with `mode=read_only_view`, `records_facts=False`, `writes_event_ledger=False`, and `mutates_cluster=False`; the formatter renders that boundary. |

Detectability: **consistently detectable**. Operational Story has multi-location
evidence: imports, builder calls, dataclass shape, unknown construction,
formatter sections, and explicit boundary.

Counterexample pressure: its bounded target is inferred from composition and
rendered sections rather than from a formal answer declaration. That is acceptable
for implementation-backed auditing, but it means an audit should report the
surface as implementation-detected rather than declared.

### Inquiry Orientation: strong but intentionally bounded evidence

Inquiry Orientation has strong evidence for answer responsibility, with the
important caveat that its answer target is orientation over preserved inquiry
prose, not semantic intent extraction.

| Evidence category | Implementation evidence |
| --- | --- |
| Bounded answer target | The module docstring calls it a minimized read-only inquiry-note orientation probe. The view contains one note, related material, uncertainty, and authority boundary. |
| Consumed authorities | It consumes an isolated inquiry-note JSONL store, projected `State`, fact supports, and Source Navigation matches. |
| Answer-shaping logic | It tokenizes note prose, computes deterministic lexical overlap against fact supports and source navigation, deduplicates related material, and caps related items. |
| Uncertainty preservation | It has separate uncertainty text for matches and no matches. The no-match branch explicitly says absence of deterministic related material does not prove unrelatedness. |
| Negative authority | The authority boundary states that the inquiry note is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction, and that lexical matches do not assert importance, ownership, intent, concern, recommended action, or next safe move. |
| Inspectable boundary | The view carries `uncertainty` and `authority_boundary`, and the formatter renders both sections. |

Detectability: **consistently detectable for the V1 probe**. The negative
authority is unusually strong. The uncertainty is explicit. The consumed
authorities are discoverable in imports and builder logic.

Counterexample pressure: many answer-like claims about inquiry, intent, or
orientation would be overreach. Implementation supports deterministic related
material and authority-boundary rendering, not semantic interpretation of the
operator's intent.

### Projection Integrity Summary: strong bounded integrity answer

Projection Integrity Summary is answer-responsible for aggregate integrity
signals, not for truth, health, repair, or verification.

| Evidence category | Implementation evidence |
| --- | --- |
| Bounded answer target | The module docstring identifies a read-only Projection Integrity Summary over existing projected State integrity signals. The dataclass is an aggregate count summary. |
| Consumed authorities | It consumes evidence summary, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, capability inventory, projection version, and last event id. Optional source-view arguments preserve already-built source semantics. |
| Answer-shaping logic | The builder aggregates counts, counts capability states with `Counter`, and composes default caveats into the returned summary. |
| Uncertainty preservation | It preserves caveats that integrity counts are projection-backed signals and that unsupported, unverified, stale, contradicted, or missing evidence does not mean false. |
| Negative authority | The module docstring says it does not create facts or evidence, execute Runtime behavior, call providers, verify capabilities, refresh stale facts, resolve contradictions, or mutate projected State. |
| Inspectable boundary | Caveats are first-class dataclass data. Projection version and last event id make the summary boundary inspectable against projected State. |

Detectability: **consistently detectable** for integrity-count answer
responsibility.

Counterexample pressure: it lacks a separate `boundary` dict like Operational
Story, Reasoning Path Audit, and Selection Path Audit. Its boundary is in the
module docstring and caveats, so a mechanical audit must avoid requiring a single
uniform boundary shape.

### Source Navigation: strong narrow answer responsibility

Source Navigation is a compact example where answer responsibility is narrow but
well supported.

| Evidence category | Implementation evidence |
| --- | --- |
| Bounded answer target | The module docstring states read-only navigation over preserved repository source facts. The view is for one query and has definitions/imports rows. |
| Consumed authorities | It consumes projected `State.fact_supports` and only `defines`/`imports` fact support predicates. |
| Answer-shaping logic | It normalizes the query, converts support rows, matches by subject/path/exact symbol/final segment, sorts rows, limits path/module lookups, and renders support summaries. |
| Uncertainty preservation | The no-match formatter branch renders `No source facts matched.` This is a weak but real negative result. |
| Negative authority | The module docstring says it does not inspect files, parse source, ingest observations, or infer behavior, reachability, or ownership. `_matches` rejects non-source predicates. |
| Inspectable boundary | The boundary is distributed across predicate constants, matching logic, row shape, bounded row limit, and rendered source-fact sections rather than a `boundary` field. |

Detectability: **consistently detectable for source-fact navigation**, but
boundary detection is surface-specific because there is no common boundary field.

Counterexample pressure: uncertainty preservation is minimal. If a future audit
requires rich uncertainty, Source Navigation would be partial. If it only requires
negative-result preservation and explicit non-inference, Source Navigation is
strong.

### Reasoning Path Audit: strong partial/composed evidence

Reasoning Path Audit is answer-responsible for explaining implemented derivation
paths for operational conclusions.

| Evidence category | Implementation evidence |
| --- | --- |
| Bounded answer target | The module docstring names read-only evidence-backed derivation paths. The dataclass fields are `evidence`, `intermediate_conclusions`, `derived_conclusions`, `consumers`, `story_impact`, `unknowns`, and `boundary`. |
| Consumed authorities | It consumes ownership discrepancies, capability needs, pressure audit, privilege discovery, Operational Story, projected `State`, and repository root. |
| Answer-shaping logic | It matches a requested subject/domain, builds evidence rows, derives intermediate and capability conclusions, identifies consumers, attaches story impact, and deduplicates consumers. |
| Uncertainty preservation | If no derivation evidence is found, it records an unknown for the derivation area and renders `Reasoning Path Incomplete`. |
| Negative authority | Its boundary defaults to read-only reasoning audit with no fact recording, event-ledger writes, or cluster mutation. |
| Inspectable boundary | The boundary is in JSON/dataclass output and rendered text. |

Detectability: **consistently detectable**, but answer scope is composed and
operationally narrow. It explains derivation evidence for known implemented
surfaces; it does not establish a universal reasoning-chain model.

Counterexample pressure: some answer target language is in formatter/title and
module docstring, while the body is implementation-specific matching. That is
still auditably useful, but a generic audit should classify this as a composed
operational derivation answer, not general reasoning.

### Selection Path Audit: partial-to-strong evidence

Selection Path Audit is answer-responsible for implemented selection evidence,
mainly current focus / primary pressure selection.

| Evidence category | Implementation evidence |
| --- | --- |
| Bounded answer target | The module docstring says read-only selection trace visibility for operational conclusions. The dataclass contains target, selected value, candidates, selection factors, non-selected candidates, evidence, outcome, unknowns, and boundary. |
| Consumed authorities | It consumes pressure audit, Operational Story, projected `State`, and repository root. |
| Answer-shaping logic | It normalizes target names, detects current-focus/primary-pressure selection, builds ranked candidates, explains non-selected candidates, and records selection factors. |
| Uncertainty preservation | Unsupported targets return `selected=unknown`, `selection_factors=["unknown"]`, and an unknown explaining that no implementation-backed selection evidence was discovered. |
| Negative authority | The builder docstring says it explains implemented selection evidence without changing selection behavior. Boundary text says read-only with no recording, event-ledger writes, or cluster mutation. |
| Inspectable boundary | The boundary is in JSON/dataclass output and rendered text. |

Detectability: **partially detectable to consistently detectable**. It is strong
for the implemented target family but not broad selection reasoning.

Counterexample pressure: answer responsibility should not be inferred for every
possible selection-like behavior in the repository. The implementation explicitly
returns unknown for unsupported targets.

## Mechanical-only and primarily mechanical surfaces

### Diagnostic Inventory: mechanical-only responsibility

Diagnostic Inventory has strong mechanical self-knowledge but does not itself
provide semantic answer responsibility for each listed surface.

Present evidence:

- surface name and CLI flags;
- projected-state and repository-file use;
- JSON and record support;
- record scope;
- diagnostic fact, cluster fact, event-ledger, and cluster-mutation flags;
- description text.

Absent or weak answer-responsibility categories:

| Category | Status |
| --- | --- |
| Bounded answer target | Partially present as a description, but mostly mechanical. |
| Consumed authorities | Present mechanically (`uses_projected_state`, `uses_repo_files`), not semantically. |
| Answer-shaping logic | Absent; the registry does not encode how the surface shapes an answer. |
| Uncertainty preservation | Absent as a general category. |
| Negative authority | Present mechanically for mutation/recording facts; absent for semantic non-authority. |
| Inspectable boundary | Strong mechanical boundary. |

Classification: **mechanical-only responsibility**. It can answer what a surface
is mechanically allowed to do; it cannot tell what semantic uncertainty or
negative authority the surface preserves.

### Diagnostic Shape Audit: mechanical-only responsibility

Diagnostic Shape Audit is a strong self-audit of mechanical declarations against
implementation markers.

Present evidence:

- audited fields such as `supports_record`, `supports_json`, `record_scope`,
  `emits_diagnostic_facts`, `writes_event_ledger`, `reads_diagnostic_facts`,
  `uses_repo_files`, `uses_projected_state`, and `mutates_cluster`;
- implementation specs binding diagnostic names to module paths, functions, CLI
  flags, JSON flags, repo-file markers, diagnostic-fact read markers, and
  mutation markers;
- row statuses such as consistent, warning, mismatch, and unknown.

Absent or weak answer-responsibility categories:

| Category | Status |
| --- | --- |
| Bounded answer target | Present for the audit itself as a mechanical consistency question, not for semantic answers. |
| Consumed authorities | Present as registry plus implementation source files. |
| Answer-shaping logic | Present mechanically as field comparison/status assignment, not answer-family shaping. |
| Uncertainty preservation | Present as audit `unknown` status, but not semantic answer uncertainty. |
| Negative authority | Present through mutation/read markers, not through semantic refusal boundaries. |
| Inspectable boundary | Strong mechanical boundary. |

Classification: **mechanical-only responsibility**. It is the precedent for
auditing implementation evidence, but its evidence categories are operational
mechanics rather than bounded answer semantics.

### Projection Shape: structural/projection-boundary responsibility, not broad answer responsibility

Projection Shape is not diagnostic inventory, but it is still primarily
structural. It provides implementation-backed projection-stage self-knowledge.

Present evidence:

- stage names;
- consumes/produces/influences/does-not-influence tuples;
- authority-boundary labels;
- implementation-backed confidence;
- read-only/event-ledger/cluster-mutation boundary.

Absent or weak answer-responsibility categories:

| Category | Status |
| --- | --- |
| Bounded answer target | Present for projection structure only. |
| Consumed authorities | Present as stage consumes fields, but these are structural inputs, not answer authorities. |
| Answer-shaping logic | Absent; the module renders declared stage shape rather than composing a semantic answer. |
| Uncertainty preservation | Mostly absent; confidence is uniform `implementation_backed`, not uncertainty/caveat handling. |
| Negative authority | Present structurally through `does_not_influence`, but not semantic non-authority. |
| Inspectable boundary | Strong structural boundary. |

Classification: **mechanical/structural responsibility**. It is answer-like only
for the question "what is the projection shape?" It should not be promoted into
a general answer-responsibility surface without additional implementation
evidence.

## Category detectability findings

| Evidence category | Overall detectability today | Notes |
| --- | --- | --- |
| Bounded answer target | Partially consistent | Usually detectable from module/dataclass/builder/formatter names, but not declared uniformly. Stronger in Operational Story, Inquiry Orientation, Projection Integrity Summary, Source Navigation, Reasoning Path Audit, and Selection Path Audit. |
| Consumed authorities | Consistently detectable | Imports, builder calls, `State` inputs, repo-root inputs, and preserved support iteration are easy to audit. |
| Answer-shaping logic | Consistently detectable but surface-specific | Aggregation, selection, lexical matching, sorting, no-match branches, and candidate ranking are implementation-visible, but each surface shapes differently. |
| Uncertainty preservation | Partially detectable | Strong where `unknowns`, `caveats`, incomplete titles, or uncertainty constants exist. Weak where only no-match formatter text exists. |
| Negative authority | Partially detectable | Strong in Inquiry Orientation, Projection Integrity Summary, Operational Story, and Source Navigation. Mechanical-only surfaces have mutation boundaries but not semantic refusal boundaries. |
| Inspectable boundary | Consistently detectable for strong surfaces, surface-specific in shape | Some surfaces use `boundary` dicts; others use docstrings, caveats, constants, predicate restrictions, or formatter sections. A detector must not require a single schema. |

## Counterexamples and weak evidence

### Formatter-only or formatter-heavy evidence

Some surfaces expose key boundary text in the formatter. That is still
implementation evidence, but weaker than builder/dataclass evidence because it
may describe behavior without enforcing it.

Examples:

- Source Navigation's no-match uncertainty is formatter text, while its stronger
  boundary is enforced by predicate matching and source predicate constants.
- Reasoning Path and Selection Path boundaries are first-class dataclass defaults
  and rendered text, making them stronger than formatter-only evidence.
- Projection Integrity Summary caveats are first-class dataclass data, but the
  no-mutation boundary is primarily docstring-level.

### Investigation-prose-only inference

Prior investigations sometimes use broad terms such as answer contract, lens,
orientation, response, or responsibility. Those terms are not automatically
repository knowledge. They are supported only when mapped back to implementation:

- `Operational Story` is supported because it composes implemented surfaces into
  current focus, pressure, evidence, impact, unknowns, and boundary.
- `Inquiry Orientation` is supported only as deterministic related-material
  orientation, not intent understanding.
- `Source Navigation` is supported only over preserved `defines` and `imports`
  facts, not source-code parsing or ownership inference.
- `Projection Shape` is supported as projection-stage shape visibility, not a
  semantic answer contract.

### Answer-like but mechanical

Diagnostic Inventory and Diagnostic Shape Audit can answer questions such as
"does this diagnostic support JSON?" or "does implementation match registry
shape?" Those are real bounded questions, but they are mechanical. They do not
show semantic answer responsibility for operational meaning, uncertainty,
negative authority, or consumed domain authorities.

### Composed responsibility

Operational Story, Reasoning Path Audit, and Selection Path Audit are composed.
They consume other surfaces. This strengthens consumed-authority evidence, but it
also requires an audit to separate:

- the composed surface's own answer responsibility; from
- responsibility delegated to consumed surfaces.

For example, Operational Story owns current operational story composition. It
does not own truth of every pressure, capability, privilege, correlation, impact,
or investigation-path source it consumes.

## Can an audit distinguish mechanical-only from answer-responsible surfaces?

Yes, with a conservative rule:

A surface should be considered answer-responsible only when implementation shows
at least:

1. a bounded target or question;
2. consumed authorities or source evidence;
3. answer-shaping logic that transforms those authorities into an answer-shaped
   result;
4. uncertainty/caveat/unknown or negative-result handling; and
5. an inspectable boundary or negative authority.

Using this rule:

| Surface | Classification | Reason |
| --- | --- | --- |
| Operational Story | Strong answer responsibility | Multi-surface composition, focus/pressure/evidence shaping, unknowns, explicit boundary. |
| Inquiry Orientation | Strong answer responsibility for V1 orientation | Preserved note, lexical related-material matching, uncertainty, strong negative authority. |
| Projection Integrity Summary | Strong bounded integrity answer | Aggregates integrity counts, preserves caveats, refuses truth/repair/execution authority. |
| Source Navigation | Strong narrow answer responsibility | Source-fact-only query answer, predicate restrictions, non-inference boundary; uncertainty is minimal. |
| Reasoning Path Audit | Strong partial/composed answer responsibility | Derivation-path explanation with evidence/intermediate/derived/consumer fields and unknowns. |
| Selection Path Audit | Partial-to-strong answer responsibility | Implemented selection trace for current focus/pressure; unknown for unsupported targets. |
| Diagnostic Inventory | Mechanical-only | Registry of mechanical surface properties; no answer-shaping logic or semantic uncertainty. |
| Diagnostic Shape Audit | Mechanical-only | Audits mechanical registry-to-implementation consistency; not semantic answer contracts. |
| Projection Shape | Mechanical/structural | Strong projection-stage boundary visibility, but answer-like only for projection structure. |

## Can implementation evidence identify strong, partial, and mechanical-only responsibility without new declarations?

Yes. The repository already contains enough implementation evidence for a
non-declarative audit to classify surfaces conservatively:

- **Strong** when all six categories appear across code paths, data shape,
  formatter, and boundary/caveat/unknown handling.
- **Partial** when the answer target is narrow, one category is formatter-heavy,
  or behavior is implemented only for a limited target family.
- **Mechanical-only** when the surface primarily reports flags, implementation
  markers, stage shape, mutation status, record scope, or structural consumes /
  produces / influences data without semantic answer shaping.

The audit would be less precise than a declaration-based system, but that is a
feature for this investigation: it keeps responsibility implementation-backed
and prevents architectural preference from becoming authority.

## Supported conclusions

1. Bounded answer responsibility can be audited from implementation evidence
   today, but the audit must be conservative and evidence-based.
2. Consumed authorities and answer-shaping logic are the most consistently
   detectable categories.
3. Uncertainty preservation and negative authority are detectable, but less
   uniform; they may appear as `unknowns`, `caveats`, constants, no-match text,
   predicate restrictions, or boundary prose.
4. Operational Story, Inquiry Orientation, Projection Integrity Summary, Source
   Navigation, Reasoning Path Audit, and Selection Path Audit all exhibit
   implementation-backed answer responsibility, with different scopes and
   strengths.
5. Diagnostic Inventory and Diagnostic Shape Audit are strong mechanical
   self-knowledge surfaces, not semantic answer-responsibility surfaces.
6. Projection Shape is structural/projection-boundary self-knowledge. It is not
   evidence for a broad semantic answer contract.
7. No new architectural object is required to recognize the current behavior.

## Unsupported conclusions

The implementation does **not** support these conclusions:

- Seed has a declared answer-contract system.
- Every diagnostic with inventory metadata is answer-responsible.
- Mechanical self-knowledge automatically implies semantic answer responsibility.
- Inquiry Orientation understands operator intent.
- Source Navigation parses source files or infers ownership/reachability.
- Projection Integrity Summary decides truth, correctness, health, repair, or
  provider availability.
- Projection Shape is a general answer-responsibility schema.
- A single uniform field shape is required before answer responsibility can be
  audited.

## Recommended next step

The recommended next step is **not** to introduce an answer inventory, schema,
registry, metadata system, runtime concept, or new visibility surface.

The smallest implementation-backed next step is to use this investigation as a
checklist during future surface work:

- when a surface is claimed to be answer-responsible, cite the exact
  implementation evidence for the six categories;
- when a surface is mechanical-only, keep it mechanical and avoid promoting its
  registry or shape fields into semantic responsibility;
- when evidence is formatter-only or prose-only, mark the claim weak until the
  builder, dataclass, tests, or boundary logic also support it.

If future work needs executable auditing, it should start as a narrow test or
repository-local analysis of one existing surface's evidence rather than as a new
registry or runtime architecture.
