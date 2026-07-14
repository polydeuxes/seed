import json

import pytest

from seed_runtime.candidate_external_grammar import (
    BOUNDARY_NOTES,
    CandidateExternalGrammarInput,
    CandidateExternalGrammarInputCandidate,
    CandidateExternalGrammarValidationError,
    assemble_candidate_external_grammar_set,
    candidate_external_grammar_json,
    format_candidate_external_grammar,
)


def _fixture():
    return CandidateExternalGrammarInput(
        representation_scope="neutral attributed sample set: fixture-001",
        candidates=(
            CandidateExternalGrammarInputCandidate(
                candidate_id="candidate-a",
                structural_claim="Records share a repeated two-element sequence shape.",
                claim_scope="$.records[*]",
                provenance=("caller:testimony:alpha",),
                supporting_testimony=("testimony-1", "testimony-2"),
                contradicting_testimony=("testimony-3",),
                unresolved_alternatives=("candidate-b", "opaque first element"),
                explicit_unknowns=("meaning of first element unknown",),
            ),
            CandidateExternalGrammarInputCandidate(
                candidate_id="candidate-b",
                structural_claim="Candidate B leaves the first element opaque.",
                claim_scope="$.records[*][0]",
                provenance=("caller:testimony:beta",),
                explicit_unknowns=("no supporting testimony supplied",),
            ),
        ),
        set_unknowns=("sample-set completeness unknown",),
    )


def test_caller_supplied_candidates_are_preserved_without_ranking_or_rewriting():
    artifact = assemble_candidate_external_grammar_set(_fixture())
    data = candidate_external_grammar_json(artifact)

    assert data["artifact_type"] == "CandidateExternalGrammarSet"
    assert data["representation_scope"] == "neutral attributed sample set: fixture-001"
    assert [c["candidate_id"] for c in data["candidates"]] == ["candidate-a", "candidate-b"]
    assert data["candidates"][0]["structural_claim"] == "Records share a repeated two-element sequence shape."
    assert data["candidates"][0]["supporting_testimony"] == ["testimony-1", "testimony-2"]
    assert data["candidates"][0]["contradicting_testimony"] == ["testimony-3"]
    assert data["candidates"][0]["unresolved_alternatives"] == ["candidate-b", "opaque first element"]
    assert data["candidates"][0]["explicit_unknowns"] == ["meaning of first element unknown"]
    assert data["set_unknowns"] == ["sample-set completeness unknown"]
    candidate_payload = json.dumps(data["candidates"]).lower()
    for marker in ("rank", "accepted", "rejected", "selected", "verified", "promoted", "confidence"):
        assert marker not in candidate_payload


def test_support_absence_and_contradiction_absence_are_not_rewritten_as_boundary_truth():
    artifact = assemble_candidate_external_grammar_set(_fixture())
    second = candidate_external_grammar_json(artifact)["candidates"][1]

    assert second["supporting_testimony"] == []
    assert second["contradicting_testimony"] == []
    rendered = format_candidate_external_grammar(artifact)
    assert "Absence of support is not contradiction." in rendered
    assert "Absence of contradiction is not verification." in rendered
    assert "semantic" in rendered
    assert "translator readiness" in rendered
    assert "translation_specification" not in json.dumps(candidate_external_grammar_json(artifact))
    assert "parser" not in json.dumps(candidate_external_grammar_json(artifact)).lower()
    assert "tool_realization" not in json.dumps(candidate_external_grammar_json(artifact))


def test_empty_candidate_set_is_not_failure_and_read_only_flags_are_fixed():
    artifact = assemble_candidate_external_grammar_set(
        CandidateExternalGrammarInput(representation_scope="empty candidate fixture")
    )

    data = candidate_external_grammar_json(artifact)
    assert data["candidates"] == []
    assert data["read_only"] is True
    assert data["writes_event_ledger"] is False
    assert data["mutates_cluster"] is False
    assert data["boundary_notes"] == list(BOUNDARY_NOTES)
    assert "zero-candidate set, not failure" in format_candidate_external_grammar(artifact)


def test_duplicate_candidate_ids_fail_deterministically():
    supplied = CandidateExternalGrammarInput(
        representation_scope="duplicate fixture",
        candidates=(
            CandidateExternalGrammarInputCandidate("dup", "shape one"),
            CandidateExternalGrammarInputCandidate("dup", "shape two"),
        ),
    )

    with pytest.raises(CandidateExternalGrammarValidationError, match="duplicate candidate_id: dup"):
        assemble_candidate_external_grammar_set(supplied)


def test_json_input_consumes_caller_supplied_testimony_only():
    supplied = CandidateExternalGrammarInput.from_json_dict(
        {
            "representation_scope": "json fixture",
            "candidates": [
                {
                    "candidate_id": "caller-candidate",
                    "structural_claim": "The value at path $.items[*].kind remains stable across supplied samples.",
                    "supporting_testimony": ["caller-testimony"],
                    "contradicting_testimony": [],
                }
            ],
            "set_unknowns": ["caller did not supply a universal grammar"],
        }
    )

    artifact = assemble_candidate_external_grammar_set(supplied)
    data = candidate_external_grammar_json(artifact)
    assert data["candidates"][0]["supporting_testimony"] == ["caller-testimony"]
    assert data["candidates"][0]["provenance"] == []


def test_cli_human_and_json_rendering_are_deterministic(tmp_path, capsys):
    path = tmp_path / "candidate.json"
    path.write_text(
        json.dumps(
            {
                "representation_scope": "cli fixture",
                "candidates": [
                    {
                        "candidate_id": "first",
                        "structural_claim": "Candidate A treats the first element as a structural discriminator.",
                        "claim_scope": "$[0]",
                        "supporting_testimony": ["t1"],
                        "contradicting_testimony": ["t2"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    import scripts.seed_local as seed_local

    assert seed_local.main(["--candidate-external-grammar", str(path)]) == 0
    human = capsys.readouterr().out
    assert "Candidate External Grammar Set" in human
    assert "candidate_id: first" in human
    assert "Supporting and contradicting testimony relationships are preserved, not evaluated." in human

    assert seed_local.main(["--candidate-external-grammar", str(path), "--json"]) == 0
    parsed = json.loads(capsys.readouterr().out)
    assert parsed["representation_scope"] == "cli fixture"
    assert parsed["candidates"][0]["candidate_id"] == "first"
    assert parsed["candidates"][0]["supporting_testimony"] == ["t1"]
    assert parsed["candidates"][0]["contradicting_testimony"] == ["t2"]
