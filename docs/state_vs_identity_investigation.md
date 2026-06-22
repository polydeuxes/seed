# State Versus Identity Investigation

## Central finding

Repository evidence supports a meaningful distinction:

```text
state
    -> what currently is

identity
    -> what remains the same thing
```

This distinction appears to underlie the earlier finding:

```text
preservation
    -> retained state

continuation
    -> retained identity across time
```

Repository evidence for state is substantially stronger than repository evidence for identity.

Identity exists in the repository, but usually appears at boundaries concerned with reconciliation, derivation, ownership, endpoint matching, principal matching, and continuity.

## State evidence

The strongest repository-visible state concepts are:

```text
unknown state

classification state

visibility state

capability state

diagnostic state
```

### Unknown state

Examples:

```text
unknown classification

unknown reachability

unknown capability state

unknown inquiry movement state
```

Observed through:

```text
classification_coverage
knowledge_reachability
capability_relationship
seed --inquiry-artifacts
```

Common property:

```text
current condition is visible
```

without needing identity continuity.

### Classification state

Examples:

```text
classified
unknown
partially classified
```

Observed through:

```text
classification_coverage
operational_surface_classification_audit
```

State changes are directly measurable.

### Visibility state

Examples:

```text
repository_visible
partially_visible
document_visible
human_interpreted
```

Observed through multiple inquiry investigations.

### Capability state

Examples:

```text
available
unavailable
unsupported
unknown
```

Observed through:

```text
capability_relationship
capability_needs
privilege_discovery
```

### Diagnostic state

Examples:

```text
consistent
unknown
warning
error
reachable
unreachable
```

Observed through:

```text
diagnostic_inventory
diagnostic_shape_audit
graph_issue_summary
knowledge_reachability
```

## Identity evidence

Identity appears most strongly in prior reconciliation work.

Examples repeatedly investigated:

```text
entity identity
principal identity
endpoint identity
measurement identity
```

### Entity identity

Observed through:

```text
entity_identity_derivation_reconciliation
```

Common concern:

```text
are these observations describing the same entity?
```

Identity is not primarily about state.

It is about sameness.

### Principal identity

Observed through:

```text
principal_identity_reconciliation
```

Common concern:

```text
does this principal remain the same principal?
```

State may change while identity remains.

### Endpoint identity

Observed through:

```text
prometheus_endpoint_identity_boundary_audit
prometheus_target_and_filesystem_identity_reconciliation
```

Common concern:

```text
does this endpoint observation refer to the same endpoint?
```

Identity determines whether measurements belong together.

### Measurement identity

Observed through:

```text
filesystem_measurement_identity_boundary_audit
```

Common concern:

```text
which measurements belong to the same measured thing?
```

Identity provides grouping continuity.

State provides the measured value.

## State change while identity remains

Repository evidence strongly supports this.

Examples:

### Endpoint identity

```text
endpoint remains same endpoint

availability changes

health changes

measurements change
```

Identity remains.

State changes.

### Principal identity

```text
principal remains same principal

capabilities change

ownership changes

relationships change
```

Identity remains.

State changes.

### Classification state

```text
entity remains same entity

classification changes
```

Identity remains.

State changes.

This is one of the strongest repository-backed patterns.

## Identity change while state remains

Repository evidence is weaker but supports candidate cases.

Examples:

### Endpoint replacement

```text
new endpoint
same observed state
```

Observed state may remain:

```text
healthy
reachable
providing service
```

while identity changes.

### Principal replacement

```text
new principal
same capability state
```

Capability state may remain unchanged.

Identity differs.

### Measurement reassociation

```text
same measurement value
new identity assignment
```

Identity changes.

State remains.

These cases motivated identity reconciliation work.

If state alone were sufficient, identity reconciliation would not be necessary.

## Preservation and state

Repository evidence strongly supports:

```text
preservation
    operates primarily on state
```

Examples:

```text
unknown state preserved

classification state preserved

visibility state preserved

capability state preserved

support context preserved
```

Preservation asks:

```text
what remained unchanged?
```

That is fundamentally state-oriented.

## Continuation and identity

Repository evidence partially supports:

```text
continuation
    operates primarily on identity
```

Examples:

```text
same inquiry later

same operator later

same entity later

same endpoint later
```

Continuation asks:

```text
is this still the same thing?
```

That is fundamentally identity-oriented.

## Counterexamples

### State preserved while identity changes

Examples:

```text
new endpoint
same state

new principal
same capability state

new measurement owner
same measurement value
```

This demonstrates:

```text
state
    !=
identity
```

### Identity preserved while state changes

Examples:

```text
same endpoint
new measurements

same principal
new capabilities

same entity
new classification
```

This demonstrates:

```text
identity
    !=
state
```

### Apparent state that is actually identity

Examples:

```text
same endpoint
```

This appears descriptive.

But it is actually an identity claim.

### Apparent identity that is actually state

Examples:

```text
healthy endpoint
reachable endpoint
classified endpoint
```

These appear entity-like.

But they are state descriptions.

## State versus identity

### State

Shape:

```text
current condition
```

Examples:

```text
unknown
classified
reachable
healthy
supported
visible
```

### Identity

Shape:

```text
sameness across observations
```

Examples:

```text
same endpoint
same principal
same entity
same measurement target
```

### Visibility

Visibility behaves more like state.

```text
repository_visible
partially_visible
document_visible
```

are conditions.

### Classification

Classification behaves more like state.

### Ownership

Ownership behaves more like state.

Ownership may change while identity remains.

### Measurement

Measurement contains both.

```text
measurement identity
```

answers:

```text
whose measurement?
```

while:

```text
measurement state
```

answers:

```text
what value?
```

## Historical perspective

Recent investigations increasingly separated:

```text
preservation
```

from:

```text
continuation
```

The deeper distinction appears to be:

```text
state
```

versus:

```text
identity
```

because:

```text
preservation
    focuses on retained state

continuation
    focuses on retained identity
```

This distinction explains why preservation repeatedly grounded itself in implementation-backed evidence.

State is easier to observe.

Identity generally requires reconciliation, matching, derivation, continuity, or temporal reasoning.

## Supported conclusions

1. Repository evidence supports state as a distinct concept.
2. Repository evidence supports identity as a distinct concept.
3. State and identity are not equivalent.
4. State can change while identity remains.
5. Identity can change while state remains.
6. Preservation operates primarily on state.
7. Continuation operates primarily on identity.
8. State and identity appear to be the deeper concepts underlying the preservation versus continuation distinction.
9. State evidence is stronger and more directly repository-visible than identity evidence.
10. Identity evidence most often appears in reconciliation and continuity investigations.

## Unsupported conclusions

- State and identity are equivalent.
- Preservation requires identity.
- Continuation requires preserved state.
- State uniquely determines identity.
- Identity uniquely determines state.
- Visibility is an identity concept.
- Classification is an identity concept.
- Ownership is an identity concept.

## Open questions

- What is the minimal repository-visible evidence required for identity?
- Can identity become repository-visible without reconciliation?
- Is continuity fundamentally retained identity?
- Is preservation fundamentally retained state?
- Are there relationship families beyond state-oriented and identity-oriented families?
- Can artifact relationships emerge first through state and later through identity?

## Acceptance answers

### What distinguishes state from identity?

```text
state
    -> current condition

identity
    -> sameness across observations
```

### Can state change while identity remains?

Yes.

Strongly supported.

### Can identity change while state remains?

Yes.

Supported by reconciliation-motivating examples.

### Does preservation primarily operate on state?

Yes.

### Does continuation primarily operate on identity?

Partially yes.

### Are state and identity the deeper concepts underlying the preservation and continuation distinction?

Repository evidence currently supports that interpretation.
