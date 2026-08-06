# Prometheus Translation ownership recovery 001

## Scope

This report tests one proposed topology against the Prometheus egress road:

```text
reusable bounded Translation competency
+ exact local demand
→ exact Translation invocation

competency != invocation != downstream Consumer
```

The decisive question posed was:

```text
Can one established Prometheus semantic competency be invoked by
different exact observation Responsibilities for different
Consumer-purposes, while remaining distinct from each invocation
and from each downstream Consumer?
```

Prometheus was chosen because the console supplies only one pipe, so console evidence cannot separate a durable owner from an interaction-local one.

This report amends no active Book law, runtime, or tests.

## Finding 1 — `competency` is not established as a constitutional kind

Active law mentions competency in three places and establishes none of them as a kind with its own grammar.

`03-goals-and-advancement/demands-and-opened-movement.md:9` lists competency among the many things a Demand may concern — *"what result, relation, clarification, inquiry, authority, transformation, competency, or other bounded condition is required"*. That is a list member, not a definition.

The same chapter at `:74` is explicitly negative:

> The possible relation is consumer-relative, material-relative, and act- and purpose-relative; it is not a global language state or **a competency by identity**... A separately established competency **might** be one candidate way to satisfy the possible bounded relation, but a competency candidate is not a Capability established.

And `operator-ingress-common-grammar-prerequisite.md:195` preserves `prose competency available != enum obs...` as a non-equivalence.

So competency is referenced conditionally — as something that *might* be separately established — and is expressly denied identity standing. Building a topology on "reusable bounded Translation competency" as the durable owner therefore rests on an unestablished kind.

This is weaker than a pure coinage, since the word appears in active law. It is still not a recovered owner.

## Finding 2 — the "many invocations" premise is not observable

`PrometheusObservationSource` has exactly **one** non-test construction site in the repository:

```python
# scripts/seed_local.py:715
def build_prometheus_observation_source(args: argparse.Namespace) -> Any:
    source = PrometheusObservationSource(
        args.observe_prometheus, timeout_seconds=args.observe_timeout
    )
```

It is constructed from CLI arguments. Its `collect()` then iterates a fixed tuple:

```python
SAFE_QUERIES = (
    "up",
    "node_uname_info",
    "node_filesystem_avail_bytes",
    "node_filesystem_size_bytes",
)
...
for query in self.SAFE_QUERIES:
```

There is no observation requirement, no applicability determination, no Consumer-purpose, and no selection among competencies. One construction site, driven by flags, iterating a hardcoded list.

So Prometheus reproduces the console's one-pipe problem rather than escaping it. The two hypotheses —

```text
a durable competency invoked by many Responsibilities

an owner coextensive with its single invocation road
```

— remain observationally identical here, exactly as they were for `capture_stdin_material`, which likewise has one non-test caller.

The expectation that the answer is yes is not supported by this repository. It may be true of an intended design; it is not recovered from observed structure.

## Finding 3 — what Prometheus does demonstrate

Prometheus contributes something the console cannot, and it is not the durable-competency claim.

`prometheus_sysname_to_os_semantic_competency_recovery_001.md` already tabulates twelve distinct crossings inside a single `node_uname_info` payload, with classifications:

```text
envelope/sample grammar        compiled realization; compatibility-tested
metric-contract recognition    frozen assumption
label-role interpretation      frozen assumption
subject formation              frozen assumption
predicate competency           frozen assumption
value grammar                  compressed
temporal convention            mixed
authority convention           frozen assumption
confidence convention          frozen assumption
relation competency            frozen assumption
compatibility/refusal          evidenced frozen realization
Fidelity examination           absent
```

and states directly:

> The stack is not one translation: it contains a structural decoder, semantic translator, implicit ontology, predicate competency, relation competency, authority/temporal/confidence conventions, compatibility rules, and frozen realizations.

That is the recoverable finding: **one external payload passes through several separable Translation-shaped crossings, compiled together in one class.** Their implementation co-location does not make them one Responsibility, and the repository has already warned that implementation owner is not constitutional Responsibility owner.

This is demonstrable from observed structure. The durable-competency claim is not.

## Finding 4 — both roads fail identically, in opposite directions

```text
operator ingress    constant under-claim
                    "Communicative meaning: unresolved (Unknown)" rendered
                    regardless of what occurred

Prometheus          frozen over-claims
                    instance is the subject; sysname means os; Linux becomes
                    linux; provider time is authoritative; confidence is 0.95
                    — all baked in, none compared
```

Both place a constant where a computed result belongs. The console asserts nothing and cannot be wrong. Prometheus asserts a semantic crossing that was never tested — `Fidelity examination: absent`, *"No preserved comparison warrants any semantic crossing."*

The prior recovery's conclusion stands: *"`sysname="Linux"` does not presently warrant constitutional `os=linux`."*

## Finding 5 — Prometheus supplies the non-empty candidate cases the console cannot

The console cannot demonstrate a live candidate road because `Hello` offers no structure to propose against, so every proposal set is empty, and a computed empty set is indistinguishable in output from a constant one.

Prometheus supplies both outcomes, already analysed:

```text
warranted     "For this occurrence, the provider record returned the
              token/value sysname="Linux" in the series-label dictionary
              associated with query token node_uname_info"
              — needs only structural recognition plus attribution

unwarranted   sysname="Linux" → os=linux
              — a semantic crossing with no preserved comparison
```

That is the varying pair required to show a candidate road is live rather than constant.

## What this settles for the console question

It does not settle ownership. It removes one proposed route to settling it and preserves a different one.

```text
not supported    a durable Translation competency, invoked by many
                 Responsibilities, distinct from each invocation

supported        within one occurrence, several distinct Translation-shaped
                 crossings may be separately owned while compiled together
```

Applied to the console: decoding to an attributed addressable representation and forming a relation proposal may be distinct Translation acts with distinct owners, even though the present implementation compiles them into one boundary. That separation does not require the durable-competency claim, and can be argued from the Prometheus layer table rather than from an unestablished kind.

## Remaining unresolved coordinates

- Whether any Translation owner survives its invocation. No repository evidence bears on this; both roads have single invocation sites.
- Whether `competency` should be recovered as a constitutional kind, or remains a report-level description of compiled implementation behaviour.
- The exact owner of each of the twelve Prometheus crossings. The prior recovery classified their standing; it did not assign owners.
- Whether the frozen assumptions are defects to correct or conventions to establish. This report does not decide that.

## Disposition

```text
proposed topology                       not recovered
competency as durable owner             unestablished kind
one competency, many invocations        not observable in this repository
one payload, several Translation acts   demonstrable
console analogy via layer separation    available
console analogy via durable competency  unavailable
```

No implementation slice follows from this report. Its use is negative and bounding: it removes the durable-competency route to console Translation ownership, and supplies the layer-separation route in its place.

## Vocabulary explicitly not adopted

```text
competency as a constitutional kind
Prometheus semantic competency as a recovered owner
competency invocation as an established act
```

`frozen assumption`, `compiled realization`, and `compressed` are quoted from the prior recovery as its classifications, not adopted as constitutional vocabulary here.
