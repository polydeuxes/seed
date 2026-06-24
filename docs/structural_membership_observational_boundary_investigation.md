# Structural Membership Observational Boundary Investigation

## Purpose

Determine the strongest form of structural membership that can remain purely
observational in the current repository, without implementing membership and
without creating membership surfaces, document families, document types, shape
candidates, ontology, recommendations, or document classification.

## Repository authority reviewed

The current documentation structure observer is explicitly read-only. Its
recurrence boundary observes structural recurrence only and excludes prose
interpretation, claim extraction, authority inference, shape inference, ontology
promotion, event-ledger writes, and repository mutation.

The current implementation already includes:

- documentation structure observation;
- recurrence counts and distributions;
- exact section-label drilldown;
- partial coverage for skeleton and outlier visibility.

Repository investigation evidence also says observation does not currently have
explicit membership facts. The closest implementation-backed membership-like
relation noted there is a local capability-to-domain map, not documentation
membership.

## Candidate membership forms

### Exact section-label membership

A document is in `section-label:<label>` only if it contains at least one
observed Markdown section heading whose heading text exactly equals `<label>`.

- **Observable evidence source:** Markdown heading and section inventory.
- **Set definition:** all document paths for which any observed section heading
  text exactly equals the requested label.
- **Membership boundary:** exact heading-label inclusion only.
- **Interpretation risk:** low to medium; labels can sound semantic, but the
  safe reading is only literal heading-string equality.
- **Recurrence overlap:** recurrence already counts section labels across the
  corpus.
- **Drilldown overlap:** current drilldown already supports only
  `section-label:<exact label>` and returns path, line, depth, occurrence count,
  and document count.

Answerable questions:

- Which documents contain the exact section label `Purpose`?
- Where does that exact label occur?

Unanswerable questions:

- Which documents are similar?
- Which documents are purpose documents?
- Which documents are the same type?
- Which documents belong together?

Interpretation pressure appears when an observed heading label is promoted into a
concept, document role, family, or type.

### Exact front-matter-key membership

A document is in `front-matter-key:<key>` only if its observed YAML-like front
matter contains exactly that key.

- **Observable evidence source:** front-matter presence and extracted key names.
- **Set definition:** all document paths whose observed front-matter key list
  includes the requested key.
- **Membership boundary:** exact key-name inclusion only.
- **Interpretation risk:** medium; metadata keys can invite concept, authority,
  or ontology interpretation.
- **Recurrence overlap:** recurrence already counts front-matter keys.
- **Drilldown overlap:** no current equivalent; current drilldown accepts only
  exact section-label targets.

Answerable questions:

- Which documents carry the exact front-matter key `defines`?
- How many documents expose this exact key?

Unanswerable questions:

- What does the key mean?
- Which documents define the same concept?
- Which documents are the same metadata type?

Interpretation pressure appears when key presence is treated as semantic concept
membership rather than structural key presence.

### Exact skeleton-signature membership

A document is in `skeleton-signature:<signature>` only if the generated raw
heading-outline skeleton signature exactly equals `<signature>`.

- **Observable evidence source:** heading outline and generated raw skeleton
  signature.
- **Set definition:** all document paths whose generated skeleton signature is
  exactly the requested signature.
- **Membership boundary:** exact generated-signature equality only.
- **Interpretation risk:** medium to high; skeleton vocabulary can easily drift
  into shape inference or document type inference.
- **Recurrence overlap:** recurrence already counts section skeleton signatures
  and preserves raw JSON signatures while compacting human output.
- **Drilldown overlap:** no current equivalent; current drilldown accepts only
  exact section-label targets.

Answerable questions:

- Which documents share this exact generated skeleton?
- How many documents have exactly this raw heading-outline signature?

Unanswerable questions:

- Which documents have similar skeletons?
- Which documents are the same type?
- Which skeletons are document families?
- Which shape should be promoted?

Interpretation pressure appears when exact signature equality becomes similarity,
family detection, type inference, or shape-candidate promotion.

### Exact outlier-signal membership

A document is in `outlier-signal:<signal>` only if the structural outlier logic
emits exactly that signal for the document.

- **Observable evidence source:** emitted structural outlier signals such as
  missing front matter, missing trailing newline, empty sections, high section
  count, high code-fence count, high link count, deep heading depth, and rare
  section labels.
- **Set definition:** all document paths whose emitted structural outlier signal
  list contains the requested signal.
- **Membership boundary:** exact emitted diagnostic signal only.
- **Interpretation risk:** medium; outlier language can imply quality judgment,
  prioritization, or recommendation.
- **Recurrence overlap:** recurrence already emits structural outlier rows and
  signal names when outlier visibility is requested.
- **Drilldown overlap:** no current equivalent; current drilldown accepts only
  exact section-label targets.

Answerable questions:

- Which documents carry the exact outlier signal `missing_front_matter`?
- Which documents carry the exact outlier signal `deep_heading_depth`?

Unanswerable questions:

- Which documents are bad?
- Which documents should be fixed first?
- Which documents belong to an outlier family?

Interpretation pressure appears when emitted signals become quality classes,
remediation queues, document families, or recommendation inputs.

## Observational boundaries

A structural membership form remains observational only when it is:

- exact;
- observable from already extracted structural fields;
- reproducible from the same repository bytes and rule set;
- limited to path, count, line, depth, key, signature, or emitted signal evidence;
- read-only;
- not recorded as cluster truth;
- not promoted into preserved knowledge;
- not interpreted as similarity, classification, family, type, ontology, or
  recommendation.

## Interpretation boundaries

Allowed statements:

- This document contains exact heading label `Purpose`.
- This document carries exact front-matter key `defines`.
- This document has exact generated skeleton signature `S`.
- This document carries exact emitted outlier signal `deep_heading_depth`.

Disallowed statements:

- This document is a purpose document.
- This document defines the same concept as another document.
- This document belongs to a skeleton family.
- This document is the same type as another document.
- This document is similar to another document.
- This document should be recommended or prioritized.

## Strongest safe membership candidate

The strongest safe form is exact structural-value membership over already
observed fields, where the set is defined only by equality against a single
emitted structural value and the output remains limited to mechanical evidence.

Among the reviewed candidates, exact section-label membership is the safest
concrete form because the repository already implements exact section-label
structural drilldown and tests that it remains exact, read-only, non-semantic,
and bounded away from prose interpretation, claim extraction, shape inference,
ontology promotion, event-ledger writes, and repository mutation.

## Unsafe membership candidates

Unsafe candidates include:

- similarity membership;
- document-family membership;
- document-type membership;
- shape-candidate membership;
- ontology membership;
- recommendation or remediation membership;
- any membership based on interpreted prose;
- any membership based on inferred conceptual relation rather than exact
  structural equality.

## Remaining uncertainties

- Front-matter-key membership is structurally plausible but not currently
  drilldown-backed.
- Skeleton-signature membership is exact but carries strong shape-inference
  pressure.
- Outlier-signal membership is reproducible but threshold-shaped and can invite
  quality or prioritization interpretation.
- Current repository evidence says explicit membership facts are not part of
  observation, so any future surface would need to remain diagnostic and avoid
  becoming cluster truth or preserved ontology.

## Files inspected

- `AGENTS.md`
- `seed_runtime/documentation_structure.py`
- `tests/test_documentation_structure.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `docs/implicit_observation_workflow_investigation.md`

## Files changed

- `docs/structural_membership_observational_boundary_investigation.md`

## LOC changed

- 226 added
