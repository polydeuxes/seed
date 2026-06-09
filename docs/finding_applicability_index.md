# Finding Applicability Index

## Purpose

A recurring finding across audits, reconciliations, operator trials, and implementation work is that the repository increasingly contains valuable findings, but there is no consistent way to answer:

```text
When is this finding useful?
```

Traditional document metadata helps navigation.

```text
topic
status
authority
category
```

Those fields help a reader locate a document.

They do not help Seed determine which findings should influence a decision, explanation, reconciliation, review, or capability proposal.

## Core Idea

Separate:

```text
Navigation Metadata
```

from:

```text
Applicability Metadata
```

Navigation metadata helps find a document.

Applicability metadata helps determine when a finding should be considered.

## Example

Finding:

```text
Imports are not calls.
```

Navigation metadata:

```text
topic: relationship evidence
status: preserved finding
```

Applicability metadata:

```text
helps_when:
  - evaluating behavior claims
  - relationship reconciliation
  - repository review

guards_against:
  - imports -> calls
  - imports -> ownership
  - imports -> behavior

related_findings:
  - behavior requires behavior evidence
  - evidence before capability
```

## Candidate Applicability Fields

```text
helps_when
prerequisites
guards_against
related_findings
supersedes
supported_by
```

These fields should remain descriptive rather than executable.

The goal is retrieval and reasoning support, not policy execution.

## Observed Motivation

Several recurring findings emerged during repository work:

```text
Evidence before capability.

Behavior requires behavior evidence.

Imports are not calls.

Observation and mutation are different risk classes.

Source authority is not content authority.

Missing capability should be surfaced before compensation.

Operator pain is often a better prioritization signal than architecture speculation.
```

These findings are valuable beyond the original documents that produced them.

The challenge is discovering when they should be recalled.

## Potential Future Use

A future system could answer:

```text
I am evaluating a behavior claim.
What findings are relevant?
```

by retrieving applicable findings rather than searching entire documents.

Likewise:

```text
I am reviewing a proposed ownership claim.
What guardrails apply?
```

could surface relevant findings without requiring a complete repository review.

## Non-Goals

This proposal does not introduce:

```text
Knowledge graph requirements
Vector search requirements
New evidence types
Runtime behavior
Policy engines
```

The proposal is purely about preserving and retrieving architectural findings.

## Current Conclusion

A Finding Applicability Index appears to be a lightweight way to preserve one of the most valuable assets emerging from Seed:

```text
Not just what was learned.

But when that learning should be applied.
```
