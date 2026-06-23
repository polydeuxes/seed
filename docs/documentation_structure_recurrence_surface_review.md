# Documentation Structure Recurrence Surface Review

## Purpose and boundary

This investigation reviews the newly implemented documentation structure and recurrence surfaces.

Repository authority wins.

This report is investigation-only.

It does not implement prose interpretation, meaning extraction, claim extraction, authority inference, shape inference, ontology promotion, recurrence detection changes, workflow systems, or automation.

## Execution note

The requested command set was reviewed against the implemented CLI and documentation structure implementation.

Direct command execution was not available in this session because no repository checkout was present in the execution sandbox and raw `git clone` to GitHub failed due name-resolution failure.

Therefore this report does not claim fresh local command output for every requested invocation.

It uses:

```text
repository implementation evidence

provided observed command output examples

surface behavior visible from the CLI and formatter code
```

Repository authority wins.

The strongest concrete recurrence counts available for this review are the operator-provided output examples:

```text
Purpose: 276
Non-Goals: 106
Conclusion: 86
Central Finding: 63
status: 135
domain: 93
doc_type: 90
```

## Surfaces reviewed

Requested surfaces:

```bash
seed --documentation-structure
seed --documentation-structure --summary-only
seed --documentation-structure --recurrence
seed --documentation-structure --recurrence --top 25
seed --documentation-structure --missing-front-matter
seed --documentation-structure --sections
seed --documentation-structure --links
seed --documentation-structure --code-fences
```

Additional relevant combinations identified from implementation:

```bash
seed --documentation-structure --document docs/example.md
seed --documentation-structure --missing-trailing-newline
seed --documentation-structure --empty-sections
seed --documentation-structure --recurrence --min-count N
seed --documentation-structure --json
```

## Implementation-backed boundary

The documentation structure observer declares itself as:

```text
read only
observes document structure only
no prose interpretation
no claim extraction
no authority inference
no shape inference
no event ledger writes
no repository mutation
```

The recurrence mode similarly declares:

```text
read only
observes structural recurrence only
no prose interpretation
no claim extraction
no authority inference
no shape inference
no ontology promotion
no event ledger writes
no repository mutation
```

This boundary is important.

The surface is explicitly structure visibility, not prose interpretation.

## What the observer actually made visible

The implementation exposes per-document structural records including:

```text
path
line_count
byte_count
blank_line_count
nonblank_line_count
empty_document
trailing newline presence
front matter presence
front matter keys
H1 heading presence
title heading
heading outline
section inventory
section count
section depth
empty section count
link observations
code fence observations
structure status
```

The summary exposes corpus-level structure counts including:

```text
total documents
matching documents
output documents
total lines
total bytes
blank lines
nonblank lines
empty documents
documents without trailing newline
with YAML front matter
missing YAML front matter
with H1 heading
missing H1 heading
internal docs links
external links
broken local docs links
fenced code blocks
unclosed fenced code blocks
fenced code block languages
sections
maximum section depth
empty sections
```

The recurrence report exposes corpus-level recurrence over:

```text
section labels
front matter keys
heading depths
code fence languages
link target classes
```

This is real visibility.

It is not merely a file listing.

## Surface-by-surface evaluation

### `seed --documentation-structure`

Provides:

```text
corpus summary
incomplete document list
default structural status
boundary statement
```

Operator questions it can answer:

```text
How many docs are structurally complete?
How many docs lack front matter?
How many docs lack H1 headings?
Are there broken local docs links?
Are there unclosed code fences?
```

Visibility still missing:

```text
which missing element is most common by document family
which documents are structural outliers
which structure patterns recur together
```

Assessment:

```text
useful as a top-level health surface
```

### `seed --documentation-structure --summary-only`

Provides:

```text
summary without document rows
boundary without noisy detail
```

Operator questions it can answer:

```text
What is the current documentation structure health at a glance?
Is there structural debt without scrolling through every file?
```

Visibility still missing:

```text
examples for each summary count
```

Assessment:

```text
useful for quick checks
```

### `seed --documentation-structure --recurrence`

Provides:

```text
corpus recurrence over section labels
front matter keys
heading depths
code fence languages
link target classes
```

Operator questions it can answer:

```text
What section labels recur across docs?
What front matter keys are common?
What code fence languages appear?
What heading depths dominate?
```

Visibility still missing:

```text
long-tail distribution buckets
rare entries surfaced separately
co-occurrence between recurring structures
example documents for each recurring entry
```

Assessment:

```text
useful, but becomes hard to interpret once recurrence lists grow
```

### `seed --documentation-structure --recurrence --top 25`

Provides:

```text
bounded recurrence list
```

Operator questions it can answer:

```text
What are the dominant repeated structures?
Which sections and metadata keys are most common?
```

Visibility still missing:

```text
what was hidden by the top bound
long-tail shape
whether top entries are too generic to be useful
```

Assessment:

```text
useful for readability
but can hide the rare/outlier structures that may be operationally valuable
```

### `seed --documentation-structure --missing-front-matter`

Provides:

```text
filtered list of documents missing YAML front matter
```

Operator questions it can answer:

```text
Which docs have no metadata block?
Where is front matter coverage incomplete?
```

Visibility still missing:

```text
which expected keys are missing when front matter exists
```

Assessment:

```text
high practical value
```

### `seed --documentation-structure --sections`

Provides:

```text
section inventory with document path
line range
heading level
heading text
child count
parent path
```

Operator questions it can answer:

```text
Where is a section located?
Which docs have unusually deep or shallow sections?
Which sections are nested under which headings?
```

Visibility still missing:

```text
section order comparison
section layout grouping
common section skeletons
```

Assessment:

```text
useful but potentially very verbose
```

### `seed --documentation-structure --links`

Provides:

```text
link target inventory
relative flag
under-docs flag
```

Operator questions it can answer:

```text
Which docs link to other docs?
Which links are external?
Which links are local docs links?
```

Visibility still missing:

```text
broken link examples in recurrence mode
most-linked docs
unlinked docs
link source-target graph summary
```

Assessment:

```text
more than grep because it classifies link target shape
but still needs aggregation to be highly useful
```

### `seed --documentation-structure --code-fences`

Provides:

```text
fenced code block inventory
line ranges
fence type
language
closed/unclosed status
```

Operator questions it can answer:

```text
Which docs contain code fences?
Which languages are used?
Are there unclosed fences?
```

Visibility still missing:

```text
documents with unusually many fences
language by document family
fences missing language labels
```

Assessment:

```text
useful structural hygiene surface
```

## Distribution investigation

The current recurrence view already exposes itemized recurrence counts and itemized summaries.

Implementation-visible recurrence categories:

```text
section_labels
front_matter_keys
heading_depths
code_fence_languages
```

The current recurrence report includes:

```text
total_distinct_entries
entries_at_or_above_min_count
```

The requested long-tail buckets are not currently visible as first-class output:

```text
count == 1
count == 2
count >= 5
count >= 10
count >= 25
```

Available evidence strongly suggests a long-tail distribution, especially section labels.

Reason:

The top observed section labels include very high-frequency items:

```text
Purpose: 276
Non-Goals: 106
Conclusion: 86
Central Finding: 63
```

but repository documentation has many investigation-specific section labels that likely appear once or only a few times.

Supported conclusion:

```text
long-tail distribution is likely
but not directly measurable from the reviewed output examples alone
```

Missing visibility:

```text
recurrence histogram
singleton count
doubleton count
threshold buckets
rare section examples
```

## Common, rare, missing, and outlier structures

### Common structures

Visible now through recurrence counts.

Examples:

```text
Purpose
Non-Goals
Conclusion
Central Finding
status
domain
doc_type
```

Value:

```text
reveals documentation conventions
```

### Rare structures

Only partially visible.

`--min-count` can lower or raise the inclusion threshold, but the surface does not directly frame rare structures as rare structures.

Value if exposed:

```text
reveals one-off document structure
reveals unusual investigation forms
reveals possible inconsistent headings
```

### Missing structures

Visible for front matter and structural completeness.

Partially visible for sections only through detail inspection.

Value:

```text
supports cleanup and consistency work
```

### Outlier structures

Partially visible through `--top` structural issue sorting.

Still missing:

```text
largest docs
most sections
deepest headings
most links
most code fences
most duplicate headings
```

Value:

```text
operator can find documents that need structural attention
```

## Does it feel like true visibility or fancy grep?

Mixed answer.

### More than grep

It is more than grep because it parses structural forms and exposes normalized observations:

```text
front matter presence and keys
heading hierarchy
section parent paths
link target classes
broken local docs link count
code fence closure
structure status
recurrence categories
```

A grep-like search would not reliably provide:

```text
heading hierarchy
empty section count
code fence closure
front matter key extraction
link target classification
```

### Where it still feels like fancy grep

The recurrence view can feel grep-like when it reports only raw labels and counts:

```text
Purpose: 276
Conclusion: 86
status: 135
```

without:

```text
examples
families
histograms
outlier framing
missing-by-pattern analysis
```

Recommendation:

```text
keep recurrence counts
add structural framing surfaces
```

## Noise sources

### Generic section labels

High-frequency labels such as:

```text
Purpose
Conclusion
Summary
```

may be structurally useful but not individually surprising.

### One-off section labels

Singletons may be meaningful, typo-like, or merely specialized.

Without grouping, they may become noise.

### Code fence language noise

Unlabeled fences may appear as `none`.

This is useful hygiene visibility but can be noisy if not paired with examples.

### Link noise

Raw link targets may become noisy without aggregation by target document or brokenness.

### Top-N truncation

`--top 25` improves readability but hides the tail.

The hidden tail may contain the best cleanup opportunities.

## Five proposed structural features

### 1. Recurrence histogram buckets

Problem addressed:

```text
The recurrence view does not directly show long-tail distribution.
```

Example output:

```text
Section label distribution:
  appears once: 412
  appears twice: 83
  appears 5+ times: 61
  appears 10+ times: 35
  appears 25+ times: 12
```

Why it remains structural:

```text
counts labels only
no interpretation of section meaning
```

### 2. Rare structure view

Problem addressed:

```text
Common structures dominate recurrence output; rare structures are hard to inspect.
```

Example output:

```text
Rare section labels:
- docs/example.md: "Boundary Narrowing Notes" count=1
- docs/other.md: "Deferred Concerns" count=1
```

Why it remains structural:

```text
reports label frequency and document path only
```

### 3. Section skeleton signatures

Problem addressed:

```text
Operators cannot see common document layouts, only individual headings.
```

Example output:

```text
Common section skeletons:
- Purpose > Findings > Supported Conclusions > Open Questions: 42 docs
- Summary > Findings > Non-Goals: 31 docs
```

Why it remains structural:

```text
uses ordered heading labels and levels
no claim or meaning extraction
```

### 4. Missing common sections

Problem addressed:

```text
The surface shows missing front matter but not missing common structural sections.
```

Example output:

```text
Docs missing common section "Non-Goals": 184
- docs/a.md
- docs/b.md
```

Why it remains structural:

```text
compares observed section labels against recurrence thresholds
no interpretation of whether the section should exist
```

### 5. Structural outlier ranking

Problem addressed:

```text
Operators need to find documents with unusual structural load or hygiene issues.
```

Example output:

```text
Structural outliers:
- docs/large.md: lines=1200 sections=84 depth=5 links=41 fences=19
- docs/deep.md: max_heading_depth=6 skipped_heading_level=true
```

Why it remains structural:

```text
uses document metrics, heading depth, section count, link count, and fence count only
```

## Recommendations

1. Add recurrence histogram buckets before adding any semantic features.
2. Add rare-structure and outlier views to make recurrence actionable.
3. Add example documents for recurrence rows so counts become navigable.
4. Preserve the current read-only and non-interpretive boundary explicitly in output.
5. Avoid any feature that says a section is important, authoritative, or conceptually related unless that remains a later investigation.

## Supported conclusions

1. The observer has made documentation structure visible without prose interpretation.
2. Recurrence mode adds real corpus-level visibility beyond per-document structure.
3. The surface is more than grep when it exposes hierarchy, parent paths, code fence closure, link classification, and structural completeness.
4. The recurrence view risks feeling like fancy grep when it only returns raw labels and counts.
5. Useful next steps remain purely structural: histograms, rare structures, section skeletons, missing common sections, and structural outliers.
6. Long-tail distribution is likely, but the current reviewed output does not directly expose requested buckets.

## Unsupported conclusions

- The current surface extracts meaning.
- The current surface extracts claims.
- Structural recurrence proves semantic recurrence.
- High-frequency section labels are automatically important.
- Rare section labels are automatically problems.
- Long-tail distribution is proven from fresh command execution in this session.
- The current recurrence surface fully answers distribution questions.

## Recommended next steps

```text
recurrence histogram buckets
rare structure view
section skeleton signatures
missing common sections
structural outlier ranking
```

These next steps are structural, read-only, and compatible with the current boundary.

## Acceptance answers

### What has the new observer actually made visible?

It has made document structure visible:

```text
front matter
headings
sections
links
code fences
metrics
structural completeness
```

and recurrence visible across:

```text
section labels
front matter keys
heading depths
code fence languages
link target classes
```

### Where does the recurrence surface become useful?

It becomes useful when it reveals common conventions, missing structure, dominant front matter keys, repeated section labels, code fence language usage, and link-target classes.

### Where does it become noisy?

It becomes noisy when raw labels dominate output without examples, buckets, families, outlier framing, or rare-structure framing.

### What structural visibility remains missing?

Missing structural visibility includes:

```text
long-tail histogram buckets
rare structures
common section skeletons
missing common sections
structural outliers
example documents for recurrence rows
```

### What are the five highest-value next features?

```text
recurrence histogram buckets
rare structure view
section skeleton signatures
missing common sections
structural outlier ranking
```

### Does the current implementation feel like a true visibility surface or merely a sophisticated grep?

It is a true visibility surface for per-document structure and structural hygiene.

The recurrence view is useful but currently close to sophisticated grep when it only emits raw recurring labels and counts.

It needs structural framing to become consistently actionable.
