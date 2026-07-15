# Shared Explanation Rendering Projection Slice 001

## Recovered responsibility

This slice recovers one bounded shared responsibility: render exactly one already-produced stage-local explanation through a read-only display projection. The projection copies recurring presentation fields and carries stage-owned material without interpreting, normalizing, comparing, reclassifying, replacing, authorizing, composing, writing events, or mutating cluster state.

## Source explanation artifacts

Supported source artifacts are:

- `MinimumLawfulAdvancementExplanation`, owned by the ingress authority/scope binding stage.
- `RepresentationGrammarApplicabilityAdvancementExplanation`, owned by the representation grammar applicability stage.

The shared projection is not a universal explanation artifact, shared decision artifact, global manager, base decision class, state normalizer, blocker registry, failure router, recovery planner, or composition manager.

## Producer and output projection

The shared producer is `SharedExplanationRenderingProjection`. Its output artifact is `SharedExplanationRenderingProjection`, a read-only rendering projection whose convention is `shared_explanation_rendering_projection_v1`.

The projection identifies:

- `source_explanation_identity`
- `source_artifact_owner`
- `source_explanation_type`
- the shared rendering `producer`

These identifiers support display. They do not transfer ownership from the source stage.

## Recurring presentation fields

The smallest recovered recurring display fields are:

- `source_explanation_identity`
- `source_artifact_owner`
- `source_explanation_type`
- `producer`
- `attempted_movement`
- `source_state`
- `source_reason`
- `preserved_unknowns`
- `preserved_conflicts`
- `prohibited_downstream_movement`
- `explanation_boundary`
- `single_explanation_boundary`
- `rendering_boundary`
- `read_only`
- `writes_event_ledger`
- `mutates_cluster`
- `stage_owned_material`

Shared field names are presentation labels only. They are not shared constitutional meanings.

## Stage-owned material treatment

Stage-specific fields are carried inside `stage_owned_material` with source-authored names and values. The shared producer does not derive conclusions from this section.

For ingress explanations, the carried stage-owned fields are:

- `established`
- `first_missing_boundary`
- `movement_blocked`
- `authority_resolvable`
- `reconsideration_transition`

For grammar-applicability explanations, the carried stage-owned fields are:

- `examined_grammar`
- `examined_demand`
- `examined_mechanism`
- `examined_contract`
- `established_applicability_evidence`
- `next_handoff_boundary`
- `handoff_permitted`
- `authority_treatment`
- `reconsideration_evidence`
- `known_loss`
- `provenance`
- `compatibility_boundary_changed`

## Ingress proving result

The ingress proving case projects one `MinimumLawfulAdvancementExplanation` into one shared rendering projection. The test proves that the projection preserves:

- source explanation identity;
- source artifact owner;
- verbatim `blocked` state;
- source reason;
- Unknowns;
- conflicts;
- prohibited downstream movement;
- `first_missing_boundary` as ingress-owned material;
- `authority_resolvable` as ingress-owned material;
- read-only, event-ledger, and cluster-mutation guarantees.

The shared projection does not reinterpret `authority_resolvable` or `first_missing_boundary`.

## Grammar-applicability proving result

The grammar-applicability proving case projects one `RepresentationGrammarApplicabilityAdvancementExplanation` into one shared rendering projection. The test proves that the projection preserves:

- source explanation identity;
- source artifact owner;
- verbatim `not_applicable` state;
- source reason;
- Unknowns;
- conflicts;
- prohibited downstream movement;
- `handoff_permitted` as grammar-owned material;
- `authority_treatment` as grammar-owned material;
- established applicability evidence;
- read-only, event-ledger, and cluster-mutation guarantees.

The shared projection does not reinterpret `handoff_permitted` or `authority_treatment`.

## State and authority distinctions

The state distinction test proves that `blocked` and `not_applicable` remain verbatim stage-owned states. The shared projection does not map either state into a generic blocker state.

The authority distinction test proves that a grammar-applicability explanation with authority treatment does not gain an ingress-owned `authority_resolvable` field. Absence of authority relevance in grammar applicability is therefore not rendered as `authority_resolvable = false`.

## Human and JSON rendering

Human rendering is provided by `format_shared_explanation_rendering(...)`.

JSON rendering is provided by `shared_explanation_rendering_json(...)`.

Both renderings expose the same copied presentation fields and the same stage-owned material. JSON recursively converts tuple values to arrays for stable data output; human output lists repeated values without changing their source-authored content.

## Single-explanation boundary

The projection consumes exactly one known stage-local explanation. A collection of explanations is rejected. The projection does not compare, aggregate, order, compose, select among, or arrange several explanations.

## Read-only guarantees

The projection preserves source read-only guarantees:

- `read_only = true`
- `writes_event_ledger = false`
- `mutates_cluster = false`

It does not write events or mutate cluster State.

## Compatibility answer

Did this slice change any existing compatibility boundary?

No.

The grammar-applicability source field `compatibility_boundary_changed` is only displayed inside stage-owned material when present. The shared projection does not change that value or derive compatibility meaning from it.

## Files changed

- `seed_runtime/shared_explanation_rendering_projection.py`
- `tests/test_shared_explanation_rendering_projection.py`
- `shared_explanation_rendering_projection_slice_001.md`

## Tests executed

- `pytest -q tests/test_shared_explanation_rendering_projection.py tests/test_operator_authority_scope_binding.py tests/test_representation_grammar_applicability.py`

## Remaining boundaries

This slice does not create a composition owner. It does not decide precedence, arrange multiple projections, compare states, authorize movement, create handoffs, modify source producers, modify REPL or CLI routing, write events, mutate cluster State, or alter existing compatibility boundaries.

## Exact next bounded question

Given several independently produced
shared explanation rendering projections,

what smallest bounded composition owner,
if any,

may select and arrange them
for one constitutional inquiry

without comparing states,
inventing blocker precedence,
or transferring decision ownership
away from their source stages?
