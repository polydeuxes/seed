# Cache boundary pass 085 — Reality audit

## Scope

This pass audits the projection, summary, and derived-index cache boundary fields added by prior cache-boundary passes. It does not treat existing code as self-justifying; it asks whether each field prevents a concrete repository-evidenced runtime failure by a real producer or consumer.

## Ground requirements that remain repository-established

- Cache identity and schema validity: cache rows must belong to the expected table, name, version, workspace, and current schema shape.
- Event horizon: projection, summary, and derived-index rows must match the state projection version and last event they were built from.
- Payload materialization: malformed or incompatible cached payloads must miss or rebuild instead of becoming runtime state.
- Rebuild behavior: incompatible cache tables may be dropped and rebuilt from the surviving event ledger.
- Ledger authority: the event ledger remains the append-only source of history; cache reads do not create event occurrence.
- Read-only execution: a cache row that testifies it mutates the cluster must not enter read-only cache consumers.

## Projection snapshot boundary fields

| Field | Incorrect runtime behavior without it | Real producer or consumer able to perform that behavior | Enforces boundary or describes it | Requirement source |
| --- | --- | --- | --- | --- |
| `artifact_standing` | No concrete runtime failure was found. Cache admission is already controlled by projection name, version, event horizon, schema, payload materialization, and read-only mutation flag. A row saying `established_fact` does not by itself mutate ledger history or make a fact true unless a consumer reads the string as authority, and no real consumer does. | Prior tests manually constructed such rows; no production producer emits strengthened standing, and cache consumers do not branch on it except the added predicate itself. | Merely describes standing; the predicate rejects labels but does not prevent a demonstrated behavior outside itself. | Inferred from constitutional vocabulary and symmetry with diagnostic/read-model language. |
| `producer_boundary` | No concrete runtime failure was found. A cache row with the expected projection identity, version, event horizon, and materializable payload is either usable or not based on those facts; the producer label is not independently verified. | Manual tests can write `sqlite_self_authorized`; the SQLite store and Python saver write constants. No consumer can use the string to reconstruct actual provenance. | Descriptive; it cannot enforce actual origin because any writer can set the string. | Inferred from pass vocabulary, not repository-established as a cache requirement. |
| `occurrence_evidence_kind` | No concrete runtime failure was found. Rehydrating a snapshot does not append events, and event occurrence remains controlled by ledger APIs and event counts, not this label. | Cache loaders read the string only in the added predicate; ledger consumers inspect events rather than this field. | Descriptive; event non-occurrence is enforced by not writing the ledger. | Repository establishes no-new-event behavior, but this field is an inferred description of that behavior rather than its enforcement mechanism. |
| `consumer_limit` | No concrete runtime failure was found for the string. A row labeled `cluster_truth` does not become cluster truth unless a consumer grants that authority, and no real consumer does. | Manual tests only; real consumers materialize state payloads for read-model use. | Descriptive; the real boundary is the read-only cache path plus `mutates_cluster=false`. | Inferred from symmetry with operational surfaces. |
| `mutates_cluster` | Concrete failure: a cache row explicitly marked mutation-bearing could be admitted into a read-only state cache path, obscuring the repository's read-only execution boundary. | SQLite rows can be externally edited; in-memory tests can construct the row; `project_state_with_cache` is the read-only consumer. | Enforces a boundary when used as an admission predicate. | Repository-established read-only execution and diagnostic/cache mutation boundary. |

## Summary snapshot boundary fields

| Field | Incorrect runtime behavior without it | Real producer or consumer able to perform that behavior | Enforces boundary or describes it | Requirement source |
| --- | --- | --- | --- | --- |
| `artifact_standing` | No concrete runtime failure was found. Summary cache identity, version, state projection version, state last event, source state join, and payload are sufficient to decide cache eligibility. | Real saver writes a constant; loaders only reject because the added predicate says so. | Descriptive. | Inferred from projection-cache symmetry. |
| `source_artifact_standing` | No concrete runtime failure was found. The source row is already joined by projection name/version/event horizon. Copying its standing label into the summary row does not prove a source boundary. | Real saver copies a constant; external SQLite edits can set any value. | Descriptive and forgeable. | Inferred from pass 074 source-limit vocabulary. |
| `source_producer_boundary` | No concrete runtime failure was found. It cannot prove Python produced the source row. | Real saver writes a constant; no independent provenance checker exists. | Descriptive. | Inferred from symmetry with projection snapshot metadata. |
| `source_occurrence_evidence_kind` | No concrete runtime failure was found. Summary cache reads do not write events; event occurrence remains a ledger fact. | Loader and manual tests only. | Descriptive. | Inferred from occurrence vocabulary. |
| `source_consumer_limit` | No concrete runtime failure was found. No consumer treats the summary as cluster truth based on this copied string. | Manual SQLite update test only. | Descriptive. | Inferred from source-limit symmetry. |
| `consumer_limit` | No concrete runtime failure was found beyond the general read-only mutation boundary. | Manual edits only; no real consumer uses this string as authority. | Descriptive. | Inferred from operator-summary vocabulary. |
| `mutates_cluster` | Concrete failure: a mutation-bearing summary cache row could enter a read-only operator-summary cache path. | SQLite external edits or constructed snapshots; `load_summary_snapshot` is the consumer. | Enforces read-only admission. | Repository-established read-only execution. |

## Derived-index snapshot boundary fields

| Field | Incorrect runtime behavior without it | Real producer or consumer able to perform that behavior | Enforces boundary or describes it | Requirement source |
| --- | --- | --- | --- | --- |
| `artifact_standing` | No concrete runtime failure was found. Index name/version, state projection version, state last event, source state join, and payload decide cache eligibility. | Real saver writes a constant; no consumer grants fact authority from the string. | Descriptive. | Inferred from projection/summary symmetry. |
| `source_artifact_standing` | No concrete runtime failure was found. The source state row is already joined by version and event horizon. | Loader and manual edits only. | Descriptive and forgeable. | Inferred from source-limit vocabulary. |
| `source_producer_boundary` | No concrete runtime failure was found. It does not prove origin. | Real saver writes a constant; external writers can forge it. | Descriptive. | Inferred. |
| `source_occurrence_evidence_kind` | No concrete runtime failure was found. Derived-index reads do not append events. | Loader and manual tests only. | Descriptive. | Inferred. |
| `source_consumer_limit` | No concrete runtime failure was found. No real consumer uses this string to authorize cluster truth. | Manual tests only. | Descriptive. | Inferred. |
| `consumer_limit` | No concrete runtime failure was found beyond read-only mutation admission. | Manual edits only. | Descriptive. | Inferred from fact-index vocabulary. |
| `mutates_cluster` | Concrete failure: a mutation-bearing derived-index cache row could be admitted into a read-only fact-index cache path. | SQLite external edits or constructed snapshots; `load_derived_index_snapshot` is the consumer. | Enforces read-only admission. | Repository-established read-only execution. |

## Result consumed by pass 086

Supported cache-boundary machinery is limited to schema validity, cache identity, version and event horizon matching, payload materialization/rebuild behavior, ledger authority by absence of event writes, and `mutates_cluster=false` admission for read-only cache consumers. The standing, producer, occurrence-kind, source-limit, and consumer-limit strings are unsupported machinery because they describe projected constitutional vocabulary without preventing a repository-evidenced runtime failure.
