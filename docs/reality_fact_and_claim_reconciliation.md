# Reality Fact And Claim Reconciliation

## Purpose

Clarify the relationship between:

```text
Reality
Fact
Observation
Evidence
Claim
```

and determine whether the repository should treat facts as existing, while remaining claim-centric in representation.

This document is documentation-only.

No code changes.

No schema changes.

No runtime changes.

---

## Central Question

Investigate:

```text
Do facts exist?
```

and:

```text
If facts exist, what is the relationship between facts and claims?
```

---

## Initial Tension

The repository has increasingly adopted claim-centric language.

A potential misunderstanding is:

```text
Claim-centric
    =>
Facts do not exist.
```

The investigation finds this conclusion is unsupported.

The stronger question is:

```text
Where do facts exist?

Where do claims exist?
```

---

## Candidate Model

A useful starting model is:

```text
Reality
    contains
Facts

Representations
    contain
Claims
```

This model is evaluated below.

---

## Reality Versus Representation

The repository repeatedly preserves the boundary:

```text
Observation != Reality

Evidence != Reality

Claim != Reality
```

Examples include:

* Prometheus observations
* Endpoint identity work
* Host observation work
* Temporal authority work
* Corroboration work

Across these investigations, observations and claims are repeatedly treated as representations of reality rather than reality itself.

---

## Phone On Table Example

Assume:

```text
A phone is on a table.
```

Reality:

```text
Phone exists.
Phone is on table.
```

These conditions are either true or false regardless of Seed.

### Operator Testimony

Operator states:

```text
There is a phone on the table.
```

Seed acquires:

```text
Observation
Evidence
Claim
```

The phone itself is not created by the claim.

The claim is a representation of the phone.

### Camera Observation

Seed later observes:

```text
phone-shaped object
```

Additional support exists.

The claim becomes better supported.

The object does not become more real.

Only represented support changes.

### Direct Interaction

Seed later:

```text
unlocks phone
launches application
receives response
```

Support grows further.

The result remains:

```text
represented understanding
```

rather than direct possession of reality.

---

## Hostname Example

Assume:

```text
hostname = example_host
```

Support may include:

```text
hostname command
/etc/hostname
hostnamectl
SSH collection
```

The claim may become extremely well supported.

The ontology does not change.

The result remains:

```text
Claim:
hostname = example_host
```

with strong support.

---

## Stale Claim Example

Reality:

```text
Phone is on table.
```

Later:

```text
Phone removed.
```

Seed has not observed the change.

Result:

```text
Claim exists.
Fact no longer exists.
```

This demonstrates:

```text
Fact != Claim
```

because one can change without the other.

---

## Can Seed Possess Facts?

The investigation finds a useful distinction:

```text
Seed can represent facts.

Seed does not possess reality.
```

Seed acquires:

```text
observations
evidence
claims
support
```

These may correspond to facts.

They are not identical to facts.

---

## Can A Claim Become A Fact?

The investigation rejects:

```text
Weak Claim
    ->
Strong Claim
    ->
Fact
```

as an ontology transition.

Instead:

```text
Weakly Supported Claim
    ->
Strongly Supported Claim
```

appears sufficient.

Support changes confidence.

Support does not transform representation into reality.

---

## Relationship To Claim-Centric Architecture

Claim-centric architecture does not require:

```text
Facts do not exist.
```

The more precise interpretation is:

```text
Seed reasons over claims.
Reality contains facts.
```

Claims are useful because they accommodate:

```text
uncertainty
ambiguity
contradiction
corroboration
revision
support growth
staleness
```

without requiring ontology transitions.

---

## Reconciled Finding

The investigation supports:

```text
Reality contains facts.

Seed contains claims about facts.

Observations provide evidence.

Evidence supports claims.

Support may strengthen claims.

Support does not transform claims into reality.
```

A claim-centric architecture therefore reflects humility about representation rather than denial of reality.

The boundary is:

```text
Reality is authoritative.

Representation is not reality.
```
