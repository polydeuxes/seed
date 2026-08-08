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

## 5. What this does not establish

**That these acts are warranted.** They are implemented, they run, and they
record narrow authority. Whether each has its requirements established is the
step-3 question `#2348` says cannot be skipped, and it has not been asked of
them here. A narrow claim is not a warranted claim — it is a smaller claim.

`01.Kinds:72` supports that an observing boundary *may* hold occurrence
evidence locally. It does not establish that this capture boundary has done
what is required for its claim.

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

What that yields is accumulated bounded testimony. Whether accumulation ever
makes an additional act lawful is exactly what is not established.
`01.Uptake.A` denies a universal order, and `05.Testimony:111` is directly on
point:

> Observation history is not trajectory or transition standing. Retaining `up
> at t1`, `down at t2`, and `up at t3` does not establish outage, recovery,
> flapping, trajectory, trend, transition, consequence, cause, or changed
> ordinary behavior without a separate comparison boundary.

More preserved occurrences do not, by accumulating, warrant anything further.

So the bootstrap gains a floor, not a staircase.

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
