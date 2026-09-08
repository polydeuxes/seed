# Operator invocation execution Responsibility investigation 001

## Question

Does the current operator/system invocation road already establish an exact
Responsibility and result physiology for external function execution that can
orient the missing Ingest-reference-to-parser-output crossing?

This investigation follows
`structure_bearing_compiled_result_responsibility_investigation_001.md`. It
changes no Book material, Witness Grammar, runtime, scripts, or tests.

```text
operator invocation Locality Responsibility
!= external function execution Responsibility

supplied output Ingest
!= external execution Yield by identity
```

## Material inspected

- `book_of_seed/chapters/04_source_coordinates.md`
- `book_of_seed/chapters/01_constitutional_standing.md`
- `book_of_seed/chapters/03_acts_and_occurrences.md`
- `book_of_seed/chapters/08_compare.md`
- `book_of_seed/chapters/06_locality_relations.md`
- `book_of_seed/chapters/11_representation_and_emission.md`
- `book_of_seed/witness_grammar.json`
- `material_witnesses/README.md`
- `seed_runtime/material_ingest.py`
- `seed_runtime/operator_console.py`
- `seed_runtime/operator_system_locality.py`
- `seed_runtime/supplied_invocation_material.py`
- `scripts/operator_host_provider.py`
- `tests/test_operator_host_invocation.py`
- `tests/test_operator_host_provider.py`
- `tests/test_operator_slash_commands.py`
- `tests/test_process_entry.py`
- history at `fdec71a1`, `49c66a1a`, and `91d57188`

Book material is primary orientation. Witness Grammar, runtime, scripts,
tests, material-witness documentation, and history are testimony.

`Execution` is investigation language for the external implementation
mechanics observed at this boundary. It does not name an active Book kind,
Responsibility kind, Act kind, occurrence kind, result kind, or Standing:

```text
external implementation mechanics
!= constitutional Execution kind
```

The exact constitutional question is whether current material establishes any
Responsibility for one external implementation-function occurrence and its
result.

## 1. The operator road owns one Locality Act exactly

Active `06.Locality.D` assigns this Seed one bounded Responsibility when
current operator Locality Standing carries one exact operator material
occurrence beginning an invocation:

```text
operator material occurrence
+ operator Locality Standing
↓
Responsibility:
preserve one operator invocation Locality relation
from one operator Locality
↓
Act:
establish one direct operator invocation Locality relation
↓
Act occurrence
↓ Yield
operator invocation Locality relation result
```

The runtime records that physiology explicitly:

```text
Responsibility assignment occurrence
Act Evidence occurrence
Evidence-of-Yield relation occurrence
Locality-relation result occurrence
```

The result carries one new destination Locality and one direct relation from
the operator Locality. Its Scope and Authority are bounded to that relation.
The Book also refuses Participation and supplied-material Applicability from
the Locality relation.

Therefore this assignment establishes exactly the Locality construction. It
does not establish external function execution.

## 2. The provider execution remains outside the recorded Seed physiology

After the Locality relation result is recorded, `operator_console.py` calls an
`OperatorInvocationProvider`:

```text
exact command material
+ callback receiving supplied material
↓
provider call
```

The live provider in `scripts/operator_host_provider.py` resolves one fixed
argument vector, invokes a host process, reads bounded stdout and stderr, and
supplies exact occurrences through the callback. It also supplies one exact
completion occurrence and, for pytest, two exact bounded artifacts.

The provider mechanics preserve real external distinctions:

```text
fixed argv
shell false
stdin boundary
stdout occurrence order
stderr occurrence order
time boundary
byte boundary
known loss
egress distinction
completion occurrence
```

None of those external mechanics is recorded as an exact Seed execution
assignment or execution Act occurrence. The ledger does not retain:

```text
provider function reference
process invocation identity
execution Responsibility assignment
execution input Applicability
execution input Participation
execution Act Evidence
execution Evidence-of-Yield relation
execution result identity
execution result boundary
execution Authority
execution Scope
execution Unknown
execution Standing
```

The console guards the provider boundary by checking that the provider did not
append ledger occurrences except through the supplied-material callback. That
guard proves the separation; it does not record the provider call as a Seed
Act.

```text
provider called by Seed runtime
!= provider execution is a Seed Act occurrence
```

## 3. Each supplied occurrence begins a fresh Ingest physiology

The callback receives one `SuppliedSystemMaterialOccurrence` carrying:

```text
exact bytes
source boundary
egress distinction
known loss
prior supplied occurrence positions
```

`ingest_supplied_invocation_occurrence` validates the exact invocation
Locality relation result, operator command occurrence, destination Locality,
and every referenced prior supplied occurrence. It then calls
`ingest_material`.

That call records a separate Seed-native physiology:

```text
Responsibility:
preserve exact material supplied at one source boundary
↓
Act:
Ingest exact material
↓
Ingest Act occurrence
↓ Yield
exact material result
```

The result preserves provenance beginning with:

```text
operator command Ingest occurrence
operator invocation Locality relation result
```

and then any exact prior supplied occurrences selected by the provider's
position references.

This establishes the supplied bytes as exact Ingest results. It does not
retroactively establish the external execution occurrence that produced the
bytes.

```text
external stdout occurrence
↓ supplied callback material
↓ new Ingest Act
exact Ingest result

external execution occurrence
-/-> Ingest Act occurrence by identity

external execution result
-/-> Ingest Yield by identity
```

The exact Yield checked by
`test_supplied_yield_cannot_be_replaced_by_another_occurrence` is the Yield of
the Ingest Act. It is not execution Yield.

### 3.1 The result-side Yield is the part that crossed into Seed

Commit `85d71e21` introduced the host provider in `scripts/` and the supplied
material acquisition road in `seed_runtime/`. The provider remained external.
The internalized occurrence was the later Ingest lifecycle for each supplied
result:

```text
external provider output
↓ supplied material boundary
Seed Ingest Act occurrence
↓ exact Evidence-of-Yield relation
exact material result
```

The later Yield adversary proves that one supplied result cannot borrow the
Ingest Yield of another supplied result or retain its Yield after command
provenance is changed. This is strong internal Seed physiology for acquisition
of the returned material.

It does not record the provider process, function invocation, or process return
as an internal Act occurrence. Thus the original witness crossed at the
result-side Ingest/Yield boundary only.

## 4. Provenance reaches the invocation boundary, not the missing execution edge

The supplied Ingest result carries exact provenance to the operator command
and invocation Locality relation result. Some witness roads additionally
supply opaque function-reference and source occurrences first, then include
those occurrence references in later result provenance.

That produces an exact lineage:

```text
operator command occurrence
invocation Locality relation result
opaque function-reference material occurrence
source material occurrence
result material occurrence
```

The lineage does not establish these relations by identity:

```text
opaque function reference --performs--> exact Act
source occurrence --Participation--> execution Act occurrence
execution Act occurrence --Yield--> supplied result
```

Commit `91d57188` deliberately decomposed function, source, and result
subjects into separate supplied occurrences. It preserved their references in
order. It did not add a constitutional relation connecting them.

This is another instance of the recurring boundary:

```text
ordered endpoints
!= evidenced edge
```

## 5. Operator Authority does not fill the execution physiology

Active `06.Locality.D` says the operator material occurrence carries operator
Authority for that exact invocation only. In the same clause, the assigned
Responsibility and exact Act are bounded to establishing the new Locality and
its direct Locality relation.

Source Locality Standing supports the assignment through its exact Evidence,
Authority, Scope, and preserved limits. Operator Authority is one coordinate
carried within that exact assignment physiology. Authority is not the support
relation by identity, and its presence does not by identity establish:

```text
another Responsibility
another exact Act
external implementation-function relation to that Act
execution Participation
execution Yield
parser-output relation Standing
```

The phrase `for that exact invocation` cannot replace those coordinates.
Borrowing it as generic execution Authority would merge the Locality Act with
the external provider call.

```text
operator Authority carried by command occurrence
!= execution Responsibility assignment
```

## 6. Witness Grammar subjects do not supply the assignment

Witness Grammar contains Fidelity subjects named:

```text
supplied_function_invocation
supplied_material_invocation
operator_function_invocation
function_invocation_occurrence
compiled_function_invocation_witness
compiled_material_invocation_witness
```

Those names orient test collection. A Fidelity subject name does not establish
the named Responsibility, Act, occurrence, or relation in Seed.

The slash-command test likewise proves that one exact registered Python
function receives one exact addressed command. The function's return shape is
explicitly unconstrained and no ledger command occurrence is recorded.

```text
test subject named invocation
!= invocation Responsibility assignment

registered implementation function called
!= exact constitutional Act occurred
```

## 7. History preserves the same boundary

Commit `fdec71a1` changed host results from one returned aggregate into streamed
exact system-attributed occurrences. Each callback occurrence entered Ingest
before the provider resumed. The change strengthened exact material ordering
and durability; it did not record provider execution as a Seed Act.

Commit `49c66a1a` then gave every invocation one fresh Locality and exact direct
Locality relation. Its Book amendment named only the Operator invocation
Locality Responsibility. It required supplied material provenance to the
operator occurrence and relation result while refusing Participation.

Commit `91d57188` demonstrated that opaque function, source, and result
occurrences can retain ordered provenance without identifying the function,
source, or result relations.

History therefore supports this exact decomposition:

```text
provider mechanics
↓ supplies
exact material occurrences
↓ each enters
Seed Ingest physiology

beside

operator command
↓ establishes
invocation Locality physiology
```

No historical amendment joins those roads into one execution physiology.

### 7.1 The calculator witness visibly intermingles external execution and internal Acts

`material_witnesses/test_calculator_relation_path.py` calls the live operator
console with the external host provider. One fixture therefore interleaves:

```text
operator material acquisition
operator command Ingest
command byte and position Measurements
invocation Locality assignment and Act
external calculator process execution
callback of calculator stdout
system-material Ingest and Yield
stdout byte and pair-position Measurements
Representations
Candidate production
```

This is real composition, but it is not one constitutional occurrence. The
external provider yields control to the callback for each supplied occurrence,
so ledger Acts happen between portions of provider execution. The console's
append-boundary guard preserves that alternation.

The calculator fixture later locates the exact `b"4\n"` system Ingest result
and its pair-position Measurement. The ledger carries no calculator execution
assignment, calculator execution Act occurrence, or calculator execution
Yield. Its exact internal results begin at the supplied-material Ingest.

```text
external execution interleaved with Seed Acts
!= external execution internalized
```

This explains why the calculator road can look more internally continuous than
its constitutional coordinates establish. The internal Ingest, Measurement,
Representation, and Candidate roads surround an external process seam.

## 8. Relation to the parser-output frontier

The operator road provides a useful exact precedent:

```text
external implementation executes
↓
exact output material crosses a callback boundary
↓
Seed records a new Ingest Act and result
```

That precedent establishes a lawful material crossing after external
execution. It does not internalize the execution itself.

Applying the same shape to Witness Grammar parsing would produce only:

```text
Witness Grammar Ingest result
↓ external parser mechanics
exact parser-output material
↓ new Ingest
exact parser-output Ingest result
```

The second Ingest would preserve exact output bytes and provenance. It would
not establish that parsing was a Seed Act, that the parser output carries Seed
structure, or that any parsed word position carries relation Standing.

Thus this family offers an exact acquisition path for externally supplied
output material, not the missing Seed-native parser execution Responsibility.

## 9. Exact elimination

### Proposed source: Operator invocation Locality Responsibility

```text
assignment subject = one direct Locality relation
exact Act = establish that Locality relation
result = that Locality relation
```

Disposition: exact but family-local; not execution Responsibility.

### Proposed source: operator Authority

```text
operator Authority supports one exact invocation boundary
↓
no execution assignment or Act occurrence recorded
```

Disposition: does not create the missing coordinates by identity.

### Proposed source: provider call

```text
runtime invokes callable
↓
external mechanics occur
↓
no execution Event physiology recorded
```

Disposition: external mechanics, not Seed execution Standing.

### Proposed source: supplied-material Ingest Yield

```text
Ingest Act occurrence
--Yield-->
exact material result
```

Disposition: exact Ingest Yield; not external execution Yield.

### Proposed source: ordered provenance references

```text
function material
source material
result material
↓
ordered occurrence references
```

Disposition: exact lineage; function-to-Act and occurrence-to-result relations
remain unestablished.

## 10. Smallest remaining boundary

The operator road does not recover the missing parser execution
Responsibility. It sharpens the remaining interrogation:

```text
exact source Ingest result reference
↓
exact execution Responsibility assignment          unestablished
↓
exact implementation-function relation to Act      unresolved
↓
source Applicability and Participation              unestablished
↓
exact execution Act occurrence                      unestablished
↓ Yield
exact parser-output result                          unestablished in Seed
```

An external provider can already carry the source reference and exact output
material together. If Seed bears a Responsibility for that external
implementation-function occurrence, its physiology requires one exact
occurrence whose Yield establishes that output as its exact result. Whether
current material establishes such a Responsibility remains unresolved.

## 11. Disposition

| Question | Finding |
|---|---|
| Does Seed bear the operator invocation Locality Responsibility? | yes |
| Does that exact Act execute the external function? | no |
| Does the provider preserve bounded external mechanics? | yes |
| Is the provider call recorded as a Seed execution Act occurrence? | no |
| Do supplied bytes enter an exact Seed Ingest physiology? | yes |
| Does supplied Ingest Yield establish external execution Yield? | no |
| Does supplied provenance preserve the command and Locality result? | yes |
| Does ordered provenance establish function-to-Act or occurrence-to-result relations? | no |
| Does operator Authority establish another execution Responsibility by identity? | no |
| Does this road establish parser-output structure or relation Standing? | no |

## Conclusion

The operator/system road contains more Seed-native physiology than the parser
witnesses, but the internal part begins before and after external execution:

```text
Seed Locality Act
↓
invocation Locality relation result

external provider execution
↓
supplied exact material

Seed Ingest Act
↓
exact material result
```

The middle occurrence remains external. Its surrounding Seed Acts cannot
identify it as their own occurrence or borrow its result relation.

This finding explains a broader repository pattern: many exact mechanics are
already present, but their exact Responsibility, Act, occurrence, Yield, and
Standing physiology remains external. Internalization is the recovery of
those relations, not relocation of the code.

The next forward slice must start from an exact existing assignment or record
the vacancy. The Operator invocation Locality Responsibility cannot be reused
as the parser execution Responsibility merely because both roads contain the
word `invocation`.
