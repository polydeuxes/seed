# Tool Presence To Capability Shape Audit

## Purpose

This audit investigates the boundary between observed software artifacts and capability knowledge.

Triggering question:

```text
When does observed software become a capability candidate?
```

This audit is not an implementation proposal, execution proposal, authority proposal, adapter implementation, or workflow design.

## Central Observation

Current repository work contains strong observation, evidence, fact, relationship, and capability boundaries.

However, an unresolved transition exists between:

```text
software observed on a system
```

and:

```text
capability knowledge about what that software can do
```

## Candidate Example: SSH

Observed:

```text
/usr/bin/ssh exists
```

Potential additional observations:

```text
ssh -V
ssh --help
man ssh
package metadata
```

These observations reveal increasing amounts of information.

## Distinction: Presence vs Shape

Observation:

```text
ssh exists
```

supports:

```text
SSH client software appears present.
```

It does not support:

```text
SSH can execute arbitrary remote actions.
```

The second statement requires understanding capability shape.

## Capability Shape Candidate

Observed documentation, help text, manual pages, or structured metadata may reveal:

```text
accepted inputs
accepted options
transport role
authentication parameters
output forms
error forms
```

These appear closer to capability-shape evidence than simple binary presence.

## Emerging Boundary

The investigation suggests:

```text
Tool Presence
        !=
Capability Shape
```

and:

```text
Capability Shape
        !=
Execution Authority
```

## Candidate Observation Chain

Observed tool:

```text
ssh binary
```

Observed documentation:

```text
help text
manual text
usage examples
```

Potentially supports:

```text
capability candidate:
    transport.ssh.client
```

with observed properties such as:

```text
host parameter
user parameter
identity parameter
remote command parameter
```

The audit does not determine how these should be modeled.

Only that the observations appear different from simple presence.

## Strongest Finding

The strongest finding is:

```text
Observed software presence appears insufficient to describe capability shape.
```

Additional observations appear necessary.

## Strongest Distinctions

```text
Tool Presence
        !=
Capability Shape

Capability Shape
        !=
Target Reachability

Target Reachability
        !=
Execution Authority

Execution Authority
        !=
Execution Result
```

## Candidate Preservation Question

Recent repository work increasingly preserves:

```text
what can be observed
```

rather than:

```text
what is assumed
```

This suggests capability shape should emerge from observation rather than hard-coded assumptions where practical.

## Unresolved Questions

```text
What observations are sufficient to infer capability shape?

Should manuals and help text be observable sources?

How should capability shape differ from capability authority?

How should capability shape differ from capability ownership?

Can capability shape be derived from source observation for local tools?
```

## Final Finding

The next boundary after software presence appears to be capability-shape observation.

Observed tools may become capability candidates only after sufficient evidence exists describing what operations they support.

The audit leaves authority, execution, routing, and policy decisions intentionally out of scope.
