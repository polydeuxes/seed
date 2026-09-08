# Operator checkout Preservation coordinate investigation 001

## Question

Does the exact operator material occurrence supplying `/checkout` become an
exact coordinate of the Preservation physiology that records a destination
Locality relation?

The checkpoint Recording subtraction left this boundary open:

```text
exact `/checkpoint` operator material occurrence Q
        ↓
Preservation binding
        ↓
Preservation Act occurrence
        ↓
Locality relation result occurrence
```

The console performs that physiology after receiving `/checkout`. This does
not by itself show that the `/checkout` occurrence is a subject, relation,
Act, or result coordinate.

This investigation changes no runtime road, Book clause, event kind, Act,
result kind, or admitted word.

## Rosetta boundary

The following words describe operator-interface mechanics in this report:

```text
checkpoint
checkout
command
request
invocation
decompile
```

They acquire no Book coordinate here.

`Preservation`, `Locality`, `Act`, `occurrence`, `result`, `subject`, `exact`,
and `current` retain their Book meanings. In particular, `current` means
present in an exact Locality reading through an addressed occurrence boundary.

The report uses `decompile` only for the laboratory operation of separating
the console behavior into its exact runtime steps. Decompiled behavior is not
an additional Seed occurrence.

## Runtime decomposition

The console records every supplied slash command first as ordinary exact
operator material:

```text
operator source Act occurrence
        ↓
exact operator material result
```

For `/checkout`, operator mechanics then performs these host steps:

```text
exact `/checkout` bytes
        ↓
slash-command parser validation
        ↓
empty OperatorCheckoutRequest host value
        ↓
call Preservation binding writer with current coordinates
        ↓
call Preservation Act writer
        ↓
call Locality relation result writer
```

`OperatorCheckoutRequest` carries no occurrence identity, material-result
reference, Locality, subject, Act, result, or boundary coordinate. It is an
in-memory control value and is never appended to the Ledger.

The Preservation writers accept no checkout occurrence reference. Their
exact inputs are:

```text
binding writer:
    source current coordinates

Act writer:
    exact Preservation binding occurrence
    destination current coordinates

result writer:
    exact Preservation Act occurrence
```

The binding writer validates the material-result coordinates supplied in the
source reading. It requires exactly one current boundary carrier. An exact
operator material occurrence supplying `/checkpoint` can be that carrier.

## Falsifier

Hold the checkpoint material occurrence `Q` and Preservation physiology
constant while varying whether an exact `/checkout` material occurrence
exists.

```text
history A
    Q recorded
    no `/checkout` occurrence
    host calls the exact Preservation writers

history B
    Q recorded
    `/checkout` recorded
    console calls the same Preservation writers
```

For both histories require:

```text
Preservation binding occurrence
Preservation Act occurrence
Locality relation result occurrence
relation subject resolves to Q
relation boundary resolves through Q
relation reader validates every addressed coordinate
```

Then ask whether the `/checkout` occurrence identity is an exact coordinate of
the binding, Act, or result in history B.

This is not a content-equality comparison between separate Ledgers. Each
history is validated through its own exact occurrence references. The
comparison concerns the coordinate shapes recorded by the two histories.

## Experiment

### A. Preservation without a checkout occurrence

One Ledger receives only:

```text
/checkpoint\n
```

The resulting current coordinates address `Q`. Calling the public
Preservation writers with those coordinates records, in order:

```text
operator.recorded_boundary_locality_subject_to_act_binding_recorded
operator.recorded_boundary_locality_act_occurrence_recorded
operator.recorded_boundary_locality_recorded
```

The result reader validates the Locality relation. Its through-occurrence
boundary reference is exactly:

```text
{"recorded_occurrence_identity": Q}
```

No `/checkout` occurrence exists in this Ledger.

### B. Console-driven Preservation

A separate Ledger receives:

```text
/checkpoint\n
/checkout\n
```

The console records both exact material results and then records the same
three-kind Preservation lifecycle in the destination Locality.

The result reader again resolves its through-occurrence boundary reference to
`Q`. The exact `/checkout` material-result occurrence identity does not occur
in the validated binding, Act, or result coordinates.

### C. Absence of console invocation

When the console receives `Q` without `/checkout`, the console records no
Preservation lifecycle. This distinguishes two host behaviors:

```text
console receives no `/checkout` material
    → console does not call the Preservation writers

console receives exact `/checkout` material
    → console calls the Preservation writers
```

That host-control difference does not make the command occurrence a subject
of the resulting Act. The exact Act occurrence is the constitutional fact
that Preservation occurred.

## Exact distinction

The experiment separates:

```text
operator material changes console control flow
```

from:

```text
operator material is an exact subject coordinate of Preservation
```

The first is observed. The second is false for the current physiology.

Likewise:

```text
no `/checkout` supplied to the console
    → no Preservation occurrence from that console run
```

does not mean:

```text
`/checkout` occurrence
    → required coordinate of every exact Preservation occurrence
```

The no-checkout experiment supplies the counterexample.

## Result-to-later-Act composition

The positive constitutional composition remains:

```text
exact operator material result Q
        ↓ addressed as subject
Preservation Act occurrence
        ↓
Locality relation result occurrence
```

`Q` becomes operative because the Preservation physiology addresses it as an
exact subject. Co-current material alone implies no Preservation Act, and the
console command that causes the host to call the writer does not become a
second subject.

This preserves the prior result-use census:

```text
recorded result
!=
subject of a subsequent Act
```

and adds:

```text
host command causing a writer call
!=
subject of the recorded Act
```

## No Request coordinate

The current runtime has no durable Request occurrence:

```text
OperatorCheckoutRequest        empty host value
request occurrence             absent
request result                 absent
request-to-Act relation        absent
checkout occurrence reference absent from Preservation
```

This investigation therefore provides no evidence for admitting `Request`,
`Invocation`, `Use`, `Play`, or `Understanding`.

The absence of a prior Request occurrence creates no producer regress. The
Preservation Act occurrence records that the exact Act occurred. Another
occurrence is required only when an independently variable coordinate must be
preserved; none was found here for `/checkout`.

## Results

```text
complete Preservation lifecycle without `/checkout`     yes
complete Preservation lifecycle through console          yes
validated subject in both histories                       Q
validated boundary in both histories                      through Q
`/checkout` exact material occurrence in console history  yes
`/checkout` occurrence referenced by Preservation         no
empty request host value appended to Ledger                no
new Book coordinate                                        no
new runtime occurrence                                     no
```

## Finding

The operator word `/checkout` is interface shorthand whose exact material can
change console control flow. It is not an exact coordinate of the current
Preservation binding, Act occurrence, or Locality relation result.

The constitutional road is:

```text
Q + Q boundary + Preservation + destination Locality
        ↓
Preservation Act occurrence
        ↓
Locality relation result occurrence
```

No connective Request or Invocation occurrence is missing between `Q` and the
Act.

## Disposition

Retain `/checkout` as operator-interface mechanics. Do not admit it, Request,
Invocation, Use, or Decompile into Book grammar from this evidence.

Leave the exact Preservation lifecycle unchanged in this investigation. Its
separate binding occurrence, prospective lifecycle identities, and copied
coordinates remain independent subtraction questions.
