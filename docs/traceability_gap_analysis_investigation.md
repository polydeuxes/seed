---
status: investigation
scope: traceability gap analysis as a repository capability
created: 2026-06-21
---

# Traceability Gap Analysis Investigation

## Status

Investigation only. This document does not implement a diagnostic surface, CLI
flag, runtime behavior, policy, ontology, architecture, recommendation system,
gap scoring system, planning system, registry, persistence model, or cluster
mutation. Repository authority wins over this investigation.

The purpose is understanding whether **traceability gap analysis** is a meaningful
repository capability: whether Seed can recognize when an explanation exists but
is incomplete because an explanatory layer is missing.

## Repository Evidence Reviewed

Primary evidence reviewed:

- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/history_brief.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `docs/candidate_baseline_traceability_investigation.md`
- `docs/reference_selection_traceability_investigation.md`
- `docs/unified_derivation_architecture_investigation.md`
- `docs/change_readiness_baseline_concept_investigation.md`
- `docs/baseline_acceptance_authority_audit.md`
- `docs/comparison_reference_authority_reconciliation.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/operational_story_implementation_characterization.md`
- tests for `reasoning_path`, `selection_path`, `history_brief`,
  `reference_selection`, diagnostic inventory, and diagnostic shape audit.

This review treats implementation and tests as stronger authority than
investigation vocabulary. Existing investigations are evidence of recurring
pressure and repository reasoning style; they are not, by themselves, authority
for new runtime concepts.

## Working Description

A **traceability gap** is a repository-observable condition where a conclusion,
comparison, selection, narrative, audit result, or visibility surface exists, but
one necessary explanatory layer is absent, unknown, unsupported, or outside the
current authority boundary.

A traceability gap is not simply that Seed lacks a feature. It is specifically
about partial explainability:

```text
some result is visible
some support path is visible
an operator or repository question still cannot be answered
because a distinct trace layer is missing
```

Examples that repository evidence supports as historical pattern, not as proof of
a general implementation:

```text
conclusion existed
    derivation visibility was missing
    reasoning_path made derivation partially visible

conclusion/focus existed
    selection visibility was missing
    selection_path made candidate and selection rationale visible

historical comparison existed
    reference visibility was missing
    reference_selection made the selected comparison reference visible for history
```

The common form is:

```text
visible output
    -> implicit dependency on another explanatory layer
    -> investigation or implementation exposes that layer
    -> remaining authority boundary is preserved
```

## Candidate Traceability-Gap Observations

### 1. Derivation gap

A derivation gap exists when Seed has a conclusion but cannot explain why the
conclusion exists in terms of source evidence, intermediate conclusions, derived
conclusions, consumers, and unknowns.

`reasoning_path` is implementation evidence that this gap was meaningful. Its
model explicitly carries evidence, intermediate conclusions, derived conclusions,
consumers, story impact, unknowns, and a read-only boundary. That shape is not a
new ontology here; it is evidence that derivation was a missing explanatory layer
for operational conclusions.

Supported observation:

```text
Conclusion exists.
Evidence and intermediate support may exist in separate diagnostics.
Without derivation traceability, the conclusion is only partially explainable.
```

Unsupported conclusion:

```text
Every Seed conclusion already has a complete derivation path.
```

The implementation is scoped to implemented diagnostic surfaces and explicitly
returns unknowns when no implementation-backed selection or derivation evidence is
available.

### 2. Selection gap

A selection gap exists when Seed can show the selected conclusion, focus, or item,
but cannot explain the candidate set, selection factors, non-selected candidates,
evidence, outcome, and unknowns.

`selection_path` is implementation evidence that selection is a distinct layer
from derivation. It explains why an operational result was selected without
changing selection behavior and without converting the explanation into cluster
truth.

Supported observation:

```text
Conclusion selected.
Selection factors absent or implicit.
Explanation is incomplete even if derivation is visible.
```

Unsupported conclusion:

```text
Selection traceability is identical to derivation traceability.
```

Repository evidence separates them: `reasoning_path` explains why a conclusion
exists, while `selection_path` explains why one candidate became the selected
operational focus.

### 3. Historical comparison gap

A historical comparison gap exists when Seed can say what changed but cannot
fully explain the comparison reference, confidence, causation boundary, or
unsupported historical conclusion.

`history_brief` demonstrates partial historical explainability. It reports
changes, stability, repository context, historical confidence, unsupported
conclusions, and explicitly preserves the causation boundary. That makes history
more explainable, but it also shows how comparison can remain partial when the
reference or authority is unclear.

Supported observation:

```text
Historical comparison exists.
Change/stability visible.
Causation or reference significance may still be unproven.
```

Unsupported conclusion:

```text
A visible historical change establishes why the change matters, what reference
should be accepted, or what expectation was violated.
```

### 4. Reference-selection gap

A reference-selection gap exists when comparison exists but the meaningful
reference is implicit, unavailable, or not authority-bounded.

`reference_selection` is implementation evidence that reference visibility is a
distinct layer. For the history domain, it reports the selected reference,
selection rationale, alternative references, authority boundary, limitations, and
read-only/non-mutating status. For unsupported domains, it keeps the unknown state
explicit instead of inventing reference authority.

Supported observation:

```text
Comparison exists.
Reference is necessary for interpretation.
Reference choice and alternatives need explanation.
```

Unsupported conclusion:

```text
Reference selection creates accepted baselines, expectations, lifecycle policy,
or general reference authority.
```

The implementation explicitly limits itself to visibility and does not create
accepted baselines or expectations.

### 5. Authority gap

An authority gap exists when Seed can show evidence, derivation, selection, and
reference, but cannot show what authority permits promotion, acceptance,
should-bearing interpretation, or mutation.

This is the strongest candidate for a future self-recognized traceability gap,
but current evidence supports it only as an investigation conclusion and boundary
pattern, not as an implemented capability.

Supported example shape:

```text
Conclusion exists.
Derivation visible.
Selection visible.
Reference visible.
Authority visibility absent.
```

Supported only as a candidate observation:

- Candidate-baseline and reference-selection investigations repeatedly separate
  plausible comparison references from accepted baselines and expectations.
- Baseline authority investigations distinguish evidence support from authority
  to accept a baseline or create should-bearing expectations.
- Diagnostic implementations repeatedly preserve read-only boundaries and avoid
  cluster mutation.

Unsupported conclusion:

```text
Seed currently has a general authority-gap analyzer.
```

Repository evidence supports authority boundaries as important; it does not show
a general implementation that detects missing authority visibility across all
surfaces.

## How Seed Would Recognize A Traceability Gap

Repository evidence suggests recognition would have to be evidence-based and
read-only. A safe recognition pattern would look like:

```text
1. Identify an implemented output or conclusion.
2. Identify which explanatory layers are visible for that output.
3. Identify an explicit unknown, limitation, unsupported conclusion, or boundary.
4. Compare that absence with the question the surface appears to answer.
5. Report only the missing explanatory layer, not a new truth claim.
```

Evidence that could support such recognition already appears in implementation
shapes:

- `unknowns` fields in derivation and selection surfaces.
- `unsupported_conclusions` in historical synthesis.
- `limitations` and `authority_boundary` in reference selection.
- diagnostic inventory metadata that records whether surfaces support JSON,
  record output, event-ledger writes, and cluster mutation.
- diagnostic shape audit metadata that ties diagnostic names to implementation
  modules, build functions, formatters, JSON functions, and registration checks.

Therefore, Seed could eventually recognize incomplete explanation when the
repository already exposes both:

```text
an answer-like surface
and
an implementation-backed admission that part of the explanation is unknown,
unsupported, limited, or authority-bounded
```

Current evidence does not support recognizing every possible gap. It supports a
narrower claim: Seed already carries enough metadata in several surfaces to make
some missing traceability layers observable without mutating runtime state.

## Recurring Categories Of Missing Visibility

The reviewed evidence suggests recurring categories, but not a final taxonomy:

| Candidate category | Missing layer | Evidence pattern |
| --- | --- | --- |
| Derivation visibility | Why the conclusion exists | `reasoning_path` exposes evidence, intermediate conclusions, derived conclusions, consumers, and unknowns. |
| Selection visibility | Why this conclusion or focus was selected | `selection_path` exposes candidates, selection factors, non-selected candidates, outcome, and unknowns. |
| Historical visibility | What changed and how confident comparison is | `history_brief` exposes changes, stability, repository context, confidence, unsupported conclusions, and causation boundary. |
| Reference visibility | Compared to what | `reference_selection` exposes selected reference, rationale, alternatives, limitations, and authority boundary for history. |
| Authority visibility | Who/what permits acceptance, expectation, promotion, or mutation | Existing investigations and read-only boundaries repeatedly separate visibility from authority. |
| Significance visibility | Why a visible difference matters | Some surfaces report change or confidence but do not always establish operational or should-bearing significance. |

These are candidate observations only. This investigation does not prescribe a
registry, scoring system, architecture, ontology, or implementation.

## How A Traceability Gap Differs From Neighboring Absences

### Traceability gap versus missing feature

A missing feature means Seed lacks a capability or behavior. A traceability gap
means Seed may already have the behavior or result, but cannot explain an
important layer of how or why it exists.

Example:

```text
Missing feature:
    Seed cannot perform a requested operation.

Traceability gap:
    Seed performs or reports something, but cannot explain derivation,
    selection, reference, significance, or authority.
```

A traceability gap may motivate a future feature, but the gap itself is an
explanatory absence, not the feature request.

### Traceability gap versus missing data

Missing data means evidence is absent. A traceability gap can occur even when
data exists, if the relationship between data and conclusion is not explainable.

Example:

```text
Missing data:
    No comparable snapshots exist.

Traceability gap:
    Comparable snapshots exist, but Seed cannot explain why one snapshot pair is
    the meaningful reference for this question.
```

The distinction matters because filling data does not automatically fill
reference selection, selection rationale, or authority boundaries.

### Traceability gap versus missing authority

Missing authority means the repository lacks authority to promote, accept,
mutate, or assert a should-bearing claim. A traceability gap is about whether the
explanation of that authority boundary is visible.

Example:

```text
Missing authority:
    No authority accepts a candidate baseline as an accepted baseline.

Traceability gap:
    Seed cannot explain whether the missing layer is evidence, reference
    selection, baseline acceptance authority, expectation authority, or mutation
    authority.
```

A traceability-gap analyzer would need to remain authority-safe by reporting the
absence rather than inventing authority.

## Relationship To Existing Traceability Surfaces

### `reasoning_path`

`reasoning_path` answers why an operational conclusion exists. It is evidence
that derivation visibility is a concrete traceability layer. It also demonstrates
gap-safe behavior because unknowns and read-only boundaries remain explicit.

### `selection_path`

`selection_path` answers why an operational result was selected. It demonstrates
that selection can be incomplete even when derivation exists, and that selection
explanation can be read-only rather than behavior-changing.

### `history_brief`

`history_brief` answers what changed, what appears stable, and how confident the
historical comparison is. It demonstrates that historical explanation is partial
when causation, accepted reference, or significance are not established.

### `reference_selection`

`reference_selection` answers compared to what for the history domain. It
demonstrates that comparison can require its own trace layer and that unknown or
unsupported domains should remain explicit.

### `candidate_baseline`

Candidate baseline is best understood as a narrower reference-selection pressure:
an evidence-supported possible comparison reference for a bounded question. It is
not, under current repository authority, an accepted baseline or expectation.

### `reference_selection_investigation`

The reference-selection investigation shows the broader comparison-reference
pressure: meaningful comparison needs question fit, evidence support, scope,
confidence limits, selection rationale, and authority boundary. This strongly
supports traceability gap analysis as a reusable way to notice missing layers,
while still not implementing a general analyzer.

### `unified_derivation_architecture_investigation`

The unified derivation investigation supports the idea that several domains can
share derivation mechanics while retaining separate authority models. That is
important for traceability gaps: a gap discipline could identify missing layers
without collapsing operational, historical, documentary, and authority-specific
models.

### `architecture_conformance`

Architecture conformance demonstrates comparison against an authority-bearing
reference domain: architecture evidence versus operational graph evidence. It is
an example where reference and authority are more explicit than in ordinary
historical comparison, which helps distinguish missing reference from missing
authority.

### `operational_story`

Operational story composes operational evidence into a narrative of focus and
pressure. It is a consumer of derivation and selection traceability, and it is a
place where incomplete explanation becomes visible to operators. It does not, by
itself, create baseline, expectation, or authority.

## Supported Examples

### Before `reasoning_path`

Supported as a recurring pattern:

```text
Operational conclusion existed.
Inputs existed in diagnostics.
Derivation path was not first-class visible.
```

Repository support: `reasoning_path` now exposes evidence, intermediate
conclusions, derived conclusions, consumers, story impact, unknowns, and read-only
boundary.

### Before `selection_path`

Supported as a recurring pattern:

```text
Operational focus or pressure existed.
Candidate ranking existed in behavior.
Selection rationale was not first-class visible.
```

Repository support: `selection_path` exposes candidates, selection factors,
non-selected candidates, evidence, outcome, unknowns, and read-only boundary.

### Before `reference_selection`

Supported as a recurring pattern for history:

```text
Historical comparison existed.
Comparable snapshot pairs could exist.
The selected comparison reference and alternatives were not first-class visible.
```

Repository support: `reference_selection` exposes selected historical reference,
rationale, alternatives, authority boundary, limitations, and read-only boundary.

### Authority visibility absent after other layers

Supported only as a candidate gap, not as implemented capability:

```text
Conclusion exists.
Derivation visible.
Selection visible.
Reference visible.
Authority visibility absent.
```

Repository support is indirect: investigations repeatedly separate evidence,
reference candidacy, accepted baseline authority, expectation authority, and
mutation boundary. There is no general authority-gap analyzer.

## Unsupported Examples

The following are not supported by current repository authority:

- `trace_patterns` as a required repository catalog.
- `trace_chain_inventory` as an implemented diagnostic or registry.
- A general traceability-gap score.
- A planning or recommendation system derived from traceability gaps.
- A universal ontology of trace layers.
- A claim that every incomplete explanation is a traceability gap rather than an
  ordinary missing feature, missing data, or missing authority.
- A claim that traceability gap analysis should mutate cluster truth, write event
  ledger entries, or record diagnostic findings against runtime entities.

## Relationship To Authority

Traceability gap analysis is only safe if it preserves authority boundaries.

The safe form is:

```text
This explanation is incomplete because authority visibility is absent.
```

The unsafe form is:

```text
Authority is absent, so Seed should create or infer the authority.
```

Repository evidence repeatedly favors the safe form. Existing traceability
surfaces preserve read-only boundaries, keep unknowns explicit, and distinguish
visibility from event-ledger writes and cluster mutation.

A future capability, if ever implemented, would need to report gaps as diagnostic
or investigation-scoped observations. It should not attach diagnostic-only
findings directly to hosts, services, filesystems, or runtime entities unless
repository authority explicitly changes.

## Relationship To Missing Visibility

Traceability gap analysis is most meaningful as **missing visibility about an
explanation**, not as missing implementation in general.

The repository evidence reviewed suggests this recognition rule:

```text
If Seed presents an answer-like surface,
and the answer depends on an explanatory layer,
and that layer is absent, unknown, unsupported, or only implicit,
then Seed may have a traceability gap.
```

This remains distinct from saying Seed must fill the gap. The investigation only
supports making the incompleteness visible.

## Can Gap Identification Remain Read-Only And Authority-Safe?

Yes, in principle, and existing surfaces demonstrate the ingredients:

- read-only boundary fields;
- explicit `writes_event_ledger=false` and `mutates_cluster=false` patterns;
- unknowns and limitations instead of invented facts;
- unsupported conclusions that remain diagnostic rather than cluster truth;
- diagnostic inventory and shape audit checks for operational visibility.

However, this is a supported possibility, not an implementation recommendation.
The repository does not yet contain a general traceability-gap diagnostic.

## Supported Conclusions

1. Seed can sometimes recognize that an explanation is incomplete when an
   implemented surface exposes unknowns, unsupported conclusions, limitations, or
   authority boundaries.
2. Existing traceability work shows recurring missing layers: derivation,
   selection, historical comparison, reference selection, and authority boundary.
3. Traceability gaps differ from missing features because they concern partial
   explainability of existing outputs.
4. Traceability gaps differ from missing data because data may exist while the
   explanatory relation remains absent.
5. Traceability gaps differ from missing authority because gap analysis can name
   the absent authority layer without creating authority.
6. Repository evidence supports traceability gap analysis as a reusable
   investigation concept.
7. Repository evidence does not yet support traceability gap analysis as an
   implemented diagnostic, registry, ontology, scoring system, or planner.
8. The concept would help Seed reason about itself only if grounded in
   implementation evidence such as unknowns, limitations, unsupported
   conclusions, and authority boundaries, rather than operator intuition alone.

## Unsupported Conclusions

1. Seed currently has a general traceability-gap analyzer.
2. Every missing explanation should become a new diagnostic surface.
3. Every traceability gap should produce recommendations or plans.
4. Traceability layers should be unified into one authority model.
5. Candidate baselines are accepted baselines.
6. Historical changes imply expectation violations.
7. Reference selection implies authority to mutate runtime state.
8. Presentation vocabulary is sufficient to create repository knowledge.

## Open Questions

- What minimum evidence would be required for Seed to say an explanatory layer is
  absent rather than merely outside the current question?
- Can traceability gaps be detected from existing `unknowns`, `limitations`, and
  `unsupported_conclusions` without adding a new diagnostic?
- How should a future read-only surface avoid turning gap labels into ontology or
  planning authority?
- Are authority gaps always traceability gaps, or are some simply settled by
  explicit absence of authority?
- Can significance visibility be distinguished from reference selection and
  authority without creating should-bearing expectations?
- Which existing surfaces already expose enough metadata for self-recognition of
  incompleteness, and which only expose operator-readable prose?
- Would an implementation-backed inventory of gaps help Seed reason about itself,
  or would it mostly help repository architects navigate existing investigations?

## Acceptance Answers

### Can Seed recognize when an explanation is incomplete?

Partially. Current repository evidence shows that some surfaces expose unknowns,
limitations, unsupported conclusions, confidence boundaries, and read-only
authority boundaries. Those are implementation-backed signals of incomplete
explanation. The repository does not show a general analyzer that recognizes all
incomplete explanations.

### Can Seed recognize missing traceability layers?

Partially. Seed can make specific missing layers visible when a surface is built
for that layer: derivation through `reasoning_path`, selection through
`selection_path`, historical comparison through `history_brief`, and historical
reference selection through `reference_selection`. It cannot yet generally infer
that an arbitrary missing layer is a traceability gap.

### Is there evidence that traceability gaps form a reusable repository concept?

Yes, as an investigation concept. The same pattern recurs across derivation,
selection, history, reference selection, and authority-boundary investigations:
Seed has an answer-like surface, discovers that an explanatory layer is implicit
or absent, and then either exposes that layer or records the unsupported boundary.

### Would such a capability help Seed reason about itself rather than merely helping operators understand Seed?

Potentially yes, but only if grounded in repository evidence. A read-only,
authority-safe capability could let Seed identify which part of its own
explanation is missing: derivation, selection, reference, significance, data, or
authority. That would be self-reasoning about explanation completeness. A catalog
of trace patterns without implementation evidence would mostly help repository
architects and would not by itself improve Seed's self-understanding.
