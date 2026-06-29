# Architectural Inquiry Orientation Surface Audit

## Scope

This is a bounded implementation audit. It does not implement a runtime surface, CLI flag, schema, registry, completion database, manual work queue, status flag, configuration file, active-edge marker, or architect-maintained metadata.

The question is whether Seed already contains enough implementation evidence to answer:

```text
Where am I
within the current architectural evolution?
```

Repository authority wins: this audit treats implementation slices, tests, generated architecture evidence, existing read-only inquiry surfaces, and prior implementation audits as evidence. It does not treat operator memory, preferred labels, or investigation prose alone as authority.

## Short answer

Partially yes.

Seed already contains enough implementation evidence to derive a bounded architectural self-orientation answer for the architectural projection work represented by the responsibility-family slices:

```text
active responsibility family
current implementation boundary
implemented boundaries
remaining compressed boundaries
natural stopping point
confidence
recommended next architectural inquiry
```

However, Seed cannot derive that answer automatically today through a dedicated runtime or CLI surface. The derivation is currently available by reading repository artifacts and implementation-backed audits. A read-only architectural inquiry orientation surface now naturally emerges as the next implementation step, but this audit does not implement it.

## Evidence reviewed

The audit reviewed these repository artifacts:

- `responsibility_family_completion_inquiry_audit.md`.
- `inquiry_lineage_architectural_projection_slice_methodology.md`.
- `operational_responsibility_slice_001.md` through `operational_responsibility_slice_006.md`.
- `execution_visibility_slice_001.md` through `execution_visibility_slice_005.md`.
- `observation_derived_capability_slice_001.md` through `observation_derived_capability_slice_005.md`.
- Existing inquiry surfaces and inquiry artifact visibility implementation:
  - `seed_runtime/inquiry_orientation.py`.
  - `tests/test_inquiry_orientation.py`.
  - `seed_runtime/inquiry_artifacts.py`.
  - `tests/test_inquiry_artifacts.py`.
- Existing implementation audits and investigations that distinguish repository-visible inquiry state from human-interpreted inquiry movement:
  - `docs/repository_visible_inquiry_state_investigation.md`.
  - `docs/inquiry_artifacts_and_inquiry_continuity_investigation.md`.
  - `docs/inquiry_orientation_surface_family_observation.md`.
  - `architectural_invariant_recovery_investigation.md`.

## What architectural self-orientation would have to answer

A repository-derived architectural orientation answer needs more than completion status. It needs to answer where the work currently sits inside the architectural evolution:

```text
active responsibility family
current implementation boundary
implemented boundaries
remaining compressed boundaries
natural stopping point
confidence
recommended next architectural inquiry
```

These fields are not proposed as stored metadata. They are the minimum orientation facts this audit looked for in existing implementation evidence.

## Required implementation evidence

A read-only architectural orientation surface would require evidence for each field.

| Orientation field | Required evidence | Current repository evidence |
| --- | --- | --- |
| Active responsibility family | A family can be identified from repository-local implementation-slice lineage rather than an operator note. | Slice families are explicit in filenames and slice reports: operational responsibility, execution visibility, and observation-derived capability. The lineage methodology identifies those as responsibility families. |
| Current implementation boundary | A most recent or terminal boundary in a family can be identified from implementation-backed slices. | The latest slices name terminal or final handoff boundaries: `Execution Recording != Post-Execution Knowledge Extraction`, `State Build Visibility != Projection Cache Diagnostics`, and `Capability Inventory != Executable Operation Contract`. |
| Implemented boundaries | Each recovered boundary has compatibility-preserving implementation evidence and tests. | The family completion audit lists implemented boundary chains and supporting implementation changes for all three families. Each slice records selected boundary, before/after implementation evidence, compatibility preservation, files changed, and tests. |
| Remaining compressed boundaries | Remaining work appears as implementation-backed compression, not a manual backlog. | Latest family slices include `Remaining compressed ... boundaries` sections with concrete implementation candidates. |
| Natural stopping point | The family has a point where continuing would require recovering a new boundary or adjacent family. | The family completion audit derives natural termination from the point where the named recovered chain has implementation-backed slices and remaining compression is adjacent or outside the chain. |
| Confidence | Confidence can be derived from strength and scope of evidence, including whether remaining compression is inside or adjacent to the named family. | The family completion audit assigns high confidence to recovered chains and medium confidence to broad domain labels because adjacent compression remains. |
| Recommended next architectural inquiry | A next inquiry can be derived from remaining compression and unsupported conclusions without introducing a manual queue. | Remaining compressed boundaries in the latest slices and unsupported conclusions in audits identify candidate next inquiries. The prior completion audit recommended a read-only responsibility-family inquiry surface rather than another projection slice. |

## Derivable answers today

### Active responsibility family

Seed can derive active responsibility-family context only within the bounded set of already documented architectural projection families.

The strongest repository evidence identifies three completed or bounded families:

```text
Operational Responsibility
Execution Visibility
Observation-Derived Capability
```

The evidence does not prove a universal active family for every possible future architectural inquiry. It supports orientation over the current architectural evolution chain because those families are named repeatedly by implementation-backed slice sequences and summarized by the responsibility-family completion audit.

Supported conclusion: Seed can identify architectural work families when the family has a repeated slice sequence with implementation evidence.

Unsupported conclusion: Seed can infer the operator's currently intended family from arbitrary prose without an explicit inquiry note or deterministic repository signal.

### Current implementation boundary

Seed can derive the current implementation boundary for each family by reading the latest implementation slice in that family:

- Operational Responsibility currently terminates at:

```text
Execution Recording != Post-Execution Knowledge Extraction
```

- Execution Visibility currently terminates at:

```text
State Build Visibility != Projection Cache Diagnostics
```

- Observation-Derived Capability currently terminates at:

```text
Capability Inventory != Executable Operation Contract
```

This is implementation-backed because the latest slice reports describe the selected architectural boundary, implementation evidence, before/after responsibility separation, files changed, tests, and remaining compression.

Supported conclusion: Current boundary is derivable for a known slice family.

Unsupported conclusion: Current boundary is derivable from vocabulary alone. Boundary labels require implementation evidence.

### Implemented boundaries

Implemented boundaries are already available from the family completion audit and the individual slice reports.

Operational Responsibility has implementation-backed slices for:

```text
Capability Recommendation != Operation Selection
Operation Selection != Registered Operation Validation
Registered Operation Validation != Policy Authorization
Policy Authorization != Execution Realization
Execution Realization != Execution Recording
Execution Recording != Post-Execution Knowledge Extraction
```

Execution Visibility has implementation-backed slices for:

```text
Status Emission != Status Consumption
Execution Status != Execution Timing
Execution Timing != Cache Visibility
Execution Visibility != Execution Diagnostics
State Build Visibility != Projection Cache Diagnostics
```

Observation-Derived Capability has implementation-backed slices for:

```text
Observed Evidence != Executable Operation Contract
Observed Evidence != Capability Verification
Capability Verification != Capability Promotion
Capability Promotion != Capability Inventory
Capability Inventory != Executable Operation Contract
```

Supported conclusion: Implemented boundaries can be derived from slice reports without a completion registry.

Unsupported conclusion: A boundary is implemented merely because it appears in investigation prose.

### Remaining compressed boundaries

Remaining compressed boundaries are already repository-visible in latest slice reports. They are not manual task records; they are implementation-backed counterexamples discovered while making a specific boundary explicit.

Examples include:

- Pending-action creation vs. policy denial routing.
- Approved pending-action resumption vs. fresh call authorization.
- Projection build diagnostics passing replay/build evidence through cache-building paths.
- Fact-index cache lookup/load timing adjacent to cache-status reporting.
- Capability inventory still presenting a compatibility union of registered operation contract labels, requested capabilities, and admitted verification fact subjects.
- Registered operation contract derivation still represented by `ToolSpec` capability metadata rather than a public contract-derivation API.

Supported conclusion: Seed can identify remaining compressed architectural work inside the audited families by reading the latest slice evidence.

Unsupported conclusion: Remaining compression should become a manual queue, priority database, or status registry.

### Natural stopping point

The responsibility-family completion audit already derives natural termination from implementation evidence:

- Operational Responsibility naturally stops after the execution-recording to post-execution-knowledge-extraction boundary because the central registered-operation chain from recommendation through extraction has implementation-backed slices.
- Execution Visibility naturally stops after state-build visibility is separated from projection-cache diagnostics because the named status/timing/cache/diagnostic chain has implementation-backed slices.
- Observation-Derived Capability naturally stops after capability inventory is separated from executable operation contract metadata because the read-only chain closes the loop between observed evidence, verification, promotion readiness, inventory, and executable contract metadata.

Natural stopping point is therefore not a stored completion flag. It is a derived conclusion: the current recovered chain has been projected, and further work would require a new recovered boundary or adjacent family.

Supported conclusion: Natural termination can be derived for already recovered family chains.

Unsupported conclusion: Natural termination means the broader domain is architecturally exhausted.

### Confidence

Confidence already emerges from evidence quality and scope:

- High confidence where a named recovered chain has slice-by-slice implementation evidence, compatibility preservation, tests, and generated architecture updates where relevant.
- Medium confidence where the broader family label includes adjacent unresolved compression.
- Low or unsupported confidence where a term is only presentation vocabulary or investigation prose without implementation-backed evidence.

This matches existing repository discipline: the family completion audit distinguishes high confidence for recovered chains from medium confidence for broad labels.

Supported conclusion: Confidence can be derived without a manual confidence flag if it is computed from evidence strength and unresolved compression scope.

Unsupported conclusion: Confidence can be inferred from operator certainty or preferred terminology.

### Recommended next architectural inquiry

The existing evidence points to one strongest next implementation step:

```text
Implement a read-only architectural inquiry orientation surface.
```

That recommendation is supported because:

- The prior family completion audit already found that a read-only responsibility-family inquiry surface naturally emerges.
- Existing inquiry orientation code proves that Seed can expose read-only orientation while preserving strong authority boundaries.
- Existing inquiry artifact visibility code proves Seed can classify inquiry artifacts without creating workflow, planning behavior, or inquiry graphs.
- The current audit widens the question from `Is this family complete?` to `Where am I within the architectural evolution?`, and the required answer fields are already present in implementation-backed artifacts.

The recommended next implementation should compose repository evidence from existing slices and audits. It should not store status, active edge, manual next work, priorities, or completion metadata.

## Relationship to responsibility families

Responsibility families are the strongest available unit of architectural self-orientation.

They provide:

- a bounded family identity;
- an ordered sequence of implementation-backed boundaries;
- a latest/current boundary;
- a family-local set of remaining compressed boundaries;
- a derived natural stopping point;
- confidence based on whether unresolved compression is inside or adjacent to the recovered chain.

The repository evidence therefore supports this orientation shape:

```text
responsibility family
    -> implemented boundaries
    -> current/terminal boundary
    -> remaining compressed boundaries
    -> natural stopping point
    -> next inquiry candidate
```

This relationship is derived from implementation slices, not from a separate responsibility-family registry.

## Relationship to inquiry orientation

Existing inquiry orientation work is adjacent but not identical.

`seed_runtime/inquiry_orientation.py` is a read-only inquiry-note orientation probe. It preserves operator prose outside the event ledger and deterministically relates note tokens to already projected read models. Its authority boundary explicitly says that the orientation does not assert importance, ownership, intent, concern, recommended action, or next safe move.

That implementation matters because it proves a compatible shape for future architectural orientation:

- read-only rendering;
- deterministic evidence selection;
- explicit uncertainty;
- explicit authority boundary;
- no event ledger writes;
- no State mutation;
- no provider calls;
- no workflow, planning, or action creation.

But the current inquiry orientation surface cannot answer the architectural self-orientation question by itself. It orients an inquiry note to related material; it does not compose responsibility-family progression, current boundary, remaining compressed boundaries, natural stopping point, or next architectural inquiry.

Supported conclusion: Existing inquiry orientation establishes a safe surface pattern.

Unsupported conclusion: Existing inquiry orientation already is the architectural work-orientation surface.

## Relationship to implementation audits

Implementation audits already preserve many of the needed orientation ingredients:

- supported conclusions;
- unsupported conclusions;
- evidence reviewed;
- boundary scope;
- remaining gaps;
- recommended next step.

However, implementation audits are currently document-visible rather than automatically composed. The repository can answer the question through those artifacts, but Seed does not yet have a dedicated implementation surface that extracts and renders the answer.

This means the evidence is sufficient for a next implementation step, not sufficient to claim an existing runtime answer surface.

## Counterexamples and limitations

Architectural self-orientation still depends on human interpretation in several cases.

### Operator memory still appears when choosing the current family

If the question is asked without a repository-visible selector, Seed cannot know whether the operator means operational responsibility, execution visibility, observation-derived capability, inquiry continuity, repository observation, source navigation, or another family.

A future surface could avoid this by rendering all derivable families or requiring an explicit family selector. It should not add a manual active-family marker.

### Investigation prose is not enough

Many documents contain boundary language, findings, and open questions. That does not make every phrase implementation-backed architectural state. Existing AGENTS instructions also warn that terms such as current work position, source navigation, active edge, and projection cache may be presentation labels rather than repository knowledge.

A future surface must rely on slice reports and implementation evidence, not arbitrary prose headings.

### Terminology is unstable

Possible names such as these are only candidate presentation labels:

```text
Architectural Inquiry Orientation
Architectural Work Orientation
Architectural Progress Inquiry
```

No naming should be treated as repository authority until the implementation chooses a bounded surface responsibility and tests it.

### No automatic derivation surface exists yet

The repository contains enough evidence to support the answer, but the answer is not yet available through a dedicated `seed` command, diagnostic surface, read model, or tested renderer.

### The evidence is strongest for projection-slice families

The derivation is strong for the three responsibility-family slice sequences. It is weaker for unrelated architectural work that has audits but not repeated compatibility-preserving implementation slices.

## Missing implementation evidence

The following evidence is still missing before Seed can answer architectural self-orientation automatically:

1. A read-only implementation surface that discovers or receives repository-local family evidence.
2. A deterministic parser or structured extractor for slice evidence, or an implementation-backed in-repository representation generated from existing artifacts.
3. Tests proving implemented boundaries, remaining compressed boundaries, natural stopping point, confidence, and next inquiry are rendered from evidence rather than hard-coded operator memory.
4. Authority-boundary tests proving the surface does not create manual queues, registries, status flags, configuration files, active-edge markers, State mutations, event-ledger writes, provider calls, plans, pending actions, or architectural projections.
5. If exposed as a diagnostic CLI, diagnostic inventory and shape-audit coverage under the repository's operational visibility contract.

## Supported conclusions

- Seed can already determine where it is within the bounded architectural evolution represented by responsibility-family projection slices, when the question is scoped to those families.
- The strongest implementation evidence is the repeated slice pattern: selected boundary, implementation evidence, compressed ownership, boundary made explicit, compatibility preserved, files changed, tests, and remaining compressed boundaries.
- Responsibility-family status is not stored metadata; it is derivable from implementation-backed slice evidence.
- Architectural self-orientation is a broader inquiry than completion. Completion is one possible output of orientation, not the central question.
- Remaining compressed boundaries already provide repository-backed next inquiry candidates without becoming a manual work queue.
- Existing inquiry orientation and inquiry artifact surfaces prove Seed can expose read-only inquiry-related orientation with explicit authority boundaries.
- A read-only architectural inquiry orientation surface now naturally emerges as the next implementation step.

## Unsupported conclusions

- Seed cannot automatically answer architectural self-orientation today through a dedicated runtime surface.
- Seed cannot infer the operator's intended active family from memory or arbitrary prose.
- Seed cannot treat every investigation heading, presentation label, or vocabulary phrase as implementation-backed architecture.
- Seed cannot claim all operational, visibility, capability, inquiry, or repository-observation architecture is complete.
- Seed should not add manual work queues, completion registries, priority databases, status flags, configuration files, architect-maintained metadata, or active-edge markers.
- Seed should not perform another architectural projection slice merely to answer the orientation question; the next work should first expose the already available evidence.

## Acceptance answers

### Can Seed determine where it is within its own architectural evolution?

Yes, partially and boundedly.

Seed can determine this for the architectural projection work represented by existing responsibility-family slices. It can derive family, implemented boundaries, latest/current boundary, remaining compressed boundaries, natural stopping point, confidence, and next inquiry candidate from repository evidence. It cannot yet do this automatically through a dedicated surface.

### What implementation evidence supports that answer?

The supporting evidence is:

- the architectural projection slice methodology;
- three responsibility-family slice sequences;
- the family completion audit;
- slice-local implementation evidence, files changed, compatibility-preservation claims, and tests;
- existing read-only inquiry orientation and inquiry artifact visibility implementations;
- implementation audits that distinguish supported and unsupported conclusions.

### What evidence is still missing?

The missing evidence is a tested read-only implementation surface that composes the existing artifacts into an architectural orientation answer. If surfaced as a diagnostic CLI, diagnostic inventory and diagnostic shape-audit evidence would also be required.

### Does a read-only architectural inquiry orientation surface now naturally emerge?

Yes.

The surface naturally emerges because the answer fields are already recurring, repository-local, and implementation-backed. The surface should be read-only, deterministic, evidence-rendering, and explicit about uncertainty and authority boundaries.

### Should the next implementation work be that inquiry surface?

Yes.

The next implementation work should be a read-only architectural inquiry orientation surface. It should compose existing implementation evidence and prove through tests that it does not create manual status state, registries, work queues, runtime mutation, or new architectural projection behavior.
