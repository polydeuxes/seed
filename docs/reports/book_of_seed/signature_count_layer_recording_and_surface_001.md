# Signature-count recording, and what the surface discriminates: run 001

Roadmap item 1's recording half, item 4's remaining check, and item 5's gate.
Then two things item 5 did not ask for: what the twelve Compare coordinates
discriminate, and what the material behind the counts actually is.

**The three occurrences exist only in a working copy** at
`/tmp/claude-1000/sig_run.db`. The operator's Test Seed store is unchanged.

## What the material is

Sixteen bodies, **300 lines of each**, taken from the middle rather than the
start. 4,800 lines. One ingress occurrence is one line.

```text
  s01 grammar_goold_brown      s09 cookbook_farmer
  s02 roget_thesaurus          s10 french_les_miserables
  s03 grammar_kittredge        s11 latin_vulgate
  s04 webster_dictionary       s12 prose_austen_pride
  s05 algebra_rivenburg        s13 prose_dickens_copperfield
  s06 unmatched                s14 latin_vulgate
  s07 euclid_elements          s15 prose_emerson_essays
  s08 bash_abs_guide           s16 prose_hume_enquiry
```

One measurement takes an ordered pair of adjacent representations — `('sum',
'of')` — and asks the fixed four-question battery of the 300 lines: what
precedes the pair, what follows it, what else occupies the left position before
the pair's right member, what else occupies the right position after its left
member. The answer is a tally, `[{'the': 2}]`.

One Compare takes the same pair and the same question in **two different
bodies** and reports which of twelve coordinates are equal. One signature
records that same/different partition.

## What was recorded

```text
  recording occurrences        3
  produced Assertions          9        set 3, count 3, recurrence 3
  unique canonical ids         9
  duplicate identities         0
  integrity of new events      3 verified
  sqlite quick_check           ok
  total occurrences            1,164,283      (+3)
```

**[measured]** Item 5's stated expectation held exactly, and item 4's remaining
check passes. Identity continuation stops here, as item 5 said it would.

## Only 2 of the 12 coordinates discriminate this population

```text
   count   pos_meas  occupanc  standing  src_prov  respons  authority  unknowns  forbidden  scope  support  compl.b  compl.s
  12,228   DIFF      DIFF      same      same      same     same       same      same       DIFF   DIFF     DIFF     DIFF
   3,447   same      DIFF      same      same      same     same       same      same       DIFF   DIFF     DIFF     DIFF
     481   same      same      same      same      same     same       same      same       DIFF   DIFF     DIFF     DIFF
```

**[measured]** The three groups partition all 16,156 signatures, so a signature
splitting the other ten differently would have formed a fourth group. None did.

**[verified in code]** The six always-same coordinates are literal constants in
`record_adjacent_pair_result`: fixed `standing`, `source_provenance`,
`POSITIONAL_RESULT_FIDELITY_RESPONSIBILITY`, a fixed authority warrant, and fixed
`unknowns` and `forbidden_inferences` lists. Two result Assertions of this kind
cannot differ on them.

**[measured]** The four always-different are provenance and boundary
coordinates, and **all 1,281 traced comparisons cross sessions** — zero
same-session pairs. That is a property of this pairing topology. It is not that
those coordinates are incapable of sameness.

**Three senses of shape were being read as one.** This is the general lesson,
and it is curator's:

```text
  fidelity envelope        what must travel for the Assertion to stay bounded
  provenance shape         where and how this production exists
  discriminating shape     coordinates whose values can differ from material
```

Reading all three as one flat surface makes a 12-coordinate Compare look far
richer than it discriminates. **None of the ten should be dropped** — the six
constants are how a reader establishes the fidelity envelope was identical
rather than assumed, and the four provenance coordinates are what keep two
productions distinguishable.

### Three signatures was the whole reachable space

**[measured]** The different-sets are strictly nested: `{4} ⊂ {5} ⊂ {6}`.

**[verified in code]** They had to be. In `measure_occupancy`, `measured += 1`
and `counts[occupant] += 1` execute together on every occupied position, so the
occupancy counts always sum to `positions_measured`. Equal occupancies therefore
force equal `positions_measured`, and the fourth combination — positions
differing while occupancies match — is unreachable.

```text
  positions DIFF / occupancies DIFF     reachable
  positions same / occupancies DIFF     reachable
  positions same / occupancies same     reachable
  positions DIFF / occupancies same     impossible
```

**So "three canonical Assertion identities" was not a corpus discovery.** Under
this producer and this pairing topology, three is the entire reachable signature
space. **The empirical content is the distribution**: 12,228 / 3,447 / 481.

## What the 481 turned out to be

The 481 group was traced back through each signature's source Compare to the two
findings and their measured representations. All 481, not a sample.

```text
  368   76.5%   the pair occurs in NEITHER body
                positions_measured 0 and occupancies [] on both sides
  111   23.1%   occurs once in each, same neighbour, once
    2    0.4%   'sum' 'of' surrounded by 'the' twice in both bodies
```

**[measured]** The two are the same ordered pair measured from two directions —
`preceding` and `following`. **One fact, recorded twice.**

**[inference]** So of 16,156 comparisons across sixteen bodies, exactly one
agreement above a single occurrence was found. The 300-line window is why:
almost every ordered pair occurs zero or one times in it, so the battery mostly
has nothing to measure.

### The signature cannot tell agreement from mutual absence

**[measured]** `positions_measured` reads `same` whether both bodies measured
zero or both measured seven.

**[inference]** The values survive in the compared Assertions; the signature
records only the same/different partition and discards them. That is why 481
reads as agreement when three quarters of it is two bodies both lacking
something. This is a property of what a signature is, not a defect in the
Compare — but a reader taking 481 as a measure of agreement is reading a number
that does not carry it.

## The three recurrence Assertions

**[measured]** All three carry identical content — `{"recurrence_established":
true}` — and identical scope, and three distinct subjects.

**A subject is not incidental.** Each carries `measured_assertion_id`,
`signature_subject`, and the `exact_equality_signature` itself. So these are:

```text
  signature A recurs
  signature B recurs
  signature C recurs
```

and **not** the same claim three times. Same predicate is not same Assertion.
The finding is that **one recurrence predicate holds over three distinct bounded
subjects**, which is what a recurrence layer over a three-signature population
should produce.

## What this gives item 6, kept narrow

Item 6 asks what responsibly proposes two different recurrence Assertions to one
exact Compare, and forbids availability, equal count, both recurring, a shared
coordinate, similar-looking content, and a universal pair population.

**The warranted observation is small.** A Compare reading only the top-level
recurrence content would find `same` every time, because that content is one
constant. It would carry no discrimination.

**It does not follow that any lawful Compare between these Assertions is
vacuous.** No cross-subject Compare surface has been warranted for them. Their
subjects carry the exact equality signatures, which differ, so a future lawful
Measurement could have discriminating coordinates inside the subject. **That
road is Unknown**, and this is not an argument for surveying the wrapper because
it exists.

### Cost and warrant are two questions, not one

`#2480` recorded that at district scale the open question is what selects the
pairs, because comparisons go as n² in bodies. Item 6 asks what warrants two
subjects becoming proposed inputs. **These are related and they are not the
same.**

```text
  cost question         which pairs can be afforded?
  warrant question      what makes these two lawful inputs?
```

**[inference]** Collapsing them produces *the quadratic requires selection,
therefore this selection rule proposes the inputs* — downstream demand standing
in for upstream warrant, which is the failure the cardboard-city rule exists to
refuse. A responsible proposer may also relieve the scaling problem. Cost can
constrain a lawful proposal; cost cannot establish one.

## What this does not establish

**That the surface is wrong.** Ten of twelve coordinates carry fidelity and
provenance information that a reader needs. They do not discriminate, which is a
different finding.

**That the two varying coordinates are the right two.** Nothing here recovers
what a signature should measure.

**That 481 means agreement about anything.** `01.External:28` bounds a count to
the counting assertion, and three quarters of the 481 is mutual absence.

## The recording decision

Appending to the operator's Test Seed is one-way; the store refuses update and
delete by trigger.

The argument for is the layer's own: a finding that vanishes with the process is
one no later act can consume, which is what `#2368` was withdrawn for. The
argument against is that nothing currently consumes it, and item 5 says identity
continuation stops.

**The cardboard-city rule decides it.** Not recorded.
