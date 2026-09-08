---
status: investigation
scope: reference selection as repository traceability concept
created: 2026-06-21
---

# Reference Selection Traceability Investigation

## Status

Investigation only. This document does not implement baselines, reference
systems, change readiness, storage, projections, runtime behavior, ontology,
policy, diagnostic surfaces, operational behavior, or architecture changes.
Repository authority wins over this investigation.

## Question

Recent traceability investigations produced a progression:

```text
reasoning_path
    -> Why does this conclusion exist?

selection_path
    -> Why was this conclusion selected?

history_brief
    -> What changed?

candidate baseline
    -> Compared to what?
```

The candidate-baseline investigation characterized candidate baseline as an
`evidence-supported possible comparison reference for a bounded question` and
located it between continuity evidence and authority-selected comparison
reference. This investigation asks whether that is the fundamental pressure, or
whether the broader pressure is **reference selection**:

```text
Which reference is meaningful for this question?
```

## Repository evidence reviewed

Primary evidence reviewed:

- `docs/candidate_baseline_traceability_investigation.md`
- `docs/candidate_baseline_accepted_baseline_expectation_audit.md`
- `docs/comparison_reference_authority_reconciliation.md`
- `docs/baseline_acceptance_authority_audit.md`
- `docs/observation_visibility_continuity_baseline_expectation_concern_reconciliation.md`
- `docs/change_readiness_baseline_concept_investigation.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/unified_derivation_architecture_investigation.md`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/history_brief.py`
- `seed_runtime/architecture_conformance_audit.py`
- tests around `selection_path`, `history_brief`, and
  `architecture_conformance_audit` as implementation evidence for existing
  surfaces.

This review treats prior investigation documents as repository evidence, not as
new authority. Where implementation exists, implementation constrains the
conclusion more strongly than vocabulary in prose.

## Working vocabulary supported by evidence

The repository already distinguishes several neighboring ideas. The following
characterizations are evidence-oriented summaries, not new ontology:

```text
snapshot
    = captured evidence or cached/persisted observation artifact

current state
    = current projection or current read-model representation

continuity
    = evidence of persistence, recurrence, or historical existence

candidate baseline
    = evidence-supported possible comparison reference
      for a bounded comparison question

accepted baseline
    = scoped selected comparison reference after authority selection

expectation
    = should-bearing claim requiring separate authority

reference selection
    = the reasoning, evidence, and authority boundary by which
      one possible comparison reference becomes meaningful for a question
```

The strongest supported refinement is that `candidate baseline` names one kind
of candidate reference, while `reference selection` names the broader discipline
of making comparison references meaningful, scoped, and authority-bounded.

## What is a reference?

A reference is not merely an artifact that exists. In repository evidence, a
reference is something used as the other side of an interpretation or comparison.
It may be historical, architectural, operational, documentary, visibility-facing,
or investigation-scoped.

Examples supported by existing surfaces:

- A prior audit snapshot can be the `before` side of impact comparison.
- Architecture documentation can be the design-side reference for conformance.
- A pressure candidate set can be the selection reference set for
  `selection_path`.
- A repository observation can be context for interpreting historical confidence.
- A historical continuity pattern can become a candidate baseline for a bounded
  comparison question.

Therefore:

```text
reference
    = evidence, source, state, candidate set, or authority-bearing artifact
      used as the comparison side for a bounded question
```

This definition is intentionally minimal. The repository does not support a
single reference object model, reference store, reference schema, or general
runtime reference system.

## What makes a reference meaningful?

Repository evidence supports at least six constraints:

1. **Question fit.** The reference must answer the bounded question being asked.
   A snapshot may exist but still be irrelevant to an architectural comparison.
2. **Evidence support.** The reference must have traceable support: source,
   snapshot, observation, implementation rule, or prior finding.
3. **Scope.** The reference must be bounded to a surface, investigation,
   subject, comparison, or authority context.
4. **Confidence limits.** The reference must preserve uncertainty, missing
   history, unsupported conclusions, or source limitations.
5. **Selection rationale.** If multiple references are possible, repository
   evidence must explain why one is selected, ranked, or merely left as a
   candidate.
6. **Authority boundary.** Evidence can make a reference plausible, but separate
   authority is required to make it accepted, should-bearing, operational, or
   mutating.

The candidate-baseline work already expresses these constraints for historical
or continuity-derived comparison. Reference selection generalizes the same
pressure to non-baseline comparisons.

## Does reference selection appear outside baseline discussions?

Yes. It appears outside baseline vocabulary in implementation-backed surfaces.

### Selection path

`selection_path` does not select baselines. It explains why an operational
conclusion or pressure was selected from candidates. Its implementation exposes a
candidate set, selection factors, non-selected candidates, evidence, outcome, and
unknowns. The implemented selection factor for pressure ordering is deterministic:
pressure candidates are ordered by descending score and category name.

This demonstrates a selection pattern:

```text
candidate set
    -> selection factors
    -> selected item
    -> non-selected candidate reasons
    -> outcome and boundary
```

That pattern is analogous to reference selection, but the selected thing is a
conclusion or focus rather than a comparison reference. It proves the repository
already values selection traceability without requiring baseline vocabulary.

### History brief

`history_brief` synthesizes impact audit, snapshot policy, and repository
observation. It reports changes, stability, repository context, historical
confidence, and unsupported conclusions. Its confidence output explicitly says
when comparison data is available or insufficient, and it preserves causation as
not proven.

This demonstrates that historical comparison already depends on reference-like
inputs even when no baseline is implemented. A change is intelligible only
because there is a `before` and `after` comparison. The brief can summarize that
comparison, but it does not authorize the `before` state as an accepted baseline.

### Architecture conformance

`architecture_conformance_audit` compares discovered architecture evidence with
operational graph evidence. It has explicit architecture evidence, operational
evidence, classifications, significance, concept realizations, and read-only
metadata. Architecture documentation functions as a meaningful reference because
repository architecture files are the intentionally scoped design evidence for
that audit.

This is reference selection outside baseline: the comparison is not historical
baseline versus current state, but design-side evidence versus observed
operational structure.

### Unified derivation

`unified_derivation_architecture_investigation` describes shared derivation
mechanics across operational, historical, and documentation reasoning while
keeping authority models separate. Reference selection fits that shape:

```text
evidence
    -> candidate references
    -> selected or candidate reference
    -> interpretation
    -> boundary-preserving output
```

The fit is mechanical, not a license to unify authority. Historical references,
architecture references, current operational observations, and operator decisions
can share derivation mechanics while retaining distinct authority models.

## Relationship to candidate baseline

Candidate baseline does not fully explain the pressure. It explains a narrower
case:

```text
Which evidence-supported possible comparison reference should be considered
for this bounded comparison question, usually from continuity or history?
```

Reference selection is broader:

```text
Which reference is meaningful for this question, and why?
```

Candidate baseline is therefore best treated as one manifestation of reference
selection, not the fundamental concept. It is the manifestation where the
reference is a plausible baseline candidate rather than an already selected
architecture reference, a candidate set for operational focus, or a before/after
artifact for historical comparison.

The distinction prevents overloading `candidate baseline` with too many roles:

- candidate baseline should not mean every reference;
- candidate baseline should not mean every selected reference;
- candidate baseline should not mean architecture documentation;
- candidate baseline should not mean current state;
- candidate baseline should not mean expectation;
- candidate baseline should not mean concern;
- candidate baseline should not become a generic name for selection rationale.

## Relationship to selection rationale

Selection-path work answers:

```text
Why was this conclusion selected?
```

Reference-selection pressure asks the analogous but distinct question:

```text
Why would this reference be selected for this question?
```

They are related because both require:

- a candidate set;
- selection factors;
- evidence;
- explanation of non-selected alternatives;
- known unknowns;
- an outcome;
- a read-only or authority boundary.

They differ in authority model. Conclusion selection can be a deterministic
implementation choice, such as score ordering. Reference selection may be:

- evidence-only candidacy, as with candidate baselines;
- implementation selection, as with an audit choosing architecture paths;
- source-authority selection, as with architecture documents functioning as
  design evidence;
- human or policy authority, as with accepting a baseline for a scoped
  investigation;
- should-bearing authority, if the selected reference becomes an expectation.

Conclusion selection and reference selection can exist independently. A
conclusion can be selected without choosing a comparison reference, such as a
primary pressure selected by score. A reference can be selected without selecting
a final conclusion, such as choosing architecture evidence as the reference side
for a conformance audit before classifying each subject.

## Relationship to history

Change significance generally cannot be fully interpreted without some reference.
A statement such as `X changed` requires at least two compared states or records.
`history_brief` makes this explicit by reporting changes and stability only when
impact metrics are comparable, and by surfacing insufficient comparison history
as an unsupported conclusion.

However, reference selection is not identical to history. History can preserve
records without selecting one as meaningful. Multiple valid historical
references can coexist:

- the immediately previous snapshot;
- the last clean repository-context snapshot;
- a repeated historical continuity pattern;
- a known-good operator-selected point;
- an architecture-era comparison point;
- an investigation-specific comparison reference.

These can all be valid for different questions. The question determines which
reference is meaningful. Candidate baseline captures the plausible-reference
case; reference selection captures the broader reasoning required when more than
one reference is possible.

## Relationship to architecture conformance

Architecture conformance already demonstrates reference selection. The audit
selects architecture documentation from scoped repository paths as the design
reference and compares it against operational graph evidence.

The reason architecture is meaningful is not that it is current state or a
historical baseline. It is meaningful because the audit's question is
conformance: whether observed operational structure aligns with documented
architecture evidence. The authority comes from the repository's architecture
sources and from the audit implementation's scoped discovery of those sources.

This is a special case of the broader pattern:

```text
question: does operation conform to architecture?
reference: architecture evidence from scoped repository architecture paths
comparison side: operational graph evidence
interpretation: aligned, drift, underspecified, obsolete design, emergent structure, unknown
boundary: read-only; no event ledger writes; no cluster mutation
```

Architecture conformance therefore supports the broader reference-selection
concept more strongly than it supports candidate baseline. It is a comparison
reference discipline without baseline semantics.

## Relationship to authority

Repository evidence requires preserving authority boundaries:

```text
evidence authority
    supports plausibility

selection authority
    chooses a reference for a scope

should-bearing authority
    creates expectation

operational authority
    permits mutation or action
```

Reference selection can happen at different strengths:

| Strength | Meaning | Example |
| --- | --- | --- |
| Candidate reference | Plausible comparison reference, not accepted | Candidate baseline from historical continuity |
| Implementation-selected reference | Audit implementation chooses a source class for its question | Architecture paths in conformance audit |
| Authority-selected reference | Decision accepts reference for a scope | Accepted baseline |
| Should-bearing reference | Reference becomes normative expectation | Expectation |
| Operational reference | Reference drives mutation or action | Out of scope for this investigation |

The important boundary is that evidence-supported meaningfulness does not imply
acceptance, and acceptance does not imply expectation or mutation.

## Supported conclusions

1. **Candidate baseline is not the fundamental concept.** It is a repository-
   supported manifestation of a broader reference-selection pressure.
2. **Reference selection appears outside baseline discussions.** It appears in
   `selection_path` candidate selection, `history_brief` historical comparison,
   and `architecture_conformance_audit` design-versus-operation comparison.
3. **The core pressure is question-bounded meaningfulness.** The repository does
   not merely ask whether a possible reference exists; it asks whether that
   reference is meaningful for the current question.
4. **Multiple valid references can coexist.** Different questions can select
   different references without contradiction.
5. **Reference selection shares derivation mechanics with selection rationale.**
   Both need candidate sets, factors, evidence, unknowns, non-selected
   alternatives, and boundaries.
6. **Reference selection does not share one authority model.** Historical,
   architectural, operational, operator, and expectation references require
   different authority boundaries.
7. **Architecture conformance is the clearest non-baseline evidence.** It uses
   architecture documentation as a selected reference for a conformance question.
8. **History implicitly relies on references.** Change and stability require
   comparison artifacts, but historical comparison does not automatically select
   an accepted baseline.
9. **`Compared to what?` is answered by scoped reference selection.** Candidate
   baseline answers it only when the relevant reference is a plausible baseline
   candidate.

## Unsupported conclusions

Repository evidence does not support claiming that:

- reference selection is an implemented general subsystem;
- candidate baselines are implemented;
- accepted baselines are implemented as storage or runtime behavior;
- reference selection should introduce ontology, schemas, projections, storage,
  CLI flags, diagnostics, or runtime behavior;
- architecture documents are always authoritative for every question;
- historical continuity automatically selects a baseline;
- a selected reference automatically creates an expectation;
- a selected reference automatically authorizes mutation;
- selection-path mechanics can be reused without preserving domain-specific
  authority models;
- every comparison should be normalized into baseline vocabulary.

## Open questions

1. If a future surface explains reference selection directly, should it compose
   existing selection evidence or remain investigation-only?
2. What evidence threshold is enough to promote a candidate reference into a
   candidate baseline for a bounded historical comparison?
3. What authority record would be required to accept a candidate baseline without
   creating an expectation?
4. How should multiple valid references be displayed without implying one is
   globally preferred?
5. Can architecture-reference selection be made more explicit in documentation
   without introducing new runtime behavior?
6. Where should non-selected reference candidates be preserved, if anywhere,
   without creating storage or ontology prematurely?
7. How should repository authority distinguish implementation-selected reference
   classes from human-selected investigation references?

## Acceptance answer

Candidate baseline is not the fundamental concept. Repository evidence supports
candidate baseline as one manifestation of a broader **reference-selection
discipline**.

The repository answer to:

```text
Compared to what?
```

is not simply:

```text
candidate baseline
```

It is:

```text
select a meaningful comparison reference for the bounded question,
using evidence, scope, confidence limits, selection rationale,
and the correct authority boundary.
```

When that meaningful reference is a plausible, evidence-supported comparison
reference derived from continuity or history, the repository-supported name is
`candidate baseline`. When the reference is architecture evidence, operational
candidate ordering, or before/after historical artifacts, baseline vocabulary is
not sufficient. The broader pattern is reference selection.
