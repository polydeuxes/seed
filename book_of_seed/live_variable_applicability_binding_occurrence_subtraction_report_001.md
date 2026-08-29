# Live variable Applicability binding occurrence subtraction report 001

## Result

The active same-position family now records one Applicability Act for every
exact member of:

```text
S(B) × C(B)
```

where:

```text
S(B) = current shared-position Measurement results through B
C(B) = current recorded-pair Compare results through B
```

The active sequence is:

```text
one exact S(B) × C(B) member
        ↓
Applicability Act occurrence
        ↓
applicable | inapplicable
        ↓ when applicable
Compare Act occurrence
        ↓
Compare result occurrence
```

The prior active sequence appended two additional events before each
Applicability Act:

```text
Compare binding occurrence
Applicability binding occurrence
```

Both are absent from new inward histories. Their public constructors and
readers remain as authored-history controls.

## Exact question coordinates

The Applicability Act carries:

```text
one shared-position result-position reference
one recorded-pair Compare result reference
the addressed Compare Act identity
Locality
through-occurrence boundary
```

Its result addresses that Act occurrence and records the variable distinction:

```text
same source occurrence
two exact pair-finding counts
applicable | inapplicable
```

The Compare Act occurs only for a positive result. It carries its exact
subjects without a binding-event reference. Its result does the same. The
recorded Act and result occurrence identities address those exact
occurrences. Neither Applicability branch carries identities for a Compare
occurrence or result that has not occurred.

## Exhaustive coverage

For two exact members in `S(B)` and two exact members in `C(B)`, the active
family records:

```text
4 Applicability Act occurrences
4 Applicability results
2 applicable
2 inapplicable
2 Compare Act occurrences
2 Compare results
```

No cross-set member is omitted. Rerunning each stage records no duplicate Act
or result. Host iteration is mechanics; the exact bounded members plus one
Applicability Act for each member establish coverage.

## Independent states preserved

Focused controls preserve:

```text
no Applicability occurrence
Applicability Act with result absent
Applicability result = inapplicable
Applicability result = applicable with Compare Act absent
Applicability result = applicable with Compare Act present
Compare Act with result absent
Compare result present
```

Absence is therefore not collapsed into `inapplicable`, and a positive answer
is not collapsed into the addressed Compare occurrence.

## Refusals preserved

The new active readers still refuse:

```text
changed exact input result
changed result-local or finding coordinate
changed source occurrence
changed lifecycle identity
changed Locality or boundary
second result for one Act
Compare occurrence after an inapplicable result
repeated Compare occurrence for one positive result
```

Current-coordinate replay and SQLite restart reconstruct the new events from
their exact subjects. Older authored Ledgers continue through their binding
readers; the two histories are validated independently.

## Finding

```text
variable Applicability distinction                 survives
Applicability Act occurrence                       survives
Compare binding occurrence before Applicability    fails active subtraction
Applicability binding occurrence                   fails active subtraction
exact bounded cross-set coverage                   survives
positive-only Compare occurrence                   survives
authored binding lifecycles                        retained as controls
```

Binding remains an exact coordinate relation. Neither active binding needs a
separate occurrence before Applicability can answer the exact question.
