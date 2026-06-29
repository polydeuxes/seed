# Architectural Object Kind Taxonomy Audit

## Scope

This is a bounded architectural audit. It does not recover a new responsibility
family, perform an implementation slice, introduce a runtime classification
system, add a classification registry, add metadata, change schemas, change CLI
behavior, or implement an automatic classifier.

The audit asks whether Seed can now distinguish multiple architectural object
kinds from implementation evidence rather than terminology. Repository authority
wins.

## Short answer

Yes, boundedly.

Seed now supports multiple implementation-backed architectural object kinds. The
strongest supported kinds are:

- Responsibility Family
- Architectural Pattern
- Implementation Idiom
- Compatibility Surface
- Inquiry
- Projection

The distinction is not a taxonomy runtime. It is a repository-evidence discipline:
a recovered concept should be classified by what it owns, what decisions it can
make, what durable artifacts it creates or preserves, what runtime behavior it
has, what invariants it maintains, and what implementation evidence proves those
claims.

This reduces unnecessary family proliferation because recurring implementation
evidence no longer implies responsibility-family status. Compatibility Handoff is
the key counterexample: it recurs across families, but the repository evidence
supports classifying it as an architectural pattern rather than a new family.

## Evidence reviewed

Primary repository evidence reviewed:

- `responsibility_family_completion_inquiry_audit.md`
- `implementation_responsibility_family_inventory_audit.md`
- `compatibility_handoff_classification_audit.md`
- `architectural_inquiry_orientation_surface_audit.md`
- `architectural_orientation_answer_composition_audit.md`
- `architectural_recoverability_inquiry_audit.md`
- `inquiry_lineage_family_vocabulary_audit.md`
- `inquiry_lineage_architectural_projection_slice_methodology.md`
- `implementation_evidence_primary_architectural_object_audit.md`
- `seed_runtime/projection_shape.py`
- `seed_runtime/projection_store.py`
- representative tests named by those audits.

The audit treats implementation files, test-backed surfaces, completed slice
reports, and prior implementation-backed audits as authority. It does not treat
conversation history, operator preference, or recurrence of a phrase as authority.

## Classification method

A candidate architectural object kind is supported only when repository evidence
can answer:

```text
owner
repository decisions
durable artifacts
runtime behavior
architectural invariants
implementation evidence
limitations
```

A concept is not promoted to a responsibility family merely because it recurs. It
must own independent repository decisions, durable artifacts or externally
observable behavior, and architectural invariants that are not already owned by
another family or surface.

## Candidate architectural kinds

### 1. Responsibility Family

#### Owner

A responsibility family owns a recurring implementation responsibility across a
bounded chain of recovered architectural boundaries. The owner is the family
itself, expressed through implementation seams, public behavior preservation, and
slice lineage rather than through a registry.

Current implementation-backed examples:

- Operational Responsibility
- Execution Visibility
- Observation-Derived Capability
- Answer Composition
- Inquiry Lineage

#### Repository decisions

Responsibility families decide how their owned responsibility is separated from
adjacent responsibilities. Examples include operation selection versus validation,
status emission versus consumption, observed evidence versus executable operation
contract, answer material versus answer presentation, and result material versus
lineage material.

#### Durable artifacts

A family may own durable events, read models, diagnostic surfaces, stable answer
objects, or implementation-local payloads when those artifacts are part of its
responsibility. The durable artifact is not required to be a new file or schema;
it may be an event kind, stable public object, report shape, or test-preserved
surface.

#### Runtime behavior

Responsibility families often own runtime behavior. Operational Responsibility
owns execution-path behavior; Execution Visibility owns status, timing, cache,
and diagnostic visibility behavior; Observation-Derived Capability owns read-only
capability verification, promotion-readiness, and inventory behavior; Answer
Composition owns bounded answer assembly; Inquiry Lineage owns result/lineage
separation inside inquiry surfaces.

#### Architectural invariants

Responsibility-family invariants are boundary invariants. Examples include:

- recommendation is not operation selection;
- registered operation validation is not policy authorization;
- execution recording is not post-execution knowledge extraction;
- status is not timing;
- cache visibility is not diagnostic mutation;
- observed capability evidence is not executable operation contract truth;
- selected result is not its lineage;
- answer composition is not rendering alone.

#### Implementation evidence

The strongest evidence is repeated compatibility-preserving projection slices.
The family completion audit lists implemented boundary chains for Operational
Responsibility, Execution Visibility, and Observation-Derived Capability. The
responsibility-family inventory audit further classifies Answer Composition and
Inquiry Lineage from recurring implementation ownership. The inquiry-lineage
vocabulary audit shows four independent specializations of `Outcome != Lineage
Frame`, `Selection Result != Selection Lineage`, `Derived Conclusion !=
Derivation Lineage`, and `Reference Choice != Comparison Lineage`.

#### Limitations

A family label can be over-broad. Existing audits repeatedly distinguish high
confidence for a recovered chain from lower confidence for the broader domain.
Adjacent compressed boundaries remain valid counterexamples to claiming that a
whole architectural area is exhausted.

#### Confidence

High for completed recovered chains. Medium for broad labels whose files still
contain adjacent compressed work.

### 2. Architectural Pattern

#### Owner

An architectural pattern owns no independent repository truth. It is a recurring
shape used by already-owned responsibilities.

Current implementation-backed example:

- Compatibility Handoff

#### Repository decisions

An architectural pattern does not make independent domain decisions. Compatibility
Handoff does not decide what a tool did, whether a capability is true, what a
diagnostic means, what answer is correct, or which reference was selected. Those
decisions remain with their owning families or surfaces.

#### Durable artifacts

A pattern owns no independent durable artifact. It may preserve or transport an
artifact owned elsewhere, such as a completed tool event, capability inventory
source set, diagnostic declaration, `OperationalStory`, or `ReferenceSelection`.

#### Runtime behavior

A pattern may have local sequencing or assembly behavior, but that behavior is
not independently architectural. Compatibility Handoff repeatedly preserves owner
boundaries while existing public compatibility objects or downstream consumers
continue to work.

#### Architectural invariants

The invariant is ownership preservation across a boundary, not creation of new
truth. Compatibility Handoff preserves before-owner and after-owner separation.

#### Implementation evidence

The compatibility handoff classification audit reviewed completed slices and
representative implementation files and classified Compatibility Handoff as a
recurring architectural pattern. The evidence shows repeated handoffs:
completed operational events to post-execution extraction, capability inventory
source unions, diagnostic inventory and shape-audit declarations, `OperationalStory`
payload assembly, and `ReferenceSelection` payload assembly.

#### Limitations

The pattern is stronger than a local idiom because it recurs across independent
families. It is weaker than a responsibility family because it owns no independent
repository decisions, durable artifacts, runtime behavior, or invariants outside
ownership preservation.

#### Confidence

High for Compatibility Handoff as a pattern. Low for promoting it to a family.

### 3. Implementation Idiom

#### Owner

An implementation idiom is owned by local code, not by architecture as an
independent object. Its owner is a function, helper, builder, fixture, naming
convention, or small internal structure.

#### Repository decisions

An idiom makes no repository-level architectural decision. It can make local code
clearer, deterministic, or easier to test, but it does not define a responsibility
boundary by itself.

#### Durable artifacts

Usually none. An idiom may contribute to an artifact produced by a family or
surface, but it does not own the artifact.

#### Runtime behavior

Any behavior is local and substitutable. If the idiom changes while external
behavior and architectural boundaries remain intact, the repository has not lost
an architectural object.

#### Architectural invariants

No independent architectural invariants. The relevant invariants are owned by the
surrounding family, pattern, or surface.

#### Implementation evidence

Repository evidence supports this kind mostly by negative classification. The
family inventory audit identifies presentation-only orientation vocabulary and
unsupported vocabulary as insufficient evidence for family status. The
recoverability audit requires a function, class, helper, dataclass, service,
event path, projection stage, diagnostic report, or read model to own part of a
distinction before it becomes recoverable. A recurring helper structure therefore
remains idiomatic unless it can show independent ownership or a repeated
recoverable boundary.

#### Limitations

The repository has not enumerated idioms, and this audit should not create an
idiom registry. Idiom classification is conservative: it is used when recurrence
is local, substitutable, and unsupported as a family or pattern.

#### Confidence

Medium. The distinction is supported as a boundary condition, but the repository
has not made idioms a first-class inventory.

### 4. Compatibility Surface

#### Owner

A compatibility surface is owned by the runtime or report surface that preserves
an existing public shape for callers, tests, JSON/text output, or diagnostic
consumers.

Current examples include:

- `OperationalStory`
- `ReferenceSelection`
- diagnostic inventory and diagnostic shape audit output
- projection-shape explanations
- cache-debug and state-build visibility output

#### Repository decisions

A compatibility surface decides what remains stable externally and which internal
payloads are assembled into that stable shape. It does not automatically own the
domain semantics of every field it carries.

#### Durable artifacts

Durable artifacts may include public object shapes, report rows, CLI output
sections, generated architecture evidence, or test-preserved output. They may be
recordable only when a specific diagnostic declares that behavior.

#### Runtime behavior

Compatibility surfaces can have runtime behavior: constructing reports,
rendering stable output, returning read-only views, or exposing diagnostic
contract rows.

#### Architectural invariants

The core invariant is compatibility preservation. Where the surface is
diagnostic, additional invariants include `record_scope=diagnostic_run`,
`writes_event_ledger` truthfulness, and `mutates_cluster=false` for read-only
surfaces.

#### Implementation evidence

Compatibility Handoff evidence demonstrates that public `OperationalStory` and
`ReferenceSelection` objects remain stable while private payload ownership is
separated. Execution Visibility evidence shows diagnostic inventory and
shape-audit output declaring and checking operational shape. Projection-shape code
composes existing projection-stage explanations without adding new evidence.

#### Limitations

A compatibility surface can be mistaken for a responsibility family when it
carries many fields. The repository evidence distinguishes the surface from the
owner of each field's truth.

#### Confidence

High for named implemented surfaces. Medium for newly observed output surfaces
until tests prove their shape and ownership boundary.

### 5. Inquiry

#### Owner

An inquiry owns a read-only architectural question and the evidence composition
needed to answer it. It does not own the underlying implementation facts.

Current examples include:

- Responsibility Family Completion
- Architectural Inquiry Orientation
- Architectural Visibility
- Architectural Recoverability
- Compatibility Handoff Classification
- Architectural Orientation Answer Composition

#### Repository decisions

An inquiry decides whether repository evidence is sufficient to answer a bounded
question and what remains unsupported. It does not implement the underlying
slice, registry, planner, or runtime system unless a separate task explicitly
asks for that work.

#### Durable artifacts

Current inquiry artifacts are audit documents and, for some non-architectural
inquiry surfaces, read-only runtime views such as `inquiry_orientation` and
`inquiry_artifacts`. The architectural inquiries reviewed here are primarily
durable reports, not implemented CLI surfaces.

#### Runtime behavior

Most reviewed architectural inquiries have no runtime behavior. Some existing
read-only inquiry surfaces demonstrate the answer-composition discipline, but the
architectural inquiry reports do not create new commands or mutation paths.

#### Architectural invariants

Inquiry invariants include repository authority, read-only scope, unsupported
conclusion sections, confidence boundaries, and separation between evidence and
operator preference.

#### Implementation evidence

The recoverability audit defines recoverability from implementation owners,
compressed call paths, bounded compatibility-preserving separation, and tests or
generated architecture evidence. The orientation audit derives active family,
current boundary, implemented boundaries, remaining compression, stopping point,
confidence, and next inquiry from repository artifacts. The answer-composition
audit shows that architectural orientation can be answered as `answer + reason +
support + boundary + limitations` rather than as a special subsystem.

#### Limitations

Architectural inquiries are not automatically runtime surfaces. The repository
can answer them by reading implementation-backed artifacts today, but many lack a
single `seed` command.

#### Confidence

High that Inquiry is a distinct kind. Medium for any given future inquiry until
it proves a bounded question and repository-local evidence basis.

### 6. Projection

#### Owner

Projection is owned by projection-state and projection-shape implementation. It
turns event or fact evidence into reusable projected state or read-only
explanations without making diagnostic-only or presentation-only findings into
cluster truth.

Current examples include:

- `ProjectionStore` and concrete snapshot stores
- `ProjectionShapeStage` definitions and explanations
- projection cache diagnostics and state-build visibility
- architectural projection slices as a methodology for making recovered
  boundaries explicit in implementation

#### Repository decisions

Projection decides how existing evidence is replayed, cached, summarized, or
explained. Architectural projection slices decide how one already-recovered
boundary becomes visible in implementation while preserving behavior and
compatibility.

#### Durable artifacts

Projection may own snapshots, summary snapshots, stage definitions, projection
shape reports, cache status, and generated architecture evidence. Architectural
projection slice reports are durable audit artifacts documenting the slice.

#### Runtime behavior

Projection has runtime behavior in state projection, projection cache storage,
projection-shape reporting, and projection diagnostics. Architectural projection
slice methodology is not itself runtime behavior; it is a recovered method shown
by implementation work.

#### Architectural invariants

Projection invariants include event-ledger versus projection-store separation,
read-only explanation boundaries, not adding evidence during explanation, and the
slice discipline of one recovered boundary, one implementation change, no
behavior change, no compatibility change, and no vocabulary migration.

#### Implementation evidence

`projection_store.py` states that event ledgers own append-only historical events
while projection stores own reusable cached projections. `projection_shape.py`
defines known projection stages and composes stage explanations from existing
fields without adding evidence. The projection slice methodology report describes
the recurring slice pattern across Operational Responsibility, Execution
Visibility, and Observation-Derived Capability.

#### Limitations

Projection is overloaded in repository vocabulary: runtime projection stores,
projection-shape explanations, projection-cache diagnostics, and architectural
projection slices are related but not identical. Classification must identify
which projection object is being discussed.

#### Confidence

High that projection exists as an implementation-backed kind. Medium where a
future use of the word `projection` is presentation vocabulary rather than a
runtime or slice-backed object.

## Supported classifications

| Concept | Supported kind | Why |
| --- | --- | --- |
| Operational Responsibility | Responsibility Family | Repeated boundary slices, runtime execution ownership, durable events, tests, remaining-compression boundaries. |
| Execution Visibility | Responsibility Family | Status/timing/cache/diagnostic slice chain, diagnostic inventory and shape audit evidence, read-only diagnostic invariants. |
| Observation-Derived Capability | Responsibility Family | Observed evidence, verification, promotion-readiness, inventory, and executable contract separation. |
| Answer Composition | Responsibility Family | Multiple answer surfaces share answer/reason/support/boundary/limitations ownership. |
| Inquiry Lineage | Responsibility Family | Repeated result-versus-lineage separations across reasoning path, selection path, reference selection, and related surfaces. |
| Compatibility Handoff | Architectural Pattern | Recurs across families but owns no independent decisions, durable artifacts, runtime behavior, or invariants beyond owner preservation. |
| `OperationalStory` public object | Compatibility Surface | Stable public answer surface assembled from privately owned answer payloads. |
| `ReferenceSelection` public object | Compatibility Surface | Stable public selection surface assembled from reference choice and comparison lineage payloads. |
| Responsibility Family Completion | Inquiry | Read-only question answered from completed slice evidence, not a runtime registry. |
| Architectural Recoverability | Inquiry | Bounded question about whether implementation evidence can recover a distinction before slice selection. |
| Projection store / projection shape | Projection | Runtime/read-only projection implementation owns cached projections and stage explanations. |
| Local helper decomposition without independent ownership | Implementation Idiom | Local, substitutable, and unsupported as independent architecture unless ownership evidence appears. |

## Unsupported classifications and counterexamples

The repository does not yet support confident classification for every recurring
concept.

### Recurring helper structures

A helper or internal payload structure may recur because it is convenient. Unless
it owns a repository decision, durable artifact, runtime behavior, or invariant,
it remains an implementation idiom. Recurrence alone is insufficient.

### Implementation conventions and coding style

Naming patterns, table formatting, dataclass grouping, or test fixture style do
not become architectural kinds without evidence of ownership. They can support a
family or surface but do not define one.

### Temporary investigation terminology

Terms used in one investigation are unsupported until tied to implementation
evidence. Repository instructions already warn that presentation vocabulary such
as continuation, current work position, source navigation, active edge, storage
topology, state build, and projection cache may be presentation labels rather
than repository knowledge.

### Unrecovered hypotheses

A concept may be plausible but unrecovered. It should remain an unsupported
hypothesis until evidence shows an owner, compressed boundary, compatibility-
preserving separation path, and testable behavior or durable artifact.

### Compatibility Handoff as a family

This is the most important negative classification. Compatibility Handoff recurs,
but prior audit evidence says it owns no independent repository truth,
decisions, artifacts, behavior, or invariants. It should remain an architectural
pattern unless future implementation evidence changes that ownership analysis.

## Ownership comparison

| Kind | Owns decisions? | Owns durable artifacts? | Owns runtime behavior? | Owns architectural invariants? | Typical evidence |
| --- | --- | --- | --- | --- | --- |
| Responsibility Family | Yes | Often | Often | Yes | Slice chains, implementation seams, tests, remaining compression. |
| Architectural Pattern | No independent decisions | No independent artifacts | No standalone behavior | Pattern-level owner-preservation invariant | Recurrence across owners without independent truth. |
| Implementation Idiom | Local only | No | Local/substitutable | No | Helper/factoring evidence without architectural ownership. |
| Compatibility Surface | Surface-shape decisions | Yes, surface/report/output shape | Yes, surface construction/rendering | Compatibility and declared boundary invariants | Stable public objects, reports, diagnostic rows, tests. |
| Inquiry | Evidence-sufficiency decisions | Audit/report artifacts; sometimes read-only views | Usually no; sometimes read-only composition | Repository authority, unsupported conclusions, confidence boundaries | Bounded question plus implementation-backed answer. |
| Projection | Evidence replay/cache/explanation decisions | Yes | Yes for runtime projection; no for methodology reports | Event/projection separation, no-added-evidence explanation, slice discipline | Projection stores, shape stages, cache diagnostics, slice reports. |

## Does the repository now support multiple implementation-backed architectural object kinds?

Yes. The repository evidence distinguishes responsibility families,
architectural patterns, implementation idioms, compatibility surfaces, inquiries,
and projections by ownership characteristics rather than by vocabulary.

The strongest proof is that Compatibility Handoff can be classified as an
architectural pattern even though it recurs across multiple family slices. That
classification would be impossible if the repository treated every recurrence as
a candidate responsibility family.

## Can future recovered concepts be classified before being promoted to responsibility families?

Yes, boundedly. A future recovered concept can be tested against ownership
questions before promotion:

1. Does it own independent repository decisions?
2. Does it own durable artifacts or stable output shape?
3. Does it own runtime behavior?
4. Does it own architectural invariants not already owned elsewhere?
5. Is there implementation evidence, not terminology, proving those answers?
6. Are counterexamples merely local idioms, compatibility surfaces, or patterns?

If the answer is mostly no, the concept should not become a responsibility
family. It may be a pattern, a surface, an inquiry, a projection object, an
implementation idiom, or an unsupported hypothesis.

## Does this reduce unnecessary family proliferation?

Yes. The audit supports a promotion boundary:

```text
recurrence
  does not imply
responsibility family
```

A recurring concept should become a responsibility family only when it owns a
stable implementation responsibility with decisions, artifacts, behavior, and
invariants. Otherwise, classifying it as a pattern, compatibility surface,
inquiry, projection, or idiom preserves architecture without inventing new
families.

## Recommended next implementation step

Do not implement a classifier, registry, schema, metadata model, or CLI in
response to this audit.

The next implementation step should be applied only when the repository next
recovers a concrete concept. At that time, perform a small classification gate in
the relevant audit or slice report before any family promotion:

```text
owner
decisions
artifacts
runtime behavior
invariants
evidence
limitations
classification
```

If a future task needs runtime visibility for these classifications, that should
first be recovered as a separate read-only inquiry or compatibility surface with
its own diagnostic inventory and shape-audit obligations. This audit does not
justify adding that runtime surface now.

## Final determination

Seed currently contains multiple architectural object kinds:

- Responsibility Families for bounded recurring ownership chains.
- Architectural Patterns for recurring ownership-preserving shapes.
- Implementation Idioms for local, substitutable implementation conventions.
- Compatibility Surfaces for stable public/report/output shapes.
- Inquiries for bounded read-only repository questions.
- Projections for evidence replay, cached state, shape explanation, and
  compatibility-preserving boundary projection.

The implementation evidence distinguishing them is ownership: who owns decisions,
artifacts, behavior, and invariants. Those distinctions can now be made from
repository evidence rather than architectural intuition, but only boundedly and
case by case.
