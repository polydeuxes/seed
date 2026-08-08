# developer-compiled probe register 001

A list of runtime surfaces that look like Seed competencies and are not. Kept
because the same mistake keeps being made, most recently by this session on
2026-08-08.

## 1. The test

A surface belongs here when the capability was written by a developer rather
than warranted by Seed's own material, and its output does not survive for a
later responsible act to consume.

```text
whose act is this?
    a function a developer wrote      -> probe
    an act Seed performs              -> candidate road

what becomes of the finding?
    vanishes with the Python objects  -> probe
    preserved for a later consumer    -> candidate road

what is the subject?
    a file read through a manifest a
    developer constructed             -> probe
    Seed's own preserved occurrence   -> candidate road
```

**Being generic does not exempt a surface.** A probe that enumerates forms
instead of accepting a supplied candidate is a better probe. It is still a
probe. Fixing caller-supplied candidates fixes one defect, not the category.

**"Zero events" is not the test on its own.** `06.Events:20` does not require
Event recording for every constitutional occurrence. The question is whether
*anything* preserves the occurrence and its finding. If nothing does, the
finding disappears and Seed holds nothing.

## 2. The register

```text
seed_runtime/external_material_testimony_binding.py       probe
seed_runtime/external_material_structural_projection.py   probe
seed_runtime/external_material_surface_feature_projection.py  probe
seed_runtime/observations.py :: ObservationIngestor       compressed, see below
seed_runtime/candidate_external_grammar.py                probe, unaudited
predicate_catalog/core.json                               compiled competency
seed_runtime/evidence_graph.py                            compiled competency
```

**The `external_material_*` chain.** Read-only line and region projection plus
surface-feature measurement over a caller-supplied artifact. Careful, honest,
and declares itself "not runtime Evidence, Fact, candidate verification, or
capability evidence" in its own boundary notes. It writes nothing and holds
nothing. PR `#2009` already classified this family as developer-compiled
behavior with no competency Standing.

**`ObservationIngestor`.** Not a probe but not a clean road either. Active law
names the compression directly at `05.Testimony:18`: "The current repository
compresses Observation intake, Evidence construction, claim-field
normalization, optional Fact artifact construction, and fact event emission in
`ObservationIngestor`. The Book recognizes that compression as implementation
testimony, not as a universal constitutional rule."

**`predicate_catalog/core.json`.** 76 rows asserting "one canonical thing Seed
can know", five fields each -- `predicate, kind, value_type, cardinality,
allowed_values` -- and no source, evidence, provenance, scope, or production
boundary. `01.Kinds:19` denies exactly this: an inventory row does not supply
kind-specific production authority without those coordinates. See
`predicate_cat_test_001.md`.

## 3. The proper path

`run_persistent_operator_console`. It is the only path where a real operator
occurrence is preserved, and it is where external material has to arrive if
Seed is to hold anything about it.

It is also the expensive one, which is the point. A probe is fast because it
does no evidence work. Measurements of a probe say nothing about what Seed
costs, and reporting them as performance findings is how this session
concluded there was "no speed problem" while the real path needed 15 days for
the same file. See `corpus_relation_observation_run_001.md`.

## 4. What this register does not establish

**That any listed surface should be deleted.** The `external_material_*` chain
is careful work and its disclaimers are accurate. The finding is that it is not
a road, not that it is worthless.

**That `ObservationIngestor` is unlawful.** `05.Testimony:18` calls the
compression constitutionally safe for weak source-relative observed Facts when
scope and claim strength are preserved.

**That the list is complete.** Four surfaces were examined closely and
`candidate_external_grammar.py` was not audited at all.

**That the console is correct.** It is the proper path and it is quadratic.
Being the right road does not make it a finished one.
