# Constitutional Pipeline Operational Documentation 001

## Orientation verification

Verified the self-consumption demonstration conclusion:

```text
Completion classification:

Operationally complete with documentation gap
```

Verified demonstrated surfaces:

```text
seed --constitutional-pipeline
seed --constitutional-pipeline-diagnostic
seed ask --question-family "constitutional pipeline" --surface-args ...
```

Verified operational limitation:

```text
bounded ask:
  accepts one exact selection_key through its positional surface-arg contract

direct constitutional pipeline:
  accepts repeated --selection-key arguments
```

This task treats the limitation as intentional current behavior and documents it rather than changing it.

## Documentation locations inspected

Inspected repository documentation conventions and routing in:

- `README.md`
- `docs/README.md`
- `docs/index.md`
- existing operator/read-model guide area under `docs/README.md`
- existing CLI and bounded ask investigations found through repository search
- `python scripts/seed_local.py --help`
- `python scripts/seed_local.py ask --help`
- `scripts/seed_local.py`
- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/constitutional_pipeline_diagnostic.py`
- `tests/test_constitutional_pipeline.py`
- `tests/test_constitutional_pipeline_public_surface.py`
- `tests/test_constitutional_pipeline_integration_wiring.py`
- `tests/test_constitutional_pipeline_diagnostic.py`
- `tests/test_constitutional_pipeline_provenance_explanation.py`
- `constitutional_pipeline_self_consumption_demonstration_001.md`
- prior constitutional pipeline implementation reports in the repository root

## Operator documentation created or updated

Created:

- `constitutional_pipeline_operations.md`

Updated documentation index routing:

- `docs/README.md`

Created this report:

- `constitutional_pipeline_operational_documentation_001.md`

## Surfaces documented

Documented three distinct surfaces:

1. Direct public pipeline: `seed --constitutional-pipeline` / `python scripts/seed_local.py --constitutional-pipeline`
2. Stage diagnostic: `seed --constitutional-pipeline-diagnostic` / `python scripts/seed_local.py --constitutional-pipeline-diagnostic`
3. Bounded ask integration: `seed ask --question-family "constitutional pipeline" --surface-args ...` / `python scripts/seed_local.py ask --question-family "constitutional pipeline" --surface-args ...`

## Accepted inputs

Documented direct and diagnostic inputs:

- `--operator-inquiry`
- `--inquiry-provenance`
- `--bounded-question`
- `--constitutional-intent`
- `--scope-status`
- repeated `--selection-key`
- repeated `--pipeline-uncertainty`
- repeated `--pipeline-unknown`
- `--json`

Documented bounded ask positional `--surface-args` order:

```text
operator_inquiry inquiry_provenance bounded_question constitutional_intent scope_status selection_key
```

## Exact supported keys

Documented exact keys and selected views:

```text
process     -> constitutional_process
governance  -> constitutional_governance
fidelity    -> constitutional_fidelity
```

Documented that matching is exact and does not imply synonyms, semantic matching, fuzzy matching, natural-language inference, or capability discovery.

## Bounded ask single-key limitation

Documented prominently:

```text
The current bounded-ask surface-arg contract accepts one exact
selection_key value.

It does not split a space-separated value into multiple keys.

For multiple keys, use the direct --constitutional-pipeline surface
with repeated --selection-key arguments.
```

## Direct repeated-key behavior

Documented direct use of repeated `--selection-key` arguments for multiple exact keys and verified the command.

## Outcome interpretation

Documented distinct interpretation for:

- empty: no explicit selection key was supplied;
- unsupported: an explicit key did not match any projected capability key;
- Unknown: typed uncertainty remains unresolved;
- refused: a selected view contributed explicit refusals.

## Provenance explanation guidance

Documented that the provenance explanation shows:

- supplied question keys;
- projected capability keys;
- exact matched keys;
- unsupported keys;
- selected views;
- composition contributors;
- remaining uncertainty;
- Unknowns;
- refusals.

Documented that provenance explains deterministic view selection, not why the operator chose a key and not whether the operator inquiry is true.

## Diagnostic guidance

Documented stage statuses:

```text
complete
empty
unsupported
unknown
refused
```

Documented that a successful function return does not necessarily mean a complete constitutional answer, including the governance case where Selection is complete and Composition is refused because the selected view preserves explicit refusals.

## Testimony boundary

Documented prominently:

```text
Operator testimony is evidence, not fact.
```

Documented that pipeline execution preserves inquiry and provenance without verifying the inquiry, creating established facts, creating constitutional authority, creating authoritative capabilities, writing the event ledger, or mutating cluster state.

## Event-ledger and mutation boundaries

Verified and documented:

- direct public pipeline reports no event-ledger writes and no cluster mutation;
- diagnostic output reports no event-ledger writes and no cluster mutation;
- a neutral temporary database path remained without an events database after the documented examples, so no event count increase was observed;
- implementation diff is zero.

## Commands verified

Help and implementation orientation:

```bash
python scripts/seed_local.py --help
python scripts/seed_local.py ask --help
```

Documented command examples executed successfully:

```bash
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite --constitutional-pipeline --operator-inquiry 'Operator says process should be visible; testimony only.' --inquiry-provenance operator:docs --bounded-question 'Which constitutional process surface is available?' --constitutional-intent 'caller supplied bounded constitutional inquiry' --scope-status bounded --selection-key process
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite --constitutional-pipeline --operator-inquiry 'Operator asks for process and fidelity; testimony only.' --inquiry-provenance operator:docs --bounded-question 'Which constitutional views are available?' --constitutional-intent 'caller supplied bounded constitutional inquiry' --scope-status bounded --selection-key process --selection-key fidelity
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite --constitutional-pipeline --operator-inquiry 'Operator says process should be visible; testimony only.' --inquiry-provenance operator:docs --bounded-question 'Which constitutional process surface is available?' --constitutional-intent 'caller supplied bounded constitutional inquiry' --scope-status bounded --selection-key process --json
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite ask --question-family 'constitutional pipeline' --surface-args 'Operator says process should be visible; testimony only.' operator:docs 'Which constitutional process surface is available?' 'caller supplied bounded constitutional inquiry' bounded process --json
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite ask --question-family 'constitutional pipeline' --surface-args 'Operator prose mentions process but key intentionally absent; testimony only.' operator:docs 'Which constitutional view should be inferred from prose?' 'caller supplied bounded constitutional inquiry' bounded '' --json
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite --constitutional-pipeline --operator-inquiry 'Operator supplies unsupported exact key; testimony only.' --inquiry-provenance operator:docs --bounded-question 'Which unsupported constitutional view matches?' --constitutional-intent 'caller supplied bounded constitutional inquiry' --scope-status bounded --selection-key unsupported-explicit-key --json
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite --constitutional-pipeline --operator-inquiry 'Operator supplies Unknown evidence; testimony only.' --inquiry-provenance operator:docs --bounded-question 'Which process surface is available with Unknown preserved?' --constitutional-intent 'caller supplied bounded constitutional inquiry' --scope-status bounded --selection-key process --pipeline-unknown 'operator assertion not verified' --json
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite --constitutional-pipeline-diagnostic --operator-inquiry 'Operator says process should be visible; testimony only.' --inquiry-provenance operator:docs --bounded-question 'Which constitutional process surface is available?' --constitutional-intent 'caller supplied bounded constitutional inquiry' --scope-status bounded --selection-key process --json
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite --constitutional-pipeline --operator-inquiry 'Operator asks governance; testimony only.' --inquiry-provenance operator:docs --bounded-question 'Which constitutional governance surface contributes?' --constitutional-intent 'caller supplied bounded constitutional inquiry' --scope-status bounded --selection-key governance --json
python scripts/seed_local.py --db /tmp/seed-cp-doc/events.sqlite ask --question-family 'constitutional pipeline' --surface-args 'Operator supplies three exact keys; testimony only.' operator:docs 'Which constitutional views are available?' 'caller supplied bounded constitutional inquiry' bounded 'process governance fidelity' --json
```

Verification findings:

1. One-key bounded ask succeeds.
2. Space-separated multiple keys remain one unsupported exact key.
3. Repeated direct `--selection-key` arguments support multiple keys.
4. No-key invocation infers nothing.
5. Unsupported keys remain unsupported.
6. Unknowns remain visible.
7. Governance refusals remain visible.
8. Diagnostic output remains distinct from public pipeline output.
9. Event-ledger count remains unchanged; no events database was created during the checked command set.
10. No cluster mutation is observed by pipeline and diagnostic outputs.

## Files changed

- `constitutional_pipeline_operations.md`
- `constitutional_pipeline_operational_documentation_001.md`
- `docs/README.md`

## Documentation LOC delta

```text
+666 / -0
```

## Implementation LOC delta

```text
+0 / -0
```

## Tests or command checks

No implementation tests were changed. This documentation task used command verification against current help and current CLI behavior.

## Commit hash

Recorded in final operator response; embedding the final hash in this committed file would change the hash.

## Explicit answers

```text
Did this task recover or implement new architecture?

No.
```

```text
Did this task change constitutional pipeline behavior?

No.
```

```text
Is bounded ask documented as accepting one exact selection key?

Yes.
```

```text
Is the direct pipeline documented as accepting repeated exact keys?

Yes.
```

```text
Does the documentation claim natural-language key inference exists?

No.
```

## Completion classification

```text
Constitutional pipeline operationally complete and documented
```
