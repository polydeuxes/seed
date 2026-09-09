# Occurrence-position Measurement coordinate closure census 001

## Boundary

This census closes the occurrence-position Measurement lifecycle after the
independent subtraction of:

```text
prospective result identity
prospective Act-occurrence identity
opaque exact-Act identity
separate binding occurrence
copied Act on the result
copied source Locality on the result
copied completeness boundary on the result
subject narration inside the Act word
```

## Durable shape

The Measurement Act occurrence `A` carries:

```text
Event.identity
Event.locality_identity = recording Locality
act = Measurement
subject_reference = exact ordered source occurrence references
source_locality_identity
completeness_boundary_identity
through_event_occurrence_identity when the recording Locality has a cut
```

The Measurement result occurrence `R` carries:

```text
Event.identity
Event.locality_identity = A.Locality
act_occurrence_event_identity = A
result_positions = exact ordered position findings
```

## Surviving distinctions

### Source Locality and recording Locality

An authored Measurement can measure exact occurrences in source Locality `S`
while its Act and result occur in recording Locality `D`. The two coordinates
do not collapse.

### Completeness boundary and recording cut

The completeness boundary bounds the source occurrences measured. The
through-occurrence coordinate identifies the recording Locality cut addressed
by the Act. They can differ; the latter can also be absent.

### Act and result occurrences

`A` can exist without `R`. `R` must follow and address one exact `A`, and one
`A` cannot receive two results.

### Findings and reconstructed coordinates

The ordered result positions remain durable findings. Source Locality,
completeness boundary, and Act are recovered through `R → A`; they are not
copied onto `R`.

### Binding and binding occurrence

The subject-to-Act binding survives as exact coordinates of `A`. A separate
binding event adds no independent occurrence.

## Active road

```text
exact occurrence-position finding
+ exact current recording coordinates
        ↓
Measurement Act occurrence A
        ↓
Measurement result occurrence R
```

The operator console records no occurrence-position binding event. An
unresulted `A` is not a current result coordinate. Current-coordinate reading
recovers the result's exact binding through `R → A`.

## Closure

```text
exact binding coordinates            retained
Measurement Act                      retained
actual Act occurrence                retained
ordered position findings            retained
actual result occurrence             retained
source/recording Locality difference retained
boundary/cut difference              retained

separate binding occurrence          withdrawn
prospective lifecycle identities     withdrawn
opaque exact-Act identity             withdrawn
copied result coordinates            withdrawn
narrated Act wording                  withdrawn
```

Further work should begin with a different Measurement family. This census
does not generalize the occurrence-position result to byte Measurement or its
downstream pair, Movement, Applicability, and Compare roads.
