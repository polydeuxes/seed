# record: cat test 001

## 1. Executive

`record` was made load-bearing by `#2363`, which found that `artifact`
decomposes into `preserved representation or record` and that nobody had
examined the second half.

**`record` defends itself.** It has everything `artifact` lacked:

```text
                              artifact        record
named clause                  no              05.Recording.A
producing boundary            no              recording boundary
produced standing             no              "a record exists and
                                               preserves an attributed
                                               assertion"
consumer relation stated      no              "the bounded consumer may
                                               take up that recorded
                                               assertion as attributed
                                               material"
forbidden inference stated    n/a             yes, explicitly
```

`05.Recording.A` is titled **Recorded assertion standing**. It names the
producing boundary, states what standing that boundary produces, states what a
consumer may do with it, and states the inference that does not follow. That
is a complete responsibility-shaped structure, and it is exactly the structure
the substitution test found missing for `artifact`.

**The preserve-versus-record distinction is real and is already in the Book.**
§3. Recording produces something new; preservation keeps something available.

## 2. Why the defence holds

`05.Recording.A`:

> A recording boundary may create retrievable assertion-bearing material
> within its declared preservation horizon. **The produced standing is that a
> record exists and preserves an attributed assertion.** The bounded consumer
> may take up that recorded assertion as attributed material. The forbidden
> inference is that the represented external occurrence, current lawful state,
> factual truth, renewed occurrence, or consumer receipt has been established
> merely because the record exists.

Applying the three-step test:

```text
1  does `record` name something?
     yes — retrievable assertion-bearing material

2  what kind of thing?
     a produced result, with its own bounded standing

3  does it own a Responsibility, or is it carried/produced by another?
     produced by another — recording owns the Responsibility

4  what exact Act produces it as itself, and what Standing does that
   production establish?
     a recording boundary; the standing that a record exists and
     preserves an attributed assertion
```

Step 4 is added by this report and is what separates the two cases.

Step 3 returns the same answer as `artifact`, and the outcome differs anyway:

```text
artifact   no act produces artifact-as-such
           no artifact-specific Standing follows

record     produced by recording
           record-existence Standing follows
```

`artifact` remains what `#2346` recovered — a carrier classification, not a
result of anything. `record` is a produced result whose producing act states
what standing that production establishes. A result does not need to own a
Responsibility when its producing act does.

Fourteen non-equivalences guard the boundary, and they are not variations on
one theme:

```text
act occurrence           != recording occurrence
measurement occurrence   != recorded measurement
comparison occurrence    != recorded comparison
comparison               != recording
operational measurement  != recording
baseline establishment   != baseline recording
recording                != knowledge extraction
record exists            != recorded assertion true automatically
record exists            != recorded standing lawfully established
retrievable record       != established fact
process-local record     != cross-restart persistent record
```

The pattern `X occurrence != recorded X` recurs three times across
measurement, comparison, and act. That is a distinction the corpus applies
repeatedly rather than a phrase used once.

## 3. preserve and record are not the same act

The operator's reading — Seed may record results to a table and preserve a
reference to that table in its ledger — is supported.

```text
preservation    keeps already-produced material or Standing available
                does not renew the original occurrence
                does not itself establish standing

recording       a responsible occurrence
                creates new retrievable assertion-bearing material
                produces the standing that a record exists
```

Active law keeps them apart directly:

```text
05.Recording:10   recording and preservation are separate responsibilities
05.Recording:70   preservation != renewed occurrence
05.Recording:65   preservation decision != standing-establishment decision
05.Recording:62   act occurrence != recording occurrence
06.Events:20      event recording != required for every constitutional
                  occurrence
```

The first four state the separation directly. `06.Events:20` is consistent
corroboration rather than proof: reading it as decisive would require assuming
that every constitutional occurrence itself requires preservation, which no
clause states. The distinction stands on the direct evidence without that
step.

Event recording is then one *form* of recording rather than its definition.
`06.Events:10` has a responsible recording occurrence preserve attributed
testimony **as an Event**, while Event preservation does not establish the
asserted occurrence as true. So the chain the operator described holds at each
step without upgrading anything:

```text
responsible act        → result R
recording occurrence   → record T carrying an assertion about R
recording occurrence   → Event E preserving testimony about T

T exists   does not establish R
E exists   does not establish T's assertion, and does not establish R
```

## 4. The reference-versus-referent point

Curator's sharpening — that preserving a reference is not preserving the
referent — has partial support and is not fully stated.

`05.Recording:73` holds `process-local record != cross-restart persistent
record`, which is the same concern in one specific form: a record that does
not survive restart is not the durable thing a later consumer needs.

But no clause states the general form. `05.Recording:10` bounds recording by
"the preservation horizon supplied by the recorder", which implies the
horizon matters without saying that a reference outliving its referent fails
to preserve it.

Recorded as a gap, not proposed as an amendment.

## 5. What this means for `artifact`

`#2363` found that `artifact` loses no distinction under substitution, and
that `artifact standing` exists only in a title, a core question, and five
links. This report shows the union's second half is genuine grammar.

The consequence is narrow and worth stating precisely: **substituting
`artifact` is now cheaper than it looked.** Both halves of
`preserved representation or record` are real terms with their own clauses, so
a clause needing a subject has two established ones to choose between rather
than an undefined pair.

That is not an argument for removing `artifact`. It removes one argument for
keeping it — that the union names something its parts could not.

## 6. What this does not establish

**That `record` and `representation` are distinct.** They are named together
in exactly one place, `01.Kinds:10`'s definition of artifact, and nowhere does
active law state `record != representation`. Both defend themselves
separately; whether the union's two halves are actually two things is
untested, and it is the obvious next question.

**That every `record` use is lawful.** The clause structure defends the term.
Individual uses across ten files were not audited.

**That `artifact` should be removed or retained.** §5 states only that one
argument for retention is weakened.

**That the preserve/record boundary is complete.** §4 records that the general
reference-versus-referent form is absent from active law.

## 7. Method note

The three-step test returned "a result, not an owner" for both `artifact` and
`record`, and the verdicts still differ. Step 3 asks whether the subject owns
a Responsibility; it does not ask **what act produces it as itself**.

```text
artifact   no act produces artifact-as-such  → nothing follows from being one
record     produced by recording            → a stated produced standing
```

That is a fourth question worth carrying, and it separates a genuine result
from an umbrella: *what act produces this, and what standing does that act
state it produces?* An umbrella has no answer to either.
