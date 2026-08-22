# SQLite Constitutional Witness Slice 002

## Evidence and Provenance Support-Binding Recovery

## Repository state examined

Before changing the witness, the surveyed checkout reported:

```text
git rev-parse HEAD
2409831950f82ba3ac1d516ddd2d693d13084a6f

git status --short

sqlite3 --version
3.45.1 2024-01-30 16:01:20 e876e51a0ed5c5b3126f52e532044363a014bc594cfefa87ffb5b82257ccalt1 (64-bit)
```

PR 1752 is present: `git log --oneline --decorate -n 20` showed `2409831 (HEAD -> work) Add Eye competency locality characterization 009 (#1752)`.

The required files existed before modification:

- `book_of_seed/sqlite_constitutional_witness_slice_001.md`
- `book_of_seed/eye_competency_composition_locality_characterization_009.md`
- `book_of_seed/realization_independence_audit_008.md`
- `witnesses/sqlite_constitutional_witness_slice_001/schema.sql`
- `witnesses/sqlite_constitutional_witness_slice_001/fixtures.sql`
- `witnesses/sqlite_constitutional_witness_slice_001/verify.sql`
- `witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh`
- `witnesses/sqlite_constitutional_witness_slice_001/README.md`

Baseline verification before changing the witness:

```text
./witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh
posture cases pass
record-not-truth case passes
no universal activity case passes
forbidden inference boundary passes
SQLite constitutional witness slice 001 verification passed: /workspace/seed/witnesses/sqlite_constitutional_witness_slice_001/witness.sqlite3
```

## Bounded constitutional question

Given one recorded constitutional-change assertion, one bounded competency declaration, one claimed evidence reference, and one claimed provenance reference, a reference may satisfy the competency's bounded evidence or provenance requirement only after SQL distinguishes reference presence from referenced material existence, applicability to the recorded assertion, subject and responsibility binding, authority binding, source context, represented lineage, verification standing, and forbidden truth or execution inferences.

The strongest positive result remains `bounded_permission_for_further_examination`. The witness does not establish external truth, fact standing, current lawful state, producer occurrence, verified causation, execution authorization, or required action.

## Existing reference-presence audit

| Field | Producer | Names | Target existence before Slice 002 | Binding before Slice 002 | Standing before Slice 002 | Slice 002 classification |
| --- | --- | --- | --- | --- | --- | --- |
| `recorded_change_assertions.evidence_ref` | fixture recorded assertion | claimed evidence identifier | unchecked string | none beyond non-nullness | could satisfy `requires_evidence` by presence | current witness mechanism that was also an unsupported semantic claim |
| `recorded_change_assertions.provenance_ref` | fixture recorded assertion | claimed provenance identifier | unchecked string | none beyond non-nullness | could satisfy `requires_provenance` by presence | current witness mechanism that was also an unsupported semantic claim |
| `bounded_competencies.requires_evidence` | fixture bounded competency | requirement flag | not a target | bound to competency row | constitutional requirement represented as a mechanism | constitutional requirement plus current witness mechanism |
| `bounded_competencies.requires_provenance` | fixture bounded competency | requirement flag | not a target | bound to competency row | constitutional requirement represented as a mechanism | constitutional requirement plus current witness mechanism |

Slice 002 does not preserve reference fields because fixtures already used them. It preserves them as recorded claims whose standing is determined only by `support_binding_examination` and `competency_change_examination`.

## Book sources examined

Initial SQL recovery was oriented from:

- `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`
- `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`
- `book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md`

Stable Slice 001 clauses retained:

- `05.Recording.A` recorded assertion standing.
- `05.Recording.B` diagnostic or examination-scoped recording.
- `04.Examination.A` bounded relevance before movement.
- `04.Examination.B` positive lawful inactivity.

## Python witnesses examined after initial SQL recovery

After forming the relational support-binding model from Book clauses, the following Python witnesses were inspected:

- `seed_runtime/evidence.py` represents `Evidence` with `id`, `workspace_id`, `source`, `kind`, `observed_at`, `payload`, and `confidence`.
- `seed_runtime/observations.py` turns observations into evidence events and optional facts while preserving observation metadata.
- `seed_runtime/facts.py` keeps `Fact.evidence_ids`, `FactSupport`, confidence, and source types distinct from event records.
- `seed_runtime/fact_extraction.py` records successful tool output as evidence only and intentionally does not infer facts without an explicit mapping.
- `seed_runtime/events.py` contains in-memory and SQLite event ledgers for event recording, not constitutional proof of truth.

No Python model identity or constructor was translated into SQL table identity. The SQL witness uses only the bounded relations required for this slice.

## Evidence support-binding characterization

The smallest recovered relation is represented by `represented_evidence_material` plus the `support_binding_examination` view. Evidence support for this bounded witness requires:

- the cited evidence identifier is present when evidence is required;
- referenced evidence material exists;
- the material represents evidence kind, source attribution, source identity, source context, responsibility family, observable subject, supported change, authority zone, preservation horizon, confidence/uncertainty label, and provenance reference where present;
- represented responsibility family, subject, supported claim, authority zone, and source context are applicable to the assertion and competency;
- the result remains applicable represented support, not fact standing.

Confidence is represented but does not grant warrant automatically. Multiple rows can be inspected, but row count is not independent corroboration.

## Provenance support-binding characterization

`represented_provenance_material` distinguishes:

- provenance identifier present;
- referenced provenance material exists;
- lineage/source is represented;
- lineage is applicable to the assertion or evidence;
- lineage may be internally conflicting;
- lineage may be represented without independent verification;
- independent verification, verified causation, and producer occurrence remain separate and are not produced by this witness.

A complete represented chain may satisfy a bounded represented-lineage requirement, as in Case N, while `producer_occurrence_status` remains `not_established` and the forbidden inference remains active.

## Subject and authority binding result

Evidence does not satisfy a competency merely because it exists. SQL checks responsibility family, observable subject, supported change identity, evidence authority zone, provenance applicability, and provenance authority zone. Unknown values preserve `unknown_preserved`; explicit mismatches become `lawful_inactivity_support_mismatch`; assertion-level authority mismatch remains `lawful_inactivity_authority_blocked`.

## Missing, dangling, unknown, mismatch, and conflict distinctions

The witness now distinguishes:

- missing evidence reference: required evidence reference absent;
- dangling evidence reference: non-null evidence reference names no represented evidence row;
- missing provenance reference: required provenance reference absent;
- dangling provenance reference: effective provenance reference names no represented provenance row;
- unknown evidence subject or claim binding: evidence exists but lacks enough represented identity;
- evidence or provenance mismatch: represented material explicitly binds elsewhere;
- authority mismatch: represented support lies outside the competency authority boundary;
- conflicting provenance: lineage exists but is internally conflicting;
- represented but not verified provenance: lineage may support represented-lineage examination without verified-causation standing.

## Relations and projections implemented

New semantic SQL objects:

- `represented_evidence_material`
- `represented_provenance_material`
- `support_binding_examination`
- `support_forbidden_inference_audit`
- `support_source_independence_boundary`

Updated SQL objects:

- `competency_change_examination`
- `book_clause_sources` fixtures
- Slice 001/002 verification assertions

## Book clauses split

Directly required Book clause splits:

- `05.Evidence.A — Evidence support binding`
- `05.Evidence.B — Provenance representation and applicability`
- `05.Testimony.A — Premise-relative testimony without fact standing`

These clauses allow SQLite and Python witnesses to cite evidence identity, support applicability, represented provenance, and testimony/fact boundaries without importing a universal fact-establishment or explanation-construction chapter.

## Book clauses retained together

The chapters were not generally rewritten. Existing `05.Recording.A`, `05.Recording.B`, `04.Examination.A`, `04.Examination.B`, authority scope, and refusal/non-performance material remained stable because this slice needed them as intact human-readable orientation rather than smaller micro-files.

## Book-to-SQL traceability updates

| SQL object | Responsibility | Book/current source | Python witness, if any | Standing produced | Support consumed | Hidden Python assumption avoided | SQLite mechanism | Forbidden inference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `represented_evidence_material` | represent support material identity | `05.Evidence.A` | `Evidence`, `Observation`, `Fact.evidence_ids` | evidence-shaped material exists as represented material | recorded evidence reference | no Python constructor or class identity becomes law | table with nullable applicability fields | row existence is not admission, truth, or warrant |
| `represented_provenance_material` | represent lineage and verification distinctions | `05.Evidence.B` | event causation/correlation fields; evidence source fields | represented provenance material exists | assertion or evidence provenance reference | no event ID or causation ID becomes producer occurrence proof | table with verification and occurrence statuses | provenance string or row is not verified causation |
| `support_binding_examination` | decide support existence/applicability/unknown/mismatch | `04.Examination.A`, `04.Examination.B`, `05.Evidence.A`, `05.Evidence.B` | no direct translation | support standing reasons | assertion, competency, evidence, provenance rows | no object graph traversal assumed | SQL joins and CASE expressions | support for examination is not truth/execution/current state |
| `support_forbidden_inference_audit` | expose guardrails | `05.Testimony.A`, `05.Evidence.B` | `FactExtractionService` evidence-only boundary | explicit non-promotion record | support-binding result | no evidence event is a fact event | view | represented support is not established fact |
| `support_source_independence_boundary` | prevent accidental corroboration by row count | `05.Testimony.A`, `05.Evidence.A` | `FactSupport` distinguishes support from facts | source-count boundary | evidence rows and source identities | no aggregate support algorithm imported | grouped view | multiple rows are not independent corroboration |

No new SQL object silently encodes missing constitutional law. No `[MISSING BOOK GRAMMAR]` entry remains necessary for this bounded slice after the three clause splits above.

## Hidden Python assumptions avoided

- `Evidence.id` is not treated as evidence standing.
- `Evidence.source` is not treated as verified producer occurrence.
- `Fact.evidence_ids` is not treated as fact establishment.
- Event ledger causation/correlation IDs are not treated as verified causation.
- `FactExtractionService` evidence output is not treated as automatic fact inference.
- `SQLiteEventLedger` persistence is not treated as a constitutional dependency for this witness.

## SQLite-specific mechanisms used

SQLite owns support binding through tables and views. The shell harness only recreates the database and invokes SQL verification. The witness uses `LEFT JOIN` to preserve dangling references and CASE expressions to classify missing, dangling, unknown, mismatch, represented, verified, and forbidden-inference outcomes.

## Referential-integrity non-dependency guardrail

The witness uses a foreign key only for `book_clause_id`, where fixtures must cite a known clause source. It intentionally does not use foreign keys for `evidence_ref` or `provenance_ref`, because dangling-reference cases are constitutional evidence for this slice. Even if a future implementation uses foreign keys for mechanical correctness, that condition can only prove target row existence; it cannot prove applicability, represented lineage coherence, independent verification, producer occurrence, truth, or warrant.

## Verification cases added

- Case H: bound evidence and provenance produces `bounded_permission_for_further_examination`.
- Case I: non-null evidence reference with no evidence row produces `lawful_inactivity_dangling_evidence` and `dangling_evidence_reference`.
- Case J: non-null provenance reference with no provenance row produces `lawful_inactivity_dangling_provenance` and `dangling_provenance_reference`.
- Case K: evidence for another subject produces `lawful_inactivity_support_mismatch`.
- Case L: insufficient subject/claim binding preserves `unknown_preserved`.
- Case M: evidence authority mismatch produces `lawful_inactivity_support_mismatch`.
- Case N: represented but not independently verified provenance can permit further examination while preserving non-verification and non-producer-occurrence boundaries.
- Case O: reference names alone produce dangling evidence, not support.
- Case P: two support rows from one represented source do not create independent corroboration or fact standing.

## All verification commands and results

After changes:

```text
./witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh
posture cases pass
record-not-truth case passes
no universal activity case passes
forbidden inference boundary passes
dangling evidence case passes
dangling provenance case passes
unknown binding case passes
represented provenance boundary passes
reference-name-alone case passes
same-source non-corroboration case passes
SQLite constitutional witness slice 001 verification passed: /workspace/seed/witnesses/sqlite_constitutional_witness_slice_001/witness.sqlite3
```

## Comparative falsification

### Hypothesis 1

The Book contained enough grammar to distinguish evidence/provenance from fact standing, but needed smaller clauses for evidence support binding, provenance applicability, and testimony-without-fact standing. Those clauses were recovered.

### Hypothesis 2

A relational realization can express evidence applicability without translating Python model identity. The witness did so with represented support and provenance tables plus SQL views. No hidden constructor assumption was required.

### Hypothesis 3

A non-null reference is insufficient to satisfy an evidence or provenance requirement. Cases I, J, and O preserve that result. Repository consumers examined did not contradict it; Python evidence and events preserve records and payloads but do not make identifiers into standing by themselves.

### Hypothesis 4

Referential integrity may support implementation correctness without becoming constitutional warrant. This witness uses no evidence/provenance foreign keys so dangling references remain observable. The precise boundary is: a foreign key could prove only row existence, not support applicability, provenance verification, truth, or producer occurrence.

### Hypothesis 5

The same recovered Book clauses can orient both Python and SQLite witnesses. Python evidence/fact/event code already preserves distinctions between evidence, fact, and event recording. The SQLite witness is a different but lawful realization; no production Python behavior was changed.

## Claims contradicted

- A non-null `evidence_ref` satisfies `requires_evidence`.
- A non-null `provenance_ref` satisfies `requires_provenance`.
- A provenance row or internally represented lineage proves producer occurrence.
- Multiple rows from one represented source are independent corroboration.
- Bounded permission for further examination establishes truth, state, execution authorization, or required action.

## Claims remaining unresolved

- Universal evidence ontology.
- Universal provenance graph.
- Independent source-corroboration algorithm.
- Fact reconciliation or external truth verification.
- Producer occurrence seals.
- Final policy for when verified provenance is required rather than merely represented lineage.

## Files changed

- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`
- `book_of_seed/sqlite_constitutional_witness_slice_002.md`
- `witnesses/sqlite_constitutional_witness_slice_001/schema.sql`
- `witnesses/sqlite_constitutional_witness_slice_001/fixtures.sql`
- `witnesses/sqlite_constitutional_witness_slice_001/verify.sql`
- `witnesses/sqlite_constitutional_witness_slice_001/README.md`
