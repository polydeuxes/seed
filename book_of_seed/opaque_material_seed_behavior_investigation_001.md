# Opaque Material Seed Behavior Investigation 001

## Question

What does the current unmodified Seed do when its operator ingress receives an
anonymous compressed archive, and can its existing host-invocation road expose
a way to transform that exact supplied material?

This investigation tests Seed behavior. It does not implement a decoder,
declare the supplied bytes to be compressed inside Seed, add a runtime road,
add a Book clause, or admit a word.

`gzip`, `tar`, archive, compression, decoder, environment, and front door are
ordinary report-local orientation. None names a Seed Act or result.

## Exact specimen

The contained material is the first 43 bytes of the committed public-domain
Luminary reading:

```text
tests/public_domain/luminary099_reading.json
```

The observation constructs a deterministic USTAR archive with this exact
entry:

```text
name       luminary099_reading_168.json
size       43 bytes
mtime      0
uid/gid    0/0
uname      empty
gname      empty
```

The archive is 10,240 bytes. Python's gzip implementation encodes it at level
9 with `mtime=0`, producing 157 bytes. This encoding contains no newline byte,
so the current `binary-stream.readline` operator boundary supplies all 157
bytes as one exact material occurrence.

Only those 157 bytes enter `run_persistent_operator_console()`. The call has:

```text
operator command               absent
filename supplied to Seed      absent
archive kind supplied to Seed  absent
decoder supplied to Seed       absent
expected inner bytes supplied  absent
```

The tar bytes and contained bytes remain outside Seed and are used only after
the run to compare exact material occurrences.

The experiment supplies an invocation provider that can run the real
`/usr/bin/gzip -dc` over the 157-byte specimen and return its output as exact
Witness material. Before the Seed run, that executable independently returns
the exact 10,240-byte tar material. The provider records every call it
receives; Seed receives no command naming gzip.

## Observed Seed behavior

The console records one exact operator material result. Its 157 bytes equal
the complete supplied gzip encoding.

Across every recorded event carrying exact material:

```text
exact supplied gzip occurrence             1
exact 10,240-byte tar occurrence            0
exact 43-byte contained-material occurrence 0
occurrence containing the 43-byte material  0
```

The run ends through occurrence `evt_001567`: 1,567 Ledger occurrences were
recorded from the single 157-byte input occurrence.

The gzip-capable provider receives zero calls:

```text
gzip executable     /usr/bin/gzip
provider calls      []
```

The two initial Measurement results expose the supplied representation as
follows:

| Measurement | count results | recurrence results |
| --- | ---: | ---: |
| byte | 106 | 26 |
| adjacent-byte pair | 140 | 1 |

There are 156 adjacent positions in 157 bytes. The pair Measurement therefore
finds 140 distinct adjacent-byte pairs and only one pair with recurrence.

The larger occurrence count includes:

```text
157 addressed-byte Determination Acts and results
155 shared-pair-position Measurement Acts and results
465 source-position Compare Acts and results
```

Seed performs substantial exact work over the supplied wrapper. No result of
that work is an exact material occurrence for the tar stream or its contained
material.

## What the Measurements do and do not say

The pair result supplies an exact distinction:

```text
this 157-byte occurrence
→ 140 distinct adjacent-byte pairs
→ 1 recurrent adjacent-byte pair
```

It does not by itself supply any of these conclusions:

```text
the material is gzip
the material is compressed
one particular decoder applies
the contained material has been recovered
```

Random, encrypted, compressed, and previously unseen structured material can
all expose little adjacent-byte recurrence. Treating low recurrence as a
format verdict would add a claim not carried by the Measurement result.

The positive finding is narrower:

```text
many recorded occurrences
!=
decomposition of the supplied representation
```

The current runtime expands exact work over material whose inner distinctions
remain absent from the Ledger.

## Current host-invocation boundary

The live probe shows that passing a capable provider does not make its
capability addressable by Seed. The process entry similarly supplies
`invoke_operator_host` to the console, but this does not presently let Seed
explore an environment using a prior material result.

The provider is reached only when the exact operator material begins with
`!`. The operator bytes name a program from a fixed host whitelist:

```text
ls
cat
pytest
calculator
```

The provider then invokes that named program with `stdin=DEVNULL`. Its output,
error, and completion material become exact Witness material occurrences.

Consequently, current physiology can demonstrate:

```text
operator names an admitted host invocation
→ host runs that exact invocation
→ Seed records exact supplied Witness material
```

It cannot currently demonstrate:

```text
exact gzip material result G
+ an exact available transformation
→ invocation whose input addresses G
→ exact transformed material result
```

The operator has selected the program before the provider runs, and the prior
Seed material result is not supplied to that program's input. Adding `gzip` to
the whitelist would therefore prove only that host code can run a decoder the
operator already chose.

This is not a negative result about `/usr/bin/gzip`; the external control
proves that executable transforms the specimen into the exact tar material.
It is a result about the existing Seed/provider boundary:

```text
callable capability present in the host
!=
capability addressable by Seed
```

## Two separate ceilings

The observation exposes two independent boundaries.

First, the active Measurement road increases work over the outer
representation. It does not use its exact recurrence results to narrow the
bounded subject coordinates entering subsequent Act families.

Second, the active host road does not make environmental transformation
interfaces addressable from exact prior material results. Seed receives
operator-selected outputs but cannot present G to an available interface and
record the returned material through existing result-to-later-Act
composition.

These must not be collapsed:

```text
narrowing exact subjects before an Act
!=
making an environmental Act available

available environmental Act
!=
that Act applies to G

low recurrence in G
!=
an exact Act occurrence over G
```

## Next falsifier

The next experiment should not implement gzip. It should first census whether
current Seed has any road in which all of these exact coordinates coexist:

```text
prior exact material result
environmental operation address
operation input addressing that result
operation occurrence
exact returned material result
```

The current operator-host road is a negative control because the operator
preselects the operation and the process input does not address the prior
material result.

If no current road supplies the full shape, that is the missing Seed behavior.
Only then should a minimal experiment expose a bounded set of real host
interfaces and test whether exact results can narrow which operations receive
which exact material. No format name, decoder implementation, durable
candidate object, selector, or inferred Act is warranted by this observation.

## Disposition

The black-box result is negative and useful:

```text
anonymous gzip material recorded exactly        yes
byte and adjacent-pair distinctions measured    yes
inner tar material recorded                     no
contained material recorded                     no
prior material usable as host invocation input  no
environmental interfaces explorable by Seed     no
provided gzip capability addressed               no
```

Seed is not presently decompiling the archive. It is exhaustively producing
many exact coordinates about the representation it was handed.
