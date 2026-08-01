# Constitutional Pipeline Operations

This operator guide describes the current constitutional-pipeline entrances and their boundaries.

## Current topology

The constitutional pipeline remains a Python API whose request must contain an already-formed `BoundedConstitutionalQuestion`:

```text
already-formed BoundedConstitutionalQuestion
        ↓
ConstitutionalPipelineRequest
        ↓
question and capability projection
        ↓
constitutional view selection and composition
        ↓
ConstitutionalPipelineResult and provenance explanation
```

Callers may invoke `invoke_constitutional_pipeline(...)` or build the corresponding diagnostic with that typed request. The pipeline remains deterministic and read-only; it does not form a constitutional question from operator fields.

## Public CLI boundary

The flags `--constitutional-pipeline` and `--constitutional-pipeline-diagnostic` remain visible compatibility surfaces, but both refuse raw question fields. They do not construct a `BoundedConstitutionalQuestion` and are not operational entrances to the pipeline.

There is no bounded-ask constitutional-pipeline entrance. In particular, this is not a recognized QuestionFamily:

```text
seed ask --question-family "constitutional pipeline"
```

Bounded ask does not accept or forward the former six positional fields (`operator_inquiry`, `inquiry_provenance`, `bounded_question`, `constitutional_intent`, `scope_status`, and `selection_key`), does not select the `constitutional_pipeline` dispatch surface, and does not set `constitutional_pipeline=True`.

## API contract

A caller that already possesses a responsibly established `BoundedConstitutionalQuestion` can use:

```python
request = ConstitutionalPipelineRequest(bounded_question=question)
result = invoke_constitutional_pipeline(request)
```

The result continues to support JSON and human renderers and a provenance explanation. The diagnostic continues to report per-stage status, empty versus unsupported selection, Unknown and refusal counts, and read-only boundaries.

Exact selection keys currently demonstrated by the API are `process`, `governance`, and `fidelity`. Matching is exact; the pipeline does not infer a key from prose.

## Refusal examples

Both commands below refuse rather than originating a bounded question:

```bash
python scripts/seed_local.py --constitutional-pipeline \
  --operator-inquiry "operator testimony" \
  --inquiry-provenance operator:docs \
  --bounded-question "raw question" \
  --constitutional-intent "raw intent" \
  --scope-status bounded

python scripts/seed_local.py --constitutional-pipeline-diagnostic \
  --operator-inquiry "operator testimony" \
  --inquiry-provenance operator:docs \
  --bounded-question "raw question" \
  --constitutional-intent "raw intent" \
  --scope-status bounded
```

This absence does not authorize a compatibility adapter, JSON reconstruction, semantic routing, automatic admission, or another replacement entrance. The responsibility that will eventually establish a lawful bounded constitutional question remains unresolved.
