PRAGMA foreign_keys = ON;

-- SQLite constitutional witness slices 001-002.
-- Boundary: deterministic side-by-side witness only; not production schema.

CREATE TABLE book_clause_sources (
  clause_id TEXT PRIMARY KEY,
  source_path TEXT NOT NULL,
  source_heading TEXT NOT NULL,
  bounded_assertion TEXT NOT NULL
);

CREATE TABLE recorded_change_assertions (
  change_id TEXT PRIMARY KEY,
  change_family TEXT,
  observable_subject TEXT,
  authority_zone TEXT,
  producer_attribution TEXT NOT NULL,
  provenance_ref TEXT,
  evidence_ref TEXT,
  assertion_text TEXT NOT NULL,
  assertion_truth_status TEXT NOT NULL DEFAULT 'not_established'
    CHECK (assertion_truth_status IN ('not_established')),
  book_clause_id TEXT NOT NULL REFERENCES book_clause_sources(clause_id)
);

CREATE TABLE bounded_competencies (
  competency_id TEXT PRIMARY KEY,
  responsibility_family TEXT NOT NULL,
  responsibility_subject TEXT NOT NULL,
  authority_zone TEXT NOT NULL,
  requires_provenance INTEGER NOT NULL CHECK (requires_provenance IN (0,1)),
  requires_evidence INTEGER NOT NULL CHECK (requires_evidence IN (0,1)),
  stop_condition TEXT NOT NULL,
  book_clause_id TEXT NOT NULL REFERENCES book_clause_sources(clause_id)
);

CREATE TABLE represented_provenance_material (
  provenance_id TEXT PRIMARY KEY,
  source_attribution TEXT NOT NULL,
  source_context TEXT,
  applies_to_change_id TEXT,
  applies_to_evidence_id TEXT,
  authority_zone TEXT,
  represented_lineage_status TEXT NOT NULL
    CHECK (represented_lineage_status IN ('represented_lineage','internally_conflicting')),
  verification_status TEXT NOT NULL
    CHECK (verification_status IN ('not_independently_verified','independently_verified')),
  producer_occurrence_status TEXT NOT NULL DEFAULT 'not_established'
    CHECK (producer_occurrence_status IN ('not_established')),
  book_clause_id TEXT NOT NULL REFERENCES book_clause_sources(clause_id)
);

CREATE TABLE represented_evidence_material (
  evidence_id TEXT PRIMARY KEY,
  evidence_kind TEXT NOT NULL,
  source_attribution TEXT NOT NULL,
  source_identity TEXT NOT NULL,
  source_context TEXT,
  responsibility_family TEXT,
  observable_subject TEXT,
  supported_change_id TEXT,
  authority_zone TEXT,
  preservation_horizon TEXT NOT NULL,
  confidence_label TEXT NOT NULL DEFAULT 'represented_not_warrant',
  provenance_ref TEXT,
  book_clause_id TEXT NOT NULL REFERENCES book_clause_sources(clause_id)
);

CREATE VIEW support_binding_examination AS
SELECT
  c.competency_id,
  r.change_id,
  r.evidence_ref,
  r.provenance_ref AS assertion_provenance_ref,
  e.evidence_id AS bound_evidence_id,
  e.provenance_ref AS evidence_provenance_ref,
  COALESCE(e.provenance_ref, r.provenance_ref) AS effective_provenance_ref,
  p.provenance_id AS bound_provenance_id,
  CASE
    WHEN c.requires_evidence = 0 THEN 'not_required'
    WHEN r.evidence_ref IS NULL THEN 'missing_evidence_reference'
    WHEN e.evidence_id IS NULL THEN 'dangling_evidence_reference'
    WHEN e.responsibility_family IS NULL OR e.observable_subject IS NULL OR e.supported_change_id IS NULL THEN 'unknown_evidence_subject_or_claim_binding'
    WHEN e.responsibility_family <> c.responsibility_family
      OR e.observable_subject <> c.responsibility_subject
      OR e.supported_change_id <> r.change_id THEN 'evidence_subject_or_claim_mismatch'
    WHEN e.authority_zone IS NULL THEN 'unknown_evidence_authority_binding'
    WHEN e.authority_zone <> c.authority_zone THEN 'evidence_authority_mismatch'
    WHEN e.source_context IS NULL THEN 'unknown_evidence_source_context'
    ELSE 'applicable_represented_evidence'
  END AS evidence_standing,
  CASE
    WHEN c.requires_provenance = 0 THEN 'not_required'
    WHEN COALESCE(e.provenance_ref, r.provenance_ref) IS NULL THEN 'missing_provenance_reference'
    WHEN p.provenance_id IS NULL THEN 'dangling_provenance_reference'
    WHEN p.represented_lineage_status = 'internally_conflicting' THEN 'conflicting_provenance_preserved'
    WHEN p.applies_to_change_id IS NULL AND p.applies_to_evidence_id IS NULL THEN 'unknown_provenance_applicability'
    WHEN NOT (p.applies_to_change_id = r.change_id OR p.applies_to_evidence_id = e.evidence_id) THEN 'provenance_applicability_mismatch'
    WHEN p.authority_zone IS NULL THEN 'unknown_provenance_authority_binding'
    WHEN p.authority_zone <> c.authority_zone THEN 'provenance_authority_mismatch'
    WHEN p.verification_status = 'not_independently_verified' THEN 'represented_provenance_not_verified'
    ELSE 'represented_provenance_independently_verified'
  END AS provenance_standing,
  CASE
    WHEN p.provenance_id IS NULL THEN 'no_provenance_material_bound'
    WHEN p.verification_status = 'independently_verified' THEN 'lineage_independently_verified_for_this_witness_only'
    ELSE 'lineage_represented_not_independently_verified'
  END AS provenance_verification_boundary,
  'producer_occurrence_not_established' AS producer_occurrence_boundary,
  'support_binding_not_truth_fact_execution_authorization_or_current_state' AS forbidden_inference
FROM bounded_competencies c
CROSS JOIN recorded_change_assertions r
LEFT JOIN represented_evidence_material e ON e.evidence_id = r.evidence_ref
LEFT JOIN represented_provenance_material p ON p.provenance_id = COALESCE(e.provenance_ref, r.provenance_ref);

CREATE VIEW competency_change_examination AS
SELECT
  s.competency_id,
  s.change_id,
  CASE
    WHEN r.change_family IS NULL OR r.observable_subject IS NULL THEN 'unknown_preserved'
    WHEN r.change_family <> c.responsibility_family
      OR r.observable_subject <> c.responsibility_subject THEN 'lawful_inactivity_irrelevant'
    WHEN r.authority_zone <> c.authority_zone THEN 'lawful_inactivity_authority_blocked'
    WHEN s.evidence_standing = 'missing_evidence_reference' THEN 'lawful_inactivity_insufficient_evidence'
    WHEN s.evidence_standing = 'dangling_evidence_reference' THEN 'lawful_inactivity_dangling_evidence'
    WHEN s.provenance_standing = 'missing_provenance_reference' THEN 'lawful_inactivity_insufficient_provenance'
    WHEN s.provenance_standing = 'dangling_provenance_reference' THEN 'lawful_inactivity_dangling_provenance'
    WHEN s.evidence_standing LIKE 'unknown_%' OR s.provenance_standing LIKE 'unknown_%' THEN 'unknown_preserved'
    WHEN s.evidence_standing LIKE '%mismatch' OR s.provenance_standing LIKE '%mismatch' THEN 'lawful_inactivity_support_mismatch'
    WHEN s.provenance_standing = 'conflicting_provenance_preserved' THEN 'unknown_preserved'
    ELSE 'bounded_permission_for_further_examination'
  END AS lawful_posture,
  CASE
    WHEN r.change_family IS NULL OR r.observable_subject IS NULL THEN 'subject_or_family_not_bound_enough_for_relevance'
    WHEN r.change_family <> c.responsibility_family
      OR r.observable_subject <> c.responsibility_subject THEN 'outside_bounded_responsibility'
    WHEN r.authority_zone <> c.authority_zone THEN 'outside_competency_authority_boundary'
    WHEN s.evidence_standing <> 'applicable_represented_evidence' THEN s.evidence_standing
    WHEN s.provenance_standing NOT IN ('represented_provenance_not_verified','represented_provenance_independently_verified','not_required') THEN s.provenance_standing
    WHEN s.provenance_standing = 'represented_provenance_not_verified' THEN 'family_subject_authority_and_represented_lineage_supported_without_truth_or_verification'
    ELSE 'family_subject_evidence_provenance_and_authority_supported'
  END AS standing_reason,
  s.forbidden_inference,
  r.assertion_truth_status
FROM support_binding_examination s
JOIN bounded_competencies c ON c.competency_id = s.competency_id
JOIN recorded_change_assertions r ON r.change_id = s.change_id;

CREATE VIEW support_forbidden_inference_audit AS
SELECT
  competency_id,
  change_id,
  bound_evidence_id,
  bound_provenance_id,
  evidence_standing,
  provenance_standing,
  provenance_verification_boundary,
  producer_occurrence_boundary,
  forbidden_inference,
  'row_or_reference_presence_does_not_create_constitutional_warrant' AS referential_integrity_boundary
FROM support_binding_examination;

CREATE VIEW support_source_independence_boundary AS
SELECT
  r.change_id,
  COUNT(e.evidence_id) AS represented_support_rows,
  COUNT(DISTINCT e.source_identity) AS represented_source_identities,
  'multiple_rows_do_not_establish_independent_corroboration_or_fact_standing' AS independence_boundary
FROM recorded_change_assertions r
LEFT JOIN represented_evidence_material e ON e.supported_change_id = r.change_id
GROUP BY r.change_id;

CREATE VIEW recorded_assertion_truth_boundary AS
SELECT
  change_id,
  'record_exists' AS recorded_status,
  assertion_truth_status,
  CASE assertion_truth_status
    WHEN 'not_established' THEN 'recording_preserves_assertion_without_establishing_external_truth'
  END AS truth_boundary
FROM recorded_change_assertions;

CREATE VIEW competency_activity_summary AS
SELECT
  change_id,
  SUM(CASE WHEN lawful_posture = 'bounded_permission_for_further_examination' THEN 1 ELSE 0 END) AS competencies_with_bounded_permission,
  COUNT(*) AS competencies_examined,
  'no_universal_activity_implied' AS universal_activity_boundary
FROM competency_change_examination
GROUP BY change_id;
