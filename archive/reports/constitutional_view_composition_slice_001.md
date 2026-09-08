# Constitutional View Composition Slice 001

This is exactly one implementation ownership audit. It determines whether repository evidence exposes one immediately adjacent implementation-local ownership boundary for composing multiple already registered constitutional read models into one bounded read-only constitutional explanation.

It does not implement constitutional composition, the Eye, orchestration, read-model redesign, registration redesign, CLI redesign, an explanation engine, runtime planning, constitutional authority, or more than one ownership boundary.

Repository authority wins.

## Implementation evidence

### Evidence reviewed

Reviewed implementation-local evidence only:

- `seed_runtime/read_model_ownership.py`
- `seed_runtime/constitutional_process_view.py`
- `seed_runtime/constitutional_governance_view.py`
- `seed_runtime/constitutional_fidelity_view.py`
- `constitutional_view_composition_investigation.md`
- adjacent CLI dispatch references in `scripts/seed_local.py` where the registered constitutional views are consumed
- adjacent diagnostic declarations in `seed_runtime/diagnostic_inventory.py` and `seed_runtime/diagnostic_shape_audit.py`
- adjacent tests proving registration, CLI exposure, JSON rendering, human rendering, diagnostic inventory, and diagnostic shape audit participation

Commands used through the app:

```bash
python scripts/seed_local.py --constitutional-process --json
python scripts/seed_local.py --constitutional-governance --json
python scripts/seed_local.py --constitutional-fidelity --json
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --diagnostic-shape-audit --json
pytest -q tests/test_constitutional_process_view.py tests/test_constitutional_governance_view.py tests/test_constitutional_fidelity_view.py tests/test_read_model_ownership.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

### Contract and registration evidence

`ConstitutionalReadModelContract` records the recurring implementation obligations already shared by the constitutional read models: name, CLI flag, builder, renderer, JSON renderer, diagnostic inventory name, shape-audit name, read-only behavior, JSON support, no recording, `record_scope="none"`, no event-ledger writes, and no cluster mutation.

The contract explicitly refuses to construct views, render output, dispatch CLI requests, register diagnostics, create constitutional authority, create implementation authority, or define future constitutional view contents.

`CONSTITUTIONAL_READ_MODEL_CONTRACTS` currently registers exactly these constitutional read-model contracts:

| Contract | CLI flag | Builder | Renderer | JSON renderer | Inventory | Shape audit |
| --- | --- | --- | --- | --- | --- | --- |
| `constitutional_process` | `--constitutional-process` | `build_constitutional_process_view` | `format_constitutional_process_view` | `constitutional_process_view_json` | `constitutional_process` | `constitutional_process` |
| `constitutional_governance` | `--constitutional-governance` | `build_constitutional_governance_view` | `format_constitutional_governance_view` | `constitutional_governance_view_json` | `constitutional_governance` | `constitutional_governance` |
| `constitutional_fidelity` | `--constitutional-fidelity` | `build_constitutional_fidelity_view` | `format_constitutional_fidelity_view` | `constitutional_fidelity_view_json` | `constitutional_fidelity` | `constitutional_fidelity` |

`constitutional_read_model_registration(contract)` converts each constitutional contract into the existing `ReadModelViewRegistration` shape.

`ReadModelViewRegistration` records an existing CLI flag, builder, renderer, and read-only boundary for a consumable read-model view. It explicitly refuses read-model construction, output rendering, CLI dispatch, argument parsing, projection publication, ledger writes, cluster mutation, and constitutional-content declaration.

### Constitutional Process View evidence

The Constitutional Process View is an implemented read-only constitutional read model. It builds a bounded `ConstitutionalProcessView` from existing process evidence, has `compatibility_answer="No."`, has `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`, preserves process Unknowns, serializes deterministically through `constitutional_process_view_json`, and renders through `format_constitutional_process_view`.

The view does not expose a dedicated explicit-refusals field, but its read-only flags, lawful-stop language, compatibility answer, implementation contract, and preserved Unknowns refuse conversion into a runtime sequence, command authority, mutation path, or new constitutional owner.

### Constitutional Governance View evidence

The Constitutional Governance View is an implemented read-only constitutional read model. It builds a bounded `ConstitutionalGovernanceView` from existing governance evidence, has `compatibility_answer="No."`, has `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`, preserves governance Unknowns, preserves explicit refusals, serializes deterministically through `constitutional_governance_view_json`, and renders through `format_constitutional_governance_view`.

Its explicit refusals include governance execution, governance ownership, constitutional recovery, implementation recovery, hierarchy, runtime governance, and repository mutation.

### Constitutional Fidelity View evidence

The Constitutional Fidelity View is an implemented read-only constitutional read model. It builds a bounded `ConstitutionalFidelityView` from completed fidelity evidence, has `compatibility_answer="No."`, has `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`, preserves fidelity Unknowns, preserves explicit refusals, preserves read-only boundaries, serializes deterministically through `constitutional_fidelity_view_json`, and renders through `format_constitutional_fidelity_view`.

Its explicit refusals include constitutional recovery, implementation recovery, ownership recovery, implementation mutation, repository mutation, runtime evaluation, fidelity enforcement, architectural redesign, and projection recovery.

### Constitutional View Composition Investigation evidence

The prior investigation concluded:

```text
Ready for constitutional view composition
```

It also established that lawful composition creates no constitutional authority, creates no implementation authority, consumes only existing read-only constitutional evidence, preserves every contributing view's explicit refusals, preserves every contributing view's Unknowns, replaces nothing, and may only produce a bounded explanation over multiple already recovered constitutional read models.

## Current ownership

### 1. Who presently owns constitutional view composition?

No implemented repository component currently owns constitutional view composition.

The existing owners stop earlier:

- each constitutional view owns only its own bounded read-only view construction, serialization, and human rendering;
- `ConstitutionalReadModelContract` owns only the implementation-local obligations shared by constitutional read-model views;
- `ReadModelViewRegistration` owns only consumable registration metadata;
- CLI dispatch owns only selecting one requested flag, building that one view, and printing JSON or human output.

Therefore constitutional view composition is presently external to the repository implementation.

### 2. Is composition currently compressed into CLI dispatch?

No.

CLI dispatch contains separate branches for `--constitutional-process`, `--constitutional-governance`, and `--constitutional-fidelity`. Each branch builds and prints one view. There is no CLI branch that selects multiple registered constitutional views, consumes their immutable artifacts together, preserves all refusals and Unknowns together, or produces one composed constitutional explanation.

The CLI is adjacent to future composition because it already consumes the views, but repository evidence does not show composition compressed into CLI dispatch today.

### 3. Is composition currently compressed into the operator?

Yes.

Today, any multi-view constitutional explanation is performed outside the implementation by the operator or Codex by running the separate view commands and correlating the outputs manually. That is compression into the operator, not an implementation-local owner.

### 4. Is composition currently compressed into future consumers?

Yes.

Because the repository exposes independent registered views but no bounded composition owner, any future consumer that needs one combined explanation must select multiple constitutional views, correlate their outputs, preserve Unknowns, preserve explicit refusals, and prevent authority creation on its own. That leaves composition responsibilities compressed into future consumers unless a later implementation slice adds the recovered boundary.

### 5. Does repository evidence expose one immediately adjacent implementation-local ownership boundary?

Yes.

Repository evidence exposes exactly one immediately adjacent implementation-local boundary: **ConstitutionalViewComposition**.

The selected boundary is adjacent because it would sit after `ReadModelViewRegistration` and the three implemented constitutional view builders/renderers, and before any future CLI surface, orchestration, Eye, external operator, or consumer. It would consume already registered constitutional read models and their immutable artifacts without changing registration, view construction, JSON shapes, human rendering, diagnostic inventory, diagnostic shape audit, or compatibility.

## Selected ownership boundary

Selected boundary: `ConstitutionalViewComposition`.

Repository evidence selects this boundary because the existing implementation already separates:

1. constitutional read-model contracts (`ConstitutionalReadModelContract`);
2. consumable view registration (`ReadModelViewRegistration`);
3. independent view construction and rendering (`Constitutional Process View`, `Constitutional Governance View`, `Constitutional Fidelity View`);
4. per-flag CLI dispatch;
5. diagnostic inventory and shape-audit visibility.

The missing adjacent responsibility is not another view contract, not another registration, not CLI redesign, not orchestration, and not a runtime planner. It is the bounded implementation-local act of composing multiple registered constitutional views into one read-only explanation artifact.

## Before

Before this audit:

- constitutional views were independently implemented and registered;
- each view could be rendered as JSON or human text;
- diagnostic inventory and diagnostic shape audit knew about each view independently;
- the composition investigation established readiness for composition;
- there was no repository owner for selecting multiple constitutional views and producing one bounded composed explanation;
- operators or future consumers had to perform that correlation externally.

## After

After this audit:

- no code behavior changes;
- no constitutional composition implementation exists;
- no new CLI flag exists;
- no JSON shape changes;
- no human rendering changes;
- no diagnostic inventory changes;
- no diagnostic shape-audit changes;
- no compatibility changes;
- exactly one implementation-local ownership boundary is recovered for a later slice: `ConstitutionalViewComposition`.

## Recovered producer

Recovered producer: `compose_constitutional_views`.

This is not implemented in this slice.

If implemented later, the producer may only accept already registered constitutional view selections and immutable artifacts from existing constitutional read models, then produce one bounded composed artifact. It must not construct constitutional authority, recover ownership, mutate implementation, mutate the repository, run orchestration, perform runtime reasoning, or invent evidence.

## Recovered artifact/helper

Recovered artifact/helper: `ComposedConstitutionalExplanation`.

This is not implemented in this slice.

If implemented later, the artifact may contain only bounded composition results over existing read-only evidence, including:

- contributing registered view names;
- contributing immutable artifacts;
- correlated existing evidence references;
- preserved Unknowns from every contributing view;
- preserved explicit refusals from every contributing view;
- compatibility answer `No.`;
- read-only status;
- `writes_event_ledger=False`;
- `mutates_cluster=False`.

## Recovered consumer

Recovered consumer: a future explicit composition surface or future caller that requests one bounded composed constitutional explanation.

This consumer is not implemented in this slice.

The existing per-view CLI branches are preserved and do not become composition consumers in this slice. A later consumer may consume `ConstitutionalViewComposition` only if it preserves the same read-only, non-authoritative, non-mutating boundary and participates in diagnostic inventory and diagnostic shape audit if exposed as a diagnostic surface.

## Boundary

`ConstitutionalViewComposition` may only:

- select already registered constitutional views;
- consume their immutable artifacts;
- correlate existing repository evidence;
- preserve explicit refusals;
- preserve Unknowns;
- produce one bounded composed artifact.

`ConstitutionalViewComposition` must explicitly refuse:

- constitutional recovery;
- ownership recovery;
- implementation recovery;
- runtime reasoning;
- evidence invention;
- Unknown resolution;
- authority creation;
- implementation mutation;
- repository mutation.

The boundary creates no constitutional authority and no implementation authority. It replaces no contributing view.

## Compatibility

Expected compatibility answer:

```text
No.
```

Compatibility is preserved because this audit changes no implementation behavior. It preserves:

- `ConstitutionalReadModelContract`;
- `ReadModelViewRegistration`;
- Constitutional Process View;
- Constitutional Governance View;
- Constitutional Fidelity View;
- CLI behavior;
- JSON output;
- human rendering;
- diagnostic inventory;
- diagnostic shape audit;
- compatibility.

## Files changed

- `constitutional_view_composition_slice_001.md`

## LOC changed

- Added: 275 lines
- Deleted: 0 lines
- Net: +275 lines

## Tests executed

```bash
python scripts/seed_local.py --constitutional-process --json
python scripts/seed_local.py --constitutional-governance --json
python scripts/seed_local.py --constitutional-fidelity --json
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --diagnostic-shape-audit --json
pytest -q tests/test_constitutional_process_view.py tests/test_constitutional_governance_view.py tests/test_constitutional_fidelity_view.py tests/test_read_model_ownership.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed responsibilities

Remaining compression after this audit:

- composition remains compressed into the operator until a later implementation slice implements `ConstitutionalViewComposition`;
- composition remains compressed into future consumers that need one composed explanation until that later slice exists;
- CLI dispatch remains intentionally per-view and does not compose;
- diagnostic inventory and diagnostic shape audit remain intentionally per existing surface and have no composition surface to inventory yet;
- the actual implementation of constitutional composition remains for a later slice.

Constitutional View Composition Slice 001 complete.
