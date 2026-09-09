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

The operating system does not need to become an external Witness. It performs
mechanics over files and processes. Seed must carry the exact coordinates on
the two sides of that change.

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

The exact output bytes and their acquisition occurrences do not retroactively
put the executable and input into the earlier Seed reading.

## Gzip consequence

Adding gzip to the provider's fixed mapping would prove only:

```text
the host script can choose /usr/bin/gzip
the operating system can execute it
Seed can record bytes returned by the callback
```

It would not prove:

```text
Seed addresses /usr/bin/gzip as a file
Seed addresses compressed material as gzip's input
Seed carries an exact B-to-C change over those filesystem coordinates
Seed found gzip in its filesystem
```

Calling the callback an external Witness, compiled behavior, or supplied
implementation does not change that result.

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

A host directory walk could expose path text or file bytes. Unless an exact
reading `B` addresses the selected file, input, and destination, that remains a
read.

Likewise, a broad `!ls` invocation does not claim that every filesystem
coordinate under an exact selected boundary was addressed. Discovery and use
remain separate experiments.

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

The current runtime cannot perform the proposed honest gzip experiment.

This is the supported result:

```text
filesystem executable use by Seed              absent
host-provider executable use                   present
Seed acquisition of provider output            present
exact B-to-C filesystem-coordinate comparison absent
```

Do not add gzip to the provider. Do not write a decoder. Do not introduce an
external Witness or callback replacement.

Any later implementation must begin at the missing lower road itself:

```text
exact B addresses filesystem-file coordinates
+ exact input and destination coordinates
-> operating-system mechanics
-> exact C addresses the output
-> Seed compares B with C
```

Do not add an Act word or occurrence unless an independently variable Act
distinction survives subtraction from that boundary physiology.
