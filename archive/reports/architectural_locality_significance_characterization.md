# Architectural Locality Significance Characterization

## Status

This characterization asks whether the implementation repeatedly assigns architectural meaning to *where* a recovered participant appears. It does not recover new participants, invent city districts, or turn presentation vocabulary into knowledge. Repository authority wins.

## Evidence reviewed

Implementation-backed evidence reviewed:

- `architectural_neighborhood_topology_characterization.md`, especially the evidence list, neighborhood survey, street survey, chokepoints, termination boundaries, and negative limits.
- `representation_transformation_discipline_investigation.md`, especially `ObservationIngestor`, `StateProjector`, question-family inventory/explanation, recurring transitions, and producer/consumer refusals.
- `question_bounded_work_invocation_investigation.md` and the bounded-work slices, especially exact `QuestionFamily` lookup, eligibility, selection, dispatch request, and existing-surface execution.
- `bounded_inquiry_recovery_characterization.md`, especially bounded question reduction and refusal of generic inquiry machinery.
- `constitutional_interpretation_characterization.md`, especially evidence-gated transitions and stops.
- `docs/implementation_relationship_grammar_investigation.md`, especially producer/consumer/owner relationships and negative relationship limits.
- Runtime implementation files including `seed_runtime/observations.py`, `seed_runtime/evidence.py`, `seed_runtime/facts.py`, `seed_runtime/state.py`, `seed_runtime/question_surface_inventory.py`, `seed_runtime/bounded_work.py`, `seed_runtime/operational_story.py`, `seed_runtime/inquiry_orientation.py`, `seed_runtime/diagnostic_inventory.py`, `seed_runtime/diagnostic_shape_audit.py`, `seed_runtime/knowledge/observation_agreement.py`, `seed_runtime/knowledge/grammar_observation.py`, and `scripts/seed_local.py`.

Commands used:

```bash
pwd && rg --files -g 'AGENTS.md' -g '*.md' -g '*.py' | head -200
find .. -name AGENTS.md -print
cat AGENTS.md && git status --short
sed -n '1,220p' architectural_neighborhood_topology_characterization.md
sed -n '1,180p' implementation_relationship_grammar_characterization.md 2>/dev/null || true
sed -n '1,180p' question_bounded_work_invocation_investigation.md
sed -n '1,220p' seed_runtime/diagnostic_inventory.py
sed -n '1,180p' seed_runtime/diagnostic_shape_audit.py
rg -n "class Observation|ObservationIngestor|observation_to_evidence|observation_to_fact|class Fact|class Evidence|StateProjector|QuestionFamily|QUESTION_SURFACES|BOUNDED_ASK|apply_bounded_ask_dispatch|ObservationAgreement|GrammarObservation|Candidate" seed_runtime tests docs *.md -S
```

## Primary answer

Yes, implementation repeatedly assigns meaning to locality, but only in a bounded way.

A participant's architectural neighborhood often constrains its lawful role, authority, and expected relationships. The strongest evidence is not a universal architectural map; it is repeated local patterns where adjacency changes what the participant can do:

- An `Observation` near ingestion may become `Evidence` and sometimes `Fact`; an `Observation` near projection is replayed as a state collection item. Its role changes with the implementation street it occupies.
- `Evidence` near fact support can support current belief; generic extracted evidence can remain non-fact-producing. Evidence locality matters because not every evidence-bearing record is a truth-promotion authority.
- A `QuestionFamily` inside the inventory can be known but not executable; a `QuestionFamily` inside bounded ask eligibility/dispatch can select an existing surface only if registered in exact maps.
- A diagnostic surface inside `DIAGNOSTIC_INVENTORY` declares record/mutation/source contracts; the same surface inside shape audit is checked against implementation specs rather than treated as self-validating.
- Candidate-like participants near admission/readiness/verification remain candidates until evidence-gated local rules permit stronger status.

The smallest truthful conclusion is therefore:

```text
Locality is not meaningless.
Implementation repeatedly uses placement to limit authority and lawful relationships.
But locality is currently family-local and cross-family recurring, not a universal zoning constitution.
```

## Neighborhood expectation survey

| Recovered neighborhood | Participants that naturally belong here | Participants that never naturally appear here | Participants that arrive through recurring bridges | Participants that terminate here / cannot lawfully proceed further | Suspicious neighboring participants |
| --- | --- | --- | --- | --- | --- |
| Provider translation / source adaptation | Provider-native payloads, source records, adapter-local observations, decode/normalization decisions. | Fact authority, current-state truth, generic answer composition, cluster mutation. | Canonical `Observation` through adapter construction; sometimes structural records before observation. | Provider-native language terminates unless converted into Seed representation. | Direct `FactSupport` or answer conclusion without observation/evidence bridge. |
| Observation | Canonical observed subject/predicate/value/provenance, dimensions, confidence, expiry, metadata. | Answer surfaces, dispatch surfaces, diagnostic shape declarations, readiness decisions. | Provider translation enters here; ingestion bridges to evidence and optional fact. | Observation may stop at observation/evidence when fact promotion is suppressed. | Direct operational command, verified capability, or current truth without ingestion/projection boundary. |
| Evidence / supporting evidence | Provenance payloads, evidence IDs, supporting fact references, source confidence, support summaries. | Surface selection authority, generic truth authority, mutation authority. | Observation ingestion, fact extraction, projected support, answer composition. | Evidence can lawfully terminate as support without becoming fact or reason. | Direct dispatch target or implementation readiness without evaluation/admission bridge. |
| Fact / projected state | Fact records, fact support, inferred facts, relationship projection, current samples, ambiguity/conflict. | Provider-native payloads, free-form questions, diagnostic declaration authority. | Observation+evidence bridge; ledger replay through `StateProjector`. | Projection terminates at read models/views; it does not rewrite event authority. | Source adapters or CLI dispatch directly mutating projected truth. |
| Bounded inquiry / QuestionFamily | Exact registered question family, inventory row, answer responsibility, boundary, diagnostic relationship. | Free-text semantic classifier, universal planner, unregistered question identity. | Bounded ask eligibility bridges known families to dispatchability; diagnostic inventory bridges visibility. | Diagnostic-only and not-dispatchable families terminate at inventory/explanation. | Arbitrary answer execution beside unknown family. |
| Bounded ask / dispatch | Eligibility result, selected existing surface, required surface args, dispatch request, CLI namespace mutation. | Answer composition internals, evidence acquisition, semantic question understanding. | Exact `QuestionFamily` plus eligibility/selection bridges into existing direct surfaces. | Dispatch terminates after setting an existing surface flag; the selected surface owns answer construction. | New generic work executor beside bounded ask maps. |
| Answer composition | Surface-local answer, reason, support, boundary, limitations, rendered output. | Raw provider translation, inventory declaration self-validation, event-ledger mutation. | Evidence/support and dispatch arrive through surface-specific builders. | Rendering is the outer boundary; composition does not create truth. | Provider-native payload or question-family registry rows treated as final answer without builder. |
| Diagnostic inventory | Diagnostic names, CLI flags, JSON/record support, record scope, event-ledger and cluster mutation declarations. | Shape-audit observed implementation result, semantic diagnostic findings, cluster truth. | Operational surfaces arrive by explicit registry entry. | Inventory declares; it does not validate its own declarations. | Unregistered operational surface, or `mutates_cluster=true` for read-only diagnostic without intentional evidence. |
| Diagnostic shape audit | Implementation specs, static markers, declared-vs-observed rows, consistency/warning/mismatch/unknown status. | Diagnostic declaration ownership, runtime semantic authority over every finding. | Diagnostic inventory bridges into audit specs. | Shape audit terminates at shape consistency rows. | A diagnostic finding promoted directly to cluster fact merely because audit saw a flag. |
| Observation agreement / grammar observation | Independent evidence stream comparisons, candidate agreement, recurring relation-shape observation. | Semantic truth, architectural truth, universal grammar law. | Exact evidence equality bridges to candidate agreement; repeated agreement shape bridges to grammar observation. | Candidate agreement and grammar observation stop at recurrence/shape unless other implementation promotes them. | Direct fact, relationship law, or architecture conclusion beside one agreement. |
| Candidate / admission / readiness | Capability candidates, candidate requests, non-selected alternatives, verification evidence, readiness support/refusal. | Verified capability, selected operation, implementation authorization by vocabulary alone. | Evidence-gated verification/admission/readiness bridges. | Candidate status lawfully terminates when evidence is absent or insufficient. | Capability execution or implementation change adjacent to unadmitted candidate. |

## Unexpected placement survey

Representative placement tests:

1. **`Observation` inside answer composition** would suggest compressed ownership or a missing evidence/support bridge unless the surface is explicitly reporting observations as observations. Implementation repeatedly places observations before evidence/fact/projection, while answer composition consumes support/reason/boundary payloads.

2. **`FactSupport` inside provider translation** would be suspicious. Provider translation can produce observations or structural source records, but support belongs after facts are projected or assembled into explanations. Such placement would likely compress source adaptation with truth/support authority.

3. **`QuestionFamily` inside projection** would not be automatically unlawful, but current implementation evidence expects question families in inventory, eligibility, and dispatch surfaces. Projection owns event replay/read models, not question registration. Its appearance there would require family-local evidence, otherwise it would look like a missing registry/dispatch bridge.

4. **`DiagnosticShapeAuditRow` inside diagnostic inventory** would suggest collapsed declaration and validation. The implementation separates inventory declarations from shape-audit observed/static checks.

5. **`Candidate` beside execution authority** is suspicious unless an admission/verification/selection bridge is present. Candidate surfaces preserve possibility and non-selected alternatives; execution or verified capability needs stronger local evidence.

6. **`Reason` beside raw evidence** can be lawful in answer builders that explicitly compose reason from support. It is suspicious if the reason appears before evidence/support acquisition or if it substitutes for support.

7. **`GrammarObservation` beside semantic truth** is suspicious. The implementation-backed grammar observation neighborhood observes recurrence shape after agreement; it does not itself prove architectural truth.

8. **Diagnostic findings attached directly to hosts/services/filesystems** are suspicious for diagnostic-only outputs unless the implemented boundary intentionally changes. The repository instructions and inventory fields require diagnostic-run scope and distinguish cluster mutation from event-ledger diagnostic writes.

## Bridge significance

Recurring bridges are significant when they preserve an authority change that neighboring districts cannot lawfully perform directly:

- **Provider translation -> Observation** exists because provider-native language is not Seed's canonical observed claim shape.
- **Observation -> Evidence** exists because observation provenance must become an evidence record before later support/explanation can refer to it.
- **Observation + Evidence -> Fact** exists because fact promotion needs both observed content and evidence linkage, and may be suppressed.
- **Event ledger -> Projection -> State/read models** exists because projected state is rebuilt from events; views and diagnostics should not rewrite ledger authority.
- **QuestionFamily -> Eligibility -> Selection/Dispatch -> Existing surface** exists because exact registration is not the same as executability, and executability is not answer composition.
- **Diagnostic inventory -> Shape audit** exists because declaration is not validation.
- **Candidate -> Admission/Verification/Readiness** exists because possibility is not capability, truth, selection, or implementation authority.
- **Observation agreement -> Grammar observation** exists because exact agreement is only candidate recurrence evidence; it does not directly authorize semantic architecture.

Some bridges also reflect implementation convenience or compressed ownership. Bounded ask still has CLI-adjacent compatibility behavior, and provider translation is not uniformly staged. These compressions do not erase the recurring meaning of the bridges; they limit how broadly the characterization can be stated.

## Negative authority

Implementation evidence rejects the following claims:

### `Location is meaningless.`

Rejected. Placement changes authority: observation ingestion, projection replay, bounded ask dispatch, diagnostic declaration, shape audit validation, and candidate admission each impose different lawful actions on participants with similar names.

### `Every participant belongs everywhere.`

Rejected. Unknown `QuestionFamily` values cannot dispatch; diagnostic-only families cannot become bounded ask execution; candidate agreement does not become semantic truth; evidence does not necessarily become fact; inventory declarations do not validate themselves.

### `Neighborhoods are interchangeable.`

Rejected. Diagnostic inventory and diagnostic shape audit are adjacent but non-interchangeable. Dispatch and answer composition are adjacent but non-interchangeable. Provider translation, observation, evidence, fact, and projection are recurring but non-interchangeable positions.

### `Topology is merely documentation.`

Rejected in part. Some topology is documented methodology only, but the strongest corridors are implemented through dataclasses, registries, conversion functions, projection replay, CLI dispatch maps, and tests. The current claim is not that every diagram is code-backed; it is that several recurring localities are code-backed.

## Locality classification

Current locality is:

- **Implementation-local** for concrete surfaces such as observation ingestion, projection, bounded ask dispatch, diagnostic inventory, diagnostic shape audit, observation agreement, and grammar observation.
- **Family-local** for observation/evidence/fact, question-family/bounded-ask, diagnostic inventory/shape-audit, candidate/admission/readiness, and answer-composition neighborhoods.
- **Cross-family recurring** in the repeated discipline that a participant's authority changes only across explicit bridges: candidate-to-admitted, declaration-to-audited, question-to-dispatch, observation-to-evidence/fact, evidence-to-support/reason.
- **Methodological** where reports name pressure, locality, recovery, or constitutional interpretation beyond a specific implemented owner.
- **Not constitutional as a universal graph.** The repository repeatedly rejects a universal architectural graph or generic transition model.
- **Unsupported** for any zoning rule that would claim every participant has one lawful neighborhood across all contexts.

## Typed unknowns

- **Neighborhoods awaiting implementation:** Some recovered neighborhoods remain primarily methodological, including broad responsibility evaluation, implementation readiness, constitutional recovery, and generalized provider-language contract recovery.
- **Compressed districts:** Provider translation and source adapters sometimes combine decoding, identity choice, predicate choice, and observation construction. Bounded ask still keeps compatibility-oriented behavior near CLI dispatch.
- **Future bridges:** Additional bridges may be needed if future work separates provider translation, candidate admission, or answer composition further, but this characterization does not recommend implementation.
- **Accidental-looking locality:** Some co-location may be file/module convenience rather than architecture; locality is only counted where conversion, registry, dispatch, projection, or validation behavior backs it.
- **Topology lacking implementation evidence:** City-like labels, presentation vocabulary, and prior prose are not promoted without implementation evidence.

## Smallest truthful answer

Implementation repeatedly assigns meaning to where a participant appears. Locality is not merely an artifact of the current implementation.

The smallest earned discipline is:

```text
A recovered participant's lawful role is family-local.
Its expected neighbors matter when implementation uses explicit bridges,
registries, conversion functions, projection replay, validation specs,
or evidence-gated admission to change its authority.
Do not generalize that locality into a universal architectural graph.
```

## Lawful termination

This characterization terminates at locality significance. It does not:

- recover new participants;
- introduce new diagnostics, CLI flags, or recordable output;
- change source code behavior;
- recommend refactors;
- promote presentation vocabulary into knowledge;
- declare a universal topology;
- assume surprising placement is incorrect without local implementation evidence.

## Remaining questions

- Which currently methodological neighborhoods have enough implementation support to become family-local rather than report-local?
- Where is provider translation intentionally compressed, and where is the compression only historical convenience?
- Are there future tests that should preserve locality boundaries for answer composition or candidate admission without adding new surfaces?
- Which locality patterns are cross-family recurrence versus coincidental similarity?
- How often do diagnostic-only findings remain scoped to diagnostic runs in recorded event-ledger practice?

## Confidence

**Moderate.** Confidence is high that locality matters in observation/evidence/fact, projection, bounded ask, diagnostic inventory/shape audit, and candidate/admission neighborhoods. Confidence is lower for broad constitutional claims, generalized locality rules, and implementation-readiness neighborhoods because those remain partly methodological or compressed.
