# Documentation Authority And Seed Thesis Reconciliation

## Purpose

This document reconciles the documentation authority boundary between the top-level `README.md`, `docs/README.md`, `docs/seed.md`, foundational reconciliation papers, and implementation-facing documentation.

The triggering question was whether the main README should become, resemble, or directly contain `docs/seed.md`, and whether earlier alignment-correcting papers should remain required reading now that `docs/seed.md` exists.

This is a documentation-authority reconciliation. It does not rewrite the README, move documents, delete documents, change code, alter schemas, or modify tests.

---

## Central Finding

The correct response is reconciliation-first, not direct duplication.

`docs/seed.md` should not simply replace `README.md`.

The documents serve different authority roles:

```text
README.md
    repository orientation

docs/seed.md
    concise architectural thesis / constitutional statement

docs/README.md
    documentation navigation and map

reconciliation documents
    boundary reasoning and architectural case law

implementation docs / tests / code
    evidence for concrete claims about behavior
```

The architectural mistake would be collapsing these roles into one file.

---

## README.md Authority

The top-level README is the repository orientation surface.

It should answer:

```text
What is Seed?
What does the repository contain?
What does Seed currently own?
What does Seed not own?
Where should a reader start?
What is the current implementation shape?
```

It may include a concise thesis summary from `docs/seed.md`, but it should not become `docs/seed.md`.

README should remain useful to:

```text
new contributors
operators landing in the repository
reviewers trying to understand current scope
agents needing initial orientation
```

README should not become:

```text
a complete architectural constitution
a full reconciliation archive
a duplicate of every invariant
a generated wiki
a dumping ground for every current frontier
```

Recommended README posture:

```text
briefly state the Seed thesis
link to docs/seed.md as the canonical concise architectural statement
link to docs/README.md for map/navigation
avoid restating every reconciliation argument
```

---

## docs/seed.md Authority

`docs/seed.md` should be treated as the concise architectural thesis.

It answers:

```text
What is Seed fundamentally?
What are the central architectural invariants?
What survives implementation changes?
What is the compact statement of the system's claim model?
```

Its role is constitutional, not navigational.

It should remain short enough to be required alignment reading. If it grows into a long archive, it stops serving that purpose.

Appropriate content:

```text
Observation / Evidence / Fact / Relationship / Projection
Trust / Authority / Corroboration distinctions
Identity and alias invariants
Operator authority boundary
Documentation-as-evidence posture
core architectural invariants
```

Inappropriate content:

```text
full Prometheus-specific reasoning
complete package observation vocabulary
all historical implementation findings
complete document index
current branch task list
all rejected alternatives
```

Those belong in reconciliation documents or navigation maps.

---

## docs/README.md Authority

`docs/README.md` should be the documentation navigation surface.

It should answer:

```text
Where should I go for the thesis?
Where should I go for architecture status?
Where should I go for the knowledge map?
Where should I go for reconciliation chains?
Where should I go for implementation-facing docs?
```

It should not restate every document's argument.

Recommended shape:

```text
Start Here
    docs/seed.md
    README.md
    architectural status / knowledge map

Foundational Reconciliation Chain
    identity derivation
    evidence trust and source authority
    corroboration and fact promotion
    relationship promotion
    operator projection/interface boundaries when added

Observation Frontiers
    local host
    users/groups
    packages
    Prometheus
    future services/ports/firewall

Read Models / Operator Surfaces
    state summary
    impact
    current facts
    fact support
    graph issues

Historical / Deep Audits
    retained for context and boundary preservation
```

The docs README should behave like a map, not an encyclopedia.

---

## Foundational Alignment Papers

The earlier alignment-correcting papers remain valuable, but their role changes once `docs/seed.md` exists.

Relevant examples include:

```text
finding_applicability_index_proposal.md
operator_pain_as_frontier_signal_reconciliation.md
boundary_preservation_as_architectural_principle.md
active_context_and_working_set_reconciliation.md
```

They should not all be copied into the README.

They should not all be treated as always-required top-level reading.

They should be classified as foundational reconciliation context:

```text
Required when doing architectural work in that domain.
Referenced by docs/README.md.
Summarized only where necessary.
Not duplicated wholesale into docs/seed.md.
```

`docs/seed.md` may be sufficient for broad alignment, but not always sufficient for specialized work.

Examples:

```text
For general Seed orientation:
    README.md + docs/seed.md may be sufficient.

For boundary-sensitive implementation:
    docs/seed.md plus the relevant reconciliation chain is required.

For prompt/handoff alignment:
    docs/seed.md plus active-context and boundary-preservation papers may be required.

For deciding what to work on next:
    operator-pain-as-frontier-signal remains relevant.
```

This preserves the finding:

```text
Not every invariant is appropriate top-level knowledge.
```

---

## Invariant Classification

Invariants should be placed according to scope.

### Constitutional Invariants

Belong in `docs/seed.md` and may be briefly echoed in README.

Examples:

```text
Evidence accumulates.
Facts normalize.
Relationships connect.
Projections select.

Promote only what the evidence supports.

Related things are not necessarily the same thing.

Alias means equivalence.

Current state is a view.
```

### Boundary Invariants

Belong in reconciliation documents and may be linked from docs/README.

Examples:

```text
Prometheus instance labels are contextual scrape-target identifiers.
Filesystem measurements do not create storage identity.
A package does not imply a running service.
A host:port endpoint is endpoint identity, not host identity.
```

### Implementation Invariants

Belong near code, tests, generated architecture docs, or focused implementation docs.

Examples:

```text
specific parser behavior
specific CLI rendering behavior
specific projection helper ownership
specific test characterization
```

### Historical Findings

Belong in audits/reconciliations when they explain why a boundary exists, but should not be repeated as current top-level guidance unless still active.

---

## Documentation Duplication Boundary

Duplication is not always a writing problem. Often it is an authority problem.

Repeated statements across README, docs/seed.md, roadmap docs, status docs, and reconciliation docs should be evaluated by asking:

```text
Which document owns this claim?
Which documents should reference it?
Which documents are repeating it because they lack a pointer?
Which copies are historical context rather than current authority?
```

Recommended rule:

```text
Own once.
Reference often.
Restate only when the local document needs the invariant to be understood.
```

This preserves readability without creating competing authorities.

---

## Reconciliation-First Documentation Posture

The repeated lesson is:

```text
Reconciliation first.
Rewrite second.
```

Directly rewriting README from `docs/seed.md` would risk collapsing roles.

Directly making docs/README contain every important invariant would risk turning navigation into doctrine.

Directly deleting older alignment papers would risk losing boundary reasoning that remains applicable in specific contexts.

The correct sequence is:

```text
identify document authority
classify claims by scope
move or reference claims according to authority
then edit documents narrowly
```

---

## Recommended Follow-Up Implementation

This reconciliation supports a later documentation update with these boundaries:

### README.md

Update lightly:

```text
reference docs/seed.md near the top as the concise architectural statement
remove or refresh stale capability-growth priority text
avoid copying all of docs/seed.md
keep repository orientation role
```

### docs/README.md

Update more substantially:

```text
make it a navigation map
add docs/seed.md as Start Here
add foundational reconciliation chain
classify alignment papers as foundational context
avoid restating all findings
```

### docs/seed.md

Leave mostly stable:

```text
keep concise
avoid turning it into a full map
avoid Prometheus/package/user-specific expansions
```

### Older Alignment Papers

Retain and reference:

```text
not superseded globally
not required for every reader
required or recommended when working in their relevant boundary area
```

---

## Non-Goals

This reconciliation does not:

```text
edit README.md
edit docs/README.md
edit docs/seed.md
delete older papers
rename documents
create a generated wiki
create a documentation build system
choose final reading order for every document
```

It defines the authority boundary needed before those edits.

---

## Conclusion

`docs/seed.md` should become the concise architectural thesis, not a replacement for the repository README.

`README.md` should orient readers to the repository and point to `docs/seed.md` for the thesis.

`docs/README.md` should become the documentation map that routes readers from the thesis to status, maps, reconciliation chains, and implementation-facing references.

The foundational alignment papers remain useful, but they become contextual references rather than universal top-level doctrine.

The governing principle is:

```text
Not every invariant is appropriate top-level knowledge.
Authority should follow scope.
Reconciliation should precede rewrite.
```
