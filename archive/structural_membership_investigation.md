# Structural Membership Investigation

## Purpose and boundary

This investigation asks whether structural membership is a distinct visibility layer beyond structural drilldown.

This is investigation only.

It does not implement prose interpretation, claim extraction, authority inference, shape inference, ontology promotion, NLP, LLM analysis, recommendation systems, classification systems, workflow systems, or automation.

Repository authority wins.

## Current context

Recent documentation structure work established:

```text
structure visibility
    -> recurrence visibility
    -> structural drilldown
```

Current documentation structure capabilities include:

```text
document structure visibility
recurrence visibility
distribution visibility
rare/common structures
structural outliers
section skeleton signatures
drilldown candidates
```

Recent findings established:

```text
recurrence visibility
    = what recurs

structural drilldown
    = where does it recur
```

The safest drilldown slice was identified as:

```text
section label
    -> matching document paths
    -> line number
    -> heading depth
```

## Central finding

Structural membership is distinct from drilldown, but only narrowly.

The safest definition is:

```text
structural membership
    = exact observed inclusion in a structural recurrence set
```

Examples:

```text
document belongs to recurrence row section-label:Purpose

document belongs to recurrence row front-matter-key:status

document belongs to exact skeleton signature S

document belongs to outlier signal high_section_count
```

Membership remains structural only when it is defined by exact observed structural inclusion.

It becomes interpretation when it is treated as:

```text
relatedness
similarity
recommendation
document family
document type
shape candidate
```

## Drilldown versus membership

### Drilldown

Drilldown answers:

```text
where does this observed structure occur?
```

Typical output:

```text
section label Purpose
    -> docs/a.md:12 depth=2
    -> docs/b.md:9 depth=2
```

Drilldown is location-oriented.

### Membership

Membership answers:

```text
which documents belong to this exact observed structural set?
```

Typical output:

```text
members of section-label:Purpose
    -> docs/a.md
    -> docs/b.md
```

Membership is set-oriented.

### Distinction

```text
drilldown
    -> location evidence for occurrences

membership
    -> inclusion in an exact structural set
```

They overlap.

A drilldown result can contain membership information.

But membership focuses on the set boundary rather than the location row.

## What constitutes membership?

### Section label membership

Shape:

```text
document contains exact normalized section label X
```

Example:

```text
section-label:Purpose
    members: 277 documents
```

Safe because:

```text
membership is exact heading-label inclusion
```

Unsafe if expanded to:

```text
documents about purpose
```

### Front matter key membership

Shape:

```text
document contains front matter key X
```

Example:

```text
front-matter-key:status
    members: 135 documents
```

Safe because:

```text
membership is exact key presence
```

Unsafe if expanded to:

```text
documents with same status meaning
```

### Skeleton signature membership

Shape:

```text
document has exact section skeleton signature S
```

Example:

```text
skeleton:S
    members: 10 documents
```

Safe because:

```text
membership is exact structural equality
```

Riskier because operators may read the set as a document family or type.

### Outlier signal membership

Shape:

```text
document carries exact mechanical outlier signal X
```

Example:

```text
outlier:high_code_fence_count
    members: docs/a.md, docs/b.md
```

Safe because:

```text
membership is exact signal inclusion
```

Unsafe if expanded to:

```text
documents needing cleanup
important documents
```

### Rare/common structure membership

Shape:

```text
document contains a structure in bucket X
```

Example:

```text
rare-section-label-member
    -> docs/a.md contains singleton label Q
```

Useful but noisier than exact key membership.

The membership set must preserve the observed key, not only the bucket.

## Does membership provide visibility beyond drilldown?

Yes, but narrowly.

Membership adds visibility when the operator question is set-oriented:

```text
Which documents belong to this recurrence row?

Which documents share this exact structural key?

Which documents share this exact skeleton?

Which documents carry this exact outlier signal?
```

Drilldown is strongest for source inspection.

Membership is strongest for set boundary visibility.

Examples:

```text
Purpose: 277
```

Drilldown asks:

```text
where are the Purpose headings?
```

Membership asks:

```text
which documents are in the Purpose set?
```

For skeleton signatures, membership may be more natural than drilldown:

```text
skeleton S: 10 docs
```

The primary question is likely:

```text
which 10 docs?
```

not:

```text
what line did the skeleton occur on?
```

## Membership versus relatedness

Membership does not mean relatedness.

Safe:

```text
docs A and B both contain section-label:Purpose
```

Unsafe:

```text
docs A and B are related
```

Relatedness implies a relationship beyond exact structural inclusion.

Membership only says both documents are in the same observed set.

## Membership versus similarity

Membership does not mean similarity unless the membership key itself is exact structural equality.

Safe:

```text
docs A and B have exact skeleton signature S
```

Unsafe:

```text
docs A and B are similar documents
```

Similarity introduces distance, weighting, thresholds, and interpretation.

Membership uses exact inclusion.

## Membership versus recommendation

Membership does not rank or recommend documents.

Safe:

```text
members shown alphabetically or deterministically
```

Unsafe:

```text
recommended members to inspect
```

A bounded member list is not a priority list.

## Membership versus document family

Membership does not establish document family.

Safe:

```text
exact skeleton members
```

Unsafe:

```text
architecture family
investigation family
status-report family
```

Family language implies classification or semantic grouping unless separately established.

## Membership versus document type

Membership does not establish document type.

Safe:

```text
document has front matter key doc_type
```

Unsafe:

```text
document is type X because it shares skeleton S
```

Document type is classification.

Membership is inclusion.

## Membership versus shape

Membership does not establish shape.

Safe:

```text
section skeleton S has 10 exact members
```

Unsafe:

```text
section skeleton S is a shape candidate
```

Shape pressure asks whether recurrence has reusable meaning.

Membership only preserves the set of documents that produced the structural recurrence row.

## Can membership remain purely structural?

Yes, if all of the following remain true:

```text
membership key is exact and structural
membership set is derived from observed structure
output uses paths, counts, line/depth evidence, and bounded examples
no semantic expansion
no relatedness claim
no similarity scoring
no recommendation
no family/type naming
no shape promotion
```

The safest phrase is:

```text
members of exact structural row
```

not:

```text
related docs
similar docs
document family
```

## Useful operator questions

Structural membership can answer:

```text
Which documents belong to this recurrence row?

Which documents share this exact structural key?

Which documents share this exact skeleton?

Which documents carry this exact outlier signal?

Which documents are members of a rare-section-label row?

Which documents are members of the front-matter-key:status set?
```

It can support:

```text
coverage review
structural auditing
source inspection
cleanup planning by humans
inventory review
```

without itself becoming recommendation or interpretation.

## Counterexamples

### Membership adds little beyond drilldown

For small or single-occurrence rows:

```text
section-label:Unique Heading -> 1 document
```

membership and drilldown may be nearly identical.

The member set adds little beyond the location.

### Very common membership sets are noisy

For rows such as:

```text
section-label:Purpose -> 277 documents
code-fence-language:text -> 7890 occurrences
```

an exhaustive member list may be noisy.

Bounded output and explicit count are important.

### Membership creates family pressure

Exact skeleton membership can tempt operators to say:

```text
these are the same kind of document
```

Repository evidence does not support that from skeleton equality alone.

### Membership creates type pressure

Front matter key membership can tempt operators to say:

```text
docs with status key are status-bearing documents
```

Key presence alone does not establish type, lifecycle, authority, or correctness.

### Membership creates recommendation pressure

Rare/outlier membership can tempt operators to say:

```text
these need cleanup first
```

Outlier membership is a structural signal, not a workflow priority.

## Important distinctions

### Visibility

```text
what exists or recurs
```

### Recurrence

```text
repeated structural observation
```

### Drilldown

```text
where occurrences are located
```

### Membership

```text
which documents are included in an exact structural set
```

### Similarity

```text
likeness across documents based on a comparison rule
```

Out of bounds unless reduced to exact structural equality.

### Relatedness

```text
relationship between documents
```

Out of bounds.

### Classification

```text
assigning category or type
```

Out of bounds.

### Type

```text
class of document or artifact
```

Out of bounds unless explicitly represented by existing structural metadata and not inferred.

### Family

```text
semantic or conceptual grouping
```

Out of bounds.

### Shape

```text
candidate recurring structure with possible meaning pressure
```

Out of bounds for this investigation.

## Relationship to prior work

The structural drilldown investigation established:

```text
structural drilldown = exact recurrence row + bounded source locations
```

This investigation refines that into:

```text
structural membership = exact recurrence row + set inclusion
```

Prior recurrence navigation work established that navigation should answer:

```text
Where does this structure occur?
```

This investigation adds a neighboring safe question:

```text
Which documents are members of this exact observed structural set?
```

The answer remains safe only while it is exact, structural, and non-semantic.

## Supported conclusions

1. Structural membership is a meaningful but narrow visibility layer beyond drilldown.
2. Drilldown is location-oriented; membership is set-oriented.
3. Membership can remain purely structural when defined as exact observed inclusion in a structural recurrence set.
4. The clearest membership sets are section-label membership, front-matter-key membership, exact skeleton-signature membership, and outlier-signal membership.
5. Membership provides useful visibility for coverage review, structural auditing, and inventory review.
6. Membership becomes unsafe when it turns into relatedness, similarity, recommendation, document family, document type, classification, or shape pressure.
7. Exact skeleton membership is useful but has the strongest family/type pressure and needs careful labeling.

## Unsupported conclusions

- Membership proves documents are related.
- Membership proves documents are similar.
- Membership recommends documents.
- Membership establishes document family.
- Membership establishes document type.
- Membership establishes shape candidates.
- Shared section labels imply shared content.
- Shared skeletons imply shared intent.
- Rare/outlier membership implies cleanup priority.
- Front matter key membership implies lifecycle or authority state.

## Recommended next step

Do not implement semantic grouping.

If membership becomes a future implementation target, the safest first slice is:

```text
section-label membership
```

Example command shape:

```bash
seed --documentation-structure --recurrence --members section-label:Purpose --limit 25
```

Safer wording may be:

```bash
seed --documentation-structure --recurrence --where section-label:Purpose --members --limit 25
```

Minimum output:

```text
category: section-label
key: Purpose
member_count: 277
shown_count: 25
members:
  - path: docs/example.md
    occurrences: 1
    lines: [12]
    depths: [2]
boundary: exact structural membership only; no relatedness, similarity, recommendation, family, type, or shape inference
```

Next slices, if needed:

```text
front-matter-key membership
skeleton-signature membership
outlier-signal membership
code-fence-language membership
```

## Acceptance answers

### What is structural membership?

Structural membership is exact observed inclusion in a structural recurrence set.

### How is it different from drilldown?

Drilldown answers where occurrences are located.

Membership answers which documents belong to the exact observed set.

### How is it different from similarity?

Similarity requires comparison, distance, weighting, or interpretation.

Membership requires only exact inclusion.

### Can membership remain purely structural?

Yes, if it is exact, bounded, source-backed, and non-semantic.

### Does membership create useful visibility?

Yes.

It can answer which documents share an exact structural key, skeleton, or signal without claiming meaning.

### Where does membership become classification or shape pressure?

It crosses the boundary when membership is treated as:

```text
related documents
similar documents
recommended documents
document family
document type
semantic group
shape candidate
```

Repository authority wins.
