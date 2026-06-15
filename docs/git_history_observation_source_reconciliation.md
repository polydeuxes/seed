# Git History Observation Source Reconciliation

## Purpose

This reconciliation examines whether Git history should be treated as a repository observation source for Seed.

It is documentation-only.

It does not implement runtime behavior, schemas, commands, collectors, projections, caches, indexes, tests, or CLI changes.

## Trigger

Recent repository-navigation and operator-surface work exposed a recurring limitation:

```text
Seed can observe current repository files,
but it does not preserve enough about how those files changed over time.
```

The current repository contents answer:

```text
What exists now?
```

Git history can answer different questions:

```text
What changed?
When did it change?
What came before?
What followed?
Which documents preceded implementation?
Which audits or observations created pressure for later code?
```

This matters because recent work repeatedly depends on sequence.

## Central Finding

Git history is a distinct repository observation source.

It should not be collapsed into current file observation.

Current file content preserves artifact state.

Git history preserves change sequence, temporal relationship, and repository evolution evidence.

The useful distinction is:

```text
Current File Observation
    answers what exists now.

Git History Observation
    answers how repository state changed.
```

Seed needs both to support inquiry lineage, implementation lineage, documentation lineage, and explanatory navigation.

## Boundary

Git history is evidence of repository change.

It is not proof of architectural correctness.

It is not authority over documentation contents.

It is not runtime truth.

It is not operator intent by itself.

It is not a complete inquiry transcript.

It is not a full explanation of why work happened.

It is a source of temporal and change evidence that can support later claims about repository evolution.

## What Git History Preserves

Git history can preserve:

- commit order;
- commit subject;
- commit body when present;
- author and committer metadata;
- timestamps;
- changed files;
- added/removed line counts;
- patch shape;
- rename/copy/delete signals;
- branch or PR association when available;
- proximity between documentation and implementation changes;
- audit-before-implementation sequences;
- implementation-before-audit sequences;
- repeated-touch surfaces;
- change clusters;
- rollback/revert signals;
- merge boundaries.

These are not the same as current repository contents.

A file can exist without preserving why it appeared, what it displaced, or what followed from it.

## What Git History Does Not Preserve By Itself

Git history does not automatically preserve:

- the full conversation that led to a commit;
- the operator's complete intent;
- whether the change was correct;
- whether a commit message accurately describes the change;
- whether the implementation fully satisfied the architectural boundary;
- whether the author understood the architecture;
- whether a later change superseded the finding;
- whether a PR discussion altered interpretation.

Those require additional evidence surfaces.

## Relationship To Inquiry Lineage

Inquiry lineage depends on order and relation.

Without git history, Seed can see:

```text
doc A exists
doc B exists
implementation C exists
```

but cannot reliably know:

```text
doc A preceded implementation C
implementation C exposed issue D
audit B followed implementation C
```

Git history can provide temporal scaffolding for inquiry lineage.

It does not replace inquiry lineage documents.

It supplies evidence that can support lineage claims.

## Relationship To Documentation Lineage

Documentation lineage asks how documents relate, move, refine, criticize, supersede, or route one another.

Current file observation can show document content and links.

Git history can show:

```text
when a document was created;
when it was routed;
when it was edited;
what files were changed with it;
whether implementation followed;
whether later navigation surfaces added it.
```

This helps distinguish:

```text
conceptual relationship
```

from:

```text
temporal repository relationship
```

Both matter, but they are not the same.

## Relationship To Implementation Lineage

Implementation lineage asks how behavior changed.

Git history can show:

```text
commit X changed state_summary_views.py
commit Y changed tests
commit Z added audit documentation
```

This helps answer operator and maintainer questions such as:

```text
Which commit introduced this behavior?
Which audit preceded this patch?
Which files changed together?
Was this cleanup part of a larger cluster?
```

Current source navigation cannot answer those questions without history.

## Relationship To Explanation Surfaces

Explanation surfaces often need sequence.

For example:

```text
Why is endpoint prominence being fixed now?
```

A current-file answer may identify code.

A git-history-aware answer can identify:

```text
storage summary leak was fixed;
endpoint prominence then became visible;
endpoint audit followed;
top-entity ranking audit followed;
implementation patch became safe.
```

That is not merely source navigation.

It is change-aware explanation.

## Relationship To Preservation

Preservation work asks what survives.

Git history preserves one kind of survival:

```text
change trace survives even when current files move on.
```

This helps with preservation failures such as:

- conclusion without discovery path;
- artifact without pressure;
- implementation without audit context;
- current state without previous state;
- navigation without sequence;
- understanding without temporal scaffold.

Git history is therefore relevant to preservation, but it is not preservation itself.

## Candidate Observations

A future git history observation source might emit observations such as:

```text
commit_observed
commit_subject
commit_timestamp
commit_author
commit_changed_file
commit_added_lines
commit_removed_lines
commit_parent
commit_touches_document
commit_touches_runtime
commit_touches_test
commit_touches_navigation
commit_reverts_commit
commit_associated_pr
```

These are candidate observations, not a schema proposal.

This document does not implement them.

## Candidate Derived Relationships

A later projection or read model might derive relationships such as:

```text
commit touches file
commit follows commit
commit precedes commit
commit creates document
commit modifies surface
commit accompanies test
commit follows audit
commit precedes implementation
```

These relationships would need careful authority boundaries.

A temporal relationship is not a causal relationship unless additional support exists.

## Important Non-Collapses

```text
Git history != current file content
Commit order != causal explanation
Commit subject != architectural truth
Changed file != behavior ownership
Patch shape != intent
Temporal proximity != dependency
PR merge != correctness
Documentation commit != authority change by itself
Implementation commit != semantic success by itself
```

These non-collapses are important because git history can be very persuasive while still being incomplete.

## Operator Questions Git History Could Help Answer

Git history observation would help Seed answer questions like:

```text
What changed recently?
What sequence led here?
Which audit came before this implementation?
Which files changed together?
When did this surface start appearing?
Was this behavior recently modified?
Did documentation or code come first?
Which commits form the current inquiry thread?
What was the previous state before this fix?
```

These questions are currently hard to answer from current repository content alone.

## Implementation Readiness Boundary

This reconciliation does not recommend immediate implementation.

Before implementation, Seed would need a design audit for:

- local git CLI versus GitHub API source authority;
- commit metadata normalization;
- patch-size limits;
- privacy and author metadata handling;
- branch and merge handling;
- PR association;
- cache strategy;
- observation volume control;
- how much diff content should be preserved;
- whether history should be sampled, bounded, or fully observed.

## Open Questions

- Should Seed observe local git history, remote GitHub history, or both?
- How should branch-specific history be scoped?
- How should merge commits be represented?
- Should commits be observations, events, evidence, or source records?
- How should commit messages be interpreted as language-bearing sources?
- How much diff content is safe and useful to preserve?
- Should git history drive inquiry lineage directly or only support lineage claims?
- How should rewritten history or rebases be represented?
- How should uncommitted working tree state relate to committed history?

## Final Reconciliation

Git history is a repository observation source distinct from current file observation.

Current files preserve present artifact state.

Git history preserves change sequence and temporal repository evidence.

Seed needs git history awareness to stop reconstructing work order from current documents alone.

However, git history must remain evidence, not authority.

The safe architectural boundary is:

```text
Repository contents show what exists now.
Git history shows how repository contents changed.
Inquiry lineage may use both,
but neither one alone proves why the work happened.
```

## Invariants

- Current file observation is not history observation.
- Commit order is not causal proof.
- Commit messages are language-bearing evidence, not authority by themselves.
- Changed-file relationships are not behavior ownership by themselves.
- Git history can support inquiry lineage but does not replace it.
- Sequence matters for explanation, preservation, and operator understanding.
- History-aware explanation must preserve uncertainty about intent and causality.
