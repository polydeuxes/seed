# External Material Representation Metrology Fidelity Recovery 001

## Scope, authority, and stopping point

This is one bounded, report-only Fidelity recovery on merged `main` after PR
2007. It changes no implementation, test, fixture, schema, export, interface,
event, persistence, projection, canonical Book chapter, root documentation,
`docs/` content, or prior report. Prior reports supplied leads and
counterevidence only; current implementation, tests, and the active Book
control.

**Governing answer:** the reusable Structure Probe does not encounter external
material as source bytes. Its request requires a Python `str`, an encoding name,
and a hash. The caller has already acquired, bounded, decoded or constructed,
and classified the material as text before the probe begins. The probe encodes
that string under the caller-supplied name and hashes the resulting bytes. This
can validate a round trip to the manifest hash; it cannot establish that the
name was declared by the source, detected from the source, or the correct
source-relative decoding.

The first absent crossing, and this report's stopping point, is:

```text
exact acquired source bytes + source-relative representation testimony
  -X-> evidence-preserving representation examination / decoded-text handoff
       that keeps the bytes, decoding claim, decoded representation, and their
       relationship separately reopenable
  -> ExternalMaterialStructuralProjectionRequest(exact_text, encoding, hash, ...)
```

The campaign is an important local counterexample: it retains a file, hashes
its bytes, and explicitly decodes UTF-8. That local file makes the selected
specimen reopenable in this repository. It does not alter the reusable request,
manifest, CLI, or projection boundary, and its `encoding="UTF-8"` is campaign
testimony plus compiled decoder choice rather than detected or verified
representation competency.

This recovery does not design a universal media system, detect codecs, or enter
mathematics, physics, semantics, modality grammar, or competency
establishment.

## Governing distinctions

The implementation supports all of the following refusals:

```text
exact bytes
!= decoded text

declared encoding
!= detected encoding
!= verified decoding

ASCII-compatible bytes
!= uniquely ASCII

successful decoding
!= correct decoding

format
!= codec
!= decoded representation
!= measured structure
!= semantic meaning

hash identity
!= representation identity
!= source identity

compiled decoder behavior
!= evidence-born representation competency
```

In particular, `encoding` is a required nonempty string, not a standing claim
with provenance or status. Python accepting that codec name proves compiled
codec availability. Successful `str.encode(name)` and hash equality prove only
that the supplied string re-encodes under that convention to hash-identical
bytes. Neither operation detects the original representation or verifies that
the decoded characters are the intended characters.

## Current road

The complete active road recovered is:

```text
external source material
  -> campaign author, API caller, or CLI-input author acquires and classifies it
  -> caller decodes bytes or constructs a JSON/Python string
  -> caller constructs manifest identities, counts, artifact hash, encoding name,
     and exact_text
  -> CLI optionally decodes the request document via Path.read_text(), then JSON
  -> ExternalMaterialStructuralProjectionRequest
  -> manifest/source/artifact relationship checks
  -> exact_text.encode(request.encoding)
  -> SHA-256 of those newly encoded bytes and manifest-hash comparison
  -> splitlines(keepends=True) over the Python string
  -> exact projected text lines + maximal nonblank line regions
  -> line/region character-length surface features (raw line text omitted)
  -> campaign record, CLI/human/JSON renderers, diagnostic inventory/shape audit,
     and examination-work references
```

There is no reusable acquisition producer on this road. There is no decoder
that consumes artifact bytes inside `project_external_material_structure`.
There is no encoding detector, byte artifact field, decoding-evidence record,
byte-offset map, normalization record, replacement record, or representation
conflict field. There is also no active PESC comparer over these projections,
as PR 2007 correctly recovered.

## Crossing audit

| Crossing | Exact input and producer | Encoding standing | Hash timing and identity | Coordinates, loss, Unknowns, refusal | Exact consumer |
| --- | --- | --- | --- | --- | --- |
| External source -> acquisition | Not owned by the reusable road. The campaign says an operator inspected Project Gutenberg material and copied an excerpt into a repository file. | Campaign `SourceArtifactIdentity` reports UTF-8; the reusable manifest has no encoding field. Nothing detects it. | Campaign `source_identity()` hashes retained selected-excerpt bytes. The selected artifact hash is not the full parent/source hash, which the manifest preserves as Unknown. | Parent byte offsets and full parent hash are Unknown. Copy/selection fidelity is attributed to the operator, not established by Seed. | Campaign-local source identity and selection producers. |
| Acquired material -> decoding/string construction | Reusable API caller supplies `exact_text: str`. Campaign `lesson_selection()` calls `selected_lesson_bytes().decode("utf-8")`. CLI input author serializes a string in JSON; the CLI first calls `Path(...).read_text()` on the JSON envelope. | API/JSON request supplies/trusts a codec name. Campaign hard-codes UTF-8. CLI envelope decoding is Python `Path.read_text()` default behavior and is separate from the payload's `encoding`. No source declaration, inference, detection, confidence, BOM evidence, or verification is represented. | Campaign hashes before decoding. Generic CLI/API has only the caller-provided hash and decoded string at entry. | The first representation change occurs at caller decoding or string construction, before request construction. Decode errors/replacement/normalization before the call are invisible. Campaign strict UTF-8 decoding refuses invalid UTF-8; CLI refuses unreadable/non-default-decodable JSON before parsing. | Request constructor / `from_json_dict`. |
| String + metadata -> manifest/request | `ExternalMaterialManifest` supplies source/artifact identifiers, locations, hashes, counts, bounds, annotations, and Unknowns. Request supplies matching ids/hash plus codec name, exact string, and projection Unknowns. | Merely trusted. Manifest cannot corroborate encoding because selected artifact records contain no encoding. | Artifact hash is an asserted identity join. Source identity is a separate record and may be empty. Artifact location is a locator, not retained bytes or proof of source identity. | Manifest and request Unknown tuples survive in their own inputs, but only request Unknowns enter the structural projection. Manifest/source/artifact Unknowns and conflicts are not joined into projection Unknowns. Malformed types/required values refuse deterministically. | `project_external_material_structure`. |
| Request -> hash validation | Producer is `project_external_material_structure`; exact operational input is `request.exact_text`, a Python Unicode string. It constructs bytes with `exact_text.encode(encoding)`. | Codec name is used, not detected or verified. Python codec lookup is compiled behavior. | Hashing occurs **after prior decoding**, over newly encoded text bytes. The probe has one hash field, not separately preserved source-byte and decoded-representation hashes. Correct round trips can coincide with the original byte hash; coincidence does not prove correct decoding. | Refuses unknown codec, unencodable characters, or hash mismatch. It does not expose encoded bytes, byte length, codec canonical name, decode errors, replacement, normalization, or byte/character alignment. | Remaining structural projector body. |
| Validated string -> structural projection | `splitlines(keepends=True)` acts on the supplied `str`; lines retain exact string slices and terminators. `strip()==""` defines blankness; contiguous nonblank lines form regions. | No further encoding operation. Output repeats the trusted name. | Artifact hash is copied. Stable line/region ids incorporate artifact hash and character coordinates, but are not representation-identity records. | Zero-based half-open **character** offsets, not byte offsets. Python `len` counts code points, not grapheme clusters or encoded bytes. No Unicode normalization occurs in the probe, but any earlier normalization is unknowable. Request projection Unknowns survive; line/region Unknowns are empty. Refuses manifest/source/artifact mismatch, re-encoded hash mismatch, line-count mismatch, and character-count mismatch. | Surface-feature producer, CLI/JSON/human formatter, campaign record, tests. |
| Structural -> surface-feature projection | Existing structural projection with exact line text, ids, order, blank/terminator flags, and regions. | No encoding examination. | Artifact hash and derived structural identity survive; raw text is intentionally not copied. | Measures raw/content/terminator **character** counts, sequences, and totals. Validates duplicate/unknown/out-of-order structural references. Projection Unknowns survive. Reopening text requires retaining the upstream structural value; reopening bytes is not supported by either artifact alone. | CLI/JSON/human rendering, campaign record, tests, diagnostic visibility, examination-work references. |
| Features -> current consumers | Returned artifacts and serialized views; campaign embeds them. Examination planning refers to representation ids/contracts rather than interpreting content. | Consumers do not improve encoding standing. | Hash remains a join/reference value. | No current consumer lawfully relies on a representation correctness, source decoding, codec, format, or semantic claim. No current comparison producer follows. | Operators/tests/diagnostic inspection and campaign reporting; no semantic or competency consumer. |

## Bounded specimens

These specimens expose the boundary; they do not establish a format or codec
grammar.

### 1. ASCII-compatible bytes also valid UTF-8

```text
bytes: 41 0a                 (b"A\n")
ASCII decode: "A\n"
UTF-8 decode: "A\n"
```

Both codec labels re-encode the same string to the same bytes and therefore the
same SHA-256. Two requests differing only in `encoding="ascii"` versus
`encoding="utf-8"` can both pass against one artifact hash and yield the same
lines/features. The output preserves the caller's differing label, so it can
distinguish two **claims**. It cannot determine whether the source was uniquely
ASCII, UTF-8, or another ASCII-compatible representation. Byte compatibility
is not codec identity.

### 2. Unicode UTF-8 with non-ASCII code points

```text
bytes: c3 a9 0a              (UTF-8 bytes for "é\n")
UTF-8-decoded string: "é\n"  (2 Python characters)
Latin-1-decoded string: "Ã©\n" (3 Python characters)
```

Both strings can re-encode under their respective conventions to the **same
bytes** and hash. Thus both can pass the present validation if the caller also
supplies matching character counts. The structural results differ in character
counts and text while sharing a byte hash. This directly demonstrates:

* different decoded strings can arise from the same bytes under different
  conventions;
* hash identity does not select the correct decoded representation;
* successful reversible decoding does not establish correct decoding; and
* the current probe measures whichever string the caller chose.

Conversely, the same decoded string `"é\n"` encoded as UTF-8 versus Latin-1 has
different bytes and hashes. If callers faithfully name each encoding and
manifest each byte sequence, current outputs can distinguish those particular
artifacts by hash and trusted label. They still do not retain the bytes or prove
the source-relative representation claim.

### 3. Opaque binary excluded from honest unchanged text ingress

```text
bytes: 00 ff 80 0a
```

This sequence is invalid UTF-8 and cannot enter `exact_text` as exact bytes: the
request field accepts only `str`, and JSON transports characters, not an opaque
byte value. A caller could refuse it, replace characters, use a reversible
single-byte mapping, or preclassify it into some textual rendering. Each option
is a caller transformation or classification. The reusable road records none
of those choices as decoding evidence. A Latin-1 round trip could preserve byte
hash equality, but the projector would then call NUL/U+00FF/U+0080/newline
Python characters and apply text line/blank/count rules. That is not unchanged
binary ingress and does not establish textual applicability.

### 4. Report-local PNG counterexample

Use only the eight-byte PNG signature as a modality counterexample:

```text
89 50 4e 47 0d 0a 1a 0a
```

It is not valid UTF-8. A caller could map it reversibly through Latin-1 and make
the current encoded-text hash pass. The Structure Probe would then split the
mapped string at CR/LF and count Python characters. Those are compiled text
operations, not PNG format examination, codec examination, image structure, or
semantic interpretation.

What does generalize is narrower: bounded artifact/source identifiers, a hash
join, explicit projection convention, stable derived identities, ordered
records, deterministic refusal, preserved Unknown carrier, read-only status,
and non-mutation declarations can describe measurements outside prose. What
does not generalize is the implemented input and metric: Python string,
character coordinates, `splitlines`, whitespace blankness, line terminators,
and line/region character lengths are decoded-text-local.

## Governing comparison

| Required distinction | Current result | Purpose-relative consequence |
| --- | --- | --- |
| Same decoded string from different byte encodings | Sometimes distinguishable by different artifact hashes and trusted `encoding` labels if the caller faithfully supplies both; original bytes are absent. Identical ASCII-compatible bytes collapse at hash/text while labels remain mere claims. | Adequate for consumers needing only the declared decoded string under a chosen convention; inadequate for reopening or verifying original representation. |
| Different decoded strings from the same mistaken decoding convention/source bytes | Can produce different structural text/counts with the same re-encoded byte hash when reversible conventions differ. No representation-evidence object relates the alternatives or marks conflict/correctness. | A text-measurement consumer may intentionally select one supplied string. A source-faithful consumer cannot infer which is correct. |
| ASCII-compatible UTF-8 from uniquely identified ASCII | Not established. The label is retained but not detected or verified; common bytes and decoded string are identical. | Often immaterial for character-line measurements; fatal to a claim of source codec identity. |
| Valid decoding from correct source-relative decoding | Not distinguishable. Codec success and hash round trip are weaker than source-relative correctness. | Fine only where the caller's chosen representation is the lawful measurement subject; blocks reopening the original interpretive choice as evidence. |
| Text material from caller-preclassified binary material | Not distinguishable from the request alone. Both arrive as `str`; `encoding` names re-encoding behavior, not material kind or applicability. | Current text consumers can rely only on caller-selected text. Substrate-general conclusions are unlawful. |

The important split is therefore not “every lost distinction is a defect.” For
the current campaign's line and length reporting, a strict, retained UTF-8 file
plus a caller-chosen string is locally sufficient. For provenance-sensitive
representation examination, byte offsets, source codec identity, decode
alternatives, or later reopening without external state, the loss occurs before
the probe and is constitutive rather than cosmetic.

## PESC at the current frontier

PESC can disclose the loss but cannot repair it:

* **P — projection examined:** the earliest reusable probe projection is the
  caller-supplied decoded Python string as ordered projected lines; later P can
  be line/region character-count features. It is not source bytes.
* **E — equivalence:** exact Python-string or projected-line equality, or exact
  equality of declared feature tuples/predicates. It is character equality or
  feature equality, not byte equality unless an examiner separately retains
  and compares byte artifacts outside this road.
* **S — scope:** one manifest/source/artifact/hash-bound supplied decoded
  representation, or its projected lines/regions. The scope is not an exact
  byte artifact merely because re-encoding matched its asserted hash.
* **C — lawful consumer:** current CLI/JSON/human diagnostic inspection,
  campaign reporting, focused tests, and examination-work planning may rely on
  the bounded compiled text measurements they actually consume. No current
  consumer may promote them to correct encoding, source representation,
  modality structure, semantic meaning, or evidence-born competency.

PESC cannot reconstruct erased bytes, choose among decodings, establish a
source declaration, convert character offsets into source byte offsets without
additional evidence, or turn a compiled codec into representation competency.

## Direct answers

1. **Does current ingress preserve original bytes?** The reusable
   manifest/request/CLI/projection ingress does not. The campaign locally
   retains and hashes one selected file's bytes, but bytes are not carried into
   the request or outputs.
2. **Does Seed detect encoding or consume caller-decoded text?** It consumes
   caller-decoded or caller-constructed text and a trusted encoding name. The
   campaign invokes compiled UTF-8 decoding; no current owner detects encoding.
3. **Where is the first representation-changing occurrence?** At acquisition
   selection/copying if that changes the source, otherwise at the caller's
   bytes-to-string decoding or string construction. For the reusable road this
   is already upstream and unevidenced when the request arrives. The campaign's
   explicit first bytes-to-text change is `.decode("utf-8")`.
4. **Is the current hash over bytes, encoded text, or both?** The campaign hash
   is over retained bytes before decode. Reusable projection validation hashes
   bytes newly produced by encoding the supplied string. One hash value is
   compared; source bytes and encoded-text bytes are not separately preserved.
5. **Can current evidence distinguish ASCII from ASCII-compatible UTF-8?** No.
   It can retain different caller labels, not establish which representation
   the shared bytes uniquely had.
6. **Can the original byte representation be reopened?** Not from the reusable
   request or projection artifacts. The campaign's repository file can be
   reopened through external location state; a generic locator may be empty,
   stale, or unavailable and is not byte preservation.
7. **What exact material can the Structure Probe currently measure?** The exact
   supplied Python string under its declared string coordinate/splitting
   conventions: ordered physical line slices, blankness, terminators, maximal
   nonblank regions, and later character-count features.
8. **What material is excluded before it begins?** Opaque bytes, invalidly
   decoded material, undecoded BOM/codec evidence, byte offsets, decoder
   alternatives/errors/replacements, source representation declarations, and
   any binary material not already caller-transformed and preclassified as a
   string.
9. **Is the current probe a text metrology instrument or a substrate-general
   instrument?** Its implementation is a decoded-text metrology instrument.
   Its constitutional restraint has substrate-general parts.
10. **Which constitutional parts already generalize beyond text?** Bounded
    identity and scope, explicit measurement convention, deterministic
    measurement/refusal, stable occurrence identity, order, Unknown
    preservation, non-interpretation, read-only behavior, no event-ledger
    writes, no cluster mutation, and purpose-limited consumer reliance.
11. **What is implementation-local to decoded text?** `str`, codec-driven
    re-encoding, Python code-point counts, character offsets,
    `splitlines(keepends=True)`, CR/LF terminator treatment, `strip` blankness,
    nonblank line regions, and line-length features.
12. **What is the first exact missing crossing toward evidence-born
    representation examination?** Exact acquired bytes plus attributed
    representation testimony do not cross into a separately preserved
    bytes/decoding/decoded-representation relationship before the current
    decoded-text request. That is the first absent crossing; this report stops
    there.
13. **Which responsibility owns that crossing?** **Unknown.** Acquisition owns
    obtaining and bounding material; representation metrology would examine
    what representation evidence exists; competency probing would be stronger
    and cannot be inferred from compiled decoding. Current producer-consumer
    evidence does not warrant assigning the absent crossing to one of them.
14. **Does this recovery enter mathematics, physics, semantics, or
    modality-specific competency?** No. The PNG signature is only a negative
    generalization witness. No format grammar, codec detection, image meaning,
    mathematics, physics, or competency standing is recovered.

## Fidelity disposition

The present road is faithful when described as **hash-checked metrology over a
caller-supplied decoded text representation under a trusted re-encoding
convention**. It is unfaithful to describe it as exact-source-byte ingress,
encoding detection, verified decoding, representation identity, or
substrate-general structure examination.

No current downstream consumer independently requires a new production
crossing, and this report makes no implementation recommendation. The missing
crossing remains a localized fidelity frontier and **Unknown responsibility**,
not a universal byte envelope, codec registry, detector, media pipeline,
automatic selector, semantic classifier, or representation learner.

## Commands and probes

All commands were read-only except creation of this report and the required
commit/PR workflow:

```text
find .. -name AGENTS.md -print
git status --short --branch
git log -8 --oneline --decorate
git show --stat --oneline HEAD
git show --format=fuller --no-ext-diff HEAD
rg -n "ExternalMaterialStructuralProjectionRequest|Structure Probe|structure probe|surface.feature|surface_feature|external material" --glob '!*.md' .
rg -n "class ExternalMaterialManifest|ExternalMaterialManifest\\(" seed_runtime scripts campaigns tests
rg -n "P —|projection or representation|declared equivalence|sameness rule|consumer.*purpose|measurement boundary|exact equality" book_of_seed --glob '*.md'
rg -n "project_external_material_surface_features\\(|structural_projection\\(\\)|surface_feature_projection\\(" seed_runtime campaigns scripts tests --glob '*.py'
sed -n '1,260p' seed_runtime/external_material_structural_projection.py
sed -n '1,240p' seed_runtime/external_material_testimony_binding.py
sed -n '1,230p' seed_runtime/external_material_surface_feature_projection.py
sed -n '1,290p' campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py
sed -n '990,1025p' scripts/seed_local.py
sed -n '6000,6060p' scripts/seed_local.py
sed -n '1,180p' tests/test_external_material_structural_projection.py
sed -n '1,140p' tests/test_external_material_surface_feature_projection.py
python - <<'PY'
from hashlib import sha256
specimens = [b"A\\n", "é\\n".encode("utf-8"), bytes([0,255,128,10]), bytes.fromhex("89504e470d0a1a0a")]
for raw in specimens:
    print(raw.hex(), sha256(raw).hexdigest())
raw = "é\\n".encode("utf-8")
for codec in ("utf-8", "latin-1"):
    text = raw.decode(codec)
    print(codec, repr(text), len(text), text.encode(codec) == raw)
PY
pytest -q tests/test_external_material_structural_projection.py tests/test_external_material_surface_feature_projection.py
git diff --check
```
