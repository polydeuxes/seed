import copy, hashlib, json, subprocess, sys
from pathlib import Path

import pytest

from seed_runtime.candidate_external_grammar import CandidateExternalGrammarInput
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.external_material_structural_projection import *
from seed_runtime.external_material_surface_feature_projection import *
from seed_runtime.external_material_testimony_binding import ExternalMaterialManifest, ExternalMaterialSelectedArtifactRecord, ExternalMaterialSourceRecord


def digest(text): return hashlib.sha256(text.encode("utf-8")).hexdigest()

def manifest(text, mid="m", sid="s", aid="a"):
    return ExternalMaterialManifest(mid, (ExternalMaterialSourceRecord(sid),), (ExternalMaterialSelectedArtifactRecord(aid, sid, digest(text), "fixture", len(text.splitlines(True)) if text else 0, len(text)),))

def structure(text, mid="m", sid="s", aid="a"):
    return project_external_material_structure(manifest(text, mid, sid, aid), ExternalMaterialStructuralProjectionRequest(mid, sid, aid, digest(text), "utf-8", text))

def features(text): return project_external_material_surface_features(structure(text))


def test_line_features_terminators_whitespace_blank_order_ids_and_empty():
    out = features("A\nBC\r\nfinal  \n\t \r")
    assert len(out.line_features) == 4
    assert [f.raw_character_count for f in out.line_features] == [2, 4, 8, 3]
    assert [f.content_character_count for f in out.line_features] == [1, 2, 7, 2]
    assert [f.line_terminator_character_count for f in out.line_features] == [1, 2, 1, 1]
    assert out.line_features[2].content_character_count == len("final  ")
    assert out.line_features[3].is_blank and out.line_features[3].content_character_count == len("\t ")
    no_term = features("last").line_features[0]
    assert no_term.raw_character_count == no_term.content_character_count == 4
    structural = structure("1\n2")
    projected = project_external_material_surface_features(structural)
    assert [f.line_id for f in projected.line_features] == [l.line_id for l in structural.lines]
    assert [f.line_number for f in projected.line_features] == [1, 2]
    empty_hash = hashlib.sha256(b"").hexdigest()
    empty_struct = project_external_material_structure(
        ExternalMaterialManifest("m", (ExternalMaterialSourceRecord("s"),), (ExternalMaterialSelectedArtifactRecord("a", "s", empty_hash, "fixture", 0, 0),)),
        ExternalMaterialStructuralProjectionRequest("m", "s", "a", empty_hash, "utf-8", ""),
    )
    empty = project_external_material_surface_features(empty_struct)
    assert empty.line_features == () and empty.region_features == ()


def test_region_features_are_composed_from_line_features_without_semantic_fields():
    structural = structure("HEAD\nbody text!\n\nrule? example exercise grammar\n")
    out = project_external_material_surface_features(structural)
    assert [r.region_id for r in out.region_features] == [r.region_id for r in structural.nonblank_regions]
    assert out.region_features[0].line_ids == (structural.lines[0].line_id, structural.lines[1].line_id)
    assert out.region_features[0].raw_line_character_count_sequence == tuple(f.raw_character_count for f in out.line_features[:2])
    assert out.region_features[0].content_character_count_sequence == tuple(f.content_character_count for f in out.line_features[:2])
    assert out.region_features[0].total_raw_character_count == sum(out.region_features[0].raw_line_character_count_sequence)
    assert out.region_features[0].total_content_character_count == sum(out.region_features[0].content_character_count_sequence)
    payload = out.to_json_dict()
    assert "text" not in payload["line_features"][0]
    feature_keys = set(payload["line_features"][0]) | set(payload["region_features"][0])
    for forbidden in ["uppercase", "punctuation", "token", "heading", "rule", "example", "exercise", "grammar"]:
        assert forbidden not in feature_keys


def test_validation_boundary_rejects_malformed_region_reference_and_order():
    structural = structure("A\nB\n")
    bad_ref = ExternalMaterialStructuralProjection(**{**structural.__dict__, "nonblank_regions": (ExternalMaterialProjectedNonblankRegion("r", 1, 1, ("missing",), 1),)})
    with pytest.raises(ExternalMaterialSurfaceFeatureProjectionError, match="unknown_region_line_id"):
        project_external_material_surface_features(bad_ref)
    bad_order = ExternalMaterialStructuralProjection(**{**structural.__dict__, "nonblank_regions": (ExternalMaterialProjectedNonblankRegion("r", 1, 2, (structural.lines[1].line_id, structural.lines[0].line_id), 2),)})
    with pytest.raises(ExternalMaterialSurfaceFeatureProjectionError, match="nondeterministic_region_line_order"):
        project_external_material_surface_features(bad_order)


def test_human_json_cli_inventory_shape_and_no_git_mutation(tmp_path):
    structural = structure("A\nB")
    p = tmp_path / "structural.json"
    p.write_text(json.dumps(structural.to_json_dict()))
    before = subprocess.run(["git", "status", "--short"], text=True, capture_output=True, check=True).stdout
    human = subprocess.run([sys.executable, "scripts/seed_local.py", "--external-material-surface-features", str(p)], text=True, capture_output=True, check=True).stdout
    payload = json.loads(subprocess.run([sys.executable, "scripts/seed_local.py", "--external-material-surface-features", str(p), "--json"], text=True, capture_output=True, check=True).stdout)
    after = subprocess.run(["git", "status", "--short"], text=True, capture_output=True, check=True).stdout
    for note in BOUNDARY_NOTES:
        assert note in human and note in payload["boundary_notes"]
    assert payload["artifact_type"] == "ExternalMaterialSurfaceFeatureProjection"
    assert payload["read_only"] and not payload["writes_event_ledger"] and not payload["mutates_cluster"]
    assert before == after
    inv = {e.name: e for e in DIAGNOSTIC_INVENTORY}["external_material_surface_features"]
    assert inv.cli_flags == ("--external-material-surface-features",) and inv.supports_json and not inv.writes_event_ledger and not inv.mutates_cluster
    rows = {(r.diagnostic, r.field): r for r in build_diagnostic_shape_audit()}
    assert rows[("external_material_surface_features", "supports_json")].status == "consistent"
    assert rows[("external_material_surface_features", "mutates_cluster")].status == "consistent"


def test_real_campaign_lesson_repository_probe_and_compatibility():
    import campaigns.graded_lessons_supervised_grammar_apprenticeship_campaign_001.campaign as c
    assert hashlib.sha256(c.SELECTED_LESSON.read_bytes()).hexdigest() == c.EXPECTED_SHA256
    sf = c.surface_feature_projection()
    assert len(sf.line_features) == 4
    assert len(sf.region_features) == 1 and sf.region_features[0].line_count == 4
    assert list(sf.region_features[0].content_character_count_sequence) == [248, 464, 433, 479]
    rec = c.campaign_record()
    assert "Seed projected length features" in rec["surface_feature_boundary"]
    assert "campaign author still interpreted" in rec["surface_feature_boundary"]

    agents = Path("AGENTS.md").read_text()
    assert digest(agents) == "60d0a3b1eb5692ef0acc49058b303eb3fcca77e271b827c5c7d03589abc3afed"
    repo_features = project_external_material_surface_features(project_external_material_structure(
        ExternalMaterialManifest("repo_probe_manifest", (ExternalMaterialSourceRecord("repo_source"),), (ExternalMaterialSelectedArtifactRecord("repo_agents_md", "repo_source", digest(agents), "AGENTS.md", len(agents.splitlines(True)), len(agents)),)),
        ExternalMaterialStructuralProjectionRequest("repo_probe_manifest", "repo_source", "repo_agents_md", digest(agents), "utf-8", agents),
    ))
    assert repo_features.to_json_dict()["artifact_type"] == "ExternalMaterialSurfaceFeatureProjection"
    assert any(r.line_count == 4 for r in repo_features.region_features) and sf.region_features[0].line_count == 4
    refusal = "regions have the same responsibility; lesson region corresponds; semantic similarity"
    assert all(term not in json.dumps(repo_features.to_json_dict()) for term in refusal.split("; "))

    supplied = CandidateExternalGrammarInput.from_json_dict({"representation_scope":"scope","candidates":[{"candidate_id":"c1","structural_claim":"claim","supporting_testimony":["source:gl001:selected_lesson_006:L1-L4"]}]})
    assert supplied.candidates[0].supporting_testimony == ("source:gl001:selected_lesson_006:L1-L4",)
    assert c.testimony_binding_set().to_json_dict()["artifact_type"] == "ExternalMaterialTestimonyBindingSet"
    assert c.structural_projection().to_json_dict()["artifact_type"] == "ExternalMaterialStructuralProjection"
