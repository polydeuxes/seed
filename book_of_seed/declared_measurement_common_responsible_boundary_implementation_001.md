# Declared Measurement common responsible boundary implementation 001

## Question

The previous investigation found two distinct declared Measurements:

```text
one exact acquisition-result occurrence
↓
position-coordinate Measurement

one complete ordered acquisition-result set
↓
exact-byte Measurement
```

Neither Measurement reads the other Measurement's assignment, Act, Yield, or
result to determine its own exact subject or finding.  The runtime nevertheless
placed them in numeric declaration order and advanced the boundary before
discovering the next subject.

This implementation asks whether the two assignments can preserve one exact
earlier responsible boundary while their occurrence records remain in one
durable sequence.

It does not establish positive assignment Standing.  It does not make bounded
Locality replay identical to Standing.  It does not make raw Witness material a
Measurement subject.

## Active sources

- `01.Source.D`
- `01.Source.E.1`
- the two declared Measurement coordinates in Witness Grammar
- position-coordinate Measurement assignment and replay
- exact-byte Measurement assignment and replay
- declared Measurement recording

## 1. One boundary can address more than one Responsibility

Active `01.Source.E.1` already assigns two bounded Responsibilities at one
exact boundary.  Active grammar therefore does not impose:

```text
one exact boundary
↓
at most one Responsibility assignment
```

The earlier `01.Source.D` sentence requiring every new occurrence to enter the
moving read before another assignment was added together with the numeric host
order.  It was not an independently recovered general rule of Standing.

The amended `01.Source.D` now preserves this narrower distinction:

```text
one exact responsible Standing boundary B
├── exact subject A and required coordinates
└── exact subject B and required coordinates

↓

assignment A carries B
assignment B carries B
```

Before either exact Act occurs, the current read must carry that Act's own
Responsibility assignment.  This does not require the later assignment to use
the earlier assignment or result as an input.

## 2. Complete exact subjects are recovered once through B

The numeric declaration coordinates and `min(eligible)` chooser are removed.
The declaration reader now freezes one exact bounded Locality replay through B
and recovers every exact unassigned subject for each declared Measurement from
that same replay:

```text
bounded Locality replay through B
├── every exact position-coordinate Measurement subject
└── the complete exact-byte Measurement subject, when present
```

It records each resulting occurrence in one durable sequence because the
writer appends one occurrence at a time.  It does not rediscover later subjects
from a replay advanced through an earlier Measurement lifecycle.

Thus:

```text
durable occurrence order
!=
input relation between declared Measurements
```

## 3. Assignment coordinates preserve the earlier boundary

Each position-coordinate assignment validates its source against the frozen
replay through B and records B as its responsible Standing boundary.

The exact-byte assignment separately validates:

```text
source set through B
=
source set still available before append
```

It records both:

```text
responsible Standing boundary = B
completeness boundary          = exact append prefix through B
```

The second coordinate matters.  Retaining the moving append prefix would have
made an earlier Measurement result part of the later assignment even after the
responsible Standing boundary was corrected.

## 4. Reversing the durable sequence does not revise the responsible boundary

The test replaces the declaration sequence with its reverse.  Result
occurrences are durably recorded in the reverse sequence, but every assignment
still preserves the same earlier responsible boundary B.  The exact-byte
assignment also preserves the same completeness boundary through B.

Therefore:

```text
position then byte
```

and:

```text
byte then position
```

remain different durable occurrence sequences without either sequence making
the first Measurement a required input to the second assignment.

## 5. Boundaries retained

Established as runtime testimony:

```text
numeric declaration order removed                         yes
one-scalar subject shape removed                          yes
complete exact subjects recovered once through B          yes
all assignments preserve B                               yes
exact-byte completeness preserves the prefix through B    yes
recording sequence can reverse without revising B          yes
```

Not established:

```text
positive Standing for each Responsibility assignment      no
bounded Locality replay equals Standing                   no
raw Witness availability supplies 01.Source.D             no
Python declaration coordinate maps to Seed-native Act     no
complete traversal of every Book Responsibility           no
```

The declaration tuple remains external runtime testimony binding two active
Book declarations to two Python roads.  This implementation removes its
numeric chooser and its one-occurrence-per-moving-boundary rule.  It does not
promote that tuple into a Seed-native traversal mechanism.
