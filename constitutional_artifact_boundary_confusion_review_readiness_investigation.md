# Constitutional Artifact Boundary-Confusion Review Readiness Investigation

## Bounded question

Across current repository evidence, do existing produced-artifact formats already expose support path, claim form, authority boundary, confidence or evidence-strength limit, Unknowns, and lawful stop consistently enough to support repeatable review of boundary-confusion risks such as Evidence != Vibes, Authority != Volume, Visibility != Truth, Repetition != Proof, Confidence != Certainty, and Narrative != History without implementing a new diagnostic surface?

Repository authority wins. This is one bounded artifact-format investigation. It does not implement code, add a diagnostic surface, create artifact scoring, create a checklist engine, create a truth engine, evaluate public-world facts, perform legal research, implement the Eye, or promote the six motivating phrases into ontology.

## App-visible evidence used

The app was used only as bounded repository evidence, not as an oracle.

Commands run:

```text
python scripts/seed_local.py --help
python scripts/seed_local.py --diagnostic-inventory --json > /tmp/di.json
python scripts/seed_local.py --diagnostic-shape-audit --json > /tmp/dsa.json
python scripts/seed_local.py --reasoning-path derivation unknown-frontier-candidate --json > /tmp/rp.json
python scripts/seed_local.py --selection-path unknown-frontier-candidate --json > /tmp/sp.json
python scripts/seed_local.py --documentation-structure --sections --json > /tmp/doc_sections.json
python scripts/seed_local.py --documentation-structure --recurrence --json > /tmp/doc_recur.json
```

App-visible evidence recovered:

- `--diagnostic-inventory --json` exposes operational boundary fields including `cli_flags`, `description`, `supports_json`, `supports_record`, `record_scope`, `emits_diagnostic_facts`, `writes_event_ledger`, `reads_diagnostic_facts`, `uses_repo_files`, `uses_projected_state`, and `mutates_cluster`.
- `--diagnostic-shape-audit --json` checks declared diagnostic fields against observed implementation fields with `diagnostic`, `field`, `declared`, `observed`, and `status`.
- `--reasoning-path derivation unknown-frontier-candidate --json` exposes `boundary`, `evidence`, `intermediate_conclusions`, `derived_conclusions`, `consumers`, `story_impact`, and `unknowns`; for an unsupported subject it preserved a typed public Unknown and a read-only, non-recording, non-mutating boundary.
- `--selection-path unknown-frontier-candidate --json` exposes `boundary`, `candidates`, candidate `reason`, candidate `evidence`, `selection_factors`, `outcome`, `selected`, and `unknowns`; for an unsupported target it returned `selected="unknown"` and a public Unknown rather than inferring a selection.
- `--documentation-structure --sections --json` exposes mechanical section outlines with a boundary that is read-only and does not infer authority, claims, shapes, or prose meaning.
- `--documentation-structure --recurrence --json` exposes section-label recurrence only as structural metadata. In the sampled top-level/document corpus visible to that surface, recurring labels include `Supported conclusions` and `Unsupported conclusions`, while exact labels such as `Bounded question`, `App-visible evidence used`, `Reviewed repository evidence`, `Preserved Unknowns`, `Lawful stop`, `Claim form`, and `Authority boundary` were not themselves common section-label evidence in that surface's top-level output.

## Reviewed repository evidence

Repository evidence reviewed included the predecessor boundary-confusion audit, artifact bounded lawful reliance, constitutional translation invariant preservation, constitutional access transition, lawful transition survey, typed Unknown preservation survey, bounded ask eligibility audit, inquiry surface classes observation, diagnostic inventory/shape-audit implementation and tests by app output, reasoning-path and selection-path app surfaces, and repository documents found through bounded text search for support path, claim form, authority boundary, confidence/evidence-strength, Unknown preservation, and lawful stop.

The strongest local predecessor is `constitutional_boundary_confusion_competency_audit.md`, which explicitly identified the missing pressure this investigation tests: produced artifacts are not uniformly required to expose in one normalized place the claim-form boundary, support path, authority boundary, confidence/evidence-strength limit, Unknowns, and lawful stop condition for each boundary-confusion risk.

## Artifact-format evidence

Current artifact formats show a mixed pattern:

1. Some app-visible JSON surfaces expose repository-visible fields, not just prose. Reasoning-path and selection-path expose `boundary`, `evidence`, and `unknowns`; diagnostic inventory and shape audit expose declared/observed operational shape fields.
2. Many produced Markdown artifacts use recurring prose sections such as `Bounded question`, `Reviewed evidence`, `Supported conclusions`, `Unsupported conclusions`, `Preserved unknowns`, `Confidence`, and `Lawful stop`, but these are conventions across artifacts rather than one enforced implementation schema for every produced artifact.
3. The documentation-structure surface can prove section-label recurrence mechanically, but its own boundary refuses claim extraction, authority inference, shape inference, ontology promotion, and prose interpretation. Therefore it supports repeatable format discovery, not semantic truth about artifact contents.
4. The diagnostic inventory and diagnostic shape audit are implementation-visible enough for operational surfaces, but they are about diagnostic surface shape, not general Markdown artifact review.

## Support-path analysis

Existing sections or fields that already expose support path:

- App-visible reasoning-path fields: `evidence`, `intermediate_conclusions`, `derived_conclusions`, `consumers`, and `story_impact` expose a support-chain shape for derivation-like subjects.
- App-visible selection-path fields: candidate `evidence`, candidate `reason`, `selection_factors`, `outcome.reason`, and `non_selected` expose selection support for implemented selection targets and preserve no-support outcomes for unsupported targets.
- Diagnostic inventory fields such as `uses_repo_files`, `uses_projected_state`, `reads_diagnostic_facts`, `writes_event_ledger`, and `record_scope` expose operational support/source boundaries for diagnostic surfaces.
- Markdown artifacts often contain `Reviewed evidence`, `Implementation evidence`, `Recurring repository evidence`, `Files inspected`, `Commands executed`, and similar support sections.

Finding: support path is recurring and partly implementation-visible, but not normalized across all produced artifacts. Existing evidence supports repeatable review where an artifact exposes evidence sections or where an app surface has explicit support fields. It does not support assuming every artifact has an equivalent support path.

## Claim-form analysis

Existing sections or fields that already expose claim form:

- Markdown artifacts often distinguish `Supported conclusions`, `Unsupported conclusions`, `Non-conclusions`, `Short answer`, `Final answer`, `Answer`, `Rejected candidates`, and `Preserved unknowns`.
- Existing reconciliation documents around claim strength and assertion semantics provide repository vocabulary for separating kinds of claims.
- App-visible reasoning-path separates `evidence`, `intermediate_conclusions`, and `derived_conclusions`, which is a stronger claim-form separation than prose alone for that surface.
- App-visible selection-path separates candidates, selected outcome, non-selected entries, and Unknown selection outcomes.

Finding: claim form is visible in many artifacts and in some app surfaces, but it is not a universal required field. Repeatable review can inspect whether an artifact distinguishes supported conclusion, unsupported conclusion, Unknown, candidate, and outcome. It cannot require one normalized claim-form field without additional repository work.

## Authority-boundary analysis

Existing sections or fields that already expose authority boundary:

- App-visible reasoning-path and selection-path `boundary` objects expose modes such as read-only audit, plus `mutates_cluster`, `records_facts`, and `writes_event_ledger`.
- Diagnostic inventory exposes `record_scope`, `writes_event_ledger`, `mutates_cluster`, `emits_cluster_facts`, `emits_diagnostic_facts`, `reads_diagnostic_facts`, `uses_repo_files`, and `uses_projected_state`.
- Diagnostic shape audit verifies diagnostic declarations against observed implementation fields.
- Many artifacts include sections named `Boundary`, `Scope`, `Purpose and boundary`, `Method and authority boundary`, or prose authority-boundary statements.

Finding: authority boundary is the strongest recurring field family. It is implementation-visible for diagnostic, reasoning-path, selection-path, bounded ask, inquiry orientation, and related operational surfaces. For general Markdown artifacts, it remains partly convention unless tied to app output, code, tests, or explicit repository evidence.

## Confidence/evidence-strength analysis

Existing sections or fields that already expose confidence or evidence-strength limit:

- Markdown artifacts often include a `Confidence` section, confidence sentence, evidence-strength discussion, or claim-strength reconciliation.
- The predecessor audit and artifact bounded lawful reliance evidence preserve confidence/evidence-strength limits as part of bounded reliance.
- App-visible reasoning-path and selection-path preserve empty evidence plus Unknown outcomes when support is absent; this is an evidence-strength limit by behavior even when no numeric confidence is emitted.
- Diagnostic shape audit status values such as `consistent`, `warning`, `mismatch`, and `unknown` expose implementation consistency state for diagnostics, not general artifact confidence.

Finding: confidence/evidence-strength limits recur, but are less uniformly implementation-visible than authority boundary and Unknown preservation. Existing artifacts support review for overclaiming when confidence or evidence-strength is present. They do not support a repository-wide assumption that every produced artifact must carry an explicit confidence field.

## Unknown preservation analysis

Existing sections or fields that already expose Unknowns:

- App-visible reasoning-path and selection-path both expose an `unknowns` list with `area` and `reason` for unsupported/unknown requests.
- Typed Unknown preservation repository evidence identifies a local typed record shape with `unknown_type`, `area`, and `reason`, projected back to public Unknown compatibility shape.
- Markdown artifacts often contain `Preserved unknowns`, `Preserved Unknowns`, `Open questions`, `Unresolved Observations`, or Unknown-specific subsections.
- Diagnostic inventory includes descriptions and fields that distinguish diagnostic facts, cluster facts, event-ledger writes, and mutation boundaries, helping prevent diagnostic Unknowns or findings from silently becoming cluster truth.

Finding: Unknown preservation is recurring and partly implementation-visible. It is reliable where surfaces expose `unknowns` or where artifacts explicitly preserve unknowns. It is not safe to infer Unknowns from silence in arbitrary artifacts.

## Lawful-stop analysis

Existing sections or fields that already expose lawful stop:

- The predecessor boundary-confusion audit includes a `Lawful stop` section and per-distinction stop conditions.
- The lawful transition survey includes recurring stop-condition analysis around evidence insufficiency, authority boundaries, and non-promotion.
- App-visible reasoning-path and selection-path implement stop behavior by returning empty support plus Unknown rather than promoting unsupported derivation or selection claims.
- Diagnostic inventory/shape-audit boundaries expose `mutates_cluster=false`, `writes_event_ledger`, and `record_scope`, which are operational stop boundaries for diagnostics.

Finding: lawful stop is strongly present as a constitutional prose discipline and visible in several app behaviors, but it is not a uniform field across all produced artifacts. Repeatable review can ask whether an artifact states a stop condition or behaves with an unknown/non-mutating stop. It cannot assume a formal `lawful_stop` field exists.

## Repeatability finding

Existing formats are recurring enough to support a bounded, manual, repeatable boundary-confusion review without adding a new diagnostic surface, provided the review remains artifact-format review rather than implementation enforcement.

The repeatable review can ask, for each artifact under review:

1. Where is support path exposed: app field, evidence section, command/file list, or explicit support prose?
2. Where is claim form exposed: supported conclusion, unsupported conclusion, candidate, selected outcome, Unknown, or final answer?
3. Where is authority boundary exposed: boundary field, scope/method section, diagnostic inventory row, shape-audit field, or explicit negative authority?
4. Where is confidence/evidence-strength limited: confidence section, evidence-strength analysis, empty evidence with Unknown, or status field?
5. Where are Unknowns preserved: `unknowns` field or preserved/open/unresolved section?
6. Where does the artifact stop lawfully: explicit lawful stop section, non-promotion statement, read-only boundary, no-record/no-mutation field, or Unknown outcome?

The review must also record when any answer is absent or unsupported. Absence should remain Unknown, not be converted into a defect, proof of safety, or authority for implementation.

## Prose convention versus repository-visible reliance

These fields are not merely prose conventions in the repository as a whole, because several app-visible surfaces expose related fields structurally: diagnostic inventory, diagnostic shape audit, reasoning-path, selection-path, and documentation-structure boundaries.

However, for general produced Markdown artifacts, many fields remain prose conventions unless anchored in:

- app-visible JSON fields;
- code and tests;
- diagnostic inventory/shape-audit declarations;
- explicit command/file evidence;
- recurring artifact sections mechanically visible through documentation-structure;
- repository documents that preserve supported and unsupported conclusions.

Therefore the current reliance boundary is: existing artifacts support repeatable review, not automated enforcement or universal schema claims.

## What remains inconsistent, missing, or unsupported

- No single normalized repository-wide artifact field set requires support path, claim form, authority boundary, confidence/evidence-strength limit, Unknowns, and lawful stop in every produced artifact.
- Exact section names vary by artifact family and are not uniformly exposed by documentation-structure recurrence.
- Confidence is not uniformly explicit.
- Claim form is often recoverable from headings and prose, but not always implementation-visible.
- Lawful stop is often present as discipline, but not a universal structured field.
- Support path can be strong in app surfaces and evidence-heavy artifacts, but not guaranteed for every Markdown artifact.
- The six boundary-confusion phrases are useful motivations for this review, but current evidence does not support promoting them into ontology or diagnostic categories.
- Documentation-structure can show section recurrence, but its boundary prohibits treating section labels as semantic proof.

## Does repository evidence support implementation work yet?

No implementation work is supported by this investigation.

Repository evidence supports a bounded manual artifact-format review using existing fields and sections. It does not yet support adding a diagnostic surface, checklist engine, scoring system, truth engine, or universal artifact schema. The smallest missing pressure identified by the predecessor audit remains real, but this investigation finds that current evidence is sufficient for repeatable bounded review before implementation.

## Supported conclusions

1. Existing produced-artifact formats already expose enough recurring structure to support bounded repeatable boundary-confusion review without a new diagnostic surface.
2. The strongest implementation-visible anchors are diagnostic inventory, diagnostic shape audit, reasoning-path, selection-path, and documentation-structure boundary metadata.
3. Authority boundary and Unknown preservation are the most implementation-visible recurring elements.
4. Support path and claim form are recurring, but mixed between app-visible fields and Markdown prose sections.
5. Confidence/evidence-strength and lawful stop recur, but are not uniformly structured across all artifacts.
6. Repeatable review must preserve missing fields as Unknown rather than infer safety, failure, or truth.
7. Repository evidence supports manual bounded review, not implementation.

## Unsupported conclusions

1. Unsupported: every produced artifact already has one normalized boundary-confusion review block.
2. Unsupported: existing app output is an oracle for artifact truth.
3. Unsupported: documentation section recurrence proves semantic adequacy.
4. Unsupported: the six boundary-confusion phrases are repository ontology.
5. Unsupported: a new diagnostic surface, checklist engine, artifact scoring system, or truth engine is warranted now.
6. Unsupported: every artifact must add a new format before more evidence is gathered.
7. Unsupported: confidence should be mandatory on every artifact based on current evidence alone.

## Preserved Unknowns

- Whether a future corpus-level artifact-format audit would find enough uniformity to justify an implementation-backed checklist remains Unknown.
- Whether specific artifact families should adopt a shared boundary-confusion review block remains Unknown.
- Whether confidence should become a mandatory artifact field remains Unknown.
- Whether lawful stop should become a structured artifact field remains Unknown.
- Whether existing section labels are sufficiently stable across future artifacts remains Unknown.
- Whether public-world source independence, source volume, or repetition could be evaluated without world research remains Unknown.

## Lawful stop

This investigation stops at one bounded artifact-format readiness review. It does not implement anything, add a diagnostic surface, require a new artifact schema, score artifacts, promote motivation into constitutional law, evaluate the Eye, or convert app-visible output into truth. Missing or inconsistent fields remain Unknown unless repository evidence supports a narrower conclusion.

## Recommendation

No implementation slice is recommended.

If a next bounded investigation is desired, repository evidence supports only a manual family-limited artifact-format audit of a small named artifact family, such as constitutional investigations or competency audits, to compare actual section usage against the six review questions above. That next step should still avoid adding a diagnostic surface unless it finds implementation-visible recurrence and a concrete repository failure that current review cannot preserve.
