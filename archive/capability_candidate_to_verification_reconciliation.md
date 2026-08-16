# Capability Candidate To Verification Reconciliation

## Purpose

Recent implementation added Capability Observation v1 as capability-candidate preservation.

The new shape is:

```text
observable projected package evidence
    ↓
capability candidates
    ↓
read-only inspection
```

This reconciliation investigates the next boundary:

```text
capability candidate
    ↓
capability verification
```

It is documentation-only.

It does not implement runtime behavior, execution, planning, schemas, policy, tool invocation, provider selection, or autonomy.

## Evidence Basis

This reconciliation is grounded in repository work around:

- capability authority and execution boundaries;
- candidate request and routing preservation;
- source type and candidate family production;
- input inspection boundaries;
- observation, evidence, fact promotion, and claim support;
- capability candidate preservation;
- existing capability inventory and `capability_verified` facts.

Repository authority wins if this reconciliation diverges from higher-authority documents.

## Central Question

What evidence justifies moving from:

```text
capability candidate
```

to:

```text
verified capability
```

without collapsing into execution authority?

## Central Finding

Capability verification should be treated as a support-strength boundary between candidate preservation and future capability selection.

It is not execution.

It is not permission.

It is not planning.

It is not provider selection.

Preferred shape:

```text
observed evidence
    ↓
capability candidate
    ↓
verification evidence
    ↓
verified capability
    ↓
future selection / review / execution boundaries
```

Rejected collapse:

```text
observed package
    ↓
capability exists
    ↓
execute
```

## Candidate Versus Verified Capability

A capability candidate answers:

```text
What capability may be present based on observed evidence?
```

A verified capability answers:

```text
What capability is sufficiently supported as available under the verification boundary?
```

Neither answer is:

```text
May Seed execute it now?
```

That remains a separate execution-authority question.

## Example: SSH

Observed package evidence:

```text
package_installed = openssh-client
```

may support:

```text
candidate: ssh_client
```

Additional verification evidence might include:

```text
ssh binary exists
ssh -V succeeds
ssh executable is on PATH
adapter contract exists
local invocation shape is known
```

These pieces of evidence differ in strength.

None of them alone grants permission to connect to a host or run a remote command.

## Verification Is Not Execution Authority

```text
Verified Capability != Execution Authority
```

A verified SSH client may mean:

```text
Seed has sufficient evidence that an SSH client is available locally.
```

It does not mean:

```text
Seed may SSH into example_host_b.
```

It does not mean:

```text
Seed may run commands remotely.
```

It does not mean:

```text
The operator approved this action.
```

## Verification Evidence Strength

Capability verification may need evidence stronger than candidate preservation.

Possible support levels:

```text
package observed
binary path observed
binary invocation succeeds
version output observed
adapter contract exists
provider registered
local dry inspection succeeds
```

This reconciliation does not define a schema or required scoring model.

It only observes that verification evidence appears stronger and more specific than candidate evidence.

## Relationship To Existing Capability Inventory

The repository already has capability-related surfaces such as capability inventory and `capability_verified` facts.

Capability Candidate Observation v1 intentionally remained separate from those surfaces.

That distinction is correct.

```text
Capability Candidate != Capability Verified Fact
```

The unresolved question is what verification boundary promotes, derives, or supports `capability_verified` facts.

## Authority Boundary

Authority appears in at least three separate places:

```text
candidate authority:
    evidence may support preserving a candidate

verification authority:
    evidence may support saying the capability is available

execution authority:
    policy/operator/context may authorize invoking the capability
```

These must not collapse.

## Strongest Similarities To Other Candidate Families

Capability candidates follow the same broad pattern seen elsewhere:

```text
source evidence
    ↓
candidate family
    ↓
promotion / verification boundary
```

Comparable examples:

```text
source code
    ↓
relationship candidates
    ↓
relationship promotion
```

```text
operator language
    ↓
request candidates
    ↓
routing preservation
```

```text
package evidence
    ↓
capability candidates
    ↓
capability verification
```

## Strongest Distinctions

Capability verification differs from fact promotion because it concerns operational availability, not merely a normalized assertion.

Capability verification differs from execution authority because it does not authorize action.

Capability verification differs from capability selection because it does not choose a capability for a task.

Capability verification differs from adapter implementation because it does not define how to invoke the capability.

## Risks Of Collapse

The strongest risks are:

```text
package installed -> verified capability
```

without stronger evidence;

```text
verified capability -> permission
```

without execution authority;

```text
adapter exists -> provider selected
```

without task context;

```text
capability candidate -> tool invocation
```

without policy and operator boundary.

## Safeguards

Existing repository boundaries already provide safeguards:

```text
Observation != Truth
Evidence != Authority By Itself
Candidate != Fact
Candidate != Capability
Verified Capability != Execution Authority
Capability Presence != Permission
Execution Decision != Tool Invocation
```

Capability verification should preserve and extend those safeguards rather than bypass them.

## Implementation Implications

If implementation follows later, the safest slice would remain read-only.

A bounded implementation could inspect capability candidates and produce verification status such as:

```text
candidate: ssh_client
verification: unverified
reason: package observed but binary invocation not observed
```

or:

```text
candidate: ssh_client
verification: verified
support: package observed + binary path observed + version output observed
```

without selecting a provider, planning an action, or executing an operator command.

## Non-Goals

This reconciliation does not:

- define a verification schema;
- implement verification;
- define scoring;
- define provider selection;
- define execution authority;
- define policy gates;
- define SSH behavior;
- define remote-command execution;
- propose autonomy.

## Final Finding

Capability candidate preservation is not enough to claim a verified capability.

Capability verification appears to require additional support that the capability is actually available under a defined verification boundary.

Even then, verified capability remains downstream of evidence and upstream of capability selection or execution authority.

The safe chain is:

```text
observed evidence
    ↓
capability candidate
    ↓
capability verification
    ↓
future capability selection / execution review
```

not:

```text
observed evidence
    ↓
execution
```
