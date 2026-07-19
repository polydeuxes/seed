# Inquiry frontier boundary testimony asymmetry recovery 001

## Observed witness behavior

The implementation preserves `evidence_currency` and `evidence_availability` separately from `clause_standing`, `scope_disposition`, and `family_disposition`. In assembly, a clause is operative when it is `established`, belongs to the `inquiry` family, is not explicitly `conflicting` in currency or availability, and, for the scope family, has `scope_disposition == "included"`. Therefore `stale` and `unavailable` do not themselves remove operative coherence, while any explicit `conflicting` standing, scope disposition, currency, or availability becomes a material binding conflict and prevents frontier establishment.

Focused tests currently prove that stale, unavailable, out-of-scope, adjacent-family, and mixed properties remain separately visible. They also prove that unsupported, unknown, mixed, adjacent-family, and out-of-scope clauses are non-operative, and that an added conflicting clause prevents establishment. The focused test set does not isolate whether a required family supported only by stale or unavailable testimony may establish the frontier.

## Repository warrant found

The Book directly establishes the frontier's conjunctive identity and negative authority: a bounded inquiry frontier must preserve exact inquiry need or uncertainty, source/provenance, current movement or consumer-local boundary, included/excluded scope, available evidence territory, sufficiency and lawful stopping conditions, Unknowns, conflicts, and negative authority. It also says stale or unavailable evidence, a selected need by itself, wording similarity, list order, and other weak signals do not establish the frontier or admit inquiry, select sources/observations, open examination, authorize access, determine the answer, write the event ledger, or mutate state.

That Book text supports these distinctions:

```text
eligible evidence territory
!= evidence availability
!= evidence currency
!= admission
!= sufficiency
```

It does not directly say that stale or unavailable boundary testimony remains operative for required-family establishment. In fact, because the same Book sentence names `available evidence territory` as part of frontier identity and then says stale or unavailable evidence by itself does not establish the frontier, the Book does not provide a standalone warrant for stale/unavailable testimony to satisfy the evidence-territory requirement.

Adjacent constitutional grammar supports preserving stale and unavailable testimony without erasing it. Evidence grammar distinguishes evidence-shaped material, availability, provenance, support, and sufficiency; testimony grammar allows premise-relative consumption while preserving attribution, conflicts, and uncertainty without establishing fact; artifact standing grammar distinguishes reachability/availability from acceptance, admission, reliance, projection, recording, or action. Adjacent inquiry grammar also distinguishes frontier membership, eligibility, selection, dispatch, evidence gathering, answer, sufficiency, completion, conflict, Unknown preservation, and lawful inactivity.

The local recovery artifacts sharpen the same distinctions. The boundary-testimony slice says stale and unavailable evidence remain testimony attributes and do not rewrite clause standing. The bounded-frontier audit says stale evidence should be preserved as evidence-quality boundary testimony and may support a stale-support or refresh-required stopping condition, while unavailable evidence may be preserved as unavailable territory or a blocking boundary and may show current-resolution insufficiency without authorizing access. The same audit says conflicting testimony should be preserved and establishment refused unless a local owner has reconciled it.

## Scope of that warrant

The repository warrants preservation and classification of stale, unavailable, and conflicting testimony as different boundary conditions. It also warrants treating conflict as establishment-blocking unless reconciled.

The repository warrants stale/unavailable testimony as possibly relevant to boundary preservation, stopping, refresh-required conditions, blocking boundaries, and Unknown/insufficiency preservation. That warrant is not the same as a warrant that stale or unavailable testimony is fully operative evidence-territory establishment.

## Remaining Unknowns

- Whether `stale` but otherwise established testimony may be operative for every required clause family, or only for stopping/refresh-required boundary clauses, remains Unknown.
- Whether `unavailable` but otherwise established testimony may be operative for every required clause family, or only for unavailable-territory/blocking-boundary clauses, remains Unknown.
- Whether a required `eligible_ineligible_evidence_territory` clause with `evidence_availability == "unavailable"` should count as satisfying the Book's `available evidence territory` requirement remains Unknown and suspicious.
- Whether the implementation intentionally encodes a family-local convention that currency/availability are non-disqualifying unless conflicting remains Unknown.
- Whether tests should require stale-only or unavailable-only required-family support to establish, fail, or produce a more specific non-established state remains Unknown; the currently inspected focused tests do not settle that case.

## Final fidelity judgment

```text
supported by adjacent constitutional grammar
```

with a boundary note:

```text
implementation-local convention / possible implementation crossing
```

The asymmetry is repository-supported only at the level that `stale != withdrawn`, `unavailable != nonexistent`, and `conflicting != unavailable`: stale and unavailable testimony may remain preserved boundary testimony and may matter to stopping or blocking boundaries, while conflicting testimony blocks unreconciled establishment. The Book does not already establish the stronger implementation behavior that stale or unavailable testimony remains operative for required frontier establishment. If the implementation permits stale-only or unavailable-only required-family testimony to establish an otherwise complete frontier, that stronger behavior is not Book-established by the inspected grammar and may be an implementation crossing rather than a report error.
