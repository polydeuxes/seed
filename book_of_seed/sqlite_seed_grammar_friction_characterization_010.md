# SQLite–Seed Grammar Friction Characterization 010

## Repository state examined

Before changing files, the surveyed checkout reported:

```text
git rev-parse HEAD
8df268836db44005baf5869d300e398529a12879

git status --short

sqlite3 --version
3.45.1 2024-01-30 16:01:20 e876e51a0ed5c5b3126f52e532044363a014bc594cfefa87ffb5b82257ccalt1 (64-bit)
```

PR 1753 is present in the surveyed checkout as `8df2688 (HEAD -> work) Add SQLite witness support binding slice 002 (#1753)`.

The required artifacts existed before modification:

- `book_of_seed/sqlite_constitutional_witness_slice_001.md`.
- `book_of_seed/sqlite_constitutional_witness_slice_002.md`.
- `book_of_seed/eye_competency_composition_locality_characterization_009.md`.
- `book_of_seed/realization_independence_audit_008.md`.
- `witnesses/sqlite_constitutional_witness_slice_001/schema.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/fixtures.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/verify.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh`.
- `witnesses/sqlite_constitutional_witness_slice_001/README.md`.

Baseline verification before changing files:

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

## Scope and non-goals

This is a characterization of the current SQLite witness as an actual host-language realization. It is not SQLite Witness Slice 003, not a new constitutional neighborhood, not a Seed-native language design, not a SQLite extension, not occurrence recording, not consumer-uptake recording, not fact establishment, and not a source-independence algorithm.

The audit preserves the completed Slice 001 and Slice 002 resolutions: record existence is not recorded assertion truth; reference presence is not referenced material existence; referenced material existence is not applicable support; applicable support is not factual truth; represented provenance is not verified provenance; multiple support rows are not independent corroboration; relevance, selection, authorization, execution, and required action remain distinct; lawful inactivity is not failure; view enumeration is not broadcast, notification, observation, or awakening; Python realization is not constitutional grammar; SQLite realization is not constitutional grammar.

## Evidence order followed

The current witness files were inspected first: `schema.sql`, `fixtures.sql`, `verify.sql`, and `README.md`. The two SQLite slice reports and their Book clauses were inspected next. Only after SQLite friction was recovered, `realization_independence_audit_008.md` and the smallest relevant Python anchors were used for comparison: events, evidence, facts, observations, fact extraction, examination applicability, authority, and execution witnesses already identified by prior audits.

## Actual SQLite constructs audited

The current witness uses tables, rows, columns, text identifiers, primary keys, nullable columns, `CHECK` constraints, selected foreign keys, intentionally absent foreign keys, `LEFT JOIN`, `CROSS JOIN`, ordinary `JOIN`, `COALESCE`, `CASE`, `LIKE`, views, grouping, `COUNT`, `COUNT(DISTINCT)`, verification by query emptiness or existence, shell-mediated database recreation, and SQLite execution against a disposable database.

No triggers, recursive queries, virtual tables, generated columns, universal enum framework, or transaction semantics were introduced for hypothetical discussion.

## Classification framework used

- **Native fit**: the SQLite mechanism directly expresses a bounded mechanical condition required by this witness, without itself asserting broader constitutional standing.
- **Bounded fit**: the SQLite mechanism expresses a real portion of a constitutional requirement, but only with an explicit boundary.
- **Compensated mismatch**: SQLite collapses distinctions Seed needs, and the witness restores them through explicit status columns, standing reasons, views, refusal rows, separate identities, or forbidden-inference text.
- **Unresolved mismatch**: the current witness cannot honestly express the distinction without unsupported Book grammar or unimplemented responsibility. These are marked `[SQLITE GRAMMAR LIMIT]` or `[MISSING BOOK GRAMMAR]`.
- **Rejected host-language temptation**: a convenient SQLite mechanism would silently create unsupported constitutional meaning and is rejected.

## Native fits

| Construct | Native fit | Boundary |
| --- | --- | --- |
| `PRIMARY KEY` on representation rows | Unique row identifiers inside this disposable witness. | Does not establish constitutional subject, occurrence, responsibility, or truth. |
| `CHECK` enumerations for fixed fixture-only fields | Mechanical exclusion of malformed witness values such as impossible truth status or boolean flags. | Rejection is not an attributed constitutional refusal. |
| `COUNT(*)` over deterministic competency/change pairs | Mechanical count of rows projected by the current view. | Count is not activity, notification, observation, or uptake. |
| Verification `assert_zero` table | Mechanical failure if a checked predicate is not satisfied. | Test success is not external fact truth. |

## Bounded fits

| Construct | Portion expressed | Required boundary |
| --- | --- | --- |
| Tables and rows | Preserved fixture representations and relation carriers. | A row is not a constitutional kind by itself. |
| Columns | First-class storage for selected dimensions: authority zone, subject, source identity, confidence label, standing reason. | Column presence does not establish warrant or applicability. |
| Selected foreign keys to Book clauses | Existence of a traceability row. | Book traceability is not proof that the row's semantic claim is true. |
| `LEFT JOIN` from assertions to evidence/provenance | Existence or absence of represented target material. | Matching values are not support, warrant, handoff, or reliance. |
| Views | Deterministic lenses over fixture rows. | View existence and query evaluation are not occurrence or consumer uptake. |

## Compensated mismatches

The witness repeatedly compensates for SQLite's relational compression by adding explicit standing strings and boundaries:

- `assertion_truth_status='not_established'` restores record-exists versus assertion-truth.
- `evidence_standing` restores missing, dangling, unknown, mismatch, and applicable represented support.
- `provenance_standing` restores missing, dangling, conflict, unknown applicability, authority mismatch, represented-not-verified, and verified-for-this-witness-only.
- `lawful_posture` restores lawful inactivity, unknown preservation, and bounded permission.
- `forbidden_inference`, `referential_integrity_boundary`, `independence_boundary`, `producer_occurrence_boundary`, `truth_boundary`, and `universal_activity_boundary` keep row mechanics from becoming fact, authority, action, occurrence, corroboration, or universal activity.
- The README explicitly compensates for `CROSS JOIN` enumeration by denying broadcast, notification, polling, receipt, observation, or awakening.

## Unresolved mismatches

- `[MISSING BOOK GRAMMAR]` A general bounded competency declaration remains only partly named by Book grammar; the witness uses a row with responsibility, authority, evidence/provenance requirements, and stop condition, but the Book has not made that row shape a constitutional type.
- `[SQLITE GRAMMAR LIMIT]` In this witness, view availability does not represent examination occurrence, responsible act recording, consumer receipt, or lawful reliance without additional occurrence and uptake grammar; that is a bounded grammar-pressure finding, not a proof of inherent SQL incapacity.
- `[SQLITE GRAMMAR LIMIT]` `NULL` cannot by itself distinguish unknown, omitted, not applicable, unobserved, withheld, or outside-authority absence.
- `[MISSING BOOK GRAMMAR]` Source independence requires a relation stronger than distinct source identity strings; the current Book supports the negative boundary, not an algorithm for positive independence.

## Rejected host-language temptations

| Temptation | Rejection |
| --- | --- |
| Foreign key as warrant | Referential integrity proves target row existence only. |
| Row count as corroboration | Multiple rows and distinct source strings do not prove independent support. |
| Empty result as lawful absence | No matching row can mean no represented row, filtering, incomplete scope, or fixture omission. |
| View as examination occurrence | A view is a stored query/lens, not an attributed act. |
| Query result as consumer uptake | Reading a result is not recorded reliance or lawful adoption. |
| `CASE` branch order as constitutional sequence | Branch order may select a presentation outcome; it is not constitutional precedence unless supported. |
| `COALESCE` as provenance topology | Evidence-level and assertion-level provenance references may independently matter; first-non-null selection cannot decide their constitutional relation. |
| `CHECK` rejection as refusal | Constraint failure has no represented responsible boundary or refusal reason. |
| One database build as one constitutional act | The harness recreates a disposable database; recording, admission, examination, projection, and verification remain separable claims. |

## Dimensionality inventory

### Recorded assertion standing

Dimensions required: representation identity, assertion identity, assertion family, observable subject, authority zone, producer attribution, evidence reference, provenance reference, assertion text, truth standing, Book traceability, preservation horizon. SQLite carries these mostly as columns on `recorded_change_assertions`; preservation horizon is present in prose and evidence rows rather than directly on the assertion row. Truth standing is compensated by a constrained status value.

First-class: `change_id`, `change_family`, `observable_subject`, `authority_zone`, `producer_attribution`, `evidence_ref`, `provenance_ref`, `assertion_text`, `assertion_truth_status`, `book_clause_id`.

Encoded indirectly or in prose: preservation horizon for the assertion, responsible recording occurrence, consumer reliance.

### Bounded competency declaration

Dimensions required: representation identity, responsibility family, responsibility subject, authority boundary, evidence requirement, provenance requirement, stop condition, Book traceability. SQLite carries these as columns, but the constitutional meaning of a general competency declaration remains partly `[MISSING BOOK GRAMMAR]`.

### Represented evidence material

Dimensions required: evidence identity, evidence kind, source attribution, source identity, source context, responsibility family, observable subject, supported claim, authority zone, preservation horizon, uncertainty/confidence, provenance relation, Book traceability, fact standing boundary. SQLite carries most dimensions as columns. Fact standing is absent except through forbidden-inference guardrails. Source identity is a string, not an independence relation.

### Represented provenance material

Dimensions required: provenance identity, source attribution, source context, assertion applicability, evidence applicability, authority zone, represented-lineage status, verification status, producer-occurrence status, Book traceability. SQLite carries these as columns. Producer occurrence is fixed to `not_established`; verified causation is not represented.

### Competency/change examination

Dimensions required: competency identity, change identity, relevance, evidence standing, provenance standing, lawful posture, standing reason, forbidden inference, truth boundary. SQLite carries these through views and status strings. Occurrence of examination and uptake by a consumer are not represented.

## NULL findings

`recorded_change_assertions.change_family` can be `NULL` to represent insufficient subject/family binding, producing `unknown_preserved`. `recorded_change_assertions.evidence_ref` can be `NULL` to represent a missing required evidence reference. `recorded_change_assertions.provenance_ref` can be `NULL`, but provenance may still be supplied by evidence-level provenance; `COALESCE` formerly risked making that topology implicit.

`represented_evidence_material.responsibility_family`, `observable_subject`, and `supported_change_id` can be `NULL` to represent unknown subject or claim binding. `authority_zone` and `source_context` can be `NULL` to represent unknown authority or source context. `represented_provenance_material.applies_to_change_id` and `applies_to_evidence_id` can both be `NULL` to represent unknown applicability; `authority_zone` can be `NULL` to represent unknown authority binding; `source_context` is nullable but not currently exercised as a standing distinction.

SQLite `NULL` remains storage-level absence/unknown. Seed unknown is only recovered when surrounding SQL names a bounded standing reason. The witness does not attempt a universal absence taxonomy.

## COALESCE and provenance-precedence findings

The prior view used `COALESCE(e.provenance_ref, r.provenance_ref)` as the effective provenance reference and joined provenance material through that selected reference. Mechanically, SQLite selects the evidence-level reference if present and otherwise the assertion-level reference. Constitutionally, that did not prove evidence provenance overrides assertion provenance, that evidence provenance is more local, that the references are alternatives, that the two must agree, or that disagreement is harmless.

The audit found this was a compensated mismatch with an under-specified compensation. Evidence occurrence and assertion occurrence may require separate provenance topology, but the current witness is not implementing that topology. The smallest correction was to preserve an explicit `conflicting_provenance_references_preserved` standing when assertion-level and evidence-level provenance references are both present and disagree. The view still exposes `effective_provenance_ref` for the current bounded join, but disagreement now blocks bounded permission and preserves unknown rather than allowing `COALESCE` to silently decide constitutional precedence.

Focused verification was added with `case_q_conflicting_provenance_refs`: assertion provenance `prov:q-assertion` and evidence provenance `prov:q-evidence` both exist and disagree. Host behavior demonstrated: `COALESCE` still mechanically selects the evidence-level string. Seed distinction protected: disagreement is preserved as provenance conflict. Stronger inference forbidden: selected effective reference is not constitutional topology, verified lineage, or permission.

## CASE ordering and overlap findings

Meaningful `CASE` expressions occur in `support_binding_examination`, `competency_change_examination`, `recorded_assertion_truth_boundary`, and `competency_activity_summary`.

`support_binding_examination.evidence_standing` chooses one evidence standing. Missing reference wins before dangling target; dangling target wins before subject/claim unknown; subject/claim unknown wins before subject mismatch; authority unknown wins before authority mismatch; source-context unknown wins before applicable support. This is witness-local decisive posture selection, not a proof that only one condition exists. It can hide overlapping problems, such as a subject mismatch plus missing source context.

`support_binding_examination.provenance_standing` now preserves conflicting assertion/evidence provenance references before target-row lookup can treat one selected row as decisive. Other ordering remains bounded: missing reference, dangling reference, internally conflicting lineage, unknown applicability, applicability mismatch, unknown authority, authority mismatch, not independently verified, independently verified.

`competency_change_examination.lawful_posture` selects one lawful posture. Relevance unknown or irrelevance and assertion-level authority block occur before support standings. This is supported as a bounded movement guard, but not as a universal constitutional sequence. Several contributing reasons can coexist; the current witness preserves only one decisive posture and one standing reason. That is adequate for this slice because it does not claim exhaustive diagnostics.

## String-shaped standing findings

The witness currently uses `LIKE 'unknown_%'` and `LIKE '%mismatch'` in `competency_change_examination`. This means family membership partly depends on status-string naming. The Book names the distinction between unknown preservation, mismatch/lawful inactivity, and bounded permission, but it does not define a general enum table for standing families.

Classification: compensated mismatch. Adequacy: bounded but fragile. A new status could be misclassified by naming or fail to be classified if wording changes. This pass did not build a universal enum system because current tests exercise the existing strings and only the provenance-reference disagreement required correction. Future falsification question: can a renamed standing retain Book meaning without changing posture? If not, the witness may need an explicit local standing-family column or mapping.

## View / occurrence / uptake findings

| View | Current role | Occurrence boundary |
| --- | --- | --- |
| `support_binding_examination` | Examination method/lens and result representation for evidence/provenance support standing. | View existence and query evaluation do not record an examination act or consumer reliance. |
| `competency_change_examination` | Lens producing lawful posture and standing reason for competency/change pairs. | A calculated pair is not notification, awakening, selection, execution, or uptake. |
| `support_forbidden_inference_audit` | Audit view collecting forbidden inference boundaries. | Audit availability is not itself an audit occurrence unless recorded elsewhere. |
| `support_source_independence_boundary` | Boundary view over row counts and distinct source strings. | Count availability is not corroboration or reliance. |
| `recorded_assertion_truth_boundary` | Boundary view over record existence and truth status. | Projection does not establish external truth. |
| `competency_activity_summary` | Summary view proving no universal activity implied by bounded permission counts. | Summary is not broadcast, observation, or universal activity. |

Evidence required to claim occurrence or uptake would include an attributed responsible examination record, consumer identity or scope, result observed, reliance or refusal standing, authority for that reliance, and preservation horizon. None is implemented here.

## Query-truth findings

SQL mechanically proves predicates over current rows: expected posture rows exist; truth status remains `not_established`; unrelated records produce zero bounded permissions; dangling references remain explicit; represented provenance not verified remains not verified; same-source rows count as two rows and one distinct source identity; conflicting provenance references are preserved.

The constitutional assertion is limited to the witness's represented standing over fixture rows. Stronger inferences remain forbidden: external truth, complete truth, current lawful state, execution authorization, producer occurrence, verified provenance, independent corroboration, and consumer reliance.

## Empty-result findings

Verification uses absence of failures in `assert_zero` and `LEFT JOIN ... WHERE a.change_id IS NULL` to detect missing expected rows. That emptiness means no counterexample was found inside the disposable fixture scope. It does not mean lawfully none, no possible evidence, complete scope, external absence, or a negative fact. The witness does not add closed-world semantics.

## CHECK / refusal findings

`CHECK` constraints restrict `assertion_truth_status`, evidence/provenance verification status, represented-lineage status, producer-occurrence status, and boolean requirement flags. They mechanically reject malformed witness representations. They do not attribute a responsible refusal boundary, preserve an independent refusal reason, or decide another lawful posture. Mechanical rejection remains useful because the witness is deterministic, but schema rejection is not complete constitutional refusal.

## Foreign-key / warrant findings

Foreign keys are used for `book_clause_id` references to `book_clause_sources`. They establish that each represented fixture row points to an existing traceability row. They do not establish that the clause supports the row correctly, that the row is true, or that constitutional warrant exists.

Foreign keys are intentionally absent for `recorded_change_assertions.evidence_ref`, `recorded_change_assertions.provenance_ref`, and `represented_evidence_material.provenance_ref`. This allows dangling-reference cases and preserves the distinction between reference presence, target existence, applicability, warrant, and truth.

## Identity-compression findings

| Identifier | Current dimension carried | Compression risk |
| --- | --- | --- |
| `change_id` | Assertion/record representation identity and join key for supported claim. | Can be mistaken for occurrence identity or truth identity. |
| `competency_id` | Fixture competency-row identity. | Can be mistaken for constitutional actor identity or Eye identity. |
| `evidence_id` | Evidence representation identity and support-reference target. | Can be mistaken for support warrant or fact identity. |
| `provenance_id` | Provenance representation identity and lineage-reference target. | Can be mistaken for verified producer occurrence. |
| `source_identity` | Represented source identity string. | Can be mistaken for independent source relation. |
| `book_clause_id` / `clause_id` | Traceability-row identity. | Can be mistaken for proof of clause applicability. |
| `authority_zone` | Represented authority boundary. | Can be mistaken for granted authority or execution authorization. |

The current witness ties assertion identity and supported claim identity through `change_id`; this is adequate for the slice but would be lossy for a future grammar where one recorded assertion mentions multiple claims or one claim is represented by multiple assertion occurrences.

## Counting / source-independence findings

`COUNT(e.evidence_id)` proves only how many represented evidence rows join to the change. `COUNT(DISTINCT e.source_identity)` proves only how many distinct source-identity strings appear among joined evidence rows. The witness correctly preserves that two rows from one source identity are not independent corroboration.

To establish positive independence, a future witness would need a constitutional relation for source responsibility, collection independence, causal independence, authority to rely on independence, and conflict handling. That is intentionally not implemented.

## Join / road findings

`LEFT JOIN` and ordinary `JOIN` are realization mechanics for matching represented identifiers. `CROSS JOIN` enumerates deterministic pairs. No SQL join is a constitutional road, handoff, admission, communication, or uptake. The support-binding view uses joins to compute support standing, but the constitutional support is the named standing after evidence/provenance/subject/authority checks, not the join itself.

## Transaction / act findings

The harness recreates a disposable SQLite database and executes schema, fixtures, and verification scripts. The current witness does not rely on explicit transaction semantics. Even if SQLite executes statements atomically, one database build is not one constitutional act. Recording, admission, examination, projection, verification, and reporting remain constitutionally separable.

## SQLite friction register

| SQLite construct | Current witness use | Native SQLite meaning | Seed distinction required | Dimension collapsed or omitted | Classification | Compensation currently used | Compensation adequacy | Book clause | Python analogue | Stronger inference forbidden | Future falsification question |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Table/row | Fixture representation storage | Relation with tuples | Record, evidence, provenance, competency standing | Constitutional subject, occurrence | Bounded fit | Explicit status columns and Book traceability | Adequate for fixture | 05.Recording.A, 05.Evidence.A | Dataclass/model instance | Row/object is not truth or act | Can a row be copied without preserving standing? |
| Primary key | Unique ids | Unique non-null key | Representation identity | Subject/occurrence/responsibility identity | Native fit | Naming and prose boundaries | Adequate | 05.Recording.A | Python object id / stable id | Unique id is not warrant | Does any key carry multiple claims? |
| Nullable columns | Missing/unknown fixture fields | NULL value | Differentiated absence | Unknown, missing, unbound, not applicable | Compensated mismatch | CASE standing reasons | Partial | 04.Examination.B | Python `None` | NULL is not Seed unknown by itself | Does a new NULL use have a reason? |
| CHECK | Value constraints | Reject invalid row | Bounded fixture vocabulary | Responsible refusal | Native/bounded fit | Narrow enums only | Adequate | 05.Recording.A | Constructor validation / exception | Constraint failure is not refusal | Does rejection need attribution? |
| Absent FK for evidence/provenance refs | Allows dangling refs | No referential enforcement | Reference vs existence | Warrant/applicability | Compensated mismatch | LEFT JOIN standings | Adequate | 05.Evidence.A/B | In-process reference or string id | Reference is not support | Would FK hide a needed dangling case? |
| FK to Book rows | Clause traceability | Target exists | Source citation | Clause applicability | Bounded fit | `book_clause_sources` row | Partial | all cited clauses | Module/path reference | Citation is not law application | Does cited clause actually support row? |
| LEFT JOIN | Evidence/provenance target lookup | Matched or unmatched rows | Existence vs missing/dangling | Support/warrant/uptake | Bounded fit | Standing CASE | Adequate | 05.Evidence.A/B | Object reference lookup | Match is not warrant | Are joins treated as handoffs? |
| CROSS JOIN | All competency/change pairs | Cartesian product | Deterministic enumeration | Broadcast/notification/observation | Compensated mismatch | README and summary boundary | Adequate | 04.Examination.A/B | Loop/call graph | Pair is not awakening | Does a consumer treat pairs as notices? |
| COALESCE | Effective provenance ref | First non-null expression | Provenance topology | Separate assertion/evidence provenance | Compensated mismatch | New conflict standing | Adequate for current slice | 05.Evidence.B | Default argument/fallback | Fallback is not constitutional precedence | Must both provenance refs be independently evaluated? |
| CASE | Standing selection | First true branch | Decisive posture plus reasons | Coexisting reasons | Compensated mismatch | Standing reason and focused conflict case | Partial | 04.Examination.B | if/elif / exception order | Branch order is not law order | Do overlapping failures need multi-reason output? |
| LIKE | Standing-family classification | Pattern matching text | Unknown/mismatch families | Explicit standing type | Compensated mismatch | Naming discipline | Fragile but bounded | 04.Examination.B | String exception codes | Prefix is not type law | Can wording change safely? |
| View | Semantic projections | Stored SELECT | Examination/audit lens | Occurrence and uptake | Compensated mismatch | Boundary strings and README | Adequate | 04.Examination.A, 05.Evidence.A | Method/property return | View is not act | Is any audit result recorded as occurrence? |
| COUNT / COUNT DISTINCT | Support row/source-string counts | Aggregate cardinality | Independence boundary | Corroboration/warrant | Compensated mismatch | `independence_boundary` | Adequate negative guardrail | 05.Evidence.A/B | list length / set length | Count is not independence | What relation would prove independence? |
| Query emptiness | Verification pass/fail | No row matched | Absence standing | Closed-world negative fact | Bounded fit | Fixture-scope tests only | Adequate | 05.Recording.B | Empty list / falsey result | Empty is not lawful absence | Does a test imply no possible cases? |
| SQLite database build | Harness execution | Statements against DB file | Acts and preservation | Responsible act composition | Rejected temptation | No transaction semantics claimed | Adequate | 07 realization audit | Batch function call | Build is not one constitutional act | Would transaction logs be overread? |

## Cross-language convergence matrix

| Constitutional dimension | Python compression mechanism | SQLite compression mechanism | Python compensation | SQLite compensation | Book clause | Shared host-language deficit? | Candidate Seed-native dimension | Remaining uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Representation identity | Object/model identity, stable id field | Row primary key/text id | Stable identifiers plus producer-boundary warnings | Primary keys plus forbidden inference | 05.Recording.A | Yes | representation identity | How identity travels across copies. |
| Constitutional subject | Class/type/module name | Table name/row shape | Book-audit demotion of classes as kinds | Prose: no table is a kind | 04/05 clauses | Yes | subject binding | General competency subject remains incomplete. |
| Assertion truth standing | Return/event payload may look true | Inserted row may look true | Fact extraction separation | `assertion_truth_status` and truth view | 05.Recording.A | Yes | assertion standing | Positive truth establishment not in this witness. |
| Source attribution | Payload/source fields | `source_attribution`, `source_identity` strings | Provenance not occurrence seal | Provenance standing and source-independence boundary | 05.Evidence.B | Yes | source attribution/provenance | Positive independent-source warrant unresolved. |
| Responsibility/authority | Function/method boundary, policy gate | Competency row and authority zone column | Responsible validated production boundary | Authority-zone matching and blocked posture | 04.Examination.A, authority scope | Yes | responsibility and authority boundary | General non-Python act grammar remains broad. |
| Unknown reason | `None`, missing field, exception path | `NULL` | Explicit result/refusal standing where implemented | CASE outcomes with unknown standings | 04.Examination.B | Yes | unknown-with-reason | No universal unknown taxonomy. |
| Refusal/non-performance | Exception/failed return | CHECK failure or lawful inactivity status | Execution/refusal records | Lawful posture strings; CHECK not refusal | refusal chapter, 04.Examination.B | Yes | refusal/non-performance reason | Schema rejection attribution absent. |
| Occurrence | Method call/return context | View evaluation/query result | Witnessed occurrence vs preserved evidence | View/occurrence/uptake boundary | realization audit 008 | Yes | occurrence evidence | No occurrence recording in SQLite witness. |
| Handoff/road | Call graph/reference passing | JOIN topology | Communication/handoff distinctions | Join/road boundary | communication and handoff; 05.Evidence.B | Yes | warranted relation/road | No handoff witness here. |
| Preservation | In-memory ledger, SQLite ledger | DB file rows | Preservation horizon audit | Disposable witness boundary and rows | 05.Recording.A/B | Partly | preservation horizon | Multi-party durability taxonomy unresolved. |

## Candidate Seed-native dimensions

Evidence-backed repeated pressure suggests candidate first-class dimensions, not a language design:

- candidate first-class dimension: representation identity distinct from constitutional subject and occurrence identity;
- candidate first-class dimension: assertion standing distinct from record existence;
- candidate first-class dimension: responsibility and authority boundary distinct from object owner, table owner, or function caller;
- candidate first-class dimension: unknown/refusal reason with bounded standing, distinct from `None`, `NULL`, exception, or empty result;
- candidate first-class dimension: provenance representation, applicability, verification, and producer occurrence as separate standings;
- candidate constitutional operator: bounded examination that produces posture without selection, execution, mutation, truth, or uptake;
- candidate constitutional operator: source/support binding that distinguishes identifier, material existence, applicability, authority, and warrant;
- unresolved language pressure: occurrence and consumer uptake are repeatedly denied but not represented in this SQLite witness.

These are pressures only. They are not a compiler, parser, virtual machine, SQLite extension, or universal intermediate representation.

## Book pressure discovered

The existing Book names most distinctions needed for this audit: bounded relevance and lawful inactivity, recorded assertion standing, evidence support binding, provenance representation/applicability, authority non-expansion, and realization independence. The main missing grammar remains the general bounded competency declaration, already identified by prior slices. No new Book clause was required because the COALESCE correction could be stated under existing `05.Evidence.B`: provenance representation, applicability, verification, and producer occurrence are separate standings, and a string/citation is not verified provenance.

## Book changes made, if any

No Book clauses outside this characterization report were changed.

## SQLite corrections made, if any

A focused correction was made to `support_binding_examination`: when assertion-level and evidence-level provenance references are both present and disagree, the witness now produces `conflicting_provenance_references_preserved` before provenance lookup can treat `COALESCE` as decisive. `competency_change_examination` now treats that standing as `unknown_preserved`.

## Focused verification added

Added `case_q_conflicting_provenance_refs` to fixtures and verification.

- Host-language behavior demonstrated: `COALESCE` still mechanically selects the evidence-level reference as `effective_provenance_ref`.
- Seed distinction protected: disagreement between assertion-level and evidence-level provenance references is preserved as a provenance conflict.
- Stronger inference forbidden: evidence-level non-nullness does not create constitutional precedence, verified lineage, or bounded permission.

## All verification commands and results

Baseline before changes:

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

After correction:

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
conflicting provenance reference boundary passes
SQLite constitutional witness slice 001 verification passed: /workspace/seed/witnesses/sqlite_constitutional_witness_slice_001/witness.sqlite3
```

## Claims contradicted

- `COALESCE(e.provenance_ref, r.provenance_ref)` is not constitutional proof that evidence-level provenance overrides assertion-level provenance.
- A view-calculated competency/change pair is not broadcast, notification, observation, awakening, examination occurrence, or uptake.
- Distinct source-identity strings are not independent corroboration.
- `NULL` is not Seed unknown unless a bounded standing reason restores that distinction.
- `CASE` branch order is not constitutional sequence by itself.
- SQLite constraint rejection is not an attributed constitutional refusal.

## Claims remaining unresolved

- Whether a future witness should evaluate assertion-level and evidence-level provenance as two independently applicable relations rather than selecting an effective reference.
- Whether standing-family classification should become an explicit local mapping instead of `LIKE` patterns.
- Whether a general bounded competency declaration should become Book grammar.
- How occurrence, consumer receipt, lawful reliance, and handoff identity should be represented if a later slice needs them.
- What positive relation would establish source independence rather than merely rejecting row-count corroboration.

## Files changed

- `book_of_seed/sqlite_seed_grammar_friction_characterization_010.md`.
- `witnesses/sqlite_constitutional_witness_slice_001/schema.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/fixtures.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/verify.sql`.

## Dimensional deficit result

SQLite naturally expresses the relational core of this witness: unique fixture identifiers, rows, columns, joins for represented target lookup, deterministic projections, and aggregate counts. But the current witness demonstrates that SQLite does not naturally own Seed's standing, authority, occurrence, provenance, unknown-reason, refusal-reason, and uptake dimensions. It can realize the current constitution only through repeated compensated mismatches: explicit status strings, standing reasons, forbidden-inference columns, intentionally absent foreign keys, prose boundaries, and focused verification.

The evidence does not show that SQLite cannot implement Seed, and it does not show that a new language is required. It does support a bounded version of the central hypothesis: Python and SQLite independently compress several of the same Seed-native constitutional dimensions, especially representation identity, occurrence, assertion standing, authority/responsibility, provenance, unknown/refusal reason, and consumer reliance. The current witness is also still small, so some observed friction may be incomplete Book grammar rather than a pure SQLite grammar limit.
