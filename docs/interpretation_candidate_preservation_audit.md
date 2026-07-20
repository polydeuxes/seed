# Interpretation Candidate Preservation Audit

## Purpose

Recent audits established two findings:

```text
Natural language should produce candidates, not commands.
```

and:

```text
capability selection behavior, and execution surfaces,
but preserves little after interpretation occurs.
```

This audit investigates:

```text
What survives interpretation?
```

This is an audit.

Not a reconciliation.

Not an implementation proposal.

Not a schema proposal.

## Evidence Basis

Reviewed findings from:

- natural_language_request_routing_audit.md
- natural_language_execution_path_inventory_audit.md
- language_candidate_routing_and_promotion_reconciliation.md
- candidate_meaning_and_ambiguity_reconciliation.md
- operator_intent_question_and_claim_interface_reconciliation.md

## Triggering Observation

Repository work increasingly preserves:

```text
observations
relationships
lineage
continuation state
active edge
```

However the inventory audit suggests that language interpretation may currently compress meaning into a decision without preserving candidate alternatives.

## Example

Input:

```text
Show me summary
```

Possible interpretations:

```text
state summary
integrity summary
impact summary
repository summary
```

After execution or classification, little evidence may remain that these alternatives ever existed.

## Candidate Preservation Question

Interpretation appears capable of producing:

```text
possible meanings
possible targets
possible capabilities
confidence judgments
```

The audit question is whether those survive.

## Observation

Many repository surfaces preserve:

```text
what was observed
```

Language processing appears closer to:

```text
what was selected
```

than:

```text
what was considered
```

## Distinction

```text
Interpretation Result
        !=
Interpretation Space
```

The result is the selected outcome.

The interpretation space contains the candidates that may have existed before selection.

## Ambiguity Pressure

Ambiguity appears difficult to preserve when only final selections survive.

Without candidate preservation:

```text
ambiguity
    ↓
selection
    ↓
ambiguity disappears
```

This does not prove ambiguity was resolved.

Only that it was no longer represented.

## Relationship To Capability Shape

A similar pattern appeared in the capability-shape audit.

There:

```text
tool presence
    ↓
human understanding
```

hid missing capability-shape knowledge.

Here:

```text
language
    ↓
human understanding
```

may hide missing candidate-preservation knowledge.

## Strongest Finding

The strongest finding is:

```text
The repository currently preserves decisions better than candidate spaces.
```

## Strongest Tension

```text
selection
        vs
preservation
```

Many systems optimize for arriving at an answer.

Recent Seed investigations often optimize for preserving how answers became possible.

## Unresolved Questions

```text
Should candidate meanings survive interpretation?

Should ambiguity be preservable?

Should routing preserve rejected candidates?

Is candidate preservation transient or durable?

What survives a clarification interaction?
```

## Final Finding

The natural-language execution-path inventory suggests the largest missing preservation surface is not execution.

It is the space between:

```text
interpretation
```

and:

```text
selection
```

where possible meanings, ambiguity, and alternative candidate routes may exist briefly and then disappear.

The audit leaves unresolved whether those candidates should be preserved, how they should be represented, and whether preservation belongs to observation, routing, capability selection, or another architectural boundary.