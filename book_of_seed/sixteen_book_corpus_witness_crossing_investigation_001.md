# Sixteen-book corpus Witness crossing investigation 001

## Question

Does any existing Witness road supply the exact sixteen-book corpus windows
outward from pytest?

This investigation changes no Book, witness grammar, runtime, provider,
pytest declaration, test-support function, or test.

It distinguishes:

```text
pytest processes exact material
!=
pytest supplies that exact material across its Witness boundary
```

## Direct finding

No current outward Witness crossing for the sixteen corpus windows was found.

The exact bytes are read inside pytest and retained in objects private to the
pytest process. The current outward provider carries only:

```text
pytest process stdout occurrences
pytest process stderr occurrences
function catalog artifact
function measurement artifact
invocation completion
```

The tests do not write the corpus bytes to process stdout or stderr. Neither
artifact contains values returned by test-support functions. No provider
callback receives the private ledger acquisitions or compiled `cat` results.

The historical road has the same boundary. Earlier versions gave the
sixteen-book tests Fidelity labels, but their outward occurrences carried
function and SQL coordinates rather than the exact corpus bytes.

Therefore:

```text
sixteen exact corpus windows
↓
private pytest material
X
no current outward Witness occurrence
```

The downstream missing material-to-this-Seed Locality relation remains real
for catalog and measurement artifacts. It is not yet the corpus blocker.

## 1. Exact corpus source

`tests/book_material_test_witness.py` addresses sixteen fixed files and a
fixed 300-line window in each file:

```text
grammar
dictionary
thesaurus
algebra
logic
geometry
shell material
cookbook material
French material
Latin material
English prose
```

The helper reads each addressed file, splits its bytes at line boundaries,
and returns the addressed 300-line byte window. The complete population is:

```text
16 byte values
300 lines per value
218,058 bytes total
```

The helper returns those bytes to its Python caller. It has no provider,
stdout, stderr, artifact, or supplied-material callback.

## 2. How pytest receives the bytes

`tests/test_supplied_book_material.py` receives the windows through the
module-scoped `supplied_material_in_order()` result:

```text
corpus files
↓
supplied_book_material(ROOT)
↓
supplied_material_in_order() result
↓
two pytest functions
```

The first function inspects the byte population and line counts.

The second function:

```text
creates a private EventLedger
↓
records each window as Witness material in that private ledger
↓
creates exact references
↓
invokes external cat with each reference
↓
captures each cat result in MaterialInvocationOccurrence.stdout_bytes
↓
asserts the captured bytes equal the input bytes
```

`stdout_bytes` here is a field on a Python object. The external `cat` process
is invoked with its stdout captured by `scripts/compiled_material_invocation.py`.
Those bytes do not become stdout of the pytest process.

The private EventLedger is likewise unrelated to the operator console ledger.
It is discarded with the pytest process.

## 3. Current pytest disposition

`tests/test_supplied_book_material.py` explicitly admits both functions in
`PYTEST_ADMISSION`.

It declares neither Fidelity uptake nor Witness Material uptake. The active
pytest boundary therefore performs:

```text
admitted function
+ no Fidelity uptake
+ no Witness Material uptake
↓
ordinary pytest execution
↓
no per-function Seed occurrence
```

The exact provider run confirms:

```text
2 passed in 1.11s
Fidelity occurrences:        0
Witness Material occurrences: 0
known loss:                   none
```

The global measurement artifact carries Python function coordinates produced
during the invocation. It does not carry function arguments, values returned
by test-support functions, private EventLedger rows, or captured
`stdout_bytes` fields.

## 4. Other current corpus consumers

### `tests/test_material_witness.py`

This file reads the same sixteen windows and records them in another private
EventLedger. Its Measurement-dependent support function currently stops before
Measurement because the corpus material lacks the required
material-to-this-Seed Locality occurrence.

The file declares selected Fidelity distinctions but no Witness Material
uptake for the corpus windows. Its private acquisition results are not an
outward pytest payload.

### `tests/test_book_material_availability.py`

This test addresses active Book files rather than the sixteen external corpus
windows. It records those files in a private EventLedger and proves that no
Measurement pressure follows. It is ordinary pytest execution and returns no
material through the provider.

### `tests/test_book_material_acquisition.py`

This file also addresses active Book files rather than the sixteen corpus
windows. Its grammar-checking Fidelity occurrence carries:

```text
test_subject = this_book_material_acquisition_witness
material_reference = this_Book
```

That exact material reference is not the referenced bytes. The remaining
private support function creates acquisitions and compiled invocations inside
pytest; they do not cross the provider.

### `material_witnesses/test_comparison_of_material_references.py`

This file reads the sixteen windows into a private EventLedger and performs
external comparisons over exact references. `material_witnesses/` is outside
the configured default pytest path. The file also has no current pytest
admission or Witness Material uptake declaration.

It is an external experiment on the corpus, not an outward corpus supplier to
the operator invocation Locality.

## 5. Provider and artifact boundary

The active host provider supplies exact process output and error as they are
read from pytest's pipes. After pytest returns, it separately supplies the
catalog and measurement files written by the measurement plugin.

The plugin's per-function outward coordinate contains:

```text
pytest reference
occurrence position
Python function positions and counts
SQL occurrence positions and counts
Fidelity coordinates where explicitly declared
```

Witness Material uptake changes which per-function occurrence population
receives those coordinates. It does not capture arbitrary values passed into
test functions.

Consequently, adding a sixteen-book function to `WITNESS_MATERIAL_TESTS`
would not make its 218,058 input bytes appear in the artifact. It would
reclassify a function-profile occurrence while leaving the corpus private.

The provider has no API for reading Python values passed into pytest test
functions or pytest's private ledger.

## 6. Historical trace

Commit `d0dc1605` introduced the ordered sixteen-window test. Its exact road
was already private:

```text
pytest support function reads corpus
↓
private ledger acquisitions
↓
compiled cat invocations capture stdout
↓
assertions inside pytest
```

It printed and supplied no corpus bytes.

Commit `386c0182` later gave these tests a developer Fidelity subject. Commit
`d4a25c4b` established a separate Witness Material occurrence population in
the pytest measurement plugin. At that boundary, a Fidelity or Witness
Material occurrence contained measured Python and SQL coordinates. It had no
exact-byte payload field.

At `d4a25c4b`, `tests/test_supplied_book_material.py` remained a Fidelity
subject named `supplied_material_invocation_witness`; it was not a Witness
Material-producing test. Even if it had been placed in the other population,
the artifact shape still did not contain corpus bytes.

The August 20 pytest admission cleanup removed the developer Fidelity label
and explicitly retained these two functions as ordinary execution. That
cleanup exposed the existing boundary; it did not remove an outward corpus
payload.

No inspected history contained:

```text
print corpus bytes from pytest
write corpus bytes into measurement artifact
supply private acquisition results through provider callback
return corpus bytes through pytest hook
```

The sixteen-window road has consistently been a private pytest experiment.

## 7. Subtraction

The following exact distinctions survive and remain useful inside pytest:

```text
fixed corpus addresses
fixed 300-line windows
exact byte preservation
private Witness acquisition results
external cat invocation inputs and captured results
source and result references
invocation-local time count
```

None establishes this additional edge:

```text
private corpus material
--supplied by pytest Witness-->
operator invocation Locality
```

Processing, preserving, comparing, or capturing material inside a subprocess
does not supply it to the parent process.

## 8. Exact stop

```text
sixteen corpus files
↓
supplied_material_in_order() returns sixteen exact windows
↓
private pytest work preserves and invokes them
↓
pytest output contains test rendering only
↓
catalog and measurement artifacts contain function / SQL coordinates only
↓
no corpus byte occurrence reaches the provider
↓
no corpus Witness acquisition occurs in the invocation Locality
↓
downstream Locality and Measurement questions concerning the corpus do not yet arise
```

No existing current or historical outward Witness crossing for the exact
sixteen corpus windows was found.

This investigation therefore stops without printing or serializing
test-support values, relabeling tests, adding a corpus provider, bypassing
pytest, or changing the downstream Witness Locality road.
