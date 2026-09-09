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
exact prior material result G
+ exact internal behavior F
+ exact input position of F
+ exact output boundary
-> F occurs with G as its exact subject
-> exact output result
```

At present `F` is neither an exact current coordinate nor an Act addressed by
`G`. It is implementation machinery selected by the Ledger reader because the
bytes occupy the private `events.material` storage coordinate.

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
input and destination coordinates that a later Act would have to carry.

## Relation to B and the later result boundary

The existing current-coordinate experiment still matters. It proves that gzip
interface material can be current through an exact boundary `B`, followed by a
new compressed material occurrence and later comparison results.

But boundary-relative availability does not place either material into
`zlib.decompress`:

```text
F's behavior occurs inside the Ledger
F is not a current coordinate through B
G is a current exact material result through the later boundary
F and G never become subjects of one Act
```

Completeness and exhaustive comparison cannot bridge an absent subject-to-Act
coordinate. They can determine whether every member of an exact bounded set
was addressed only after that set and Act are exact.

## Disposition

Do not add a DEFLATE reader. Do not infer gzip from low recurrence. Do not feed
external bytes into private SQLite representation fields.

The next exact experiment should expose one already-running implementation
behavior as bounded testimony about this Seed, without yet treating a Python
callable as an Act. Then pressure whether an exact prior material result can
address that behavior's input and output coordinates.

The first positive specimen should remain smaller than the tar archive:

```text
exact zlib-wrapped JSON bytes
-> the exact JSON bytes or structure Seed's internal behavior already returns
```

Only after that coordinate crossing is real should the wrapper vary from zlib
to gzip and the expanded result vary from JSON text to arbitrary bytes.
