# Python–SQLite Frontier Pass 083 — Derived Fact-Index Boundary

Repository authority wins. This pass consumes pass 082 and changes no code.

## Selected boundary

Select exactly one boundary: Python-produced derived fact index → SQLite-preserved `derived_index_snapshots` row → Python fact-index cache consumer.

## Why this boundary is critical now

The repository already established the source projection cache boundary and the state-summary source boundary. The fact-index cache remains the smallest crossing artifact with an actual producer, durable SQLite row, and consumer, but without its own boundary testimony. Pass 080 made source-row eligibility necessary; it did not make the derived row testify to its own standing.

This matters because the fact index is a downstream read model. Its payload is compressed JSON, not authority. A row whose source projection is eligible still must not be consumed if the derived row itself claims cluster truth, mutates cluster state, or lacks the bounded fact-index cache consumer limit.

## Why neighboring candidates stop

- Projection cache schema/reset is already recovered by pass 081.
- State-summary cache consumption already preserves source and own consumer boundaries.
- Event-ledger durability is authoritative and should not be altered.
- Diagnostic inventory, receipt, reliance, correction, reopening, and circulation topologies are broader than this concrete handoff.
- No compatibility, legacy, universal schema, or future-proofing obligation is selected.

## Required proof for pass 084

Pass 084 must prove:

1. Producer: `load_or_build_fact_index` / fact-index construction emits a bounded derived-index snapshot.
2. Crossing artifact: SQLite stores derived-index boundary testimony alongside the compressed payload.
3. Consumer: `SQLiteProjectionStore.load_derived_index_snapshot` rejects rows outside the fact-index cache boundary.
4. Lawful result: rejection is a cache miss and rebuild from projected State, not ledger mutation or cluster truth promotion.
5. Stop condition: source projection eligibility remains required and neighboring topologies remain untouched.
