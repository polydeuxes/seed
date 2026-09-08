# Constitutional View Capability Slice 001

This is exactly one implementation ownership audit. It determines whether repository evidence exposes one immediately adjacent implementation-local ownership boundary responsible only for describing the constitutional capability of each registered constitutional read model.

It does not implement the boundary, redesign `ConstitutionalViewSelection`, redesign `ConstitutionalViewComposition`, redesign registration, redesign CLI behavior, invent semantic reasoning, invent constitutional authority, recover more than one ownership boundary, perform runtime reasoning, discover evidence at runtime, mutate repository behavior, or create authority.

Repository authority wins.

## Investigation scope

Reviewed implementation evidence was limited to:

- `ConstitutionalReadModelContract`;
- `ReadModelViewRegistration`;
- Constitutional Process View;
- Constitutional Governance View;
- Constitutional Fidelity View;
- Constitutional View Composition;
- Constitutional View Selection Slice 001.

Expansion was limited to adjacent implementation evidence naturally required to confirm registered view fields, immutable artifacts, read-only boundaries, composition consumption, and the pre-existing `BoundedConstitutionalQuestion` recovery.

## Implementation evidence

### ConstitutionalReadModelContract

`ConstitutionalReadModelContract` records recurring implementation obligations shared by registered constitutional read-model views:

- name;
- CLI flag;
- builder;
- renderer;
- JSON renderer;
- diagnostic inventory name;
- diagnostic shape-audit name;
- read-only mutation boundary;
- JSON support;
- recording boundary;
- event-ledger boundary;
- cluster-mutation boundary.

It explicitly refuses to construct views, render output, dispatch CLI requests, register diagnostics, create constitutional authority, create implementation authority, or define future constitutional view contents.

The registered constitutional contracts are exactly:

- `constitutional_process`;
- `constitutional_governance`;
- `constitutional_fidelity`.

Every registered constitutional contract preserves `read_only=True`, `supports_json=True`, `supports_record=False`, `record_scope="none"`, `writes_event_ledger=False`, and `mutates_cluster=False`.

This evidence proves registered constitutional views expose implementation metadata, but the contract does not own a semantic capability description of constitutional questions each view may lawfully answer or topics intentionally outside that view's scope.

### ReadModelViewRegistration

`ReadModelViewRegistration` records an already-consumable read-model view by name, CLI flag, builder, renderer, and read-only boundary. It explicitly refuses read-model construction, output rendering, CLI dispatch, argument parsing, projection publication, ledger writes, cluster mutation, and constitutional-content declaration.

`constitutional_read_model_registration(contract)` consumes each `ConstitutionalReadModelContract` into the registration family. This proves existing registration can carry implementation entry points, but repository evidence does not show registration owning constitutional capability semantics.

### Constitutional Process View

The Constitutional Process View is an immutable read-only view over existing constitutional process evidence. It preserves `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`. It preserves process stages, evidence, Unknowns, and remaining candidate views.

Its builder name and artifact name imply process relevance to a human reader, and its staged content contains constitutional process material, but no separate immutable capability artifact states which constitutional questions it may lawfully contribute toward or which topics are outside its scope.

### Constitutional Governance View

The Constitutional Governance View is an immutable read-only view over existing constitutional governance evidence. It preserves `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`. It preserves governance relationships, evidence, Unknowns, explicit refusals, and remaining candidate views.

Its builder name and artifact name imply governance relevance to a human reader, and its relationships contain constitutional governance material, but no separate immutable capability artifact states which constitutional questions it may lawfully contribute toward or which topics are outside its scope.

### Constitutional Fidelity View

The Constitutional Fidelity View is an immutable read-only view over completed Constitutional Fidelity evidence. It preserves `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`. It preserves classifications, recurring constitutional discipline, Unknowns, explicit refusals, read-only boundaries, and remaining candidate views.

Its builder name and artifact name imply fidelity relevance to a human reader, and its classifications contain constitutional fidelity material, but no separate immutable capability artifact states which constitutional questions it may lawfully contribute toward or which topics are outside its scope.

### Constitutional View Composition

`ConstitutionalViewCompositionRequest` accepts `requested_views`, `composition_purpose`, and `output_format`. Its docstring states that the request owns only explicit registered-view selection, purpose labeling, and output-format intent, and does not select views heuristically, discover evidence, reason at runtime, recover authority, plan, orchestrate, or mutate repository state.

`build_constitutional_view_composition` composes only explicitly requested registered constitutional views. It validates requested names against `CONSTITUTIONAL_READ_MODEL_CONTRACTS` and the local builder map, builds those view artifacts, correlates their already-existing evidence, preserves their Unknowns and refusals, and returns one immutable `ConstitutionalViewCompositionArtifact`.

Composition therefore consumes selected registered view names after relevance has already been decided. It does not describe constitutional capability and does not determine which constitutional questions a registered view is capable of answering.

### Constitutional View Selection Slice 001

`constitutional_view_selection_slice_001.md` recovered `ConstitutionalViewSelection` as the pre-composition owner for selecting relevant registered constitutional views. The slice established that selection sits after bounded-question intake and registered constitutional view metadata, and before `ConstitutionalViewCompositionRequest`.

The slice says selection may only accept one bounded constitutional question, inspect registered constitutional view metadata, determine which already registered views are relevant, preserve unsupported selection uncertainty, and produce one immutable `SelectedConstitutionalViews` artifact. It must refuse constitutional recovery, ownership recovery, implementation recovery, evidence discovery, evidence invention, runtime reasoning, planning, orchestration, composition, repository mutation, and authority creation.

This evidence creates the present pressure: selection is expected to inspect registered constitutional view metadata, but current metadata does not expose the semantic capability description selection would need to deterministically know which constitutional questions a view may lawfully contribute toward.

### BoundedConstitutionalQuestion

`bounded_constitutional_question_slice_001.md` recovered `BoundedConstitutionalQuestion` as the immediately adjacent owner before `ConstitutionalViewSelection`. It produces a bounded constitutional question from an admitted operator constitutional inquiry without selecting views, composing views, discovering evidence, or creating authority.

That recovered boundary remains preserved. The present pressure is after `BoundedConstitutionalQuestion` and before `ConstitutionalViewSelection` can make a deterministic registered-view relevance decision.

## Current ownership

### 1. Who presently owns the capability description of a registered constitutional view?

No implementation-local component presently owns the capability description of a registered constitutional view.

Repository evidence shows ownership of adjacent responsibilities only:

- `ConstitutionalReadModelContract` owns recurring implementation obligations and metadata;
- `ReadModelViewRegistration` owns consumable registration metadata;
- each constitutional view owns its own immutable read-only artifact and rendered/json output;
- `BoundedConstitutionalQuestion` owns the bounded question before selection;
- `ConstitutionalViewSelection` owns a future relevance selection responsibility;
- `ConstitutionalViewComposition` owns composition of explicitly requested registered views.

None of those boundaries owns a one-view semantic capability description that says which constitutional questions the registered view may lawfully contribute toward, which topics are intentionally outside scope, and when capability remains Unknown.

### 2. Is capability currently compressed into implementation metadata?

Yes.

The closest current machine-inspectable metadata is the registered contract and registration fields: `name`, `cli_flag`, `builder`, `renderer`, `json_renderer`, `inventory_name`, and `shape_audit_name`. Those fields identify implementation entry points and operational visibility names, not constitutional question capability.

A future selector could inspect those strings, but doing so would compress semantic capability into implementation metadata that currently refuses to define future constitutional view contents.

### 3. Is capability currently compressed into builder naming?

Yes.

Names such as `build_constitutional_process_view`, `build_constitutional_governance_view`, and `build_constitutional_fidelity_view` imply broad topic areas to a human reader. Repository evidence does not show those names as lawful capability artifacts, question scopes, or out-of-scope declarations.

Using builder names to decide relevance would compress constitutional capability into naming conventions rather than into an implementation-local capability owner.

### 4. Is capability currently compressed into prompt knowledge?

Yes, for prompt-driven or operator-driven use.

When an operator or future caller asks a bounded constitutional question, the repository currently has no capability artifact between a bounded question and selection. Therefore the caller, prompt, or operator must know that process questions should likely include the process view, governance questions should likely include the governance view, fidelity questions should likely include the fidelity view, or that unsupported relevance should remain Unknown.

That prompt knowledge is not repository-owned implementation evidence.

### 5. Does repository evidence expose one immediately adjacent implementation-local ownership boundary?

Yes.

Repository evidence exposes exactly one immediately adjacent implementation-local ownership boundary: **ConstitutionalViewCapability**.

The boundary is adjacent because it sits after one registered constitutional view is known and before `ConstitutionalViewSelection` determines relevance for one `BoundedConstitutionalQuestion`. It does not replace the existing contract, registration, view builders, view artifacts, CLI behavior, JSON output, human rendering, diagnostic inventory, diagnostic shape audit, selection, composition, or compatibility behavior.

## Selected ownership boundary

Selected boundary: `ConstitutionalViewCapability`.

Repository evidence selects this boundary because the implemented and recovered system already has:

1. registered constitutional view metadata;
2. immutable read-only constitutional view producers and artifacts;
3. a recovered bounded constitutional question boundary before selection;
4. a recovered selection boundary that must inspect registered constitutional view metadata and determine relevance;
5. an implemented composition boundary that consumes explicitly requested registered view names after selection;
6. no implementation-local owner for the semantic capability of one registered constitutional read model.

The missing responsibility is not selection, composition, another registration layer, another read-model contract, a redesigned view, a CLI redesign, a planner, an orchestrator, the Eye, runtime reasoning, evidence discovery, or authority creation. It is the narrower description of what one registered constitutional view is capable of lawfully contributing toward.

## Before

Before this audit:

```text
Registered Constitutional View
        ↓
Implementation metadata, builder names, prompt/operator knowledge
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
```

Capability was not owned by a repository artifact. It was compressed into implementation metadata, builder naming, and prompt/operator knowledge.

## After

After this audit, no code behavior changes. The recovered implementation-local boundary for a possible later slice is:

```text
Registered Constitutional View
        ↓
ConstitutionalViewCapability
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
```

This is an ownership recovery only. `ConstitutionalViewCapability` is not implemented here.

## Recovered producer

Recovered producer: `ConstitutionalViewCapability` production for one registered constitutional view.

If implemented later, the producer may only:

- consume one already registered constitutional read-model view identity and its existing implementation-local registration metadata;
- describe that view's constitutional scope;
- describe the constitutional questions that view may lawfully contribute toward;
- describe constitutional topics intentionally outside that view's scope;
- preserve Unknown capability where unsupported;
- produce one immutable capability artifact.

The producer must explicitly refuse:

- constitutional recovery;
- ownership recovery;
- implementation recovery;
- evidence discovery;
- evidence invention;
- view selection;
- composition;
- planning;
- orchestration;
- runtime reasoning;
- repository mutation;
- authority creation.

## Recovered artifact/helper

Recovered artifact/helper: `ConstitutionalViewCapability`.

If implemented later, the artifact should preserve only one registered view's capability description, such as:

- registered view name;
- registered CLI flag or stable registration identity;
- constitutional scope label for that view;
- supported bounded constitutional question families or patterns where repository evidence supports them;
- intentionally out-of-scope constitutional topics;
- Unknown capability notes where support is insufficient;
- read-only and non-mutating boundary flags.

It should not contain selected view sets, composed view artifacts, constitutional findings, newly discovered evidence, recovered evidence, reasoning traces, plans, orchestration state, implementation mutations, repository mutations, or authority claims.

## Recovered consumer

Recovered consumer: `ConstitutionalViewSelection`.

The recovered selection boundary can consume capability artifacts because `constitutional_view_selection_slice_001.md` already requires selection to inspect registered constitutional view metadata and determine which already registered views are relevant. Capability would provide the missing repository-owned semantic description without making selection own capability description, without making composition own selection, and without making registration own constitutional semantics.

## Relationship to ConstitutionalViewSelection

Repository evidence supports this relationship:

```text
Registered Constitutional View
        ↓
ConstitutionalViewCapability
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
```

The reason is implementation-local:

- registered constitutional views already exist;
- registered constitutional contracts expose implementation entry points and operational visibility metadata;
- existing view artifacts expose bounded read-only content, Unknowns, refusals, and compatibility answers;
- `BoundedConstitutionalQuestion` is already recovered as the adjacent pre-selection question boundary;
- `ConstitutionalViewSelection` is already recovered as the pre-composition relevance boundary;
- selection is expected to inspect registered constitutional view metadata, but current metadata lacks a repository-owned semantic capability description;
- `ConstitutionalViewComposition` already consumes explicit registered view names and refuses heuristic selection.

Therefore capability is a pre-selection description responsibility, selection remains a relevance decision responsibility, and composition remains a post-selection composition responsibility.

## Compatibility

Expected compatibility answer:

```text
No.
```

Compatibility is preserved because this slice changes only one audit document and does not modify:

- `ConstitutionalReadModelContract`;
- `ReadModelViewRegistration`;
- Constitutional Process View;
- Constitutional Governance View;
- Constitutional Fidelity View;
- Constitutional View Composition;
- Constitutional View Selection;
- `BoundedConstitutionalQuestion`;
- CLI behavior;
- JSON output;
- human rendering;
- diagnostic inventory;
- diagnostic shape audit;
- compatibility.

No diagnostic, audit, probe, view, operational CLI flag, or recordable output is added or modified. No runtime behavior changes. No JSON shape changes. No human rendering changes. No diagnostic registry or diagnostic shape-audit implementation change is required.

## Files changed

- `constitutional_view_capability_slice_001.md`

## LOC changed

- Added: 335 lines
- Modified: 0 existing lines
- Deleted: 0 lines

## Tests executed

- `python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining work before bounded constitutional attention

Before bounded constitutional attention can deterministically select constitutional views from an operator constitutional question, later slices would still need to:

1. implement `BoundedConstitutionalQuestion` without expanding its authority;
2. implement `ConstitutionalViewCapability` as an immutable per-registered-view capability artifact without expanding registration, view, selection, or composition ownership;
3. prove unsupported capability remains Unknown instead of becoming prompt knowledge or invented authority;
4. implement `ConstitutionalViewSelection` so it consumes a bounded constitutional question and registered capability artifacts;
5. define an immutable `SelectedConstitutionalViews` artifact or equivalent helper;
6. prove selected view names can feed existing `ConstitutionalViewComposition` without changing composition ownership;
7. preserve CLI behavior, JSON output, human rendering, diagnostic inventory, diagnostic shape audit, and compatibility.

## Audit conclusion

This slice identifies exactly one immediately adjacent implementation-local ownership boundary responsible only for describing the constitutional capability of each registered constitutional read model: `ConstitutionalViewCapability`.

It preserves all existing implementation contracts and compatibility, separates capability description from selection and composition, introduces no new authority, performs no runtime reasoning, and provides the missing implementation evidence needed for future deterministic constitutional view selection.
