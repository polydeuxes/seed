import copy, hashlib, json, subprocess, sys
from pathlib import Path

import pytest

from seed_runtime.candidate_external_grammar import CandidateExternalGrammarInput, assemble_candidate_external_grammar_set
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.external_material_testimony_binding import *

HASH="h-artifact"; SOURCE_HASH="h-source"

def manifest():
    return ExternalMaterialManifest(
        "m1",
        (ExternalMaterialSourceRecord("s1","work:x","manual",SOURCE_HASH,"loc","Title","Creator","operator"), ExternalMaterialSourceRecord("s2", source_hash="other")),
        (ExternalMaterialSelectedArtifactRecord("a1","s1",HASH,"artifact-loc",4,100,"lines 1-4"), ExternalMaterialSelectedArtifactRecord("a2","s2","h2","other",2,20,"lines 1-2")),
        (ExternalMaterialAnnotationRecord("ann1","a1",1,2, supplied_by="human", annotation_kind="note"), ExternalMaterialAnnotationRecord("ann_chars","a1",2,2,3,8), ExternalMaterialAnnotationRecord("ann_other","a2",1,1)),
        ("unknown source authority",),
    )

def req(id="t1", **kw):
    d=dict(testimony_reference_id=id, manifest_id="m1", source_id="s1", artifact_id="a1", expected_artifact_hash=HASH, start_line=1, end_line=2, unknowns=("u",))
    d.update(kw); return ExternalMaterialTestimonyBindingRequest(**d)

def validate(*requests): return validate_external_material_testimony_bindings(manifest(), tuple(requests), ("set-u",))

def fails(code, *requests):
    with pytest.raises(ExternalMaterialTestimonyBindingValidationError) as e: validate(*requests)
    assert str(e.value)==code

def test_valid_one_and_identity_boundaries():
    out=validate(req(optional_annotation_id="ann1")); b=out.bindings[0]
    assert b.testimony_reference_id=="t1" and b.source_id=="s1" and b.artifact_id=="a1"
    assert b.artifact_hash==HASH and SOURCE_HASH != HASH and b.binding_status=="reference_validated"
    assert out.read_only and not out.writes_event_ledger and not out.mutates_cluster
    assert "material-reference integrity only" in " ".join(out.boundary_notes)

def test_multiple_valid_references_independent_and_unique():
    out=validate(req("t1"), req("t2", start_line=3, end_line=4))
    assert [b.testimony_reference_id for b in out.bindings]==["t1","t2"]
    fails("duplicate_testimony_reference_id", req("dup"), req("dup"))

def test_hash_and_missing_reference_failures():
    fails("unknown_manifest", req(manifest_id="missing")); fails("unknown_source", req(source_id="missing"))
    fails("unknown_artifact", req(artifact_id="missing")); fails("source_artifact_mismatch", req(source_id="s1", artifact_id="a2"))
    fails("artifact_hash_mismatch", req(expected_artifact_hash="bad"))

def test_line_and_character_bounds():
    assert validate(req(start_line=1,end_line=4)).bindings[0].start_line==1
    for s,e in [(0,1),(-1,1),(3,2)]: fails("invalid_line_bounds", req(start_line=s,end_line=e))
    fails("line_bounds_out_of_range", req(start_line=1,end_line=5))
    assert validate(req("chars", start_line=2,end_line=2, optional_start_character=3, optional_end_character=8, optional_annotation_id="ann_chars")).bindings[0].optional_start_character==3
    for s,e in [(0,2),(3,2),(101,102),(1,None)]: fails("invalid_character_bounds", req(optional_start_character=s, optional_end_character=e))

def test_annotation_identity_and_exact_span_rule():
    out=validate(req(optional_annotation_id="ann1")); assert out.bindings[0].optional_annotation_id=="ann1"
    fails("unknown_annotation", req(optional_annotation_id="missing"))
    fails("annotation_artifact_mismatch", req(optional_annotation_id="ann_other"))
    fails("annotation_span_mismatch", req(start_line=1,end_line=3,optional_annotation_id="ann1"))

def test_empty_rendering_and_no_semantic_words():
    out=validate_external_material_testimony_bindings(manifest(), (), ())
    human=format_external_material_testimony_binding(out); payload=json.dumps(external_material_testimony_binding_json(out), sort_keys=True)
    assert "zero-binding set" in human and '"bindings": []' in payload
    forbidden=["support_validated","claim_verified","grammar_verified","authoritative_source","annotation_correct","confidence","warrant"]
    combined=human+payload
    assert "reference_validated" not in combined
    for word in forbidden: assert word not in combined

def test_cli_json_and_human_outputs(tmp_path):
    data={"manifest": manifest().__dict__ | {"sources":[s.to_json_dict() for s in manifest().sources],"selected_artifacts":[a.to_json_dict() for a in manifest().selected_artifacts],"annotations":[a.to_json_dict() for a in manifest().annotations],"manifest_unknowns":[]}, "binding_requests":[req().__dict__], "set_unknowns":[]}
    p=tmp_path/"in.json"; p.write_text(json.dumps(data))
    h=subprocess.run([sys.executable,"scripts/seed_local.py","--external-material-testimony-bindings",str(p)], text=True, capture_output=True, check=True)
    j=subprocess.run([sys.executable,"scripts/seed_local.py","--external-material-testimony-bindings",str(p),"--json"], text=True, capture_output=True, check=True)
    assert "External Material Testimony Binding Set" in h.stdout
    assert json.loads(j.stdout)["artifact_type"]=="ExternalMaterialTestimonyBindingSet"

def test_inventory_and_shape_audit_registered():
    inv={e.name:e for e in DIAGNOSTIC_INVENTORY}["external_material_testimony_bindings"]
    assert inv.cli_flags == ("--external-material-testimony-bindings",) and inv.supports_json and not inv.writes_event_ledger and not inv.mutates_cluster
    rows={(r.diagnostic,r.field):r for r in build_diagnostic_shape_audit()}
    assert rows[("external_material_testimony_bindings","supports_json")].status=="consistent"
    assert rows[("external_material_testimony_bindings","writes_event_ledger")].status=="consistent"

def test_no_event_or_state_mutation_by_construction_and_rendering():
    before=list(Path('.').glob('.seed*'))
    out=validate(req()); format_external_material_testimony_binding(out); external_material_testimony_binding_json(out)
    assert list(Path('.').glob('.seed*'))==before

def test_candidate_grammar_schema_unchanged_and_ids_handoff():
    ids=["t1","t2"]
    supplied=CandidateExternalGrammarInput.from_json_dict({"representation_scope":"scope","candidates":[{"candidate_id":"c1","structural_claim":"claim","supporting_testimony":[ids[0]],"contradicting_testimony":[ids[1]]}]})
    art=assemble_candidate_external_grammar_set(supplied)
    assert art.candidates[0].supporting_testimony==(ids[0],) and art.candidates[0].contradicting_testimony==(ids[1],)

def test_campaign_real_lesson_integration_and_no_canonical_campaign_import():
    import campaigns.graded_lessons_supervised_grammar_apprenticeship_campaign_001.campaign as c
    data=c.SELECTED_LESSON.read_bytes()
    assert hashlib.sha256(data).hexdigest()=="01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963"
    assert len(data.decode('utf-8').splitlines())==4
    bs=c.testimony_binding_set(); full=[b for b in bs.bindings if b.testimony_reference_id=="source:gl001:selected_lesson_006:L1-L4"][0]
    assert (full.start_line, full.end_line)==(1,4)
    assert "campaigns" not in Path("seed_runtime/external_material_testimony_binding.py").read_text()
