PRAGMA foreign_keys = ON;

-- SQLite constitutional witness slice 001.
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

CREATE VIEW competency_change_examination AS
SELECT
  c.competency_id,
  r.change_id,
  CASE
    WHEN r.change_family IS NULL OR r.observable_subject IS NULL THEN 'unknown_preserved'
    WHEN r.change_family <> c.responsibility_family
      OR r.observable_subject <> c.responsibility_subject THEN 'lawful_inactivity_irrelevant'
    WHEN r.authority_zone <> c.authority_zone THEN 'lawful_inactivity_authority_blocked'
    WHEN (c.requires_provenance = 1 AND r.provenance_ref IS NULL)
      OR (c.requires_evidence = 1 AND r.evidence_ref IS NULL)
      THEN 'lawful_inactivity_insufficient_evidence'
    ELSE 'bounded_permission_for_further_examination'
  END AS lawful_posture,
  CASE
    WHEN r.change_family IS NULL OR r.observable_subject IS NULL THEN 'subject_or_family_not_bound_enough_for_relevance'
    WHEN r.change_family <> c.responsibility_family
      OR r.observable_subject <> c.responsibility_subject THEN 'outside_bounded_responsibility'
    WHEN r.authority_zone <> c.authority_zone THEN 'outside_competency_authority_boundary'
    WHEN (c.requires_provenance = 1 AND r.provenance_ref IS NULL)
      OR (c.requires_evidence = 1 AND r.evidence_ref IS NULL)
      THEN 'required_evidence_or_provenance_absent'
    ELSE 'family_subject_evidence_provenance_and_authority_supported'
  END AS standing_reason,
  'relevance_result_not_execution_authorization_or_truth_establishment' AS forbidden_inference,
  r.assertion_truth_status
FROM bounded_competencies c
CROSS JOIN recorded_change_assertions r;

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
