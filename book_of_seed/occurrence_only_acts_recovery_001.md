# Occurrence-only acts at ingress: recovery 001

## 1. Executive

The observation under test: there are immediately lawful acts available at
ingress, which make narrow claims about what just occurred without needing to
know what the material means.

**The observation is confirmed in the running code, and it is substantial.**
Live ingress performs four acts, each recording an authority string that limits
it to what it directly witnessed:

```text
seed_runtime/operator_ingress.py:161   "occurrence evidence only"
seed_runtime/operator_ingress.py:194   "decoder outcome evidence only"
seed_runtime/operator_ingress.py:265   "closes only this interaction"
seed_runtime/operator_ingress.py:297   "occurrence-only; meaning Unknown"
```

Four separate boundaries, four separate refusals to claim more. This is not a
sketch of what Seed might do; it is what runs on every console cycle.

**But the name is wrong, and the campaign's own rule catches it.** These were
called *temporal* acts. Cat test on the coinage:

```text
temporal act              0 occurrences in active law
temporal responsibility   0
temporal dimension        0
temporal spine            0

temporal standing        10 — a different thing entirely (§3)
occurrence               92
```

The established word for what these acts claim is **occurrence**, and it is one
of the most heavily used terms in active law. Naming a new category for
something that already has a name is the move this campaign has spent twelve
reports undoing.

**And the two-spine picture is a topology claim.** §4. What is recovered is a
class of acts, not an ordering.

**These acts are warranted, and this report first said otherwise.** §5 corrects
it. An occurrence within a Responsibility's bounded Authority is warranted at
that bounded strength, without requiring an upstream coordinate to establish
that the boundary may witness what crosses it. `#2348`'s step-3 rule governs
the establishment of stronger relation Standing, not this.

## 2. What the four acts actually claim

Read against `01.Kinds:72`, which supplies the backing:

> occurrence evidence may be local to a producing or **observing** boundary and
> absent from the resulting artifact

An observing boundary may hold occurrence evidence locally. That is the shape
these acts have.

```text
capture              standing="captured"
                     authority="occurrence evidence only"
                     claims: these exact bytes crossed this boundary

decoder examination  standing=examination.outcome
                     authority="decoder outcome evidence only"
                     claims: this decoder produced this outcome over
                             those exact bytes

close                standing="closed"
                     authority="closes only this interaction"
                     claims: this interaction ended

ingress              standing="occurred"
                     authority="occurrence-only; meaning Unknown"
                     claims: this represented material occurred
```

Each names what it does **not** claim by naming precisely what it does. The
fourth is the sharpest: `meaning Unknown` is recorded as part of the act's own
authority, not left implicit.

Note what none of them requires: a meaning relation, an applicability
determination, a consumer purpose, a goal, or any judgement about whether the
material is true, intended, or useful. The decoder boundary does not claim its
outcome is what the operator meant. The ingress boundary does not claim the
material means anything at all.

## 3. Why `temporal` is the wrong word

`temporal standing` is real — ten occurrences — but it means something else:

```text
"...boundary, act or movement authorized, scope, purpose, temporal
 standing, constraints, evidence, occurrence, negative authority..."

"...source, recipient, scope, purpose, duration or temporal standing,
 constraints, evidence, and occurrence..."
```

It appears in authority-grant coordinate lists, paired with *duration*, and
sits **alongside** `occurrence` rather than covering it. `temporal standing` is
how long an authority holds. It is not a category of act concerning what just
happened.

So the vocabulary already available is exact:

```text
proposed        established
────────────────────────────────────────────
temporal act    occurrence-only act
temporal spine  (see §4 — no spine is recovered)
```

`occurrence-only` is not a coinage either — it is the runtime's own word, at
`operator_ingress.py:297`.

## 4. What is recovered, and what is a topology claim

The sketch these acts prompted has an occurrence spine feeding a semantic
branch, each with ordered arrows. **The class of acts is recovered. The
ordering is not.**

```text
recovered   a class of acts whose warrant concerns what the boundary
            directly witnessed, which claim nothing about meaning

not         that they form a spine
recovered   that the semantic side branches off them
            that either proceeds in the drawn order
```

This is the campaign's most repeated error and it is worth naming again here,
because the picture is attractive. `01.Uptake.A` requires no universal order
among availability, applicability, admission, consumption, Uptake, reliance,
and standing change. `04.Question:21` holds that naming several standings "in
one report, graph, implementation surface, or sequence does not establish a
canonical node inventory, universal pipeline, constitutional ordering, or
missing edge."

Four acts that happen to run in sequence in one console loop establish a
sequence in that loop. They do not establish that occurrence acts precede
semantic ones constitutionally, and the ingress code's own ordering is control
flow, which #2347 established does not supply warrant.

## 5. What warrants these acts

An earlier draft of this section said "these acts are not shown to be
warranted," applying `#2348`'s step-3 caution mechanically. **That is
withdrawn.** It made this report contradict itself: §1 called the acts
immediately lawful while §5 denied they were warranted. Both cannot stand.

Stated in established grammar, with no new species of Warrant:

```text
a Responsibility, its Authority, and an occurrence it witnesses or
performs within that Authority
  → bounded occurrence Standing at that strength

a stronger relation Standing
  → whatever that exact Responsibility requires
```

`#2348`'s step-3 rule governs the second. It does not govern the first, because
an observing boundary's competence to witness what crosses it is constituted by
its Responsibility and Authority, not established by some upstream coordinate.
The boundary does not need to determine whether an occurrence is *applicable to
its own ability to observe that occurrence*.

An earlier version of this correction named those two cases `DIRECT WARRANT`
and `DERIVED WARRANT`. **Withdrawn.** Naming them invents two constitutional
species of Warrant where the existing coordinates already say everything
needed, which is the exact move this campaign exists to catch.

`01.Kinds:72` supports the shape — occurrence evidence may be local to a
producing or observing boundary. What this report has not done is verify that
each of the four acts stays inside its stated Authority. That is a narrower and
answerable question than the one the draft asked, and it remains open.

**That "meaning Unknown" is a lawful resting place rather than an unfilled
coordinate.** The ingress act records it as authority. Whether recording
`Unknown` there discharges a requirement or defers one is unexamined.

**That this answers what the first lawful post-ingress act is.** It reframes
the question rather than answering it. The honest revision:

```text
was      what is the first lawful post-ingress Act?

now      occurrence-only acts are implemented and running at ingress.
         What additional Act may lawfully interpret, relate, compare,
         consume, or otherwise advance preserved material beyond
         occurrence testimony — and what does it require?
```

The second question is the open one, and it is the same question `#2348` ended
on, reached from the other side.

## 6. Why this matters for the bootstrap

Recorded as an implication, not a finding.

If occurrence-only acts are lawful without semantic prerequisites, then an
ingress does not leave Seed frozen. `E1` "hello", `E2` "learn proficient
english language", `E3` grammar book and dictionary — each can be captured,
examined, and preserved as occurrence testimony immediately, with meaning
recorded as Unknown, without waiting for anything to become interpretable.

What that yields is a growing body of individually warranted occurrence
testimony — which is more than an earlier draft of this section allowed. It
said "accumulation warrants nothing further by itself." **Withdrawn as
overbroad**, and its replacement narrowed too. An intermediate draft said
"accumulation warrants claims about the accumulation," which is too generic.
What is actually recovered:

```text
preserved append order       → exact append-order claims
directly witnessed order     → exact observed-order claims
```

and nothing wider.

`06.Events:47` is precise about where the line falls:

> Event timestamp and ledger order are distinct. **Ledger order is the append
> sequence a projector replays**; event timestamp is event-carried metadata
> that may be supplied out of sequence. Chronology is not causation: causal or
> correlation fields can preserve local linkage evidence, but **earlier time or
> earlier append position does not by itself prove production, reliance, or
> response**.

Append order is a real, replayable sequence. What it does not prove is
production, reliance, or response. And `05.Evidence.D:30` states the positive
half explicitly — sequence and co-occurrence "may orient inquiry or **support a
bounded claim that such a relation was observed**", while not establishing
causation, explanation, conduct, or responsibility.

So "E3 came after E2" is several claims with different warrant:

```text
E2 was appended before E3                       warranted, ledger order
Seed observed E2 before E3 at this boundary     warranted where the
                                                boundary directly
                                                preserves that order
E3's external source occurrence happened
  after E2's                                    not warranted by either
E3 was a response to E2                         not warranted
E2 caused E3                                    not warranted, 05.Evidence.D
E3 advanced the goal expressed by E2            not warranted
```

The first two are not Unknown. Seed witnessed them.

`05.Testimony:111` is consistent with this and denies only the stronger
reading:

> Observation history is not trajectory or transition standing. Retaining `up
> at t1`, `down at t2`, and `up at t3` does not establish outage, recovery,
> flapping, trajectory, trend, transition, consequence, cause, or changed
> ordinary behavior without a separate comparison boundary.

What that clause refuses is *therefore there was an outage*. It does not refuse
*up was observed at t1, and t1 precedes t2*. `history != trajectory` does not
mean history has no warranted internal chronology.

So the bootstrap does not merely gain a floor. From the instant Seed exists it
preserves a growing body of **individually warranted occurrence testimony** and
bounded witnessed chronology. It does not accumulate an aggregate Standing over
that history — saying so would rebuild the universal derived object active law
denies at `06.Events:10`. Each occurrence carries its own warrant at its own
strength.

What it does not acquire, without the Responsibility that establishes it, is
relational, semantic, trajectory, causal, or goal Standing over that history.

## 7. Method note

The finding and the correction came from the same command. Confirming the
operator's observation took one grep of the ingress module; testing the name
proposed for it took one fan-out, and the fan-out returned zero for every form
of the proposed word and 92 for the established one.

The rule that caught it is the one this campaign built, now applied to
vocabulary the campaign itself was generating rather than to inherited Book
terms:

```text
before naming a class of acts, check whether active law
already names it
```

`occurrence` was not a near-miss. It is one of the most used words in the
corpus, and it appears in the runtime string that prompted the question.

**Correction recorded, and it is the more instructive one.** The first draft
denied that these acts were warranted and denied that accumulation warrants
anything — while its own §1 called them immediately lawful. A report that
contradicts itself has usually applied a rule outside its scope, and that is
what happened: `#2348`'s step-3 caution governs *derived* warrant and was
applied to *direct* warrant.

The generalisation worth keeping: **a correction learned in one place is not
automatically a rule everywhere.** Four consecutive reports had found
overclaims, so the fifth reached for the strongest available limit and
overshot. Caution is not free — an unwarranted denial is as wrong as an
unwarranted assertion, and it costs more here, because it denies Seed standing
it actually has.
