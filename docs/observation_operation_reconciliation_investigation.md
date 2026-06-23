# Observation Operation Reconciliation Investigation

## Purpose and boundary

This investigation asks whether recurrence, distribution, drilldown, membership, and coverage are better understood as reusable observation operations rather than visibility layers.

This is investigation only.

It does not implement new visibility systems, new operational surfaces, semantic interpretation, claim extraction, authority inference, ontology promotion, recommendation systems, classification systems, shape inference, workflow systems, or automation.

Repository authority wins.

## Central finding

Repository evidence supports a clearer type distinction:

```text
observable material
    -> what kind of repository material is being observed

observation operation
    -> what visibility operation is applied to that material
```

The strongest supported model is:

```text
observable material
    = artifact | language | structure | event | measurement | relationship evidence | other directly observed material

observation operation
    = recurrence | distribution | drilldown | membership | coverage
```

The prior visibility-layer stack remains useful as an operator-facing progression, but it mixed two categories:

```text
material layers
```

and:

```text
operations over material
```

Repository authority wins.

## Visibility layer versus observation operation

### Visibility layer

A visibility layer answers:

```text
what kind of thing can be directly observed?
```

Examples:

```text
artifact visibility
language visibility
structure visibility
```

These identify observed material or an observation family.

### Observation operation

An observation operation answers:

```text
what can be done over observed material while remaining observational?
```

Examples:

```text
count recurring values
summarize distributions
locate occurrences
list members
measure coverage
```

These do not define new material.

They transform existing observations into a different visibility view.

## Candidate observable materials

### Artifact

Examples:

```text
document
file
repository artifact
language-bearing artifact
```

Primary question:

```text
what exists?
```

### Language

Examples:

```text
words
terms
phrases
identifiers
references
operator utterances
document prose
```

Primary question:

```text
what language exists?
```

### Structure

Examples:

```text
yaml front matter
heading hierarchy
section label
front matter key
code fence language
link target class
section skeleton
```

Primary question:

```text
what structure exists?
```

### Meaning

Meaning is not currently in the safe visibility stack.

It requires interpretation.

Therefore:

```text
meaning
```

is not a safe input for these operations under the current investigation boundary.

## Candidate observation operations

### Recurrence

Input:

```text
observed material units
```

Examples:

```text
section labels
front matter keys
exact terms
identifiers
references
```

Operation:

```text
count repeated exact observed units
```

Output:

```text
unit -> occurrence count
unit -> document count
```

Examples:

```text
section-label:Purpose -> 277
front-matter-key:status -> 135
term:"Repository authority wins" -> N
identifier:RepositoryArtifactFact -> M
```

Status:

```text
strong operation candidate
already demonstrated for structure
plausible for language
```

### Distribution

Input:

```text
recurrence rows or counted observations
```

Operation:

```text
bucket, rank, or summarize frequency shape
```

Output:

```text
common rows
rare rows
singleton counts
long-tail buckets
outlier counts
```

Examples:

```text
section labels appearing once: N
terms appearing 10+ times: M
common front matter keys
rare code fence languages
```

Status:

```text
strong operation candidate
```

### Drilldown

Input:

```text
one recurrence row or exact observed key
```

Operation:

```text
locate source occurrences
```

Output:

```text
document path
line number
heading depth
fence range
source span
bounded examples
```

Examples:

```text
section-label:Purpose -> docs/a.md:12 depth=2
term:"identity" -> docs/x.md:44
identifier:RepositoryArtifactFact -> seed_runtime/y.py:10
```

Status:

```text
strong operation candidate
safe while source-location only
```

### Membership

Input:

```text
one recurrence row or exact observed key
```

Operation:

```text
return the set of documents or artifacts that contain the key
```

Output:

```text
member documents
member artifacts
member count
bounded member examples
```

Examples:

```text
members(section-label:Purpose) -> documents containing Purpose
members(front-matter-key:status) -> documents containing status
members(term:"identity") -> documents containing exact term identity
```

Status:

```text
derived operation candidate
```

### Coverage

Input:

```text
membership set + defined corpus denominator
```

Operation:

```text
measure participation and absence over corpus
```

Output:

```text
present count
missing count
percentage
coverage denominator
```

Examples:

```text
coverage(front-matter-key:status) = 135 / 442
coverage(section-label:Purpose) = 277 / 442
coverage(term:"identity") = X / 442
```

Status:

```text
derived operation candidate
```

## Do the candidates behave like layers or operations?

### Recurrence

Previously treated as:

```text
recurrence visibility layer
```

Better current reading:

```text
recurrence operation over observable units
```

Reason:

The same operation appears applicable to structure and language.

### Distribution

Better current reading:

```text
distribution operation over recurrence rows
```

Reason:

Distribution requires counted inputs and summarizes frequency shape.

It is not a new observed material.

### Drilldown

Better current reading:

```text
locate operation over exact observed keys
```

Reason:

Drilldown adds source locations, not new material.

### Membership

Better current reading:

```text
set-membership operation over exact observed keys
```

Reason:

Membership is derivable from occurrence records.

It answers set inclusion.

### Coverage

Better current reading:

```text
coverage operation over membership set and corpus denominator
```

Reason:

Coverage is explicitly derived from membership plus denominator plus absence.

## Can the same operation apply to multiple observed materials?

Repository evidence supports this for at least recurrence and plausibly for the others.

### Structure -> operations

```text
structure
    -> recurrence
    -> distribution
    -> drilldown
    -> membership
    -> coverage
```

Already supported by documentation structure investigations.

### Language -> operations

```text
language
    -> lexical recurrence
    -> lexical distribution
    -> lexical drilldown
    -> lexical membership
    -> lexical coverage
```

Plausible and supported as investigation direction by lexical recurrence visibility, with boundaries preserved.

### Artifact -> operations

```text
artifact
    -> recurrence by artifact type or path pattern
    -> distribution by artifact kind
    -> drilldown to artifact paths
    -> membership in artifact sets
    -> coverage over corpus
```

Plausible, but less developed in the reviewed branch.

## Why membership and coverage appear derived

Membership appears derived because it requires:

```text
observed key
    + occurrence records
    -> member set
```

Coverage appears derived because it requires:

```text
member set
    + corpus denominator
    + absence set
    -> coverage
```

Neither introduces a new material class.

Both are operations over already observed material.

This explains why recent investigations found membership and coverage useful but not primitive.

## Counterexamples

### Recurrence as standalone visibility layer

The prior visibility reconciliation treated recurrence as a layer because it appears to add a new operator-facing question:

```text
what recurs?
```

This remains valid from the interface perspective.

However from the repository model perspective, recurrence depends on observed units.

Therefore recurrence can be both:

```text
operator-facing visibility layer
```

and:

```text
underlying observation operation
```

The operation model is more general.

### Structural operations may not transfer cleanly to language

Language has tokenization, casing, punctuation, stemming, phrase boundaries, and synonym pressure.

These make lexical operations noisier than structural operations.

Therefore reuse is plausible only for exact lexical units, not semantic units.

### Drilldown may require different location models

Structural drilldown can use heading lines, depths, and fence ranges.

Lexical drilldown would use text spans, line numbers, or occurrence snippets.

The operation generalizes, but the output fields differ by material.

### Coverage denominator can vary by material

Structural coverage may use document corpus.

Lexical coverage may use documents, sections, or artifacts.

Artifact coverage may use files or repository paths.

A reusable operation still requires explicit denominator.

### No formal operation model exists today

Repository evidence supports an explanatory model.

It does not prove an implemented operation abstraction.

## Important distinctions

### Artifact

Observed repository object.

### Language

Observed words or language-bearing material.

### Structure

Observed organization or deterministic form.

### Meaning

Interpretation result.

Out of scope.

### Recurrence

Operation that counts repeated observed units.

### Distribution

Operation that summarizes recurrence shape.

### Drilldown

Operation that locates observed units or recurrence rows.

### Membership

Operation that returns exact set inclusion.

### Coverage

Operation that measures participation across a defined corpus.

## Best repository model

The best current model is a two-axis model:

```text
Axis 1: observed material
    artifact
    language
    structure
    event
    measurement
    relationship evidence

Axis 2: observation operation
    recurrence
    distribution
    drilldown
    membership
    coverage
```

Example matrix:

```text
structure + recurrence
    -> section labels recur

structure + coverage
    -> front matter key coverage

language + recurrence
    -> terms recur

language + drilldown
    -> phrase source locations

artifact + membership
    -> artifact set members
```

This model explains the evidence better than a single linear visibility stack.

The linear stack remains useful as a story of discovery.

The two-axis model better explains reuse.

## Supported conclusions

1. Repository evidence supports distinguishing observed material from observation operations.
2. Artifact, language, and structure behave more like observed materials than operations.
3. Recurrence, distribution, drilldown, membership, and coverage behave more like operations than observed materials.
4. Recurrence and distribution are already strongly demonstrated as structural operations.
5. Lexical recurrence suggests the same operation can apply to language under exact-string boundaries.
6. Drilldown, membership, and coverage appear reusable across materials if each material provides exact observed units and source/corpus boundaries.
7. Membership and coverage appear derived because they are operations over occurrence records and corpus denominators.
8. The prior visibility-layer stack is still useful operator-facing language, but the operation model better explains cross-domain recurrence.

## Unsupported conclusions

- A formal observation-operation abstraction is implemented today.
- All operations apply equally well to all materials.
- Lexical recurrence can safely infer semantic recurrence.
- Coverage is always meaningful regardless of denominator.
- Membership implies relatedness.
- Drilldown implies recommendation.
- Distribution implies importance.
- Recurrence implies authority.
- Meaning is safe observed material under current boundaries.

## Recommended next step

The next investigation should be:

```text
observation operation boundary investigation
```

Central question:

```text
What evidence is required before an operation can safely apply to a material type?
```

It should review each operation against each material:

```text
artifact
language
structure
```

and ask:

```text
what is the observed unit?
what is the corpus denominator?
what is the source-location model?
what are the noise risks?
what boundary prevents interpretation?
```

This remains investigation-only and avoids implementation.

## Acceptance answers

### What is a visibility layer?

A visibility layer identifies a class of repository material or observation family that can be seen without unsupported interpretation.

Examples:

```text
artifact visibility
language visibility
structure visibility
```

### What is an observation operation?

An observation operation is a reusable read-only transformation over observed material that produces additional visibility.

Examples:

```text
recurrence
distribution
drilldown
membership
coverage
```

### Are recurrence, distribution, drilldown, membership, and coverage operations?

Repository evidence currently supports yes, with the caveat that prior reports also used them as operator-facing visibility layer names.

### What inputs do they operate on?

They operate on exact observed units such as:

```text
section labels
front matter keys
skeleton signatures
terms
phrases
identifiers
references
artifact paths
```

plus source-location records or corpus denominators where needed.

### Can they be reused across multiple visibility domains?

Partially yes.

They are strongly demonstrated for structure and plausibly reusable for exact lexical language observations.

### Why do membership and coverage appear derived?

Because:

```text
membership
    = observed key + occurrence records -> member set

coverage
    = member set + corpus denominator -> participation/absence ratio
```

### What repository model best explains the evidence?

A two-axis model:

```text
observed material
    x
observation operation
```

This better explains why the same sequence appears under both structure and language while preserving the existing non-semantic boundaries.

Repository authority wins.
