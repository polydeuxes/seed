INSERT INTO book_clause_sources VALUES
('recording.assertion-not-truth', 'book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md', 'Recovered clauses for recorded-change witnesses / 05.Recording.A', 'Recording creates retrievable assertion-bearing material without establishing truth.'),
('events.record-not-fact', 'book_of_seed/06-state-and-projection/events-facts-and-state.md', 'Initial resolution', 'Events record assertions; facts and state require separate standing.'),
('competency.bounded-relevance', 'book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md', 'Recovered clauses for bounded examination witnesses / 04.Examination.A', 'Applicability or relevance is distinct from selection, execution, and fact establishment.'),
('authority.no-expansion', 'book_of_seed/08-authority-communication-and-stopping/authority-scope.md', 'Initial resolution', 'Internal records cannot create or enlarge authority.'),
('refusal.non-performance', 'book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md', 'Initial resolution', 'Non-performance reasons must remain distinguishable from successful action.');

INSERT INTO bounded_competencies VALUES
('competency:eye-evidence-local', 'constitutional_change', 'evidence_boundary', 'local_observation', 1, 1, 'inactive_when_irrelevant_unknown_unsupported_or_authority_blocked', 'competency.bounded-relevance'),
('competency:projection-cache-local', 'constitutional_change', 'projection_cache', 'local_observation', 1, 1, 'inactive_when_irrelevant_unknown_unsupported_or_authority_blocked', 'competency.bounded-relevance'),
('competency:external-admin', 'constitutional_change', 'evidence_boundary', 'external_admin', 1, 1, 'inactive_when_irrelevant_unknown_unsupported_or_authority_blocked', 'authority.no-expansion');

INSERT INTO recorded_change_assertions VALUES
('case_a_relevant_supported', 'constitutional_change', 'evidence_boundary', 'local_observation', 'fixture:operator-note', 'prov:a', 'evidence:a', 'Evidence boundary wording changed in Book fixture.', 'not_established', 'recording.assertion-not-truth'),
('case_b_irrelevant', 'constitutional_change', 'projection_cache', 'local_observation', 'fixture:operator-note', 'prov:b', 'evidence:b', 'Projection cache note changed in Book fixture.', 'not_established', 'recording.assertion-not-truth'),
('case_c_insufficient_evidence', 'constitutional_change', 'evidence_boundary', 'local_observation', 'fixture:operator-note', 'prov:c', NULL, 'Evidence boundary change lacks evidence reference.', 'not_established', 'recording.assertion-not-truth'),
('case_d_unknown', NULL, 'evidence_boundary', 'local_observation', 'fixture:operator-note', 'prov:d', 'evidence:d', 'Change family is not bound enough for relevance.', 'not_established', 'recording.assertion-not-truth'),
('case_e_authority_blocked', 'constitutional_change', 'evidence_boundary', 'external_admin', 'fixture:operator-note', 'prov:e', 'evidence:e', 'Evidence boundary change lies outside local authority.', 'not_established', 'recording.assertion-not-truth'),
('case_f_record_not_truth', 'constitutional_change', 'evidence_boundary', 'local_observation', 'fixture:mechanical-insert', 'prov:f', 'evidence:f', 'Mechanically valid assertion is preserved but not verified.', 'not_established', 'recording.assertion-not-truth'),
('case_g_unrelated_no_universal_activity', 'constitutional_change', 'unrelated_subject', 'local_observation', 'fixture:operator-note', 'prov:g', 'evidence:g', 'Unrelated record must not awaken all competencies.', 'not_established', 'recording.assertion-not-truth');
