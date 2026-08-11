import copy, hashlib, json, subprocess, sys
from pathlib import Path

import pytest

from seed_runtime.candidate_external_grammar import CandidateExternalGrammarInput
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.external_material_structural_projection import *
from seed_runtime.external_material_testimony_binding import ExternalMaterialManifest, ExternalMaterialSelectedArtifactRecord, ExternalMaterialSourceRecord


def digest(text, enc="utf-8"):
    return hashlib.sha256(text.encode(enc)).hexdigest()


def manifest(text="Alpha\nBeta", *, mid="m1", sid="s1", aid="a1", h=None, lines=None, chars=None):
    h = h or digest(text)
    return ExternalMaterialManifest(mid, (ExternalMaterialSourceRecord(sid),), (ExternalMaterialSelectedArtifactRecord(aid, sid, h, "fixture", len(text.splitlines(True)) if lines is None else lines, len(text) if chars is None else chars),))


def request(text="Alpha\nBeta", *, mid="m1", sid="s1", aid="a1", h=None, enc="utf-8"):
    return ExternalMaterialStructuralProjectionRequest(mid, sid, aid, h or digest(text), enc, text, ("u",))


def project(text="Alpha\nBeta", **kw):
    return project_external_material_structure(manifest(text, **{k:v for k,v in kw.items() if k in {"mid","sid","aid","h","lines","chars"}}), request(text, **{k:v for k,v in kw.items() if k in {"mid","sid","aid","h","enc"}}))


def fails(code, man, req):
    with pytest.raises(ExternalMaterialStructuralProjectionError) as e:
        project_external_material_structure(man, req)
    assert str(e.value) == code


def test_valid_exact_text_and_deterministic_failures():
    out = project("A\nB")
    assert len(out.lines) == 2 and out.read_only and not out.writes_event_ledger and not out.mutates_cluster
    fails("unknown_manifest", manifest("A"), request("A", mid="missing"))
    fails("unknown_source", manifest("A"), request("A", sid="missing"))
    fails("unknown_artifact", manifest("A"), request("A", aid="missing"))
    man = ExternalMaterialManifest("m1", (ExternalMaterialSourceRecord("s1"), ExternalMaterialSourceRecord("s2")), (ExternalMaterialSelectedArtifactRecord("a1", "s2", digest("A"), line_count=1, character_count=1),))
    fails("source_artifact_mismatch", man, request("A"))
    fails("artifact_hash_mismatch", manifest("A"), request("B", h=digest("A")))
    fails("unsupported_encoding", manifest("A"), request("A", enc="no-such-encoding"))
    fails("text_encode_failure", manifest("é", h=hashlib.sha256("é".encode("utf-8")).hexdigest()), request("é", h=hashlib.sha256("é".encode("utf-8")).hexdigest(), enc="ascii"))
    fails("line_count_mismatch", manifest("A\nB", lines=1), request("A\nB"))
    fails("character_count_mismatch", manifest("A\nB", chars=99), request("A\nB"))


def test_line_records_order_blank_terminator_empty_and_stable_ids():
    out = project("One\n\nTwo")
    assert [l.line_number for l in out.lines] == [1,2,3]
    assert [l.text for l in out.lines] == ["One\n", "\n", "Two"]
    assert out.lines[1].is_blank and out.lines[1].has_line_terminator
    assert not out.lines[2].has_line_terminator
    assert out.lines[0].line_id == project("One\n\nTwo").lines[0].line_id
    assert project("Solo").lines[0].line_number == 1
    empty_hash = hashlib.sha256(b"").hexdigest()
    empty = project_external_material_structure(manifest("", h=empty_hash, lines=0, chars=0), request("", h=empty_hash))
    assert empty.lines == () and empty.nonblank_regions == ()


def test_regions_split_only_on_blank_lines_and_ids_exact_membership():
    out = project("A\n\n\nB\nC\n")
    assert [(r.start_line, r.end_line, r.line_count) for r in out.nonblank_regions] == [(1,1,1),(4,5,2)]
    assert out.nonblank_regions[1].line_ids == (out.lines[3].line_id, out.lines[4].line_id)
    assert out.nonblank_regions[0].region_id == project("A\n\n\nB\nC\n").nonblank_regions[0].region_id
    assert project("A", aid="other").lines[0].line_id != project("A").lines[0].line_id
    assert project("A", h=digest("A")).lines[0].line_id != project("B", h=digest("B")).lines[0].line_id


def test_preserves_case_punctuation_whitespace_and_emits_no_semantic_labels():
    text = "Capitalized?!\n  Mixed  CASE.  \n"
    out = project(text)
    assert out.lines[0].text == "Capitalized?!\n" and out.lines[1].text == "  Mixed  CASE.  \n"
    payload = external_material_structural_projection_json(out)
    for line in payload["lines"]:
        assert not any(k in line for k in ["heading", "rule", "example", "exercise", "sentence", "code", "grammar_label"])


def test_human_json_cli_inventory_shape_and_no_mutation(tmp_path):
    text="A\nB"
    data={"manifest": manifest(text). __dict__ | {"sources":[s.to_json_dict() for s in manifest(text).sources], "selected_artifacts":[a.to_json_dict() for a in manifest(text).selected_artifacts], "annotations":[], "manifest_unknowns":[]}, "projection_request": request(text).__dict__}
    p=tmp_path/"in.json"; p.write_text(json.dumps(data))
    before_git=subprocess.run(["git","status","--short"], text=True, capture_output=True, check=True).stdout
    h=subprocess.run([sys.executable,"scripts/seed_local.py","--external-material-structure",str(p)], text=True, capture_output=True, check=True).stdout
    j=json.loads(subprocess.run([sys.executable,"scripts/seed_local.py","--external-material-structure",str(p),"--json"], text=True, capture_output=True, check=True).stdout)
    after_git=subprocess.run(["git","status","--short"], text=True, capture_output=True, check=True).stdout
    assert "Lines and regions are mechanical projections" in h and "A line boundary is not a semantic boundary" in h
    assert j["artifact_type"] == "ExternalMaterialStructuralProjection" and j["lines"][0]["line_number"] == 1
    assert before_git == after_git
    inv={e.name:e for e in DIAGNOSTIC_INVENTORY}["external_material_structure"]
    assert inv.cli_flags == ("--external-material-structure",) and inv.supports_json and not inv.writes_event_ledger and not inv.mutates_cluster
    rows={(r.diagnostic,r.field):r for r in build_diagnostic_shape_audit()}
    assert rows[("external_material_structure","supports_json")].status == "consistent"
    assert rows[("external_material_structure","mutates_cluster")].status == "consistent"


def test_real_lesson_campaign_and_schema_compatibility():
    import campaigns.graded_lessons_supervised_grammar_apprenticeship_campaign_001.campaign as c
    data=c.SELECTED_LESSON.read_bytes()
    assert hashlib.sha256(data).hexdigest()==c.EXPECTED_SHA256
    out=c.structural_projection()
    assert len(out.lines)==4 and len(out.nonblank_regions)==1 and (out.nonblank_regions[0].start_line, out.nonblank_regions[0].end_line)==(1,4)
    rec=c.campaign_record()
    assert "Seed projected lines" in rec["structural_projection_boundary"]
    supplied=CandidateExternalGrammarInput.from_json_dict({"representation_scope":"scope","candidates":[{"candidate_id":"c1","structural_claim":"claim","supporting_testimony":["source:gl001:selected_lesson_006:L1-L4"]}]})
    assert supplied.candidates[0].supporting_testimony == ("source:gl001:selected_lesson_006:L1-L4",)


def test_repository_artifact_same_projection_and_no_semantic_correspondence():
    path=Path("AGENTS.md"); text=path.read_text(); h=digest(text)
    man=ExternalMaterialManifest("repo_probe_manifest", (ExternalMaterialSourceRecord("repo_source"),), (ExternalMaterialSelectedArtifactRecord("repo_agents_md", "repo_source", h, str(path), len(text.splitlines(True)), len(text)),))
    out=project_external_material_structure(man, ExternalMaterialStructuralProjectionRequest("repo_probe_manifest", "repo_source", "repo_agents_md", h, "utf-8", text))
    assert len(out.lines) > 0 and len(out.nonblank_regions) > 0
    blob=json.dumps(out.to_json_dict())
    assert "equivalent" not in blob and "correspondence" not in blob and "semantic grammar" not in blob
