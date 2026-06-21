---
doc_type: investigation
status: exploratory
domain: derivation architecture
related:
  - derivation_frontier.md
  - reasoning_roadmap.md
  - claim_support_characterization.md
  - evidence_trust_and_source_authority_reconciliation.md
  - knowledge_acquisition_and_selection.md
  - repository_observation_characterization.md
  - documentation_observation_characterization.md
  - operator_pressure_as_evidence_observation.md
  - prediction_forecasting_and_future_claims_reconciliation.md
  - reality_fact_and_claim_reconciliation.md
---

# Unified Derivation Architecture Investigation

## Purpose

This document investigates whether Seed is converging on shared derivation
mechanics across operational facts, historical knowledge, documentation evidence,
operator inputs, and future claim-like reasoning.

It is an observation/investigation document only. It does not introduce an
ontology, redefine claims, redefine facts, propose implementation work, propose
runtime changes, prescribe architecture changes, or add a new diagnostic surface.

The central distinction preserved throughout this investigation is:

```text
same mechanics
    ≠
same authority model
```

Repository authority wins over this document. Existing implementation,
reconciliations, and runtime boundaries remain authoritative for their own
scopes.

## Central Observation

Seed repeatedly answers:

```text
Why does Seed believe this?
```

by preserving a derivation chain rather than relying only on an explicit claim
object.

The most visible operational shape is:

```text
observations
    -> facts
    -> relationships
    -> reasoning paths
    -> conclusions
```

Recent operational visibility surfaces make that shape concrete. The
`reasoning_path_audit` implementation describes itself as read-only,
evidence-backed derivation paths for operational conclusions, consumes existing
implemented diagnostic surfaces, and emits evidence, intermediate conclusions,
derived conclusions, consumers, story impact, unknowns, and a read-only boundary.
The operational graph implementation preserves nodes, edges, evidence, and
confidence for implementation-backed operational relationships. The history brief
builds a read-only historical synthesis from impact, snapshot policy, and
repository observation, while preserving unsupported conclusions and historical
confidence limits.

The conclusion can behave like a claim in operator-facing language:

```text
Current Focus: capability
```

but the repository evidence does not require that every such conclusion first be
modeled as a standalone claim object. Some conclusions emerge from derivation
surfaces that retain their supporting path.

## Evidence Reviewed

This investigation reviewed repository materials in these clusters:

- Operational derivation implementations: `reasoning_path_audit`,
  `operational_graph`, `architecture_conformance_audit`, `snapshot_policy_audit`,
  `history_brief`, diagnostic inventory, and diagnostic shape audit entries.
- Knowledge and evidence architecture: top-level architecture, implementation
  status, knowledge acquisition and selection, evidence trust/source authority,
  fact confidence/corroboration, reality/fact/claim reconciliation, and claim
  support characterization.
- Documentation and repository observation materials: documentation observation,
  repository observation, observation surface/blind-spot audit, source/repository
  observation boundaries, and repository observation implementation audits.
- Operator evidence materials: operator pressure, interaction as evidence,
  input-source authority, operator interface/projection authority, and pressure
  visibility documents.
- Future-oriented reasoning materials: derivation frontier, prediction,
  forecasting, future claims, temporal reasoning, learning, knowledge change,
  recommendation, and decision authority documents.

The finding below is bounded by those surfaces. It is not a full repository-wide
lineage claim.

## Emerging Pattern

The repository appears to be converging on a broader traceability pattern:

```text
evidence source
    -> domain-specific derivation
    -> domain-specific authority
    -> traceability
```

This is not the same as a single claim-centric, fact-centric,
documentation-centric, historical, or operational subsystem. It is a repeated
mechanical pattern for preserving how a represented conclusion became available,
while keeping the authority of that conclusion tied to its domain and source.

A more detailed neutral shape is:

```text
source event / source artifact / source statement / source observation
    -> preserved evidence or observation record
    -> normalized or scoped representation
    -> relation, support, confidence, contradiction, or limitation
    -> selected conclusion, explanation, recommendation, or future claim
    -> traceable answer to "why this?"
```

The reusable part is the path discipline. The non-reusable part is the authority
model.

## What Appears Shared Across Domains

Several mechanics recur across operational, documentary, repository, operator,
historical, and future-oriented reasoning.

### 1. Provenance before assertion

Seed preserves source/provenance before treating a conclusion as current
knowledge. The evidence trust reconciliation states the baseline as observation,
evidence, fact, and projection/read view, and warns that evidence support, source
trust, source authority, and truth are distinct. Documentation observation uses
explicit documentation structures and phrases as allowed evidence, while rejecting
broad prose summarization and automatic implementation inference. Repository
observation similarly starts from structural artifact facts, not architectural
meaning.

Shared mechanic:

```text
preserve where the representation came from
before deciding what it can support
```

Authority remains domain-specific: documentation prose can support claims about
what documentation says; repository source can support claims about artifacts;
operator input can support pressure or intent; operational providers can support
observed runtime state.

### 2. Intermediate representations are load-bearing

Seed often does not jump from raw evidence to final conclusion. It preserves
intermediate facts, relationships, conflicts, gaps, confidence tiers, caveats,
and read-model selections.

Operationally, the reasoning path audit explicitly separates evidence,
intermediate conclusions, derived conclusions, consumers, story impact, and
unknowns. The operational graph separates nodes from edges, edge evidence, and
confidence. Knowledge acquisition and selection separates acquisition,
projection, integrity, selection, and response.

Shared mechanic:

```text
raw support
    -> intermediate representation
    -> downstream conclusion
```

Authority remains domain-specific: an intermediate diagnostic finding is not a
cluster mutation; a documentation-derived architectural claim is not proof of
implementation; a future claim is not observation of the future.

### 3. Explanation is downstream of support

Many surfaces answer an operator question by showing support rather than simply
announcing an answer. This is visible in fact support aggregation, why-fact style
explanation, operational graph evidence, reasoning path consumers, history brief
confidence, and documentation observation lineage.

Shared mechanic:

```text
answer
    -> support path
    -> source and boundary
```

Authority remains domain-specific: an explanation can make a conclusion
understandable without upgrading its source into a stronger authority.

### 4. Read-only diagnostics can derive without mutating truth

The recent operational surfaces repeatedly declare read-only boundaries. The
reasoning path audit boundary says it does not record facts, write the event
ledger, or mutate the cluster. The operational graph and related diagnostic
inventory entries are also non-recording, non-mutating surfaces. Snapshot policy
and history brief preserve similar read-only fields.

Shared mechanic:

```text
read-only derivation can create an explanation surface
without creating cluster truth
```

Authority remains domain-specific: diagnostic derivation may explain operational
pressure, but it is not itself operational mutation or durable fact promotion
unless routed through an authorized recording boundary.

### 5. Absence and limitation are part of the derivation

Unknowns, unsupported conclusions, snapshot constraints, confidence tiers,
blind spots, caveats, contradictions, and source limits recur as first-class
parts of explanation.

Shared mechanic:

```text
traceability includes what support is missing or weak
```

Authority remains domain-specific: absence in one observation surface does not
prove absence in reality; it only bounds what that surface can justify.

## What Should Remain Domain-Specific

The repository evidence strongly suggests that shared derivation mechanics should
not collapse authority boundaries.

| Domain | Evidence source | Derivation can support | Authority boundary |
| --- | --- | --- | --- |
| Operational runtime | Provider results, local observations, event ledger, projected facts, diagnostics | Current operational conclusions, capability needs, pressure stories, graph relationships | Must not silently mutate cluster truth; read-only diagnostics remain read-only unless explicitly recorded through the proper boundary. |
| Repository observation | Source files, parsed artifacts, repository structure, git/repository context | Artifact existence, structural relationships, implementation-backed support | Does not by itself decide architectural correctness or runtime behavior. |
| Documentation observation | Explicit docs, frontmatter, headings, lists, diagrams, boundary phrases | What documentation says, architectural claims, reading/navigation relationships | Documentation evidence is not proof that implementation conforms. |
| Operator input | Operator reports, pressure, goals, intent, pain, questions | Manual evidence, frontier pressure, goal relevance, candidate work direction | Operator perspective is high-value evidence, not direct implementation cause or repository truth. |
| Historical reasoning | Preserved events, snapshots, git history, external/primary sources, dated observations | Historical conclusions, change/stability claims, confidence-limited narratives | Historical support depends on source quality and temporal provenance; it is not current operational observation. |
| Future reasoning | Current/historical support, trends, assumptions, scenarios, forecasts | Future claims, consequences, recommendation support | Future claims are not observations of the future and remain revisable. |

The safe unifying statement is:

```text
Domains may share traceable derivation shape while retaining separate rules for
what counts as authoritative support.
```

## Reusable Derivation Primitives Already Visible

Without introducing a new ontology, the repository already uses or describes
several reusable primitives:

- **Source**: the provider, file, operator, artifact, snapshot, event, or other
  origin of a representation.
- **Observation/evidence record**: the preserved source-attributed statement,
  artifact fact, event, or support payload.
- **Normalization/scoping**: the act of making evidence comparable without
  overwriting the raw source record.
- **Fact or represented proposition**: scoped represented knowledge used by
  projections, support, or explanation.
- **Relationship/support edge**: a link explaining why one representation matters
  to another.
- **Confidence/strength/limitation**: support count, confidence tier, caveat,
  contradiction, source limitation, or snapshot constraint.
- **Consumer surface**: the view, diagnostic, explanation, response, audit, or
  recommendation that uses the represented support.
- **Boundary marker**: read-only, records facts, writes event ledger,
  mutates cluster, documentation-only, source-authority, or domain authority
  metadata.

These are primitives in the ordinary descriptive sense only. This document does
not propose a schema or object model for them.

## Where Operational Reasoning Already Demonstrates The Pattern

Operational reasoning is the strongest implemented evidence.

The pattern appears as:

```text
ownership_discrepancies
    -> owner_not_observed / incomplete attribution
    -> capability_needs
    -> pressure_audit
    -> operational_story
    -> reasoning_path explanation
```

`reasoning_path_audit` builds the path from implemented diagnostics instead of
inventing a new truth store. It reads ownership discrepancies, capability needs,
pressure audit, privilege discovery, and operational story; then it renders the
relevant evidence, intermediate conclusions, derived conclusions, consumers,
story impact, unknowns, and read-only boundary.

`operational_graph` demonstrates the related relationship form: operational
nodes and edges are represented with evidence and confidence. The graph can then
support confidence analysis and taxonomy without becoming cluster mutation.

`architecture_conformance_audit` consumes operational graph structure to compare
architecture evidence with observed operational structure. This shows derivation
stacking: one read-only evidence surface can feed another read-only audit while
preserving its boundary.

`history_brief` demonstrates a historical-adjacent operational pattern. It builds
from impact audit, snapshot policy, and repository observation; preserves
changes, stability, repository context, historical confidence, and unsupported
conclusions; and remains non-mutating.

## Where Historical Reasoning Would Fit

Historical reasoning appears structurally compatible with the shared mechanics,
but its authority model must differ from current operational observation.

A historical conclusion such as:

```text
Abraham Lincoln was assassinated.
```

would need a chain more like:

```text
historical conclusion
    -> dated historical facts and claims
    -> source-attributed observations or records
    -> primary sources / archival sources / secondary synthesis
    -> source quality, temporal provenance, and confidence limits
```

This resembles operational traceability because both ask for the support path.
It differs because historical authority depends on source provenance,
corroboration, preservation, dating, and historiographical limits rather than
live provider observation or current projection freshness.

Repository evidence supporting this fit includes:

- the event/change/learning family, which preserves historical existence of
  claims, changes, and revisions rather than erasing earlier support;
- snapshot policy and history brief, which already treat historical confidence
  and unsupported conclusions as first-class;
- prediction/future-claim reconciliation, which distinguishes historical claims,
  current-state claims, future claims, and later outcomes.

The fit is therefore mechanical, not authoritative. Historical sources would not
become operational providers merely because both can feed a traceable derivation
chain.

## Where Documentation Reasoning Would Fit

Documentation reasoning already fits the pattern as a bounded source domain.

Documentation observation asks what the repository says it is meant to be. It can
extract explicit architectural claims and navigation relationships from allowed
documentation structures. It explicitly does not decide what the repository
actually contains, whether code matches documentation, or which source is
ultimately correct.

The documentation path is therefore:

```text
documentation artifact
    -> explicit documentation observation
    -> documentation-grounded fact or claim
    -> support for architecture evidence / navigation / reconciliation
    -> caveated explanation
```

This shares mechanics with operational reasoning because it preserves source,
intermediate representation, support, and caveat. It does not share operational
authority. Documentation can support architecture evidence, but it cannot prove
implementation conformance without repository or runtime evidence.

## Where Operator Evidence Would Fit

Operator input already appears as evidence, pressure, goal, intent, and manual
statement rather than automatic truth.

The operator pressure investigation is the clearest example. The operator report
that `seed --state-build` was too slow was valid pressure evidence. It was not a
complete diagnosis. Instrumentation transformed that pressure into a narrower
implementation-backed understanding: warm cache worked, compact summary
derivation was expensive, and projection replay/build remained the large cold
path cost.

The operator-evidence path is:

```text
operator report / pain / intent
    -> pressure or manual evidence
    -> measured repository or runtime evidence where available
    -> bounded conclusion about problem shape
    -> candidate work direction, not automatic implementation authority
```

This shares derivation mechanics with operational and documentation reasoning:
it preserves source, transforms evidence through intermediate representations,
and can explain why a conclusion became salient. It does not give operator input
unbounded authority over implementation cause, architectural correctness, or
cluster truth.

## Claim-Centric And Fact-Centric Interpretations

The repository has substantial claim-support material. It also has substantial
fact/evidence/projection material. The emerging pattern does not appear to make
either one disappear.

Claim Support asks which facts support which claims; it does not ask which claims
are true. Reality/fact/claim reconciliation preserves the distinction between
reality and representation. Evidence trust/source authority warns that support,
trust, authority, and truth are not interchangeable.

The broader pattern can include claim-like conclusions without requiring every
derived conclusion to originate inside a separate claim system:

```text
fact support can support claims
claim support can support conclusions
operational diagnostics can derive conclusions
documentation observations can support architectural claims
future reasoning can produce future claims
historical evidence can support historical conclusions
```

The shared architecture, if one is emerging, is therefore better described as
traceability-centered derivation than as claim-only or fact-only architecture.
Claims remain important; facts remain important; neither alone explains the full
observed pattern.

## Potential Implications

These implications are observations, not prescriptions.

1. **Traceability may be the common requirement.** The repeated question is less
   "which object type owns truth?" and more "can Seed show the support path and
   authority boundary for this conclusion?"
2. **Authority metadata is as important as support metadata.** A path without a
   domain boundary risks converting documentation prose, operator pressure, or
   diagnostic output into stronger authority than the repository allows.
3. **Historical reasoning can fit without becoming operational reasoning.** The
   same traceability discipline can support historical conclusions if historical
   source authority remains distinct.
4. **Future claim-like reasoning can fit without observing the future.** Future
   claims can be support-preserving and revisable while remaining clearly
   different from facts observed at a later time.
5. **Documentation reasoning can remain useful without becoming implementation
   proof.** Documentation can be evidence for architecture language and intent,
   while repository and runtime observation remain necessary for implementation
   conformance.
6. **Operator evidence can remain first-class without becoming diagnosis.**
   Operator pressure can identify where the system hurts, while instrumentation
   and repository evidence identify what the implementation can justify.

## Open Questions

The repository evidence supports the existence of a shared pattern, but several
questions remain open:

1. What minimum support path is required before a derived conclusion should be
   surfaced to an operator?
2. When should a derived conclusion be represented as an explicit claim, and when
   is a diagnostic explanation sufficient?
3. How should Seed preserve the transformation step between support and result
   without introducing an overbroad derivation ontology?
4. How should historical source quality, primary/secondary source distinction,
   and temporal provenance be represented if historical reasoning becomes a real
   domain?
5. How should operator-provided evidence be weighted when it conflicts with
   measured repository or operational evidence?
6. How should documentation evidence support architecture conformance without
   letting documentation assert implementation reality by itself?
7. When a read-only diagnostic produces a useful conclusion, what distinguishes
   explanation from recordable knowledge?
8. How should future failed predictions revise confidence without erasing the
   original prediction and its original support?

## Conclusion

The repository appears to be converging on shared derivation mechanics:

```text
source
    -> preserved evidence or observation
    -> scoped representation
    -> support / relation / confidence / limitation
    -> traceable conclusion or explanation
```

But it is not converging on shared authority.

The strongest supported characterization is:

```text
Seed is moving toward traceability-centered derivation across domains, while each
domain retains its own authority rules.
```

Operational facts, historical knowledge, documentation evidence, operator inputs,
and future claim-like reasoning can therefore share support-path mechanics
without collapsing into one authority model. That distinction is the key finding
of this investigation.
