# Live Compare Act subject copy subtraction report 001

## Question

Does the active Compare Act need to repeat its two exact subjects when it also
addresses one exact positive Applicability result?

The reference chain before subtraction is:

```text
Applicability Act occurrence
    exact shared-position result-position reference
    exact recorded-pair Compare result reference
    Applicability
    addressed Compare

Applicability result occurrence
    exact Applicability Act occurrence reference
    applicable

Compare Act occurrence
    copied exact subjects
    exact positive Applicability result occurrence reference
    Compare
```

## Falsifier

Remove only the Compare Act `subject_reference`.

Keep the exact positive Applicability result reference and follow it through
its exact Act occurrence to recover both subjects. Preserve positive-only
Compare, occurrence order, restart, replay, finding coordinates, later
Distinction Measurement, and subject-mutation refusal.

## Result

The active Compare Act now carries:

```text
Compare
exact positive Applicability result occurrence reference
Locality on the occurrence
```

Its reader follows:

```text
Compare Act
→ positive Applicability result
→ Applicability Act
→ exact two subjects
```

The Applicability result must remain positive, its Act must address Compare,
and the reconstructed subjects must establish the applicable relation. A
changed occurrence reference or changed subject coordinate is refused through
the same chain.

## Finding

```text
Compare Act occurrence                         survives
Compare                                        survives
positive Applicability result reference        survives
exact Compare subjects                         recoverable
copied Compare Act subject_reference           no distinction found
```

The positive Applicability result carries the exact addressed question into
the Compare occurrence through exact occurrence references. Repeating its two
subjects on the Compare Act adds no independently variable coordinate.
