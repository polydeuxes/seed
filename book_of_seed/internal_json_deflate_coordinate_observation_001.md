# Internal JSON and DEFLATE coordinate observation 001

## Question

Does Seed already perform the lower behavior needed to expand compressed
material, and if so, why does an exact gzip material result remain opaque?

This is a Ledger-mechanics observation. It changes no runtime road, Book
clause, Witness Grammar, or admission. JSON, DEFLATE, gzip, LZ77, codec,
placement, and behavior are ordinary report-local terms.

## Correction to the preceding experiment

The opaque-material investigation treated decompression behavior as something
Seed might need to acquire from gzip interface material. A proposed follow-up
then began adding a handwritten DEFLATE reader to `seed_runtime`.

That was the wrong experiment. Seed already imports `json` and `zlib` in its
Ledger implementation. SQLite event material crosses this exact mechanical
road on ordinary writes and reads:

```text
Event.material dictionary
-> json.dumps
-> zlib.compress when the bytes become smaller
-> SQLite events.material

SQLite events.material
-> zlib.decompress when stored as bytes
-> JSON decode
-> Event.material dictionary
```

The uncommitted handwritten reader was removed. It would have proved only that
new Python written for the experiment could decode DEFLATE.

## Equal-byte coordinate control

The focused control constructs one large exact coordinate dictionary and asks
Seed's existing `_stored_material` behavior for its storage representation.
The result is compressed bytes.

One SQLite Event is then recorded with:

```text
Event.material       = the exact coordinate dictionary
Event.exact_material = the compressed bytes
```

The raw SQLite row carries the same compressed byte sequence in two places:

```text
events.material
event_exact_materials.exact_material
```

The equality is checked before the Ledger is reopened.

On ordinary Seed read, the two coordinates separate:

```text
events.material
-> existing zlib behavior
-> existing JSON behavior
-> exact coordinate dictionary

event_exact_materials.exact_material
-> exact compressed bytes
```

Thus content equality does not determine behavior. The addressed coordinate
does.

## What Seed has

The control proves that the running Seed already performs:

```text
JSON serialization
DEFLATE compression through zlib
DEFLATE expansion through zlib
JSON decoding
```

Those mechanics are not inferred from source text alone. A real SQLite write,
close, reopen, and read exercises them, and the same compressed bytes survive
unchanged in the neighboring exact-material coordinate.

This corrects two overstatements:

```text
Seed has not consumed JSON behavior       false
Seed has no LZ77/DEFLATE behavior         false
```

The exact narrower statements are:

```text
internal Event.material uses those behaviors             yes
external exact material is addressed to those behaviors  no
```

## Why gzip remains opaque

`Event.exact_material` is intentionally a byte-preserving coordinate. Its
reader must not inspect some byte sequences as JSON or compressed storage merely
because they happen to be decodable. Doing that would make content select its
own interpretation and would destroy the exact-material boundary.

The current internal expansion is also coupled to one narrower storage shape:

```text
zlib-wrapped compressed JSON text
```

The supplied specimen is:

```text
gzip wrapper
+ DEFLATE payload
+ gzip trailer

expanded result = arbitrary tar bytes, not JSON text
```

Having the DEFLATE mechanism does not by itself address that gzip occurrence
to the mechanism or define the expected output coordinate.

## Recovered vacancy

The missing lower crossing is no longer accurately described as “teach Seed
LZ77.” The mechanism is present. The vacancy is:

```text
exact reading B contains material result G
+ exact input and destination coordinates
-> mechanics occur
-> exact reading C contains the output
-> Seed compares B with C
```

At present the zlib behavior applies only because bytes occupy the private
`events.material` storage coordinate. An exact material result `G` does not
cross that input coordinate, and no later exact reading `C` contains its
expanded result.

Moving G into that private column would not solve the vacancy. It would corrupt
the occurrence representation and confuse exact external material with the
Ledger's own coordinate envelope.

This is the binary-level form of the placement question:

```text
same bytes
+ different addressed coordinate
-> different behavior
```

`placement` is not proposed as a Book word here. It is shorthand for the exact
input and destination coordinates required at `B` and `C`.

## Relation to B and the later result boundary

The existing current-coordinate experiment still matters. It proves that gzip
interface material can be current through an exact boundary `B`, followed by a
new compressed material occurrence and later comparison results.

But boundary-relative availability does not place either material into
`zlib.decompress`:

```text
zlib behavior occurs on the Ledger's private storage coordinate
G is current as an exact material result through B
G does not reach that behavior's input coordinate
no expanded result is current through later reading C
```

The current `B`-to-`C` physiology can compare exact earlier and later
coordinates. It does not presently include a filesystem or private-storage
change that places `G` at the decoder input and its output in `C`.

## Disposition

Do not add a DEFLATE reader. Do not infer gzip from low recurrence. Do not feed
external bytes into private SQLite representation fields.

Do not expose a Python callable, callback, provider, or external Witness and
then treat that surface as Seed behavior. That would preserve the missing road
behind a new wrapper.

The next work must first census the real filesystem and process roads. A
positive experiment must address an executable file, exact input, and exact
destination through an exact reading `B`, then address the output through an
exact later reading `C` and compare their coordinates.

The first experiment may be given an exact executable-file coordinate. That
would test use of supplied filesystem material, not discovery. It must not add
an Act occurrence merely to explain the `B`-to-`C` change. If the current
runtime cannot carry those boundary coordinates, the result is a missing lower
road; observer code must not impersonate it.

The rejection gates for that work are recorded in
`seed_behavior_experiment_protocol_001.md`.
