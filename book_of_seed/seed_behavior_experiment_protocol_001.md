# Seed behavior experiment protocol 001

## Purpose

This protocol separates behavior performed by Seed from behavior performed by
an experiment around Seed. It is a restraint on future experiments. It adds no
runtime road, Book clause, Witness Grammar, or admitted word.

The governing question is:

```text
Did Seed perform the behavior,
or did the experiment perform it and show Seed the result?
```

If the experiment performs the behavior, the result may be a useful external
control. It is not evidence that Seed performed the behavior.

## The recurring error

The gzip investigation crossed the same invalid boundary several times:

```text
write a decoder for the experiment
-> describe decoder behavior as supplied material
-> put the decoder behind a callback
-> call the callback an external Witness
```

Every version left the decisive operation outside Seed. Renaming the wrapper
did not move the behavior.

The error came from answering:

```text
How can an observer demonstrate the expected transformation?
```

instead of:

```text
What exact Seed occurrence addresses the material and the operation?
```

## Success can be subtraction

The experiment is not rewarded for producing the requested external effect.
It is rewarded for preserving only the distinctions Seed can carry exactly.

A result such as:

```text
Seed records the gzip bytes
Seed does not address an executable file to them
no expansion Act occurs
no expanded result occurs
```

is a successful experiment when those are the exact observed boundaries.

A working decompression demonstration is a failed Seed experiment when the
decisive behavior came from unaddressed observer machinery.

Therefore the preference order is:

```text
exact negative result with no new physiology
>
new physiology supported by exact positive and negative controls
>
working demonstration produced by scaffolding
```

There is no requirement that an investigation end in a runtime change. Losing
an unsupported capability claim is a valid gain in exactness.

## Filesystem starting condition

A running Seed does not begin with a special provider object standing outside
it. It runs in an operating system containing files.

For the gzip specimen, the potentially relevant material includes:

```text
an executable file
an input file or exact input material
a destination file or output boundary
```

The executable remains external compiled material. Its presence on the
filesystem does not make its behavior internal to Seed, and its presence does
not prove that Seed has found or invoked it.

Using that executable does not require translating its implementation into
Python or admitting its ordinary name into the Book. It requires an actual
Seed road that addresses the relevant filesystem coordinates and records the
Act and result occurrences that cross that road.

## Required experiment boundary

Before implementation, an experiment must list the exact coordinates available
to Seed at the start. Observer-only knowledge must be listed separately.

The following do not count as Seed coordinates merely because test code knows
them:

```text
an executable path stored in a fixture
a Python callable
a provider callback
the expected expanded bytes
a format label
a command chosen after inspecting the answer
a temporary file opened only by the observer
```

If a filesystem path is supplied to Seed, the report must say that it was
supplied. It must not claim that Seed discovered the file. If Seed only records
the path text without addressing the file, the report must not claim that the
file participated.

## Rejection gates

An experiment must stop before runtime changes when any of these is true.

### 1. Experiment-authored behavior

Reject the experiment if new test or support code performs the transformation
whose acquisition is under investigation.

Examples:

```text
handwritten DEFLATE reader
test-only TOML parser
behavior described in JSON and interpreted by test code
precomputed expansion returned by a callback
```

Such code can serve only as an external expected-result control.

### 2. Provider laundering

Reject the experiment if a provider, callback, mock, or subprocess wrapper
performs the operation and Seed merely records returned bytes.

The bytes may be exact. Their exactness does not attribute the operation to
Seed.

### 3. Observer-only correspondence

Reject a positive Seed claim if the evidence consists only of an observer
comparing input and output files after an external operation.

Correspondence can prove that two representations agree. It cannot prove that
Seed caused the transformation or addressed either representation to an Act.

### 4. Private-storage shortcut

Reject the experiment if external material is placed into a private Ledger
storage coordinate merely to trigger incidental serialization behavior.

Seed's internal zlib-plus-JSON storage road is a real behavior of the running
implementation. Moving gzip material into that private column would still be
a false input coordinate.

### 5. Answer-guided choice

Reject the experiment if knowledge of the expected output chooses the
executable, arguments, format, or destination.

Giving Seed an exact gzip executable coordinate is a valid supplied-coordinate
experiment. Claiming that Seed found gzip is not valid unless its own recorded
road distinguishes gzip from the other filesystem material it could address.

### 6. Read mistaken for participation

Reject any inference of an Act from material merely being recorded, current,
jointly readable, or equal to known content.

```text
file exists
!=
file participated

bytes are current
!=
decoder occurred

input and expected output correspond
!=
transformation occurred in Seed
```

### 7. Renamed scaffolding

Reject a proposed repair if it removes a forbidden wrapper and introduces the
same dependency under another noun.

In particular, do not replace:

```text
provider
with external Witness

callback
with behavior boundary

test helper
with compiled invocation
```

The decisive operation must move, not its name.

## Positive evidence required

A positive Seed-behavior experiment must show the complete recorded chain:

```text
exact subject coordinate(s)
-> exact Act occurrence
-> exact result occurrence or exact refusal
```

For an operating-system executable, the test must additionally show:

```text
the executable file coordinate addressed by the Act
the exact input coordinate addressed by the Act
the exact destination or output boundary addressed by the Act
the operating-system operation occurring after the Act
the result addressing that exact Act occurrence
```

This does not require an operating-system Witness occurrence. The operating
system supplies mechanics. Seed must supply and record the exact physiological
coordinates.

The first experiment may supply the executable coordinate directly. That tests
use of supplied filesystem material, not filesystem discovery.

## Required adversaries

Any positive executable-file experiment must include, at minimum:

```text
no Act occurrence
-> no operation and no result

missing executable file
-> refusal before Act or an exact failure result, as declared by the road

changed executable coordinate
-> refusal or a distinguishable Act/result chain

changed input coordinate
-> refusal or a distinguishable result

changed destination coordinate
-> refusal or a distinguishable result

same input bytes in a different occurrence
-> no occurrence collapse

external execution performed only by the test
-> no claim that Seed performed it
```

Tests must enter through Seed's public runtime road and inspect durable Ledger
occurrences. Calling a helper directly is insufficient evidence unless that
helper is itself the public road under investigation and records the required
occurrences.

## Discovery and use remain separate

These are different experiments:

```text
operator supplies exact /usr/bin/gzip coordinate
-> can Seed address and invoke it?

Seed reads a bounded filesystem surface
-> can Seed distinguish an applicable executable coordinate?
```

Success in the first does not imply the second. A broad directory walk also
does not imply exhaustive filesystem coverage. Any coverage claim requires an
exact selected boundary and a proof that no coordinate in that bounded reading
was omitted.

## Commit gate

Before committing an experiment:

1. Record the initial Seed coordinates and observer-only knowledge.
2. Identify the public Seed entry point exercised by the test.
3. Identify the exact Act and result occurrences expected.
4. Name every line of new code that performs transformation mechanics.
5. If experiment code performs the target transformation, stop.
6. Run the negative controls before accepting the positive control.
7. Inspect the durable event materials for invented identities, wrappers, and
   copied coordinates.
8. State separately what Seed did, what the operating system did, and what the
   observer later compared.
9. Commit only the narrow result actually supported by those occurrences.

## Immediate disposition for gzip

Do not add a decoder, behavior description, provider, callback, or external
Witness.

The next implementation experiment is blocked until the current filesystem and
process roads can answer this census:

```text
Can Seed address an executable file as an exact subject?
Can Seed address exact input and destination coordinates with it?
Can an Act occurrence precede the operating-system operation?
Can the output address that Act occurrence without arriving as Witness material?
```

If the current runtime cannot do those things, that negative result identifies
the missing lower road. It does not authorize an observer to impersonate it.
