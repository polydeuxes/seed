# Capability Verification Promotion Reconciliation

## Purpose

Recent capability work established three distinct read-only surfaces:

```text
package_installed evidence
    ↓
capability candidate
```

```text
local PATH filesystem metadata
    ↓
verification evidence
```

```text
capability_verified facts
    ↓
verification status inspection
```

This reconciliation investigates the missing boundary:

```text
capability candidate
    +
verification evidence
    ↓
capability_verified
```

It is documentation-only.

It does not implement runtime behavior, verification promotion, schemas, policy, capability selection, planning, provider selection, tool invocation, command execution, SSH execution, remote execution, or autonomy.

## Evidence Basis

This reconciliation follows from repository work around:

- Capability Observation v1;
- capability verification inspection;
- verification-evidence acquisition;
- capability authority and execution boundaries;
- candidate request and routing preservation;
- source type and candidate family production;
- input inspection boundaries;
- observation, evidence, fact promotion, and claim support;
- existing `capability_verified` facts and capability inventory surfaces.

Repository authority wins if this reconciliation diverges from higher-authority documents.

## Central Question

What evidence and authority are required to promote:

```text
capability candidate
    +
verification evidence
```

into:

```text
capability_verified
```

without collapsing into capability selection, permission, policy approval, or execution?

## Current Shape

The current capability chain is:

```text
package_installed fact
    ↓
capability candidate
    ↓
verification evidence inspection
    ↓
capability verification inspection
```

Existing `capability_verified` facts are consumed by verification inspection, but the repository has not yet reconciled what creates them.

That leaves a visible gap:

```text
capability candidate
    +
verification evidence
    ↓
???
    ↓
capability_verified
```

## Central Finding

Capability verification promotion is a separate authority boundary.

It should answer:

```text
Is there enough supported verification evidence to create or accept a capability_verified fact?
```

It should not answer:

```text
Should this capability be selected?
```

It should not answer:

```text
May Seed execute this capability?
```

It should not answer:

```text
Has the operator approved an action?
```

## Promotion Is Not Inspection

Verification evidence inspection preserves evidence such as:

```text
binary_path_observed: /usr/bin/ssh
```

Verification status inspection reports whether a candidate is backed by an existing `capability_verified` fact.

Promotion would be the act of creating or accepting that `capability_verified` fact under a support and authority boundary.

Therefore:

```text
Verification Evidence != Capability Verified
Verification Inspection != Verification Promotion
Capability Verified != Capability Selection
Capability Verified != Execution Authority
```

## Candidate Evidence Versus Verification Evidence

Candidate evidence may be weak but useful:

```text
package_installed = openssh-client
```

This can support preserving:

```text
candidate: ssh_client
```

Verification evidence should be stronger or more direct:

```text
binary_path_observed = /usr/bin/ssh
```

This may support verifying local availability.

But even stronger verification evidence still does not become permission.

```text
Observed Binary != Permission
Verified Capability != Authorization
```

## Example: SSH

Possible chain:

```text
package_installed=openssh-client
    ↓
capability candidate: ssh_client

binary_path_observed=/usr/bin/ssh
    ↓
verification evidence for ssh_client

promotion boundary accepts support
    ↓
capability_verified: ssh_client
```

The result only means:

```text
Seed has sufficient support that an SSH client capability is locally available.
```

It does not mean:

```text
Seed may SSH to a target.
Seed may run remote commands.
Seed has credentials.
Seed has operator approval.
Policy approved an action.
```

## Authority Needed For Promotion

Capability verification promotion appears to require at least:

```text
candidate identity
supporting candidate evidence
verification evidence
source/provenance
verification rule or rationale
freshness/staleness handling
explicit boundary notes
```

This reconciliation does not define a schema or implementation.

It only identifies that promotion requires more than candidate existence and more than raw evidence display.

## Relationship To Fact Promotion

`capability_verified` is fact-like, but capability verification promotion is not ordinary assertion copying.

It must preserve:

```text
support provenance
verification rationale
candidate linkage
non-execution boundary
staleness or freshness behavior
```

This is consistent with broader repository findings:

```text
Observation != Fact
Evidence != Authority By Itself
Candidate != Promotion
Promotion != Execution
```

## Relationship To Capability Inventory

Capability verification inspection already consumes capability inventory state derived from projected `capability_verified` facts.

That is downstream of promotion.

The inventory should not be treated as the source of promotion authority by itself.

Preferred shape:

```text
verification promotion
    ↓
capability_verified fact
    ↓
capability inventory / verification inspection
```

Rejected collapse:

```text
capability inventory
    ↓
authority to execute
```

## Strongest Risks Of Collapse

The strongest risks are:

```text
candidate exists -> capability_verified
```

without verification evidence;

```text
binary observed -> capability_verified
```

without an explicit promotion boundary;

```text
capability_verified -> capability selected
```

without task context;

```text
capability_verified -> execution permitted
```

without policy/operator authority;

```text
verification evidence -> tool invocation
```

without execution review.

## Safeguards

Any future promotion surface should preserve these constraints:

```text
Capability Candidate != Capability Verified
Verification Evidence != Capability Verified
Capability Verified != Capability Selection
Capability Verified != Execution Authority
Capability Verified != Execution Decision
Capability Verified != Tool Invocation
Observed Binary != Permission
Verified Capability != Operator Approval
```

## Implementation Implications

If implementation follows later, the safest slice would be read-only or explicitly bounded promotion inspection before actual fact creation.

A possible inspection-only output could say:

```text
candidate: ssh_client
promotion_readiness: supported
candidate_support: package observed
verification_support: binary path observed
would_promote: capability_verified ssh_client
boundary: no selection, no execution
```

Actual promotion into facts should only follow if repository authority supports it.

## Non-Goals

This reconciliation does not:

- implement promotion;
- define promotion schemas;
- define scoring;
- define provider selection;
- define execution authority;
- define policy gates;
- define SSH behavior;
- define remote-command execution;
- propose autonomy.

## Final Finding

The missing boundary is capability verification promotion.

Capability candidates and verification evidence can make a capability verification claim supportable, but they do not themselves create a verified capability without an explicit promotion boundary.

The safe chain is:

```text
observed evidence
    ↓
capability candidate
    ↓
verification evidence
    ↓
capability verification promotion
    ↓
capability_verified
    ↓
future capability selection / execution review
```

not:

```text
observed evidence
    ↓
execution
```
