# Natural Language Request Routing Audit

## Purpose

This document audits how Seed should treat natural-language operator requests
that appear to ask for existing capability surfaces.

The triggering examples were:

```text
Show me state summary
```

and:

```text
Show me summary
```

The question is whether Seed should treat these as direct commands, aliases, or
language-derived candidates that must pass through interpretation, routing,
capability selection, ambiguity handling, and execution authority.

This is an audit. It is not an implementation proposal, routing schema,
command vocabulary, capability ontology, or natural-language parser design.

## Evidence Basis

This audit is grounded in recent repository language and capability boundaries,
including:

- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/language_candidate_routing_and_promotion_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/candidate_meaning_and_ambiguity_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/capability_verification_reconciliation.md`
- `docs/execution_status_and_operator_feedback_reconciliation.md`

Repository authority wins if this audit diverges from any referenced
reconciliation.

## Central Finding

Natural language should produce candidates, not commands.

A command may eventually emerge after interpretation, routing, capability
selection, ambiguity handling, and execution decision. But the language act
itself should not be collapsed into execution.

Preferred chain:

```text
Communicative Act
    ↓
Language Observation
    ↓
Interpretation
    ↓
Candidate Request
    ↓
Routing
    ↓
Capability Selection
    ↓
Execution Decision
    ↓
Execution
```

Rejected collapse:

```text
Language
    ↓
Nearest Capability
    ↓
Execution
```

## Example: "Show Me State Summary"

The phrase:

```text
Show me state summary
```

has a relatively strong candidate interpretation:

```text
candidate request: display state-summary surface
candidate route: state summary read-model / operator surface
ambiguity: low
```

This still does not mean interpretation is execution. It means the request may
be routed to the state-summary capability or surface with high confidence,
assuming the capability exists, is available, and is safe to execute.

## Example: "Show Me Summary"

The phrase:

```text
Show me summary
```

is weaker.

Possible meanings include:

```text
state summary
integrity summary
impact summary
repository summary
handoff summary
execution-status summary
conversation summary
future summary surfaces not yet implemented
```

Therefore the phrase should not be hard-coded as an alias for state summary.

A safer interpretation is:

```text
candidate request: display a summary
candidate route: summary-capability selection / ambiguity handling
ambiguity: medium or high
```

## Capability Availability Tension

A tempting rule is:

```text
if only one summary capability exists,
then "summary" means that capability
```

This is unsafe as an architectural default.

Capability availability does not prove operator intent.

```text
available capability != intended meaning
```

However, capability inventory may be used as part of response selection.

For example, if only one summary surface exists, Seed may respond:

```text
I only have state summary available. Showing state summary.
```

or, in stricter ambiguity mode:

```text
I found one summary surface: state summary. Should I show that?
```

The difference depends on execution authority, risk, interface mode, and
operator preference. It should not be implemented as a silent alias collapse.

## Ambiguity Boundary

Ambiguity is not failure.

Ambiguity should be representable and explainable.

For `Show me summary`, Seed should be able to preserve a candidate set such as:

```text
candidate targets:
  - state_summary
  - integrity_summary
  - impact_summary
  - repository_summary
```

If the candidate set has more than one plausible target, execution should either
ask for clarification or make an explicit bounded assumption.

The assumption should be visible:

```text
Assuming state summary because it is the only available summary surface.
```

This is different from silently treating `summary` as a CLI alias.

## Routing Boundary

Routing answers:

```text
which architectural boundary should consider this candidate?
```

Routing does not answer:

```text
what action should execute?
```

Therefore `Show me summary` may route to a capability-selection boundary rather
than directly to the state-summary execution path.

## Execution Boundary

Execution should require at least:

```text
candidate request
    ↓
routed boundary
    ↓
selected capability or surface
    ↓
sufficient confidence / authority
    ↓
execution
```

A matched capability is not itself an execution decision.

```text
candidate != command
matched capability != accepted execution
```

## Relationship To CLI Commands

CLI flags remain explicit operator commands.

```text
seed --state-summary
```

is different from:

```text
Show me summary
```

The first is already a structured command surface. The second is a communicative
act that must be interpreted.

Natural-language routing should not be implemented as an expanding pile of CLI
aliases. CLI commands can be execution targets, but natural language should pass
through interpretation and routing first.

## Relationship To Current Summary Surfaces

As Seed grows, more summary-like surfaces are likely:

```text
state summary
integrity summary
impact overview
repository summary
execution-status summary
handoff summary
```

Every new summary surface increases ambiguity pressure around the word
`summary`.

This reinforces the finding that hard-coded natural-language aliases are fragile.

## Strongest Failure Mode

The strongest failure mode is:

```text
language phrase
    ↓
nearest known capability
    ↓
execution
```

This lets capability availability become authority over operator intent.

It also makes future capability growth dangerous because adding a new capability
can silently change what old language means.

## Strongest Safe Behavior

The strongest safe behavior is:

```text
language phrase
    ↓
meaning candidates
    ↓
capability candidates
    ↓
ambiguity/confidence decision
    ↓
explicit execution or clarification
```

For high-confidence phrases like `show me state summary`, execution may proceed
if the surface is available and safe.

For underspecified phrases like `show me summary`, Seed should preserve ambiguity
or make an explicit assumption based on available capability inventory.

## Architectural Invariants

```text
Language Observation != Interpretation
Interpretation != Routing
Routing != Capability Selection
Capability Selection != Execution
Candidate != Command
Matched Capability != Accepted Execution
Available Capability != Intended Meaning
CLI Alias != Natural-Language Meaning
Ambiguity != Failure
Clarification != Rejection
```

## Implementation Implications

If implementation follows later, the safest initial slice is not broad natural
language command execution.

A bounded implementation should likely:

1. Observe the language act.
2. Produce candidate request records or in-memory decision objects.
3. Route only a very small set of high-confidence requests.
4. Represent ambiguous requests explicitly.
5. Keep execution behind the existing capability/execution authority boundary.

Potential acceptance examples:

```text
"Show me state summary"
  -> high-confidence state-summary candidate

"Show me summary"
  -> ambiguous summary candidate, or explicit assumption if only one available
     summary surface exists

"Show me impact summary"
  -> impact-summary candidate if such a surface exists
```

## Non-Goals

This audit does not:

- define a natural-language parser;
- define a command grammar;
- define aliases;
- implement routing;
- implement execution;
- modify CLI behavior;
- modify capability inventory;
- change state-summary semantics;
- create schema.

## Final Finding

Seed should not hard-code `summary` as an alias for `state summary`.

`Show me state summary` and `Show me summary` should produce different
candidate-routing outcomes because the first names a specific surface while the
second names a broader class of possible surfaces.

The safest architectural path is to treat natural language as communicative-act
observation, derive candidate meaning, route to capability-selection boundaries,
and execute only when ambiguity and authority conditions are satisfied.
