# Bootstrap Invariants

## Purpose

Bootstrap invariants are a small set of architectural findings that should survive continuation even when authoritative references are temporarily unavailable.

They are not a substitute for architecture.

They are not authority.

They are not a compressed ontology.

They are the minimum assumptions required to interpret the architecture correctly.

## Motivation

A handoff should primarily contain references.

However, a future session may temporarily lack access to:

- repository documents;
- reconciliations;
- ontology references;
- architectural maps.

Without a minimal set of preserved invariants, the architecture may be misinterpreted before authoritative documents are consulted.

Bootstrap invariants exist to reduce that risk.

## Important Distinction

Bootstrap invariants are context-dependent.

Different continuation paths may require different bootstrap assumptions.

Examples:

- Human-to-Seed continuation may require language-related invariants.
- Seed-to-Seed continuation may already share protocol semantics and therefore not require language-related invariants.
- Operator handoffs may require authority-boundary invariants.
- Federation handoffs may require provenance-boundary invariants.

Therefore there is not necessarily one universal bootstrap invariant set.

## Characteristics

A bootstrap invariant should:

- be small;
- be stable;
- prevent major misinterpretation;
- help decode authoritative documents;
- not require reproducing architecture.

A bootstrap invariant should not:

- become authority;
- replace documentation;
- summarize entire reconciliations.

## Example Human-Oriented Bootstrap Invariants

- Seed is claim-centric.
- Natural language observes communicative acts.
- Import is not verification.
- Learning does not erase history.
- Projection is not authority.
- Handoff is not authority.

## Relationship To Handoffs

A handoff should primarily contain references.

Bootstrap invariants exist only to help a future reader interpret those references correctly.

The handoff remains a continuation-alignment artifact.

The architecture remains authoritative elsewhere.

## Conclusion

Bootstrap invariants are continuity aids.

Their purpose is to prevent immediate architectural drift before authoritative references are available and validated.

Different participants may require different bootstrap invariant sets depending on the continuation context.