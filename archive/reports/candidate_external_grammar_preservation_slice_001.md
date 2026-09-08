# Candidate External Grammar Preservation Slice 001

## Recovered responsibility

Preserve caller-supplied competing structural grammar hypotheses and their attributed testimony as one immutable read-only artifact.

## Selected implementation boundary

This slice adds a narrow producer/artifact/consumer chain:

```text
caller-supplied attributed structural testimony
→ candidate grammar set assembler
→ immutable candidate external grammar artifact
→ read-only diagnostic/operator consumer
```

Seed owns only structural validation, tuple normalization, immutable assembly, deterministic JSON rendering, and deterministic human rendering.

## Why caller-supplied testimony is the producer boundary

No implementation-backed generic structural comparison owner currently produces candidate grammars. This slice therefore follows the existing boundary pattern in which the caller owns acquisition or candidate formation, and Seed owns bounded preservation. Future structural comparison may produce the same input shape without changing this artifact authority.

## Producer

The producer is the caller-supplied JSON input consumed by `--candidate-external-grammar`. The producer supplies representation scope, candidate identities, structural claims, claim scope, provenance, testimony references, unresolved alternatives, and explicit Unknowns.

## Input artifact

`CandidateExternalGrammarInput` preserves:

- `representation_scope`
- `candidates`
- `set_unknowns`

Each `CandidateExternalGrammarInputCandidate` preserves:

- `candidate_id`
- `structural_claim`
- `claim_scope`
- `provenance`
- `supporting_testimony`
- `contradicting_testimony`
- `unresolved_alternatives`
- `explicit_unknowns`

## Immutable output artifact

`CandidateExternalGrammarSet` preserves the supplied input as frozen dataclasses and adds fixed boundary/read-only fields:

- `boundary_notes`
- `read_only = true`
- `writes_event_ledger = false`
- `mutates_cluster = false`

## Consumer

The consumer is the bounded diagnostic/operator surface:

```bash
python scripts/seed_local.py --candidate-external-grammar INPUT.json
python scripts/seed_local.py --candidate-external-grammar INPUT.json --json
```

It only builds and displays the supplied candidate set.

## Candidate identity rules

Candidate IDs are stable only within the candidate set. They are not capability identities, tool identities, semantic entities, verified grammar identities, accepted candidates, rejected candidates, selected candidates, promoted candidates, or ranked candidates. The assembler validates that candidate IDs are present and unique within the set.

## Testimony-reference rules

Supporting and contradicting testimony are caller-supplied string references. They are preserved as references only. The assembler does not count them as confidence, evaluate support, evaluate contradiction, resolve conflict, infer warrant, generate testimony, or attach testimony to runtime evidence.

## Structural-only guardrail

The assembler preserves caller-provided structural claims without proving, ranking, rewriting, enriching, classifying, or semantically interpreting them. It does not use an LLM or heuristic classifier to determine whether text is structural or semantic. The human and JSON surfaces expose boundary notes that no semantic truth is established.

## Unknown preservation

Candidate-level `explicit_unknowns` and set-level `set_unknowns` are preserved as supplied. Unknown is not rewritten as false, absence of support is not contradiction, and absence of contradiction is not verification.

## Validation boundary

Validation is limited to deterministic structural integrity:

- required representation scope is present;
- required candidate ID is present;
- required structural claim is present;
- candidate IDs are unique;
- collection fields are lists or tuples of strings;
- immutable output can be constructed.

Validation does not determine truth, evidence quality, semantic equivalence, usefulness, verification, translator readiness, or capability readiness. Invalid duplicate candidate IDs fail through `CandidateExternalGrammarValidationError`. Invalid CLI input fails through the existing `parser.error(...)` boundary. Invalid input does not append events.

## Fields included

Included fields are representation scope, candidate ID, structural claim, claim scope, provenance, supporting testimony, contradicting testimony, unresolved alternatives, explicit Unknowns, set Unknowns, boundary notes, read-only flag, event-ledger flag, and cluster-mutation flag.

## Fields excluded

Excluded fields include ranking, selection, acceptance, rejection, promotion, confidence, semantic interpretation, parser realization, tool realization, translation specification, probe, verification, capability evidence, runtime Evidence, runtime Facts, Observations, event-ledger entries, projected State mutation, repository mutation, and cluster mutation.

## Read-only guarantees

The artifact and diagnostic preserve:

```text
read_only = true
writes_event_ledger = false
mutates_cluster = false
```

The diagnostic inventory declares the surface as non-recording, non-event-writing, and non-mutating. The diagnostic shape audit checks this registration.

## Compatibility answer

Did this slice change any existing compatibility boundary?

```text
No.
```

Existing observation behavior, structure-observation behavior, candidate-request behavior, capability candidate behavior, capability verification behavior, toolkit generation/validation/registration behavior, CLI flags, diagnostic inventory behavior, human output, JSON output, and existing tests are preserved.

## Files changed

- `seed_runtime/candidate_external_grammar.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_candidate_external_grammar.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`
- `candidate_external_grammar_preservation_slice_001.md`

## LOC delta

Final pre-commit `git diff --cached --numstat` reported 601 insertions and 2 deletions across the bounded implementation slice, focused tests, diagnostic registrations, and this report.

## Tests executed

- `pytest -q tests/test_candidate_external_grammar.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining missing roads

The following roads remain explicitly out of scope and unresolved:

```text
attributed samples
→ structural comparison
```

```text
structural comparison
→ candidate grammar generation
```

```text
candidate grammar
→ discriminating evidence need
```

```text
probe result
→ support / contradiction / inconclusive testimony
```

```text
supported candidate grammar
→ translation specification
```

```text
translation specification
→ validated translator realization
```

```text
translator validation
→ bounded capability evidence
```

```text
sufficient for inquiry
→ lawful stop
```
