# Filesystem executable boundary coordinate census 001

## Question

Can the current Seed address a filesystem executable, exact input, and exact
destination through a reading `B`, then address the resulting material through
a later reading `C`?

This is a read-only census under
`seed_behavior_experiment_protocol_001.md`. It adds no runtime road, Book
clause, Witness Grammar, or admitted word. Filesystem, executable, process,
path, command, input, and output are ordinary report-local terms.

## Positive shape under pressure

The required shape is:

```text
exact reading B addresses:
    executable-file coordinate E
    input coordinate I
    destination or output boundary D
        ↓
operating-system mechanics
        ↓
exact reading C addresses output coordinate O
        ↓
exact comparison of B with C
```

The operating system does not require an additional Witness road. Existing
operator invocation output is material supplied by this Witness. Seed must
carry the exact coordinates on the two sides of the change through that
existing source physiology.

No new Act occurrence is presumed between `B` and `C`. If an existing Act
physiology independently addresses the operation, it must survive. The diagram
does not gain an occurrence merely because an observer wants a name for what
happened.

The first experiment may supply E directly. Such an experiment tests use of a
supplied file coordinate; it does not test filesystem discovery.

## Active process entry

`seed_runtime.process_entry.main()` constructs a Ledger and calls
`run_persistent_operator_console()` with:

```text
operator input stream
operator Locality
operator invocation provider = scripts.operator_host_provider.invoke_operator_host
```

The provider is a Python function supplied to the console. It is not a
filesystem coordinate or Ledger occurrence.

## What Seed records before host mechanics

For material beginning with `!`, the console records:

```text
exact operator material result Q
Measurement occurrences over current material
Locality Act occurrence from Q to destination Locality D
Locality relation result
```

These are real Seed occurrences. The Locality Act addresses Q and the exact
source cut. That reading does not address an executable file, argument vector,
input file, process, or output-file boundary.

The console then calls the provider with:

```python
operator_invocation_provider(command_material, record_witness_material)
```

That function call is host control flow. No Seed reading contains the
executable, input, and destination coordinates before it.

## What the host script does privately

`scripts.operator_host_provider._invocation_argv()` interprets the command
bytes and maps a small fixed set of names to paths such as:

```text
/usr/bin/ls
/usr/bin/cat
the current Python executable
/usr/bin/gnome-calculator
```

Those paths and the constructed argument vector remain Python variables in the
host script. The Ledger does not receive a filesystem-file coordinate for
them.

`_bounded_invocation()` then calls `subprocess.Popen()`, reads stdout and
stderr, enforces host time and byte limits, and passes the captured bytes to
the console callback.

The decisive operation therefore has this current shape:

```text
Q recorded by Seed
        ↓
unrecorded provider dispatch
        ↓
unrecorded executable-path choice
        ↓
unrecorded process occurrence
        ↓
captured bytes supplied through callback
        ↓
Witness material result recorded by Seed
```

The exact output bytes are already attributed to this Witness, the exact
operator command occurrence, and its invocation Locality. Those source
coordinates do not retroactively turn the provider's private executable-path
choice into a Ledger coordinate.

## Gzip consequence

Adding gzip to the provider's fixed mapping would establish:

```text
the host script can choose /usr/bin/gzip
the operating system can execute it
Seed can record exact material supplied by this Witness
the result addresses the operator command and invocation Locality
```

It would not prove:

```text
Seed addresses /usr/bin/gzip as a file
Seed separately addresses compressed material as gzip's exact input
Seed carries an exact B-to-C change over those filesystem coordinates
Seed found gzip in its filesystem
```

The existing Witness source attribution must not be replaced by a new
filesystem Source family. It also must not be stretched into an unrecorded
executable-selection coordinate.

## Existing internal JSON and DEFLATE behavior

The internal-coordinate observation remains exact:

```text
same compressed bytes in events.material
-> Seed's private zlib-plus-JSON storage mechanics apply

same compressed bytes in Event.exact_material
-> bytes remain opaque
```

That proves the behavior is present in the running implementation and that the
addressed storage coordinate matters. It does not supply E, I, D, or C for an
arbitrary material result.

Therefore these are separate facts:

```text
Seed implementation contains zlib behavior                 yes
filesystem contains executable files                       yes
Seed can address an executable file through exact B        no current road
Seed can address arbitrary material to that executable     no current road
```

## Search and broad listing do not repair the gap

An exact `!ls` invocation already yields an exact Witness result whose source
references address the command occurrence and invocation Locality. Its output
bytes can be current through `B`.

That result does not automatically decompose every output line into a separate
filesystem-entry occurrence. A broad `!ls` invocation also does not claim
that every filesystem coordinate under an exact selected boundary was
addressed. Source attribution, decomposition, exhaustive coverage, and later
use remain separate questions.

## Emission is a neighboring boundary, not the missing operation

Active Book law for Emission already addresses:

```text
exact source material result
+ exact destination boundary
+ Locality
+ Emission
-> accepted boundary write
+ destination-reported count
```

That is relevant to placing exact bytes at a destination boundary. It does not
say that an executable file interprets those bytes or that a later filesystem
coordinate is the expansion of an earlier compressed coordinate.

There is also no active Emission runtime road in `seed_runtime`. The current
executable provider does not record an Emission Act or an accepted-write result
before starting its subprocess.

Therefore this census must not stretch the admitted word:

```text
Emission
!=
execute a filesystem file
!=
decompress material
!=
the complete B-to-C filesystem change
```

If a later road writes exact input to a process boundary, Emission may describe
that write independently. Its existence does not supply the remaining
filesystem coordinates or mechanics.

## Disposition

This is the supported result at this census boundary:

```text
exact Witness source attribution of output                 present
exact command and invocation Locality provenance            present
host-provider executable-path choice                        present
Ledger coordinate for that executable-path choice           absent
decomposition of result bytes into filesystem-entry subjects absent
exact B-to-C comparison of Witness results                   available to test
```

Do not write a decoder. Do not introduce a third Source family, another
Witness, or a callback replacement.

The next experiment must begin with the existing Witness results:

```text
exact Witness result(s) current through B
-> operating-system mechanics
-> exact Witness result(s) current through C
-> Seed compares those exact results
```

Pressure which filesystem subjects, if any, the result bytes address. Do not
add an Act word or occurrence unless an independently variable Act
distinction survives subtraction from that boundary physiology.
