.bail on
.headers off
.mode list

CREATE TEMP TABLE expected_postures(competency_id TEXT, change_id TEXT, lawful_posture TEXT);
INSERT INTO expected_postures VALUES
('competency:eye-evidence-local','case_a_relevant_supported','bounded_permission_for_further_examination'),
('competency:eye-evidence-local','case_b_irrelevant','lawful_inactivity_irrelevant'),
('competency:eye-evidence-local','case_c_insufficient_evidence','lawful_inactivity_insufficient_evidence'),
('competency:eye-evidence-local','case_d_unknown','unknown_preserved'),
('competency:eye-evidence-local','case_e_authority_blocked','lawful_inactivity_authority_blocked'),
('competency:eye-evidence-local','case_f_record_not_truth','bounded_permission_for_further_examination'),
('competency:eye-evidence-local','case_g_unrelated_no_universal_activity','lawful_inactivity_irrelevant');

CREATE TEMP TABLE assert_zero(label TEXT, failures INTEGER CHECK (failures = 0));

INSERT INTO assert_zero
SELECT 'expected posture missing', COUNT(*) FROM expected_postures e
LEFT JOIN competency_change_examination a
  ON a.competency_id=e.competency_id AND a.change_id=e.change_id AND a.lawful_posture=e.lawful_posture
WHERE a.change_id IS NULL;
SELECT 'posture cases pass';

INSERT INTO assert_zero
SELECT 'record promoted to truth', CASE WHEN EXISTS (
  SELECT 1 FROM recorded_assertion_truth_boundary
  WHERE change_id='case_f_record_not_truth'
    AND recorded_status='record_exists'
    AND assertion_truth_status='not_established'
    AND truth_boundary='recording_preserves_assertion_without_establishing_external_truth'
) THEN 0 ELSE 1 END;
SELECT 'record-not-truth case passes';

INSERT INTO assert_zero
SELECT 'unrelated record implied activity', CASE WHEN EXISTS (
  SELECT 1 FROM competency_activity_summary
  WHERE change_id='case_g_unrelated_no_universal_activity'
    AND competencies_with_bounded_permission=0
    AND universal_activity_boundary='no_universal_activity_implied'
) THEN 0 ELSE 1 END;
SELECT 'no universal activity case passes';

INSERT INTO assert_zero
SELECT 'forbidden inference missing', CASE WHEN EXISTS (
  SELECT 1 FROM competency_change_examination
  WHERE lawful_posture='bounded_permission_for_further_examination'
    AND forbidden_inference='relevance_result_not_execution_authorization_or_truth_establishment'
) THEN 0 ELSE 1 END;
SELECT 'forbidden inference boundary passes';
