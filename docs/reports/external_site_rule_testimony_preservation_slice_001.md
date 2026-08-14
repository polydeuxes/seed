# External Site Rule Testimony Preservation Slice 001

## Recovered responsibility

This slice recovers exactly one implementation-local responsibility:

```text
caller- or observer-supplied attributed rule testimony
→ external site-rule testimony set assembler
→ immutable external site-rule testimony set
→ read-only diagnostic/operator consumer
```

Seed can preserve what multiple external website surfaces said about access or use, including distinct sources, claimed scopes, acquisition provenance, and Unknowns, without flattening them into one site policy and without allowing them to govern Seed directly.

## Campaign evidence supporting recovery

The Project Gutenberg external orientation campaign exposed a recurring substrate-neutral pattern: encountered external rule statements were retained as attributed testimony rather than promoted into authorization, applicability, or movement decisions. Examples included robots.txt statements, automation policy prose, and catalog or machine-access guidance. This slice recovers only that testimony boundary and does not canonicalize the campaign observer, HTTP acquisition, homepage traversal, link discovery, request budgeting, machine-path preference, catalog lookup, rendition selection, or exception handling.

## Selected implementation boundary

The implementation is a small immutable dataclass artifact and assembler in `seed_runtime/external_site_rule_testimony.py`, plus a CLI diagnostic/operator surface:

```text
seed --external-site-rule-testimony JSON_FILE [--json]
```

The CLI owns only JSON-file parsing, typed input construction, testimony-set assembly, and deterministic human or JSON rendering.

## Producer

The producer is caller supplied. The input may come from a temporary website observer, fixture, operator, imported archive, or future acquisition mechanism. The producer does not acquire website content in this slice, and the assembler never fetches URLs.

## Input artifact

The typed caller-input artifact is `ExternalSiteRuleTestimonyInput`, containing:

- `site_scope`
- `testimonies`
- `set_unknowns`

Each testimony is represented by `ExternalSiteRuleTestimonyInputTestimony`, containing:

- `testimony_id`
- `source_url`
- `acquired_at`
- `content_hash`
- `bounded_rule_text`
- `claimed_scope`
- `rule_kind`
- `discovery_route`
- `operator_supplied_seed`
- `interpretation_status`
- `unknowns`

## Output artifact

The immutable output artifact is `ExternalSiteRuleTestimonySet`, containing:

- `site_scope`
- independently attributed `testimonies`
- `set_unknowns`
- required `boundary_notes`
- `read_only=True`
- `writes_event_ledger=False`
- `mutates_cluster=False`

## Consumer

The consumer is a read-only diagnostic/operator renderer. Human and JSON output expose the preserved testimony and boundary notes without selecting routes, authorizing movement, resolving conflict, or mutating event ledger or cluster state.

## Testimony identity rules

`testimony_id` is stable only within the testimony set. It is not a policy identity, authorization identity, capability identity, movement identity, or verified rule identity. Duplicate testimony IDs fail structural validation.

## Source attribution rules

`source_url` is preserved exactly as supplied by the caller. Distinct URLs are not normalized into one source, and multiple testimonies from the same source remain independently attributable.

## Claimed-scope behavior

`claimed_scope` is preserved as caller-supplied testimony. The assembler does not determine whether the claimed scope applies to the site, host, path, operation, or Seed movement.

## Interpretation-status boundary

`interpretation_status` is preserved only as a bounded caller-supplied status. The assembler rejects Seed-verdict statuses such as `authorized`, `permitted`, `prohibited`, `applicable`, `binding`, `overrides`, and `safe_to_execute`.

## Unknown preservation

Testimony-level `unknowns` and set-level `set_unknowns` are preserved exactly as supplied. Unknowns are not rewritten as false, absent, unrestricted, permitted, prohibited, or resolved.

## Validation boundary

Validation is structural only:

- required strings must be present;
- `operator_supplied_seed` must be boolean;
- testimony IDs must be unique within a set;
- Unknown collections must contain strings;
- disallowed Seed-verdict interpretation statuses fail.

The assembler does not validate URL existence, remote hash correctness, statement currency, source control of a site, legal binding effect, scope applicability, conflict, precedence, or whether Seed may act.

## Boundary notes

Human and JSON output include notes equivalent to:

- External site rules are preserved as attributed testimony, not Seed authority.
- Each testimony retains its independent source and claimed scope.
- The testimony set does not determine permission, prohibition, applicability, or precedence.
- Site-reported permission does not grant Seed authorization.
- Absence of prohibition is not permission.
- robots.txt is not treated as complete site policy.
- Possible consistency or conflict is preserved without resolution.
- This artifact does not select or authorize external movement.

## Read-only guarantees

The artifact, assembler, CLI surface, and renderers preserve:

```text
read_only = true
writes_event_ledger = false
mutates_cluster = false
```

The slice does not fetch URLs, inspect live websites, execute observers, create runtime Observations, create runtime Evidence, create Facts, alter projected State, authorize an operation, select an access route, execute external movement, or mutate a repository or cluster.

## Campaign integration

No Project Gutenberg scaffold integration was necessary. The campaign remains noncanonical. No campaign acquisition code was moved into `seed_runtime`.

## Compatibility answer

Did this slice change any existing compatibility boundary?

No.

## Files changed

- `seed_runtime/external_site_rule_testimony.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_external_site_rule_testimony.py`
- `external_site_rule_testimony_preservation_slice_001.md`

## LOC delta

Pre-report implementation/test/registration delta from `git diff --numstat` was 58 insertions and 2 deletions across tracked modified files, plus new artifact and test files. Final repository diff should be read from `git diff --numstat` before commit.

## Tests executed

- `pytest -q tests/test_external_site_rule_testimony.py`
- `pytest -q tests/test_external_site_rule_testimony.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining missing roads

The following roads remain explicitly out of scope and unimplemented:

```text
external site encounter
→ rule testimony acquisition
```

```text
rule testimonies
→ scope comparison
```

```text
scope comparison
→ applicable external constraints
```

```text
applicable external constraints
+
Seed authorization
→ eligible external movement
```

```text
eligible external movement
→ selected acquisition path
```

```text
selected path
→ attributed external result
```
