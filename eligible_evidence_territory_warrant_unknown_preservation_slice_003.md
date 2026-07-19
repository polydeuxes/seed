# Eligible evidence territory warrant Unknown preservation slice 003

## Selected overcorrection

The selected overcorrection was the bounded inquiry frontier witness turning an unrecovered eligible-evidence-territory warrant into a runtime result that looked stronger than the investigation supported. The prior local witness correctly refused to infer required-family coverage from `eligible_evidence_territory_refs`, but its implementation/commentary shape risked reading the present absence of a recovered positive warrant as an always-non-operative family rule.

A second overreach was the shared operativity predicate treating `stale` or `unknown` currency and `unavailable` or `unknown` availability as non-operative for every frontier clause family, even though the current implementation evidence only ties those support coordinates to the evidence-territory family.

## Book expectation

The Book discipline starts from `Unknown / uncommitted`, requires evidence to move a subject toward a supported state, and stops at insufficient evidence rather than promoting absence into truth. That means tuple presence alone cannot create eligible-territory warrant, but failure to recover the warrant in this slice also cannot become a universal impossibility claim.

The same discipline preserves bounded unknowns and explicit stops. Therefore `unknown` currency or availability must remain distinguishable from stale or unavailable, and unsupported family-global gates must not be imposed on neighboring clause families without direct implementation or Book support.

## Current witness

The current witness is `BoundedInquiryFrontier`. It consumes already-preserved boundary testimony, computes operative clause refs, missing required clause families, conflict refs, standing refs, and read-only compatibility flags. The testimony layer preserves eligible territory references but does not select sources or observations.

Before this correction, `_is_operatively_coherent` globally blocked clauses with `evidence_currency in {"conflicting", "stale", "unknown"}` or `evidence_availability in {"conflicting", "unavailable", "unknown"}`. It also returned `False` for every `eligible_ineligible_evidence_territory` clause because no local positive warrant had been recovered. Public projection grouped unknown currency into `stale_clause_refs` and unknown availability into `unavailable_clause_refs`.

## Permanent-impossibility distinction

The corrected witness preserves the negative result only as present insufficiency: non-empty `eligible_evidence_territory_refs` still do not count toward required-family coverage, but the code no longer describes that as proof that future eligible-territory warrant is impossible. The eligible-territory branch now states that supplied refs and presently insufficient standing are preserved, tuple non-emptiness is not positive support, and absence of current support is not proof of future impossibility.

## Family-relative currency and availability finding

Direct implementation evidence showed currentness and availability fields on the boundary clause payload, but did not establish that these fields are universal operativity gates for all four required frontier families. The smallest correction keeps explicit `conflicting` currency/availability as material conflict input, keeps stale/unavailable visibility, and applies the current/available operativity requirement only inside the eligible-evidence-territory branch where the coordinate is evidence-territory-local.

Neighboring families are not made subject to an unsupported family-global policy: scope, resolution, and stopping clauses with unknown currency/availability can remain operative when their own standing, disposition, and family-local requirements are otherwise coherent.

## Unknown representation finding

The public artifact already had `unknown_clause_refs`, but that field means clause standing is `unknown`; it does not represent unknown currency or unknown availability. Reusing it for currency/availability would erase the difference between an unknown clause standing and an unknown support coordinate.

The smallest faithful representation is therefore explicit coordinate-local Unknown fields:

- `unknown_currency_clause_refs`
- `unknown_availability_clause_refs`

`stale_clause_refs` now contains only clauses whose currency is actually `stale`, and `unavailable_clause_refs` now contains only clauses whose availability is actually `unavailable`.

## Smallest correction

The implementation correction is bounded to `seed_runtime/bounded_inquiry_frontier.py`:

1. Remove stale/unknown currency and unavailable/unknown availability from the universal operativity gate.
2. Preserve explicit currency/availability conflicts as conflict-blocking.
3. Apply current/available checks only to `eligible_ineligible_evidence_territory` before the existing no-positive-warrant result.
4. Keep eligible-territory refs preserved and non-operative when no positive claim-relative warrant is recovered.
5. Split Unknown currency/availability into explicit public projection fields rather than silently reporting them as stale/unavailable.

## Focused tests

Focused tests in `tests/test_bounded_inquiry_frontier.py` now cover:

- eligible-territory ref present with no recovered positive warrant: preserved, non-operative, not counted toward required-family coverage, reported as missing `eligible_ineligible_evidence_territory`;
- `currency == stale`: preserved, non-operative for evidence territory, reported under `stale_clause_refs`;
- `currency == unknown`: preserved, non-operative for evidence territory, reported under `unknown_currency_clause_refs`, not under `stale_clause_refs`;
- `availability == unavailable`: preserved, non-operative for evidence territory, reported under `unavailable_clause_refs`;
- `availability == unknown`: preserved, non-operative for evidence territory, reported under `unknown_availability_clause_refs`, not under `unavailable_clause_refs`;
- neighboring frontier families with unknown currency/availability are not blocked by an unsupported universal gate.

## Preserved compatibility

The corrected witness preserves read-only behavior, testimony serialization, explicit conflict blocking, stale visibility, unavailable visibility, Unknown visibility, missing-required-family visibility, and the no-inquiry/no-source-selection/no-observation-selection/no-access-authorization/no-execution/no-recording/no-event-ledger-write/no-mutation boundary.

The change intentionally does not recover or invent a positive eligible-territory warrant shape, warrant engine, territory registry, admission layer, ownership system, generalized validation framework, or new frontier architecture.

## Remaining Unknowns

Remaining Unknowns are deliberately left unresolved:

- the future claim-relative shape that could positively warrant eligible evidence territory;
- whether additional family-local currentness or availability requirements exist for non-evidence frontier families;
- whether a future artifact should carry richer warranted / insufficient / Unknown / conflicting standings beyond the now-separated coordinate visibility fields.

How does the corrected witness preserve “no positive eligible-territory warrant currently recovered” without declaring the family constitutionally impossible, applying unsupported universal gates to neighboring families, or relabeling Unknown currency and availability as stale or unavailable?
