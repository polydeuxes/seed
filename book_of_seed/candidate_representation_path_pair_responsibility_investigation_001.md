# Candidate Representation-Path Pair Responsibility Investigation 001

## Status and boundary

This is an investigation record outside active Book law.

It tests one question exposed by the read projection introduced at
`d1de8c8b` and corrected through `c249ccdb`:

```text
For every ordered-pair Candidate C(A, B),
what exact Responsibility, if any, owes every nested
representation path of A paired with every nested
representation path of B?
```

The investigation does not ask whether the projection is deterministic. Its
tests already establish deterministic order, exact replay, and no append. It
asks whether that projection is one constitutionally owed result.

The words `Cartesian product` and `path-pair projection` are explanatory
language in this record. They do not name active constitutional kinds.

## Result

No current active-Book Responsibility owes the nested representation-path
product.

The current exact distinction is:

```text
01.Source.E.1 Candidate debt
    every exact source Assertion required through B
    every distinct ordered source-Assertion pair required through B
    every Candidate required by those two exact Acts

implementation read projection
    every serialized dict/list path in first source material
    x
    every serialized dict/list path in second source material
```

The first boundary has an exact Responsibility, Act, Applicability,
Participation, Evidence, Yield, result, completeness replay, and Standing.
The second boundary has none of those coordinates. It is a deterministic,
read-only calculation over already recovered material.

Disposition:

```text
exact representation-path read                    implementation mechanism
cross-role path pairing                            implementation projection
Candidate completeness debt for that pairing      not established
relation between paired paths                      not established
represented_relation coordinate per Candidate     exact, material Unknown
```

## 1. Exact Candidate debt recovered by active Book

Active `01.Source.E.1` assigns this Seed two bounded Responsibilities at one
exact ledger boundary.

The first exact Act records one Candidate for each exact source Assertion in
event order. The second records one Candidate for each distinct ordered source
Assertion pair in first-role event order and then second-role event order.

The clause fixes:

- the eligible result-Assertion families;
- exact source Assertion references;
- source Locality and source Standing boundary;
- Evidence, Authority, Scope, limits, and Unknown;
- first and second source-Assertion roles for the ordered-pair Act;
- source Applicability and Participation in that Act;
- one complete Candidate result;
- the exact B and later result boundary C physiology;
- omission, addition, repetition, substitution, ordering, integrity, and
  partial-result refusal.

The clause does not name:

- a nested representation path as an Act input;
- a first-path or second-path role;
- intermediate container paths or leaf paths;
- an Act over path pairs;
- completeness of a path-pair result;
- a path-pair result occurrence or Standing;
- a relation between any two paths.

The Candidate source roles remain Assertion roles:

```text
first_source_Assertion
second_source_Assertion
```

They are not nested-path roles by identity.

## 2. What the runtime path reader actually does

`_exact_representation_paths` recursively visits Python representation
material.

For a dictionary it visits authored dictionary iteration order. For a list it
visits numeric list order. It records every encountered location as:

```text
path
material
```

The read includes intermediate dictionary/list material as well as leaf
material. It deep-copies what it reads.

This is exact for the serialized runtime representation supplied to the
reader. It does not establish that every visited location is a constitutional
coordinate.

That distinction was already recovered by `79a3721f`:

```text
exact representation path
!=
Book grammar coordinate
```

The runtime and test names were changed from `material_coordinates` to
`representation_paths` for that reason.

## 3. What the path-pair reader adds

For each already-recorded ordered-pair Candidate, the reader performs:

```text
for every first-role representation path
    for every second-role representation path
        expose the ordered pair of path records
```

After `c249ccdb`, the exact returned shape is:

```text
Candidate identity
one represented_relation coordinate carrying Unknown
all mechanically paired first-role and second-role paths
```

One Candidate therefore retains exactly one unresolved
`represented_relation` coordinate regardless of the number of path pairs.

The reader appends no event. It records no Responsibility assignment,
Applicability, Participation, Act Evidence, Evidence of Yield relation,
result, or Standing. SQLite restart reproduces the read because the source
Candidate and source Assertions are durably recoverable, not because the
path-pair projection has its own recorded occurrence.

## 4. Active Responsibility elimination

### 4.1 Candidate production

`01.Source.E.1` owes source-Assertion Candidates. It does not recursively
promote every serialized position inside each source Assertion into an Act
input or Candidate source role.

The exact B boundary freezes the source reality from which the clause's
source-Assertion enumeration may be replayed. B cannot enlarge that
enumeration rule by identity.

### 4.2 Representation

`01.Source.A` preserves exact source coordinates. Chapter 14 permits an exact
Representation to preserve an addressed source and established coordinates.
Neither clause assigns an Act that pairs every serialized path of two source
Assertions.

Preservation of A and preservation of B do not establish an A-path/B-path
pairing debt.

### 4.3 Measurement

`01.Source.D` bounds each declared Measurement to its exact rule and boundary.
Current declared Measurement families count or recover exact byte,
occurrence, position, recurrence, or addressed-reference findings. No active
Measurement rule enumerates arbitrary nested Python representation paths or
their cross-role pairs.

The existence of complete fan-out in those exact families cannot supply a new
Measurement rule by analogy.

### 4.4 Compare

`04.Compare.A` has exact earlier/later pair-Measurement inputs and its own
finding subjects. `04.Compare.B` has one exact ordered relation-path Assertion
and one exact recorded pair-finding comparison result under same-Locality and
source-occurrence requirements.

Neither Compare accepts one Candidate's nested representation paths as its
input surface. Reading two path records beside each other does not supply
Compare Applicability, Participation, an Act occurrence, or a finding.

### 4.5 Supplied relation material

`01.Source.F` permits supplied material to assert one exact relation from X to
Y while requiring responsible occurrences for the source and represented
relations. It explicitly refuses relation support from shape, repetition,
labels, Locality, or reference resolution.

It therefore cannot turn mechanically paired paths into established relation
participants or an established relation.

### 4.6 Fidelity

The first report boundary found that the Fidelity subject
`candidate_source_representation_path_order` had no exact
`grammar_coordinate_reference`. The explicit test-to-grammar-coordinate siren
correctly rejected that state; a Fidelity subject may not use an absent
reference to represent unresolved constitutional debt.

The follow-up removes that subject from witness grammar and declares the three
path-projection test functions explicitly as `WITNESSES`. The measurement hook
runs those pytest functions without recording them as Fidelity occurrences.
Structural collection coverage requires every pytest function to occur exactly
once in either one Fidelity subject or `WITNESSES` and rejects overlap,
repetition, or an undeclared function.

The existing tests establish that the implementation projection is ordered,
exactly reproducible, and read-only. Fidelity to that implementation behavior
does not assign this Seed a path-pair production Responsibility.

## 5. Completeness boundaries remain distinct

Candidate completeness is recoverable as:

```text
B
-> exact source-Assertion enumeration of E.1
-> exact unary or ordered-pair Candidate Act
-> every Candidate owed by that Act
-> recorded result through C
-> replay refusal when expected and recorded Candidate coordinates differ
```

The path projection currently has only:

```text
exact Candidate result
-> exact source Assertion material
-> serialized paths
-> nested runtime loops
-> returned Python value
```

There is no exact path source boundary distinct from the recovered Assertion
material, no path enumeration grammar, no path-pair Act, and no recorded
result boundary for the projection.

Therefore:

```text
Candidate result complete through C
!=
path-pair projection constitutionally owed through C
```

The fact that a Python loop visited every current path does not establish a
constitutional completeness finding.

## 6. Growth pressure

For one Candidate whose first source material has `P` visited representation
paths and whose second source has `Q`, the current helper materializes `P * Q`
path pairs and deep-copies both path records.

For `N` source Assertions, the ordered-pair Candidate Act already produces
`N * (N - 1)` Candidates. Candidate Assertions can enter a later source
surface, so both `N` and the nested material sizes may grow across later
production boundaries.

This does not warrant a silent cap. A cap would be unlawful if a future exact
Responsibility owed the full product. It instead reinforces the present
boundary:

```text
do not make downstream Standing depend on this materialized projection
until its exact debt is independently recovered
```

The current focused implementation witness remains bounded. Its bounded cost
does not establish a general constitutional obligation.

## 7. Vacancy for any future path-pair Act

Before path pairing can become load-bearing, an exact assignment would need to
recover at least:

- the responsible boundary;
- exact Authority;
- the source subject and frozen boundary;
- whether paths are representation locations, grammar coordinates, or another
  exact species;
- whether intermediate containers, leaf material, or both belong;
- first and second path roles;
- ordering, repetition, and empty-source treatment;
- Applicability of each proposed input;
- Participation in the exact Act;
- the exact Act and occurrence;
- Evidence and Evidence of Yield relation;
- the exact result and result boundary;
- the completeness rule and restart replay;
- Scope, limits, provenance, conflicts, and Unknown;
- what the Act establishes neither about the Candidate's represented relation
  nor about any paired material.

No current active clause supplies that physiology.

## 8. Answer

The current path-pair helper is retained as a deterministic, non-mutating read
projection over exact already-recovered material. It is useful implementation
testimony, carried by explicit Witnesses, that no serialized path pairing is
hidden by a developer-selected read.

It is not currently a Candidate Act result, Candidate completeness debt,
Measurement, Compare, Representation result, or established relation surface.

The smallest exact disposition is:

```text
retain as non-mutating Witnesses
preserve one represented_relation coordinate per Candidate
do not give path pairs grammar-coordinate Standing
do not make a later Responsibility depend on path-pair completeness
current active-Book owning Responsibility: not established
future exact owning Responsibility: Unknown
```

## What this investigation does not establish

- That the path-pair projection must be deleted.
- That it must be retained as constitutional machinery.
- That every runtime representation path is a Book coordinate.
- That every first-role path is related to every second-role path.
- That paired paths are endpoints of the Candidate's represented relation.
- That one path pair owns a represented-relation vacancy.
- That shape, repeated material, or matching path text supplies a relation.
- A generic fan-out, discriminator, comparator, Cartesian-product, or brute-
  force constitutional kind.
- Equality, identity, membership, classification, predication, similarity, or
  meaning.
- Authority for the next calculator crossing.
