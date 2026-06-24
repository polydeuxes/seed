# Structural Coverage Exact-Observable Investigation

## Purpose and boundary

This is a bounded structural investigation.

It characterizes the smallest repository-supported definition of structural coverage.

It does not implement coverage.

It does not create a coverage surface, document family, document type, similarity system, classification system, ontology, shape inference, or recommendation system.

Repository authority wins.

## Files inspected

- `AGENTS.md`
- `seed_runtime/documentation_structure.py`
- `tests/test_documentation_structure.py`
- `docs/structural_coverage_visibility_investigation.md`
- `docs/structural_membership_investigation.md`
- `docs/structural_membership_observational_boundary_investigation.md`
- `docs/structural_drilldown_investigation.md`
- `docs/structural_recurrence_visibility_investigation.md`
- `docs/documentation_structure_recurrence_surface_review.md`
- `docs/recurrence_first_shape_discovery_investigation.md`
- `docs/observation_first_discovery_recurrence_investigation.md`
- `docs/recurrence_navigation_investigation.md`
- `docs/documentation_structure_phase_3_investigation.md`

## Metadata characterization

All inspected investigation documents were missing YAML front matter.

| File | Front matter | `doc_type` | `status` | `domain` | `defines` count | `depends_on` count | `related` count |
|---|---:|---:|---:|---:|---:|---:|---:|
| `docs/structural_coverage_visibility_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/structural_membership_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/structural_membership_observational_boundary_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/structural_drilldown_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/structural_recurrence_visibility_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/documentation_structure_recurrence_surface_review.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/recurrence_first_shape_discovery_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/observation_first_discovery_recurrence_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/recurrence_navigation_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |
| `docs/documentation_structure_phase_3_investigation.md` | missing | missing | missing | missing | 0 | 0 | 0 |

## Smallest repository-supported definition

The smallest repository-supported definition is:

```text
structural coverage =
    presence and absence of an exact observed structure
    across a defined document corpus,
    expressed as counts and proportion
```

Equivalently:

```text
coverage = exact structural membership + corpus denominator + missing set
```

Coverage remains structural when it reports only:

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

Coverage becomes unsupported when interpreted as:

```text
compliance
policy
correctness
required shape
standardization
shape authority
document family
document type
similarity
classification
ontology
recommendation
prose meaning
```

## Coverage candidate models

### Candidate: coverage = recurrence + denominator

Support:

- Recurrence reports structural rows and counts.
- Recurrence reports the selected document count.
- A document-level recurrence count can be a coverage numerator.

Contradiction:

- Raw recurrence can count occurrences, not documents.
- A document may contain the same section label multiple times.
- Therefore occurrence recurrence is not always a valid coverage numerator.

Observable inputs:

- exact structural row
- corpus documents
- recurrence count

Observable outputs:

- item count
- possible corpus proportion if the count is document-level

Interpretation pressure:

- Frequency may be read as importance or requiredness.

Implementation evidence:

- Recurrence counts section labels, front matter keys, heading depths, and code fence languages.
- Recurrence separately has document-count context.

Assessment:

```text
partially supported, incomplete
```

### Candidate: coverage = membership measurement

Support:

- Membership is exact observed inclusion in a structural recurrence set.
- Coverage is explicitly dependent on membership plus denominator and missing set.
- Membership supplies the present set.
- The denominator supplies the corpus.
- Set subtraction supplies absence.

Contradiction:

- Membership alone does not report denominator or missing set.
- For tiny membership sets, coverage percentage may add little.

Observable inputs:

- exact structural row
- member set
- corpus denominator

Observable outputs:

- present count
- missing count
- coverage percentage
- optional bounded present and missing examples

Interpretation pressure:

- Absence may be misread as non-compliance.
- Presence may be misread as semantic adoption.

Implementation evidence:

- Exact section-label membership is implemented.
- The membership implementation checks exact section-label containment.
- Membership output reports category, key, member count, members, and boundary.

Assessment:

```text
strongest supported model
```

### Candidate: coverage = drilldown aggregation

Support:

- Drilldown reports exact occurrences and source locations.
- Drilldown also reports a document count for exact section-label matches.
- Drilldown can contain membership-like information.

Contradiction:

- Drilldown is source-location oriented.
- Coverage is denominator/proportion/absence oriented.
- Aggregating drilldown still requires an external denominator and missing set.

Observable inputs:

- exact structural row
- source-location matches
- corpus denominator

Observable outputs:

- occurrences
- documents with occurrences
- source locations
- possible proportion if denominator is added

Interpretation pressure:

- Drilldown paths may be misread as related, similar, recommended, or important documents.

Implementation evidence:

- Drilldown is implemented for exact section labels.
- Drilldown outputs occurrences, documents, path, line, and depth.

Assessment:

```text
weak as the primary coverage model
```

### Candidate: coverage = distinct operation

Support:

- Coverage has a distinct question:

```text
how much of the defined corpus is included or excluded?
```

- Recurrence does not directly answer absence and proportion.
- Membership does not directly answer denominator and absence.
- Drilldown does not directly answer corpus proportion.

Contradiction:

- Coverage is not implemented as a distinct option or report.
- Coverage is data-derived from membership rather than independent.

Observable inputs:

- exact structural row
- member set
- corpus denominator
- missing set

Observable outputs:

- corpus documents
- present
- missing
- coverage percentage
- structural boundary

Interpretation pressure:

- Percentages can create compliance, standardization, or shape pressure.

Implementation evidence:

- No coverage surface is implemented.
- Recurrence, drilldown, and membership are implemented.
- Existing common-section missing evidence is coverage-like but not a coverage operation.

Assessment:

```text
conceptually distinct, data-derived, not implemented
```

## Coverage responsibilities

Coverage is responsible for:

```text
how many corpus documents contain the exact structure
how many corpus documents do not contain the exact structure
what proportion of the corpus contains the exact structure
```

Coverage is not responsible for:

```text
why the structure appears
whether the structure is required
whether absence is an error
whether presence is correctness
whether documents are related
whether documents form a type or family
```

## Coverage inputs

The minimal inputs are:

```text
exact structural target
defined corpus denominator
present membership set
missing set derived from denominator minus present set
```

Examples of exact structural targets:

```text
section-label:Purpose
section-label:Conclusion
section-label:Boundary
front-matter-key:status
```

## Coverage outputs

The minimal outputs are:

```text
Category
Key
Corpus Documents
Present
Missing
Coverage percentage
Boundary
```

Example shape:

```text
Category: section-label
Key: Purpose
Corpus Documents: 480
Present: 267
Missing: 213
Coverage: 55.6%
Boundary: structural coverage only; absence is not non-compliance, error, or required-shape failure
```

The numbers above illustrate the observed current `Purpose` member count against the observed current documentation-structure corpus size at investigation time. They are not a proposed implementation contract.

## Exact examples

### `section-label:Purpose`

Recurrence reports:

```text
Purpose occurrence frequency
```

Membership reports:

```text
documents containing exact section label Purpose
```

Drilldown reports:

```text
exact Purpose heading locations with path, line, and depth
```

Coverage would report:

```text
corpus documents
present documents containing exact Purpose
missing documents not containing exact Purpose
present / corpus percentage
```

### `section-label:Conclusion`

Recurrence reports:

```text
Conclusion occurrence frequency
```

Membership reports:

```text
documents containing exact section label Conclusion
```

Drilldown reports:

```text
exact Conclusion heading locations with path, line, and depth
```

Coverage would report:

```text
corpus documents
present documents containing exact Conclusion
missing documents not containing exact Conclusion
present / corpus percentage
```

### `section-label:Boundary`

Recurrence reports:

```text
Boundary occurrence frequency, if visible at the selected recurrence threshold
```

Membership reports:

```text
documents containing exact section label Boundary
```

Drilldown reports:

```text
exact Boundary heading locations with path, line, and depth
```

Coverage would report:

```text
corpus documents
present documents containing exact Boundary
missing documents not containing exact Boundary
present / corpus percentage
```

Coverage would not infer that documents without `Boundary` are incomplete.

## Comparison with recurrence

Shared evidence:

- Both use exact observed structural rows.
- Both can remain non-semantic.

Distinct responsibility:

```text
recurrence = what recurs and how often
coverage = how much of the denominator contains or lacks it
```

Reducibility:

- Coverage is not reducible to raw recurrence when recurrence counts occurrences.
- Coverage can use document-level recurrence as numerator evidence.

New visibility:

- denominator
- absence
- proportion
- fragmentation/adoption visibility

## Comparison with membership

Shared evidence:

- Both depend on exact structural inclusion.

Distinct responsibility:

```text
membership = which documents are included
coverage = what proportion is included or excluded
```

Reducibility:

- Coverage is reducible to membership plus denominator plus missing set.
- Membership alone is not coverage.

New visibility:

- corpus denominator
- missing count
- percentage

## Comparison with drilldown

Shared evidence:

- Both can start from one exact observed structural row.

Distinct responsibility:

```text
drilldown = where occurrences are located
coverage = how much of the corpus contains or lacks the structure
```

Reducibility:

- Coverage is not best reduced to drilldown.
- Drilldown can help prove the numerator but does not supply coverage by itself.

New visibility:

- absence and corpus proportion rather than source locations.

## Coverage boundary analysis

Coverage can remain purely structural if it reports only exact presence, exact absence, counts, percentages, and structural boundaries.

Coverage introduces pressure toward unsupported interpretation when operators read it as:

```text
similarity
classification
document family
document type
shape inference
ontology promotion
prose interpretation
policy
compliance
standardization
recommendation
```

The safest wording is descriptive:

```text
present
missing
coverage
```

The unsafe wording is evaluative:

```text
compliant
non-compliant
valid
invalid
required
standard
family
type
recommended
```

## Evidence supporting coverage as distinct

Strong:

- Coverage has a distinct question: how much of the defined corpus is included or excluded.
- Coverage adds denominator and absence visibility not directly supplied by recurrence, membership, or drilldown.

Moderate:

- Existing recurrence output includes corpus document count and structural counts.
- Existing membership output supplies exact included documents.
- Existing common-section recurrence evidence already contains present and missing counts for common labels.

## Evidence contradicting coverage as distinct

Strong:

- Coverage is not implemented as a distinct documentation-structure operation.
- Existing implementation exposes recurrence, drilldown, and membership, not coverage.

Moderate:

- Coverage is derived from membership and denominator rather than independent.

Weak:

- For very common or very small sets, coverage may add little beyond recurrence or membership.

## Evidence strength assessment

| Claim | Strength |
|---|---:|
| Coverage requires a denominator | strong |
| Coverage depends on exact membership | strong |
| Coverage is distinct from recurrence in responsibility | strong |
| Coverage is distinct from drilldown in responsibility | strong |
| Coverage is distinct from membership in output | moderate to strong |
| Coverage is implemented | contradicted |
| Coverage can remain structural | moderate to strong |

## Strongest repository-supported model

The strongest repository-supported model is:

```text
coverage = membership measurement over a defined corpus
```

Expanded:

```text
coverage = exact structural membership + corpus denominator + missing set + counts/proportion
```

This is the smallest model that answers:

```text
what coverage measures
what coverage is measured across
why coverage is distinct from recurrence
why coverage is distinct from membership
why coverage is distinct from drilldown
```

## Remaining uncertainties

- Coverage is not implemented.
- Corpus denominator labeling would need to be explicit if coverage were ever implemented.
- Raw occurrence recurrence must not be mistaken for document coverage.
- Front matter key coverage is strongly supported conceptually, but exact membership implementation evidence is currently strongest for section labels.
- Skeleton coverage has stronger document-family, document-type, and shape-pressure risk.

## Files changed

- `docs/structural_coverage_exact_observable_investigation.md`

## LOC changed

One Markdown investigation file was added.
