import json, subprocess
import pytest

from seed_runtime.bounded_constitutional_question import produce_bounded_constitutional_question
from seed_runtime.candidate_examination_work import *
from seed_runtime.examination_frontier import CorpusMember, project_examination_frontier

LESSON_HASH="01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963"

def rep(kind="exact_text", rid="r", h="h", status="known"):
    return RepresentationVisibility(rid,kind,"a",h,"v",status)
def mem(mid="m", h="h", reps=(rep(),)):
    return BoundedCorpusMember(mid,"book","artifact",h,reps)
def contract(cid="c", need="exact_text", out="structural_projection", ver="v1", avail="available", mids=()):
    return ExaminationWorkContract(cid,"cap","kind",need,out,ver,avail,mids,("explicit contract",))
def workset(ms=(mem(),), cs=(contract(),)):
    return project_candidate_examination_work("corpus",tuple(ms),tuple(cs),("caller supplied contract visibility",))
def q():
    return produce_bounded_constitutional_question(operator_inquiry="x",inquiry_provenance="test",bounded_question="x",constitutional_intent="x",scope_status="bounded")

def test_compatible_candidate_identity_stability_and_version_sensitivity():
    ws=workset()
    assert len(ws.candidate_work)==1
    c=ws.candidate_work[0]
    assert c.compatibility_observation=="compatible" and c.available_matching_representation=="r"
    assert c.candidate_work_id==workset().candidate_work[0].candidate_work_id
    assert c.candidate_work_id!=workset((mem(h="h2"),)).candidate_work[0].candidate_work_id
    assert c.candidate_work_id!=workset(cs=(contract(ver="v2"),)).candidate_work[0].candidate_work_id

@pytest.mark.parametrize("bad", ["member","contract","candidate"])
def test_deterministic_duplicate_and_unknown_failures(bad):
    if bad=="member":
        with pytest.raises(CandidateExaminationWorkError, match="duplicate_corpus_member_id"): workset((mem("m"),mem("m")))
    elif bad=="contract":
        with pytest.raises(CandidateExaminationWorkError, match="duplicate_contract_id"): workset(cs=(contract("c"),contract("c")))
    else:
        with pytest.raises(CandidateExaminationWorkError, match="duplicate_candidate_work_id"): workset(cs=(contract("c1", mids=("m","m")),))
    with pytest.raises(CandidateExaminationWorkError, match="unknown_corpus_member"):
        workset(cs=(contract(mids=("missing",)),))

def test_observations_are_not_frontier_classifications_or_authorization():
    records = [
        workset((mem(reps=(rep("other"),)),)).candidate_work[0],
        workset(cs=(contract(avail="unavailable"),)).candidate_work[0],
        workset((mem(reps=(rep("other",status="unknown"),)),)).candidate_work[0],
        workset(cs=(contract(avail="unknown"),)).candidate_work[0],
    ]
    assert [r.compatibility_observation for r in records] == ["missing_required_representation","capability_unavailable","representation_unknown","contract_unknown"]
    assert records[0].missing_prerequisites == ("exact_text",)
    blob=json.dumps([r.to_json_dict() for r in records])
    forbidden="eligib examined blocked deferred failed selected priority authorized".split()
    assert not any(f in blob for f in forbidden)

def test_free_form_names_do_not_generate_ordering_and_render_notes():
    data={"corpus":{"corpus_id":"corpus","members":[mem().to_json_dict()]},"contracts":[contract().to_json_dict()],"candidate_work_names":["invent prose","compare"]}
    ws=project_candidate_examination_work(*input_from_json_dict(data))
    assert len(ws.candidate_work)==1
    ws2=workset((mem("b"),mem("a")), (contract("z"),contract("a")))
    assert [(r.corpus_member_id,r.contract_id) for r in ws2.candidate_work] == sorted((r.corpus_member_id,r.contract_id) for r in ws2.candidate_work)
    human=format_candidate_examination_work(ws)
    j=json.dumps(candidate_examination_work_json(ws))
    for note in BOUNDARY_NOTES:
        assert note in human and note in j
    assert ws.read_only and not ws.writes_event_ledger and not ws.mutates_cluster

def test_projection_is_read_only_no_events_actions_facts_or_execution():
    before=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    ws=workset()
    _=format_candidate_examination_work(ws); _=candidate_examination_work_json(ws)
    after=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    assert before==after
    blob=json.dumps(ws.to_json_dict()).lower()
    assert all(x not in blob for x in ["observation_id","evidence_id","runtime_fact_id","pending_action","event_ledger_entry"])

def test_mixed_corpus_proving_and_no_prose_or_comparison_invention():
    structural=contract("external_material_structure_v1","exact_text","structural_projection","external_material_structural_projection_v1")
    surface=contract("external_material_surface_features_v1","structural_projection","surface_feature_projection","external_material_surface_feature_projection_v1")
    acquire=contract("website_acquisition_orientation_v1","acquisition_target","raw_bytes","website_acquisition_orientation_v1",mids=("web",))
    members=(
        BoundedCorpusMember("web","website_target","Project Gutenberg acquisition target","",(rep("acquisition_target","gutenberg-target",""),)),
        BoundedCorpusMember("lesson","book","selected_lesson_006.txt",LESSON_HASH,(rep("exact_text","lesson-text",LESSON_HASH),rep("structural_projection","lesson-struct",LESSON_HASH),rep("surface_feature_projection","lesson-surface",LESSON_HASH))),
        BoundedCorpusMember("agents","repository","AGENTS.md","repohash",(rep("exact_text","agents-text","repohash"),rep("structural_projection","agents-struct","repohash"),rep("surface_feature_projection","agents-surface","repohash"))),
    )
    ws=project_candidate_examination_work("mixed",members,(structural,surface,acquire),("structural/surface contracts are implementation-backed; acquisition contract is caller-supplied visibility",))
    by={(r.corpus_member_id,r.contract_id):r for r in ws.candidate_work}
    assert by[("web","website_acquisition_orientation_v1")].compatibility_observation=="compatible"
    assert by[("web","website_acquisition_orientation_v1")].available_matching_representation=="gutenberg-target"
    assert by[("lesson","external_material_structure_v1")].compatibility_observation=="compatible"
    assert by[("lesson","external_material_surface_features_v1")].available_matching_representation=="lesson-struct"
    assert by[("agents","external_material_structure_v1")].compatibility_observation=="compatible"
    assert by[("agents","external_material_surface_features_v1")].compatibility_observation=="compatible"
    blob=json.dumps([r.to_json_dict() for r in ws.candidate_work]).lower()
    assert "prose" not in blob and "comparison" not in blob and "semantic correspondence" not in blob and "live gutenberg bytes" not in blob

def test_frontier_adapter_preserves_frontier_ownership_and_existing_behavior():
    ws=workset()
    fw=ws.to_frontier_candidate_work()
    f=project_examination_frontier(q(),"corpus","label",(CorpusMember("m","book","artifact","h"),),fw)
    item=f.work_items[0]
    assert item.candidate_work_id == ws.candidate_work[0].candidate_work_id
    assert hasattr(item,"classification") and item.classification.unknown and not hasattr(ws.candidate_work[0],"classification")
    # Existing public compatibility imports remain unchanged.
    import seed_runtime.external_material_testimony_binding, seed_runtime.external_material_structural_projection, seed_runtime.external_material_surface_feature_projection, seed_runtime.candidate_external_grammar, seed_runtime.capability_inventory, seed_runtime.execution, seed_runtime.pending_actions, seed_runtime.events
