# Constitutional View Composition package-standing repair 001

## Book grammar consumed

This repair consumes `06.Projection.B — Purpose-relative lossless projection and package standing`. The governing grammar says that a projection, view, package, set, or handoff is lossless only for a declared bounded consumer purpose, and only when the responsible formation preserves the distinctions the consumer needs without inventing missing standing or strengthening upstream claims. It specifically keeps empty contents, unavailable input, incomplete input, Unknown input, no testimony, negative testimony, contents, cardinality, and aggregate judgment distinct unless a local warranted rule intentionally relates them.

## 1832 consumer witness consumed

The local consumer road is implemented by `ConstitutionalViewCompositionRequest`, `build_constitutional_view_composition(...)`, `ConstitutionalViewCompositionArtifact`, `constitutional_view_composition_json(...)`, and `format_constitutional_view_composition(...)`. Downstream pipeline rendering and diagnostics transport the composition artifact's scalar compatibility answer, but they do not independently form compatibility testimony for Constitutional View Composition.

The artifact and renderers require a scalar string because `compatibility_answer` is a dataclass field and the JSON and human renderers expose that field. The same consumers also preserve separate standing through requested view identity, contributing view count, preserved Unknowns, preserved refusals, read-only boundaries, and mutation flags. No recovered consumer requires a new package object or a new public JSON/human shape.

## 1834 crossing consumed

The survey witness established this local crossing:

```text
empty compatibility contribution package
→ Python all([])
→ compatibility_answer = "No."
```

The crossing was bounded to the scalar aggregate. It did not prove that view construction, artifact existence, contributing-view evidence, Unknown preservation, refusal preservation, JSON shape, or read-only boundaries were globally unfaithful.

## Local formation responsibility

`build_constitutional_view_composition(...)` owns local formation. It validates every requested name against registered constitutional read-model contracts and the local builder map, refuses unsupported requested identities before building, invokes each requested builder and JSON renderer, appends one `ConstitutionalContributingView` per successfully built requested view, carries evidence/Unknown/refusal material from the payload, and appends one compatibility answer per rendered payload.

The request itself does not form testimony. The JSON and human renderers do not form testimony. Downstream diagnostics transport or classify the already-formed artifact; they do not own the aggregate claim.

## Compatibility contribution definition

One compatibility contribution is one compatibility-answer slot produced during the local loop for one successfully built requested registered view. If the rendered payload has `compatibility_answer`, that value is the contribution's contents. If the rendered payload lacks the key, the local builder records a conservative `Unknown.` value for that built view. Therefore a successfully built view can lack explicit compatibility testimony, and the local default `Unknown.` counts as a formed contribution whose content is Unknown rather than No.

Distinctions recovered:

- `requested_views = ()` means the caller requested no registered view identities for this composition. It is not a failed build and not unsupported identity.
- `contributing_views = ()` means no requested view was successfully built into a contributing view for the artifact. In the reachable empty request path this follows from no requested identities.
- `compatibility_answers = []` means the local compatibility contribution package is empty. It carries known cardinality zero and no compatibility testimony.
- `compatibility_answer = "No."` claims that the bounded composition's formed compatibility contributions are populated and every formed contribution answered `No.`.
- Authority for `compatibility_answer = "No."` belongs only to `build_constitutional_view_composition(...)` at the aggregate boundary, after local request validation and contribution formation.
- The required testimony for `No.` is at least one formed compatibility contribution and every formed compatibility contribution content equal to `No.`.

## Package standing recovered

The boundary does not need a named package object. Existing local standing is sufficient:

- requested identities are preserved in `artifact.request.requested_views`;
- successful formation is preserved in `artifact.contributing_views`;
- compatibility contribution cardinality is represented locally by the length of `compatibility_answers` during aggregation and externally by contributing-view cardinality for supported current builders;
- Unknown payloads are preserved in `artifact.preserved_unknowns` and by scalar `Unknown.`;
- explicit refusals are preserved in `artifact.preserved_refusals`;
- unsupported requested identities are refused by `ValueError` before artifact formation;
- read-only, event-ledger, and mutation boundaries are preserved as artifact fields.

No evidence required preserving package unavailable, incomplete, refused, or cardinality-Unknown states as new fields for this local repair. Unsupported requested identities remain refusal before artifact formation, not Unknown compatibility.

## Aggregation question recovered

The scalar answers this bounded aggregation question:

```text
Did this composition form one or more compatibility contributions, and did every formed contribution answer No.?
```

Recovered local rules:

- Populated package, all `No.`: aggregate `No.`.
- Populated package, at least one `Unknown.`: aggregate `Unknown.`.
- Populated package, mixed testimony including any non-`No.`: aggregate `Unknown.` under current implementation evidence.
- Empty package: aggregate `Unknown.` because no negative compatibility testimony was formed.
- Unavailable or incomplete package: not independently evidenced as a separate artifact state in this boundary; remaining standing is Unknown unless later implementation evidence creates a distinct local state.

The scalar does not answer whether the composed views establish constitutional truth, whether composition was sufficient for every external purpose, whether the repository has no compatibility, or whether artifact existence by itself establishes incompatibility.

## Consumer reliance

`ConstitutionalViewCompositionArtifact` stores a scalar string and separate contribution/evidence/Unknown/refusal/boundary fields. `constitutional_view_composition_json(...)` serializes the artifact shape without interpreting compatibility. `format_constitutional_view_composition(...)` renders the scalar and the preserved fields. Direct tests inspect the scalar, contributing views, Unknowns, refusals, read-only boundaries, and mutation fields. Pipeline diagnostics and rendering transport the composition scalar and can classify `Unknown.` as unknown without requiring `No.` for empty composition.

Changing empty-package scalar standing from `No.` to `Unknown.` preserves shape and prevents empty cardinality from being rendered as negative testimony. Populated all-negative output remains `No.`, so existing lawful populated compositions remain compatible.

## Established Fidelity crossing

Constitutional grammar requires no compatibility testimony and negative compatibility testimony to remain distinct for this consumer-visible claim. The implementation witness was the unguarded `all(answer == "No." for answer in compatibility_answers)`: empty package and populated all-negative package both produced `No.`. This was an unfaithful crossing only in the scalar aggregate because it let an empty realization borrow the standing of populated all-negative testimony.

## Lawful empty-package outcome

The lawful empty-package scalar outcome is `Unknown.`. The artifact may still exist as a composition artifact with no requested views, no contributing views, no correlated evidence, and read-only boundaries. Artifact existence is not evidence that compatibility was negatively established.

## Implementation boundary selected by repository evidence

The smallest faithful boundary is the local aggregate assertion inside `build_constitutional_view_composition(...)`. The repair adds a non-empty contribution guard before the all-negative aggregate can produce `No.`. It does not force upstream producers to manufacture testimony, does not add artifact fields, and does not alter JSON or human shape.

## Before / after standing

Before:

```text
compatibility_answers = []
all([]) = True
compatibility_answer = "No."
```

After:

```text
compatibility_answers = []
compatibility_answers and all(...) = falsey
compatibility_answer = "Unknown."
```

Populated all-negative packages still produce `No.`. Populated Unknown or mixed packages still produce `Unknown.`.

## Compatibility preservation

Preserved behavior:

- existing contributing-view evidence remains unchanged;
- Unknown payloads remain preserved;
- explicit refusals remain preserved;
- unsupported requested views still refuse composition;
- JSON and human rendering shape remains unchanged;
- read-only remains true;
- writes-event-ledger remains false;
- mutates-cluster remains false;
- populated all-`No.` compositions still answer `No.`.

## Tests

Focused tests prove empty requested views produce `Unknown.` rather than `No.`, JSON and human rendering preserve that repaired standing, populated all-`No.` contributions still produce `No.`, a formed contribution with missing compatibility testimony defaults to `Unknown.`, contributing evidence/Unknown/refusal boundaries remain preserved, unsupported requested views still refuse, and read-only/event-ledger/mutation boundaries remain unchanged.

## Negative authority

This repair does not create `UniversalPackage`, `PackageStatus`, `AggregateResult`, `CompatibilityPackage`, a shared aggregation framework, a repository-wide truthiness helper, or a universal rule for empty collections. It does not copy Constitutional View Selection. It does not repair unrelated defaults, cache misses, JSON omissions, subprocess boundaries, or other `all(...)` calls. It does not add another Book clause because `06.Projection.B` already governs the recovered distinction.

## Required distinctions

- No requested contributions are not failed contribution construction.
- Failed construction is not evidenced as a successful artifact state at this boundary.
- Unsupported requested identity is a pre-artifact refusal by validation, not Unknown compatibility.
- Unknown compatibility is a formed conservative contribution content or aggregate non-negative result, not negative compatibility.
- Negative compatibility requires populated formed testimony whose every compatibility answer is `No.`.

## Remaining Unknowns

It remains Unknown whether future requested registered views can fail after validation and before contribution formation in a way that should produce a separate incomplete or unavailable package standing. It remains Unknown whether future view renderers will emit compatibility answers other than `No.` or `Unknown.`. It remains Unknown whether a future public consumer will need explicit package cardinality fields rather than the existing request/contribution/scalar relation. It remains Unknown whether other composition families require different aggregation questions.

## Closing questions

What responsibility forms the compatibility package? `build_constitutional_view_composition(...)`, specifically the validated requested-view loop that builds each requested registered view, renders its payload, appends the contributing view, and records one compatibility answer per built payload.

What standing does an empty package carry? Known empty compatibility-contribution cardinality with no negative compatibility testimony, rendered as aggregate `Unknown.`.

What exact question does compatibility aggregation answer? Whether one or more formed compatibility contributions exist and every formed contribution answered `No.`.

Why was the previous empty result lossy? Python `all([])` collapsed no compatibility testimony and populated all-negative testimony into the same substantive `No.` claim.

What smallest repair restores purpose-relative losslessness? Guard the all-negative aggregate with non-empty compatibility contributions at the local aggregate assertion.

What public behavior remains compatible? Populated all-`No.` compositions still render and serialize `No.`, Unknown or mixed populated contributions still produce `Unknown.`, unsupported requested views still refuse, shapes remain unchanged, and read-only/no-ledger/no-mutation boundaries remain unchanged.

What stronger package architecture remains unwarranted? A universal package abstraction, package-status enum, aggregate-result object, compatibility-package dataclass, shared aggregation framework, or repository-wide truthiness helper.

What local Unknowns remain after repair? Post-validation build failure standing, future non-`No.`/non-`Unknown.` contribution contents, future explicit cardinality consumer needs, and aggregation rules for unrelated composition families remain Unknown.
