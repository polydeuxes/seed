# Source-Local Testimony Competency Investigation

This is exactly one Constitutional Competency Investigation. It begins from `source_local_testimony_profile_implementation_visibility_audit.md`, inspects only the three independently recovered implementation occurrences named there, and expands only where recurring repository evidence naturally leads.

This investigation does not recover another ownership boundary, does not recommend implementation, does not recover a citizen merely because recurrence exists, and does not introduce a testimony engine, comparison engine, workflow, planner, scheduler, registry, universal testimony model, universal profile type, implementation, or architectural redesign.

Repository authority wins.

## Reviewed evidence

Implementation evidence reviewed for the three occurrences only:

- `source_local_testimony_profile_implementation_visibility_audit.md` as the starting audit and scope boundary.
- Observation Agreement: `seed_runtime/knowledge/observation_agreement.py` and `tests/test_observation_agreement.py`.
- Grammar Observation: `seed_runtime/knowledge/grammar_observation.py` and `tests/test_grammar_observation.py`.
- Inquiry Orientation: `seed_runtime/inquiry_orientation.py` and `tests/test_inquiry_orientation.py`.

No provider translation, diagnostic inventory, diagnostic shape audit, knowledge reachability, or other adjacent neighborhood was promoted into this investigation.

## Stage 1 — Independent Competency Testimony

### Occurrence 1: Observation Agreement

- **Implementation producer:** `observe_observation_agreements(...)`.
- **Bounded profile preserved:** `ObservationAgreementRecord` preserves participating observation streams, supporting `ObservationAgreementEvidence`, provenance, candidate agreement text, and a candidate-only non-promotion boundary. Each `ObservationAgreementEvidence` preserves stream, provenance, and evidence text.
- **Comparison gate:** candidate agreement is emitted only after supplied evidence text matches exactly, after trimming, across at least two independent observation streams. Non-independent or textually different supplied evidence produces no agreement record.
- **Downstream consumer:** `observe_grammar_observations(...)` consumes `ObservationAgreementRecord` artifacts; tests also consume the artifact to prove candidate agreement, provenance, independence, and non-promotion.
- **Constitutional movement exercised:** preserve source-local evidence, provenance, independence, and negative authority before permitting candidate agreement comparison or downstream grammar-shaped comparison.
- **Preserved Unknowns:** no typed Unknown field is present. Unknown remains whether richer upstream observation streams preserve additional testimony fields. Absence of agreement is preserved only by no emitted record, not by a typed Unknown.
- **Confidence:** High that this occurrence exercises bounded source-local preservation before comparison. Medium that the stop condition can be read as constitutional stop, because the repository implements it as filtering/no record and a non-promotion boundary rather than a named lawful-stop field.

### Occurrence 2: Grammar Observation

- **Implementation producer:** `observe_grammar_observations(...)`.
- **Bounded profile preserved:** `GrammarObservationRecord` preserves an observed relation shape, supporting agreement records, flattened provenance, recurrence evidence, and a grammar-observation-only non-promotion boundary.
- **Comparison gate:** relation-shape observation starts only from supplied `ObservationAgreementRecord` artifacts. A grammar observation is emitted only when at least two agreement records share the same syntactic relation shape. Malformed or non-recurring candidates are ignored.
- **Downstream consumer:** the immediate visible consumers are module-level return callers and tests proving recurrence evidence, provenance, support, and non-promotion. No broader runtime consumer is recovered here.
- **Constitutional movement exercised:** preserve the local agreement-backed recurrence profile before comparing relation shapes and before allowing any downstream use of the grammar observation artifact.
- **Preserved Unknowns:** no typed Unknown field is present. Unknown remains whether a current app or diagnostic surface consumes grammar observations beyond tests and module-level implementation. Unknown remains whether ignored malformed or single-use shapes should ever become typed Unknowns.
- **Confidence:** High that this occurrence exercises bounded artifact preservation before recurrence comparison. Medium for downstream consumer scope because repository evidence proves tests/module use, not a recurring app surface.

### Occurrence 3: Inquiry Orientation

- **Implementation producer:** `record_inquiry_note(...)` preserves the inquiry note, and `_prepare_inquiry_orientation_composition(...)` prepares preserved note material for orientation composition.
- **Bounded profile preserved:** `InquiryNoteRecord` preserves note id, raw note, recorded time, source, and optional workspace/session identifiers. The orientation path then preserves local request, evidence, selected material, support, answer payload, boundary, reason, and limitations through implementation-local dataclasses.
- **Comparison gate:** lexical related-material matching starts only after a preserved `InquiryNoteRecord` is supplied to `build_inquiry_orientation(...)` and converted into `_InquiryOrientationCompositionRequest`. Matching is deterministic lexical overlap against projected fact supports and source-navigation matches; raw operator prose is not compared as unpreserved cluster truth.
- **Downstream consumer:** `build_inquiry_orientation(...)` consumes the preserved note and returns `InquiryOrientationView`; `format_inquiry_orientation(...)` renders the bounded orientation view.
- **Constitutional movement exercised:** preserve operator testimony and its provenance/authority boundary before permitting bounded related-material comparison, selection, answer preparation, and rendering.
- **Preserved Unknowns:** uncertainty is preserved as limitation strings for matched and unmatched material, not as typed Unknown records. Unknown remains whether confidence should be preserved; current implementation has no confidence field. Unknown remains whether unmatched notes should become typed Unknowns; current implementation preserves uncertainty text only.
- **Confidence:** High that this occurrence exercises bounded note preservation before lexical comparison. Medium that limitation strings satisfy Unknown preservation, because repository evidence names them uncertainty/limitations rather than typed Unknown artifacts.

## Stage 2 — Competency Cross-Examination

### Recurring constitutional movement

Across the three independently evolved occurrences, the recurring movement is:

Preserve a bounded source-local testimony artifact with provenance/support and negative authority before allowing a downstream comparison, recurrence test, related-material match, or consumer-facing composition to proceed.

This movement is recoverable as a competency because it recurs across independent implementations with consistent responsibilities and stop conditions, while remaining smaller than any implementation owner, shared engine, registry, workflow, or universal profile type.

### Recurring responsibilities

The recurring responsibilities are:

- accept only already supplied or locally preserved testimony material;
- preserve the source-local artifact rather than immediately converting it into truth;
- preserve provenance, support, or evidence references sufficient for local accountability;
- preserve a negative authority boundary that refuses promotion, semantic interpretation, ownership recovery, architectural truth, runtime mutation, repository mutation, ledger writes, or cluster mutation as applicable to the local surface;
- delay downstream comparison until the bounded local artifact exists;
- emit only the local bounded artifact or local bounded view supported by that artifact;
- stop by refusing emission, ignoring unsupported candidates, or rendering uncertainty/limitations when local admissibility is not met.

### Recurring admissibility conditions

The recurring admissibility conditions are:

- the testimony must already be supplied or locally recorded;
- the local producer must preserve a bounded artifact with evidence, support, provenance, source, or boundary fields appropriate to the neighborhood;
- downstream comparison must wait for that local artifact rather than operate over unpreserved raw substrate;
- comparison must stay within the local implementation rule: exact evidence equality for Observation Agreement, recurring syntactic relation shape over agreement records for Grammar Observation, deterministic lexical overlap after note preservation for Inquiry Orientation;
- the result must remain non-promotional and must not become architectural truth or cluster mutation merely because comparison was possible.

### Recurring producer obligations

The recurring producer obligations are:

- produce only the local artifact it owns;
- keep source, support, provenance, evidence, or note identity attached to the artifact;
- keep negative authority explicit;
- avoid semantic promotion beyond the local evidence rule;
- refuse empty, unsupported, non-independent, malformed, non-recurring, or unmatched material according to local rules.

### Recurring comparison obligations

The recurring comparison obligations are:

- compare only after bounded local testimony preservation;
- compare only the permitted local surface, not all repository material;
- preserve the evidence basis used for comparison;
- avoid converting recurrence, equality, or lexical overlap into truth, ownership, intent, action, or architecture;
- expose limitation or refusal when comparison is unsupported.

### Recurring consumer obligations

The recurring consumer obligations are:

- consume the bounded artifact, not the unpreserved substrate;
- honor the artifact's non-promotion boundary;
- retain support/provenance in downstream artifacts where a downstream artifact is emitted;
- do not infer a shared implementation owner, universal profile, engine, planner, scheduler, workflow, registry, or new citizen from recurrence alone.

### Recurring stop conditions

The recurring stop conditions are:

- Observation Agreement stops with no emitted record when evidence lacks at least two independent matching streams.
- Grammar Observation stops with no emitted record when relation text is malformed or when a relation shape is not recurring across at least two agreement records.
- Inquiry Orientation stops short of promotion by preserving uncertainty/limitations and bounded read-only output when related material is absent, incomplete, incidental, or only lexically overlapping.

### Preserved Unknowns

- Unknown whether a future local surface should add typed Unknown fields; current recurring evidence does not require that recovery.
- Unknown whether confidence fields should exist in any of the three neighborhoods; current recurring evidence does not preserve confidence as a shared field.
- Unknown whether Grammar Observation has a runtime consumer beyond current module/test evidence.
- Unknown whether other repository neighborhoods exercise similar movement; this investigation intentionally remained within the three recovered occurrences.
- Unknown whether a stronger constitutional participant should ever be recovered; current recurring evidence does not require one.

### Confidence

Confidence is high that the recurring movement is real and implementation-backed across the three inspected occurrences. Confidence is high that it does not recover implementation ownership, shared machinery, a universal model, a registry, a workflow, or a citizen. Confidence is medium on typed Unknown and confidence-field implications because current repository evidence preserves limitation/no-record behavior more strongly than typed constitutional fields.

## Required Questions

1. **What recurring competency is being exercised?**

   Source-local testimony competency: the competency to preserve bounded source-local testimony with provenance/support and negative authority before downstream comparison is permitted.

2. **What constitutional movement defines that competency?**

   The constitutional movement is bounded preservation before comparison: source-local testimony is first held as a limited artifact, with its authority boundary and support preserved, and only then may local comparison, recurrence observation, related-material matching, or rendering proceed.

3. **What implementation responsibilities consistently exercise it?**

   The consistently recurring responsibilities are local production of a bounded artifact, preservation of support/provenance/source identity, preservation of negative authority, delayed comparison over the preserved artifact, non-promotion of comparison results, and stopping/refusal/uncertainty when local admissibility conditions are not met.

4. **Does the competency own any implementation?**

   No.

5. **Does the competency require a new constitutional participant?**

   No.

6. **Did any previously recovered constitutional or implementation boundary change?**

   No.

## Recovered competency

The smallest recurring competency supported by repository evidence is:

**Source-local testimony competency** — a constitutional competency exercised when independently evolved implementations preserve bounded source-local testimony, including local support/provenance and negative authority, before permitting downstream comparison or composition.

This competency owns no implementation. It does not introduce a citizen, engine, workflow, registry, universal profile type, universal testimony model, planner, scheduler, or architectural redesign. It changes no previously recovered boundary.

## Readiness classification

Recoverable constitutional competency

## Final answer

According to recurring
repository evidence,

what constitutional
competency

is being exercised

when independently evolved
implementations

preserve a bounded
source-local testimony profile

before permitting
downstream comparison?

Source-local testimony competency.

Source-local testimony competency investigation complete.
