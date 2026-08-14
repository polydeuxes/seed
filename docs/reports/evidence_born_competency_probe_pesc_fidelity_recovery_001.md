# Evidence-Born Competency Probe PESC Fidelity Recovery 001

## 1. Boundary, authority, and governing answer

This is one bounded, report-only Fidelity recovery against commit `ea120c7`
after PR 2013. It adds no probe, diagnostic, audit, CLI, schema, event, Fact,
projection, competency standing, parser, codec, test, or production behavior. It
does not edit a canonical Book, root documentation, `docs/`, a prior report, or
any implementation. Current code and tests control; prior reports are navigation
and counterevidence only.

**Governing answer.** The smallest truthful implementation slice is a read-only
**exact-window recurrence measurement over explicitly selected, already-existing
string-bearing Evidence payload leaves**. The caller must supply all four PESC
terms: the leaf-to-UTF-8-byte representation and window width (**P**), exact byte
equality (**E**), a finite set of Evidence ids plus per-item/window bounds (**S**),
and a named inspection purpose whose only permitted reliance is candidate
measurement (**C**). The output must preserve every matching occurrence's
Evidence id, payload path, byte coordinates, count, exclusions, loss, and STOP
boundary. It may say only that equal byte windows recur in that declared scope.

That slice searches evidence material rather than developer-precompiled domain
structures. It can encounter unfamiliar Unicode or ASCII without naming a
language. It deliberately cannot yet inspect PNG, PCM, or H.264 bytes because
the generic Observation -> Evidence road does not preserve arbitrary raw binary
blobs as a reopenable byte substrate. A report claiming foreign binary support
now would invent evidence. Binary acquisition is a later missing-evidence issue,
not a reason to smuggle codec signatures into the first comparer.

PESC is therefore **(2) partially implemented with one missing owner**, with an
important qualification: its terms occur separately in several bounded roads,
but no evidence-generic owner binds them into one measurement occurrence.
Documentation Structure binds all four for its compiled Markdown destination;
external-material projection supplies an occurrence-bearing P and S but no
comparer; Observation Agreement and Grammar Observation compare compiled record
fields/shapes without a caller-declared PESC contract. PESC is also constitutional
grammar for lawful disclosure. It is not yet a repository-wide abstraction and
does not warrant a universal request schema.

The first slice stops at:

```text
selected existing Evidence string leaves
  -> declared UTF-8 byte-window projection
  -> exact-equality groups with addressable occurrences
  -> bounded recurrence measurement for one inspection purpose
  -> STOP
```

It does not form an abductive semantic candidate, make a deductive prediction,
acquire more evidence, generalize, issue a Fidelity finding, or establish
competency. Those later stages remain separately unwarranted.

## 2. Exact current PESC topology

### 2.1 Event Ledger Observation/Evidence road

```text
Observation(id, source_type, observed_at, subject, predicate, value,
            confidence, metadata, dimensions, expires_at)
  -> ObservationIngestor.observation_to_evidence
  -> Evidence(id, workspace_id, source, kind, observed_at, payload, confidence)
  -> observation.observed + evidence.observed + optional fact event
  -> EventLedger / SQLiteEventLedger append order
  -> StateProjector
  -> State.observations / State.evidence / State.facts and derived support
```

The producer chooses the Observation fields. `ObservationIngestor` then chooses
the Evidence representation: it nests observation id, source type, subject,
predicate, value, metadata, dimensions, and expiry in a generic payload. Event
serialization preserves this material only if it is serializable. The ledger
assigns event identity, timestamp, workspace, actor, session, causation, and
correlation, but those envelope coordinates are not copied into `Evidence`.

There is **no recurrence E**, no counting S beyond ledger/workspace listing, and
no recurrence consumer C. Append order is preservation order, not a sameness
rule. Repeated equal payloads remain distinct Evidence/event occurrences, which
is valuable input, but State projection does not compare them as recurrence.

Eight-dimensional survival (orientation only, not a universal schema):

| Dimension | Survives | Loss before comparison |
| --- | --- | --- |
| subject / identity | Observation, Evidence, and event ids; subject in payload; workspace on Evidence/event | Evidence lacks producing event id; arbitrary payload leaves have no canonical leaf occurrence id |
| assertion / content | predicate, value, metadata, dimensions | source normalization may already compress physical source bytes; binary content is ordinarily absent |
| standing | generic Evidence and optional mechanically promoted Fact | no recurrence, candidate, finding, or competency standing |
| source / provenance | source type, source label, observed time, confidence | producer implementation/version, acquisition byte range, content hash, and chain to event envelope are not intrinsic to Evidence |
| responsibility | ingestor and ledger implementation are identifiable in code | no responsible recurrence examiner or admission owner |
| authority / warrant | actor exists on event; source testimony is preserved | no authority to compare for a purpose or rely on recurrence |
| scope / locality | workspace, subject, dimensions, expiry may survive | no corpus completeness, leaf inclusion rule, byte bound, or comparison horizon |
| occurrence / preservation | distinct event, Observation, and Evidence ids and append order | invocation context may be missing; equal representations have no comparison occurrence |

The searched-for structure is evidence-born only at the payload-value level.
The payload schema and all observation source normalizers are compiled producer
choices. Treating predicate names or source-specific metadata keys as discovered
grammar would be contamination.

### 2.2 Projected State

`StateProjector` replays workspace events and decodes known event kinds into
typed Observation, Evidence, and Fact objects, then rebuilds support, evidence
relations, conflicts, expiry-sensitive current selection, and indexes. State is
a consumer-oriented projection of ledger material, not a raw corpus and not a
recurrence examiner.

* **P:** typed State dictionaries and derived indexes, selected by developer
  event decoders and model schemas.
* **E:** id-key replacement/lookup, predicate/value rules, currentness and
  conflict rules local to each projection; none is evidence-content recurrence.
* **S:** one workspace replay/as-of event selection plus projection rules.
* **C:** current State and read-model construction.

State preserves useful identity/content/standing/provenance/scope/occurrence
coordinates inherited from events. It also loses event-envelope adjacency when
consumers take only the projected Evidence object, and most read models further
compress payload, conflicts, time, and Unknowns. A recurrence probe should read
the exact selected `State.evidence` records or ledger evidence events, not Facts,
candidate views, summaries, or current-fact indexes. Otherwise comparison begins
after assertion and provenance loss and silently searches projection policy.

### 2.3 Structure Probe

“Structure Probe” currently has two materially different parts:

1. `StructureObservationBoundary`, a boundary declaration shared by substrate
   adapters. It owns no parser, grammar, lexicon, recurrence, or record schema.
2. The external-material manifest/binding/structural/surface road, which validates
   caller-supplied identity, encoding and hash, projects exact text into physical
   lines and maximal nonblank regions, then measures line/region lengths.

For the external road:

| PESC term | Current owner |
| --- | --- |
| P | developer-compiled `splitlines(keepends=True)`, blank predicate, regions, and raw/content/terminator counts over caller-supplied exact text |
| E | only identity/hash validation and exact field equality internal to validation; no cross-occurrence recurrence comparer |
| S | one manifest/source/artifact/hash and its line/region coordinates |
| C | read-only structural/surface measurement, explicitly not semantics or grammar |

Exact line text, distinct duplicate line occurrences, ordering, coordinates,
hash, encoding, line/region ids, feature convention, Unknowns and mutation limits
survive. Feature projection intentionally drops raw text while retaining the
structural projection identity. Invocation time, durable recording, cross-artifact
corpus, producer version, consumer-specific loss decision, and comparison
occurrence do not survive. Physical-line structure is produced from evidence;
the line and region representation is nevertheless compiled measurement policy.
No current producer searches those records for recurrence.

### 2.4 Documentation Structure Probe

```text
selected top-level repository .md files
  -> UTF-8 decode + compiled regex/state parser
  -> headings, sections, front matter, links, fences, architectural relations
  -> Counter over exact compiled fields and skeleton tuples
  -> DocumentationStructureRecurrenceReport
  -> CLI/JSON/human documentation-inspection consumer
```

Its PESC is complete but destination-specific:

* **P:** `DocumentationStructureRecord` fields selected by developer code.
* **E:** exact Python string/integer/tuple equality for section labels, keys,
  depths, fence languages and skeleton signatures; outlier predicates are also
  compiled.
* **S:** files selected by repository traversal/options, then min/max/top/limit
  and feature-specific document membership.
* **C:** read-only repository documentation structure inspection.

Path, line/byte counts, headings with coordinates, section hierarchy, links,
fences, selected relation evidence, counts and distributions survive to varying
output detail. Raw bytes, most prose, stripped heading whitespace, suppressed
fence content, parsing alternatives, grammar provenance, applicability Unknowns,
and excluded documents are lost before or during comparison. The structure
searched for comes from developer-compiled Markdown expectations. Counts are
evidence about that parser's output, not evidence-born grammar learning.

### 2.5 `CapabilityCandidate`

```text
projected Fact(predicate == package_installed)
  -> lowercase package value
  -> fixed _PACKAGE_CAPABILITY_CANDIDATES lookup
  -> CapabilityCandidate + lossy Fact/Evidence summaries
```

* **P:** current projected package Facts and normalized package-name string.
* **E:** exact membership in a fixed developer table; filter aliases are another
  compiled normalization.
* **S:** supplied State/current Fact index and optional filter.
* **C:** preserve package-derived capability candidates for inspection.

Candidate label, Fact id/predicate/subject/value/source/confidence, Evidence ids
and summaries survive. Evidence payload, observed time, expiry, event identity,
package version/architecture, conflicts, producer occurrence, locality binding,
grammar, mechanism and consumer applicability are lost. The destination
structure (`python3 -> python_runtime`, etc.) is entirely developer-precompiled.
This road must not seed an evidence-born recurrence search.

### 2.6 `VerificationEvidence`

```text
package-derived CapabilityCandidate
  -> fixed _CAPABILITY_BINARY_CANDIDATES lookup
  -> ordered PATH scan
  -> first path that is_file && X_OK per compiled binary name
  -> VerificationEvidence
```

* **P:** candidate strings, compiled binary filenames, process PATH entries and
  live filesystem metadata.
* **E:** exact candidate-table membership, exact filename construction, and the
  conjunction `is_file && X_OK`; this is not behavioral equivalence.
* **S:** package-gated candidates and current process PATH order.
* **C:** support a later verification inspection that no longer exists after PR
  2013; single-capability presentation remains a visibility consumer.

Candidate/path/source labels and denial notes survive. Candidate support,
package/path provenance relation, PATH snapshot, host/workspace, symlink/stat
identity, time, errors, alternate hits, contents, loader, dependencies, argv,
inputs, outputs, and transformation evidence are lost. Both candidate and binary
structures are compiled developer expectations. An executable present without
package-derived candidacy is invisible. Executable presence is not transformation
evidence.

### 2.7 Observation Agreement and Grammar Observation

Observation Agreement consumes three already-compiled record families,
extracts their evidence text, groups by exact text, and emits only groups with
at least two distinct stream labels. Grammar Observation then parses exactly one
of a fixed set of relation operators, normalizes each side to `term`, groups by
that compiled shape, and emits only shapes backed by at least two agreement
records.

These are real comparison/recurrence islands, but not the missing generic owner:

* **P:** developer-selected textual fields, then a compiled `term OP term` shape.
* **E:** exact evidence-text equality, distinct stream-name count, exact operator
  parsing, then shape-string equality.
* **S:** supplied record sequences; “independence” is distinct string labels,
  not independently established source occurrence.
* **C:** candidate agreement and recurring relation-shape observation only.

Provenance strings and supporting records survive. Original source bytes,
complete corpus, source independence warrant, nonmatching records, ambiguity,
operator escaping/context, frequency beyond the threshold, and consumer-local
applicability are absent or compressed. The accepted record types and relation
operators are developer-precompiled domain structure. Calling this learned
grammar would collapse compiled parsing into learning.

## 3. Missing-owner and missing-evidence table

| Crossing/material | Current producer | Missing owner | Missing evidence or disclosure | Consequence |
| --- | --- | --- | --- | --- |
| ledger Evidence -> examinable scalar occurrences | Observation ingestor + State projector | bounded evidence-material selector | payload-leaf ids/paths, inclusion/exclusion record, serialization convention | comparer cannot yet identify exactly what it examined |
| selected occurrences -> PESC measurement | none | **first-slice owner: read-only evidence recurrence measurement** | explicit P/E/S/C, measurement occurrence id, coordinates, excluded-material reasons, loss | no honest evidence-generic recurrence result exists |
| raw binary source -> Evidence bytes | source-specific observers do not generically retain blobs | future attributed binary acquisition/preservation owner | byte content or reopenable hash-bound blob, byte offsets, media/container provenance, size bounds | PNG/PCM/H.264 recurrence cannot be searched today without invention |
| external structural records -> recurrence | structure/surface projectors | external-record comparer, only if a consumer demands it | corpus identity, cross-artifact scope, E and C | occurrence-bearing input exists but no Seed comparison |
| recurrence -> abductive candidate | none generically | Unknown, later | alternative hypotheses, negative/counterexamples, provenance and loss | recurrence must STOP as measurement |
| candidate -> prediction | none | Unknown, later | falsifiable expected representation, scope and failure rule | candidate is not prediction |
| prediction -> new acquisition/comparison | none | Unknown, later | acquisition authority, independent occurrence, comparison convention | prediction is not verification |
| scoped induction -> Fidelity finding | none | Unknown, later | sufficiency, conflicts, Unknowns, consumer relevance, responsible finding occurrence | frequency cannot become significance |
| Fidelity finding -> competency standing | no admission owner after prior excisions | Unknown, later | transformation identity, applicability, mechanism/result evidence, authority/currentness | no competency promotion is warranted |
| package candidate -> executable observation | `VerificationEvidence` | truthful observation owner/name still unresolved | package/path locality, occurrence time, errors, all hits | current name overstates metadata check |

The one owner missing for the first slice is intentionally narrow. It owns a
measurement result, not evidence acquisition, semantic interpretation,
candidate formation, finding admission, or competency establishment.

## 4. Contamination boundary

### Evidence-first measurement (inside)

* begins only with selected existing Evidence ids;
* addresses literal string leaves by payload path without interpreting key names;
* uses an explicit UTF-8 encoding and fixed-width byte windows;
* compares windows by exact byte equality only;
* retains every occurrence separately even when values are equal;
* counts only inside declared Evidence/item/window bounds;
* identifies omitted non-string/binary material and truncation as known loss;
* states the exact consumer purpose and denies stronger reliance.

### Compiled destination knowledge (outside)

* selecting only `predicate=package_installed` or mapping packages to capabilities;
* selecting filenames because they are known executables;
* recognizing Markdown headings, front matter, fences, links or sections;
* embedding PNG magic bytes, RIFF/WAVE chunks, PCM framing, H.264 NAL units,
  container boxes, encodings beyond declared UTF-8, language tokens, formulas,
  codecs, morphology, or semantic similarity;
* normalizing case, whitespace, Unicode, punctuation, paths or ASTs and calling
  the result equivalence without a separately warranted rule;
* ranking repeated windows as important, explanatory, causal or competent.

Exact equality is one lawful E, not a universal equivalence. A fixed window is
one lawful P, not a discovered grammar. A frequent window is not significant.
Two objects sharing a window are not materially equivalent. Consumer purpose
limits reliance; it does not grant authority or make the measurement true.

## 5. Asymmetric specimen cross-examination

### 5.1 Recurring ASCII and Unicode across unrelated Evidence

If independently addressed Evidence string leaves contain `alpha` or the same
UTF-8 sequence for `λ`, a window-width-matched measurement can report their
exact repeated bytes and coordinates. It cannot infer word, letter, token,
language, common source, or meaning. Unicode code-point or grapheme equivalence
is not implemented: canonically similar spellings remain different bytes.

### 5.2 PNG, PCM, H.264 signatures or container structure

Current generic Evidence supplies no guaranteed raw-byte substrate. A textual
hex dump is text about bytes, not those bytes. The first slice must list raw
binary as excluded/unavailable and STOP. Later attributed blob preservation may
permit exact windows, but codec/container parsing remains outside unless a
separate consumer warrants a compiled representation. No signatures are added.

### 5.3 Markdown structures already recognized by compiled code

Documentation Structure may count two `## Heading` instances as heading/section
records because its regex and parser already supply that interpretation. The
first slice sees only equal byte windows in Evidence strings and cannot call
them headings. Parallel results are not equivalent standings: one measures a
compiled Markdown projection; the other measures literal evidence bytes.

### 5.4 Novel executable without package-derived candidacy

`VerificationEvidence` emits nothing because package candidacy gates inspection.
The proposed recurrence measurement may encounter the executable's path string
only if some existing Evidence already contains it; it still has no file-content
or transformation evidence. Presence, X_OK metadata, invocability, behavior and
competency remain distinct.

### 5.5 Materially different objects sharing a superficial pattern

A prose observation and a base64-looking configuration string may share an
exact four-byte window. Both occurrences count under E. The output must not
merge subjects, infer similarity, correlate causes, or suggest a common grammar.
This is the decisive negative test against treating recurrence as equivalence of
objects.

### 5.6 Real transformation with little recurrence

A single hash-bound external-material projection can demonstrably transform
exact supplied text into addressable line measurements even if no window recurs.
Zero or one recurrence says nothing about whether the transformation occurred,
is useful, or is competent. Frequency cannot substitute for transformation
input/output evidence.

### 5.7 Purpose-relative recurrence

Repeated delimiter bytes may matter to a consumer checking whether truncation
markers contaminate a bounded evidence export, while being immaterial to a
consumer checking whether two source observations were independently acquired.
The same count may be lawfully relied on for the first declared inspection and
not the second. C bounds reliance; it does not change the count, confer authority,
or establish significance automatically.

## 6. Smallest implementation-ready first slice

Implement, in a later PR, one pure read-only producer with no CLI initially:

1. **Input:** projected `State`, an explicit ordered tuple of Evidence ids, an
   explicit tuple of included payload paths (or a strict “all string leaves”
   selector recorded in output), `encoding="utf-8"`, positive fixed window width,
   per-leaf maximum bytes/windows, and nonempty consumer-purpose text.
2. **Validation:** reject unknown/duplicate Evidence ids, unknown selected paths,
   non-string selected leaves, invalid bounds, and any implicit whole-workspace
   selection. Do not stringify arbitrary objects.
3. **Projection:** encode each selected string exactly as UTF-8; enumerate
   overlapping fixed-width byte windows with zero-based half-open byte offsets.
4. **Equivalence:** exact byte equality only. No normalization, tokenization,
   regex, hashing as a substitute for retained bytes, approximate match, or
   domain signature.
5. **Scope/counting:** count distinct addressed window occurrences inside the
   supplied Evidence/path/bound set. Preserve same-Evidence and cross-Evidence
   counts separately; require at least two occurrences to label `recurring`.
6. **Output:** stable content-derived measurement id, P/E/S/C declarations,
   Evidence id + payload path + coordinates for every occurrence, exact window
   bytes in a JSON-safe encoding, counts, exclusions, truncations, Unknowns,
   known loss, `read_only=true`, `writes_event_ledger=false`, and
   `mutates_cluster=false`.
7. **Standing:** `measurement_only`; names must not include capability,
   verification, grammar, significance, finding, promotion, or competency.
8. **Tests:** ASCII/Unicode exact recurrence; composed/decomposed Unicode stays
   unequal; overlap/count bounds; unrelated objects sharing a window remain
   distinct; non-string/binary refusal; no recurrence; purpose changes identity
   but not counts; deterministic ordering; no ledger/state mutation.

This is implementation-ready but intentionally not a universal grammar. If a
CLI/diagnostic/recording surface is later added, the operational visibility
contract applies then: inventory, shape audit, their tests, diagnostic-run
record scope, and nonmutation proof must accompany it. The recommended first
slice avoids that surface and remains directly testable as a pure producer.

## 7. Explicit STOP conditions

The implementation pass must STOP and refuse or return bounded unavailability
when any of these holds:

* Evidence ids or payload paths are implicit, unknown, duplicate, or unbounded;
* selected material is not an existing string leaf or exceeds declared bounds;
* raw bytes are required but only a textual encoding/summary is preserved;
* representation, exact equality, counting scope, or consumer purpose is absent;
* a requested equivalence needs Unicode normalization, regex, tokenization,
  semantic similarity, file formats, codecs, language or domain knowledge;
* occurrence identity or byte coordinates cannot be preserved;
* truncation/exclusion cannot be disclosed;
* the caller asks the producer to rank significance, correlate sources, infer a
  mechanism, explain a pattern, form a semantic candidate, predict, acquire new
  evidence, verify, generalize, emit a Fidelity finding, or establish standing;
* recurrence is being used as evidence of object equivalence, competency,
  authority, currentness, transformation, or consumer uptake;
* recording would attach diagnostic-only output to cluster subjects or mutate
  cluster truth;
* satisfying the request would require adding a signature/grammar table.

No result, including a high count, may cross these stops.

## 8. Later deletion boundary

Deletion is warranted only after truthful material recurs in replacement owners
and every current consumer is migrated; naming discomfort alone is insufficient.

| Existing artifact | Earliest lawful deletion condition | Material that must recur elsewhere |
| --- | --- | --- |
| `CapabilityCandidate` | package-derived candidate presentation has no consumer, or a replacement evidence-measurement/candidate owner preserves its exact bounded use and denials | Fact/Evidence lineage, subject and package value, candidate association provenance, filters, read-only/no-selection/no-authority boundaries; compiled package mapping must be either explicitly retained as destination knowledge or intentionally retired, never relabeled learned |
| `VerificationEvidence` | candidate-correlated executable-file availability is renamed/reowned or no longer consumed | candidate/path association, exact `is_file && X_OK` measurement, PATH/locality/time/error scope newly made explicit, all current single-capability visibility, and denials of invocation/verification/authority; executable-only observations must not remain package-invisible accidentally |
| Structure Probe | each bounded external-material consumer uses a replacement with equal or intentionally revised measurement fidelity | manifest/source/artifact/hash/encoding validation, exact line text/order/coordinates, duplicate occurrence identity, nonblank regions, feature counts, Unknowns, refusal behavior, provenance reopenability, and no semantics/grammar/ledger/mutation boundaries |
| Documentation Structure Probe | every documentation inspection consumer has an evidence-born or intentionally compiled replacement whose applicability and differences are proven | traversal/options, UTF-8/refusal behavior, metrics, headings, sections, front matter, links, fences, architectural relation records, recurrence/distributions/outliers/skeletons, coordinates, output bounds, diagnostic visibility, and negative-authority contract |

The recurrence probe alone satisfies none of these deletion packets. Exact byte
windows do not replace package candidacy, filesystem metadata inspection,
external structural coordinates, or Markdown destination behavior. Eventually,
truthful common measurement material may move to narrower owners, after which
compatibility shells should be deleted rather than preserved indefinitely. The
compiled destination knowledge must either remain explicitly compiled or be
removed; it must never be backfilled as evidence-born.

## 9. Files inspected and LOC

The following current files were inspected directly for this recovery:

* `AGENTS.md`
* `seed_runtime/events.py`
* `seed_runtime/models.py`
* `seed_runtime/observations.py`
* `seed_runtime/evidence.py`
* `seed_runtime/facts.py`
* `seed_runtime/state.py`
* `seed_runtime/evidence_graph.py`
* `seed_runtime/capability_candidates.py`
* `seed_runtime/verification_evidence.py`
* `seed_runtime/structure_observation.py`
* `seed_runtime/external_material_testimony_binding.py`
* `seed_runtime/external_material_structural_projection.py`
* `seed_runtime/external_material_surface_feature_projection.py`
* `seed_runtime/documentation_structure.py`
* `seed_runtime/knowledge/observation_agreement.py`
* `seed_runtime/knowledge/grammar_observation.py`
* `seed_runtime/diagnostic_inventory.py`
* `seed_runtime/diagnostic_shape_audit.py`
* `scripts/seed_local.py`
* `tests/test_observation_agreement.py`
* `tests/test_grammar_observation.py`
* `tests/test_structure_observation.py`
* `tests/test_documentation_structure.py`
* `tests/test_projected_state_consumers.py`
* `tests/test_diagnostic_inventory.py`
* `tests/test_diagnostic_shape_audit.py`
* `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
* `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`
* `book_of_seed/05-evidence-and-knowledge/evidence.md`
* `book_of_seed/06-state-and-projection/events-facts-and-state.md`
* `book_of_seed/06-state-and-projection/projection-and-current-state.md`
* `evidence_born_competency_probe_frontier_fidelity_recovery_001.md`
* `capability_candidate_verification_readiness_fidelity_characterization_001.md`
* the parent diff for commit `ea120c7` (PR 2013)

**LOC added: 509 report lines (`git diff --numstat`). Production LOC added: 0; test LOC added: 0.**

## 10. Final adjudication

The exact topology contains strong evidence preservation, several compiled
representations, one compiled documentation recurrence consumer, and two narrow
agreement/shape grouping islands. It contains no evidence-generic PESC owner.
The first missing owner is not a competency probe in full; it is only a bounded
exact recurrence measurement producer.

The first slice should deliberately accept less material than the long-term
question names. Existing UTF-8 string leaves are truthfully available; generic
raw binary evidence is not. Exact byte equality is truthfully implementable;
semantic or format equivalence is not. Bounded recurrence is truthfully
reportable; significance, mechanism, finding and competency are not.

Therefore the lawful next implementation road is:

```text
existing selected Evidence strings
  -> disclosed fixed-width UTF-8 byte representation
  -> exact equality within explicit finite bounds
  -> occurrence-preserving recurrence measurement for one purpose
  -> STOP before candidate, prediction, acquisition, induction, finding,
     standing, execution, or promotion
```

That is the smallest slice that searches evidence rather than a developer's
precompiled destination grammar.
