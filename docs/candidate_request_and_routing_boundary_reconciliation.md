# Candidate Request And Routing Boundary Reconciliation

## Purpose


They also found missing explicit stages for:

```text
communicative acts
language observations
interpretation objects
candidate request sets
routing boundaries
standalone capability selection
execution-decision artifacts
bounded assumptions
capability-ambiguity clarification lifecycles
```

This reconciliation defines the architectural boundary between candidate requests, routing, capability selection, and execution decision.

It is documentation-only.

It does not implement runtime behavior, define schemas, create command aliases, or add execution authority.

## Evidence Basis

This reconciliation follows from:

- `docs/natural_language_request_routing_audit.md`
- `docs/natural_language_execution_path_inventory_audit.md`
- `docs/interpretation_candidate_preservation_audit.md`
- `docs/language_candidate_routing_and_promotion_reconciliation.md`
- `docs/candidate_meaning_and_ambiguity_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`

Repository authority wins if this document diverges from higher-authority reconciliations.

## Central Finding

A candidate request is the preserved possibility that an operator communicative act may be asking for some kind of response, surface, information, or action.

It is not yet a command.

It is not yet a selected capability.

It is not yet an execution decision.

Preferred shape:

```text
Communicative Act
    ↓
Language Observation
    ↓
Interpretation
    ↓
Candidate Request Set
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

## Candidate Request

A candidate request answers:

```text
What might the operator be asking for?
```

Examples:

```text
show state summary
show a summary
explain why nginx is down
run uptime on example_host_b
find where StateProjector is defined
```

A candidate request may contain uncertainty.

For example:

```text
Show me summary
```

may produce candidate requests or target candidates such as:

```text
state summary
integrity summary
impact summary
repository summary
execution-status summary
conversation summary
```

The important point is that these alternatives can exist before selection.

## Candidate Request Is Not A Command

```text
Candidate Request != Command
```

A candidate request is interpretation output.

A command is accepted executable intent under an appropriate interface and authority boundary.

The phrase:

```text
Show me state summary
```

may become a high-confidence candidate for the state-summary surface.

But the candidate itself is not the command execution.

## Routing

Routing answers:

```text
Which architectural boundary should consider this candidate?
```

Examples:

```text
state-summary surface
impact surface
source-navigation query
capability-selection boundary
clarification boundary
execution proposal boundary
```

Routing does not answer:

```text
Which capability has been selected?
```

and does not answer:

```text
Should execution occur?
```

Therefore:

```text
Routing != Capability Selection
Routing != Execution Decision
```

## Capability Selection

Capability selection answers:

```text
Which available capability, if any, could satisfy the routed candidate?
```

This depends on capability inventory, available providers, adapter compatibility, current state, and safety constraints.

But:

```text
Available Capability != Intended Meaning
Selected Capability != Execution Authority
```

A capability may be available and still not be what the operator meant.

A capability may be selected and still not be authorized to execute.

## Execution Decision

Execution decision answers:

```text
Should the selected capability actually be invoked now?
```

This is where authority, policy, approval, risk, and confirmation boundaries apply.

Execution decision is downstream of interpretation, routing, and capability selection.

It must not be collapsed into them.

```text
Capability Selection != Execution Decision
Candidate Request != Execution Decision
```

## Example: Show Me State Summary

Input:

```text
Show me state summary
```

Possible flow:

```text
candidate request:
    display state-summary surface

routing:
    state-summary surface boundary

capability selection:
    state-summary read-model renderer

execution decision:
    safe read-only display; may proceed if interface policy allows
```

This is a relatively low-ambiguity case.

Even here, the chain remains conceptually distinct.

## Example: Show Me Summary

Input:

```text
Show me summary
```

Possible candidate targets:

```text
state summary
integrity summary
impact summary
repository summary
execution-status summary
conversation summary
```

Routing may choose:

```text
summary ambiguity / capability-selection boundary
```

rather than directly choosing state summary.

If only one summary capability exists, Seed may make an explicit bounded assumption:

```text
I only have state summary available. Showing state summary.
```

or ask for clarification:

```text
Which summary do you want: state, integrity, impact, or repository?
```

But it should not silently define:

```text
summary == state summary
```

## Bounded Assumptions

A bounded assumption is an explicit bridge from ambiguity to action.

It should preserve that uncertainty existed.

Example:

```text
Assuming state summary because it is the only available summary surface.
```

This is safer than a hidden alias because it does not erase ambiguity.

```text
Bounded Assumption != Alias
Bounded Assumption != Proof Of Intent
```

## Clarification

Clarification is a valid routing outcome.

Ambiguity does not mean the system failed.

```text
Ambiguity != Failure
Clarification != Rejection
```

Clarification preserves the boundary between possible meaning and selected meaning.

## Relationship To Existing Implementation

The inventory audit found existing implementation surfaces around:

```text
raw user-message capture
context composition
structured decision kinds
runtime decision routing
tool-intent guard behavior
validation and policy gates
ToolExecutor
```

These are useful surfaces.

However, the missing preservation boundary is the candidate space between interpretation and selection.

The current implementation may arrive at decisions without preserving alternatives considered along the way.

This reconciliation identifies the missing conceptual boundary before implementation attempts to fill it.

## Strongest Failure Mode

The strongest failure mode is:

```text
language phrase
    ↓
nearest matching tool
    ↓
execution
```

This allows capability availability to become authority over operator meaning.

It also makes future capability growth dangerous because adding a capability may change how old language routes.

## Architectural Invariants

```text
Communicative Act != Candidate Request
Language Observation != Interpretation
Interpretation != Routing
Candidate Request != Command
Candidate Request != Capability
Candidate Request != Execution Decision
Routing != Capability Selection
Capability Selection != Execution Decision
Available Capability != Intended Meaning
Selected Capability != Execution Authority
Bounded Assumption != Alias
Ambiguity != Failure
Clarification != Rejection
```

## Non-Goals

This reconciliation does not:

- define a schema;
- implement candidate objects;
- implement natural-language routing;
- implement execution;
- create aliases;
- change CLI commands;
- modify capability inventory;
- modify policy gates;
- define UI behavior;
- define audio behavior.

## Implementation Implications

If implementation follows later, the safest first slice is non-executing.

A bounded implementation could test:

```text
"show me state summary"
    -> high-confidence state-summary candidate

"show me summary"
    -> ambiguous summary candidate set

"show me impact summary"
    -> impact-summary candidate if surface exists
```

without invoking capabilities.

This would validate candidate preservation before execution authority enters the path.

## Final Finding

Candidate requests preserve possible operator meaning after interpretation and before capability selection.

Routing chooses the architectural boundary that should consider those candidates.

Capability selection chooses a possible satisfying capability.

Execution decision determines whether anything should actually be invoked.

These are separate boundaries.

Keeping them separate prevents natural language from collapsing into nearest-tool execution while still allowing Seed to become more useful as its capability inventory grows.
