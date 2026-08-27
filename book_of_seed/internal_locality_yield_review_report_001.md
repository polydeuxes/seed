# Internal Locality and Yield review report 001

## Review range

```text
bc130287..3aefecba
```

Commits:

```text
7276c92e  Subtract material Locality certificates
418d7ddf  Census separate Yield occurrences
82cbca0c  Subtract destination Locality Yield event
a8ebbf8c  Subtract recorded boundary Yield event
20707602  Subtract continuation Locality Yield event
86c39432  Reconcile Locality without separate Yield
fea01dea  Name Locality coordinates directly
3aefecba  Remove withdrawn Locality Yield boundaries
```

## Material result Locality

The source-specific Locality requirement readers returned three booleans after
the exact material result reader had already required:

```text
exact result occurrence
exact event Locality
intact source Act and Yield
```

The operator requirement reader was called by the operator exact reader. The
Witness requirement reader called the Witness exact reader again. Later roads
then called the combined reader after resolving the exact result.

All three requirement readers were removed. Consumers now resolve the exact
material result once and address its event Locality directly.

Removed runtime surface:

```text
read_material_result_locality_requirements
read_operator_material_source_locality_requirements
read_witness_material_source_locality_requirements
```

No replacement certificate, relation wrapper, or current-coordinate collection
was added.

## Separate Yield occurrence census

Every inspected Yield road recorded this order:

```text
subject-to-Act binding
Act occurrence
Yield relation event
result occurrence
```

The Yield event was therefore recorded before its declared result subject
existed. `_record_yield_relation()` received the future result identity and
complete result dictionary, copied them into a new event, and recorded a map
back to the result material recorded afterward.

The census is recorded separately in:

```text
book_of_seed/yield_relation_occurrence_census_001.md
```

## Locality subtraction results

Three independent Locality roads removed the separate Yield event:

```text
operator destination Locality
recorded-boundary Locality
Locality continuation
```

Their resulting order is:

```text
subject-to-Act binding
Act occurrence
recorded Locality result occurrence
```

Each result reader now:

```text
resolves the exact Act occurrence
derives the expected result from the Act and binding
requires Act-before-result append order in the exact Locality
refuses changed result coordinates
refuses changed endpoints
refuses corruption and substitution
refuses two results for one Act occurrence
```

Current-coordinate replay records each Locality result as both the exact result
for its binding and the Locality relation occurrence.

### Continuation refusal exposed by subtraction

The Locality-continuation result reader previously accepted the result's own
`result_identity`. The copied Yield event supplied the only contradicting copy.

After removing that event, changing only `result_identity` was accepted. The
reader now derives the expected identity from:

```text
Act occurrence
→ subject-to-Act binding reference
→ result boundary identity
```

Changing the recorded result identity is refused independently of the result
under test.

## Book and Witness Grammar

`06.Locality.B`, `06.Locality.C`, and `06.Locality.D` no longer require a
separate Yield occurrence. Their recorded result occurrence is the exact
Locality relation occurrence and directly records its Act occurrence and
Locality coordinates.

Yield remains admitted by `02.Acts.A` and remains active on other Act roads.
This review range does not withdraw Yield outside the three tested Locality
roads.

The three withdrawn Locality boundary values were removed from
`OCCURRENCE_BOUNDARIES_OF_YIELD_RELATION`.

## Vocabulary cleanup

The three recovered Locality roads now have zero occurrences of:

```text
carry
carries
carried
carrying
```

Those locations now name current coordinates, binding references, source
boundaries, or addressed subjects directly.

## Test results

Material-result Locality subtraction:

```text
104 focused source and recurrent-position tests passed
184 byte Measurement, position, current-coordinate, and console tests passed
53 Book, admission, and Witness Grammar tests passed; 8 skipped
```

Locality Yield subtraction and consumer checks:

```text
115 destination Locality, console, current-coordinate, Witness-source,
    and host-invocation tests passed
73 recorded-boundary Locality and current-coordinate tests passed
96 Locality result, current-coordinate, and console tests passed
92 Book, grammar, and three Locality-road tests passed
47 focused Locality vocabulary tests passed
73 final Locality and grammar tests passed
```

The groups overlap. These counts report the executed commands rather than one
combined suite total.

Additional checks:

```text
git diff --check                           passed
ContextVar                                 zero runtime/test hits
lru_cache and cache decorators             zero runtime/test hits
cache_key and _cache                       zero runtime/test hits
```

No complete-suite or remote-CI result is claimed.

## Unresolved review points

```text
1. Does a separate Yield occurrence add an independently addressable
   distinction on any remaining Act road?

2. If another Act road removes its copied Yield event, which exact Act or
   binding coordinate independently reconstructs the result?

3. Does `02.Acts.A` describe every Act result, or only roads where a distinct
   Yield occurrence survives its own subtraction test?

4. Does Assertion establish an occurrence or coordinate beyond exact content
   addressed by parent result occurrence plus result-local position?
```

No Assertion runtime or Book changes are included in this review range.
