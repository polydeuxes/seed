# Python–SQLite Frontier Pass 084 — Derived Fact-Index Boundary Implementation

Repository authority wins.

## Implemented boundary

Pass 084 implements only the selected derived fact-index boundary:

Python fact-index construction produces `DerivedIndexSnapshot` with `DerivedIndexSnapshotBoundary`; SQLite preserves that boundary in `derived_index_snapshots`; Python cache consumption admits the row only when both the source projection boundary and derived-index boundary remain within read-model cache limits.

## Preserved behavior

- The event ledger remains authoritative.
- Incompatible disposable cache schemas are still dropped and recreated.
- Projection source eligibility remains required.
- Rejection of an ineligible derived-index row is a cache miss/rebuild condition, not corruption proof, cluster mutation, or a new event occurrence.
- Existing public fact-index payload behavior is unchanged.

## Stop condition

This pass does not implement receipt, reliance, correction, reopening, diagnostic surfaces, universal cache envelopes, compatibility migrations, or new constitutional vocabulary. It stops at the concrete producer → SQLite artifact → consumer handoff for the derived fact index.

## Tests

Focused tests prove that SQLite preserves the derived-index boundary, rejects a row whose own consumer limit/mutation flag leaves the fact-index cache boundary, rebuilds the same lawful read model from projected State, and appends no ledger events. Existing projection-store reset tests prove the new schema remains disposable and recoverable.
