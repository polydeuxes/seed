# Observation Operation Boundary Investigation

## Purpose and boundary

This investigation asks what evidence is required before an observation operation can safely apply to observed material.

This is investigation only.

It does not implement new operations, new visibility systems, semantic interpretation, claim extraction, authority inference, ontology promotion, recommendation systems, classification systems, workflow systems, or automation.

Repository authority wins.

## Central finding

Repository evidence supports a prerequisite model for observation operations.

The strongest supported model is:

```text
observed material
    + operation-specific prerequisite evidence
    -> safe operation output
```

Material existence alone is insufficient.

Each operation requires different evidence before it becomes meaningful, supported, and safe.

Repository authority wins.

## Availability, meaningfulness, support, and safety

The investigations repeatedly mix several states that should remain distinct.

### Operation available

An operation is available when the operator or implementation can attempt it.

This does not imply the output is meaningful.

Example:

```text
count terms in text
```

may be available even when tokenization is unstable.

### Operation meaningful

An operation is meaningful when its input units are defined well enough that the output answers a stable question.

Example:

```text
coverage(front-matter-key:status)
```

is meaningful only when the corpus denominator is known.

### Operation supported

An operation is supported when repository evidence supplies the required input records.

Example:

```text
drilldown(section-label:Purpose)
```

is supported only when occurrence records have source locations.

### Operation safe

An operation is safe when it preserves the non-interpretive boundary.

Example:

```text
membership(section-label:Purpose)
```

is safe when it reports exact set inclusion and does not claim relatedness, family, type, recommendation, or shape.

## Operation prerequisites

## 1. Recurrence

### Operation

```text
count repeated observed units
```

### Minimum evidence

```text
observed material units
stable unit boundary
exact key or normalized key
countable occurrence records
```

### Required evidence

```text
what unit is being counted
how duplicate occurrences are handled
whether count is occurrence-based or document-based
corpus boundary or source set
normalization rule, if any
```

### Optional evidence

```text
source location
material type
case-sensitivity rule
bounded examples
per-document counts
```

### Insufficient evidence

```text
material exists but no unit boundary
free-form text with no tokenization rule
labels without normalization rule
counts without corpus boundary
same-looking strings with no exact comparison rule
```

### Material-specific notes

#### Structure

Recurrence is strongly supported for structure when structural units are parsed:

```text
section label
front matter key
heading depth
code fence language
skeleton signature
```

#### Language

Lexical recurrence is plausible only when the lexical unit is exact and bounded:

```text
exact string
exact term
exact phrase
identifier
reference
```

It becomes unsafe when it collapses synonyms, stems, concepts, or meanings.

#### Artifact

Artifact recurrence requires a unit such as:

```text
artifact kind
path pattern
file extension
front matter doc_type
```

Path existence alone is not enough unless the counted unit is path itself.

## 2. Distribution

### Operation

```text
summarize frequency shape over counted observations
```

### Minimum evidence

```text
counted observations
recurrence rows
frequency table
```

### Required evidence

```text
recurrence input
bucket definitions
ranking or sorting rule
thresholds for common/rare/outlier labels
corpus boundary inherited from recurrence
```

### Optional evidence

```text
histogram buckets
long-tail summary
examples per bucket
percentages
trend or drift information if snapshots exist
```

### Insufficient evidence

```text
raw observations without counts
counts from incomparable corpora
thresholds without explanation
common/rare labels without bucket rule
ranked rows that imply importance
```

### Material-specific notes

Distribution depends less on material type and more on count quality.

For structure:

```text
section label frequency distribution
```

is meaningful when labels are counted consistently.

For language:

```text
term frequency distribution
```

is meaningful only if token/phrase boundaries are stable.

## 3. Drilldown

### Operation

```text
locate source occurrences for an observed key or recurrence row
```

### Minimum evidence

```text
exact observed key
occurrence records
source location evidence
```

### Required evidence

```text
document path or artifact identifier
line number, range, span, or equivalent location
material-specific location model
bounded output rule
```

### Optional evidence

```text
heading depth
section parent path
front matter range
code fence range
snippet
occurrence count per source
```

### Insufficient evidence

```text
recurrence row with count but no source records
material unit without location
source path without line/range when operator needs source inspection
unbounded output list
drilldown that ranks or recommends documents
```

### Material-specific notes

#### Structure

Drilldown can use:

```text
document path
line number
heading depth
fence range
front matter range
```

#### Language

Lexical drilldown needs:

```text
document path
line number or text span
exact matched string
```

Snippets are useful but risk interpretation if they become meaning analysis.

#### Artifact

Artifact drilldown may simply be:

```text
path
artifact id
metadata location
```

because the artifact itself is the location.

## 4. Membership

### Operation

```text
return exact set inclusion for an observed key
```

### Minimum evidence

```text
exact observed key
occurrence records
member identity boundary
set boundary
```

### Required evidence

```text
what counts as a member
how repeated occurrences within one member are handled
whether members are documents, artifacts, sections, or files
member deduplication rule
bounded display rule
```

### Optional evidence

```text
occurrence count per member
first occurrence location
member examples
member coverage percentage if denominator exists
```

### Insufficient evidence

```text
no exact key
fuzzy similarity instead of exact inclusion
member identity unclear
duplicate occurrences treated as separate members without rule
membership labels that imply relatedness, family, type, or shape
```

### Material-specific notes

#### Structure

Supported examples:

```text
documents containing section-label:Purpose
documents containing front-matter-key:status
documents with exact skeleton signature S
```

#### Language

Potential examples:

```text
documents containing exact term X
documents containing exact phrase Y
```

Risk is higher because exact lexical membership can be mistaken for concept membership.

#### Artifact

Potential examples:

```text
files with extension .md
artifacts under docs/
artifacts with front matter doc_type key
```

Member boundary must be explicit.

## 5. Coverage

### Operation

```text
measure participation and absence over a defined corpus
```

### Minimum evidence

```text
member set
corpus denominator
absence model
```

### Required evidence

```text
exact observed key
member set
corpus definition
denominator count
missing/absent set or computable complement
percentage calculation rule
boundary statement that absence is not failure
```

### Optional evidence

```text
bounded present examples
bounded missing examples
coverage by subcorpus
confidence caveats
fragmentation indicators
```

### Insufficient evidence

```text
coverage without denominator
membership without absence model
presence count only
corpus boundary unknown
missing set that confuses not-observed with absent
coverage phrased as compliance or correctness
```

### Material-specific notes

#### Structure

Strong cases:

```text
front matter coverage
front matter key coverage
section label coverage
structural completeness coverage
```

#### Language

Potential cases:

```text
exact term coverage across documents
exact phrase coverage across documents
identifier coverage across files
```

Risk is higher because coverage can be misread as conceptual adoption.

#### Artifact

Potential cases:

```text
artifact kind coverage across repository
metadata coverage across documents
```

The denominator must be explicit.

## Operation-specific evidence table

| Operation | Minimum input | Required evidence | Common failure |
| --- | --- | --- | --- |
| recurrence | observed units | unit boundary, key, count rule, corpus/source set | counting without stable unit |
| distribution | counted observations | recurrence rows, bucket/rank rules, thresholds | buckets without count quality |
| drilldown | exact key | source locations, path/span model, bounds | count without location |
| membership | exact key | occurrence records, member identity, dedupe/set rule | fuzzy inclusion or unclear member |
| coverage | member set | denominator, absence/complement model, percentage rule | coverage without corpus boundary |

## Counterexamples

### Coverage without denominator

```text
status appears 135 times
```

This is recurrence or membership evidence.

It is not coverage until the corpus denominator is known.

### Membership without exact key

```text
documents about identity
```

This is semantic grouping, not structural or lexical membership.

Safe membership requires exact observed key.

### Distribution without counts

```text
common-looking headings
```

This is impression, not distribution.

Distribution requires counted observations and bucket/rank rules.

### Drilldown without source location

```text
Purpose appears 277 times
```

This is recurrence.

It is not drilldown until paths, lines, ranges, or equivalent source locations are available.

### Recurrence without stable unit

```text
language repeats
```

This is too weak.

Recurrence requires a defined unit such as exact string, term, phrase, identifier, section label, or front matter key.

### Same operation, different material evidence

Drilldown over structure may need heading depth.

Drilldown over language may need text spans.

Drilldown over artifacts may need only paths.

The operation is reusable, but prerequisites are material-specific.

## Distinguishing observed material, supporting evidence, and output

### Observed material

```text
the thing being observed
```

Examples:

```text
structure
language
artifact
```

### Supporting evidence

```text
records that allow an operation to apply safely
```

Examples:

```text
parsed structural units
exact lexical units
source locations
occurrence records
corpus denominator
```

### Operation output

```text
visibility produced by the operation
```

Examples:

```text
counts
buckets
locations
member sets
coverage percentages
```

A safe operation requires all three to remain distinct.

## Best repository model

The best model is a three-part model:

```text
observed material
    + prerequisite evidence
    + observation operation
    -> bounded visibility output
```

This refines the previous two-axis model:

```text
observed material
    x
observation operation
```

The missing axis was:

```text
operation-specific prerequisite evidence
```

In full:

```text
material
    x
operation
    x
prerequisite evidence
    -> safe visibility
```

Repository authority wins.

## Supported conclusions

1. Material existence alone is insufficient for safe operation application.
2. Each operation has operation-specific evidence requirements.
3. Recurrence requires stable observed units and count rules.
4. Distribution requires counted observations and bucket/rank rules.
5. Drilldown requires source-location evidence.
6. Membership requires exact keys, occurrence records, member identity, and set boundaries.
7. Coverage requires member set, corpus denominator, and absence model.
8. The same operation can apply to multiple materials, but required evidence differs by material.
9. Membership and coverage appear derived because their prerequisites depend on prior operation outputs.
10. The best repository model is material x operation x prerequisite evidence -> bounded visibility output.

## Unsupported conclusions

- Any operation can apply whenever material exists.
- Recurrence is meaningful without unit boundaries.
- Distribution is meaningful without counts.
- Drilldown is meaningful without source locations.
- Membership is meaningful without exact keys or member boundaries.
- Coverage is meaningful without denominator or absence model.
- Lexical operations can infer semantics.
- Structural operations imply correctness.
- Coverage implies compliance.
- Drilldown implies recommendation.

## Recommended next step

The next investigation should be:

```text
operation-material matrix investigation
```

Central question:

```text
Which material/operation pairs are currently supported,
which are plausible,
and which are unsafe?
```

Suggested matrix:

```text
artifact x recurrence
artifact x drilldown
artifact x membership
artifact x coverage

structure x recurrence
structure x distribution
structure x drilldown
structure x membership
structure x coverage

language x recurrence
language x distribution
language x drilldown
language x membership
language x coverage
```

For each pair, evaluate:

```text
observed unit
required evidence
safe output
known risks
unsupported transitions
```

This remains investigation-only and avoids implementation.

## Acceptance answers

### What evidence is required for recurrence?

```text
stable observed unit
exact or normalized key
occurrence records
count rule
corpus/source boundary
```

### What evidence is required for distribution?

```text
counted observations
recurrence rows
bucket/rank rules
thresholds
corpus boundary
```

### What evidence is required for drilldown?

```text
exact observed key
occurrence records
source locations
material-specific location model
bounded output rule
```

### What evidence is required for membership?

```text
exact observed key
occurrence records
member identity boundary
set boundary
deduplication rule
```

### What evidence is required for coverage?

```text
member set
corpus denominator
absence/complement model
percentage rule
explicit non-compliance boundary
```

### When is an operation available?

When it can be attempted technically or conceptually.

### When is an operation meaningful?

When its units, boundaries, and question are stable enough to answer something.

### When is an operation unsupported?

When required prerequisite evidence is missing or the output would require interpretation, authority, recommendation, or classification not supported by the evidence.

### What repository model best explains operation prerequisites?

```text
observed material
    x
observation operation
    x
prerequisite evidence
    -> bounded visibility output
```

Repository authority wins.
