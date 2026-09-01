# Bootstrap Invariants

## Purpose

Bootstrap invariants are a small set of architectural findings that should survive continuation even when authoritative references are temporarily unavailable.

They are not a substitute for architecture.

They are not authority.

They are not a compressed ontology.

They are the minimum assumptions required to interpret the architecture correctly.

They help activation, but they do not guarantee activation. A future participant
may possess or even read bootstrap invariants without making them active working
state or complying with the validated continuation boundary.

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

Different continuation contexts and paths may require different bootstrap
assumptions. The invariant set should fit the participant, task, authority
surface, risk, and handoff boundary rather than becoming a universal checklist.

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
- help activate the continuation boundary in working state;
- not require reproducing architecture.

A bootstrap invariant should not:

- become authority;
- replace documentation;
- be treated as proof of activation or compliance;
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

Bootstrap invariants exist only to help a future reader interpret those references
correctly and activate the relevant boundary before full reference validation.

The handoff remains a continuation-alignment artifact.

The architecture remains authoritative elsewhere.

## Conclusion

Bootstrap invariants are continuity aids.

Their purpose is to reduce immediate architectural drift before authoritative
references are available and validated. They do not guarantee that the handoff was
consumed, that the bootstrap was activated, or that the continuation remains
compliant with validated references, repository state, operator intent, frontier,
boundaries, and risks.

Different participants may require different bootstrap invariant sets depending on
the continuation context.
