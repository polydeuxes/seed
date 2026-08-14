# Constitutional View Selection Slice 002

This slice implements exactly one implementation-local responsibility:
`ConstitutionalViewSelection`.

Repository authority wins.

## Implementation evidence

Implementation was limited to the recovered topology:

```text
Question Projection
        +
Capability Projection
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
```

The implementation is in `seed_runtime/constitutional_view_selection.py`.
It defines deterministic immutable projection input records, the single immutable
selection artifact, the exact-key selection function, a JSON helper for the
selection artifact, and one adapter from `SelectedConstitutionalViews` into the
existing `ConstitutionalViewCompositionRequest`.

The implementation does not consume raw questions. It does not consume immutable
constitutional views directly. It does not perform semantic reasoning, ranking,
heuristics, planning, orchestration, evidence discovery, constitutional recovery,
ownership recovery, implementation mutation, event-ledger writes, or cluster
mutation.

## Producer

Producer: `ConstitutionalViewSelection`.

Implementation producer function:

```text
select_constitutional_views(...)
```

The producer accepts only deterministic projection inputs:

- `ConstitutionalQuestionProjection`;
- `ConstitutionalCapabilityProjection` records.

## Immutable input artifacts

### Question Projection

`ConstitutionalQuestionProjection` preserves only:

- bounded-question identity;
- exact projected selection keys;
- existing projected uncertainty;
- read-only, event-ledger, and cluster-mutation boundary flags.

It does not carry a raw question.

### Capability Projection

`ConstitutionalCapabilityProjection` preserves only:

- registered view name;
- exact projected capability keys;
- compatibility answer;
- read-only, event-ledger, and cluster-mutation boundary flags.

It does not carry the immutable constitutional view artifact.

## Selection behavior

Selection performs only deterministic exact-key comparison:

- question projection keys are compared with capability projection keys;
- registered view names with exact overlap are selected;
- unsupported projected keys are preserved as selection uncertainty;
- an empty deterministic match preserves uncertainty instead of inventing a view;
- duplicate selected names are collapsed deterministically while preserving order.

No semantic matching, ranking, heuristics, planning, orchestration, evidence
discovery, constitutional recovery, ownership recovery, or authority creation was
introduced.

## Immutable output artifact

Output artifact: `SelectedConstitutionalViews`.

The artifact contains only:

- selected registered view names;
- preserved bounded-question identity;
- preserved selection uncertainty;
- read-only boundary flags;
- compatibility answer.

The artifact does not contain composed explanations, constitutional findings,
reasoning traces, implementation mutations, or authority claims.

## Consumer

Consumer: `ConstitutionalViewComposition`.

The adapter function is:

```text
selected_constitutional_views_to_composition_request(...)
```

It wires only the selected registered view names into the existing
`ConstitutionalViewCompositionRequest`, preserving the Composition contract.
Composition remains responsible for composing explicitly requested registered
views.

## Compatibility

Expected compatibility answer:

```text
No.
```

Selection returns `No.` when every selected capability projection reports `No.`.
Unsupported or empty deterministic selection preserves uncertainty and reports
`Unknown.` rather than inventing compatibility.

## Files changed

- `seed_runtime/constitutional_view_selection.py`
- `tests/test_constitutional_view_selection.py`
- `constitutional_view_selection_slice_002.md`

## LOC changed

Added 451 lines total:

- `seed_runtime/constitutional_view_selection.py`: 165 lines;
- `tests/test_constitutional_view_selection.py`: 128 lines;
- `constitutional_view_selection_slice_002.md`: 158 lines.

## Tests executed

- `pytest -q tests/test_constitutional_view_selection.py`

## Remaining work after Selection implementation

Remaining work is not architectural redesign of Selection. The implemented
boundary is complete for the recovered irreducible implementation-local ownership
responsibility.

Potential later work, if separately admitted by repository evidence, is limited
to producers that create deterministic Question Projection and Capability
Projection artifacts from their already-owned sources, plus any public CLI or
diagnostic exposure if such exposure is explicitly required. Such later work must
not move raw-question intake, immutable view construction, composition, semantic
reasoning, ranking, heuristics, planning, orchestration, evidence discovery,
constitutional recovery, or authority creation into Selection.
