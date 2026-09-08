# Comparative Answer Surface Characterization

## Question

Which existing answer-responsible surfaces most completely preserve the currently supported implementation shape?

This is characterization only. It does not propose `AnswerInventory`, an answer-contract schema, metadata registry, runtime registration, a new visibility system, or a new answer framework. Repository implementation evidence wins over investigation terminology.

## Method and evidence boundary

Reviewed implementation and prior characterization for these surfaces:

- Operational Story
- Inquiry Orientation
- Projection Integrity Summary
- Source Navigation
- Reasoning Path Audit
- Selection Path Audit

The comparison uses the implementation-backed shape already characterized in prior reports:

```text
bounded read-only view
+
builder over existing authorities
+
answer material
+
uncertainty visibility
+
authority visibility
+
authority boundary
```

For this report, the compared dimensions are:

- **bounded view**: an explicit data shape or view contract that narrows scope;
- **answer material**: fields or formatter sections that answer a bounded question rather than only listing raw records;
- **authority visibility**: visible evidence, source surfaces, support, candidates, consumers, or derivation inputs;
- **uncertainty visibility**: unknowns, caveats, no-match explanation, incomplete-result text, or unsupported-target status;
- **authority boundary**: explicit statement or data field that limits what the surface is allowed to decide, record, mutate, infer, or promote.

Strength labels are comparative:

- **Strong**: implemented as first-class data and rendered or serialized.
- **Medium**: implemented but narrower, delegated, formatter-heavy, or distributed across several places.
- **Weak**: present mainly as prose, absence text, or incidental behavior.
- **Absent**: not found for the dimension in answer-surface form.

## Comparative matrix

| Surface | Family | Bounded view | Answer material | Authority visibility | Uncertainty visibility | Authority boundary | Overall characterization |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Operational Story | composition | Strong | Strong | Medium-strong | Strong | Strong | Strongest broad answer surface; best balanced across major dimensions. |
| Inquiry Orientation | orientation / matching | Strong | Strong narrow | Strong narrow | Strong | Strong | Strongest narrow orientation surface; excellent boundary and uncertainty. |
| Projection Integrity Summary | aggregation | Strong | Strong narrow | Medium | Strong | Medium | Uncertainty-heavy aggregate answer; boundary exists but is split between docstring and caveats. |
| Source Navigation | navigation / lookup | Strong narrow | Medium-strong narrow | Strong | Weak | Medium | Authority-heavy navigation answer; weak structured uncertainty. |
| Reasoning Path Audit | derivation audit | Strong | Strong | Strong | Medium | Strong | Strong derivation surface; authority and boundary are strong, uncertainty is target-dependent. |
| Selection Path Audit | selection audit | Strong | Strong | Strong | Strong | Strong | Strong selection surface for implemented targets; returns explicit unknown for unsupported targets. |

## Surface characterizations

### Operational Story

**Family:** composition.

Operational Story is the strongest current broad answer surface. Its dataclass contains answer sections rather than only diagnostic rows: `focus`, `pressure`, `supporting_evidence`, `capabilities`, `constraints`, `correlation_gaps`, `impact`, `recent_changes`, `observed_outcomes`, `investigation_path`, `unknowns`, and `boundary`.

Implementation evidence:

- The builder consumes existing authorities: pressure audit, capability needs, privilege discovery, correlation audit, impact audit, investigation-path audit, and projected State.
- The answer material is composed into current focus, primary pressure, supporting evidence, missing capabilities, access constraints, correlation gaps, impact, recent changes, observed outcomes, and investigation path.
- Uncertainty is structured as `unknowns` for no pressure, no capability needs, and unknown impact.
- The authority boundary is structured and rendered: read-only view, no fact recording, no event-ledger writes, and no cluster mutation.

Strengths:

- Best simultaneous preservation of answer material, uncertainty visibility, and authority boundary.
- Strong answer breadth: it joins several existing visibility surfaces into a current operational story.
- Strong answer strength despite breadth because its builder and formatter preserve the read-only boundary and unknowns.

Limitations:

- Authority visibility is strong at the consumed-surface level, but not always deep at item-level provenance for every rendered sentence.
- It is not a general explanation framework; it composes a bounded operational story.

### Inquiry Orientation

**Family:** orientation / matching.

Inquiry Orientation is a narrow but strong answer surface. Its view contains preserved inquiry prose, related material, uncertainty, and authority boundary. Narrowness is not weakness here: the surface states that it performs deterministic lexical overlap against already projected read models and source-navigation material.

Implementation evidence:

- Inquiry notes are stored outside the event ledger for this probe, and rendering does not mutate projected state, append events, call providers, execute tools, or create facts, goals, needs, decisions, proposals, or plans.
- `InquiryOrientationView` carries the note, related material, uncertainty text, and authority boundary.
- The builder tokenizes a preserved inquiry note, matches projected fact supports and Source Navigation rows, deduplicates related material, caps output, and selects match/no-match uncertainty.
- The formatter always renders uncertainty and authority boundary sections.

Strengths:

- One of the clearest authority-boundary surfaces: it refuses promotion of operator prose into facts, claims, goals, requirements, decisions, plans, authorizations, commands, runtime instructions, intent, concern, recommended action, or next safe move.
- Strong uncertainty visibility for both matches and no matches.
- Strong answer strength within a narrow orientation question.

Limitations:

- It is lexical orientation, not semantic intent understanding.
- Authority depth is intentionally narrow: it exposes why material is related, not full provenance or behavioral correctness.

### Projection Integrity Summary

**Family:** aggregation.

Projection Integrity Summary is a strong narrow aggregation surface. It summarizes existing projection-integrity signals as counts and caveats. It is answer-responsible for aggregate integrity visibility, not for truth, correctness, health, execution, repair, or provider availability.

Implementation evidence:

- The dataclass carries unsupported facts, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, capability-state counts, caveats, projection version, and last event id.
- The builder aggregates existing evidence summary, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, and capability inventory.
- Default caveats explicitly distinguish integrity counts from truth/correctness judgments and state that refresh recommendations do not execute refresh or verification.

Strengths:

- Strong uncertainty-heavy surface: caveats are first-class data and consistently attached to the summary.
- Strong bounded aggregation: it counts already-derived integrity signals and preserves their limited meaning.
- Good example of answer strength without broad narrative breadth.

Limitations:

- Authority visibility is medium: counts expose categories and projection version, but not always the underlying item chain in the summary itself.
- Authority boundary is medium: the boundary is real, but split between module docstring/class docstring and caveats rather than a first-class `boundary` field like Operational Story, Reasoning Path Audit, or Selection Path Audit.

### Source Navigation

**Family:** navigation / lookup.

Source Navigation is an authority-heavy narrow surface. It answers where preserved source facts define or import a query. It is strongly bounded to existing `imports` and `defines` facts and refuses source parsing, file inspection, ingestion, behavior inference, reachability inference, or ownership inference.

Implementation evidence:

- The module docstring restricts input authority to preserved repository source facts and says it does not inspect files, parse source, ingest observations, or infer behavior, reachability, or ownership.
- `SourceNavigationView` is bounded to one query with definition and import rows.
- Rows include subject, predicate, value, path, support count, representative fact id, and representative support id.
- Matching is syntactic and limited to definition values, final symbols, subjects, and preserved path dimensions.
- Formatter exposes definitions/imports, support counts, representative fact/support identifiers for exact lookups, and “No source facts matched” for misses.

Strengths:

- Strong authority visibility for preserved source facts: path, module/subject, support counts, representative fact, and representative support are exposed.
- Strong authority boundary at the module/matching level.
- Good example that a narrow lookup can still be answer-responsible when match semantics and non-authority are implementation-bounded.

Limitations:

- Weak uncertainty visibility compared with other surfaces: no-match text exists, but there is no first-class uncertainty field.
- Answer material is narrow and navigational; it does not compose behavioral explanation.
- Boundary is distributed across docstring, predicates, matching logic, and formatter behavior rather than a structured boundary field.

### Reasoning Path Audit

**Family:** derivation audit.

Reasoning Path Audit is a strong derivation surface for implemented operational conclusions. It exposes evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and boundary.

Implementation evidence:

- The dataclass contains domain, subject, evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and read-only boundary.
- The builder consumes ownership discrepancies, capability needs, pressure audit, privilege discovery, and Operational Story.
- The builder records evidence, intermediate conclusions, derived capability needs, consumers, privilege boundaries, and Operational Story impact when the target is matched.
- If no derivation evidence is available, it returns an explicit unknown.
- The formatter renders observed evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and boundary.

Strengths:

- Strong authority visibility: evidence, surfaces, consumers, and story impact are visible.
- Strong boundary visibility: read-only, no recording, no event-ledger writes, no cluster mutation.
- Strong answer material for derivation questions.

Limitations:

- Uncertainty visibility is medium: explicit unknowns exist, but mostly for absence of derivation evidence, not for grading partial chain quality.
- Matching is broad string matching over implemented diagnostic outputs; the surface explains implemented derivation, not universal reasoning.

### Selection Path Audit

**Family:** selection audit.

Selection Path Audit is the strongest selection-family answer surface for currently implemented targets. It explains current-focus and primary-pressure selection by exposing the selected item, candidates, factors, non-selected candidates, evidence, outcome, unknowns, and boundary.

Implementation evidence:

- The dataclass carries selected item, candidates, selection factors, non-selected candidates, evidence, outcome, unknowns, and read-only boundary.
- The builder consumes pressure audit and Operational Story.
- Implemented targets are current focus, primary pressure, and pressure-category matches.
- For unsupported targets, it returns selected=`unknown`, candidate context, unknown selection factors, an outcome reason, and explicit unknowns.
- The implemented selection explanation preserves candidate rank, score, reason, evidence, non-selection reasons, and outcome.

Strengths:

- Best simultaneous preservation in the selection family: answer material, authority visibility, uncertainty visibility, and boundary are all first-class.
- Clear distinction between implemented selection explanation and unsupported target unknowns.
- Strong example of answer strength over narrow scope.

Limitations:

- It is strong only for implemented focus/pressure selection surfaces.
- It does not create or alter selection behavior; it explains current implementation evidence.

## Answer-surface families

Distinct families do exist, but only as implementation-characterization labels, not as a proposed registry or framework.

| Family | Surfaces | Implementation pattern | Dimensions usually strongest | Dimensions usually weaker |
| --- | --- | --- | --- | --- |
| Composition | Operational Story | Compose multiple existing visibility surfaces into a bounded operator answer. | Answer material, uncertainty, boundary, breadth. | Item-level authority depth. |
| Orientation / matching | Inquiry Orientation | Relate preserved operator prose to already projected material using deterministic overlap. | Boundary, uncertainty, boundedness. | Semantic depth and authority depth. |
| Aggregation | Projection Integrity Summary | Aggregate existing integrity signals into counts and caveats. | Uncertainty/caveats, bounded counts. | Deep authority lineage and first-class boundary. |
| Navigation / lookup | Source Navigation | Select preserved source facts for one query. | Authority visibility and narrow boundary. | Structured uncertainty and answer breadth. |
| Derivation audit | Reasoning Path Audit | Trace implemented derivation from evidence to conclusions and consumers. | Authority visibility, answer material, boundary. | Graded uncertainty. |
| Selection audit | Selection Path Audit | Trace implemented selection from candidates to selected outcome. | Balance across answer, authority, uncertainty, boundary. | Breadth beyond implemented targets. |

These families are meaningful as observed implementation patterns. They should not be treated as repository knowledge categories unless future implementation makes them durable.

## Strongest and most balanced surfaces

### Strongest overall

1. **Operational Story** — strongest broad composition answer. It preserves all major elements and has the best breadth while retaining explicit unknowns and boundary.
2. **Selection Path Audit** — strongest narrow balanced surface. It preserves all major elements simultaneously and handles unsupported targets with explicit unknowns.
3. **Reasoning Path Audit** — strong derivation answer with excellent authority visibility and boundary; uncertainty is less rich than Selection Path Audit.
4. **Inquiry Orientation** — very strong narrow orientation surface; answer strength is high because its authority boundary is explicit and enforced.

### Balanced surfaces

- **Operational Story** is the most balanced broad surface.
- **Selection Path Audit** is the most balanced narrow trace surface.
- **Inquiry Orientation** is balanced within its intentionally narrow lexical-orientation scope.

### Surfaces preserving all major implementation-shape elements simultaneously

- **Operational Story**: bounded view, answer material, authority visibility, uncertainty visibility, authority boundary.
- **Inquiry Orientation**: bounded view, answer material, authority visibility, uncertainty visibility, authority boundary.
- **Reasoning Path Audit**: bounded view, answer material, authority visibility, uncertainty visibility, authority boundary.
- **Selection Path Audit**: bounded view, answer material, authority visibility, uncertainty visibility, authority boundary.

Projection Integrity Summary nearly satisfies all elements, but boundary is not a first-class field. Source Navigation nearly satisfies all elements, but structured uncertainty is weak.

## Specialized surfaces

### Authority-heavy

- **Source Navigation**: strongest narrow authority exposure for preserved source facts.
- **Reasoning Path Audit**: strongest derivation authority exposure across evidence, conclusions, consumers, and story impact.
- **Selection Path Audit**: strong selection authority through candidates, scores, factors, non-selected reasons, and evidence.

### Uncertainty-heavy

- **Projection Integrity Summary**: caveats are first-class and central to the answer.
- **Inquiry Orientation**: match/no-match uncertainty is explicit and rendered every time.
- **Operational Story**: structured unknowns cover missing pressure, capability needs, and unknown impact.
- **Selection Path Audit**: unsupported targets and absent candidates produce explicit unknowns.

### Answer-heavy

- **Operational Story**: broadest answer material and strongest composition.
- **Reasoning Path Audit**: strongest derivation answer material.
- **Selection Path Audit**: strongest selection answer material.
- **Projection Integrity Summary**: strongest compact aggregate answer material.

### Boundary-heavy

- **Inquiry Orientation**: strongest negative promotion boundary.
- **Operational Story**: clear read-only/no-record/no-ledger/no-mutation boundary.
- **Reasoning Path Audit** and **Selection Path Audit**: structured read-only audit boundaries.
- **Source Navigation**: strong non-inference boundary, but distributed rather than structured.

## Recurring successful patterns

### Pattern 1: answer material + explicit unknowns + visible evidence + boundary

Best examples:

- Operational Story
- Reasoning Path Audit
- Selection Path Audit

This pattern explains the strongest broad and trace surfaces. The answer is not just formatted prose: it is built from existing authorities, preserves evidence/candidates/consumers, records unknowns, and renders a no-mutation boundary.

### Pattern 2: answer material + caveats + bounded aggregation

Best example:

- Projection Integrity Summary

This pattern is strong where the answer is aggregate rather than narrative. It preserves uncertainty through caveats, not through a derivation chain.

### Pattern 3: query-bounded lookup + support identifiers + non-inference boundary

Best example:

- Source Navigation

This pattern is strong for authority visibility and weak for uncertainty richness. It succeeds as a narrow answer surface because it names exactly which source facts can answer the query and refuses behavioral inference.

### Pattern 4: preserved operator material + deterministic relatedness + negative promotion boundary

Best example:

- Inquiry Orientation

This pattern succeeds by preventing presentation vocabulary or operator prose from silently becoming repository knowledge.

## Counterexamples and caution cases

### Source Navigation: authority strong, uncertainty weak

Source Navigation appears strong because it exposes source authority well, but it does not preserve uncertainty as first-class data. “No source facts matched” is useful, but not equivalent to structured uncertainty or caveats.

### Projection Integrity Summary: uncertainty strong, authority depth moderate

Projection Integrity Summary appears very strong because caveats are first-class. However, the summary itself compresses authority into counts and source categories. It is strongest for aggregate integrity answers, not item-level authority depth.

### Operational Story: broad answer, shallower item lineage

Operational Story is broad and balanced, but authority visibility is mostly at consumed-surface and rendered-field level. A broad answer surface can be strong without proving deep provenance for every sentence; answer strength and answer breadth are distinct.

### Reasoning Path Audit: derivation-specific, not universal reasoning

Reasoning Path Audit exposes implemented derivation paths. It should not be read as a general reasoning model. Its answer responsibility is bounded to currently implemented diagnostic chains and matching behavior.

### Strong answer surface is meaningful, but only comparatively

The category is meaningful when it refers to surfaces that simultaneously preserve answer material, authority visibility, uncertainty visibility, and boundary. It is not meaningful as a global architectural type independent of implementation evidence.

## Important distinctions

### Answer strength vs answer breadth

- Operational Story has both relatively high breadth and high strength.
- Inquiry Orientation and Source Navigation are narrow but still strong within their scopes.
- Projection Integrity Summary is narrow and aggregate but strong because caveats preserve meaning.

A narrow surface can be stronger than a broad surface if it enforces its boundary and uncertainty more clearly.

### Authority visibility vs authority depth

- Source Navigation has strong authority visibility for source facts and support identifiers.
- Operational Story has visible composing authorities, but less item-level depth.
- Projection Integrity Summary exposes integrity categories and counts, but not full item chains.
- Reasoning Path Audit and Selection Path Audit provide deeper authority traces within their audit domains.

Authority visibility means the surface shows where the answer came from. Authority depth means it preserves enough chain detail to inspect each step. They are related but not identical.

### Uncertainty visibility vs boundary visibility

- Projection Integrity Summary has strong uncertainty visibility through caveats, while boundary is less structured.
- Source Navigation has a strong authority boundary, while uncertainty is weakly structured.
- Inquiry Orientation preserves both: uncertainty text and negative authority boundary are separate fields/sections.

Uncertainty says what the answer does not know or cannot establish. Boundary says what the surface is not authorized to decide, mutate, promote, or infer.

## Supported conclusions

1. **The most complete current surfaces are Operational Story, Selection Path Audit, Inquiry Orientation, and Reasoning Path Audit.**
2. **Operational Story is the strongest broad answer-responsible surface.**
3. **Selection Path Audit is the strongest narrow balanced surface for selection questions.**
4. **Source Navigation specializes in authority visibility.**
5. **Projection Integrity Summary specializes in uncertainty/caveat preservation.**
6. **Inquiry Orientation specializes in negative authority boundary and uncertainty around relatedness.**
7. **Distinct families exist as implementation patterns: composition, orientation/matching, aggregation, navigation/lookup, derivation audit, and selection audit.**
8. **The strongest recurring model is a bounded read-only view built over existing authorities, with answer material, visible evidence or chain/candidate support, explicit unknowns or caveats, and an explicit authority boundary.**

## Unsupported conclusions

The implementation evidence does not support these conclusions:

- There is a repository-wide answer framework.
- There is or should be an `AnswerInventory`.
- There is an answer-contract schema or runtime registration mechanism.
- All strong answer surfaces need the same data schema.
- Source Navigation understands behavior, reachability, ownership, or source correctness.
- Inquiry Orientation understands operator intent or recommended next action.
- Projection Integrity Summary decides truth, correctness, health, repair, or provider availability.
- Reasoning Path Audit explains reasoning beyond implemented diagnostic derivation chains.
- Selection Path Audit explains selection beyond implemented focus/pressure targets.

## Recommended next step

If future work needs one implementation-backed improvement, improve tests or documentation for one already-implemented surface rather than introducing a new framework. The best candidate is **Operational Story**, because it is the strongest broad composition surface and already preserves most major answer-shape elements. A narrow alternative is **Selection Path Audit**, because it most cleanly demonstrates simultaneous answer material, authority visibility, uncertainty visibility, and boundary within one bounded selection problem.
