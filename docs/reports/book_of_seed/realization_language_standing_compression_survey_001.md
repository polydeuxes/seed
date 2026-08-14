# Realization-language standing-compression survey 001

## Book grammar consumed

This bounded survey consumes `06.Projection.B — Purpose-relative lossless projection and package standing` as its constitutional grammar. The clause requires a projection, view, package, set, or handoff to preserve the distinctions needed by the declared bounded consumer purpose. It especially preserves formation standing, contents, cardinality, availability, completeness, Unknowns, conflicts, refusals, known loss, negative authority, and aggregate judgment as distinct unless a local warranted rule intentionally relates them.

Operational grammar used here:

```text
Book grammar
→ realization-language witness
→ local formation responsibility
→ projected or transported representation
→ local consumer claim
→ faithful compression / lossy crossing / Unknown
```

Negative authority for the whole survey: this document does not claim that every use of truthiness, `None`, SQL `NULL`, no rows, defaults, JSON omission, process output, cache miss, exception handling, or provider silence is defective. It does not prescribe a universal wrapper, package lifecycle, status enum, result object, aggregate abstraction, or repair.

## Survey method and bounds

The survey was bounded to implementation neighborhoods evidenced in `seed_runtime`, `scripts`, and tests. It preferred one or two strong witnesses per realization mechanism and stopped at twelve neighborhoods. It used the Constitutional View Composition empty-input aggregate as a calibration witness only, not as a repair target and not as a license to generalize all `all(...)` calls.

Categories with no strong independent witness in this pass are recorded as not evidenced rather than padded. Distributed/provider-like behavior is represented only where actual HTTP/model or Prometheus-style provider boundaries exist; no distributed architecture is invented.

## Neighborhoods inspected

### 1. Constitutional View Composition compatibility aggregate

- **Local constitutional question:** For an explicitly requested set of registered constitutional read-model views, can the composition answer the compatibility question as `No.` or must it preserve `Unknown.`?
- **Subject/package:** `request.requested_views` and the payloads produced by each registered view builder/JSON renderer.
- **Lawful standing:** populated all-negative compatibility package may support aggregate `No.`; at least one non-`No.` or unavailable answer preserves `Unknown.`; an empty requested package has empty-package standing unless a separate rule makes it a negative aggregate.
- **Formation responsibility:** `build_constitutional_view_composition(...)` forms `compatibility_answers` while iterating requested views, validates unsupported names before the loop, and appends the payload value or default `Unknown.` for each built view.
- **Language operator:** `all(answer == "No." for answer in compatibility_answers)`.
- **Distinct standings entering:** empty requested/formed contribution package; populated package whose every compatibility answer is `No.`.
- **Representation produced:** both become `compatibility_answer="No."` when the list is empty or all-negative.
- **Consumer claim:** the artifact's JSON and human formatter expose `Compatibility answer: No.`; pipeline diagnostics also transport the composition compatibility answer.
- **Distinction preserved elsewhere:** contributing views, preserved unknowns, and requested view material remain available, but the scalar `compatibility_answer` itself does not preserve cardinality or empty-package standing.
- **Fidelity finding:** **lossy constitutional compression** for the scalar compatibility answer. Under the recovered Book grammar, the calibration witness exemplifies empty package standing collapsed into aggregate negative testimony.
- **Negative authority:** this does not establish that every `all(...)` is defective; the selection aggregate below uses an explicit non-empty guard.

### 2. Constitutional View Selection guarded compatibility aggregate

- **Local constitutional question:** Given question projection keys and capability projections, which registered views are deterministically selected and what compatibility standing may be handed to composition?
- **Subject/package:** matched capability projections, selected view names, unsupported keys, and accumulated uncertainty.
- **Lawful standing:** selected populated all-negative matches may support `No.`; no selected match or unsupported keys may preserve uncertainty and `Unknown.`.
- **Formation responsibility:** `select_constitutional_views(...)` builds `selected`, `unsupported_keys`, `uncertainty`, and `compatibility_answers`; it appends a no-match uncertainty when `selected` is empty.
- **Language operator:** `compatibility_answers and all(answer == "No." for answer in compatibility_answers)`.
- **Distinct standings entering:** empty match package and all-negative populated match package are distinguishable because the non-empty list itself gates the aggregate.
- **Representation produced:** empty selection becomes `Unknown.` plus uncertainty; populated all-negative becomes `No.`.
- **Consumer claim:** downstream composition receives requested views and selection uncertainty rather than only the compatibility scalar.
- **Distinction preserved elsewhere:** no-match standing is preserved in `selection_uncertainty` and by `selected_view_names=()`.
- **Fidelity finding:** **faithful because separate standing is preserved elsewhere** and because the aggregate is non-vacuously guarded.
- **Negative authority:** this does not prove all compatibility aggregation is safe; it only shows this local boundary guards the distinction required by its consumer.

### 3. Capability projection `getattr(..., "Unknown.")` fallback

- **Local constitutional question:** When a registered constitutional source view is projected into a capability projection, what compatibility testimony can be transported without giving the projection constitutional authority?
- **Subject/package:** a `ConstitutionalProcessView`, `ConstitutionalGovernanceView`, or `ConstitutionalFidelityView`, or an absent view.
- **Lawful standing:** present view with its own compatibility answer; absent view as `Unknown.`; present object lacking the field as unsupported/Unknown rather than negative testimony.
- **Formation responsibility:** `project_constitutional_capability(...)` explicitly returns `Unknown.` when the view is `None`; for a present view it reads capability keys and uses `getattr(view, "compatibility_answer", "Unknown.")`.
- **Language operator:** `getattr(..., "Unknown.")`.
- **Distinct standings entering:** present object missing a compatibility attribute and present object explicitly saying `Unknown.` become the same scalar `Unknown.`.
- **Representation produced:** `compatibility_answer="Unknown."`.
- **Consumer claim:** selection treats `Unknown.` as not enough for an aggregate `No.`.
- **Distinction preserved elsewhere:** `capability_keys`, view registration name, read-only/event flags, and explicit `view is None` branch preserve core handoff limits; the consumer does not need missing-attribute provenance to avoid negative authority.
- **Fidelity finding:** **faithful because consumer does not require the distinction**. The default is conservative Unknown, not fabricated `No.`.
- **Negative authority:** this does not establish every `getattr` default is lawful; this one is bounded by a conservative consumer.

### 4. External material surface-feature JSON unknown-list default

- **Local constitutional question:** Can a structural projection JSON object be accepted and projected into surface features while preserving line/region unknowns required by the feature projection?
- **Subject/package:** external material structural projection JSON, including root `projection_unknowns`, line `unknowns`, and region `unknowns`.
- **Lawful standing:** supplied unknowns must remain Unknowns; a legacy payload with omitted unknown fields may be accepted as absence of unknown testimony if the bounded feature consumer does not require distinguishing legacy absence from explicitly empty unknowns.
- **Formation responsibility:** deserialization validates required object/list/string/int/bool fields, requires `line_ids` for regions without a default, and defaults `projection_unknowns` and per-line `unknowns` to `[]`.
- **Language operator:** `data.get("projection_unknowns", [])` and `data.get("unknowns", [])`.
- **Distinct standings entering:** omitted unknown-list field and explicitly empty unknown-list field become the same empty tuple.
- **Representation produced:** `projection_unknowns=()` or `line.unknowns=()`.
- **Consumer claim:** `_line_feature(...)` carries `line.unknowns` forward; feature rendering does not claim that unknowns were audited absent, only displays feature counts and unknown payload when present.
- **Distinction preserved elsewhere:** required structural coordinates remain strictly validated; root artifact identity and line features remain available.
- **Fidelity finding:** **representation collision without evidenced consumer consequence**. No recovered consumer in this pass relies on omitted-unknown-list as audited negative unknown testimony.
- **Negative authority:** this does not mean omitted and explicit empty are always equivalent; it only records no stronger consumer reliance recovered here.

### 5. Response-summary JSON payload fallback

- **Local constitutional question:** How should a CLI response summary render a provider/tool response payload, recommendations, and output?
- **Subject/package:** a response dictionary with optional `message`, `payload`, `output`, and `recommendations` fields.
- **Lawful standing:** malformed or absent payload may still permit a compact display of response kind/message; recommendation display requires a non-empty list.
- **Formation responsibility:** `format_response_summary(...)` validates response is a dict, narrows payload to a dict or `{}`, and renders output only if present.
- **Language operator:** `response.get("payload") if isinstance(...) else {}`, `response.get("message") or ""`, and `if isinstance(recommendations, list) and recommendations`.
- **Distinct standings entering:** absent payload and non-dict payload become `{}` for recommendation/output purposes; absent message and intentionally blank message become the same fallback to response kind.
- **Representation produced:** compact human summary lacking output/recommendations/message line.
- **Consumer claim:** the formatter claims display sufficiency, not semantic completeness of provider testimony.
- **Distinction preserved elsewhere:** the original `response` can still be stringified when not a dict; JSON command paths can expose structured data separately.
- **Fidelity finding:** **faithful because consumer does not require the distinction** for a human summary.
- **Negative authority:** this does not authorize discarding payload shape at a semantic or recording boundary.

### 6. SQLite projection snapshot no-row lookup

- **Local constitutional question:** Is there a persisted projection snapshot for a workspace/name/version that can be loaded as a cache hit?
- **Subject/package:** `projection_snapshots` rows keyed by workspace, projection name, and projection version.
- **Lawful standing:** row present with JSON payload; no row as cache miss; incompatible schema may have been dropped before lookup; JSON decode failure is not represented as miss.
- **Formation responsibility:** `SQLiteProjectionStore` opens/migrates the cache tables, drops incompatible cache tables, and `load_snapshot(...)` queries a specific key.
- **Language operator:** SQL `SELECT ... fetchone()` and Python `if row is None: return None`.
- **Distinct standings entering:** no row and row with malformed JSON do not collide; malformed JSON raises during `json.loads`. No row and incompatible dropped cache both surface as miss, but schema compatibility is owned earlier by `_drop_incompatible_cache_tables()`.
- **Representation produced:** `ProjectionSnapshot | None`.
- **Consumer claim:** cache users treat `None` as miss and rebuild; they do not claim that a projection never existed.
- **Distinction preserved elsewhere:** cache debug surfaces can expose hit/miss/unavailable/skipped; table compatibility is checked locally before load.
- **Fidelity finding:** **faithful compression** for cache lookup. Absence-as-miss is lawful for rebuilding a read model.
- **Negative authority:** this does not mean no SQL row is globally negative constitutional fact.

### 7. SQLite derived-index join with `IS` for nullable event identity

- **Local constitutional question:** Is a derived index snapshot valid for the current state projection version and nullable `last_event_id`?
- **Subject/package:** derived index snapshot joined to the state projection snapshot that it depends on.
- **Lawful standing:** hit only when derived and state snapshots agree on state projection version, nullable last-event identity, and read-only mutation flags; otherwise miss.
- **Formation responsibility:** `load_derived_index_snapshot(...)` joins derived and state snapshots and requires both `mutates_cluster=0`.
- **Language operator:** SQL `JOIN`, nullable comparison by `IS`, and `fetchone() -> None`.
- **Distinct standings entering:** no derived row, stale derived row, missing state partner, mutation-flag mismatch, and last-event mismatch all become `None` to the cache consumer.
- **Representation produced:** `DerivedIndexSnapshot | None`.
- **Consumer claim:** consumer reads `None` as cache miss, not as unsupported relation or negative index fact.
- **Distinction preserved elsewhere:** the SQL predicate itself preserves the current dependency identity before deciding hit/miss; rebuild path can reconstruct from current state.
- **Fidelity finding:** **faithful because consumer does not require the distinction** among miss causes for its bounded rebuild purpose.
- **Negative authority:** this does not establish that stale, absent, and mutation-mismatched rows are constitutionally equivalent outside cache eligibility.

### 8. State-build cache-debug status assembly

- **Local constitutional question:** What cache visibility can the CLI diagnostic report for state-build: eligible, unavailable, hit, miss, skipped, and associated event ids?
- **Subject/package:** projection store availability, current ledger event id, state summary snapshot lookup, state snapshot lookup, and cache eligibility conditions.
- **Lawful standing:** unavailable store/eligibility, summary hit, state lookup skipped, state hit, state miss, stale snapshot, and current empty ledger may need distinct diagnostic statements.
- **Formation responsibility:** `_state_build_cache_debug_evidence_from_args(...)` initializes statuses as `unavailable`, records ineligible reasons, computes current last event id as `None` for an empty ledger, and distinguishes summary hit from state skipped and state miss.
- **Language operator:** `latest_events[-1].id if latest_events else None`, `"hit" if snapshot is not None and snapshot.last_event_id == current_last_event_id else "miss"`, and status strings.
- **Distinct standings entering:** current empty ledger and last-event id `None` in a snapshot can compare equal; stale, absent, and mismatch become `miss`.
- **Representation produced:** explicit status fields plus nullable cached/current event ids.
- **Consumer claim:** cache-debug output reports status and ids; cache rebuilding logic treats miss as a reason to rebuild, not as negative cache truth.
- **Distinction preserved elsewhere:** `cache_eligible`, `cache_ineligible_reason`, `summary_cache_status`, `state_cache_status`, `current_last_event_id`, `cached_*_last_event_id`, and notes preserve more than a single boolean.
- **Fidelity finding:** **faithful because separate standing is preserved elsewhere** for the diagnostic purpose, with a possible follow-up question around empty-ledger snapshot equality if a future consumer treats it as a stronger currentness claim.
- **Negative authority:** this does not require every cache status to expose every miss cause.

### 9. Repository observation Git subprocess collapse

- **Local constitutional question:** Can repository state be observed from Git for a repository path?
- **Subject/package:** local Git command execution, return code, stdout text, and path availability.
- **Lawful standing:** successful command with stdout; command unavailable; invalid cwd; nonzero Git status; parse/semantic absence.
- **Formation responsibility:** `_git_text(...)` runs `git`, catches `OSError`/`ValueError`, maps nonzero return codes to `None`, and returns stdout on success.
- **Language operator:** subprocess exit code plus `return None` for both caught execution errors and nonzero return code.
- **Distinct standings entering:** command unavailable/OS error, invalid invocation/value error, and Git nonzero response become indistinguishable as `None`.
- **Representation produced:** `str | None`.
- **Consumer claim:** `_git_ok(...)` treats `None` as not-ok (`False`) by requiring text to be present and equal to `true` after strip.
- **Distinction preserved elsewhere:** no separate reason is carried by `_git_text`; higher-level observation may only know that the Git-based testimony is unavailable/not affirmative.
- **Fidelity finding:** **possible crossing — consumer not yet recovered**. If the consumer only needs safe non-affirmation, this is faithful; if it reports negative repository facts, the unavailable/nonzero distinction may become lossy.
- **Negative authority:** this does not indict subprocess use; it identifies a bounded reason-collapse seam.

### 10. Command model transport stdout-only return

- **Local constitutional question:** What text completion did a configured local command return for a prompt?
- **Subject/package:** subprocess completion with stdout, stderr, exit code, timeout, and command availability.
- **Lawful standing:** successful empty completion, successful non-empty completion, command failure, timeout, command not found, and stderr-only diagnostic need different treatment at the transport boundary.
- **Formation responsibility:** `CommandTransport.complete(...)` delegates to `subprocess.run(..., check=True, timeout=..., capture_output=True)` and returns only `completed.stdout` on success.
- **Language operator:** subprocess `check=True` exception boundary plus stdout-only projection.
- **Distinct standings entering:** successful empty stdout and successful meaningful empty model response both return `""`; stderr on successful exit is discarded from the returned representation; failures/timeout are exceptions rather than returned status.
- **Representation produced:** `str` on success; exceptions otherwise.
- **Consumer claim:** `DecisionPromptModelClient` consumes the transport as text completion. It needs stdout text, while failure remains exceptional rather than collapsed into empty output.
- **Distinction preserved elsewhere:** command failure and timeout are not converted to empty stdout; they remain exception standing. Successful stderr is not preserved in the `str`.
- **Fidelity finding:** **faithful for failure-vs-empty**, with **representation collision without evidenced consumer consequence** for successful empty stdout versus successful stderr-bearing stdout-only completion.
- **Negative authority:** this does not require a universal process result object for every transport.

### 11. Audit snapshot Git metadata best-effort fallback

- **Local constitutional question:** What Git metadata can be attached to an audit snapshot without blocking snapshot creation?
- **Subject/package:** branch, commit, porcelain status, and Git availability for the repository root.
- **Lawful standing:** available Git metadata; unavailable Git; command failure; unexpected exception; dirty vs clean status.
- **Formation responsibility:** `collect_git_metadata(...)` runs three Git commands and returns `available=True` plus fields on success; any exception returns `available=False` and a reason.
- **Language operator:** broad exception fallback and `dirty: bool(changed)`.
- **Distinct standings entering:** command not found, not-a-git-repo, permission error, and other Git failures all become `available=False` with textual reason; clean repo and empty porcelain output become `dirty=False`.
- **Representation produced:** availability boolean plus reason or metadata.
- **Consumer claim:** audit snapshots use Git metadata as best-effort context; snapshot creation must continue.
- **Distinction preserved elsewhere:** `reason` preserves some failure testimony; `changed_files` preserves details when available.
- **Fidelity finding:** **faithful because consumer does not require the distinction** among Git failure kinds for snapshot creation, and because absence of changed lines lawfully supports clean working tree within successful Git status testimony.
- **Negative authority:** this does not mean `bool(changed)` is always sufficient for repository state; it is bounded by successful `git status --porcelain`.

### 12. Architecture generator metadata defaults

- **Local constitutional question:** Can architecture graph nodes be generated from class metadata embedded in source code?
- **Subject/package:** AST-scanned class metadata literal with optional owner/layer/summary/events/routes/edges.
- **Lawful standing:** class with no recognized metadata; metadata present with omitted optional fields; explicitly empty metadata fields.
- **Formation responsibility:** `_build_graph(...)` skips classes whose `scan.metadata` is falsy, then defaults optional display fields using `.get(..., default)`.
- **Language operator:** `if not scan.metadata: continue` and `scan.metadata.get("owner", "unspecified")`, etc.
- **Distinct standings entering:** no metadata and empty metadata dictionary are both skipped; omitted owner and explicit absence of an owner field become `"unspecified"` in the graph.
- **Representation produced:** graph node with default display values, or no node.
- **Consumer claim:** generated architecture graph is a documentation/read-model artifact over recognized metadata, not constitutional proof that an owner is absent.
- **Distinction preserved elsewhere:** source file and line are preserved for included nodes; classes without metadata are outside the graph's declared input package.
- **Fidelity finding:** **faithful because consumer does not require the distinction** for this generated architecture documentation purpose.
- **Negative authority:** this does not promote `unspecified` into repository knowledge or require all omitted fields to become explicit status values.

## Language-specific compression patterns

- **Python truthiness and vacuous quantification:** Python makes empty packages easy to turn into aggregate truth. This is lossy in the composition scalar when the consumer reads `No.` as aggregate negative testimony. It is faithful in selection because the list is explicitly guarded and no-match uncertainty is preserved.
- **Default substitution:** `.get(..., [])`, `.get(..., {})`, `.get(..., "Unknown.")`, and `or` defaults can erase omitted-vs-empty or blank-vs-absent distinctions. They are faithful when the consumer only needs conservative display or Unknown; they are riskier when the default is negative testimony.
- **SQL/SQLite no row and nullable comparison:** SQLite naturally preserves row presence and nullable columns, but application code often compresses all non-hit reasons into `None`. In cache districts this is generally faithful because the consumer purpose is rebuild eligibility, not negative constitutional fact.
- **Serialization boundaries:** JSON omission and explicit empty lists collide in several deserializers. Stronger loss was not evidenced where required fields remain strict and omitted optional unknown lists are not consumed as audited negative unknown testimony.
- **Process boundaries:** Subprocess APIs preserve exit, stdout, stderr, timeout, and exceptions, but local helpers may project them to `None` or stdout-only strings. Failure-vs-empty is preserved in `CommandTransport` through exceptions, but `_git_text` collapses failure reasons into `None`.
- **Cache sentinels:** `None` is used as a cache miss sentinel. This is faithful where separate status fields or rebuild logic prevent interpreting miss as nonexistence; possible crossings appear where later users might treat `None` as a negative fact.
- **Provider/transport silence:** Actual provider-like code was evidenced at model HTTP/command and Prometheus-style boundaries, but this pass did not recover a strong no-response/timeout consumer reliance beyond process/model transport. Timeout should not be read as negative response unless a local consumer proves that purpose.

## Rejected universalizations

This survey rejects these conclusions:

- every `all(...)`, `any(...)`, `if not value`, `None`, empty collection, SQL no-row, JSON omission, or default is defective;
- Python, SQLite, JSON, subprocesses, or HTTP are globally more or less constitutionally faithful;
- all empty values require explicit status fields;
- all packages need a lifecycle object;
- all consumers require full producer provenance;
- all collisions require implementation repair;
- a universal package/projection/status/result/aggregate abstraction is warranted.

## Preserved Unknowns

Recovered preserved Unknowns include:

- selection no-match and unsupported keys are carried in `selection_uncertainty`;
- missing capability compatibility on a present projected view defaults conservatively to `Unknown.`, not `No.`;
- contributing view unknowns and explicit refusals are preserved in composition even though the compatibility scalar is lossy for empty input;
- external material unknown lists are carried when present;
- cache-debug status preserves unavailable/hit/miss/skipped and event ids rather than a single truthy cache value.

## Final comparison table

| Neighborhood | Language mechanism | Formation standing | Representational collision | Consumer reliance | Fidelity finding | Next bounded question |
|---|---|---|---|---|---|---|
| Constitutional View Composition | Python `all([])` | requested contributing view package | empty package + all-negative package -> `No.` | compatibility scalar is rendered and transported as `No.` | lossy constitutional compression | Should empty requested composition preserve empty-package standing separately from compatibility answer? |
| Constitutional View Selection | guarded `all(...)` | matched capability package | no empty/all-negative collision in scalar because of guard | composition receives uncertainty and selected names | faithful because separate standing is preserved elsewhere | None for this survey. |
| Capability projection | `getattr(..., "Unknown.")` | present/absent view compatibility testimony | missing attr + explicit Unknown -> `Unknown.` | selection treats Unknown conservatively | faithful because consumer does not require distinction | None unless a future consumer audits producer schema conformance. |
| External material features | JSON `.get(..., [])` | unknown-list handoff | omitted unknowns + explicit empty unknowns -> `()` | feature projection carries unknowns but does not claim audited absence | representation collision without evidenced consumer consequence | Does any downstream audit treat empty unknowns as complete no-unknown testimony? |
| Response summary | `.get`, `or`, `{}` fallback | provider response display payload | absent/non-dict payload and absent/blank message collapse for display | human summary only | faithful because consumer does not require distinction | None unless summary becomes recordable semantic output. |
| Projection snapshot cache | SQL no row -> `None` | persisted snapshot lookup | no row + compatible cache miss reasons -> `None` | rebuild/read cache miss | faithful compression | None for cache rebuild purpose. |
| Derived index cache | SQL join + nullable `IS` + `None` | dependency-valid derived index | absent/stale/mismatched rows -> `None` | rebuild/read cache miss | faithful because consumer does not require distinction | None unless diagnostic starts explaining miss causes. |
| State-build cache debug | status strings + nullable ids | cache visibility evidence | stale/absent/mismatch -> miss; empty ledger id is `None` | diagnostic reports statuses and ids | faithful because separate standing is preserved elsewhere | Does empty-ledger snapshot equality need explicit standing if currentness claims expand? |
| Repository observation Git | subprocess errors/nonzero -> `None` | Git operational testimony | OS error + nonzero Git -> `None` | `_git_ok` reads `None` as not affirmative | possible crossing — consumer not yet recovered | Does any rendered repository observation turn `None` into negative Git/repo testimony? |
| Command model transport | subprocess check + stdout-only | model command completion | successful empty stdout + successful stdout-only completion -> `""`; stderr discarded | model client consumes stdout text | faithful for failure-vs-empty; collision without evidenced consequence for stderr | Does any model caller need successful stderr diagnostics? |
| Audit snapshot Git metadata | exception fallback + `bool(changed)` | Git snapshot metadata | Git failure kinds -> unavailable; empty porcelain -> clean | best-effort snapshot context | faithful because consumer does not require distinction | None for snapshot continuation purpose. |
| Architecture generator | truthiness + `.get` defaults | AST metadata presence | missing/empty metadata skipped; omitted owner -> unspecified | generated documentation graph | faithful because consumer does not require distinction | Do generated docs ever become ownership authority? |

## Closing questions

### Which realization-language operators actually collapse constitutionally distinct standings in this repository?

`all([])` in Constitutional View Composition collapses empty package standing into aggregate `No.`. JSON `.get(..., [])` collapses omitted unknown-list fields into explicitly empty unknown lists. `.get`/`or` display fallbacks collapse absent/blank or malformed/absent display fields. SQL `fetchone() -> None` collapses multiple cache non-hit causes. Subprocess helpers collapse OS/nonzero Git failures into `None` or project successful commands to stdout-only strings. Truthiness in graph generation collapses no metadata and empty metadata for documentation inclusion.

### Which collisions are harmless because the consumer does not require the distinction?

Capability projection's missing-attribute/explicit-Unknown collision is harmless for selection because selection only needs to avoid manufacturing `No.`. Response-summary defaults are harmless for human display. SQL cache miss collisions are harmless for rebuild-oriented cache consumers. Audit snapshot Git failure-kind compression is harmless for best-effort snapshot continuation. Architecture metadata defaults are harmless for generated documentation when not treated as ownership authority.

### Which distinctions are preserved through another local artifact or responsibility?

Selection preserves no-match and unsupported-key standing through `selection_uncertainty` and an explicit non-empty aggregate guard. Composition preserves contributing unknowns/refusals even though the compatibility scalar is lossy for empty input. Cache debug preserves status, eligibility reason, notes, and event ids. Projection store preserves read-only mutation flags and dependency identity in SQL predicates before compressing non-hits into miss.

### Which collisions become lossy because a consumer relies on stronger standing?

The strongest recovered lossy crossing is Constitutional View Composition: empty `compatibility_answers` and all-negative populated `compatibility_answers` both produce `compatibility_answer="No."`, and that scalar is exposed as the composition compatibility claim.

### Which findings remain possible crossings because the consumer has not yet been independently recovered?

Repository observation Git `_git_text(...) -> None` remains a possible crossing because command unavailability, invocation errors, and nonzero Git responses collapse before `_git_ok(...)`; this is faithful only if later consumers read it as non-affirmation rather than negative repository fact. State-build empty-ledger snapshot equality is a smaller possible follow-up if future diagnostics strengthen currentness claims.

### Which local district is the strongest candidate for the next bounded recovery or repair?

The strongest candidate is Constitutional View Composition compatibility aggregation, because it is already calibrated by the Book grammar and has an evidenced scalar consumer. The next bounded recovery should stay local to composition standing and should not design a universal aggregate abstraction.

### What cross-language compression patterns recur without warranting a universal abstraction?

Recurring patterns are vacuous aggregate truth, conservative Unknown defaults, omission-to-empty JSON defaults, no-row/cache-miss sentinels, subprocess failure-to-`None` seams, stdout-only transport, exception best-effort fallback, and display-only default labels such as `unspecified`. They recur as local realization risks, not as proof that a universal package, status, result, projection, or aggregate architecture is warranted.
