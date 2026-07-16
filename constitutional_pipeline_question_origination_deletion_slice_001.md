# Constitutional Pipeline Question Origination Deletion Slice 001

This slice removes raw bounded-question origination from `ConstitutionalPipelineRequest` and `invoke_constitutional_pipeline(...)`.

The pipeline now consumes exactly one already-established `BoundedConstitutionalQuestion` and owns only downstream projection, capability projection, view selection, view composition, provenance explanation, and rendering.

Removed from the pipeline request shape:

- `operator_inquiry`
- `inquiry_provenance`
- `bounded_question` as raw text
- `constitutional_intent`
- `scope_status`
- `uncertainty`
- `unknowns`
- `bounded_question_id`
- `caller_supplied_fields`

The invocation no longer imports or calls `produce_bounded_constitutional_question(...)`. Existing raw CLI pipeline and pipeline-diagnostic ingress now refuses instead of minting a canonical question from caller-supplied fields.

Read-only boundaries remain preserved: no event-ledger writes and no cluster mutation are performed by the pipeline, diagnostic helper, provenance explanation, JSON rendering, or human rendering.
