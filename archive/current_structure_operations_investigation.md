# Current Structure Operations Investigation

## Purpose and boundary

This is a read-only structural investigation committed as a Markdown record.

It characterizes current repository evidence for structure operations.

It does not implement membership, create membership surfaces, create document families, create document types, create ontology, create shape candidates, create classification systems, create similarity systems, create recommendation systems, or propose future architecture.

Repository authority wins.

## Files inspected

Repository authority and implementation evidence:

- `AGENTS.md`
- `seed_runtime/documentation_structure.py`
- `scripts/seed_local.py`
- `tests/test_documentation_structure.py`

Investigation and phase-report evidence:

- `docs/documentation_structure_phase_3_investigation.md`
- `docs/documentation_structure_recurrence_surface_review.md`
- `docs/structural_recurrence_visibility_investigation.md`
- `docs/recurrence_navigation_investigation.md`
- `docs/structural_drilldown_investigation.md`
- `docs/structural_membership_investigation.md`
- `docs/structural_membership_observational_boundary_investigation.md`
- `docs/structural_coverage_visibility_investigation.md`

## Metadata characterization

The inspected investigation documents are represented structurally by filenames, headings, and prose bodies. They do not expose front-matter metadata in the inspected files.

| File | Front matter | `doc_type` | `status` | `domain` | `defines` count | `depends_on` count | `related` count |
|---|---:|---|---|---|---:|---:|---:|
| `docs/documentation_structure_phase_3_investigation.md` | missing | — | — | — | 0 | 0 | 0 |
| `docs/documentation_structure_recurrence_surface_review.md` | missing | — | — | — | 0 | 0 | 0 |
| `docs/structural_recurrence_visibility_investigation.md` | missing | — | — | — | 0 | 0 | 0 |
| `docs/recurrence_navigation_investigation.md` | missing | — | — | — | 0 | 0 | 0 |
| `docs/structural_drilldown_investigation.md` | missing | — | — | — | 0 | 0 | 0 |
| `docs/structural_membership_investigation.md` | missing | — | — | — | 0 | 0 | 0 |
| `docs/structural_membership_observational_boundary_investigation.md` | missing | — | — | — | 0 | 0 | 0 |
| `docs/structural_coverage_visibility_investigation.md` | missing | — | — | — | 0 | 0 | 0 |

## Implemented structure operations

### Documentation structure observation

The repository implements read-only documentation structure observation for Markdown documentation. Its declared boundary excludes prose interpretation, claim extraction, authority inference, shape inference, event-ledger writes, and repository mutation.

Observed output includes structural document records such as front-matter presence and key names, heading outlines, section inventories, link observations, code-block observations, counts, and summary fields.

Implementation status: implemented.

### Recurrence

Recurrence is implemented as a documentation structure recurrence report.

Observable evidence source:

- section labels
- front-matter key names
- heading depths
- code-fence languages
- link target classes
- section skeleton signatures
- common and missing section labels
- structural outlier signals

Question answered:

```text
what recurs?
how often does it recur?
how is recurrence distributed?
which rows are common, rare, missing, or outlying?
```

Authority owned:

- count and distribution visibility over observed structural rows

Input shape:

- repository documentation Markdown records under the implemented documentation structure observer
- optional output bounds such as top, min-count, max-count, limit, and summary-only

Output shape:

- itemized counts
- recurrence distributions
- rare rows
- section skeleton signature rows
- common section labels
- documents missing common section labels
- structural outlier rows
- link target class totals

Observational boundary:

- read only
- structural recurrence only
- no prose interpretation
- no claim extraction
- no authority inference
- no shape inference
- no ontology promotion
- no event-ledger writes
- no repository mutation

Implementation status: implemented.

Evidence strength: strong.

### Drilldown

Drilldown is implemented narrowly for exact section-label targets.

Observable evidence source:

- parsed section records containing exact heading text, document path, section start line, and heading level

Question answered:

```text
where does this already observed structure occur?
which exact source locations produced this count?
```

Authority owned:

- source-location evidence for an exact observed structural row

Input shape:

```text
--where section-label:<exact label>
```

Output shape:

- category
- key
- occurrence count
- document count
- bounded matches containing path, line, and depth

Observational boundary:

- read only
- exact structural occurrence visibility only
- no prose interpretation
- no claim extraction
- no authority inference
- no shape inference
- no ontology promotion
- no repository mutation

Implementation status: implemented for exact section-label drilldown only.

Evidence strength: strong for section-label drilldown; insufficient for broader drilldown categories.

## Candidate structure operations

### Membership

Membership is investigation-supported but not implemented as an explicit surface.

Safest observed definition:

```text
structural membership = exact observed inclusion in a structural recurrence set
```

Observable evidence source:

- exact section-label inclusion
- exact front-matter-key presence
- exact skeleton-signature equality
- exact outlier-signal inclusion

Question answered:

```text
which documents belong to this exact observed structural set?
```

Authority owned:

- set-boundary visibility for exact structural rows

Input shape:

- candidate exact structural key such as `section-label:<label>`, `front-matter-key:<key>`, `skeleton-signature:<signature>`, or `outlier-signal:<signal>`

Output shape:

- document set membership

Observational boundary:

- exact structural inclusion only
- no similarity
- no relatedness
- no recommendation
- no document family
- no document type
- no classification
- no shape candidate
- no ontology promotion

Implementation status: not implemented as an explicit membership operation.

Evidence strength: moderate as a candidate operation; insufficient as an implemented operation.

### Coverage

Coverage is investigation-supported as a distinct visibility layer, but only partially represented in current recurrence output.

Safest observed definition:

```text
structural coverage = presence / absence of an exact observed structure across a defined document corpus
```

Observable evidence source:

- exact structural row presence
- exact structural row absence
- corpus document count
- membership-like present and missing totals

Question answered:

```text
how much of the corpus participates?
how much does not?
```

Authority owned:

- corpus participation and absence visibility

Input shape:

- defined corpus
- exact observed structural key

Output shape:

- present count
- missing count
- optional percentage in the candidate model
- included/excluded corpus visibility

Observational boundary:

- presence
- absence
- counts
- percentages
- membership totals
- no compliance claim
- no policy claim
- no correctness claim
- no required shape
- no standardization claim
- no shape authority

Implementation status: not implemented as a standalone operation; partially represented by common section labels and documents missing common section labels in recurrence output.

Evidence strength: moderate as a candidate and partial recurrence substructure; weak as a standalone implemented operation.

## Operation responsibilities

| Operation | Current status | Primary question | Responsibility |
|---|---|---|---|
| Recurrence | Implemented | What recurs, and how often? | Count and distribution visibility over exact observed structural rows |
| Drilldown | Implemented narrowly | Where does this exact structure occur? | Source-location expansion for exact section-label rows |
| Membership | Candidate | Which documents belong to this exact structural set? | Set-boundary visibility over exact structural rows |
| Coverage | Candidate / partial | How much of the corpus participates or does not? | Presence/absence and corpus participation visibility |

## Operation comparison matrix

| Pair | Shared evidence | Distinct responsibility | Subsumption | Necessity |
|---|---|---|---|---|
| Recurrence vs membership | Both use exact observed structural rows | Recurrence counts rows; membership identifies included documents | Recurrence does not subsume membership because counts do not expose the set boundary | Both remain conceptually necessary; only recurrence is implemented |
| Recurrence vs drilldown | Drilldown expands an already observed recurrence row | Recurrence answers what/how many; drilldown answers where | Neither subsumes the other | Both remain necessary for implemented recurrence plus section-label source visibility |
| Recurrence vs coverage | Coverage uses presence/absence over exact structures; recurrence has common/missing rows | Recurrence counts/distributes; coverage frames corpus inclusion/exclusion | Recurrence partially contains coverage-like rows but does not standalone-subsumes coverage | Both remain conceptually necessary; coverage is partial |
| Membership vs drilldown | Both can expose documents for exact rows | Drilldown is location-oriented; membership is set-oriented | Section-label drilldown can approximate membership, but does not subsume broader membership candidates | Both remain conceptually distinct |
| Membership vs coverage | Coverage derives from membership-like present sets plus corpus denominator | Membership identifies included documents; coverage compares included and excluded corpus portions | Coverage depends on membership-like sets but does not subsume member listing | Both remain conceptually distinct |
| Drilldown vs coverage | Both can relate structures to documents | Drilldown gives path/line/depth occurrence evidence; coverage gives presence/absence and corpus proportion | Neither subsumes the other | Both remain conceptually distinct |

## Shared evidence

The shared implementation evidence is the documentation structure observer and recurrence boundary.

All current and candidate operations remain structurally safe only when they preserve exact observed structural evidence and avoid prose interpretation, authority inference, shape inference, ontology promotion, similarity, recommendation, and classification.

## Distinct evidence

### Recurrence

Distinct evidence for recurrence is implemented code, CLI exposure, formatter output, and tests asserting structural counts and boundaries.

### Drilldown

Distinct evidence for drilldown is implemented `--where section-label:<exact label>` behavior returning bounded path, line, and depth matches.

### Membership

Distinct evidence for membership is investigation evidence defining set-oriented exact inclusion in a recurrence set. Current implementation does not expose explicit membership facts.

### Coverage

Distinct evidence for coverage is investigation evidence defining corpus presence/absence visibility, plus implemented recurrence rows for common section labels and documents missing common section labels.

## Overlap analysis

Membership overlaps most strongly with recurrence and drilldown.

For section labels, recurrence can show a row count and drilldown can show path, line, and depth matches. Collapsing drilldown matches by path gives membership-like information for that exact section-label row.

That does not make membership identical to recurrence plus drilldown in the repository-supported candidate model, because membership is set-boundary visibility and applies to candidate structures where current drilldown has no equivalent, including front-matter-key membership, skeleton-signature membership, and outlier-signal membership.

The strongest repository-supported statement is:

```text
membership is distinct as a candidate structural operation,
but not implemented as an independent current surface.
```

## Boundary analysis

| Operation | Purely structural if | Pressure begins when |
|---|---|---|
| Recurrence | It reports exact observed structural counts and distributions | Counts are interpreted as meaning, importance, authority, shape, or ontology |
| Drilldown | It reports exact source locations for exact structural rows | It becomes navigation priority, recommendation, relatedness, or semantic expansion |
| Membership | It reports exact set inclusion only | It becomes similarity, document family, document type, classification, shape candidate, or ontology |
| Coverage | It reports presence, absence, counts, percentages, and corpus participation only | It becomes compliance, correctness, policy, standardization, required shape, or shape authority |

## Supporting evidence and contradicting evidence

### Recurrence

Supporting evidence:

- implemented recurrence report and builder
- CLI `--recurrence`
- tests for structural counts and boundary
- investigation evidence that structural recurrence can exist before interpretation

Contradicting evidence:

- none found against recurrence as an implemented structure operation

Evidence strength: strong.

### Drilldown

Supporting evidence:

- implemented drilldown report
- CLI `--where`
- exact section-label parser
- tests for exact structural source-location output and boundary
- investigation evidence defining drilldown as exact recurrence row plus bounded source locations

Contradicting evidence:

- broader drilldown categories are not implemented

Evidence strength: strong for section-label drilldown; insufficient beyond that.

### Membership

Supporting evidence:

- investigation defines exact observed structural membership
- investigation distinguishes set-oriented membership from location-oriented drilldown
- investigation identifies exact section-label, front-matter-key, skeleton-signature, and outlier-signal membership as clearest forms

Contradicting evidence:

- current implementation has no explicit membership facts or membership CLI surface
- section-label drilldown already contains membership-like path evidence

Evidence strength: moderate as a candidate; insufficient as an implemented operation.

### Coverage

Supporting evidence:

- investigation defines structural coverage as presence/absence across a defined corpus
- implementation computes common section labels and documents missing common section labels inside recurrence
- tests assert common/missing section visibility

Contradicting evidence:

- no standalone coverage operation or CLI surface is implemented
- coverage-like behavior currently exists only as part of recurrence output

Evidence strength: moderate as a candidate and partial recurrence substructure; weak as a standalone operation.

## Strongest supported structure-operation model

Current implemented model:

```text
documentation structure observation
    -> recurrence
        answers what/how many/how distributed
        includes rare/common/missing/outlier/skeleton visibility
    -> exact section-label drilldown
        answers where for exact section-label rows
```

Current candidate model:

```text
recurrence
    answers frequency

membership
    answers exact set inclusion

drilldown
    answers occurrence/source-location visibility

coverage
    answers representation and corpus participation visibility
```

Repository authority supports the distinction between these responsibilities, but implementation authority currently establishes only recurrence and exact section-label drilldown as explicit operations.

## Remaining uncertainties

- Whether membership should be treated as current operation: current evidence says no explicit implementation, yes as candidate.
- Whether coverage should be treated as current operation: current evidence says no standalone implementation, yes as partial recurrence visibility and candidate.
- Whether exact front-matter-key, skeleton-signature, or outlier-signal membership should be considered more than candidates: current evidence says no.
- Whether drilldown extends beyond section labels: current implementation says no.

## Files changed by this record

- `docs/current_structure_operations_investigation.md`
