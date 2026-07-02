# Constitutional Transition Family Characterization

## Executive answer

Repository evidence does **not** support one generic constitutional movement. It supports several recurring transition families with different effects and different authority boundaries.

The repeated mistake risk is compression: treating orientation, inquiry, evidence acquisition, candidacy, admission, fact projection, implementation recovery, and methodology earning as the same architectural verb. The repository instead keeps asking what changed and whether the change is authority-bearing.

The smallest recurring constitutional transition currently supported is:

```text
communication / observation / pressure
↓
orientation
```

That transition is real, recurring, and constitutionally weak. It changes what can be looked at next, but it does not by itself change repository knowledge, authority, runtime state, fact projection, implementation, or admission status.

## Evidence reviewed

This investigation reviewed implementation and repository evidence rather than treating transition vocabulary as authority:

- `constitution.md` defines the governing sequence from unknown through observation, inquiry, evidence, supported transition or stop, and bounded handoff; it also states that observation creates orientation, not truth.
- `seed_runtime/inquiry_orientation.py` implements the inquiry-orientation boundary: inquiry notes are preserved operator prose, related material is deterministic lexical overlap, and the result explicitly denies fact, claim, goal, requirement, decision, plan, command, ownership, intent, recommendation, or next-safe-move authority.
- `scripts/seed_local.py --record-inquiry-note "."` followed by `scripts/seed_local.py --inquiry-orientation` demonstrated the specific `.` probe: the app preserved the note, found no deterministic related material, and denied truth/authority promotion.
- `seed_runtime/question_surface_inventory.py` and `seed_runtime/bounded_ask.py` implement exact Question Family eligibility, required-argument checks, diagnostic-only and non-dispatchable stops, dispatch request construction, and dispatch execution.
- `scripts/seed_local.py --question-surface-inventory --json` showed distinct bounded statuses such as `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, and `not_dispatchable`.
- `02-domain-model.md` distinguishes immutable Evidence from projected Facts, FactSupport aggregates, best/current beliefs, and the rebuildable ProjectionStore cache.
- `candidate_inquiry_reconciliation.md` rejects first-class raw-token Candidate Interpretation for `.`, but supports a narrower constitutional pattern in which ambiguous observations can frame candidate bounded inquiries that gather or compose evidence and stop safely when unsupported.
- `question_to_inquiry_transition_characterization.md` narrows possible questions into exact registered Question Families, preserved inquiry notes, eligibility checks, map-backed selection, surface execution, and surface-local evidence collection.
- `observation_transition_recovery_characterization.md` distinguishes discussion/orientation from evidence-bearing observation or bounded evidence-bearing interpretation.
- `architectural_frontier_characterization.md` identifies the same negative boundary: human cognition and discussion orient inquiry, but repository authority requires implemented surfaces, tests, diagnostics, reports, or compatibility behavior.
- `docs/support_change_and_learning_observation.md` and `docs/claim_support_characterization.md` distinguish observations, evidence, facts, support, derivation, and represented knowledge.
- Prior transition reports, including architecture/implementation, working/earned methodology, support-change, promotion backlog, and frontier characterizations, were treated as repository artifacts only where they tied their conclusions back to implementation evidence.

## Recurring transition families

### 1. Communication / observation / pressure -> orientation

**Status:** independently recurring and strongly supported.

This family includes the bare `.` probe, pressure rows, operator concerns, roadmap pressure, inquiry notes, and discussion that frames a bounded question. The app demonstration is the cleanest current case: recording `.` produced an inquiry note, and orientation over that note produced no deterministic related material while explicitly denying fact, command, ownership, intent, recommendation, and next-safe-move authority.

**What changes?**

- The repository gains or exposes orientation material: a note, pressure, prompt, possible target, or related-material view.
- The next inquiry can be framed more lawfully.

**What does not change?**

- Repository knowledge does not change.
- Runtime authority does not change.
- Cluster state does not change.
- No fact is projected.
- No candidate is admitted.
- No implementation boundary is recovered.

**Does knowledge change?** No. The current implementation explicitly keeps inquiry orientation outside facts, claims, requirements, commands, and ownership.

**Does authority change?** No. Orientation is read-only and non-authorizing.

**Does state change?** Only local/preserved orientation state changes when a note is recorded. The orientation result itself is read-only.

**Does only orientation change?** Yes, in the strict `.` case.

**Does evidence increase?** Not necessarily. The app found no deterministic related material for `.`. A note can preserve material without adding supportable implementation evidence.

**Does promotion occur?** No.

**Does nothing permanent occur?** If a note is recorded, a note artifact exists; nevertheless no permanent knowledge, authority, or implementation promotion occurs.

### 2. Orientation -> bounded inquiry eligibility / running inquiry

**Status:** independently recurring, but implementation-local rather than universal.

Question-surface inventory and bounded ask show that possible inquiry does not become running inquiry automatically. It must pass exact family lookup, status/eligibility checks, required-argument checks, and dispatch mapping where implemented. Inquiry orientation remains explicitly not dispatchable.

**What changes?**

- A possible question may become an eligible or executable bounded inquiry when it matches an exact implemented surface.
- A dispatch request can set the specific CLI surface and arguments for the selected bounded work.

**What does not change?**

- Unknown families remain unknown.
- Diagnostic-only and not-dispatchable surfaces remain stopped.
- The dispatch layer does not decide evidence semantics or promote results.

**Does knowledge change?** Not at eligibility time. Eligibility changes answerability/routability, not truth.

**Does authority change?** Yes, narrowly: an eligible surface gains permission to run its bounded implementation. That authority is local to the surface.

**Does state change?** Usually no durable state changes; dispatch mutates the CLI namespace for execution, not repository truth.

**Does only orientation change?** No. The key distinction is transition from orientation to executable bounded work.

**Does evidence increase?** Not yet. Evidence increases only inside the selected surface if it collects or composes evidence.

**Does promotion occur?** No.

**Does nothing permanent occur?** Usually yes; eligibility and dispatch are procedural unless the invoked surface records output under its own rules.

### 3. Inquiry -> evidence-bearing result or explicit stop

**Status:** independently recurring and strongly supported.

The constitution, observation-transition reports, diagnostic/audit surfaces, and bounded ask all distinguish running inquiry from evidence-bearing results. Safe stop is a positive result when implementation evidence is insufficient.

**What changes?**

- Evidence may be acquired or composed.
- A report, diagnostic output, answer, or negative finding may become available.
- Insufficiency may be preserved as a lawful conclusion.

**What does not change?**

- Evidence does not automatically become a fact, admission, implementation boundary, or mutation.
- A failed or unsupported inquiry does not become latent truth.

**Does knowledge change?** Possibly, but only if the evidence-bearing result supports a bounded conclusion. Some inquiries only preserve insufficiency.

**Does authority change?** Surface-local authority may be exercised, but broader authority is not granted automatically.

**Does state change?** Only if the surface is designed to record. Diagnostic and audit surfaces are repeatedly read-only and non-mutating.

**Does only orientation change?** No.

**Does evidence increase?** Yes for evidence-acquiring or evidence-composing inquiry; no for a pure stop that only records lack of evidence.

**Does promotion occur?** Not by default.

**Does nothing permanent occur?** Read-only inquiry may leave no runtime state, but a report can preserve its conclusion as repository artifact.

### 4. Evidence -> candidate / support

**Status:** independently recurring, but not always by this label.

The domain model and support-change documents repeatedly separate raw Evidence from Facts, support, candidates, and projected belief. Evidence may support candidate claims, candidate routes, candidate requests, architectural boundaries, or fact support. It is not self-promoting.

**What changes?**

- A subject can move from uncommitted to candidate, supported, bounded, or worth considering.
- Support paths can become visible.

**What does not change?**

- Candidate is not verified.
- Support is not admission.
- Evidence is immutable and remains separate from projected facts.

**Does knowledge change?** Potentially: evidence can justify a supported candidate or support relation, but not automatic truth.

**Does authority change?** Only enough to consider or evaluate the candidate under local rules.

**Does state change?** Possibly, if facts/support records are recorded; not inherently.

**Does only orientation change?** No.

**Does evidence increase?** The transition depends on evidence already acquired; additional evidence may or may not be gathered.

**Does promotion occur?** No. This is pre-promotion.

**Does nothing permanent occur?** If not recorded, it can remain only in the report; when recorded, it remains bounded support, not truth.

### 5. Candidate / support -> admitted / verified / promoted

**Status:** independently recurring, but guarded and narrower than the candidate examples imply.

Capability verification, promotion readiness, architecture recovery, fact projection, and completion-audit patterns all preserve a gate between candidate/support and admitted or verified status. Candidate-to-admitted is not one universal transition; it is family-local and governed by the target surface's tests, registries, compatibility behavior, or projection rules.

**What changes?**

- A candidate may become admitted knowledge, verified capability, supported boundary, promoted documentation knowledge, or accepted implementation surface.
- Authority increases within the relevant family.

**What does not change?**

- Admission in one family does not imply global runtime authority.
- Verification is not interpretation.
- Promotion is not mutation unless the implementation specifically mutates state.

**Does knowledge change?** Yes, when admission is successful.

**Does authority change?** Yes, within the relevant family.

**Does state change?** Sometimes. Documentation promotion changes repository artifacts; fact/event recording changes stores; read-only verification may only change a report.

**Does only orientation change?** No.

**Does evidence increase?** Admission relies on evidence and may add verification evidence.

**Does promotion occur?** Yes, when the family defines and satisfies a promotion/admission gate.

**Does nothing permanent occur?** No when promotion is actually recorded; yes if the conclusion remains only a non-recorded read-only report.

### 6. Observation -> Evidence -> Fact / projected belief

**Status:** independently recurring and implementation-backed, but not identical to generic inquiry movement.

`02-domain-model.md` states that raw observations may support Evidence, Evidence is immutable, Facts are interpretations of Evidence, FactSupport is rebuilt from Facts, and ProjectionStore is a deterministic cache rather than source of truth.

**What changes?**

- Raw observations can become immutable evidence records.
- Evidence-backed interpretations can become facts.
- Facts can aggregate into support and best/current belief projections.

**What does not change?**

- Observation is not fact.
- Evidence remains distinct from Fact.
- Projection is not verification and is not source of truth.

**Does knowledge change?** Yes when evidence-backed Facts are recorded or projected.

**Does authority change?** Yes within the knowledge/projection family, bounded by provenance, confidence, recency, and projection rules.

**Does state change?** Yes when events/facts/projections are written or rebuilt.

**Does only orientation change?** No.

**Does evidence increase?** Yes at observation/evidence acquisition; fact projection interprets existing evidence.

**Does promotion occur?** Yes only at the Evidence-to-Fact or FactSupport/current-belief boundary, not at raw observation.

**Does nothing permanent occur?** No if recorded; current projections remain rebuildable cache, not source of truth.

### 7. Architecture / pressure / boundary hypothesis -> implementation-backed recovery

**Status:** independently recurring as a recovery pattern, not as a generic transition engine.

Architecture-to-implementation recurs when implementation evidence shows a compressed boundary, owner, helper, payload, request, result, registry entry, diagnostic surface, or compatibility-preserving slice. It does not recur as architecture preference becoming implementation.

**What changes?**

- A responsibility boundary may become explicit in code, tests, registries, diagnostics, or documentation.
- Compatibility-preserving implementation can relieve pressure.

**What does not change?**

- Architecture prose alone does not create implementation.
- Presentation vocabulary does not become repository knowledge.
- Future pressure does not become a mandate.

**Does knowledge change?** Yes when implementation-backed recovery is documented and tested.

**Does authority change?** Yes for the recovered owner or surface, limited by implementation evidence.

**Does state change?** Code and tests change in implementation slices; characterization-only reports change repository documentation.

**Does only orientation change?** No.

**Does evidence increase?** Implementation evidence may be exposed, added, or tested.

**Does promotion occur?** Yes when a boundary is recovered or implemented; no when a report stops at frontier.

**Does nothing permanent occur?** No if code/docs/tests are committed; frontier reports preserve non-promotion.

### 8. Working methodology -> earned methodology

**Status:** recurring as a methodological pattern, but not a runtime family.

The repository repeatedly uses working methodology in reports, then earns or narrows it only when implementation evidence, repeated safe stops, tests, and compatibility behavior support it. Methodology can be preserved constitutionally without becoming runtime behavior.

**What changes?**

- A local working discipline becomes reusable repository method when repeatedly supported.
- The method may constrain future recovery work.

**What does not change?**

- It does not create a subsystem.
- It does not create runtime authority.
- It does not make its vocabulary canonical beyond what evidence supports.

**Does knowledge change?** Yes, as documented methodology.

**Does authority change?** Methodological authority changes for future investigations, not runtime authority.

**Does state change?** Only repository documentation unless implemented elsewhere.

**Does only orientation change?** No, but it remains weaker than implementation.

**Does evidence increase?** Usually the methodology is earned by accumulated evidence rather than by one new observation.

**Does promotion occur?** Yes, from local method to repository-preserved method, if documented and supported.

**Does nothing permanent occur?** No if the methodology is committed as repository artifact.

## Candidate transition families not independently recovered

The following candidate labels were not recovered as independently recurring families at the requested strength:

- **Communication -> truth.** Counterevidence is strong: orientation and inquiry notes explicitly deny truth authority.
- **Pressure -> implementation.** Pressure informs inquiry but does not command implementation.
- **Candidate Interpretation -> Selected Interpretation** for raw tokens such as `.`. Prior evidence rejected a first-class raw-token interpretation owner.
- **Question -> Inquiry** as an automatic transition. The repository requires exact eligibility, dispatch, or preserved note boundaries.
- **Evidence -> conclusion** as automatic movement. Evidence can support, contradict, remain insufficient, or feed projection; it does not conclude by itself.
- **Projection -> verification.** Projection is repeatedly bounded as rebuildable/current belief, not verification.
- **Architecture -> implementation** by preference. Architecture becomes implementation-backed only through code/tests/registries/compatibility evidence or remains frontier.

## Independence analysis

### Orientation != promotion

Orientation changes what can be lawfully examined next. Promotion changes repository knowledge, authority, implementation, documentation, or projection status. The `.` probe demonstrates orientation without promotion: the note was preserved, but the app found no deterministic related material and denied fact/claim/command/ownership/intent authority.

### Inquiry != admission

Inquiry is bounded work with a question, surface, evidence path, and stop condition. Admission is a later family-local gate. Bounded ask can reject unknown, diagnostic-only, missing-argument, or not-dispatchable families; those stops prove inquiry eligibility and admission are not the same.

### Evidence gathering != knowledge promotion

Observation and evidence acquisition can add evidence without producing a Fact or current belief. The domain model keeps Evidence immutable and Facts as interpretations; support aggregation and ProjectionStore rebuilds are separate.

### Interpretation != verification

Fact projection, answer composition, and orientation can interpret evidence or related material under limits. Verification requires a family-local gate such as capability verification, implementation tests, or explicit promotion readiness. The repository repeatedly warns that projection is not verification and candidate is not verified.

### Methodology != runtime

Constitutional documents and recovery reports can preserve earned methodology. They do not create runtime behavior unless implementation evidence supports a runtime owner.

## Negative transition analysis

Recurring architectural mistakes do arise from collapsing distinct families, but only the following are implementation-supported:

1. **Orientation becoming knowledge.** Inquiry orientation explicitly denies that preserved operator prose is a fact, claim, requirement, command, ownership assertion, intent, recommendation, or next safe move. Treating `.` orientation as repository knowledge would violate the app boundary.
2. **Candidate becoming admission.** Candidate inquiry reconciliation and the constitution preserve candidate/support/verified distinctions. Candidate inquiries must gather or compose evidence and can stop safely.
3. **Evidence becoming conclusion.** The domain model separates Evidence from Facts and FactSupport. Evidence can support conclusions but does not itself become the conclusion.
4. **Pressure becoming implementation.** The constitution states pressure informs inquiry and does not command work. Frontiers preserve pressure that recovery cannot yet relieve.
5. **Communication becoming truth.** The app-level orientation surface and constitutional rules show communication can orient or be preserved without becoming truth.
6. **Presentation vocabulary becoming knowledge.** AGENTS instructions and knowledge-reachability discipline warn that presentation labels are not automatically repository knowledge.

No stronger negative examples were recovered without risking invention.

## Locality

- **Globally shared discipline:** Repository authority wins; Null persists until evidence; stop is positive; observation is not fact; candidate is not verified; visibility is not authority.
- **Family-local transitions:** Observation/Evidence/Fact projection, capability verification, diagnostic recording, bounded ask dispatch, repository observation, and implementation recovery each define their own gates and state effects.
- **Competency-local transitions:** Inquiry orientation, answer composition, diagnostic/audit views, pressure audits, completion audits, and source navigation have local authority boundaries and should not be generalized into a universal engine.
- **Still unknown:** Transition composition across families, concurrent transitions, interruption, reversal, lineage, and whether a common transition vocabulary can be safely canonicalized beyond the constitution.

## Typed unknowns

- **Transition composition:** Unknown whether orientation, inquiry, evidence, support, and promotion compose under one formal model.
- **Concurrent transitions:** Unknown how simultaneous evidence acquisition and promotion gates should be described constitutionally.
- **Transition interruption:** Unknown whether a running inquiry has a preserved interruption state outside existing stop/report behavior.
- **Transition reversal:** Unknown beyond known supersession, stale facts, contradictions, and archive/promotion reviews.
- **Transition lineage:** Partially visible in evidence support and reasoning paths, but not recovered as a general constitutional transition lineage system.
- **Global naming:** Unknown whether labels such as `transition family` should be promoted to canonical repository vocabulary.
- **Runtime representation:** No evidence supports a universal transition engine or runtime transition registry.

## Smallest truthful answer

The smallest recurring constitutional transition is:

```text
orientation
```

More precisely:

```text
communication / observation / pressure
↓
orientation
```

It is the smallest because it can occur without evidence increase, knowledge change, authority change, state mutation, promotion, admission, fact projection, or implementation recovery. The `.` probe demonstrates this boundary directly: it lawfully preserved/used orientation and produced no new knowledge.

## Lawful termination

This report stops at characterization. It does not introduce a transition engine, redesign runtime, stabilize new terminology as canonical, recommend implementation, or assume that every transition promotes knowledge.

The strongest supported answer is:

```text
There are many constitutional transition families, not one generic movement.
The families recur because their effects differ.
The repository has compressed some of them in language, but implementation evidence repeatedly separates orientation, inquiry, evidence, support, admission, projection, implementation recovery, and earned methodology.
```

## Remaining questions

1. Are transition-family labels useful enough to add to any registry, or should they remain report vocabulary?
2. Can knowledge-reachability audits prove or reject `transition family` as repository knowledge?
3. Which family owns reversal/supersession when a promoted conclusion later loses support?
4. Are diagnostic recording boundaries sufficient to prevent orientation or evidence from becoming cluster truth?
5. Do completion audits and promotion reviews share a deeper transition pattern, or only a methodological resemblance?

## Confidence

- **High confidence** that orientation, bounded inquiry, evidence/support, promotion/admission, fact projection, implementation recovery, and earned methodology are distinct recurring constitutional movements.
- **High confidence** that `.` demonstrates orientation without promotion.
- **High confidence** that evidence gathering and knowledge promotion are distinct.
- **Medium confidence** in the family names used here; they are characterization labels, not canonical vocabulary.
- **Low confidence** that the repository should implement a general transition model; current evidence argues against that step.
