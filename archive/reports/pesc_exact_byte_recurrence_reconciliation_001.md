# PESC Exact-Byte Recurrence Reconciliation 001

## 1. Boundary and governing adjudication

This is one bounded, report-only reconciliation of the proposed first PESC
implementation slice in PR 2014 (`f411d26`). It adds no capability, grammar
learning, significance, verification, promotion, competency standing, semantic
interpretation, binary decoding, CLI surface, diagnostic, event, persistence,
production code, or test. It does not amend PR 2014's report, a canonical Book,
root documentation, or `docs/`. Current implementation and canonical clauses
control; prior reports are testimony to cross-examine rather than authority.

**Adjudication: the PR 2014 proposal is a lawful specimen of one possible
compiled measurement instrument, not the first implementation of a general
evidence PESC owner.** In its exact proposed form, the producer compiles the
projection family: select an already-decoded string leaf, encode that string as
UTF-8, and enumerate overlapping fixed-width byte windows. The caller selects
Evidence records, leaf paths, width, and finite bounds, but does not supply an
arbitrary representation function. Therefore the report's statement that the
caller supplies P is too broad.

The proposal also lacks an evidenced consumer contract. Nonempty purpose prose
changes a requested artifact's content identity but neither constrains the
producer's measurement nor proves applicability, admission, authority, uptake,
or lawful reliance. Finally, a deterministic digest can identify the instrument
definition or equivalent measured content, but cannot identify an invocation.
Two executions over identical State and inputs are two producer occurrences,
even when every content field and count is equal.

The governing topology is consequently:

```text
current repository evidence
  -> no generic PESC owner warranted

exact selected Evidence string leaves
  -> possible local, developer-compiled UTF-8/window instrument
  -> exact recurrence measurement occurrence
  -> possible consumer-local use only under a separate operational contract
  -> STOP
```

Until one named consumer accepts the exact output under a bounded contract, the
proposal remains a **specimen proving that such a local instrument is possible**.
If that consumer is evidenced, the same narrow design may become **one compiled
PESC measurement instrument**. Neither state warrants a generic PESC owner or a
repository-wide PESC request grammar.

## 2. Corrected P: what is received and what is created

### 2.1 Representations that must remain distinct

| Representation | Status in the proposed road |
| --- | --- |
| Preserved source representation | Whatever the upstream source actually preserved. It may already have decoded, normalized, summarized, or omitted source material. The proposed producer neither receives nor recovers the physical source representation. |
| `Evidence.payload` representation | A Python/serialized mapping selected by the existing Observation-to-Evidence and State projection roads. It is a compiled Evidence representation, not source bytes. |
| Selected string leaf | One existing string value addressed by an explicit Evidence id and payload path. This is the immediate measurement substrate. A path is an address inside an Evidence payload, not a repository-wide leaf identity. |
| UTF-8 re-encoding | Bytes newly created by applying the producer's compiled `utf-8` encoder to the already-decoded string. These bytes faithfully represent that string under UTF-8; they do **not** recover original source bytes or prove the source used UTF-8. |
| Fixed-width byte windows | Newly created, ordered, overlapping slices of the UTF-8 re-encoding, addressed by zero-based half-open byte coordinates. They are measurement projection occurrences, not preserved source occurrences. |
| Caller-selected width | A positive bounded parameter to the compiled window procedure. It selects one definition instance; it does not make the projection algorithm caller-provided. |
| Caller-supplied representation | **Absent.** The proposal has no caller-supplied projector, projection artifact, codec, or equivalence implementation. Adding one would create an unexamined grammar and execution boundary. |
| Producer-compiled representation | **Present.** String-leaf selection semantics, UTF-8 encoding, overlapping-window enumeration, coordinate convention, truncation convention, and exact-byte grouping are developer-compiled measurement policy. |

### 2.2 Exact producer boundary

A possible local producer would receive:

* a read-only `State` projection with `workspace_id`, `projection_version`, and
  `last_event_id` when available;
* an explicit ordered, nonempty set of existing Evidence ids;
* explicit payload paths to existing string leaves (or one precisely specified,
  compiled all-string-leaves selector whose expansion is returned);
* a positive window width and finite per-leaf/per-request limits;
* a structured consumer contract, if a real consumer is later established; and
* occurrence coordinates supplied or created for this invocation.

It would create:

* one bounded projection of each selected decoded string into newly encoded
  UTF-8 bytes;
* overlapping windows under the compiled width/offset convention;
* exact-byte equality groups without normalization or interpretation;
* addressed window occurrences retaining Evidence id, payload path, and byte
  range;
* exclusions, truncations, Unknowns, and known loss; and
* one returned measurement artifact whose occurrence is distinct from its
  deterministic definition and content identities.

P therefore should not be a registered generic instrument or caller-provided
projection evidence. No repository evidence warrants either registry. For this
exact instrument, P should be an **explicit bounded projection declaration and
returned projection coordinates local to a developer-compiled producer**. The
request chooses operands and parameters; the implementation owns the method.
An independently preserved projection artifact is unnecessary unless a later
consumer requires reopening it. Pure returned testimony can preserve the
distinction without an event, ledger, or persistence.

## 3. Corrected P/E/S/C definitions for this instrument

| Term | Correct definition | Not established |
| --- | --- | --- |
| **P — projection/representation** | For each explicitly addressed existing string leaf, apply the producer-compiled UTF-8 encoder to the decoded string and enumerate all overlapping width-`w` byte slices within declared limits, preserving Evidence/path/offset coordinates and loss. | Original source bytes, arbitrary caller representation, decoded binary, character/code-point/grapheme windows, domain structure, tokens, or learned grammar. |
| **E — equivalence** | Two projected windows are equal iff their retained byte sequences are exactly equal. Group addressed occurrences without merging their Evidence, path, or offset identities. | Object equivalence, semantic similarity, Unicode canonical equivalence, source independence, significance, explanation, transformation identity, verification, or competency. |
| **S — scope** | The exact ordered Evidence-id set, expanded selected paths, State/workspace projection horizon, width, per-leaf/request bounds, inclusion/exclusion rules, and inspected Evidence identities used by this occurrence. | Workspace completeness, source-corpus completeness, unselected leaves, raw binary, historical Evidence outside the projection horizon, or future/current applicability. |
| **C — consumer contract** | A structured, consumer-local contract naming the bounded question, consumer, measurement subject, permitted assertion and reliance, required P, required S, exclusions, Unknown treatment, and mandatory refusal/STOP rules. | Authority from prose, automatic applicability/admission/uptake, permission to generalize, or proof that any consumer actually relied. |

The producer's only assertion is: under definition D, occurrence O inspected the
listed Evidence leaves at horizon H and found the listed exact-equal projected
window occurrences and counts within S. C may narrow whether a consumer can use
that assertion. C cannot change the observed counts, cure missing evidence, or
strengthen the assertion.

## 4. Consumer purpose: operational contract, not decorative prose

### 4.1 Minimum operational fields

Arbitrary `purpose: str` is insufficient. A consumer contract must make at least
the following independently inspectable:

1. **Bounded question:** the exact question to which recurrence is relevant.
2. **Consumer and subject:** the responsible consumer identity and the exact
   measured subject; an operator-readable label alone is not consumer uptake.
3. **Permitted reliance:** the precise assertion the consumer may accept, the
   decision (if any) it may constrain, and the stronger conclusions denied.
4. **Required representation:** whether this compiled decoded-string-to-UTF-8
   window projection is acceptable. A need for source bytes must refuse it.
5. **Required scope:** required Evidence/path set, horizon, bounds, completeness
   conditions, and whether same-leaf/cross-leaf occurrences are usable.
6. **Exclusions and STOP:** unavailable material, truncation tolerance,
   Unknown/conflict handling, and conditions requiring refusal rather than a
   count-shaped answer.
7. **Applicability/admission state:** enough evidence for the consumer to report
   applicable, inapplicable, Unknown, conflicting, admitted, or refused rather
   than treating a matching purpose label as admission.

These fields constrain production by validation and constrain reliance by an
explicit consumer-side check. Changing only descriptive wording may change the
request/artifact digest, but it must not change recurrence groups. Changing a
required representation or scope changes the applicable measurement definition
or produces refusal.

### 4.2 Same counts, different lawful reliance

Assume two selected leaves yield the same three occurrences of byte window
`2e 2e 2e` under the same P/E/S.

* **Consumer A — bounded export-truncation-marker examiner.** Its question is
  whether the compiled UTF-8 representation of the selected export fields
  contains the exact marker bytes within the complete export-field set. If the
  selection is proven complete and untruncated, it may rely on the three
  addressed occurrences solely to identify fields for a subsequent bounded
  inspection. It may not infer that source records were truncated.
* **Consumer B — source-acquisition independence examiner.** It asks whether two
  source observations were independently acquired. It must refuse reliance:
  identical payload bytes contain no acquisition episode, producer independence,
  source-byte provenance, or causation evidence. The count remains three; lawful
  reliance is none.
* **Consumer C — one selected field's delimiter-density examiner.** It accepts
  only occurrences in one named Evidence/path and excludes cross-leaf matches.
  It may rely on the within-leaf subset if that path and limit are satisfied,
  while refusing the other two occurrences. Its count input is identical to A's,
  but the portion admitted to its assertion differs.

Purpose prose does not create these outcomes. Required representation, scope,
applicability evidence, permitted reliance, and refusal rules do.

### 4.3 Present implementation finding

PR 2014 did not identify an active consumer that supplies and enforces this
contract for generic Evidence recurrence. Therefore **C cannot yet be truthfully
implemented as operational consumer purpose for this slice**. A producer can
validate a contract-shaped request, but that proves only request formation; it
does not prove consumer applicability, admission, uptake, or reliance. This is
the decisive reason not to implement even the narrow instrument yet. The
contract should be implemented only with the first evidenced consumer, locally,
rather than standardized speculatively.

## 5. Truthful identity topology

| Identity | Meaning | Content-derived? | Required coordinates |
| --- | --- | --- | --- |
| Measurement definition identity | One exact compiled method and parameterization. | **Yes**, from an explicit instrument name/version, UTF-8 policy, overlapping/offset convention, exact equality, width, bounds semantics, selector semantics, and output convention. Source-code commit may be disclosed but is not a substitute for method version. | Must change when measurement semantics change. It need not include selected Evidence or consumer prose. |
| Measurement content identity | Equivalence of the bounded measurement assertion/result content. | **Yes**, from definition id, projection horizon, selected Evidence/path identities, limits, exclusions/loss, retained window bytes/coordinates, and counts under a canonical serialization. If the envelope includes C, use a separate request/artifact id so purpose changes do not falsely imply changed measured content. | Identifies equivalent result content, not production. |
| Producer occurrence identity | This invocation of the producer. | **No.** A digest of equal inputs/results collapses repeats. | A fresh invocation id or caller-supplied unique occurrence coordinate, created even for a pure function call and returned transiently. No durability is implied. |
| Projection horizon | The State boundary from which selected Evidence was read. | May be included in a content digest, but is not reducible to payload content. | At least workspace, projection version, and `last_event_id`/equivalent as-of coordinate; if absent, disclose Unknown rather than claim current completeness. |
| Inspected Evidence identities | The actual Evidence records and expanded leaf paths examined. | Evidence ids are upstream identities; a canonical set digest may summarize but not replace the returned members. | Preserve ordered ids, paths, and enough leaf-value/content binding to detect mismatch; do not equate equal leaf content with equal Evidence occurrence. |
| Inspection time | When this occurrence inspected the supplied projection. | **No.** | A fresh observed/inspection timestamp tied to producer occurrence, with clock semantics disclosed. It is not source occurrence time or ledger time. |
| Repeated execution relation | Two or more producer occurrences use the same definition and perhaps equal content. | The equality relation can compare content-derived ids; membership cannot be reconstructed from one digest. | Preserve each occurrence id separately in the caller-held returned artifacts. Ordering/episode claims require additional evidenced coordinates and are otherwise Unknown. |

An implementation must permit:

```text
occurrence O1 --uses--> definition D --produces--> content M
occurrence O2 --uses--> definition D --produces--> content M
O1 != O2
```

`M` may be identical without collapsing `O1` and `O2`. The returned object can
carry `producer_occurrence_id` and `inspected_at` without recording either.
Caller retention can demonstrate two returned measurement occurrences if both
artifacts retain distinct ids; it still does not prove a complete episode,
durable history, execution order, or repository currentness.

## 6. Eight-dimensional cross-examination

The dimensions below are orientation, not a new universal schema.

| Dimension | Corrected specimen | Missing boundary / refusal |
| --- | --- | --- |
| **Identity** | Separates definition D, content M, producer occurrence O, upstream Evidence ids, leaf paths, and byte-window coordinates. | A single stable measurement id fails by collapsing definition, content, request purpose, and occurrence. Free-text labels cannot repair this. |
| **Evidence / provenance** | Retains State horizon, Evidence ids, payload paths, decoded leaf binding, compiled method/version, created UTF-8 bytes/windows, exclusions, and known loss. | It lacks original source bytes, source decoding history, producer-event linkage intrinsic to Evidence, acquisition independence, and arbitrary binary substrate. Re-encoding is not provenance recovery. |
| **Scope / locality** | Explicit workspace/projection horizon, finite Evidence/path expansion, width, limits, and coordinate bounds. | No implicit all-workspace, corpus-complete, cross-workspace, source-complete, or future scope. Boundary prose without expanded members is insufficient. |
| **Applicability** | A named consumer evaluates whether exact P/E/S satisfies its bounded question and can return applicable, inapplicable, Unknown, conflicting, or refused. | Nonempty purpose text, matching vocabulary, or available recurrence does not prove applicability, admission, consumption, or reliance. No active applicable consumer was found. |
| **Grammar / representation** | Developer-compiled decoded-string -> UTF-8 -> overlapping width-`w` windows, exact byte equality, and explicit offset convention. | No source-byte recovery, normalization, parsing, tokenization, domain signature, caller code, learned representation, arbitrary codec, or semantic equivalence. |
| **Constraints** | Positive width, finite ids/paths/bounds, exact types, canonical ordering, explicit truncation/exclusion, no mutation/recording, and operational C refusal rules. | A boundary note is not enforcement. Invalid paths, missing horizons, unmet completeness, unsupported representations, and excessive limits must refuse rather than silently narrow. |
| **Authority** | Producer authority extends only to the bounded exact recurrence assertion its method directly establishes. Consumer authority, if any, is separate and purpose-local. | Caller selection and purpose prose confer no authority to establish significance, source truth, independence, explanation, verification, currentness, or standing. |
| **Currentness / occurrence** | Every call has a distinct returned occurrence id and inspection time tied to an explicit State horizon; upstream `observed_at` remains source-relative testimony. | Content hashes do not prove invocation, present applicability, latest State, completeness, order, or durability. Repeated identical calls remain distinct and may both be transient. |

No `limitations` paragraph, arbitrary declaration, `measurement_only` label, or
`read_only=true` flag substitutes for one of these missing dimensions. Such
fields are useful disclosures only when the producer actually enforces or
preserves the boundary they name.

## 7. Smallest corrected implementation-ready slice

**Current decision: no implementation is warranted.** The repository supports
the mechanical possibility of a local exact-byte-window producer, but supplies
no named consumer with operational C and no evidence for a general owner. The
smallest corrected next slice is therefore not code; it is one consumer-local
implementation precondition:

```text
identify one active consumer and bounded question
  -> prove it accepts the compiled UTF-8/window representation
  -> specify required Evidence/path/horizon scope and exclusions
  -> specify permitted reliance and enforceable refusal conditions
  -> only then implement the pure producer beside that consumer
```

If that precondition is later met, the implementation-ready code slice is only:

1. one pure, local producer for explicitly addressed existing string leaves;
2. one versioned compiled UTF-8/overlapping-window/exact-equality definition;
3. finite scope and projection-horizon validation;
4. separate definition, measured-content, request/artifact, and fresh producer
   occurrence identities;
5. returned inspection time, every addressed match, exclusions, Unknowns, and
   known loss;
6. one structured C contract enforced for that named consumer; and
7. direct unit tests for method, identity separation, scope refusal, and the
   consumer's different reliance/refusal outcomes.

It remains local to exact-byte recurrence. It is not a base PESC type, generic
Evidence examiner, registry, plugin surface, projection language, diagnostic,
or record. No CLI, event, persistence, or mutation boundary is needed.

## 8. Explicit STOP conditions

Stop before implementation unless all of these are evidenced: one active named
consumer, one bounded question, accepted representation, exact scope/horizon,
permitted reliance, applicability/refusal states, and testable STOP behavior.

Once implemented locally, refuse a request when:

* it asks for original/source bytes from an already-decoded Evidence string;
* Evidence ids, expanded leaf paths, State horizon, width, bounds, or occurrence
  coordinates are missing, implicit, duplicate where forbidden, or unbounded;
* a selected value is not a string, or arbitrary object stringification would
  be required;
* required source completeness, path completeness, or currentness is absent or
  Unknown and the consumer does not permit that Unknown;
* truncation or exclusion cannot be disclosed or violates C;
* P requires caller code, an unregistered arbitrary representation, Unicode
  normalization, character/grapheme comparison, regex, parsing, tokenization,
  file-format knowledge, signature tables, semantic similarity, or binary
  decoding;
* E requires anything other than exact equality of retained projected bytes;
* the caller uses nonempty purpose prose as applicability, admission, authority,
  uptake, or reliance evidence;
* definition/content identity would be used as producer occurrence identity, or
  repeated equal executions would be deduplicated as one occurrence;
* a count is requested as proof of source independence, object equivalence,
  materiality, explanation, causal relation, transformation, verification,
  competency, authority, currentness, or consumer uptake;
* the result would form a candidate, prediction, acquisition request, induction,
  Fidelity finding, promotion, standing change, action, or cluster mutation;
* satisfying the request requires a CLI, diagnostic inventory entry, shape
  audit, event, ledger write, record scope, persistence, or durability; or
* the local consumer requirement is being generalized into a universal PESC
  owner, request schema, registry, or grammar without new repository evidence.

A refusal is more truthful than a count whose shape invites unlawful reliance.
No count, including zero or a large recurrence, crosses these STOPs.

## 9. Files inspected and LOC

Current repository files inspected directly:

* `AGENTS.md`
* `evidence_born_competency_probe_pesc_fidelity_recovery_001.md`
* `evidence_born_competency_probe_frontier_fidelity_recovery_001.md`
* `external_material_representation_metrology_fidelity_recovery_001.md`
* `seed_runtime/evidence.py`
* `seed_runtime/models.py`
* `seed_runtime/observations.py`
* `seed_runtime/state.py`
* `seed_runtime/events.py`
* `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
* `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`
* `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`
* `book_of_seed/operational_measurement_baseline_and_preservation_amendment_001.md`
* `book_of_seed/operational_measurement_responsibility_topology_correction_001.md`
* the commit and parent diff for `f411d26` (PR 2014)

**Report LOC added: 330 lines. Production LOC added: 0. Test LOC added: 0.**

## 10. Final answer to the governing question

Exact-byte recurrence is **not** the first implementation of a general evidence
PESC owner. The current proposal is **a specimen proving that a later local
owner is mechanically possible**. With an evidenced, operational consumer C,
it may become **one compiled PESC measurement instrument** whose P is the
producer's fixed decoded-string-to-UTF-8 overlapping-window method and whose
caller chooses only bounded operands and parameters.

The correction is not to make P more generic. It is to tell the truth about its
compiled representation, refuse claims about source bytes, keep C separate from
purpose prose, and preserve occurrence coordinates independently of stable
definition and content identities. Since the active consumer is still absent,
the smallest lawful implementation slice today is no implementation at all.
