# Luminary 099 Decompiled Structure and Use Investigation 001

## Question

What exact distinctions remain between recovered source structure, an exact
binary image, placement of generated words in that image, recording the
material, and performing an Act with it?

This investigation uses a bounded public-domain specimen. It adds no runtime
road, Book clause, Act, result kind, or admitted word.

## Public specimen

The specimen is Luminary 1A revision 099, the Apollo 11 Lunar Module Apollo
Guidance Computer program in the Virtual AGC repository. The observation pins
upstream revision:

```text
ebd8695d23bde6eb9f26933ddf244b8d18987f21
```

The upstream [main source](https://github.com/virtualagc/virtualagc/blob/ebd8695d23bde6eb9f26933ddf244b8d18987f21/Luminary099/MAIN.agc)
and [program Makefile](https://github.com/virtualagc/virtualagc/blob/ebd8695d23bde6eb9f26933ddf244b8d18987f21/Luminary099/Makefile)
identify the program material as public domain. The source describes its
transcription from images of the original hardcopy program listing. The
upstream [binary-source file](https://github.com/virtualagc/virtualagc/blob/ebd8695d23bde6eb9f26933ddf244b8d18987f21/Luminary099/Luminary099.binsource)
is a separately entered octal representation of the executable listing.

Virtual AGC's build produces two exact binary files by different roads:

```text
transcribed AGC source
→ yaYUL assembly
→ MAIN.agc.bin

separately entered octal binary source
→ oct2bin conversion
→ Luminary099.bin
```

The tools are not copied into Seed. The committed evidence contains only a
small public-domain source excerpt and exact coordinates observed from a
pinned external build.

## Whole-result control

Both produced files contain 73,728 bytes and have the same SHA-256 digest:

```text
1f5326e038de5b741b2f27b01ec949dbd688cf1906994e997402587c8628f40e
```

The build's exact byte comparison also reports the files as identical.

This is stronger than comparing one convenient excerpt. A difference at any
binary position makes the observer refuse the reading, including a difference
outside the selected window.

The two files nevertheless remain separate filesystem results reached through
separate construction roads:

```text
same complete bytes
!=
same result occurrence
```

The filesystem does not itself give either file a Seed occurrence identity.
The inequality above is therefore orientation for a later supplied-material
experiment, not a claim that this external build occurred inside Seed.

## Bounded exact correspondence

The focused specimen is six statements from
`Luminary099/CONTROLLED_CONSTANTS.agc`, exact source lines 40 through 45:

```text
FDPS       2DEC  4.3670 B-7
MDOTDPS    2DEC  0.1480 B-3
DTDECAY    2DEC  -38
FAPS       2DEC  1.5569 B-7
MDOTAPS    2DEC  0.05135 B-3
ATDECAY    2DEC  -10
```

Their generated listing rows address twelve words:

```text
bank 36, address 2000: 01056 37167
bank 36, address 2002: 00457 03250
bank 36, address 2004: 77777 77731
bank 36, address 2006: 00307 11040
bank 36, address 2010: 00151 05214
bank 36, address 2012: 77777 77765
```

In the Block II binary bank ordering, bank `36` occupies zero-based bank
position 30. Each bank contains `02000` octal words and each encoded word uses
two bytes. Address `2000` is therefore byte offset 61,440 in the complete
image. The exact 24-byte window through address `2013` is:

```text
045c7cee025e0d50fffeffb2018e244000d21518fffeffea
```

The observer independently requires:

```text
six exact source statements
→ six exact listing rows
→ twelve exact listing words

twelve exact listing words
→ exact 15-bit-word encoding
→ exact 24-byte window position

reference binary window = listing-derived window
assembled binary window = listing-derived window
complete reference binary = complete assembled binary
```

A changed source label, changed addressed binary position, changed binary byte,
missing listing row, changed revision, or whole-image difference refuses the
observation.

## Placement

`Placement` is useful Rosetta compression for this exact relation:

```text
listing bank and address
+ Block II bank ordering
+ two-byte word encoding
→ exact binary position
```

The experiment establishes why the twelve words are read at byte positions
61,440 through 61,463. Equal bytes at another position would not satisfy that
coordinate relation.

This does not admit Placement as a Book word or create a Placement occurrence.
The exact bank, address, bank position, byte offset, word count, and byte count
carry the observed distinction without a new wrapper.

## Decompiled

`Decompiled` remains a composite Rosetta orientation, not the name of an Act
observed here.

The public history includes recovery from hardcopy listing images into
source-like and octal forms. This focused experiment begins after that human
transcription and follows the forward assembly road back to exact binary
bytes. It therefore does not falsely claim that yaYUL decompiled the binary or
that the six source statements were mechanically recovered from the committed
binary.

The Super Smash Bros analogy from the preceding result-use investigation still
separates the relevant states:

```text
artifact decompiled
!=
game played
!=
material understood
```

For this public specimen the exact equivalent is:

```text
source/listing/binary correspondence observed
!=
binary executing
!=
result participating as a subject of a later Act
```

## Assembly

`Assembly` is ordinary language for the external yaYUL transformation. The
observation has exact source, listing, and output coordinates, but Seed records
no Assembly Act or Assembly result for them.

Naming an Assembly Act would merely label the known external tool invocation.
It would not yet recover the general physiology by which a representation and
its exact construction rules become the subjects and coordinates of an Act.

The test therefore preserves the evidence without importing Assembly into
Book grammar.

## Emit and emission

The build tools write files. That host write does not automatically establish
a Seed Emission occurrence.

Current Book Emission has exact coordinates including a source material result,
an exact destination boundary, an emission Act, accepted material, and the
count reported by the boundary. This external observation has filesystem paths
and exact bytes; it does not supply that Seed lifecycle.

Consequently:

```text
external tool produced a file
!=
Seed Emission occurred
```

This experiment gives no reason to replace Emission with Placement. Placement
describes where the observed words occur in the binary; Emission addresses a
source-result-to-destination-boundary physiology. Their ordinary proximity
does not establish identity.

## Record and recorded

The pinned files are durable public artifacts, and `record` is useful Rosetta
language for that fact. But filesystem persistence is not a Seed Ledger
occurrence.

In current Book grammar, `recorded` qualifies an exact occurrence that can be
addressed and validated in the Ledger. Supplying either binary to Seed could
produce a recorded material result. The external file's existence alone does
not.

Therefore:

```text
public artifact exists
!=
exact Seed occurrence recorded
```

No Record Act is inferred.

## Execute, play, use, and understand

No emulator is invoked by this experiment. No instruction is executed. No
external effect of an instruction is observed.

The complete binary equality and the exact source-to-position correspondence
remain unchanged whether an emulator exists, whether the image is loaded, or
whether any later Act addresses the result. Those dimensions can vary
independently:

```text
exact binary correspondence      yes
exact placement coordinates      yes
Seed material occurrence         no
execution occurrence             no
later Act using the result       no
understanding coordinate         none
```

As in `recorded_result_later_act_subject_investigation_001.md`, `use` is only
report-local shorthand for a result becoming an exact subject of a later Act.
Nothing in the external build establishes such a later Seed Act.

## What the experiment finds missing

The experiment does not find a missing word. It finds a boundary between two
classes of testimony:

```text
exact representation correspondence
    source lines
    listing addresses and words
    binary positions and bytes

exact operation with the representation
    an Act occurrence addressing exact prior results as subjects
    an exact result occurrence of that Act
```

The first class can be exhaustively checked for this bounded specimen. It does
not entail the second.

Seed can currently be supplied the bytes and can measure their exact structure.
That would still not mean Seed assembled, executed, played, or understood the
program. A future experiment must introduce independently warranted exact Act
coordinates, not promote successful structural correspondence into an Act.

## Reproduction

Build the pinned Virtual AGC checkout so that these paths exist:

```text
Luminary099/Luminary099.lst
Luminary099/Luminary099.bin
Luminary099/MAIN.agc.bin
```

Then run:

```text
python3 scripts/observe_luminary099_source_binary.py \
  /path/to/virtualagc \
  --expected tests/public_domain/luminary099_reading.json
```

The observer prints the exact reading and refuses if it differs from the
committed evidence. It requires the pinned Git revision and copies no external
build product into Seed.

## Disposition

The public specimen establishes a complete source/listing/binary
correspondence and one bounded exact position mapping.

It does not establish:

```text
Decompile Act
Assembly Act
Placement occurrence
Record Act
Seed Emission occurrence
execution occurrence
Use relation
understanding coordinate
```

No word enters Book admission. The next live question is not whether exact
structure can be recovered. It is what exact supplied Act coordinates can make
an already exact result participate as the subject of a later Act without
inferring that Act from the result itself.
