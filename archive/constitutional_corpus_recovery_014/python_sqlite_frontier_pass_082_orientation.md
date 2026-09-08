# Python–SQLite Frontier Pass 082 — Orientation

Repository authority wins. This pass changes no code.

## High-resolution frontier

| Pressure | Classification | Evidence | Finding |
| --- | --- | --- | --- |
| Python performs constitutional acts while SQLite preserves durable artifacts and disposable read models. | repository-established | Passes 069–081 and `SQLiteProjectionStore` separate event replay, projection construction, cache preservation, and cache reset. | The implementation picture is bounded and should not be broadened into a generic hybrid framework. |
| Event ledger remains authoritative. | repository-established | Cache reset in pass 081 leaves ledger tables untouched and rebuilds projections from events. | Cache rows may be dropped; event rows may not be invented or interpreted from cache compatibility. |
| Projection snapshot boundary columns gate state-cache consumption. | implementation evidence | `projection_snapshots` stores standing, producer boundary, occurrence kind, consumer limit, and mutation flag. | State projection cache has explicit preservation testimony and Python rehydration eligibility. |
| Summary read-model rows carry inherited source limits and own consumer limit. | implementation evidence | `state_summary_snapshots` stores source standing columns plus `operator_summary_cache_only`. | Summary consumption has a concrete cross-realization handoff. |
| Derived fact-index rows are source-gated but do not carry their own boundary testimony. | unresolved | Pass 080 gates load on the source projection row, while `derived_index_snapshots` stores only identity, payload, and timestamps. | The fact-index crossing artifact has weaker testimony than the summary crossing artifact. |
| Complete circulation, correction, reopening, receipt, and reliance topology. | unresolved | Circulation current state leaves delivery/receipt/reliance/correction/reopening proof mechanics open. | No Python–SQLite implementation seam should claim these broader topologies now. |
| Missing constitutional acts beyond projection/cache consumption. | unsupported | Current evidence shows local projection, summary, and fact-index cache mechanics, not a new constitutional act family. | Do not promote cache vocabulary into constitutional grammar. |

## Ground-resolution map

| Ground item | Classification | Concrete evidence | Pressure |
| --- | --- | --- | --- |
| Python owner: `StateProjector` / `project_state_with_cache`. | implementation evidence | Builds `State` from ledger or eligible snapshot. | Owns projection act, not durable authority. |
| SQLite artifact: `projection_snapshots`. | implementation evidence | Stores state JSON plus boundary columns. | Disposable cache with explicit standing. |
| Consumer: Python state cache loader. | implementation evidence | Rejects stale or boundary-ineligible snapshots. | Lawful result is cache hit or rebuild. |
| Python owner: state-summary construction. | implementation evidence | Summary cache load requires matching source testimony. | Boundary already implemented. |
| SQLite artifact: `state_summary_snapshots`. | implementation evidence | Preserves inherited source columns and own consumer limit. | Not the critical missing seam now. |
| Python owner: `load_or_build_fact_index`. | implementation evidence | Builds fact index from projected State and saves `DerivedIndexSnapshot`. | Producer exists. |
| SQLite artifact: `derived_index_snapshots`. | unresolved | Payload is compressed JSON with state projection version/event id, but no own boundary columns. | Crossing artifact does not testify to derived-index standing or mutation limit. |
| Consumer: fact-index cache load. | unresolved | Load checks source projection row only. | Consumer cannot distinguish a row claiming fact-index cache from a mutating or cluster-truth derived row except by absent columns. |
| Compressed payloads. | implementation evidence | State, summary, and index payloads are JSON. | Payload identity is not authority; boundary columns must carry cache limits where needed. |
| Untested handoff: derived-index own boundary. | unresolved | Tests cover source projection mismatch but not derived row standing/mutation mismatch. | Smallest actionable pressure. |
| Disconnected witnesses: receipt/reliance/correction/reopening. | unresolved | Reports preserve them as unknown topology. | Stop outside pass 084. |
| Ambiguous mutation or occurrence boundaries in derived-index rows. | unresolved | `derived_index_snapshots` has `created_at` but no `mutates_cluster` or occurrence-kind equivalent. | Candidate for recovery. |

## Orientation result

The critical remaining pressure inside the implemented Python–SQLite frontier is not another cache reset seam. It is the derived fact-index crossing artifact: Python produces it, SQLite preserves it, and Python consumes it, but the row does not preserve its own derived-read-model standing, occurrence boundary, consumer limit, or mutation limit. Neighboring circulation, correction, receipt, and reliance topologies remain unresolved but are broader than the available implementation evidence.
