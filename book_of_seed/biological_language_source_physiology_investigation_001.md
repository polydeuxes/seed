# Biological language and source physiology investigation 001

## Boundary

Findings only. No active Book, machine grammar, runtime, storage, or test
change.

This investigation places verified DNA/RNA physiology beside the current Seed
source road. Biology is outside testimony. Its nouns and mechanisms do not
become Seed grammar through resemblance.

The question is narrower:

```text
what exact distinctions does a working material language preserve
between material, boundary occurrences, actionable continuation,
cross-material correspondence, and newly produced continuity?
```

## 1. Biological material does not perform its own continuation

DNA and RNA carry exact molecular sequences. A sequence alone does not perform
transcription or translation.

Eukaryotic translation begins through an initiation physiology that recruits
mRNA, scans it, recognizes a start codon in context, places initiator tRNA, and
forms a ribosome ready for elongation. After initiation, elongation advances
the mRNA by one codon and presents the next codon for the next cycle.

Thus biology distinguishes:

```text
material is present
!=
one exact continuation is active

initiation establishes one active reading position
-> each completed cycle presents the next position
```

The source material does not choose an Act by itself. Current cellular
conditions and already-present molecular machinery participate in making an
exact next reaction possible.

This resembles, but does not establish, the Seed topology:

```text
current Standing carries exact material
+ exact relations already carried
-> exact Responsibility
-> Act occurrence
-> Yield
-> richer current Standing
```

Biology therefore supports the importance of the unresolved crossing. It does
not supply that crossing to Seed.

## 2. An active path discriminates its continuation

The ribosome does not repartition the remaining mRNA in every possible way
after each amino acid is added. Its binding sites keep adjacent tRNAs aligned
with adjacent codons. Translocation moves mRNA by three nucleotides and exposes
the next codon.

The exact biological mechanism is not Seed grammar. Its topology nevertheless
matches the already-live source-position finding:

```text
established path
-> only the exact next position can answer
-> ordinary exact test still decides whether it answers
```

Commit `e9879301` recovered this behavior in Seed. One recurrence result
addresses only `final_position + 1`; it does not test every later coordinate.
Biology does not warrant a new Seed path rule. It confirms that local
continuation through an already-established path is sufficient for a working
material language; a prior complete parse is not required.

## 3. Biological correspondence is enacted through exact relations

An mRNA codon does not bind directly to an amino acid. tRNA relates one codon
surface to one tRNA surface, while aminoacyl-tRNA synthetase relates that tRNA
to an amino acid.

The two relations act in sequence:

```text
codon
<-> tRNA anticodon

tRNA
<-> attached amino acid
```

Changing an amino acid after it has been attached to its tRNA causes that
changed amino acid to be inserted where the tRNA answers the codon. The
ribosome follows the enacted molecular relations; it does not recover an
intrinsic codon meaning from the codon's appearance.

This gives a precise external control for the cross-surface observation in
`bd3a6470`:

```text
exact recurring correspondence
!=
intrinsic meaning

source-supported relation chain
!=
domain truth
```

The sparse digit/word bridges and larger arrangement constrained one exact
cross-surface renaming. That finding need not say that one surface intrinsically
means the other. It can remain an exact correspondence enacted by the carried
relations. Biology supplies no reason to add a generic adaptor object to Seed.

## 4. Mechanical reads do not own material continuity

Current Seed already contains a direct runtime finding that matches this
distinction.

Commit `7dec913b` changed ordinary host output from:

```text
one operating-system read
-> one Witness material result
```

to:

```text
one bounded invocation-output occurrence
├── exact read occurrence 0
├── exact read occurrence 1
├── ...
└── exact read occurrence n

-> one exact material result
```

Each read occurrence retains:

```text
source boundary
invocation position
start position
end position
```

The exact bytes of all reads must reconstruct the result bytes in order. The
read coordinates must cover the result without gaps or overlaps.

The focused live test supplies `b"abcdef"` once as one read and once as three
reads. It finds:

```text
exact material                    equal
read occurrence count            1 != 3
adjacent byte-position findings  equal
```

The ordinary `!cat` observation supplies 218,058 bytes through four mechanical
reads. One exact material result carries all four read histories, while
position Measurement produces all 218,057 adjacent positions, including the
three positions crossing mechanical read joins.

Therefore current runtime already establishes:

```text
read partition
!=
material-position partition
```

This is the narrow correction required by the one/four/many acquisition result
in `e9879301`. The number of reads need not alter later grammar when the exact
source boundary supplies one material result.

## 5. The existing road is not constitutional recovery

The read/result distinction entered in `7dec913b`, `Preserve stdout across
provider reads`. Book, machine grammar, implementation, and prior findings did
not first recover a general relation by which multiple reads must become one
material result.

The implementation currently receives from its caller:

```text
the complete exact bytes
one output boundary
the read occurrences
their invocation positions
```

It then validates that the reads reconstruct the bytes. This is exact source
testimony and useful runtime physiology. It is not a discovery by Seed that
arbitrary supplied occurrences are continuous.

Active `01.Source.A` requires one responsible source-preservation Act
occurrence to preserve supplied material and its source coordinates. Active
machine grammar does not carry the nested read occurrence coordinates.
The Witness road also still lacks the standalone Responsibility assignment
that precedes the operator source Act.

The durable finding is conditional:

```text
if one exact source-boundary occurrence supplies one exact material result
and carries multiple read occurrences that reconstruct that material,

then later material-position work may use the result's exact positions
without treating the mechanical reads as grammar boundaries.
```

This does not answer what makes that source-preservation Responsibility
present, and it does not authorize Seed to join separate material results.

## 6. New continuity requires a new result

RNA splicing supplies the strongest external distinction for truly separate
material.

Pre-mRNA splicing identifies splice sites, cleaves the pre-mRNA, removes an
intron, and ligates the two exons. The mature RNA is a new molecular result in
which the joined exons are now continuous. Their earlier positions and the
splicing reaction remain part of its history.

The relevant topology is:

```text
earlier material coordinates
+ exact recognition relations
-> responsible transformation
-> new material result
-> new exact continuity
```

It is not:

```text
two earlier pieces are nearby or useful together
-> pretend they were continuous
```

Applied cautiously to Seed:

```text
multiple mechanical reads carried by one supplied material result
-> one result's positions may already be continuous

multiple exact material results
-> no continuity between them is established

if later work genuinely joins or reorders those results
-> that work must Yield new exact material
-> positions belong to the new result
-> earlier result references remain provenance
```

This avoids inventing `cross-acquisition continuity`, global concatenation, or
a relation that changes old source occurrences after the fact.

## 7. Relation to Acquisition cleanup

The biological comparison strengthens the decomposition in `ace2ab4e` and
`8d2b4de5`:

```text
boundary-specific contact/read mechanics
-> one responsible source-preservation occurrence
-> one exact material result carrying exact source coordinates
-> common internal Measurement / Compare / path physiology
```

`Acquisition` adds no required layer to that flow. Mechanical reads, operator
calls, file reads, socket reads, and Witness supply may differ at their exact
boundaries. Once one exact material result exists, they do not warrant separate
internal grammar roads.

The exact source route and every read occurrence remain recoverable through
their carried coordinates. Removing the Acquisition compression must not erase
them.

## 8. What biology does not solve

A modern cell already contains transcription machinery, ribosomes, tRNAs,
synthetases, factors, membranes, energy gradients, and reaction conditions.
Evolution produced that machinery together with the material language.

Biology therefore does not demonstrate:

```text
raw material alone
-> discovers the machinery required to act on itself
```

Nor does it warrant any Seed identification such as:

```text
Responsibility = promoter
Act = transcription
Seed correspondence = genetic code
```

The comparison supports only these decompressed distinctions:

```text
material presence
!= active continuation

mechanical read boundary
!= material-position boundary

material recurrence
!= intrinsic meaning

exact relation chain
!= domain truth

old nonadjacent material
!= newly produced continuity

local discrimination
!= enumeration of all possible continuations
```

## 9. Smallest live vacancy

The closest existing Seed physiology is not a new syntax recognizer. It is the
common source-preservation road already identified in `8d2b4de5`, extended only
by exact boundary testimony where one supplied result required more than one
mechanical read.

The unresolved question is:

```text
what exact current Standing coordinates warrant
one source-preservation Responsibility whose Act
Yields one exact material result carrying these exact read occurrences?
```

Until that antecedent is recovered:

```text
Witness caller assembly remains source testimony
separate material results remain separate
continuity between separate results remains Unknown
no new internal grammar family is warranted
```

The next investigation should begin immediately before the already-live
one-read/three-read invariant. It should ask why one exact invocation-output
boundary supplies one material result, without assuming that the word
`Acquisition`, the provider callback, or developer control flow owns the
answer.

## External source testimony

- [Transcription in Prokaryotes](https://www.ncbi.nlm.nih.gov/books/NBK9850/)
  describes promoter recognition by RNA polymerase with its sigma subunit,
  formation of the open-promoter complex, initiation, elongation, and
  termination.
- [Translation Phases in Eukaryotes](https://www.ncbi.nlm.nih.gov/books/NBK586875/)
  describes initiation, start-codon recognition, elongation, and one-codon
  translocation.
- [From RNA to Protein](https://www.ncbi.nlm.nih.gov/books/NBK26829/)
  describes tRNA and aminoacyl-tRNA synthetase as sequential adaptors, the
  changed-amino-acid experiment, reading-frame maintenance, and exact
  three-nucleotide translocation.
- [RNA Processing and Turnover](https://www.ncbi.nlm.nih.gov/books/NBK9864/)
  describes splice-site recognition, cleavage, intron removal, and exon
  ligation into mature RNA.
