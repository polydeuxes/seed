# Recurrent-pair position constraint decomposition investigation 001

## Question

What distinction is protected by each current recurrent-position constraint:

```text
same invocation Locality address
caller-supplied recurrence Assertion addresses
caller-supplied positive integer occurrence limit
```

This investigation changes no Book, witness grammar, runtime, or test.

## Direct disposition

| current implementation constraint | protected distinction | disposition |
|---|---|---|
| pair result and later acquisition have equal `locality_identity` values | exact current Standing and Scope carry both addressed subjects | the equality check is a conservative implementation of the distinction, not the distinction itself |
| caller supplies `recurrence_assertion_identities` | each subject is an exact recurrence Assertion from the addressed pair result, without duplicates or crossed support | exact addressing is required; developer enumeration is not established |
| caller supplies positive `occurrence_limit` | the result preserves its applied bound and known loss instead of silently discarding findings | an exact bound is real when the result is partial; caller provision and positive-integer form are implementation choices |

The prior activation investigation promoted all three current forms into live
constitutional prerequisites. That conclusion was too strong.

## Active Book boundary

Active `01.Source.D` requires a declared Measurement Responsibility as a branch
of current Standing with its exact subject and required coordinates. A result
preserves its exact rule, subjects, source occurrences, completeness boundary,
Scope, Locality, limits, conflicts, findings, and Unknown.

Active law does not say:

```text
both subjects must carry equal invocation-Locality addresses
limits must be a caller-supplied integer
the caller must enumerate the subject population
```

The specialized recurrent-position entry that named `Locality`,
`completeness_boundary`, and `occurrence_limit` together was removed from the
machine grammar by `f956b6fd` when the active Book was reduced to the common
Measurement grammar. Runtime and tests retained the specialized implementation.

That history does not make the retained fields false. It does mean each field
must be tested for the exact work it performs rather than read back into the
Book as law.

## Locality equality

### Current enforcement

`_measurement_source_position_coordinates` currently requires:

```text
pair result locality_identity
=
later acquisition locality_identity
```

It then:

- proves pair-result-before-acquisition order inside that Locality;
- proves both occurrences are inside the supplied completeness boundary;
- records the Responsibility, Act occurrence, and result in the acquisition
  Locality;
- requires current Locality Standing to carry both exact inputs.

The later Standing checks independently require the pair Measurement and later
acquisition to appear in the same Locality-scoped replay. Removing the first
equality test would therefore not create a lawful cross-Locality road. The
Responsibility recording would still lack current Standing carrying both
subjects.

### Protected distinction

The equality test prevents an exact recurrence Assertion in an unrelated
Locality from being borrowed merely because its address exists in the ledger.
It is a compact proxy for:

```text
current Standing at the responsible boundary
├── exact recurrence Assertion through pair result P
└── exact later acquisition M

Scope and Locality of the Measurement address P and M together
```

This protects bounded subject carriage and source crossing. It does not
establish a universal rule that every Measurement subject must originate at
the same invocation Locality.

Both acquisitions carrying:

```text
exact material --Locality--> this Seed
```

does not by itself put their results into the same current Standing or Scope.
Exact source references, provenance, and the material-to-this-Seed Locality
relations preserve the inputs, but they do not create the missing
cross-Locality Standing work.

### History

`814c3806` introduced the equality check, its refusal test, and the specialized
machine-grammar Locality bound together. History contains no earlier separate
Responsibility from which equality of invocation addresses was recovered.
`6062bb09` migrated the source from Ingest to source-specific material
acquisition while preserving the check unchanged.

The test `test_distinct_locality_and_pre_source_boundary_are_refused` therefore
proves the current implementation contract. It does not independently prove
that equal invocation addresses are the constitutional relation.

### Consequence for repeated `!cat`

Separate ordinary invocations produce separate invocation Localities. Current
Standing in the later Locality does not carry the earlier pair result. No
current Standing Locality continuation or Assertion Locality movement road
carries this recurrence subject across that boundary.

The repeated sixteen-book experiment therefore remains blocked across its two
ordinary invocations. The reason is not that unequal strings are forbidden by
law. The exact subjects are not together under the current responsible
Standing and Scope.

## Recurrence subject addresses

### The population is already bounded by the pair result

The addressed pair Measurement result `P` already carries:

```text
every exact pair count Assertion produced by P
every exact recurrence Assertion produced by P
the count support of each recurrence Assertion
the exact source occurrence population
the exact completeness boundary
```

The later acquisition result `M` is also returned as an exact occurrence. The
local subject frontier is therefore:

```text
P
├── recurrence Assertion R1
├── recurrence Assertion R2
└── ...

+ later exact acquisition M
```

No global ledger search is required to recover the recurrence population.
Filtering the exact Assertions carried by `P` for the already-established
`recurrence` result yields that population.

### What the caller tuple actually does

The bulk function validates that every supplied address:

- belongs to the same exact pair result;
- addresses a recurrence Assertion rather than its count support;
- retains the exact count support for the same pair material;
- appears without duplication;
- remains inside the exact result boundary.

Those are real exact-address distinctions.

The function does not prove that the supplied tuple is the complete recurrence
population carried by `P`. The caller can provide a strict subset. Thus the
tuple currently combines two different jobs:

```text
validate exact addresses
+
let the developer choose which addresses enter this call
```

Only the first job is independently established.

### History

`b4e73f38` added the bulk tuple so the pair result, later acquisition, byte
position index, order, and boundary could be read once for several recurrence
subjects. The commit was a bounded-read correction. `e8fe832a` renamed the
former fan-out language as same-boundary pair subjects. Neither commit added an
independent rule that the caller determines the population.

### Remaining distinction

`P` and `M` being available does not itself establish Applicability,
Participation, or an Act occurrence. Existing tests demonstrate the
Measurement after exact addresses are supplied. They do not demonstrate live
exhaustion of every recurrence Assertion carried by `P` against `M`.

The correct live question is therefore narrow:

```text
current Standing and Scope carry exact P and M
↓
does the existing recurrent-position Responsibility address
the recurrence Assertion population carried by P against M?
```

It is not:

```text
how does the runtime search the complete ledger?
```

## Occurrence limit

### Exact material is a finite mathematical bound

For exact material `M`, byte-position populations are finite. The existing
rule calculates the full available count for a recurrent pair from the two
byte-position populations, excluding a repeated scalar position when both
bytes are equal.

Using the complete finite population would need no externally chosen cap and
would carry no known loss.

### Finite does not mean practical

For the 218,058-byte sixteen-book value, the current rule produces these
mathematical populations before any cap is applied:

| coordinate | count |
|---|---:|
| distinct observed adjacent pairs | 2,708 |
| recurrent pair subjects | 2,162 |
| available ordered position findings across those subjects | 39,175,638,934 |
| largest subject, space followed by space | 1,492,315,530 |

The exact material and Measurement rule therefore establish finiteness, but
they do not make exhaustive durable recording operationally reasonable.

These counts were calculated directly from the exact corpus bytes and the
recurrent adjacent-pair population already reported by the experiment. The
calculation appended no Seed occurrence.

### Protected distinction

The current `occurrence_limit` performs real work when a result carries less
than the available population:

```text
available occurrence count
applied result bound
exact carried findings in source iteration order
known loss beyond the applied bound
```

`test_occurrence_limit_is_explicit_and_preserves_exact_known_loss` proves that
a bound of `2` carries two of four available findings and records the known
loss. Removing the bound while silently retaining a prefix would erase a real
distinction.

The protected distinction is therefore bounded partial Measurement with exact
known loss. It is not:

```text
a developer must supply a positive integer to every invocation
```

The active Book requires exact limits. Its source and result roads preserve
known loss where that coordinate is established. It does not choose the
integer form, the value, or the caller as source. The current function
parameter is an implementation of that bounded-result distinction.

### History

`814c3806` introduced the integer parameter, truncation behavior, known-loss
test, and specialized machine-grammar coordinate together. Tests use `16` for
ordinary fixtures and `2` for the explicit known-loss case. No history gives
`16` independent force for live material.

`f956b6fd` removed the specialized `occurrence_limit` entry from active machine
grammar while retaining generic Measurement limits. This leaves the real
bounded-result distinction intact without making the current parameter shape
constitutional.

## Corrected stopping boundary

The demonstrated same-Locality `tatatata` path remains exact:

```text
pair Measurement P
→ recurrence Assertions carried by P
+ later same-Locality acquisition M
→ recurrent-position results
→ shared-position result
→ ordered_relation_path
```

Its current test-bench invocation supplies exact addresses and a cap of `16`.
Those supplied values prove the physiology; they do not prove that live Seed
must receive them from a developer.

The live boundary now decomposes as follows:

```text
real distinction:
current responsible Standing and Scope must carry the exact subjects

current implementation:
requires equal invocation-Locality addresses

real distinction:
each recurrence subject must be exact and retain its pair-result boundary

current implementation:
caller enumerates recurrence Assertion addresses

real distinction:
a partial result must preserve its exact applied bound and known loss

current implementation:
caller supplies a positive integer occurrence_limit
```

No runtime correction follows merely by deleting those checks. The next live
slice must preserve the real distinctions while refusing to grant the current
parameter shapes constitutional force.
