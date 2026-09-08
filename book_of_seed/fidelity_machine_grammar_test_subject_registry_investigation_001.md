# Fidelity machine-grammar test-subject registry investigation 001

## Question

What constitutional distinction did the old Fidelity `test_subjects[]`
registry preserve, and where does that work live after the active Book and
Witness Grammar replaced `clause_coordinates` with `book_coordinates`?

This investigation begins at the ordinary `!pytest` refusal:

```text
scripts/implementation_function_measurement.py
↓
grammar["clause_coordinates"]["01.Source.C"]
↓
KeyError: clause_coordinates
```

It does not restore `clause_coordinates`, add a compatibility schema, restore
`witness_for`, or amend the implementation-measurement harness.

## Direct finding

`book_coordinates` is the active machine rendering.  The old
`clause_coordinates` Fidelity registry has no current constitutional owner.

Active `01.Source.C` establishes this shape:

```text
Fidelity
├── exact Responsibility
├── exact Compare Act
├── this Seed exact occurrence          Compare subject
├── this witness grammar                Compare subject
└── this Book material acquisition witness
                                        exact test subject
```

Each deterministic test carries an exact declared distinction.  The test does
not become another constitutional subject merely because the implementation
harness needs to associate a pytest function with that distinction.

The old registry collapsed two unlike coordinates:

```text
exact Fidelity test subject

and

declared distinction addressed by a deterministic test occurrence
```

into:

```text
each developer-labelled test family = Fidelity test subject
```

The old `witness_for` relation then asserted an edge from every such subject to
`this_Fidelity`.  Active grammar has no `witness_for` relation.  No responsible
Act, relation occurrence, Authority, Scope, or result establishes it.

The smallest current contract for implementation measurement is therefore:

```text
deterministic pytest occurrence
├── exact pytest occurrence reference
├── exact current book-coordinate reference for its declared distinction
└── exact observed implementation coordinates
```

For the Book-material acquisition test only:

```text
test subject = this_book_material_acquisition_witness
material reference = this_Book
```

The implementation occurrence does not gain `witness_for`, `distinct_from`,
or another Fidelity subject merely from collection metadata.  Recording those
coordinates also does not itself perform the declared Fidelity Compare.

## 1. Active law and machine rendering

The active Book says:

```text
Fidelity is one declared Compare Act with this Seed exact occurrence and
this witness grammar as subjects.

Each deterministic test carries one exact declared distinction.

This Book material acquisition witness carries this Book as material.
It is one test subject and no other subject.
```

Current `witness_grammar.json` renders the same distinction under
`book_coordinates["01.Source.C"]`:

```json
{
  "subject": "Fidelity",
  "Responsibility": "compare_this_Seed_occurrence_with_this_Grammar",
  "exact_Act": "Compare",
  "test_subject": "this_book_material_acquisition_witness"
}
```

The active relation inventory contains:

```text
participation
carriage
yield
locality
support
```

It contains neither `witness_for` nor a generic relation that makes a
developer test-family label a Fidelity subject.

Therefore a direct dictionary-key edit would only expose the next refusal:

```text
book_coordinates["01.Source.C"]
├── no test_subject_relation
└── no test_subjects[]
```

Those missing fields are not omissions from the active schema.  Their removal
is part of the recovered grammar.

## 2. Provenance of the old registry

The history is exact.

### 2.1 A material-witness marker enters pytest

Commit `6c7fd06f` (`Carry admitted material witness test subjects`) added a
pytest subject marker and one machine-grammar entry:

```text
this_material_Witness
├── material_reference = this_Book
└── distinct_from = this_Witness
```

At that point the Book said each deterministic test had its declared
distinction *as its subject*.  The implementation hook copied the marker into
the measured pytest occurrence.

### 2.2 The Book-material witness gains `witness_for`

Commit `8472530c` (`Name the Book material acquisition witness`) renamed the
marker to `this_book_material_acquisition_witness` and added:

```text
witness_for = this_Fidelity
```

The implementation hook copied that value directly.  No relation occurrence
was introduced.

### 2.3 Developer test categories become machine-grammar subjects

Commit `c83f0063` (`Make every Fidelity witness subject explicit`) replaced
per-test pytest markers with module-level `FIDELITY_SUBJECT` and
`FIDELITY_SUBJECTS` declarations.  It expanded `test_subjects[]` into a
registry of every named test category and required collection to resolve every
deterministic pytest function through exactly one registry entry.

The registry therefore had a clear implementation purpose:

```text
collected pytest function
↓ developer module declaration
named test category
↓ machine registry lookup
measured occurrence coordinates
```

Its existence did not establish that every category was a constitutional
subject.  The registry was a developer-compiled routing table.

### 2.4 A few categories gain direct grammar references

Commit `95e514be` (`Expose missing test grammar coordinates`) added explicit
machine-grammar references to a small subset of registry entries.  Commit
`695ace1a` (`Narrow test grammar references and distinguish storage`) then
removed the intermediate `witness_for this_Grammar` wrapper and retained the
coordinate paths directly.

Immediately before the active grammar replacement, the registry contained 231
entries:

```text
204  subject label only
13   subject + grammar_coordinate_reference
8    subject + material_reference
4    subject + embedded first_subject/relation/second_subject
2    subject + two material references
```

Only 13 entries attempted to address machine grammar directly.  Eleven of
those paths began at `clause_coordinates`; another began at the removed
`words` registry.  Those 12 paths do not address the current machine
rendering.  The remaining path addresses the top-level `responsibility`
coordinate, which still exists, but its old test-category use must still be
checked against the current Responsibility coordinates.

The overwhelming majority of registry entries were names with no exact
grammar coordinate at all.  Even the old registry and its structural siren had
already drifted: the machine object contained 231 entries while the frozen
test expected 229.

### 2.5 Active recovery removes the registry

Commit `f956b6fd` (`Reorder active Book around exact relations`) made the
decisive change:

```text
clause_coordinates
↓
book_coordinates
```

It also replaced the large `01.Source.C` object and its `test_subjects[]`
registry with the four current coordinates.  The Book wording changed at the
same boundary:

```text
old:
each test has its declared distinction as its subject

current:
each deterministic test carries one exact declared distinction
```

The implementation hook was not migrated.  Its `clause_coordinates` lookup,
`test_subject_relation`, `test_subjects[]`, and manufactured `witness_for` /
`distinct_from` values remained byte-for-byte active.  Several structural
tests also continued to freeze the deleted schema.

That is the provenance of the ordinary `!pytest` refusal.

## 3. Subtraction of the old inner coordinates

### 3.1 `test_subject_relation`

Old work:

```text
test_subject --witness_for--> this_Fidelity
test_subject distinct_from this_Witness
```

Current owner:

```text
none identified
```

The current Fidelity subjects are stated directly.  The Book-material witness
is stated directly as the exact test subject.  No extra relation is required
to repeat those coordinates, and no active relation physiology establishes
`witness_for`.

What becomes inexpressible when this object is removed:

```text
nothing identified
```

### 3.2 `test_subjects[]`

Old work:

```text
registry of developer-labelled test categories
complete pytest collection routing
lookup table for copied occurrence fields
```

Current owner:

```text
implementation collection validation, not active Book grammar
```

The useful constraint survives without constitutional subjects: every
deterministic test occurrence must address an exact declared distinction, and
no pytest function may silently escape measurement.  That can be checked from
direct current coordinate references.

What becomes inexpressible without the constitutional registry:

```text
nothing identified
```

### 3.3 Per-entry `subject`

Old work:

```text
developer name for a family of tests
dictionary key joining module declarations to registry entries
```

Current owner:

```text
none as a Fidelity subject
```

Where the label described a real distinction, that distinction must be
addressed at its current Book coordinate.  A label such as
`current_Locality_Standing` does not itself establish Standing, Locality, or a
subject.

### 3.4 `grammar_coordinate_reference`

Old work:

```text
address the exact declared distinction exercised by a deterministic test
```

Current owner:

```text
the active book_coordinates entry addressed by that test occurrence
```

This is the only registry coordinate whose work survives directly.  Its old
paths do not survive: references to `clause_coordinates`, the former `words`
registry, and deleted nested structures are stale.  The distinction must be
re-addressed rather than path-renamed mechanically.

The reference belongs to the deterministic test occurrence.  It does not turn
the referenced distinction into the occurrence's constitutional subject.

### 3.5 `material_reference`, `first_material_reference`, and
`second_material_reference`

Old work:

```text
name exact material addressed by a deterministic test category
```

Current owner:

```text
exact source/material coordinates carried by the deterministic occurrence
```

The special Book-material test has an active owner:

```text
this_book_material_acquisition_witness carries this_Book as material
```

Other material references require their own current source coordinates.  They
do not warrant independent Fidelity subjects.

### 3.6 Embedded `first_subject`, `relation`, and `second_subject`

Old work:

```text
compile an asserted relation directly into a test-category registry entry
```

Current owner:

```text
none as registry metadata
```

The four old embedded relations used `bears`, `of`, or `input_to`.  None is in
the active relation inventory.  If a deterministic test addresses a current
relation, its declared-distinction reference must point to that exact current
relation coordinate.  Registry metadata may not instantiate it.

### 3.7 Manufactured `witness_for` and `distinct_from` output fields

Old work:

```text
copy the deleted test_subject_relation into every measured pytest occurrence
```

Current owner:

```text
none identified
```

The current Witness Material path already demonstrates the lawful neutral
shape: it records the exact pytest occurrence and observed coordinates without
adding `subject`, `witness_for`, or `distinct_from`.

Fidelity occurrences need their exact declared distinction reference in
addition to those observation coordinates.  They do not need the deleted
relation copied back in.

## 4. Clause-level residue around the registry

The deleted `01.Source.C` object carried more than the registry.  Its remaining
fields classify as follows.

| Old coordinate | Current disposition |
|---|---|
| `subject: this_Fidelity` | Current machine grammar names the subject `Fidelity`; `this_Fidelity` remains a reference to a bounded Fidelity finding, not a registry container. |
| `book_material_reference` | Witness Grammar already carries the Book material reference at its exact source position. It does not warrant the old registry. |
| `grammar: established` | Deleted scalar. Current grammar is the exact artifact and coordinates, not an `established` label. |
| `recorded_occurrence_kind` | Deleted implementation taxonomy. It does not classify Fidelity constitutionally. |
| `comparison` | Its surviving work is the current exact Responsibility and Compare Act. Its old `this_Witness` first subject conflicts with current law naming this Seed exact occurrence. |
| `preserves` | Current prose preserves exact source, provenance, Authority, Scope, Locality, limits, conflicts, loss, and Unknown at each deterministic test boundary. These are occurrence coordinates, not registry ownership. |
| `comparison_order` | No active owner identified. Current law names exact Compare subjects; it does not establish the old four-item sequence. |
| `representation_order` | No active owner identified in `01.Source.C`. It cannot be restored through the Fidelity harness. |
| `standing_not_established` | The deleted negative list is not a current machine coordinate. A test occurrence or passing result does not gain later Standing automatically. |

## 5. Smallest lawful current contract

The implementation-measurement hook needs no Book-wide test-subject registry.
Its bounded contract can be smaller:

```text
collection
↓
every deterministic pytest function is classified exactly once as either
    a deterministic test occurrence carrying an exact declared distinction
or
    a Witness Material-producing test occurrence

deterministic test occurrence
├── pytest occurrence reference
├── direct reference into current book_coordinates
├── observed Python invocation coordinates
├── observed SQL invocation/material coordinates
└── exact source/provenance/limits already measured at that boundary
```

The Book-material acquisition test additionally carries:

```text
test_subject = this_book_material_acquisition_witness
material_reference = this_Book
```

The direct coordinate reference must resolve against the current object.  It
cannot be inferred from an admitted label, old registry position, storage
routing value, test filename, event kind, or renamed path.

This contract preserves the useful sirens:

```text
no unclassified deterministic test
no test entered twice
no Fidelity / Witness Material crossing
no stale or missing declared-distinction reference
exact observation boundary per pytest occurrence
```

It removes the unsupported claims:

```text
every test family is a constitutional subject
test subject --witness_for--> this_Fidelity
test subject distinct_from this_Witness
developer label establishes a Book distinction
implementation measurement itself performs Fidelity Compare
```

## 6. Exact stopping boundary

The active repository does not yet provide a complete current mapping from
every deterministic pytest function to an exact `book_coordinates` path.

The old registry cannot supply that mapping:

```text
231 old entries
├── 218 without any grammar-coordinate reference
├── 12 with references into deleted structures
└── 1 with a syntactically surviving top-level path whose current use remains
    to be established
```

Therefore the lawful implementation repair is not a dictionary-key rename.
It requires re-addressing each deterministic test's declared distinction
against current machine grammar and deciding whether tests with no current
declared distinction are Witness Material rather than Fidelity.

Until that work is performed:

```text
ordinary !pytest
↓
implementation-measurement collection
↓
STOP
```

The 16 Book-material witnesses remain available through the ordinary pytest
road, but the harness cannot lawfully classify the deterministic test
occurrences needed to execute that road.

## Answer

`book_coordinates` wins.

The old `test_subjects[]` registry preserved a developer-compiled association
between pytest functions and named test categories.  That association was
useful implementation routing, but it did not establish 231 constitutional
Fidelity subjects.

The current grammar has one exact Book-material acquisition test subject.
Each deterministic test occurrence must instead carry a direct reference to
the exact current distinction it exercises.  `witness_for` has no active
owner and must not be restored.

The smallest lawful implementation-measurement contract is exact occurrence
measurement plus an exact current declared-distinction reference, with the
Book-material test carrying its separately established subject and material
coordinates.  Building that reference set is the next implementation boundary;
this investigation does not cross it.
