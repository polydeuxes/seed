.bail on
.headers off
.mode list

CREATE TEMP TABLE expected_postures(competency_id TEXT, change_id TEXT, lawful_posture TEXT);
INSERT INTO expected_postures VALUES
('competency:evidence-boundary-local-observation','case_a_relevant_supported','bounded_permission_for_further_examination'),
('competency:evidence-boundary-local-observation','case_b_irrelevant','lawful_inactivity_irrelevant'),
('competency:evidence-boundary-local-observation','case_c_insufficient_evidence','lawful_inactivity_insufficient_evidence'),
('competency:evidence-boundary-local-observation','case_d_unknown','unknown_preserved'),
('competency:evidence-boundary-local-observation','case_e_authority_blocked','lawful_inactivity_authority_blocked'),
('competency:evidence-boundary-local-observation','case_f_record_not_truth','bounded_permission_for_further_examination'),
('competency:evidence-boundary-local-observation','case_g_unrelated_no_universal_activity','lawful_inactivity_irrelevant'),
('competency:evidence-boundary-local-observation','case_h_bound_support','bounded_permission_for_further_examination'),
('competency:evidence-boundary-local-observation','case_i_dangling_evidence','lawful_inactivity_dangling_evidence'),
('competency:evidence-boundary-local-observation','case_j_dangling_provenance','lawful_inactivity_dangling_provenance'),
('competency:evidence-boundary-local-observation','case_k_other_subject','lawful_inactivity_support_mismatch'),
('competency:evidence-boundary-local-observation','case_l_unknown_binding','unknown_preserved'),
('competency:evidence-boundary-local-observation','case_m_authority_mismatch','lawful_inactivity_support_mismatch'),
('competency:evidence-boundary-local-observation','case_n_represented_not_verified','bounded_permission_for_further_examination'),
('competency:evidence-boundary-local-observation','case_o_reference_name_only','lawful_inactivity_dangling_evidence'),
('competency:evidence-boundary-local-observation','case_p_same_source_rows','bounded_permission_for_further_examination'),
('competency:evidence-boundary-local-observation','case_q_conflicting_provenance_refs','unknown_preserved');

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
    AND forbidden_inference='support_binding_not_truth_fact_execution_authorization_or_current_state'
) THEN 0 ELSE 1 END;
SELECT 'forbidden inference boundary passes';

INSERT INTO assert_zero
SELECT 'dangling evidence did not remain explicit', CASE WHEN EXISTS (
  SELECT 1 FROM support_binding_examination
  WHERE change_id='case_i_dangling_evidence'
    AND evidence_standing='dangling_evidence_reference'
) THEN 0 ELSE 1 END;
SELECT 'dangling evidence case passes';

INSERT INTO assert_zero
SELECT 'dangling provenance did not remain explicit', CASE WHEN EXISTS (
  SELECT 1 FROM support_binding_examination
  WHERE change_id='case_j_dangling_provenance'
    AND provenance_standing='dangling_provenance_reference'
) THEN 0 ELSE 1 END;
SELECT 'dangling provenance case passes';

INSERT INTO assert_zero
SELECT 'unknown support binding not preserved', CASE WHEN EXISTS (
  SELECT 1 FROM support_binding_examination
  WHERE change_id='case_l_unknown_binding'
    AND evidence_standing='unknown_evidence_subject_or_claim_binding'
) THEN 0 ELSE 1 END;
SELECT 'unknown binding case passes';

INSERT INTO assert_zero
SELECT 'represented provenance promoted too far', CASE WHEN EXISTS (
  SELECT 1 FROM support_forbidden_inference_audit
  WHERE change_id='case_n_represented_not_verified'
    AND provenance_standing='represented_provenance_not_verified'
    AND provenance_verification_boundary='lineage_represented_not_independently_verified'
    AND producer_occurrence_boundary='producer_occurrence_not_established'
) THEN 0 ELSE 1 END;
SELECT 'represented provenance boundary passes';

INSERT INTO assert_zero
SELECT 'reference name alone supplied standing', CASE WHEN EXISTS (
  SELECT 1 FROM competency_change_examination
  WHERE change_id='case_o_reference_name_only'
    AND lawful_posture='lawful_inactivity_dangling_evidence'
) THEN 0 ELSE 1 END;
SELECT 'reference-name-alone case passes';

INSERT INTO assert_zero
SELECT 'same source rows became corroboration', CASE WHEN EXISTS (
  SELECT 1 FROM support_source_independence_boundary
  WHERE change_id='case_p_same_source_rows'
    AND represented_support_rows=2
    AND represented_source_identities=1
    AND independence_boundary='multiple_rows_do_not_establish_independent_corroboration_or_fact_standing'
) THEN 0 ELSE 1 END;
SELECT 'same-source non-corroboration case passes';


INSERT INTO assert_zero
SELECT 'conflicting provenance references were collapsed by COALESCE', CASE WHEN EXISTS (
  SELECT 1 FROM support_binding_examination
  WHERE change_id='case_q_conflicting_provenance_refs'
    AND assertion_provenance_ref='prov:q-assertion'
    AND evidence_provenance_ref='prov:q-evidence'
    AND effective_provenance_ref='prov:q-evidence'
    AND provenance_standing='conflicting_provenance_references_preserved'
) THEN 0 ELSE 1 END;
SELECT 'conflicting provenance reference boundary passes';
