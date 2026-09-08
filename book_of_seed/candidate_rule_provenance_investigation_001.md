# Candidate rule provenance investigation 001

## Status

Findings only from current tip `7945de52`.

This investigation changes no active Book clause, witness grammar, runtime, or
test. It adds no Candidate rule and produces no Candidate.

The question is the provenance of the two rules currently carried by
`01.Source.E.1`:

```text
one Candidate for each exact source Assertion

one Candidate for each pair of distinct exact source Assertions
in both source orders
```

The audit distinguishes their present active status from how they entered the
repository.

## 1. Result

Both rules were authored as bounded calculator-serving design choices. Neither
was independently recovered before it entered active Book.

The chronology is exact:

```text
7cf1bf3c
pre-build investigation says G, source surface,
Responsibility, and Authority remain unrecovered

        ↓ next commit

c962a5c2
Book amendment + machine witness + runtime + tests
+ calculator witness
introduce the unary rule together

        ↓ one correction

5e9fc00f
recover exact Act-local input role
does not recover another G

        ↓ next commit

07625cad
Book amendment + machine witness + runtime + tests
+ calculator witness
introduce pair arity, distinctness, and both source orders together
```

Passing tests demonstrate that the implementation follows those authored
rules. They do not warrant the rules.

The repository chronology identifies the Calculator witness as the proving
pressure in both introducing commits. The unary rule made the calculator
claim-side and output-side Assertions separately available as Candidates. The
pair rule immediately made both arrangements of those two exact calculator
Assertions available together. Calling that the motivating pressure is an
inference from the same-commit coupling and the exact test assertions; neither
commit records a separate statement of author intent.

No earlier report recovered:

```text
why every exact source Assertion was owed a unary Candidate
why every distinct pair was owed
why both source orders were owed
why self-pairs were excluded
why three-or-more-source Candidate subjects were not owed
```

The rules are active Book assignments today. Their provenance is nevertheless
developer-authored witness scaffolding, not independently recovered
constitutional precedent.

## 2. What the pre-build investigation established

The last findings commit before the unary build was `7cf1bf3c`, *Recover the
Candidate completeness boundary*.

It recovered an important conditional:

```text
if an exact G already requires exact Candidate subjects,
then omission of one required subject defeats completion
```

It explicitly did not recover G.

Its final vacancy was:

```text
exact bounded source surface
exact source-reference enumeration
exact candidate rule G
exact production Responsibility
exact production Authority
source Applicability and Participation
exact completion and result boundary
```

Its calculator disposition was equally explicit:

```text
no complete calculator source surface recovered
no formation arity or source roles recovered
no source order or self-pair rule recovered
no Candidate-producing Responsibility or Authority recovered
```

It also refused these generalizations:

```text
every Standing Assertion is automatically proposed input
one universal arity or source-order rule
one generic all-Assertion Candidate-producing Responsibility
```

Thus `7cf1bf3c` recovered the mechanics of completeness under an exact prior G.
It did not authorize the rule introduced by the next commit.

## 3. Unary rule provenance

### 3.1 Introducing change

`c962a5c2`, *Build unary Candidate Standing through exact boundaries*, is the
direct child of `7cf1bf3c`.

One commit added all of these:

```text
active Book clause 01.Source.E.1
machine rule coordinates
new Candidate runtime
new runtime occurrences and Standing projection
new Candidate tests
calculator witness use
```

The Book amendment directly assigned:

```text
at one exact ledger boundary,
one Candidate for each exact Measurement or Compare result Assertion
and each exact Assertion carried by those results and Locality Standing
through that boundary, in event order
```

The machine witness directly named:

```text
one_candidate_for_each_exact_source_Assertion_in_event_order
```

The runtime then implemented that exact rule. No earlier producing finding is
referenced by the Book, machine witness, or runtime.

### 3.2 Calculator pressure in the same commit

The calculator witness was modified in `c962a5c2` to invoke the new Candidate
road at the exact calculator boundary.

Its new proving test required the Candidate result to contain separately:

```text
the calculator claim-side path finding
the calculator output-side position Assertion
```

The test also proved that no Candidate yet carried both together. That is
useful implementation testimony about the unary rule. It directly establishes
that the new rule was used to satisfy the calculator crossing; the stronger
claim about author motive remains the chronology-based inference stated above.

### 3.3 Missing warrant

No report before `c962a5c2` establishes why Candidate work owed one Candidate
for every source Assertion.

The earlier reports established only:

```text
a neutral Candidate may exist before its represented relation is warranted
Candidate existence does not establish that relation
completion cannot omit work an exact G already requires
```

They did not establish:

```text
all Measurement and Compare Assertions through B are Candidate inputs
one source Assertion is one required Candidate subject
event order is Candidate-result order
every such source Assertion is applicable to this Candidate Act
```

The unary rule therefore entered as a bounded design choice authored into the
Book and calculator witness together.

## 4. Pair rule provenance

### 4.1 No intervening G recovery

Only one commit lies between `c962a5c2` and `07625cad`:

```text
5e9fc00f Recover the exact Candidate input role
```

That correction established the source Assertion's Act-local input role and
its Applicability/Participation coordinates. It changed no Candidate arity,
source surface, self-reference condition, or source-order warrant.

Thus no independent pair-rule recovery occurred between the unary build and
the pair build.

### 4.2 Introducing change

`07625cad`, *Record every ordered pair Candidate*, changed Book, machine
witness, runtime, tests, and calculator witness together.

The Book amendment directly assigned another rule:

```text
one Candidate for each pair of distinct exact source Assertions
in source event order for the first Act-local source position
and then the second
```

The machine witness directly supplied:

```text
arity: two source Assertions
first and second Act-local source positions
distinct references required
first source event order, then second source event order
relation: Unknown
```

The runtime used nested iteration over every first and second source position,
skipped equal positions, and therefore produced both source orders for every
distinct pair.

These are not findings that entered the implementation. They are coordinates
authored in the same change as the implementation.

### 4.3 Calculator pressure in the same commit

The calculator witness immediately invoked the new pair road. Its new test
required both arrangements:

```text
claim-side path finding, output-side position Assertion

output-side position Assertion, claim-side path finding
```

The test asserted both must appear and remain relation Unknown.

That is the exact shape the immediately preceding investigations had wanted to
make addressable without choosing A+B. The same commit supplied the rule and
proved the calculator now received those Candidates.

This establishes motivation. It does not establish constitutional warrant.

### 4.4 Unanswered rule coordinates

No earlier report established:

```text
why arity two is owed
why source position makes the two arrangements distinct Candidate subjects
why both arrangements are owed rather than one
why a source Assertion may not occupy both Act-local positions
why source order is the completion order
why arity three or higher is absent
```

The final pre-build report had expressly listed arity, roles, order, and
self-reference treatment as unrecovered. The pair commit filled each by direct
Book amendment.

## 5. Present status versus provenance

Two statements must remain separate:

```text
the active Book currently assigns these two rules

!=

these two rules were recovered from prior independent evidence
```

At the current tip, each rule is mechanically a Responsibility-local rule
coordinate. The Book directly assigns it; the runtime records it with an exact
Candidate Responsibility; replay uses it to determine required Candidate
subjects.

But its provenance is:

```text
operator/developer authored bounded rule
Book amendment
runtime implementation
calculator witness
all introduced together
```

Therefore the current rules are best classified as:

```text
current mechanical status:
    active Responsibility-local rules assigned by Book

recovery status:
    not independently recovered

historical function:
    bounded calculator-serving witness scaffolding
```

Subsequent dependence cannot repair that provenance.

## 6. What remains valid independently of the two Gs

The provenance defect does not erase every result produced during that
campaign. These distinctions remain independently supported by active law,
runtime validation, and later correction:

```text
Candidate can exist with represented relation Unknown

Candidate existence
!= represented relation Standing

one exact Candidate Responsibility can be local to one exact occurrence

an exact G must bound required Candidate subjects before completion is claimed

completion under G permits neither omission nor addition

Candidate production
!= Compare

Candidate
!= source Assertion

source Assertion
!= relation Standing
```

What no longer serves as clean constitutional precedent:

```text
unary enumeration of every source Assertion
pair enumeration
both source orders
distinct-source condition
event-order completion
the exact Measurement/Compare Assertion source species
specific arity ceiling
```

These remain active authored rules until the Book is separately corrected.
This investigation neither deletes nor amends them.

## 7. Selection audit

The proposed Selection layer is not available at the current tip.

Search of active Book chapters, `witness_grammar.json`, runtime, and tests finds
no constitutional Selection Responsibility, Act, basis, or result.

Older reports use Selection vocabulary. That report history is not active law.
The most direct local correction is `7c10c4e2`, *Remove the host chooser from
O3*. It replaced:

```text
Selection addresses none, some, or all supplied material
```

with:

```text
no selecting subject is established
every exact supplied-material occurrence faces its family-local
Responsibility and Applicability pressure
```

Therefore this investigation does not place Selection between Candidate
formation and later work.

The distinctions supported here are only:

```text
forming exact Candidates required by G
!= comparing exact Candidates under a Compare Responsibility
!= establishing a represented relation occurrence and Standing
```

No separate constitutional selecting Act is recovered. Historical phrases
such as `bounded candidate set`, `selection basis`, and `selected result` are
not imported.

## 8. What produces or warrants G?

The repository does not recover one generic producer for G, and this
investigation does not infer that one is needed.

The available classifications are:

### A. Direct Book assignment

This is how both current E.1 rules enter active physiology. The Book states
them, and an exact local Candidate Responsibility carries the applicable one.

### B. Derived from an independently established bounded Candidate surface

Not demonstrated for either E.1 rule. The pre-build investigation explicitly
said the surface and G were missing.

### C. Selection-side coordinate

Refused. Selection is not an active constitutional layer, and even the
historical distinction would begin after Candidates were already addressable.

### D. Responsibility-local authored rule

Mechanically accurate for the current E.1 rules. Their exact rule coordinates
are carried by exact Candidate Responsibilities. Their content was authored by
Book amendment rather than produced by an earlier Seed occurrence.

### E. Source testimony

Not demonstrated. Neither source material nor calculator output supplied the
unary or pair rule as an exact carried Assertion.

### F. Produced result

Not demonstrated. No preceding Act occurrence Yields either G.

The answer is therefore two-layered:

```text
what G is mechanically now:
    exact rule coordinate assigned by Book and carried by a local Responsibility

what warranted the content of the two existing Gs before Book assignment:
    unrecovered
```

## 9. Return to W

The W vacancy is differently located and epistemically larger than
`7945de52` stated.

It is smaller mechanically:

```text
once an exact G is legitimately available,
the existing Candidate production physiology shows how an exact local
Responsibility can owe and Yield every required neutral Candidate
```

It is larger constitutionally:

```text
the unary and pair Gs cannot serve as independently recovered precedent
for deriving a third G from W
```

Current Standing.E supplies the dimensions of an already exact relation
Assertion:

```text
first subject
exact relation content
second subject
```

W supplies three exact source-derived coordinate findings.

Nothing active establishes:

```text
equal cardinality requires correspondence
each source coordinate may occupy each Standing.E dimension
every coordinate must be used once
all six permutations are Candidate subjects
symmetry creates Candidate debt
enumerability creates Candidate debt
```

The present missing floor is no longer merely:

```text
where is the next Candidate rule?
```

It is:

```text
what independently warrants any exact Candidate surface
before one local Responsibility owes its completion?
```

The current repository answers that only by direct Book assignment for two
developer-authored cases. It gives no general derivation principle for W.

## 10. Required answers

### 1. Where did the unary Candidate rule come from?

It was directly authored in `c962a5c2` into Book, machine witness, runtime,
tests, and calculator witness. The immediately preceding report said G and its
source surface were unrecovered.

### 2. Where did the pair Candidate rule come from?

It was directly authored in `07625cad` into the same five surfaces. The only
intervening commit corrected the Candidate input role and supplied no pair-rule
warrant.

### 3. Were those rules recovered or authored?

Authored bounded design choices serving the calculator witness. They are active
Book assignments now, but not independently recovered constitutional
precedent.

### 4. What invariant Candidate-production responsibility remains?

Given an already exact G and exact local Responsibility, every Candidate G
requires must be produced with none omitted or added. Each Candidate may remain
relation Unknown.

### 5. Are Candidate formation, Selection, Compare, and relation Standing distinct?

Candidate production, Compare, and relation Standing are distinct. Selection
is not recovered as an active constitutional layer and therefore cannot occupy
one of these crossings.

### 6. What is G in current Seed?

For active E.1, G is an exact Responsibility-local rule coordinate directly
assigned by Book. It is not source testimony or a produced result. The warrant
for the content of the two current rules before their Book assignment is
Unknown.

### 7. How did the W vacancy change?

Mechanically smaller, because occurrence-local Candidate production under an
exact G is known. Constitutionally larger and differently located, because the
existing Gs do not demonstrate how a Candidate surface becomes warranted.

## 11. Stop

No new G is proposed.

No Book amendment or runtime implementation is warranted in this
investigation.

The exact next question is preserved without answering it:

```text
what independent evidence makes one bounded arrangement surface
the required Candidate subjects of one exact occurrence?
```
