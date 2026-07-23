---
doc_type: observation
status: exploratory
domain: support change and learning language
defines:
  - support change observation
  - support-change evidence
  - learning-language overlap evidence
  - support versus understanding pressure
related:
  - seed.md
  - understanding_claim_and_decompression_observation.md
  - knowledge_and_understanding_distinction_observation.md
  - documentation_compression_observation.md
  - compression_candidate_observation.md
  - explanatory_load_observation.md
  - derivation_frontier.md
  - preservation_failure_observation.md
  - continuity_frontier.md
  - learning_and_knowledge_change_reconciliation.md
  - claim_support_characterization.md
  - claim_support_design.md
  - reality_fact_and_claim_reconciliation.md
  - observation_evidence_change_event_reconciliation.md
---

# Support Change And Learning Observation

## Purpose

This observation investigates how repository evidence describes support changing
and how that evidence relates to repository language about learning.

It is an observation only. It is not a frontier, reconciliation, ontology
proposal, vocabulary proposal, implementation proposal, workflow proposal,
governance proposal, memory-system proposal, learning-system proposal, schema
proposal, or runtime design.

This document does not define `support change` canonically. It does not define
`learning` canonically. It does not assume that support change and learning are
identical. It observes repository evidence and preserves uncertainty where the
evidence is mixed.

## Central question

```text
How does repository evidence describe support changing?
```

A secondary question is narrower:

```text
When repository participants use learning language, what repository evidence
appears closest to that language, and where does it diverge from support-change
language?
```

## Method and authority boundary

The review inspected repository documentation directly, including:

- `docs/seed.md`;
- `docs/archive/original_book_of_seed/13-knowledge-and-evidence.md`;
- `docs/claim_support_characterization.md`;
- `docs/claim_support_design.md`;
- `docs/reality_fact_and_claim_reconciliation.md`;
- `docs/observation_evidence_change_event_reconciliation.md`;
- `docs/learning_and_knowledge_change_reconciliation.md`;
- `docs/understanding_claim_and_decompression_observation.md`;
- `docs/knowledge_and_understanding_distinction_observation.md`;
- `docs/documentation_compression_observation.md`;
- `docs/compression_candidate_observation.md`;
- `docs/explanatory_load_observation.md`;
- `docs/derivation_frontier.md`;
- `docs/preservation_failure_observation.md`;
- `docs/continuity_frontier.md`;
- adjacent contradiction, discovery-path, lineage, knowledge-representation,
  and current-work-position documents where they clarified support movement.

Existing reconciliations remain stronger scoped authority than this observation.
This document does not reconcile their vocabularies. Where it compares `support`,
`understanding`, `knowledge`, `derivation`, `decompression`, and `learning`, it
only records observed pressure and does not promote a new canonical model.

## High-level observation

Repository evidence describes support changing in more than one way.

The strongest recurring pattern is not simply:

```text
new observation arrives -> support increases
```

That pattern exists, but it is incomplete. Repository evidence also describes
support changing when:

- an existing observation is interpreted differently;
- an inference or derivation becomes visible;
- a claim's scope narrows or expands;
- caveats become explicit;
- provenance, authority, source trust, or freshness is reclassified;
- a contradiction is discovered within already preserved material;
- a compressed term decomposes into distinct concerns;
- a support path becomes visible or disappears;
- responsibility for explanation moves from one concept to another;
- a projection selects different represented material for a purpose;
- a conclusion survives while the reason it was usable is lost.

This makes support change broader than evidence arrival but narrower than all
possible knowledge or understanding change. Support change appears to concern
what justifies, qualifies, scopes, challenges, or explains a represented claim or
usable conclusion. Learning language sometimes overlaps that pattern, especially
where the repository says current understanding improves or changes through
preserved support and qualifications. But learning language also reaches beyond
support change into current understanding, historical preservation, selection,
correction, and safe continuation.

## What appears to change when support changes?

### Evidence can change

The clearest support change occurs when additional evidence enters the system.
`docs/archive/original_book_of_seed/13-knowledge-and-evidence.md` describes evidence as immutable raw observation,
facts as projected interpretations of evidence, and fact support aggregation as
multiple evidence-backed facts supporting or conflicting with a value. In that
case the changed support is additional preserved provenance: a new source,
payload, time, fact, or corroborating/conflicting fact joins the support set.

The phone-on-table example in `reality_fact_and_claim_reconciliation.md` shows
the same pattern. Operator testimony supports a represented claim; camera
observation adds support; direct interaction adds still more support. The phone
does not become more real. Represented support changes.

### Interpretation can change

Repository evidence repeatedly separates observation from interpretation. The
same preserved material may later support a different claim, weaker claim,
scoped claim, or caveated claim because interpretation changed. Natural-language
and documentation-observation materials treat language as evidence of a
communicative act, not direct authority for environmental truth. The support
therefore changes when a statement is reinterpreted as testimony, intent,
attribution, candidate meaning, or documentation excerpt rather than as direct
fact.

This is a support change without necessarily adding a new external observation.
The preserved artifact can remain the same while its support role changes.

### Derivation can change

Derivation-related documents describe a movement from preserved support to
additional represented knowledge. The endpoint-identity normalization example in
`docs/archive/original_book_of_seed/13-knowledge-and-evidence.md` is concrete: when a batch contains explicit
identity material such as `ip_address`, `alias`, or `ansible_host`, the
normalizer derives an alias observation that lets endpoint-scoped facts be found
through a stable node name. The support change is not merely another raw fact.
It is a derived support path that connects otherwise separated represented
entities while preserving provenance and avoiding unsupported inference from
naming conventions.

Derivation therefore changes support visibility and reach. A future participant
can ask not only whether a claim exists, but what prior facts and rules made the
claim available.

### Scope can change

Support changes when a claim's scope changes. Claim-centric documents repeatedly
warn that a claim may be observed, historical, current, selected, projected,
future-oriented, imported, inferred, scoped, or authority-limited. A statement
that was too broad can become better supported by becoming narrower. A statement
can also become weaker when its asserted scope exceeds its evidence.

The understanding and compression observations show this pattern frequently. A
participant may have enough support for a conclusion, but not enough support for
a universal formulation, a continuity claim, a learning claim, or a claim that a
compressed term names only one concern.

### Caveats can change

Support changes when caveats become explicit. Evidence-strength and
claim-strength work distinguishes evidence strength from assertion strength.
Knowledge and understanding observations repeatedly describe caveats, authority
limits, freshness, contradiction status, and unknown unknowns as part of what
makes represented knowledge safe to use.

A caveat can weaken a broad claim while strengthening a narrower one. This is a
support change even when the underlying observations are unchanged.

### Support visibility can change

Repository evidence frequently treats invisible support as a problem distinct
from absent support. Preservation-failure and discovery-path documents observe
that conclusions may survive while the path, rationale, critique sequence, or
active pressure that made them understandable is lost. In those cases the claim
may still have historical support somewhere in the repository, but its visible
support for a future participant is weaker.

Support visibility therefore appears as a support-change dimension. A support
path can become more usable when lineage, derivation, discovery path, or
explanation is preserved; it can become less usable when only the conclusion is
preserved.

### Distinctions can change

Documentation compression shows a repeated pattern:

```text
accepted term -> task pressure -> ambiguity or contradiction -> hidden
distinction exposed -> terminology expands -> later understanding changes
```

When a distinction appears, support changes because earlier evidence no longer
supports all of the meanings that were hidden under the compressed term. The
same evidence may support one decompressed concern strongly, another weakly, and
a third not at all.

This is one of the strongest repository examples of support changing without a
new observation. The new item is often a distinction, not a new external source.

### Authority can change

Support changes when authority routing changes. Evidence trust, source
authority, federation, documentation authority, and operator authority materials
all preserve the boundary that source, scope, and authority affect how evidence
supports claims. A foreign Seed correction, operator correction, documentation
excerpt, runtime observation, and LLM interpretation may all be preserved, but
they do not carry the same authority.

A claim may become less supported for one use and more supported for another
when its authority is reclassified. This is not ontology reconciliation; it is an
observed repository pressure around provenance and authority boundaries.

## Critical examples

### Example 1: Fact -> claim

The fact-to-claim shift is the earliest major architectural support-change
example. Earlier fact-centric language could make `fact` carry too much
responsibility: represented reality, claim, state, support, and authority could
blur. Claim-centric architecture decompressed that pressure. `seed.md` now says
Seed begins with observation, is claim-centric, treats facts as normalized claim
forms, and keeps projections from becoming authority.

What support changed?

- The represented object changed from apparent settled fact to supportable
  claim form.
- Evidence became explicit provenance rather than an implicit truth marker.
- Fact support aggregation made corroboration, conflict, confidence, recency,
  and source type inspectable.
- Claim support materials separated evidence supporting facts from facts
  supporting claims.
- Assertion safety improved because claims can be scoped, challenged,
  contradicted, and explained without denying reality.

This is a support change primarily through representation, scope, and authority
boundary. It may include new documents, but the conceptual change is not merely
new evidence. It changes what counts as adequate support for saying something in
Seed.

### Example 2: Observation -> derivation

Observation-to-derivation examples show support becoming usable for claims that
were not directly observed. Endpoint identity normalization is the clearest local
case. An inventory observation and metrics observation do not by themselves make
all endpoint and node facts identical. When explicit alias or address evidence
exists in the same batch, a derived alias observation can bridge them.

What support changed?

- Support became relational rather than only local to one observation.
- The derivation path became part of the support.
- Scope was constrained: no inference from naming conventions, no network calls,
  no external authority, and no entity equivalence overclaim.
- Future facts can be found through the alias-aware support path.

This is a derivation-related support change. It is not learning by assumption,
but it resembles learning language when repository participants describe Seed as
knowing how one represented entity relates to another because preserved support
now permits that relationship.

### Example 3: Persistence -> continuity

Persistence-to-continuity investigations ask whether something merely remains or
whether it remains recognizable through change. Persistence can preserve an
artifact, claim, or wording. Continuity asks what survives across transition:
question, gap, contradiction, finding, frontier, inquiry, relationship, or
working position.

Did support change?

Sometimes yes. If later work preserves a lineage or continuation path, support
for a continuity claim becomes stronger. If only an artifact persists while the
active pressure, discovery path, or reason for use is lost, support for
continuity is weaker even though persistence remains.

Did interpretation change?

Yes. The interpretation changed from `the thing still exists` toward `the thing
remains connected enough across change to be recognized or continued`. That is
not automatically a new ontology. It is an observed distinction that altered what
existing evidence could support.

### Example 4: understanding-claim observation

The understanding-claim observation found that repository uses of
`understanding` often behave claim-like. Understanding can be supported,
challenged, scoped, strengthened, weakened, partially preserved, or made unsafe
by missing caveats and lost paths.

What changed when understanding changed?

- The final conclusion was no longer treated as sufficient.
- Support path, caveats, decompressed distinctions, and active pressure became
  part of what made the conclusion usable.
- Unknown unknowns and hidden compression could weaken prior understanding
  without showing that all prior knowledge was false.
- Understanding appeared to change when support became visible, scoped, or
  decompressed.

This is one of the strongest overlaps between support change and understanding
change. It does not prove that understanding is support change. It shows that
repository participants often notice understanding change when support posture
changes.

### Example 5: explanatory load observation

The explanatory-load observation looked at concepts that appeared to carry too
much responsibility. When pressure exposed that a concept was explaining several
concerns at once, responsibility shifted to more specific concepts or routes.

What changed when responsibility shifted?

- A broad concept stopped serving as support for all uses.
- Some support moved to more precise distinctions.
- Earlier language could remain useful as an umbrella but became less safe as a
  specific explanation.
- The repository gained better routing: future readers can see which document or
  concept owns which kind of answer.

This is support change through responsibility routing. It is also a strong
learning-language neighbor because participants may say the repository `learned`
a distinction. Observationally, what is visible is a changed support and routing
posture, not proof of a canonical learning mechanism.

## Required findings

### Strongest support-change examples

1. **Claim-centric shift.** Fact-centric language gave way to claim-centric
   representation where facts are normalized claim forms, evidence is
   provenance, support is inspectable, and projections do not create authority.
2. **Phone-on-table support growth.** Operator testimony, camera observation,
   and direct interaction add represented support while reality itself does not
   become more real.
3. **Fact support aggregation.** Additional supporting or conflicting facts
   change aggregate confidence, source-type mixture, recency, and current-belief
   selection.
4. **Observation/evidence/change/event distinction.** A repeated observation can
   add support without creating a meaningful change event; a new claim or
   confidence shift can be a change.
5. **Compression decompression.** A hidden distinction can change what existing
   evidence supports without new external observation.

### Strongest understanding-change examples

1. **Understanding as claim-like.** Understanding changes when support, scope,
   caveats, explanation, or discovery path changes.
2. **Knowledge versus understanding distinction.** Knowledge-like preservation
   keeps represented support; understanding-like preservation keeps usable,
   scoped, explainable grasp.
3. **Preservation failure.** A conclusion may remain while its rationale,
   support path, or active orientation is lost, weakening later understanding.
4. **Continuity pressure.** Persistence is insufficient when future participants
   need to recognize what survived across change.
5. **Current work position and active edge.** Facts may survive while the active
   pressure needed to continue safely does not.

### Strongest derivation-related changes

1. **Endpoint identity normalization.** Explicit identity evidence allows a
   derived alias observation while preserving provenance and avoiding unsupported
   equivalence.
2. **Natural-language interpretation.** A communicative act can support a
   candidate meaning or attribution claim without becoming direct evidence for
   environmental truth.
3. **Observation-to-claim formation.** Evidence may justify package, service,
   relationship, identity, or measurement claims, but not every observation
   becomes evidence and not every evidence path supports a claim.
4. **Inferred facts.** Inferred facts carry weaker source type and confidence
   caps, so derivation changes support while retaining limits.
5. **Derivation frontier pressure.** Existing evidence may support additional
   represented knowledge only when the derivation path is visible and bounded.

### Strongest distinction-emergence examples

1. **Fact versus claim.** Facts are not abolished; facts are normalized claim
   forms in representation while reality remains outside the claim layer.
2. **Evidence versus support.** Evidence supports facts; facts support claims in
   claim-support materials.
3. **Observation versus evidence versus change versus event.** Acquisition,
   justification, transition, and preservation answer different questions.
4. **Persistence versus continuity.** Survival of an artifact does not prove
   survival of inquiry, working position, or recognizable pressure.
5. **Knowledge versus understanding.** Represented support and usable grasp
   overlap but do not appear identical.
6. **Decompression versus learning.** Decompression exposes distinctions;
   learning language may describe the resulting changed understanding but should
   not be assumed identical.

### Strongest contradiction-driven changes

1. **Conflicting facts.** Conflicting values for the same subject and predicate
   remain visible rather than being silently averaged away.
2. **Compression pressure.** Ambiguity or contradiction can expose that one term
   was carrying multiple meanings.
3. **Knowledge-change correction.** Later correction can distinguish a prior
   mistaken, stale, or mis-scoped claim from a current selected understanding.
4. **Contradiction discovery without new observation.** Re-running a projection
   or inspecting existing records can expose an already preserved tension.
5. **Claim-strength challenge.** A claim can be contradicted by showing its
   assertion strength exceeds available evidence.

### Strongest cases where support changed without new observation

1. **Hidden distinction exposure.** Existing documentation can support different
   decompressed claims once compression is noticed.
2. **Derivation over preserved facts.** Existing facts can support a derived
   relationship or inferred fact once a bounded derivation path is applied.
3. **Authority reclassification.** A preserved source can shift from local
   evidence to testimony, imported claim, attribution, or documentation evidence.
4. **Contradiction discovery.** Existing claims can become conflict-visible when
   inspected together.
5. **Freshness/staleness characterization.** An unchanged observation can become
   less usable for current-state selection as time and scope change.

### Strongest cases where understanding changed without new observation

1. **Documentation compression.** A term's hidden meanings become visible under
   task pressure, changing what participants understand by the term.
2. **Understanding-claim investigation.** The repository reinterprets
   understanding as claim-like pressure rather than a settled fact-like state.
3. **Knowledge/understanding distinction.** Existing documents show a split
   between represented knowledge and usable grasp.
4. **Preservation failure.** Recognizing that a conclusion survived without its
   discovery path changes how usable the conclusion appears.
5. **Explanatory-load shift.** A concept becomes less explanatory once its
   responsibilities are redistributed.

### Strongest overlap between support change and learning language

Learning language appears closest to support change when documents describe:

- new or reinterpreted support changing what Seed can responsibly understand;
- preserved history plus preserved support plus preserved qualifications leading
  to current understanding for a purpose;
- correction or supersession preserving the old support path while changing the
  current selected interpretation;
- contradiction discovery changing what Seed can explain without erasing prior
  observations;
- decompression making previously hidden distinctions available for safer use.

The overlap is strongest where learning is described as changed represented
understanding with preserved provenance and qualifications.

### Strongest distinctions between support change and learning language

Support-change language appears narrower than learning language in several
places:

- Support change can occur without any claim that the repository learned; for
  example, a second corroborating observation can increase support while the
  selected state remains unchanged.
- Learning language often includes current understanding, selection, correction,
  historical preservation, and safe continuation, not merely support strength.
- Support can become more visible while understanding still fails if active
  pressure, caveats, or continuation orientation are missing.
- Understanding can change through decompression or distinction emergence even
  before support aggregation changes in a formal sense.
- Derivation can change support reach without necessarily being described as
  learning.

## Required tensions

### Claim versus support

A claim is the represented statement under consideration. Support is what makes
that claim available, stronger, weaker, scoped, caveated, challenged, or
explainable. Claim-centric architecture makes claims central, but the pressure
in this observation is that claim centrality does not by itself explain how the
support posture changes.

### Support versus understanding

Support can exist without being usable by a future participant. Understanding
language appears when support must be visible, scoped, decompressed, and
connected to a continuation path. Support change and understanding change
therefore overlap but do not collapse.

### Support versus knowledge

Knowledge-like uses preserve represented supportable material: observations,
evidence, facts, relationships, provenance, confidence, conflicts, and
projections. Support is a justification relation within that represented
material. Knowledge change can include support change, but also selection,
projection, freshness, contradiction status, and answerability.

### Support versus learning

Learning language in the repository is broader than support change. It includes
improvement or extension of represented understanding while preserving history.
Support change may be a mechanism, evidence, or symptom of learning-language
uses, but the repository does not require treating them as identical.

### Derivation versus learning

Derivation changes what existing support can justify or connect. Learning
language may describe the resulting change in represented understanding, but a
derivation is not automatically learning. The important observed boundary is the
visible derivation path and its limits.

### Decompression versus learning

Decompression exposes distinctions hidden by a compressed term. Participants may
experience this as learning, but the repository evidence more directly shows
changed interpretive support: prior evidence is redistributed across newly
visible concerns.

### Contradiction discovery versus learning

Contradiction discovery can change support and understanding without creating a
new observation. It may be learning-like when it changes current understanding,
but contradiction itself is not correction, resolution, or learning.

### Represented change versus understanding change

A represented change can occur without understanding improving: a fact, event,
or projection may change while explanation remains poor. Conversely,
understanding can change when existing represented material is decompressed,
rerouted, caveated, or made visible. The repository repeatedly treats final
state and usable grasp as different preservation concerns.

## Learning-related observations

When repository participants describe `learning`, the closest evidence appears
to be:

1. **Support change.** New, reinterpreted, contradicted, or better-scoped support
   changes what can be responsibly represented.
2. **Understanding change.** Participants describe a changed ability to explain,
   use, continue from, or safely scope a conclusion.
3. **Derivation.** Existing represented material supports additional represented
   material through bounded, inspectable paths.
4. **Decompression.** Hidden distinctions appear, changing how existing terms
   can be used.
5. **Contradiction discovery.** Existing claims become newly tensioned or
   visibly incompatible.
6. **Responsibility routing.** Explanatory burden moves to more precise concepts
   or documents.
7. **Correction and selection.** Later support changes the selected current
   interpretation while preserving prior claims and support.

The evidence diverges from learning language where learning would imply a
canonical process, a new architecture, a memory system, or an implementation
mechanism. This observation finds pressure signals, not a learning ontology.

## Unresolved observations

1. **Support visibility versus support existence remains under-specified.** The
   repository often cares that support is visible to future participants, but it
   does not appear to have one canonical way to distinguish invisible support
   from absent support.
2. **Understanding change can outpace represented support change.** A reader can
   understand a distinction after reading existing documents even if no formal
   support aggregate changes.
3. **Learning language is useful but high-risk.** It captures cross-layer change
   in represented understanding, but it can over-suggest a system, process, or
   ontology that this observation does not find authority to define.
4. **Derivation and decompression are adjacent but distinct.** Both can produce
   changed understanding without new external observation, but derivation is
   support-path generation while decompression is distinction exposure.
5. **Contradiction can change support without resolving anything.** Discovery of
   conflict changes what can be responsibly asserted, but does not decide which
   claim wins.
6. **Continuity claims need more than persistence evidence.** The repository has
   strong evidence that persistence is insufficient, but continuity forms remain
   exploratory.
7. **Responsibility routing changes support expectations.** When explanatory
   load moves, future support standards change, but repository evidence does not
   make that a formal support-change type.

## Closing observation

Claim-centric architecture explains how represented knowledge is justified by
making claims, evidence, facts, support, projection, and authority inspectable.
The pressure preserved here is narrower and later:

```text
Once a claim is represented, repository evidence still needs to explain how its
support posture changes.
```

The repository's strongest answer is observational rather than canonical.
Support changes through evidence arrival, interpretation, derivation, scope,
caveats, visibility, distinction emergence, contradiction discovery, authority
routing, and explanatory responsibility shifts. Learning language overlaps this
when participants describe changed represented understanding, especially when
history and support are preserved. But the evidence does not require support
change and learning to be identical, and this document does not make them so.
