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

### Correction record

The first version overreached in five places, recorded rather than silently replaced:

```text
1. it called several Translation Acts "demonstrable" while leaving every
   crossing's owner unresolved, and treated all twelve inventory items as
   Translation when several are structural decoding, conventions, or an
   absence

2. it reasserted that `Hello` necessarily produces an empty candidate set
   — a claim already withdrawn in
   orientation_attempt_observable_evidence_recovery_001.md

3. it presented structural testimony and a semantic relation proposal as a
   warranted/unwarranted pair from one candidate road; they are different
   result kinds

4. it said both roads place a constant where a computed result belongs;
   Prometheus's output varies with the payload, and its defect is
   unexamined semantic mapping rather than constant output

5. it said competency is "expressly denied identity standing"; the cited
   clauses are non-equivalences, and the finding rests on absence of
   recovered grammar
```

The negative result survives unchanged: the durable-competency topology is not recovered, and no implementation follows from it.

## Finding 1 — `competency` is not established as a constitutional kind

Active law mentions competency in three places and establishes none of them as a kind with its own grammar.

`03-goals-and-advancement/demands-and-opened-movement.md:9` lists competency among the many things a Demand may concern — *"what result, relation, clarification, inquiry, authority, transformation, competency, or other bounded condition is required"*. That is a list member, not a definition.

The same chapter at `:74` is explicitly negative:

> The possible relation is consumer-relative, material-relative, and act- and purpose-relative; it is not a global language state or **a competency by identity**... A separately established competency **might** be one candidate way to satisfy the possible bounded relation, but a competency candidate is not a Capability established.

And `operator-ingress-common-grammar-prerequisite.md:195` preserves `prose competency available != enum obs...` as a non-equivalence.

Both cited clauses are **non-equivalences**, not denials of standing:

```text
possible relation      != competency by identity
competency candidate   != Capability established
```

Neither establishes that competency has no standing. What is absent is any recovered grammar defining competency as a kind — no owner, act, evidence, result, or boundary. The finding rests on that absence, not on a positive denial. An earlier version of this report said competency was "expressly denied identity standing"; that read a non-equivalence as a positive claim about one side, and is withdrawn.

Building a topology on "reusable bounded Translation competency" as the durable owner therefore rests on a kind the Book has not recovered.

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

That inventory is **not twelve Translation Acts**. It mixes kinds:

```text
structural decoder        != Translation automatically
confidence convention     != Translation automatically
compatibility/refusal     != Translation automatically
absent Fidelity           != an Act occurrence at all
```

The recoverable finding is narrower: **one external payload passes through several separable structural and semantic crossings, compiled into one implementation boundary.**

Separability is not cardinality:

```text
separable crossings        != several Responsibilities established
implementation co-location != one Responsibility established
separable outputs          != distinct owners established
```

This report classifies standing; it does not assign owners, and it cannot claim established Act cardinality while leaving ownership unresolved. What is demonstrable is that one compiled boundary may conceal several independently meaningful crossings — not how many Responsibilities those crossings constitute.

## Finding 4 — the two roads fail in opposite ways, not identically

```text
operator ingress    constant under-claim
                    "Communicative meaning: unresolved (Unknown)" rendered
                    regardless of what occurred

Prometheus          frozen over-claims
                    instance is the subject; sysname means os; Linux becomes
                    linux; provider time is authoritative; confidence is 0.95
                    — all baked in, none compared
```

An earlier version said both place a constant where a computed result belongs. That is wrong for Prometheus and is withdrawn.

```text
console      no candidate or Compare result is consumed
             → a fixed literal is emitted regardless of ingress
             → fixed under-claim

Prometheus   input-dependent mapping does occur; the emitted value
             varies with the payload
             → but fixed semantic relations are applied without Fidelity
             → potentially unwarranted over-claim
```

The console's output is constant. Prometheus's output is not — `Linux` becomes `linux` because the payload said `Linux`. Its defect is unexamined semantic mapping, not constant output: `Fidelity examination: absent`, *"No preserved comparison warrants any semantic crossing."*

The prior recovery's conclusion stands: *"`sysname="Linux"` does not presently warrant constitutional `os=linux`."*

## Finding 5 — Prometheus supplies the non-empty candidate cases the console cannot

An earlier version of this report said `Hello` offers no structure to propose against, so every proposal set is necessarily empty. That reintroduces a claim already withdrawn in `orientation_attempt_observable_evidence_recovery_001.md`:

```text
candidate set not presently computed
!= candidate set established empty
```

`Hello` supplies a presentation and Seed supplies available grammar. Whether that combination forms zero, one, or several candidate relations is unresolved until the candidate-forming Act occurs. The supportable claim is only that the console presently provides **no observable computed candidate result at all**.

What Prometheus supplies is more explicit structural material, from which semantic proposals are easier to construct and test:

```text
warranted     "For this occurrence, the provider record returned the
              token/value sysname="Linux" in the series-label dictionary
              associated with query token node_uname_info"
              — needs only structural recognition plus attribution

unwarranted   sysname="Linux" → os=linux
              — a semantic crossing with no preserved comparison
```

These are **not two outcomes of one candidate road**. The first is source-attributed testimony about returned syntax; the second is a proposed semantic relation:

```text
source-relative testimony != candidate semantic relation
```

What the pair establishes is that structural testimony may be warranted while a stronger semantic relation over the same material remains unwarranted. That is useful, and it is not proof that one candidate producer yielded two candidate outcomes.

## What this settles for the console question

It does not settle ownership. It removes one proposed route to settling it and preserves a different one.

```text
not supported    a durable Translation competency, invoked by many
                 Responsibilities, distinct from each invocation

supported        one compiled implementation boundary may conceal several
                 independently meaningful crossings

not supported    how many Responsibilities those crossings constitute,
                 in either direction
```

Applied to the console: that decoding to an attributed addressable representation and forming a relation proposal are compiled into one boundary does not establish that they are one Responsibility — and separability does not establish that they are two. Neither cardinality follows from separability alone.

What this does remove is the argument that they must be one because the implementation compiles them together. That argument is unavailable in both directions, which leaves the ownership question open on its own terms rather than settled by implementation shape.

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
one payload, several separable crossings demonstrable
Act and Responsibility cardinality  unresolved
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
