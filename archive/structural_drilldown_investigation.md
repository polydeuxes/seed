# Structural Drilldown Investigation

## Purpose and boundary

This investigation asks whether source-location visibility can safely extend structural recurrence visibility.

This is investigation only.

It does not implement prose interpretation, claim extraction, authority inference, shape inference, ontology promotion, NLP, LLM analysis, recommendation systems, workflow systems, or automation.

Repository authority wins.

## Current context

Recent documentation structure work established:

```text
Phase 1
    structure visibility

Phase 2
    recurrence visibility

Phase 3
    recurrence framing
```

Current documentation structure capabilities include:

```text
document structure visibility
recurrence visibility
histogram buckets
rare/common structures
missing common structures
structural outliers
section skeleton signatures
```

The next safe question identified by prior work is:

```text
Where does this structure occur?
```

not:

```text
What does this structure mean?
```

## Central finding

Structural drilldown is a safe extension of recurrence visibility when it is limited to:

```text
one observed structural category
one exact structural key
bounded source locations
no semantic expansion
```

The safest first slice is:

```text
section label
    -> matching document paths
    -> optional line number and heading depth
```

This remains structural because it answers:

```text
where did this observed recurrence row come from?
```

without answering:

```text
what does this recurrence mean?
```

## Recurrence visibility versus structural drilldown

### Recurrence visibility

Recurrence visibility answers:

```text
what recurs?
how often does it recur?
how is recurrence distributed?
which rows are common, rare, missing, or outlying?
```

Examples:

```text
Purpose: 277
status: 135
skeleton S: 10 docs
text: 7890
1 occurrence section-label bucket: 7976
```

This is useful but abstract.

### Structural drilldown

Structural drilldown answers:

```text
where does this already observed structure occur?
which exact documents produced this recurrence row?
which exact source locations produced this count?
```

Examples:

```text
section label Purpose
    -> docs/a.md:12 depth=2
    -> docs/b.md:9 depth=2

front matter key status
    -> docs/a.md
    -> docs/c.md

skeleton signature S
    -> docs/x.md
    -> docs/y.md
```

The distinction is:

```text
recurrence visibility
    -> item + count + distribution

structural drilldown
    -> item + count + bounded source locations
```

## Structural drilldown versus navigation

Navigation is broader.

It may include:

```text
where to inspect
how to move through documents
what examples to open
```

Structural drilldown is narrower.

It should mean only:

```text
source-location expansion for an already observed structural row
```

Therefore:

```text
all structural drilldown is navigation-like
but not all navigation is structural drilldown
```

Drilldown should not choose what an operator should inspect next.

It should only expose where the structural evidence exists.

## Drilldown forms that remain structural

### Document paths

Safe:

```text
section label Purpose -> docs/foo.md
```

Reason:

```text
path is source location
```

### Line numbers

Safe:

```text
docs/foo.md:37
```

Reason:

```text
line number is source location
```

### Heading depth

Safe:

```text
heading depth=2
```

Reason:

```text
heading depth is parsed structure
```

### Front matter key locations

Safe:

```text
front matter key status -> docs/foo.md
```

Reason:

```text
key presence is structure
```

### Code fence locations

Safe:

```text
code fence language python -> docs/foo.md:81-96
```

Reason:

```text
fence language and line range are parsed structure
```

### Exact skeleton membership

Safe:

```text
skeleton signature S -> docs/a.md, docs/b.md
```

Reason:

```text
membership is exact structural equality
```

### Occurrence count

Safe:

```text
occurrences in document: 3
```

Reason:

```text
count is structural frequency
```

### Bounded examples

Safe:

```text
show first 10 matching documents
```

Reason:

```text
bounded examples improve inspectability without ranking importance
```

## Drilldown forms that become interpretation

### Related documents

Unsafe because:

```text
related implies relationship beyond shared structure
```

### Similar documents

Unsafe unless exact structural equality is used.

Similarity scoring introduces distance, weighting, and interpretation.

### Recommended documents

Unsafe because recommendation introduces selection pressure and workflow guidance.

### Important documents

Unsafe because importance is not structurally observable from recurrence alone.

### Document families

Unsafe when family means semantic type or conceptual grouping.

Safe only if named mechanically as:

```text
exact skeleton membership
```

### Document intent

Unsafe because intent requires interpretation.

## Smallest useful drilldown slice

Candidate slices reviewed:

```text
section label -> matching document paths
front matter key -> matching document paths
skeleton signature -> matching document paths
```

### Section label drilldown

Best first slice:

```text
section label
    -> bounded matching document paths
    -> optional line number
    -> optional heading depth
```

Why strongest:

```text
section labels are already visible
section labels are recurrence-heavy
section labels include both high-frequency and rare rows
line/depth evidence is already structural
```

### Front matter key drilldown

Second-best slice:

```text
front matter key
    -> bounded matching document paths
```

Why useful:

```text
supports metadata coverage review
exact key presence is structural
```

Limitation:

```text
key presence alone should not imply lifecycle, authority, or completeness
```

### Skeleton signature drilldown

Third slice:

```text
skeleton signature
    -> exact member documents
```

Why useful:

```text
turns skeleton recurrence counts into inspectable membership
```

Risk:

```text
operator may read exact skeleton membership as document type or family
```

Safe naming must avoid semantic family language.

## Does drilldown improve visibility or reproduce grep?

Mixed answer.

### Drilldown improves visibility when

```text
it starts from a parsed structural recurrence row
it returns source locations for that exact row
it includes line/depth/fence/key evidence
it is bounded
it preserves the non-interpretive boundary
```

This is more than grep because the keys are already normalized structural observations:

```text
heading labels
heading depth
front matter keys
fence language
skeleton signatures
outlier signals
```

A raw grep does not reliably provide:

```text
heading hierarchy
front matter key scope
exact skeleton membership
code fence closure
link classification
structural outlier membership
```

### Drilldown reproduces grep when

```text
it only lists every textual match for a label
it ignores heading/front-matter/fence scope
it returns unbounded path lists
it lacks line/depth/source evidence
```

Example:

```text
Purpose -> 277 paths
```

without line/depth/bounds may be only marginally better than grep.

## Information that should appear in drilldown output

Minimum useful output:

```text
category
key
corpus count
shown count
limit
matching document paths
boundary statement
```

For section labels:

```text
document path
line number
heading depth
occurrence count in document
```

For front matter keys:

```text
document path
front matter key
front matter line range if available
```

For code fences:

```text
document path
start line
end line
language
closed/unclosed status
```

For skeleton signatures:

```text
signature id or literal signature
matching document path
section count
max depth
```

For outlier signals:

```text
signal name
document path
metric value
threshold if explicit
```

## Counterexamples

### Drilldown provides little value

Very common generic rows:

```text
Purpose: 277
text: 7890
heading depth 2: many occurrences
```

An exhaustive list is noisy.

Bounded examples help, but may still not answer an operator question unless scoped.

### Drilldown adds little over existing document filter

If a document-specific view already shows all sections, drilling into a one-document row may duplicate existing `--document` or `--sections` visibility.

### Drilldown creates interpretation pressure

Risky transitions:

```text
section label match
    -> documents about that topic

same skeleton
    -> same document type

rare structure
    -> cleanup needed

outlier signal
    -> important document

matching front matter key
    -> same authority state
```

These must remain unsupported.

### Bounded examples can be mistaken for recommendations

A bounded list is not a ranked list.

The output should not imply:

```text
these are the best documents
these are the most important documents
these should be inspected first
```

## Important distinctions

### Visibility

```text
what exists or recurs
```

### Drilldown

```text
where the already visible structure occurs
```

### Navigation

```text
how an operator can move to source locations
```

Navigation is broader than drilldown.

### Exploration

```text
operator-driven inspection of visible structures
```

The system can support exploration by exposing locations, but should not decide meaning.

### Recommendation

```text
system-guided selection of what to inspect
```

Out of bounds.

### Similarity

```text
distance or likeness between documents
```

Out of bounds unless exact structural equality is explicitly used.

### Interpretation

```text
meaning assigned to structure
```

Out of bounds.

## Relationship to prior work

The Phase 3 investigation concluded:

```text
Phase 3 should continue structural visibility
and stop before shape pressure
```

The recurrence navigation investigation concluded:

```text
visibility = item + count + bucket + structural signal
navigation = item + bounded document locations/examples for source inspection
```

This investigation narrows navigation into drilldown:

```text
structural drilldown = exact recurrence row + bounded source locations
```

## Supported conclusions

1. Structural drilldown is a safe extension of recurrence visibility when bounded to exact structural keys and source locations.
2. Drilldown differs from recurrence visibility by answering `where`, not `what` or `how many`.
3. Drilldown differs from navigation by being narrower: it expands one recurrence row into source-location evidence.
4. The smallest useful slice is `section label -> bounded matching document paths`, optionally with line number and heading depth.
5. Front matter key drilldown is the next safest slice.
6. Skeleton signature drilldown is useful but needs careful naming to avoid semantic family pressure.
7. Drilldown improves visibility when it uses parsed structure and bounded locations.
8. Drilldown becomes grep-like when it emits unbounded textual matches without structural scope.
9. Drilldown becomes interpretation when it claims relatedness, similarity, recommendation, importance, family, type, intent, or meaning.

## Unsupported conclusions

- Drilldown proves document meaning.
- Drilldown proves documents are related.
- Drilldown recommends documents.
- Drilldown identifies important documents.
- Skeleton membership means document family.
- Same section label means same content.
- Rare structures are defects.
- Outlier signals are cleanup priorities.
- Bounded examples are ranked recommendations.

## Recommended next step

Investigate or implement only the smallest structural drilldown slice:

```text
section label
    -> bounded matching document paths
    -> line number
    -> heading depth
    -> occurrence count
```

Suggested command shape, if implemented later:

```bash
seed --documentation-structure --recurrence --drilldown section-label:Purpose --limit 25
```

Alternative safer wording:

```bash
seed --documentation-structure --recurrence --where section-label:Purpose --limit 25
```

The `--where` wording may be safer because it directly states the boundary:

```text
where does this observed structure occur?
```

not:

```text
what does it mean?
```

Next slices after section labels:

```text
front matter key -> bounded matching document paths
code fence language -> bounded line ranges
skeleton signature -> exact member documents
outlier signal -> matching documents with metric values
```

## Acceptance answers

### What is structural drilldown?

Structural drilldown is a read-only source-location expansion for an already observed structural recurrence row.

It answers:

```text
where did this structural count come from?
```

### How is it different from recurrence visibility?

Recurrence visibility answers:

```text
what recurs and how often?
```

Structural drilldown answers:

```text
where does that observed recurrence occur?
```

### How is it different from navigation?

Navigation is broader movement through source material.

Structural drilldown is narrower: one exact structural key expanded into bounded source locations.

### What is the smallest useful drilldown slice?

```text
section label
    -> bounded matching document paths
```

with optional:

```text
line number
heading depth
occurrence count
```

### What information can be exposed while remaining structural?

```text
document path
line number
heading depth
front matter key presence
code fence line range
code fence language
skeleton membership
occurrence count
bounded examples
```

### Where does drilldown become interpretation?

It becomes interpretation when it claims:

```text
related documents
similar documents
recommended documents
important documents
document families
document intent
semantic meaning
shape authority
```

Repository authority wins.
