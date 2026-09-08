# Structural Coverage Visibility Investigation

## Purpose and boundary

This investigation asks whether structural coverage visibility is a distinct layer beyond recurrence, drilldown, and membership.

This is investigation only.

It does not implement prose interpretation, claim extraction, authority inference, shape inference, ontology promotion, NLP, LLM analysis, recommendation systems, classification systems, compliance systems, workflow systems, or automation.

Repository authority wins.

## Current context

Recent documentation structure work established:

```text
structure visibility
    -> recurrence visibility
    -> structural drilldown
    -> structural membership
```

Current documentation structure capabilities include:

```text
document structure visibility
recurrence visibility
distribution visibility
rare/common structures
structural outliers
section skeleton signatures
drilldown concepts
membership concepts
```

The emerging question is:

```text
how much of the repository is covered by this structure?
```

not:

```text
what does this structure mean?
```

## Central finding

Structural coverage is a distinct visibility layer, but it is derived from membership.

The safest definition is:

```text
structural coverage
    = presence / absence of an exact observed structure
      across a defined document corpus
```

Coverage answers:

```text
how much of the corpus participates?

how much does not?
```

It remains structural when it reports only:

```text
presence
absence
counts
percentages
membership totals
```

It becomes unsafe when interpreted as:

```text
compliance
policy
correctness
required shape
standardization
shape authority
```

## Recurrence versus drilldown versus membership versus coverage

### Recurrence

Recurrence answers:

```text
what recurs?
how often does it recur?
```

Example:

```text
section-label:Purpose -> 277 occurrences or documents
front-matter-key:status -> 135 documents
skeleton:S -> 10 documents
```

### Drilldown

Drilldown answers:

```text
where does it recur?
```

Example:

```text
section-label:Purpose
    -> docs/a.md:12 depth=2
```

### Membership

Membership answers:

```text
which documents belong to the exact observed set?
```

Example:

```text
members of front-matter-key:status
    -> docs/a.md
    -> docs/b.md
```

### Coverage

Coverage answers:

```text
how much of the defined corpus is included or excluded?
```

Example:

```text
front-matter-key:status
    corpus_documents: 442
    present: 135
    missing: 307
    coverage: 30.5%
```

The distinction is:

```text
recurrence = count of observed structural rows

drilldown = source locations for rows

membership = exact included documents

coverage = corpus proportion and absence visibility
```

## What coverage means for observed structures

### Section label coverage

Structure:

```text
section-label:Purpose
```

Coverage means:

```text
documents containing exact section label Purpose
documents not containing exact section label Purpose
percentage of corpus containing Purpose
```

Safe because:

```text
presence and absence are structural
```

Unsafe if interpreted as:

```text
documents without Purpose are incomplete
```

### Front matter key coverage

Structure:

```text
front-matter-key:status
```

Coverage means:

```text
documents whose YAML front matter contains status
documents whose YAML front matter lacks status
documents without front matter at all
percentage of corpus containing status
```

Safe because:

```text
key presence is structural metadata visibility
```

Unsafe if interpreted as:

```text
documents without status violate policy
```

unless a separate policy exists.

### Skeleton coverage

Structure:

```text
skeleton:S
```

Coverage means:

```text
documents with exact skeleton signature S
documents without skeleton signature S
percentage of corpus matching S
```

Safe because:

```text
exact skeleton equality is structural
```

Riskier because skeleton coverage can create pressure toward:

```text
document family
document type
template
shape authority
```

### Outlier signal coverage

Structure:

```text
outlier:high_code_fence_count
```

Coverage means:

```text
documents carrying exact mechanical outlier signal X
documents not carrying signal X
percentage carrying signal X
```

Safe because:

```text
signal inclusion is mechanical
```

Unsafe if interpreted as:

```text
these documents need cleanup
```

### Structural completeness coverage

Structure:

```text
front matter present
H1 present
trailing newline present
no unclosed fences
```

Coverage means:

```text
number and percentage of documents with or without each structural completeness item
```

This is one of the strongest coverage cases because it is already close to existing structural completeness visibility.

Risk:

```text
completeness can sound like correctness
```

Output should remain descriptive.

## Does coverage answer questions recurrence and membership cannot?

Yes.

Recurrence can answer:

```text
status appears in 135 documents
```

Membership can answer:

```text
which 135 documents?
```

Coverage can answer:

```text
what proportion of the corpus is that?
how many documents do not contain status?
how fragmented is adoption?
```

Coverage is especially useful for:

```text
adoption visibility
absence visibility
fragmentation visibility
structural completeness visibility
corpus-wide comparison
```

Examples:

```text
How many documents contain status?
How many do not?
How much of the corpus uses YAML front matter?
How much of the corpus matches a common skeleton?
Which common structures have shallow adoption?
Which rare structures have tiny coverage?
```

## Coverage versus compliance

Coverage does not mean compliance.

Safe:

```text
front-matter-key:status coverage = 30.5%
```

Unsafe:

```text
69.5% of documents are non-compliant
```

Compliance requires:

```text
policy
standard
requirement
authority
```

Coverage only reports presence and absence.

## Coverage versus policy

Coverage does not define policy.

Safe:

```text
Non-Goals section appears in 106 documents and is absent in 336 documents
```

Unsafe:

```text
Non-Goals should appear in every document
```

unless a policy exists elsewhere.

## Coverage versus correctness

Coverage does not imply correctness.

Safe:

```text
document has YAML front matter
```

Unsafe:

```text
document metadata is correct
```

Presence is not correctness.

Absence is not error.

## Coverage versus required shape

Coverage does not imply required shape.

Safe:

```text
skeleton S covers 10 documents
```

Unsafe:

```text
skeleton S is the required shape for these documents
```

## Coverage versus standardization

Coverage can reveal adoption patterns.

It cannot define standardization by itself.

Safe:

```text
status key appears in 135 of 442 docs
```

Unsafe:

```text
status key should be standardized
```

Standardization is an authority or workflow decision.

## Coverage versus shape

Coverage can reveal how broadly a structure appears.

It cannot say the structure is a shape candidate.

Safe:

```text
section skeleton S covers 2.3% of corpus
```

Unsafe:

```text
section skeleton S is a repository shape
```

Shape pressure requires a different investigation.

## Can coverage remain purely structural?

Yes, if it reports only:

```text
corpus size
presence count
absence count
coverage percentage
membership totals
bounded present examples
bounded missing examples
explicit non-compliance boundary
```

Safe output example:

```text
Coverage

Category: front-matter-key
Key: status
Corpus Documents: 442
Present: 135
Missing: 307
Coverage: 30.5%
Boundary:
  structural coverage only; absence is not non-compliance, error, or required-shape failure
```

## Coverage opportunities

### Front matter coverage

Strongest opportunity:

```text
yaml front matter present / missing
front matter key present / missing
```

Reason:

```text
already structural
already corpus-level
operator value is clear
```

### Section label coverage

Opportunity:

```text
section label present / missing across corpus
```

Value:

```text
shows adoption of recurring section labels
```

Risk:

```text
can imply expected sections
```

### Skeleton coverage

Opportunity:

```text
exact skeleton signature coverage
```

Value:

```text
shows how concentrated or fragmented layouts are
```

Risk:

```text
can imply document family or template
```

### Outlier signal coverage

Opportunity:

```text
percentage of documents carrying mechanical outlier signals
```

Value:

```text
helps understand structural load and hygiene distribution
```

Risk:

```text
can imply cleanup priority
```

### Structural completeness coverage

Opportunity:

```text
coverage over H1, front matter, trailing newline, closed fences, non-empty sections
```

Value:

```text
strong structural health visibility
```

Risk:

```text
can sound like compliance if not labeled carefully
```

## Coverage limitations

### Denominator matters

Coverage must define corpus scope.

Examples:

```text
all docs
only docs with front matter
only markdown docs
only docs under docs/
only investigation docs
```

Without a denominator, coverage is ambiguous.

### Absence is not failure

A missing structure may be intentional.

### Presence is not adoption of meaning

A document containing `status` does not necessarily share status semantics with another document.

### Percentages can overstate authority

A high percentage can create pressure toward standardization.

A low percentage can create pressure toward cleanup.

Both pressures are unsupported by coverage alone.

### Skeleton coverage is especially risky

Exact skeleton membership may invite family/type/template interpretation.

Coverage should not name skeletons semantically.

## Counterexamples

### Coverage adds little beyond recurrence

For extremely common structures:

```text
heading depth 2 appears in most documents
```

coverage may simply restate recurrence.

### Coverage adds little beyond membership

For small exact sets:

```text
skeleton S -> 1 document
```

coverage percentage may add little beyond membership.

### Coverage creates compliance pressure

```text
Non-Goals missing from 336 documents
```

can be misread as:

```text
336 documents are wrong
```

Unsupported.

### Coverage creates standardization pressure

```text
status appears in 135 documents
```

can be misread as:

```text
status should be standardized everywhere
```

Unsupported.

### Coverage creates shape pressure

```text
skeleton S covers 10 documents
```

can be misread as:

```text
skeleton S is a document shape
```

Unsupported.

## Important distinctions

### Recurrence

```text
repeated structural observation
```

### Membership

```text
which documents are included in an exact structural set
```

### Coverage

```text
how much of a defined corpus is included or excluded
```

### Compliance

```text
conformance to a policy or requirement
```

Out of bounds.

### Policy

```text
authoritative requirement or rule
```

Out of bounds.

### Standardization

```text
adoption or enforcement of common structure
```

Out of bounds unless separately authorized.

### Shape

```text
candidate recurring structure with possible meaning pressure
```

Out of bounds.

## Relationship to prior work

Structural membership established:

```text
membership = exact observed inclusion in a structural recurrence set
```

Structural coverage extends this by adding denominator and absence:

```text
coverage = membership + corpus denominator + missing set
```

Structural drilldown established:

```text
drilldown = where occurrences are located
```

Coverage differs by focusing on corpus proportion rather than source location.

Observation-first work supports this conservative path:

```text
observe
accumulate
evaluate later
```

Coverage remains observation and accumulation.

It should not become evaluation of correctness.

## Supported conclusions

1. Structural coverage is a distinct visibility layer beyond recurrence, drilldown, and membership.
2. Coverage is derived from membership plus a defined corpus denominator and absence set.
3. Coverage can remain purely structural when limited to presence, absence, counts, percentages, and membership totals.
4. Coverage adds useful visibility around adoption, absence, fragmentation, and structural completeness.
5. Coverage is strongest for front matter, front matter keys, structural completeness, and section label presence.
6. Skeleton coverage is useful but carries stronger shape/family/type pressure.
7. Coverage becomes unsafe when interpreted as compliance, policy, correctness, required shape, standardization, or shape authority.

## Unsupported conclusions

- Coverage proves compliance.
- Coverage defines policy.
- Coverage proves correctness.
- Coverage establishes required structures.
- Coverage establishes document standards.
- Coverage establishes document shape.
- High coverage means importance.
- Low coverage means error.
- Missing structure means defect.
- Presence means semantic adoption.

## Recommended next step

If coverage becomes a future implementation target, the safest first slice is:

```text
front matter coverage
```

because it is already structural and already present in summary visibility.

Next safe slice:

```text
front matter key coverage
```

Example command shape:

```bash
seed --documentation-structure --coverage front-matter-key:status
```

Minimum output:

```text
Category: front-matter-key
Key: status
Corpus: docs markdown documents
Corpus Documents: 442
Present: 135
Missing: 307
Coverage: 30.5%
Boundary:
  structural coverage only; absence is not non-compliance, error, or required-shape failure
```

Next candidates after front matter:

```text
section-label coverage
structural-completeness coverage
skeleton-signature coverage
outlier-signal coverage
```

Skeleton coverage should come later because it has higher shape/family pressure.

## Acceptance answers

### What is structural coverage?

Structural coverage is presence and absence of an exact observed structure across a defined document corpus, expressed as counts and percentages.

### How is it different from recurrence?

Recurrence says what recurs and how often.

Coverage says how much of the corpus contains or lacks the structure.

### How is it different from membership?

Membership says which documents are included.

Coverage says what proportion of the corpus is included or excluded.

### Can coverage remain purely structural?

Yes, if limited to presence, absence, counts, percentages, membership totals, bounded examples, and explicit non-compliance boundaries.

### What visibility does coverage add?

Coverage adds adoption, absence, fragmentation, and structural completeness visibility.

### Where does coverage become compliance or shape pressure?

Coverage crosses the boundary when it is treated as:

```text
compliance
policy
correctness
required structure
standardization
document shape
importance
cleanup priority
```

Repository authority wins.
