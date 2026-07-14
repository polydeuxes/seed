import json

from campaigns.graded_lessons_supervised_grammar_apprenticeship_campaign_001.campaign import (
    EXPECTED_SHA256,
    annotations,
    campaign_record,
    candidate_outputs,
    lesson_selection,
    selected_lesson_bytes,
    source_identity,
    supervision_trace,
    validate_source_identity,
)


def test_exact_source_hash_and_byte_length_are_preserved():
    identity = validate_source_identity()
    assert identity.sha256 == EXPECTED_SHA256
    assert identity.byte_length == len(selected_lesson_bytes()) == 1628


def test_selected_material_bounds_and_identity_are_preserved():
    selection = lesson_selection()
    assert selection.exact_bounds == "selected_lesson_006.txt lines 1-4; Project Gutenberg web-rendered text lines 59-62 in the retrieval view"
    assert selection.selected_text.encode("utf-8") == selected_lesson_bytes()
    assert selection.parent_source_sha256 == source_identity().sha256


def test_annotations_retain_exact_references_and_authorship():
    records = annotations()
    assert all(a.material_reference.startswith("selected_lesson_006.txt:") for a in records)
    assert {a.supplied_by for a in records} == {"campaign author supplied"}
    assert any(a.annotation_kind == "candidate_rule_statement" for a in records)


def test_human_interpretation_is_not_attributed_to_seed():
    for annotation in annotations():
        assert annotation.supplied_by != "Seed supplied"
    human_steps = [s for s in supervision_trace() if "appears" in s.operation]
    assert human_steps
    assert {s.supplied_by for s in human_steps} == {"campaign author supplied"}


def test_candidate_testimony_references_survive_canonical_handoff():
    output = candidate_outputs()["json"]
    testimony = output["candidates"][0]["supporting_testimony"]
    assert testimony[0] == "source:gl001:selected_lesson_006:L1-L3#ann_model_intemperance"
    assert output["read_only"] is True
    assert output["writes_event_ledger"] is False
    assert output["mutates_cluster"] is False


def test_competing_candidates_remain_unranked_and_no_semantic_truth_added():
    output = candidate_outputs()["json"]
    assert [c["candidate_id"] for c in output["candidates"]] == [
        "gl001_pair_label_example",
        "gl001_repeated_two_part_structure",
        "gl001_model_then_exercise",
    ]
    serialized = json.dumps(output).lower()
    for forbidden in ["winner", "ranked_first", "true rule", "seed read"]:
        assert forbidden not in serialized


def test_deterministic_human_and_json_output():
    first = candidate_outputs()
    second = candidate_outputs()
    assert first["human"] == second["human"]
    assert first["json"] == second["json"]


def test_campaign_record_keeps_live_material_distinct_from_synthetic_fixtures():
    record = campaign_record()
    assert record["source_identity"]["reported_title"] == "Graded Lessons in English"
    assert "synthetic" not in json.dumps(record).lower()


def test_no_event_ledger_or_projected_state_or_cluster_mutation_surface():
    output = candidate_outputs()["json"]
    assert output["writes_event_ledger"] is False
    assert output["mutates_cluster"] is False
    assert "projected_state" not in json.dumps(campaign_record()).lower()
