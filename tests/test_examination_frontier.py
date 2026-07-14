import copy, json, subprocess, sys
from pathlib import Path

import pytest

from seed_runtime.bounded_constitutional_question import produce_bounded_constitutional_question
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.examination_frontier import *

LESSON_HASH="01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963"

def q():
    return produce_bounded_constitutional_question(operator_inquiry="examine bounded corpus", inquiry_provenance="testimony", bounded_question="For known artifacts and candidate work, what is eligible, examined, blocked, unsupported, deferred, failed, or Unknown?", constitutional_intent="frontier projection", scope_status="bounded", unknowns=("campaign history absent",))

def members(hash="h1"):
    return (CorpusMember("m1","book","selected_lesson_006.txt",hash), CorpusMember("repo","repository","AGENTS.md","rh"), CorpusMember("web","website_target","Project Gutenberg homepage target",""))

def work(**kw):
    d=dict(candidate_work_id="w1", corpus_member_id="m1", work_kind="external-material structural projection", capability_id="external_material_structure", convention="external_material_structural_projection_v1", compatibility_status="compatible", authorization_status="authorized")
    d.update(kw); return CandidateWork(**d)

def frontier(ws, ms=None): return project_examination_frontier(q(),"c1","corpus", ms or members(), tuple(ws))

def test_identity_validation_determinism_and_summary_counts():
    f=frontier([work()])
    assert f.artifact_type=="ExaminationFrontier" and f.read_only and not f.writes_event_ledger and not f.mutates_cluster
    assert f.work_items[0].classification.eligible and not hasattr(f.work_items[0], "priority_rank") and not hasattr(f.work_items[0], "selected")
    assert f.work_items[0].work_item_id == frontier([work()]).work_items[0].work_item_id
    assert f.work_items[0].work_item_id != frontier([work()], members("h2")).work_items[0].work_item_id
    assert f.work_items[0].work_item_id != frontier([work(convention="v2")]).work_items[0].work_item_id
    assert f.summary_counts["eligible"] == sum(i.classification.eligible for i in f.work_items)
    with pytest.raises(ExaminationFrontierError, match="duplicate_corpus_member_id"): frontier([work()], members()+ (CorpusMember("m1","x","x"),))
    with pytest.raises(ExaminationFrontierError, match="duplicate_candidate_work_id"): frontier([work(), work()])
    with pytest.raises(ExaminationFrontierError, match="unknown_corpus_member"): frontier([work(corpus_member_id="missing")])
    ordered=frontier([work(candidate_work_id="b",work_kind="b"), work(candidate_work_id="a",work_kind="a")]).work_items
    assert [i.work_item_id for i in ordered] == sorted(i.work_item_id for i in ordered)

def test_existing_result_matching_and_orthogonal_classification():
    r=WorkResultReference("r1","m1","h1","external-material structural projection","external_material_structure","external_material_structural_projection_v1","completed")
    item=frontier([work(existing_results=(r,))]).work_items[0]
    assert item.classification.examined and not item.classification.eligible
    blob=json.dumps(item.to_json_dict())
    assert all(s not in blob.lower() for s in ["complete verdict","true claim"])
    assert "Examined work is not necessarily understood" in blob
    bad=WorkResultReference("r1","repo","h1","external-material structural projection","external_material_structure","external_material_structural_projection_v1","completed")
    with pytest.raises(ExaminationFrontierError, match="existing_result_work_mismatch"): frontier([work(existing_results=(bad,))])
    combo=frontier([work(failure_references=("attempt failed",))]).work_items[0].classification
    assert combo.failed and combo.eligible and not combo.blocked and not combo.unsupported

def test_classification_boundaries_conflicts_deferred_unknown():
    assert frontier([work(blockers=("environment access failure before live bytes",))]).work_items[0].classification.blocked
    assert not frontier([work(blockers=("dependency unavailable",))]).work_items[0].classification.unsupported
    u=frontier([work(compatibility_status="unsupported", authorization_status="not_applicable", capability_id="")]).work_items[0]
    assert u.classification.unsupported and not u.classification.blocked
    assert "prohibited" not in json.dumps(u.to_json_dict()).lower()
    assert frontier([work(deferral_testimony=("campaign author deferred",))]).work_items[0].classification.deferred
    assert not frontier([work()]).work_items[0].classification.deferred
    unk=frontier([work(compatibility_status="unknown", authorization_status="unknown")]).work_items[0]
    assert unk.classification.unknown and not unk.classification.eligible
    conflict=frontier([work(compatibility_status="unsupported", capability_id="", supplied_status="eligible")]).work_items[0]
    assert conflict.classification.conflict and conflict.classification.unknown

def test_cli_human_json_inventory_shape_and_read_only(tmp_path):
    data={"bounded_inquiry": q().__dict__, "corpus":{"corpus_id":"c1","members":[m.to_json_dict() for m in members()]}, "candidate_work":[work().__dict__]}
    p=tmp_path/"frontier.json"; p.write_text(json.dumps(data))
    before=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    h=subprocess.run([sys.executable,"scripts/seed_local.py","--examination-frontier",str(p)],text=True,capture_output=True,check=True).stdout
    j=json.loads(subprocess.run([sys.executable,"scripts/seed_local.py","--examination-frontier",str(p),"--json"],text=True,capture_output=True,check=True).stdout)
    after=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    assert before==after and "The frontier is not a scheduler" in h
    assert j["artifact_type"]=="ExaminationFrontier" and j["read_only"] is True and j["writes_event_ledger"] is False and j["mutates_cluster"] is False
    forbidden="priority_rank selected_work probe_request queue_state scheduler_state recurrence_conclusion semantic_interpretation campaign_completion".split()
    assert not any(x in json.dumps(j) for x in forbidden)
    inv={e.name:e for e in DIAGNOSTIC_INVENTORY}["examination_frontier"]
    assert inv.cli_flags == ("--examination-frontier",) and inv.supports_json and inv.record_scope=="none" and not inv.writes_event_ledger and not inv.mutates_cluster
    rows={(r.diagnostic,r.field):r for r in build_diagnostic_shape_audit()}
    assert rows[("examination_frontier","supports_json")].status=="consistent"
    assert rows[("examination_frontier","mutates_cluster")].status=="consistent"

def test_mixed_corpus_demonstration_and_compatibility_boundaries():
    r1=WorkResultReference("lesson-struct","lesson",LESSON_HASH,"external-material structural projection","external_material_structure","external_material_structural_projection_v1","completed")
    r2=WorkResultReference("lesson-surface","lesson",LESSON_HASH,"external-material surface-feature projection","external_material_surface_features","external_material_surface_feature_projection_v1","completed")
    r3=WorkResultReference("agents-struct","agents","repohash","external-material structural projection","external_material_structure","external_material_structural_projection_v1","completed")
    r4=WorkResultReference("agents-surface","agents","repohash","external-material surface-feature projection","external_material_surface_features","external_material_surface_feature_projection_v1","completed")
    ms=(CorpusMember("web","website_target","Project Gutenberg website acquisition target"), CorpusMember("lesson","book","selected_lesson_006.txt",LESSON_HASH), CorpusMember("agents","repository","AGENTS.md","repohash"))
    ws=(work(candidate_work_id="web-acquire", corpus_member_id="web", work_kind="acquire bounded homepage material", capability_id="website_acquisition", blockers=("environment access failure before confirmed live Gutenberg bytes",)), work(candidate_work_id="lesson-struct", corpus_member_id="lesson", existing_results=(r1,)), work(candidate_work_id="lesson-surface", corpus_member_id="lesson", work_kind="external-material surface-feature projection", capability_id="external_material_surface_features", convention="external_material_surface_feature_projection_v1", existing_results=(r2,)), work(candidate_work_id="lesson-prose", corpus_member_id="lesson", work_kind="request attributed prose interpretation", compatibility_status="unknown", authorization_status="unknown", capability_id=""), work(candidate_work_id="agents-struct", corpus_member_id="agents", existing_results=(r3,)), work(candidate_work_id="agents-surface", corpus_member_id="agents", work_kind="external-material surface-feature projection", capability_id="external_material_surface_features", convention="external_material_surface_feature_projection_v1", existing_results=(r4,)), work(candidate_work_id="compare", corpus_member_id="lesson", work_kind="compare selected structural features", compatibility_status="unsupported", authorization_status="not_applicable", capability_id=""))
    f=project_examination_frontier(q(),"mixed","mixed corpus",ms,ws)
    by={i.candidate_work_id:i for i in f.work_items}
    assert {m.member_id for m in f.corpus_members}=={"web","lesson","agents"}
    assert by["web-acquire"].classification.blocked and "refusal" not in json.dumps(by["web-acquire"].to_json_dict()).lower()
    assert by["lesson-struct"].classification.examined and by["lesson-surface"].classification.examined
    assert by["lesson-prose"].classification.unknown and not by["lesson-prose"].classification.examined
    assert by["agents-struct"].classification.examined and by["agents-surface"].classification.examined
    assert by["agents-struct"].work_kind == "external-material structural projection"
    assert by["compare"].classification.unsupported
    assert all(i.classification.newly_eligible == "unresolved_no_previous_frontier_input" for i in f.work_items)
    # Existing compatibility boundaries remain import-compatible and unmodified by this test.
    import seed_runtime.bounded_constitutional_question, seed_runtime.external_site_rule_testimony, seed_runtime.external_material_testimony_binding, seed_runtime.external_material_structural_projection, seed_runtime.external_material_surface_feature_projection, seed_runtime.candidate_external_grammar, seed_runtime.execution, seed_runtime.pending_actions, seed_runtime.events, seed_runtime.capability_inventory
