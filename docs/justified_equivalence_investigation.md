# Justified Equivalence Investigation

## Purpose and boundary

This investigation asks what repository evidence is sufficient to justify treating two observations, identifiers, subjects, or artifacts as the same thing.

This is investigation only.

It does not implement merging, graph collapse, identity systems, equivalence systems, Git analysis, prose ingestion, workflow systems, or automation.

Repository authority remains implementation-backed behavior, existing reconciliation documents, identity-boundary audits, and repository-visible evidence.

## Central finding

Repository evidence supports a strong asymmetry:

```text
boundary creation
    requires enough evidence to avoid collapse

boundary collapse
    requires stronger positive equivalence evidence
```

The repository is intentionally better at saying:

```text
related
    != identical
```

than at saying:

```text
these are the same thing
```

The strongest current rule is:

```text
prefer relationship before merge
```

and:

```text
alias_of
    means identity equivalence
```

Therefore `alias_of` must remain reserved for cases where the repository has strong equivalence evidence.

## Evidence baseline

The state-versus-identity investigation found:

```text
state
    -> current condition

identity
    -> sameness across observations
```

It also found:

```text
state can change while identity remains

identity can change while state remains
```

This matters for equivalence because shared state is not enough to justify sameness.

Examples:

```text
same health state
    != same endpoint

same capability state
    != same principal

same measurement value
    != same measurement owner
```

Equivalence requires stronger evidence than shared condition.

## Repository-visible equivalence examples

### Strong host identity equivalence

Candidate evidence:

```text
machine_id
explicit operator alias
inventory-declared host identity
stable provider identity
hardware serial
```

These are among the strongest examples where two identifiers may be treated as the same host or entity.

Supported shape:

```text
host115
    alias_of
    stable host identity
```

Status:

```text
strong equivalence evidence when present
```

### Filesystem or storage identity equivalence

Candidate evidence:

```text
filesystem UUID
PARTUUID
WWN
serial number
pool or dataset identity
explicit operator declaration
```

The storage and filesystem identity work rejected mountpoint path alone as identity evidence.

Supported shape:

```text
storage observation A
    same storage identity as
storage observation B
```

only when strong storage identity evidence exists.

Status:

```text
strong when unique storage identity exists
weak or rejected when only mountpoint/path matches
```

### Principal identity equivalence

Candidate evidence:

```text
authenticated principal
trusted boundary verification
approval grant identity for a specific grant
explicit authenticated source metadata
```

The principal identity reconciliation found that many current surfaces are identity-like but not principal identity proof.

Rejected examples:

```text
actor=user
workspace_id
session_id
source_type=user
text says I am admin
```

Status:

```text
current implemented generic input principal equivalence is weak or absent
```

### Endpoint reconciliation

Candidate evidence:

```text
same endpoint-shaped subject
same address and port in same scope
stable scrape target identity
explicit endpoint identity evidence
```

Rejected collapse:

```text
host
    alias_of
host:port endpoint
```

Preferred relationship:

```text
host
    has_endpoint
endpoint
```

Status:

```text
endpoint identity exists
endpoint-to-host equivalence is rejected
```

### Measurement reassociation

Candidate evidence:

```text
explicit measurement owner
complete subject plus dimensions
storage UUID or host ownership evidence
projection-specific ownership rule
```

Rejected collapse:

```text
endpoint-owned filesystem measurement
    silently becomes
host-owned filesystem measurement
```

Status:

```text
measurement ownership requires explicit ownership evidence
alias-like knowledge is not enough
```

## Boundary creation versus boundary collapse

### Boundary creation

Shape:

```text
A and B may be related
but evidence is insufficient to treat them as identical
```

Examples:

```text
host
    != endpoint

endpoint
    != application

application
    != backend

username
    != cross-host user identity

mountpoint
    != storage identity

package
    != capability

service name
    != service instance
```

Boundary creation is conservative.

It protects evidence from overclaiming.

### Boundary collapse

Shape:

```text
A and B are sufficiently supported as the same identity
```

Examples:

```text
host alias
    -> machine_id identity

explicit operator alias
    -> same host

filesystem UUID
    -> same storage identity
```

Boundary collapse is stronger.

It changes how facts can attach, query, aggregate, and project.

### Key distinction

```text
boundary creation
    can be justified by uncertainty or mismatch

boundary collapse
    requires positive equivalence evidence
```

This explains why conservative separation appears easier than justified collapse.

## Minimum evidence for equivalence

Repository evidence suggests a hierarchy.

### Strong equivalence evidence

```text
unique stable identifier
explicit operator alias
trusted provider identity
machine_id
hardware serial
filesystem UUID / PARTUUID / WWN
container ID
trusted authenticated principal
```

### Moderate contextual evidence

```text
hostname observed from local host
IP address observed on interface
DNS name within known scope
Prometheus target associated with known host
provider-specific instance reference
```

Moderate evidence may support candidate association or relationship.

It should not always support collapse.

### Weak or non-equivalence evidence

```text
host:port endpoint
scrape target label alone
service name
package name
username
mountpoint path
reverse-proxy route name
same state
same health
same capability
same measurement value
```

Weak evidence can support relationship, visibility, or candidate association.

It should not support identity collapse by itself.

## Failures that motivated conservative separation

### Endpoint identity failures

Prometheus ingestion exposed host, endpoint, service, capability, monitoring system, alias, scrape target, and monitored entity scopes collapsing into too few predicates.

Rejected examples:

```text
host alias_of host:port endpoint

endpoint provides monitoring system as capability

host facts attach to endpoint subject
```

Boundary preserved:

```text
host
    != endpoint
```

### Filesystem measurement identity failures

Prometheus filesystem samples live on endpoint subjects.

Alias-like knowledge does not transfer measurement ownership to host subjects.

Boundary preserved:

```text
endpoint visibility
    != host ownership

measurement subject
    != entity identity

alias-like knowledge
    != ownership transfer
```

### Principal identity failures

Seed has identity-like surfaces, but many are not principal proof.

Rejected examples:

```text
actor=user
    != authenticated principal

workspace_id
    != authenticated principal

session_id
    != authenticated principal

source_type=user
    != verified principal

text identity claim
    != authentication
```

Boundary preserved:

```text
claimed identity
    != authenticated identity
```

### Entity identity derivation failures

The entity identity reconciliation explicitly rejected broad collapse.

Examples:

```text
same username across hosts
    != same identity

same mountpoint across hosts
    != same storage identity

package installed
    != service running

package identity
    != service instance identity
```

Boundary preserved:

```text
relationship before merge
```

## Equivalence without identity?

Repository evidence suggests only a weak yes, and only in scoped senses.

Examples:

```text
same classification state
same health state
same visibility class
same capability state
same measurement value
```

These are equivalences of state or value.

They are not identity equivalence.

Therefore:

```text
equivalence of state
    can exist without
identity equivalence
```

But this should not be called identity collapse.

## Identity without equivalence?

Repository evidence suggests yes, depending on meaning of equivalence.

Examples:

```text
same entity
    with changed state

same endpoint
    with changed availability

same principal
    with changed capability
```

The identity remains, but not all states, attributes, measurements, roles, or relationships are equivalent.

Therefore:

```text
identity
    does not imply total equivalence
```

Identity means sameness of referent.

It does not mean sameness of every state or relationship.

## Apparent equivalence repository evidence rejects

```text
host
    == host:port endpoint
```

Rejected.

```text
same username on different hosts
    == same principal
```

Rejected.

```text
same mountpoint path
    == same storage identity
```

Rejected.

```text
package installed
    == service available
```

Rejected.

```text
endpoint reachability
    == backend availability
```

Rejected.

```text
source_type=user
    == authenticated principal
```

Rejected.

## Apparent difference repository evidence can reconcile

```text
hostname
    and
machine_id
```

can collapse when the machine ID supports stable host identity.

```text
explicit operator alias
    and
host identity
```

can collapse when operator authority establishes aliasing.

```text
filesystem path observation
    and
storage identity
```

can reconcile when UUID, PARTUUID, serial, or pool identity supports it.

```text
provider instance reference
    and
local entity
```

can reconcile when stable provider identity and local observation agree.

## Important distinctions

### Identity

Sameness of referent across observations.

### Equivalence

A claim that two representations may be treated as the same for a specific purpose.

Identity equivalence is stronger than value equivalence, state equivalence, or query equivalence.

### Collapse

Operational or conceptual removal of a boundary so facts, queries, or relationships can attach across it.

### Reconciliation

Evidence-backed decision to collapse, separate, or relate.

### Boundary

A retained separation between concepts, identities, states, scopes, or ownership domains.

### Separation

The conservative result when evidence is insufficient for collapse.

### Derivation

How a stronger identity or relationship claim is produced from evidence.

### Ownership

Which subject owns a fact, measurement, capability, or relationship.

Ownership may depend on identity but is not identical to identity.

## Historical perspective

Repository history supports this pattern:

```text
conservative separation
    is default

justified equivalence
    requires stronger evidence
```

This is not a weakness.

It protects Seed from false identity collapse.

Recent investigations repeatedly succeeded at distinctions because distinctions can be supported by mismatch, uncertainty, scope, or missing evidence.

Equivalence requires positive evidence strong enough to let a boundary collapse.

That is a higher bar.

## Supported conclusions

1. Repository evidence supports justified equivalence only under stronger evidence than boundary creation.
2. `alias_of` is identity equivalence and must remain reserved for same-entity claims.
3. Related things are not necessarily identical.
4. Conservative separation is the repository default when equivalence evidence is weak.
5. Boundary collapse requires positive equivalence evidence such as stable identifiers, explicit aliases, trusted provider identity, or unique storage identity.
6. Shared state does not justify identity equivalence.
7. Equivalence can exist without identity when it is state or value equivalence.
8. Identity can exist without total equivalence of state, attributes, measurements, or relationships.
9. Ownership is not identity, and alias-like knowledge is not ownership transfer.
10. Justified collapse is harder than boundary creation because collapse affects fact attachment, query ownership, projection, and interpretation.

## Unsupported conclusions

- Any relationship implies identity.
- Any shared state implies identity.
- Any shared name implies identity.
- Any endpoint associated with a host is equivalent to that host.
- Any user-like source field is an authenticated principal.
- Any mountpoint path identifies storage globally.
- Any package fact implies service capability.
- Equivalence and identity are always the same thing.
- Identity implies all state remains equivalent.
- Boundary collapse should happen by default.

## Open questions

- What is the minimum repository-visible evidence for identity equivalence in each domain?
- Can equivalence be typed without implementing an equivalence system?
- Should the repository distinguish state equivalence, value equivalence, query equivalence, and identity equivalence?
- Can ownership reconciliation be represented without identity collapse?
- What surface should expose why a boundary was not collapsed?
- Can justified equivalence become visible before full identity implementation?

## Acceptance answers

### What evidence is sufficient for justified equivalence?

Strong positive identity evidence such as:

```text
machine_id
explicit operator alias
trusted provider identity
hardware serial
filesystem UUID / PARTUUID / WWN
container ID
trusted authenticated principal
```

Domain-specific evidence must match the identity being collapsed.

### How does boundary collapse differ from boundary creation?

```text
boundary creation
    is justified by uncertainty, mismatch, or insufficient evidence

boundary collapse
    requires positive equivalence evidence
```

### Does identity imply equivalence?

Only identity equivalence of referent.

It does not imply equivalence of all state, measurements, roles, ownership, or relationships.

### Does equivalence imply identity?

Not always.

State equivalence, value equivalence, and visibility equivalence can exist without identity equivalence.

### Why is conservative separation easier than justified collapse?

Because separation can be justified by lack of evidence or scope mismatch.

Collapse changes fact ownership, query behavior, projection, and interpretation, so it requires stronger evidence.

### What repository-visible evidence permits treating two things as the same thing?

Stable identifiers, explicit aliases, trusted provenance, unique storage or hardware identity, authenticated principal evidence, or domain-specific identity evidence strong enough to support `alias_of`-style equivalence.
