# Project Gutenberg External Orientation Campaign 001

## 1. Bounded inquiry

This campaign asked whether a small noncanonical Seed scaffold can orient to Project Gutenberg, preserve attributed website access testimony, prefer a declared machine pathway, and acquire one bounded public-domain grammar rendition for caller-supplied candidate grammar preservation. The live environment could not complete first contact because the outbound HTTPS tunnel returned `403 Forbidden` before any Project Gutenberg response bytes were acquired.

## 2. Scaffold status

The implementation is a reference scaffold only. It is not canonical website architecture, not a general crawler, and not a permanent Project Gutenberg competency. It lives under `campaigns/` rather than `seed_runtime/` to keep the campaign noncanonical and upstream of permanent Seed runtime ownership.

## 3. Starting repository evidence

The repository already contains the candidate grammar preservation path: `CandidateExternalGrammarInput`, `CandidateExternalGrammarSet`, deterministic JSON output, and deterministic human presentation. The scaffold imports and uses that surface without changing it.

## 4. First-contact behavior

The live first-contact command attempted only a bounded campaign run using `GET` through `LiveHttpClient` with a truthful campaign User-Agent. The environment blocked the HTTPS tunnel before a request reached Project Gutenberg, so the run preserved an environment failure rather than fabricating site testimony.

## 5. Pages and machine surfaces encountered

Local deterministic tests exercised homepage, `robots.txt`, policy, catalog, and rendition fixture surfaces. The live campaign encountered no Project Gutenberg page bytes because the tunnel failed before first contact.

## 6. Site rules preserved

The scaffold preserves `robots.txt` separately from prose automation policy. In local fixtures, robot directives and bounded policy excerpts become attributed `SiteRule` testimony with source URL, acquisition time, content hash, bounded text, scope, kind, discovery path, operator-seed flag, interpretation status, and Unknowns.

## 7. Rule conflicts and Unknowns

Rule relationships are not flattened into a single `site_policy` value. The scaffold preserves unresolved `scope_unknown` interpretation and carries the Unknown that `robots.txt` is not complete site policy. Live rule consistency remains Unknown because no Project Gutenberg rule surface was acquired.

## 8. Request and byte budget

The scaffold constants enforce `maximum_requests = 15`, `maximum_total_download_bytes = 15 MiB`, `maximum_acquired_ebook_renditions = 1`, and a two-second minimum live delay. The live campaign result recorded `request_count = 0` and `byte_count = 0` due to the pre-request tunnel failure.

## 9. Selected access route

No live access route was selected. In local deterministic coverage, a declared machine catalog path is preferred over an ordinary human-facing ebook page.

## 10. Rejected routes and reasons

The scaffold rejects recursive crawl behavior and does not continue to ordinary pages once a machine catalog path is sufficient in the fixture. In live execution, all acquisition routes remained unavailable because first contact was blocked by the environment.

## 11. Catalog queries

Local deterministic tests preserve ordered catalog attempts, including no-match and ambiguous-match outcomes. No live Project Gutenberg catalog query was performed.

## 12. Selected or unavailable work

No live grammar work was selected. Fixture coverage selects the first sufficiently identified ordered candidate record, `Graded Lessons in English`, when present and unambiguous.

## 13. Catalog record identity

The fixture-selected record remains a Project Gutenberg ebook record identity distinct from the historical work. Live catalog identity is unavailable.

## 14. Rendition selection

Fixture coverage acquires exactly one plain-text UTF-8-like rendition when that is the available simple inspectable representation. Live rendition selection was blocked before acquisition.

## 15. Acquisition result

No live rendition bytes were acquired. The live failure is preserved as `URLError: <urlopen error Tunnel connection failed: 403 Forbidden>`.

## 16. Exact SHA-256 and byte length

No live SHA-256 or byte length exists because no live bytes were acquired. Fixture tests prove acquired rendition bytes are hashed and altered bytes produce a different hash.

## 17. Work/edition/ebook/rendition distinctions

The scaffold keeps historical work, print source, Project Gutenberg ebook publication, catalog record, downloaded rendition, local byte artifact, selected excerpt, and candidate grammar testimony distinct in field names and Unknowns. It explicitly preserves that a downloaded rendition is not the historical work.

## 18. Bounded material selection

Fixture coverage selects at most 250 lines and 12,000 characters from the acquired rendition, records the parent rendition SHA-256, line bounds, heading context, unaltered selected content, purpose, selection time, selector attribution, and Unknowns.

## 19. Candidate grammar handoff

The scaffold creates caller-supplied structural candidate testimony and passes it to the existing candidate external grammar surface. The resulting artifact remains read-only, does not write the event ledger, and does not mutate cluster state.

## 20. Explicit operator-supplied responsibilities

The operator supplied the campaign objective, initial Project Gutenberg seeds, fallback policy neighborhoods, ordered candidate shelf, and required structural-candidate discipline. In local fixture handoff, the campaign author supplies the initial structural candidates.

## 21. Seed-owned responsibilities

Seed owns preservation of caller-supplied structural testimony through `CandidateExternalGrammarInput` and `CandidateExternalGrammarSet`, deterministic read-only JSON and human presentation, and fixed `writes_event_ledger=false` / `mutates_cluster=false` boundaries.

## 22. Failures and Unknowns

Preserved live failure: environment HTTPS tunnel refusal before first contact. Unknowns include actual Project Gutenberg homepage testimony at acquisition time, actual robots testimony at acquisition time, actual automation policy testimony at acquisition time, machine pathway discovery status, catalog availability, candidate work availability, rendition availability, and selected material identity.

## 23. Event-ledger and mutation checks

The scaffold has no event-ledger dependency and no State/projected cluster mutation path. Tests assert `writes_event_ledger is False` and `mutates_cluster is False` in campaign and candidate handoff outputs.

## 24. Scaffold responsibilities that appear reusable

Reusable responsibilities exposed: bounded request accounting, byte accounting, redirect preservation, attributed rule testimony, separate robot/prose policy preservation, machine-path preference, catalog attempt preservation, rendition hashing, parent-hash selection binding, and caller-supplied candidate handoff.

## 25. Responsibilities that remain compressed

Compressed responsibilities include real Project Gutenberg catalog discovery, robust RDF parsing, provenance-rich rendition choice, richer rule relationship classification, live artifact storage policy, and human-facing exception handling for bounded adventure cases.

## 26. Missing canonical artifacts or roads exposed

The campaign exposes absence of a canonical external-site testimony model, external byte-artifact store, sanctioned machine-catalog route abstraction, external acquisition budget ledger, and canonical separation between external metadata testimony and Seed facts.

## 27. Whether a bounded implementation slice is now warranted

Yes. The campaign supports exactly one next implementation slice, but this campaign does not implement it.

## 28. Exact next bounded question

Should Seed add a canonical read-only `ExternalSiteRuleTestimony` artifact that preserves source URL, acquisition time, content hash, bounded rule text, claimed scope, rule kind, discovery route, operator-seed status, interpretation status, and Unknowns without granting Seed authorization?

## 29. Files changed

- `campaigns/project_gutenberg_external_orientation_campaign_001.py`
- `tests/test_project_gutenberg_external_orientation_campaign_001.py`
- `project_gutenberg_external_orientation_campaign_001.md`

## 30. Tests and live commands executed

- `python -m black campaigns/project_gutenberg_external_orientation_campaign_001.py tests/test_project_gutenberg_external_orientation_campaign_001.py`
- `pytest -q tests/test_project_gutenberg_external_orientation_campaign_001.py tests/test_candidate_external_grammar.py`
- `python - <<'PY' ... run_campaign(LiveHttpClient(), live=True) ... PY`
- `git diff --stat`
- `git diff --numstat`
- `git diff --check`
- `git status --short`

## 31. Confidence statement

Confidence is high that the local scaffold preserves the requested boundaries and deterministic behaviors under fixture conditions. Confidence is low for live Project Gutenberg acquisition because the environment blocked first contact before any site response could be acquired.

## Required campaign conclusion

E. Environment or repository evidence was insufficient to run the live campaign safely.

The campaign supports exactly one next implementation slice: canonicalize attributed external site-rule testimony without adding a crawler or external fact promotion.
