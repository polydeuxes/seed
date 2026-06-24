# Uncertainty and Authority Visibility Characterization

## Scope and method

This is a characterization-only investigation of how uncertainty visibility and authority visibility are represented today across answer-responsible surfaces. It does not propose a new schema, registry, metadata system, answer framework, or runtime concept.

The implementation evidence reviewed includes the six recurring answer-responsible surfaces named in the task:

- Operational Story
- Inquiry Orientation
- Projection Integrity Summary
- Source Navigation
- Reasoning Path Audit
- Selection Path Audit

The prior investigations were used only as context and cross-checks. Implementation evidence wins over investigation vocabulary.

## Executive characterization

Uncertainty and authority are currently represented as related but not identical concerns.

The strongest current implementation model is:

```text
bounded read-only view
+
builder over existing authorities
+
answer/route shaping
+
structured or semi-structured uncertainty
+
explicit authority boundary
```

The model is strongest when the builder returns data fields that carry both the answer material and the limits of that material. It is weakest when uncertainty appears only as formatter prose or when authority is visible only as a surface family rather than item provenance or a derivation chain.

## Surface-by-surface findings

### Operational Story

#### Uncertainty representation

Operational Story has first-class structured uncertainty. The `OperationalStory` dataclass includes an `unknowns` field, and the builder appends area/reason dictionaries when no pressure is identified, no capability needs are identified, or impact is unknown. The formatter renders these unknowns only when present.

Forms observed:

- missing operational pressure;
- missing capability needs;
- unknown impact;
- unavailable or incomparable impact metrics;
- fallback text such as `none observed` and `unknown` in rendered sections.

Classification: **structured**, with some formatter fallbacks.

#### Authority representation

Operational Story composes authority from implemented diagnostic/read surfaces: pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit. Its returned shape exposes pressure evidence, supporting evidence, capability diagnostics and needed evidence, constraints, correlation gaps, impact metrics, recent changes, observed outcomes, and investigation path steps.

Authority visibility level: **surface-level and item-level**, with partial chain visibility. The surface names and evidence summaries are visible, but not every upstream source row is expanded into full provenance.

#### Limitations

Operational Story shows strong answer shaping and good uncertainty preservation, but its authority chain is summarized. It exposes consumed surface products rather than every underlying fact, event, or support chain.

### Inquiry Orientation

#### Uncertainty representation

Inquiry Orientation has first-class semi-structured uncertainty as a string field on `InquiryOrientationView`. The builder selects one of two fixed uncertainty statements depending on whether related material exists. With matches, uncertainty says related material may be incomplete or incidental and lexical overlap is not semantic interpretation. Without matches, uncertainty says no deterministic related material was found but that absence does not prove unrelatedness.

Forms observed:

- incomplete or incidental match caveat;
- no-match uncertainty;
- negative inference boundary;
- non-interpretation of operator intent.

Classification: **semi-structured**. It is data on the view, but the family is a small set of fixed prose statements rather than typed uncertainty rows.

#### Authority representation

Inquiry Orientation exposes authority through related material rows. Each row includes material type, label, surface, support, why-related text, and surface family. Fact-support matches expose subject, predicate, path, and token-overlap rationale. Source-navigation matches expose representative support identity through the source-navigation row.

Authority visibility level: **item-level**, but mostly as support summaries rather than full provenance chains.

#### Limitations

Inquiry Orientation is one of the clearest examples where authority boundary is very explicit. However, uncertainty is mostly prose in a field, not a typed family list. Authority visibility identifies why an item was related and where support came from, but it does not prove semantic relevance, operator intent, ownership, or recommended action.

### Projection Integrity Summary

#### Uncertainty representation

Projection Integrity Summary represents uncertainty primarily as aggregate counts and caveats. Its dataclass includes counts for unsupported facts, conflicts, contradictions, graph issues, stale facts, refresh recommendations, verified/unverified/stale/unknown/provider-reported capabilities, plus `caveats`. Default caveats explicitly state that integrity signals are projection-backed counts, not truth or correctness judgments; missing evidence does not mean false; and refresh recommendations are inventory signals only.

Forms observed:

- unsupported fact counts;
- fact conflict counts;
- contradiction counts;
- graph issue counts;
- stale fact and refresh recommendation counts;
- unknown capability counts;
- caveats about count meaning and non-execution.

Classification: **structured counts plus structured caveat list**.

#### Authority representation

Projection Integrity Summary exposes authority mostly as aggregate source families. The builder derives counts from existing evidence summary, fact conflicts, contradictions, graph issues, stale fact data, refresh recommendations, and capability inventory. It preserves projection version and last event id, but it does not expose individual evidence rows, contradiction rows, graph issues, or capability records in the summary itself.

Authority visibility level: **surface-level**, with minimal item-level visibility.

#### Limitations

This surface preserves uncertainty strongly for aggregate integrity status but exposes authority weakly. It is a key counterexample: strong uncertainty visibility, low provenance visibility.

### Source Navigation

#### Uncertainty representation

Source Navigation has minimal uncertainty visibility. It only projects existing `defines` and `imports` fact supports. The formatter renders `No source facts matched.` when there are no matches. The module docstring and matching code enforce a boundary: it does not inspect files, parse source, ingest observations, or infer behavior, reachability, or ownership.

Forms observed:

- no-match result;
- bounded row limit for path/module lookups;
- implementation boundary excluding behavior/reachability/ownership inference.

Classification: **implicit plus formatter-only** for no-match uncertainty; boundary is implementation/docstring backed.

#### Authority representation

Source Navigation exposes authority at the row level for exact symbol lookups. Rows include subject, predicate, value, path, support count, representative fact id, and representative support id. For bounded path/module lookups, the formatter shows counts and a support summary but hides per-row representative fact/support details to keep the view bounded.

Authority visibility level: **item-level for exact rows**, **surface/count-level for bounded rows**.

#### Limitations

Source Navigation is a counterexample in the opposite direction from Projection Integrity Summary: it can expose strong item-level source support for matches, but it preserves little uncertainty beyond no-match prose and the narrow implementation boundary.

### Reasoning Path Audit

#### Uncertainty representation

Reasoning Path Audit has first-class structured uncertainty. The dataclass includes `unknowns`, and the builder records an unknown derivation when no evidence, intermediate conclusions, derived conclusions, consumers, or story impact are found. The formatter changes the title to `Reasoning Path Incomplete` when unknowns are present.

Forms observed:

- incomplete derivation marker;
- no derivation evidence currently available;
- formatter-visible incomplete title;
- read-only boundary.

Classification: **structured**, with formatter reinforcement.

#### Authority representation

Reasoning Path Audit exposes authority across a derivation chain. It collects evidence from ownership discrepancies, derives intermediate conclusions, derives capability-needs conclusions, records consuming surfaces such as capability needs, pressure audit, privilege discovery, and Operational Story, and records story impact when the operational story includes the subject/domain.

Authority visibility level: **chain-level**, with item-level dictionaries for evidence, intermediate conclusions, derived conclusions, consumers, and story impact.

#### Limitations

The chain is implementation-backed for the specific diagnostic surfaces it knows. It does not claim a general repository reasoning graph. Its authority visibility is strong inside this bounded derivation path and unsupported outside it.

### Selection Path Audit

#### Uncertainty representation

Selection Path Audit has first-class structured uncertainty. It returns `selected="unknown"`, `selection_factors=["unknown"]`, an outcome reason, and an `unknowns` row when the target is not an implemented selection surface. If no pressure candidates exist for an implemented target, it records candidate-set uncertainty.

Forms observed:

- unsupported target marker;
- unknown selected value;
- unknown selection factors;
- missing candidate set;
- no implementation-backed selection evidence.

Classification: **structured**.

#### Authority representation

Selection Path Audit exposes selection authority through candidate rows, selection factors, non-selected candidate reasons, selected evidence from pressure audit, and outcome. It preserves the implemented rule that pressure candidates are ordered by descending score and then category name.

Authority visibility level: **item-level and selection-rule-level**, with partial chain visibility back to pressure audit evidence.

#### Limitations

Selection Path Audit exposes selection mechanics well for current focus/primary pressure, but unsupported targets return structured uncertainty rather than inferred selection authority. It does not prove broader selection logic outside the implemented target families.

## Recurring uncertainty families

The implementation evidence supports these recurring uncertainty families:

| Family | Evidence surfaces | Current representation |
| --- | --- | --- |
| Missing evidence / unsupported support | Projection Integrity Summary, Reasoning Path Audit, Selection Path Audit | Counts, unknown rows, unsupported target/outcome reasons |
| No matching material | Inquiry Orientation, Source Navigation | Fixed uncertainty text or formatter no-match text |
| Unsupported scope / target | Inquiry Orientation, Source Navigation, Selection Path Audit | Authority-boundary prose, predicate restrictions, unknown selection target |
| Incomplete derivation | Reasoning Path Audit | Structured unknown row plus incomplete title |
| Unknown outcome / impact | Operational Story, Projection Integrity Summary | Unknown rows, impact metrics, unknown capability counts |
| Missing authority / insufficient provenance | Projection Integrity Summary, Source Navigation bounded mode | Aggregate counts or support summary without full row provenance |

## Recurring authority representations

The implementation evidence supports these recurring authority forms:

| Authority form | Evidence surfaces | Visibility level |
| --- | --- | --- |
| Consumed surfaces | Operational Story, Reasoning Path Audit, Selection Path Audit | Surface-level |
| Consumed facts/supports | Inquiry Orientation, Source Navigation | Item-level |
| Evidence rows | Reasoning Path Audit, Selection Path Audit, Source Navigation | Item-level |
| Source references / support identities | Inquiry Orientation, Source Navigation | Item-level |
| Authority summaries | Projection Integrity Summary, Operational Story | Surface-level / aggregate |
| Support / derivation chains | Reasoning Path Audit, Selection Path Audit | Chain-level or partial chain-level |

## Strong examples

### Strong uncertainty preservation

- Projection Integrity Summary preserves uncertainty strongly through typed aggregate counts and caveats. It is especially strong for unsupported, stale, conflicted, contradicted, and unknown-capability states.
- Reasoning Path Audit preserves derivation uncertainty strongly through structured unknowns and an incomplete-path rendering.
- Selection Path Audit preserves target and candidate-set uncertainty strongly by returning unknown selected values, unknown factors, and explicit outcome reasons rather than inventing selection authority.
- Operational Story preserves uncertainty strongly when composed inputs fail to identify pressure, capability needs, or impact.

### Strong authority visibility

- Reasoning Path Audit is the strongest chain-level authority example because it separates evidence, intermediate conclusions, derived conclusions, consumers, and story impact.
- Selection Path Audit is strong for implemented selection authority because it exposes candidates, ranking rule, non-selected reasons, selected evidence, and outcome.
- Source Navigation is strong for item-level source support on exact rows because it exposes representative fact and support identities.
- Inquiry Orientation is strong for item-level related-material support because it exposes why-related rationale and support text for each related material row.

## Weak examples and counterexamples

### Preserves uncertainty strongly but exposes little authority

Projection Integrity Summary is the clearest case. It preserves many uncertainty/integrity conditions as counts and caveats, but the summary itself does not expose item provenance for the underlying unsupported facts, contradictions, graph issues, stale facts, or capability inventory rows.

### Exposes authority strongly but preserves little uncertainty

Source Navigation is the clearest case. Exact-match rows expose source-support identity, representative fact id, path, subject, predicate, and support count. But uncertainty is mostly a no-match formatter sentence plus the implementation boundary that no behavior/reachability/ownership inference is performed.

### Uncertainty only formatter prose

Source Navigation's `No source facts matched.` is formatter-only uncertainty. The view has query, definitions, and imports, but no structured `unknowns`, `limitations`, or `caveats` field.

### Authority visibility inferred by investigation prose rather than direct implementation evidence

Any claim that Projection Integrity Summary exposes full provenance for each integrity count would be unsupported by the summary implementation. The builder consumes existing authoritative structures, but the returned summary exposes aggregate counts and caveats rather than item provenance. Similarly, Source Navigation's module boundary supports `defines` and `imports` source-fact navigation; claims about behavior, runtime reachability, or ownership would be inferred beyond implementation evidence.

## Important distinctions

### Uncertainty vs limitation vs boundary vs negative authority

- **Uncertainty** is the visible absence, incompleteness, unknown value, no-match result, or incomplete derivation. Examples: Operational Story unknowns, Reasoning Path unknown derivation, Selection Path unknown target, Projection Integrity unknown capability counts.
- **Limitation** is a statement about what the current surface cannot conclude from its data. Examples: Inquiry Orientation says lexical overlap is not semantic interpretation; Projection Integrity Summary says missing evidence does not mean false.
- **Boundary** is the authority/mutation contract. Examples: read-only boundary dictionaries on Operational Story, Reasoning Path Audit, and Selection Path Audit; Projection Integrity Summary's read-only module contract; Source Navigation's predicate/source-fact boundary.
- **Negative authority** is an explicit refusal to promote a result beyond its source authority. Inquiry Orientation is strongest here: the note is not a fact, goal, tool need, requirement, decision, plan, authorization, command, or runtime instruction.

### Authority visibility vs provenance visibility vs support visibility vs derivation visibility

- **Authority visibility** identifies which implemented surface or source family is allowed to speak. Operational Story and Projection Integrity Summary are strong at surface-family authority.
- **Provenance visibility** identifies the concrete source/support row or event-like origin. Source Navigation and Inquiry Orientation expose this more directly through representative support identities and support strings.
- **Support visibility** shows what material supports a row or conclusion. Selection Path Audit and Reasoning Path Audit expose support/evidence dictionaries.
- **Derivation visibility** shows how evidence becomes intermediate or derived conclusions and consumers. Reasoning Path Audit is the strongest current example.

### Structured visibility vs formatter visibility

Structured visibility exists when uncertainty or authority is present in returned dataclasses/JSON dictionaries. Formatter visibility exists only in rendered text. Operational Story, Reasoning Path Audit, Selection Path Audit, and Projection Integrity Summary carry structured uncertainty. Inquiry Orientation carries semi-structured prose fields. Source Navigation carries authority structurally in rows but no structured uncertainty field; its no-match uncertainty is formatter-only.

## Cross-surface comparison

Uncertainty and authority visibility are **independent concerns that often appear in paired implementation patterns**.

They are independent because a surface can preserve one strongly while weakening the other:

- Projection Integrity Summary: strong uncertainty, weak item provenance.
- Source Navigation: strong item authority for matches, weak structured uncertainty.

They are paired when a builder exposes both the answer material and why the answer cannot exceed its source authority:

- Inquiry Orientation pairs related material with uncertainty and authority boundary.
- Reasoning Path Audit pairs derivation evidence with unknown derivation rows and a read-only boundary.
- Selection Path Audit pairs candidate/selection evidence with unknown target and candidate-set uncertainty.
- Operational Story pairs composed operational evidence with unknowns and boundary.

## Implementation shapes that preserve both

The recurring successful shape is:

```text
dataclass view
+
builder over existing read models
+
explicit answer material fields
+
explicit unknowns/caveats/uncertainty field
+
evidence/support/consumer fields
+
read-only boundary
+
formatter that renders the same fields without adding new authority
```

Reasoning Path Audit and Selection Path Audit most clearly fit this shape. Operational Story also fits it, though authority is more summarized. Inquiry Orientation fits a lighter version using fixed uncertainty and authority-boundary strings plus related-material rows.

## Implementation shapes that preserve one while weakening the other

### Aggregate summary shape

```text
source views
-> aggregate counts
-> caveats
```

This preserves uncertainty well but weakens item provenance. Projection Integrity Summary is the example.

### Narrow lookup shape

```text
preserved facts
-> matching rows
-> row support identities
-> no-match formatter text
```

This preserves authority for matches but weakens structured uncertainty. Source Navigation is the example.

### Composed answer shape

```text
multiple surfaces
-> selected focus/story/path
-> supporting summaries
-> unknowns
-> boundary
```

This balances the two, but may summarize authority rather than expose complete provenance. Operational Story is the example.

## Supported conclusions

1. Uncertainty is represented today as a mixture of structured unknown rows, aggregate counts, caveat lists, fixed uncertainty prose, no-match formatter text, unsupported target markers, and read-only/non-inference boundaries.
2. Authority is represented today as consumed surface names, evidence dictionaries, support strings, representative fact/support identities, candidate rows, consumer rows, derivation stages, and aggregate authority summaries.
3. The surfaces that preserve uncertainty best are Projection Integrity Summary, Reasoning Path Audit, Selection Path Audit, and Operational Story.
4. The surfaces that expose authority best are Reasoning Path Audit for chain-level authority, Selection Path Audit for selection authority, and Source Navigation/Inquiry Orientation for item-level support authority.
5. Uncertainty and authority visibility are not the same concern. They can be paired, but the implementation contains clear counterexamples where one is strong and the other weak.
6. The best evidence-backed model is not a new framework. It is the existing bounded read-only view pattern: builders over existing authorities return bounded answer material, explicit unknown/caveat/limitation data, visible support/authority, and a read-only boundary.

## Unsupported conclusions

The implementation evidence does **not** support these stronger claims:

- that the repository has a general uncertainty schema across all answer surfaces;
- that all authority is exposed at item or chain level;
- that all uncertainty is structured rather than formatter prose;
- that Projection Integrity Summary exposes full provenance for each count;
- that Source Navigation proves behavior, reachability, ownership, runtime execution, or semantic importance;
- that Inquiry Orientation interprets operator intent;
- that Reasoning Path Audit is a general reasoning graph beyond its implemented diagnostic surfaces;
- that Selection Path Audit explains arbitrary repository selection logic.

## Recommended next step

The smallest implementation-backed next step, if future work asks for operational change, is to choose one existing surface and strengthen tests around its already-implemented uncertainty/authority behavior rather than introduce a new concept. The best candidates are:

1. **Source Navigation**, if the pressure is structured uncertainty, because its no-match uncertainty is currently formatter-only.
2. **Projection Integrity Summary**, if the pressure is authority visibility, because it preserves uncertainty strongly but exposes authority only as aggregate counts and source-family summaries.
3. **Reasoning Path Audit**, if the goal is to preserve the strongest paired pattern, because it already has structured uncertainty and chain-level authority visibility.

For this characterization task, no implementation change is recommended.
