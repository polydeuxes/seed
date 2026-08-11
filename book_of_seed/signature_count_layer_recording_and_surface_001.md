# Signature-count recording, and what the surface actually carries: run 001

Roadmap item 1's recording half, item 4's remaining check, and item 5's gate.
Then one thing item 5 did not ask for, which is the reason its gate should hold.

**The three occurrences exist only in a working copy** at
`/tmp/claude-1000/sig_run.db`. The operator's Test Seed store is unchanged.
Whether to record into it is a separate decision, taken below.

## What was recorded

`record_equality_signature_count_layer` over the 16,156-signature population,
63 s, three occurrences appended.

```text
  recording occurrences        3
  produced Assertions          9        exact_production_set 3, count 3, recurrence 3
  unique canonical ids         9
  duplicate identities         0
  integrity of new events      3 verified
  sqlite quick_check           ok
  total occurrences            1,164,283      (+3)
```

**[measured]** Item 5's stated expectation — nine produced Assertions, nine
unique canonical identities — held exactly. Item 4's remaining check passes.
**Identity continuation stops here**, as item 5 said it would.

## Item 5's gate holds for a stronger reason than nine

Nine unique identities does not mean nine distinct things were said.

```text
                        subject      scope       content
  exact_production_set  3 distinct   identical   3 distinct
  count                 3 distinct   identical   3 distinct
  recurrence            3 distinct   identical   IDENTICAL
```

**[measured]** All three recurrence Assertions carry the same content —
`{"recurrence_established": true}` — and the same scope. They are distinguished
only by subject.

**[inference]** So the recurrence stratum says one thing three times. The
identities differ because the subject is hashed into them, not because three
different findings were made. A survey of that stratum would be counting hash
inputs.

## The 12-coordinate surface carries 2 coordinates

The signature partitions a 12-coordinate Compare surface into same and
different. Across the whole population:

```text
   count   positions_  occupanci  standing  source_p  responsi  authorit  unknowns  forbidde  scope  support  compl.b  compl.s
  12,228   DIFF        DIFF       same      same      same      same      same      same      DIFF   DIFF     DIFF     DIFF
   3,447   same        DIFF       same      same      same      same      same      same      DIFF   DIFF     DIFF     DIFF
     481   same        same       same      same      same      same      same      same      DIFF   DIFF     DIFF     DIFF
```

```text
  always same (6)       standing, source_provenance, responsibility,
                        authority_warrant, unknowns, forbidden_inferences
  always different (4)  scope, support_basis, completeness_boundary,
                        completeness_scope
  varies (2)            positions_measured, occupancies
```

**[measured]** The three groups partition all 16,156 signatures, so a signature
splitting those ten differently would have formed a fourth group. None did.

**[verified in code]** The six are **literal constants** in the producing
function. `record_adjacent_pair_result` writes `standing: "measured"`,
`source_provenance: "preserved operator-ingress occurrences"`,
`POSITIONAL_RESULT_FIDELITY_RESPONSIBILITY`, a fixed authority warrant, a fixed
`unknowns` list and a fixed `forbidden_inferences` list. Two result Assertions of
this kind cannot differ on them.

**[verified in code]** The four are per-occurrence provenance —
`assertion_scope` carries `session_id`, `completeness_scope` carries workspace,
session and kind, `support_basis` carries the consumed occurrence identities,
`completeness_boundary` carries the prefix commitment. Every compared pair spans
two bodies and therefore two sessions, so all four differ by construction.

**Ten of twelve coordinates are determined before any material is read.**

### And the three groups were not free to be anything else

**[measured]** The different-sets are strictly nested:
`{4} ⊂ {5} ⊂ {6}`.

**[inference]** They had to be. `positions_measured` is the number of positions
measured and `occupancies` is the tally over them, so the occupancy counts sum to
`positions_measured`. Two productions differing in `positions_measured`
necessarily differ in `occupancies`. The fourth combination — positions differing
while occupancies match — is unreachable.

**So "three canonical identities" is forced by the encoding.** Two varying
coordinates with one implying the other admit exactly three signatures, and
exactly three occurred. The count was not a discovery about the corpus.

**What is empirical is the distribution**: 12,228 / 3,447 / 481. That is a fact
about the sixteen bodies. It says that in 481 of 16,156 Compares the two
productions measured the same number of positions *and* found the same occupancy
tally, and in 12,228 they agreed on neither.

## What this means for item 6

Item 6 asks what responsibly proposes two different recurrence Assertions to one
exact Compare, and forbids availability, equal count, both recurring, a shared
coordinate, similar-looking content, and a universal pair population.

**The measurement adds a reason the gate should stay shut that is not on that
list.** The three recurrence Assertions are content-identical. A Compare across
any two of them would return `same` on content and `different` on subject, for
every pair, every time — because that is what the encoding guarantees, not
because of anything in the material.

**[inference]** So the proposer question is not the only thing missing. Even
granting a lawful proposer, the Compare it fed at this layer would be vacuous.
Recovering the proposal boundary is worth doing on its own terms; it is not what
would make this stratum say something.

**This is the same unrecovered thing as the register's open question.**
`#2480` recorded that at district scale the open question is *what selects the
pairs*, because comparisons go as n² in bodies. Item 6 asks what proposes two
subjects to one Compare. Those are one question seen from the cost side and from
the warrant side.

## What this does not establish

**That the surface is wrong.** Six constant coordinates are how the layer
declares its own limits, and carrying them into the Compare is what lets a reader
confirm the limits were identical rather than assumed. The finding is that they
carry no *discriminating* information, not that they should be dropped.

**That the two varying coordinates are the right two.** Nothing here recovers
what a signature should measure. It measures what this one does.

**That 481 means agreement about anything.** `01.External:28` bounds a count to
the counting assertion. Two productions agreeing on a position count and an
occupancy tally have agreed on a position count and an occupancy tally.

## The recording decision

The three occurrences are in a copy. Appending to the operator's Test Seed is
one-way — the store refuses update and delete by trigger — so it is left to the
operator rather than taken.

**[inference]** The argument for recording there is the layer's own: a finding
that vanishes with the process is one no later act can consume, which is what
`#2368` was withdrawn for. The argument against is that nothing currently
consumes it, and item 5 says identity continuation stops. Recording it preserves
a finding for a consumer that does not exist yet, which is the pattern the
cardboard-city rule refuses.

**The rule decides it.** Do not record into the durable store until an act
consumes it.
