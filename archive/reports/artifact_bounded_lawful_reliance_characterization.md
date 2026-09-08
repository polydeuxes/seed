# Artifact Bounded Lawful Reliance Characterization

Repository authority wins.

## Bounded question

```text
According to recurring
repository evidence,

what constitutional movement,
if any,

does an artifact perform
that ordinary language
does not?
```

This characterization answers only that question. It does not define communication, authority, trust, ontology, legal theory, linguistic theory, or a general theory of artifacts.

## Short answer

Recurring repository evidence supports a narrow distinction:

```text
Ordinary language may communicate candidate content.

A repository-supported artifact may establish a bounded lawful reliance surface
for a named downstream consumer.
```

The movement is not that the artifact becomes inherently authoritative. The movement is that preserved evidence, provenance, role, authority boundary, negative authority, unknowns, confidence, and stop conditions become inspectable enough that a downstream consumer may lawfully use the content for a specific repository-supported role.

In shorter form:

```text
An artifact can move communicated or candidate material
into bounded lawful downstream reliance.

Ordinary language alone does not do that in the recurring evidence reviewed.
```

## Recurring repository evidence

### Reliance evidence

`constitutional_reliance_characterization.md` is the strongest prior characterization. It states that Reliance is the constitutional use-status that follows when a bounded downstream consumer may treat preserved content as lawfully usable for a specific role without promoting it beyond evidence, authority boundary, negative authority, unknowns, or confidence limits.

It also distinguishes expression, warrant, and reliance:

```text
Expression carries candidate content.
Constitutional Warrant authorizes bounded lawful reliance.
Constitutional Reliance is the bounded lawful use that warrant permits.
```

This supports the present distinction. Communication or expression can make content available. The artifact matters only when it preserves the warrant profile that makes bounded consumer use lawful.

### Lawful transition evidence

`constitutional_lawful_transition_survey.md` repeatedly refuses naked transfer. Movement across source, constitutional representation, consumer view, diagnostic record, and report boundaries is lawful only when evidence and the competent local boundary authorize the transformation, and when provenance, support, authority scope, confidence, contradiction, and unknown state survive.

The same survey states that diagnostic output, presentation vocabulary, projection, explanation, imported output, agreement, and unknown preservation do not automatically become truth, knowledge, mutation authority, or universal law.

This supports a narrower artifact distinction: the artifact does not turn words into truth. It can make a bounded transition inspectable and consumable where the artifact preserves the required limits.

### Movement versus artifact evidence

`constitutional_movement_vs_artifact_emission_investigation.md` prevents overclaiming. It says performed movement and produced artifact are constitutionally distinct at investigation resolution. A report artifact may preserve a movement result, but the movement is not identical to the report.

That means this characterization cannot say, “artifact equals movement.” The supported answer is weaker and more precise:

```text
The artifact can carry the conditions under which movement becomes lawful
for a downstream consumer.

The artifact is not itself the whole movement,
and artifact production is not automatically authority.
```

### Translation invariant evidence

`constitutional_translation_invariant_investigation.md` and `constitutional_translation_invariant_preservation_characterization.md` recur around a common rule: content may move across form only when warranted content survives and carrier-specific excess does not become promoted truth. Translation can change wording, shape, provider expression, presentation, or record form while preserving the reliance profile.

This supports the artifact distinction because an artifact may carry the preserved invariant across form. Ordinary language may restate content, but repository evidence treats lawful downstream use as depending on preserved warrant, not wording alone.

### Producer → artifact → consumer evidence

Recurring competency-interrogation slices use a producer, private artifact/helper, and consumer pattern. Examples include diagnostic-surface consumption identification, diagnostic-surface field label preparation, and rendered diagnostic-surface line artifacts. These slices repeatedly recover a narrow producer that owns a small responsibility, an artifact that carries a bounded value or identification, and a consumer that may then compose an unchanged public surface.

The constitutional significance is not philosophical. The recurring pattern shows that after an artifact exists, the consumer no longer lawfully reaches through the boundary to re-own producer work. It consumes the bounded artifact in the role the implementation gives it.

### Diagnostic artifact evidence

Diagnostic inventory implementation records each diagnostic surface with explicit fields for JSON support, record support, record scope, event-ledger writes, cluster fact emission, diagnostic fact emission, and mutation. The public AGENTS.md operational contract requires inventory and shape-audit updates for new diagnostic surfaces and requires recordable diagnostics to prove `record_scope=diagnostic_run` unless intentionally different.

This is direct implementation evidence for bounded reliance. A diagnostic artifact can become safe for downstream operational visibility only because its declared artifact shape distinguishes diagnostic facts from cluster facts and read-only diagnostics from mutation.

### Observation, evidence, and fact evidence

The observation ingestion implementation converts an `Observation` into provenance `Evidence`, and only then into a `Fact` unless fact promotion is explicitly suppressed. The artifact sequence matters:

```text
Observation -> Evidence -> optional Fact
```

Ordinary language or raw observation text does not by itself become a fact. The implementation requires bounded artifacts that preserve source type, observed time, subject, predicate, value, metadata, dimensions, expiration, and confidence.

### Input artifact evidence

`InputInspector.inspect_file(...)` hashes file bytes, samples content without executing it, detects a bounded format, preserves warnings, and returns an `InputArtifact`. The artifact establishes bounded inspection metadata: path, size, digest, extension, declared purpose, detected format, confidence, and warnings.

This supports the same pattern. The file's language-like content does not become executable authority or repository truth. The artifact permits bounded downstream reliance on inspection metadata.

## Implementation evidence

Implementation evidence supports three recurring forms of artifact movement.

### 1. Bounded inspection artifact

Producer:

- `InputInspector.inspect_file(...)`

Artifact:

- `InputArtifact`

Consumer:

- downstream code or tests that need file identity, digest, bounded format classification, warnings, and confidence.

What becomes lawful afterward:

- relying on the file inspection metadata as a bounded content-classification result.

What remains unlawful:

- executing file content;
- resolving embedded references;
- treating extension as truth when content disagrees;
- promoting file prose or bytes into repository knowledge merely because a file was inspected.

### 2. Observation/evidence/fact artifact sequence

Producer:

- `ObservationIngestor.ingest_many(...)`, `observation_to_evidence(...)`, and `observation_to_fact(...)`.

Artifacts:

- `Observation`;
- provenance `Evidence`;
- optional `Fact`.

Consumer:

- projected state, fact views, context views, explanation, and other fact/evidence consumers.

What becomes lawful afterward:

- relying on an admitted fact as an observed or inferred fact only when evidence exists and promotion is not suppressed.

What remains unlawful:

- treating every observation as a fact;
- bypassing evidence provenance;
- treating suppressed diagnostic/provider findings as cluster truth;
- erasing confidence, source type, dimensions, metadata, or expiration.

### 3. Diagnostic visibility artifact

Producer:

- diagnostic inventory entries and diagnostic-surface definition helpers.

Artifacts:

- `DiagnosticInventoryEntry`;
- implementation-local diagnostic boundary, consumption, shape-registration, definition, and explanation artifacts.

Consumer:

- `seed --diagnostic-inventory`, `seed --diagnostic-shape-audit`, diagnostic-surface explanation, tests, and operators reading these surfaces.

What becomes lawful afterward:

- relying on declared diagnostic shape and boundary for operational visibility.

What remains unlawful:

- treating a diagnostic row as cluster mutation authority;
- treating diagnostic findings as cluster facts unless declared;
- recording outside the declared record scope;
- adding new operational surfaces invisibly.

## Recovered constitutional movement

The recovered recurring movement is:

```text
artifact-supported bounded lawful reliance
```

More explicitly:

```text
A producer emits or preserves an artifact that carries enough bounded evidence,
provenance, role, authority limit, negative authority, unknowns, confidence,
and stop information for a downstream consumer to use the content lawfully
inside a specific role.
```

This is narrower than “artifacts are authoritative acts.” It is also narrower than “lawful implies bounded.” The artifact supports lawful bounded reliance only when repository implementation or prior characterization evidence shows the required boundary is present.

## Supported distinction

The supported distinction is:

| Ordinary language | Repository-supported artifact |
| --- | --- |
| May communicate candidate content. | May preserve the warrant profile required for bounded reliance. |
| May expose a claim, question, label, or explanation. | May carry evidence/provenance/role/boundary/unknown/confidence/stop conditions. |
| Does not by itself authorize downstream promotion. | Can make a specific downstream use lawful when the artifact is produced by the competent owner and consumed by the competent consumer. |
| Can be presentation, testimony, expression, or candidate material. | Can be a bounded inspection, observation, evidence, fact, diagnostic declaration, projection, report, or characterization artifact with explicit limits. |

## Producer, artifact, consumer, lawful afterward, unlawful afterward

### Recurring producer

The recurring producer is not a single global role. It is a competent local producer: an input inspector, observation ingestor, diagnostic inventory registry/helper, projection builder, investigation writer, characterization writer, or recovery-slice implementation owner.

### Recurring artifact

The recurring artifact is a bounded carrier with implementation-visible or repository-visible shape. Examples include:

- `InputArtifact`;
- `Observation`;
- `Evidence`;
- `Fact`;
- `DiagnosticInventoryEntry`;
- diagnostic-surface boundary/consumption/shape artifacts;
- projection/read-model outputs;
- implementation recovery slices;
- characterization artifacts.

### Recurring consumer

The recurring consumer is the downstream surface that has a defined role: fact consumer, projection consumer, context/explanation consumer, diagnostic audit consumer, report reader, family-completion auditor, or later bounded investigation.

### Exactly what becomes lawful afterward

Only this becomes lawful:

```text
The consumer may use the artifact's preserved content
for the artifact's supported role
within the artifact's preserved boundary.
```

Examples:

- after an `InputArtifact`, downstream use may rely on bounded file metadata and format classification;
- after provenance `Evidence`, fact promotion may become lawful if the implementation permits it;
- after a `Fact`, projections and fact views may consume the fact as projected state input;
- after a diagnostic inventory entry, diagnostic surfaces may be inventoried and shape-audited;
- after a characterization artifact, a later investigation may cite its bounded conclusion as prior repository evidence, not as implementation truth.

### Exactly what remains unlawful

These remain unlawful unless separately supported:

- treating communicated content as truth merely because it was said;
- treating an artifact as globally authoritative;
- treating diagnostic output as cluster truth;
- treating presentation vocabulary as repository knowledge;
- treating projection as verification;
- treating observation as fact when promotion is suppressed or evidence is missing;
- mutating cluster state through read-only diagnostic or audit artifacts;
- exceeding record scope;
- dropping provenance, confidence, unknowns, negative authority, or stop conditions;
- using a characterization artifact as implementation evidence for behavior it did not inspect.

## Unsupported candidates

The following candidate conclusions are not supported by recurring repository evidence:

1. **Artifacts are authoritative acts.** Unsupported. Artifacts can carry bounded authority conditions, but authority remains local, evidence-bound, and consumer-specific.
2. **Language cannot participate constitutionally.** Unsupported. Language can communicate, express, testify, label, ask, explain, or preserve candidate material. The distinction is not exclusion from constitutional participation.
3. **Every artifact establishes lawful reliance.** Unsupported. Repository evidence repeatedly requires competent production, evidence binding, provenance, role, authority boundary, and stop conditions.
4. **Lawful means bounded by default.** Unsupported as a slogan. Boundedness must be preserved by the artifact or surrounding repository evidence.
5. **Diagnostic artifacts may become cluster truth.** Unsupported and usually explicitly refused.
6. **Characterization artifacts are implementation facts.** Unsupported. They can be prior bounded repository evidence, not a substitute for code, tests, or app behavior.

## Preserved unknowns

- Whether “ordinary language” should become canonical repository vocabulary remains unknown.
- Whether “artifact-supported bounded lawful reliance” should become a canonical named constitutional movement remains unknown.
- Whether every artifact family shares one deeper implementation owner remains unknown.
- Whether communication itself has subtypes that can preserve warrant in some cases remains unknown.
- Whether future implementation should add a first-class reliance object remains unknown and is not recommended by this characterization.

## Confidence

High confidence for the narrow distinction: recurring repository evidence supports artifacts as bounded carriers that can make specific downstream reliance lawful where ordinary language alone only communicates or expresses candidate content.

Medium confidence for naming the movement `artifact-supported bounded lawful reliance`; the phrase accurately summarizes the evidence but is not proven as canonical repository vocabulary.

Low confidence for any broader theory of communication, authority, ontology, or artifacts. Those expansions are forbidden here and unsupported by the reviewed implementation evidence.

## Final answer to the bounded question

```text
According to recurring repository evidence,
an artifact performs the constitutional movement
of preserving a bounded warrant profile
so that a specific downstream consumer
may lawfully rely on specific content
for a specific role.

Ordinary language may communicate the content,
but it does not by itself establish
that bounded lawful downstream reliance.
```
