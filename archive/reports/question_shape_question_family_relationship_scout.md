# Question Shape / Question Family / Survey Warrant Family Relationship Scout

## Scout boundary

This is exactly one bounded Scout investigation. It asks only what recurring repository evidence supports about the relationship, if any, between Question Shapes, Question Families, and Survey Warrant Families.

It does not recover new implementation, recover runtime behavior, recover competencies, stabilize vocabulary, recommend implementation, recommend slices, promote consumer hypotheses into repository architecture, or invent missing intermediate concepts.

Repository authority wins.

## Reviewed implementation evidence

- `seed_runtime/question_surface_inventory.py` contains the strongest implementation-backed Question Family evidence: static inventory rows, bounded ask dispatch maps, required surface arguments, diagnostic-only family declarations, eligibility preparation, bounded work selection, and QuestionFamily explanation payloads.
- `scripts/seed_local.py` contains the bounded `ask --question-family <exact-question-family>` dispatch path and CLI guardrails that reject free-text or unsupported usage before mapping to existing answer surfaces.
- `tests/test_question_surface_inventory.py` proves the static inventory, bounded ask dispatch, unknown-family handling, diagnostic registration consistency, presentation surfaces, and free-text rejection behavior around Question Families.
- `seed_runtime/diagnostic_inventory.py` and `seed_runtime/diagnostic_shape_audit.py` register and audit `question_surface_inventory` as a diagnostic surface, including the QuestionFamily definition and explanation flags.
- `inquiry_subject_resolution_investigation.md` reviews the implementation boundary around exact question-family identity, bounded ask dispatch, explicit surface arguments, and surface-local evidence selection.
- `docs/knowledge_requirement_discovery_investigation.md` reviews exact question-family-to-surface routing and preserves that it does not perform general question interpretation or knowledge discovery.
- `docs/bounded_ask_question_family_eligibility_audit.md` reviews the current Question Family classifications and bounded ask eligibility posture.

## Reviewed constitutional and investigation evidence

- `survey_warrant_recurrence_investigation.md` is the primary recurring evidence for Survey Warrant Families. It treats a warrant family as supported only when multiple artifacts show the same bounded question shape, implementation-evidence posture, investigation shape, and produced artifact pattern.
- `constitution.md` names question-family dispatch as one specialized inquiry form when it follows recovery, pressure visibility, capability verification, answer composition, repository orientation, diagnostic shape audit, and completion-audit discipline.
- `constitutional_expression_characterization.md` treats question-family identity as one possible expression identity that can drift if changed beyond evidence.
- `docs/observation_question_template_reconciliation.md` is the clearest reviewed evidence for `question shape` as a recurring observation-oriented template rather than a universal subject-owned property.
- `docs/inquiry_state_reasoning_reconciliation.md` uses `Bounded self-question` for repository-owned question shapes answered from implementation-backed evidence, while explicitly excluding introspective or natural-language-chat interpretations.
- `narrative_neighborhood_methodology_characterization.md` preserves `question shape` as something that can survive a narrative neighborhood only when repository evidence continues to support it.
- `docs/architectural_recovery_hit_list.md` uses `question shape` near QuestionFamily Admission as the thing a compatibility boundary may decide is registered or handled, but this is a recovery candidate, not implementation authority.
- `unknown_currency_survey.md` treats unknown question-family material as an explicit bounded status and preserves that question-surface inventory and constitutional inquiry terrain may or may not be connected.

## Concept recovery

### Question Shapes

**Recurring implementation evidence:** Limited. The phrase appears in implementation-adjacent documents as a recurring form or template of asking, especially observation-oriented or bounded self-question forms. The clearest repository statements are document-level, not a central implementation registry. `docs/observation_question_template_reconciliation.md` says the implementation shows a recurring observation-oriented question shape, but not as a property of every observed subject. `docs/inquiry_state_reasoning_reconciliation.md` defines bounded self-question as a repository-owned question shape answered from implementation-backed evidence.

**Observable purpose:** Question Shapes name the repeated form of a bounded question: what is being asked, at what resolution, and under what evidence posture. They help describe inquiry patterns without necessarily making them public dispatch identities.

**Recurring neighboring concepts:** observation question templates, bounded self-questions, narrative neighborhoods, repository knowledge, evidence posture, Scout/Survey/Characterization report shapes, and QuestionFamily Admission candidate boundaries.

**Recurring consumers:** Scout, survey, reconciliation, and characterization artifacts consume question shapes as observational patterns; QuestionFamily Admission discussion may consume them when asking whether a shape is registered or handled.

**Recurring producers:** Reconciliations, surveys, narrative-neighborhood methodology, constitutional/recovery artifacts, and some implementation-backed inquiry analyses produce or preserve question shapes.

**Confidence:** Medium-low as an implementation concept; medium as a recurring investigation/documentation concept. Evidence supports recurrence, but not a single implementation owner or stable registry.

### Question Families

**Recurring implementation evidence:** Strong. `QuestionSurfaceInventoryRow` is a static public registry row with `question_family`, example questions, answering surface, CLI surface flag, answer responsibility, authority boundary, bounded status, dispatch surface, required surface args, diagnostic relationships, and implementation reason. Bounded ask maps exact family strings to existing surfaces through `BOUNDED_ASK_DISPATCH_SURFACES`, required argument declarations through `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`, and eligibility/status derivation. Unknown families are rejected or reported as unknown rather than inferred.

**Observable purpose:** Question Families are implementation-backed public inquiry identities. They bind exact operator-supplied family names to inventory visibility, bounded eligibility, optional required surface arguments, presentation/explanation surfaces, and deterministic dispatch to existing answer surfaces.

**Recurring neighboring concepts:** Question Surface Inventory, bounded ask dispatch, surface flags, answer responsibilities, authority boundaries, diagnostic inventory, diagnostic shape audit, required surface args, QuestionFamily definition/explanation, unknown-family boundary, and answer-composition surfaces.

**Recurring consumers:** `ask --question-family`, QuestionFamily definition/explanation presentation, tests, diagnostic inventory, diagnostic shape audit, inquiry subject investigations, knowledge requirement investigations, bounded ask eligibility audits, operational/external orientation documents, and roadmap/recovery artifacts.

**Recurring producers:** `build_question_surface_inventory()`, static bounded ask maps, diagnostic inventory declarations, diagnostic shape audit specs, CLI parser and bounded dispatch code, and tests.

**Confidence:** High. Question Families have explicit implementation identity, registration, validation, presentation, dispatch, and tests.

### Survey Warrant Families

**Recurring implementation evidence:** Mostly constitutional/investigation evidence, not runtime implementation. `survey_warrant_recurrence_investigation.md` recovers recurring warrant families only when multiple artifacts show the same bounded question shape, implementation-evidence posture, investigation shape, and produced artifact pattern. It supports Scout/reconnaissance, Survey/neighborhood-resolution, Characterization/comparative-distinction, Inventory/coverage, Implementation-boundary, Completion/audit, and Boundary/non-collapse-like warrants with varying confidence.

**Observable purpose:** Survey Warrant Families describe recurring authorization patterns for inquiry artifacts: why a bounded Scout, Survey, Characterization, Inventory, audit, or boundary investigation is permitted to ask a particular kind of question and what conclusion strength it may preserve.

**Recurring neighboring concepts:** Scout investigations, Survey reports, Characterizations, neighborhood investigations, constitutional recovery reports, bounded inquiries, warrant, bounded question shape, implementation-evidence posture, investigation shape, produced artifact pattern, unsupported conclusions, preserved unknowns, and confidence.

**Recurring consumers:** Later Scout, Survey, Characterization, constitutional recovery, and bounded-inquiry artifacts can consume warrant-family evidence as methodological permission or boundary evidence. The current task consumes it as constitutional evidence, not implementation architecture.

**Recurring producers:** `survey_warrant_recurrence_investigation.md` is the direct producer. The recurring source material includes previous Scout investigations, Survey reports, Characterizations, neighborhood investigations, constitutional recovery reports, and bounded inquiries.

**Confidence:** Medium-high that survey warrant families recur as constitutional/investigation patterns. Low that they are implemented public inquiry identities like Question Families.

## Relationship evidence

### Question Shapes and Question Families

Supported relationship: **adjacent**, with partial implementation projection only in registered cases.

Recurring evidence shows Question Shapes can describe bounded forms of asking, while Question Families are exact implementation-backed public inquiry identities. The QuestionFamily Admission candidate in `docs/architectural_recovery_hit_list.md` explicitly frames admission as deciding whether a question shape is registered or handled. That supports adjacency: a question shape may be considered by an admission boundary, and a registered/handled shape may become or correspond to a Question Family.

The evidence does not support equality. Question Families are static rows and dispatch identities; Question Shapes recur more broadly in observation templates, bounded self-questions, Scout/Survey method, and narrative-neighborhood outputs. Many shapes are not registered as Question Families. Conversely, a Question Family includes more than shape: surface mapping, required args, authority boundary, diagnostic relationships, and implementation reasons.

### Question Shapes and Survey Warrant Families

Supported relationship: **recurring expressions of one larger concern**, specifically bounded inquiry form under evidence discipline.

`survey_warrant_recurrence_investigation.md` uses bounded question shape as one support criterion for a recurring survey warrant family, alongside implementation-evidence posture, investigation shape, and produced artifact pattern. This means Question Shape is a recurring component of Survey Warrant Family evidence, but not the whole warrant. A warrant family additionally constrains method, conclusion strength, artifact pattern, unsupported conclusions, and confidence.

The evidence does not support an implementation projection relationship. Survey Warrant Families are constitutional/investigation patterns, while Question Shapes are recurring inquiry forms that can appear inside those patterns.

### Question Families and Survey Warrant Families

Supported relationship: **adjacent**, not implementation projection.

Question Families are implementation-backed public inquiry identities and dispatch boundaries. Survey Warrant Families are constitutional/investigation authorization patterns for bounded reports. Both participate in bounded inquiry discipline and both refuse unsupported inference, but their evidence sources and consumers differ.

The strongest connection is indirect: constitutional and recovery documents list question-family dispatch alongside other specialized inquiry forms, and survey warrant recurrence uses question shape plus evidence posture to authorize bounded investigations. However, there is no recurring evidence that a Survey Warrant Family registers a Question Family, dispatches bounded ask, or owns Question Surface Inventory rows. There is also no recurring evidence that a Question Family grants survey warrant authority.

### Three-way relationship

Supported relationship: **adjacent recurring expressions of a larger bounded-inquiry concern**, with only one implementation-projected branch.

The larger concern visible across the repository is: bounded questions must preserve identity, evidence posture, authority boundary, consumers/producers, and unsupported conclusions. Question Shapes express recurring ask forms. Survey Warrant Families express recurring methodological authorization for investigation artifacts that use bounded question shapes. Question Families express the implementation-backed public inquiry identities that can be registered, explained, and dispatched.

Only Question Families have strong current implementation projection. Survey Warrant Families have constitutional/investigation projection. Question Shapes are a recurring descriptive bridge across both, but repository evidence does not make them a universal architecture owner or stabilized vocabulary.

## Supported relationships

- **Question Shapes ↔ Question Families:** Adjacent. Some registered Question Families may be implementation projections of supported question shapes, but only after explicit registry/admission evidence. Unsupported for unregistered shapes.
- **Question Shapes ↔ Survey Warrant Families:** Recurring expressions of one larger bounded-inquiry concern. Question Shape is one criterion or component used in Survey Warrant Family evidence, not the entire warrant.
- **Question Families ↔ Survey Warrant Families:** Adjacent. Both enforce bounded inquiry discipline, but one is an implementation dispatch identity and the other is a constitutional/investigation warrant pattern.
- **All three:** Partial convergence around bounded inquiry identity and evidence discipline, not equality and not a single owner.

## Unsupported relationships

- Unsupported: Question Shapes, Question Families, and Survey Warrant Families are equal concepts.
- Unsupported: Every Question Shape is or should be a Question Family.
- Unsupported: Every Question Family was recovered from a Survey Warrant Family.
- Unsupported: Survey Warrant Families are public bounded ask dispatch identities.
- Unsupported: Question Families grant constitutional survey warrant authority.
- Unsupported: Question Shapes have a single implementation registry or stabilized ontology in current repository evidence.
- Unsupported: The consumer hypothesis name `survey warrant families` should be promoted beyond the scoped recurrence investigation without further authority.

## Preserved unknowns

- Whether the repository will later stabilize `Question Shape` as a canonical architecture term remains unknown.
- Whether future QuestionFamily Admission work will explicitly convert some recurring question shapes into registered Question Families remains unknown.
- Whether Survey Warrant Families should become canonical constitutional vocabulary or remain a scoped investigation artifact remains unknown.
- Whether the supported Survey Warrant Families are complete remains unknown.
- Whether there are additional intermediate concepts between question shape, implementation family, and constitutional warrant remains unknown; this Scout does not invent them.

## Confidence

- **High** confidence that Question Families are implementation-backed public inquiry identities with registration, bounded dispatch, and presentation boundaries.
- **Medium-high** confidence that Survey Warrant Families recur as constitutional/investigation patterns, not implementation dispatch identities.
- **Medium** confidence that Question Shapes recur as descriptive bounded ask forms across investigation and reconciliation artifacts.
- **Medium** confidence in the three-way conclusion: adjacent recurring expressions of bounded inquiry discipline, with Question Families as the implementation-projected branch and Survey Warrant Families as the constitutional/investigation-projected branch.
- **Low** confidence in any stronger convergence claim.

Scout investigation complete.
