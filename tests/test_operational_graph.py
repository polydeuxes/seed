import json

from scripts import seed_local
from seed_runtime.events import EventLedger
from seed_runtime.operational_graph import (
    build_operational_graph,
    build_operational_graph_confidence,
    format_operational_graph_confidence,
)


def test_operational_graph_renders(capsys):
    assert seed_local.main(["--operational-graph"]) == 0
    out = capsys.readouterr().out
    assert "Operational Graph" in out
    assert "Nodes:" in out
    assert "Edges:" in out
    assert "Relationship types:" in out
    assert "Confidence counts:" in out


def test_operational_graph_json_valid(capsys):
    assert seed_local.main(["--operational-graph", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "nodes" in data
    assert "edges" in data
    assert "summary" in data


def test_operational_graph_discovers_nodes_edges_evidence_and_confidence():
    graph = build_operational_graph()
    assert graph.nodes
    assert graph.edges
    assert all(edge.evidence for edge in graph.edges)
    assert {edge.confidence for edge in graph.edges}


def test_operational_graph_includes_emitter_to_event_relationships():
    graph = build_operational_graph()
    assert any(
        edge.source == "emitter:action_plan"
        and edge.target == "event:action_plan.created"
        and edge.type == "emits"
        and edge.confidence == "high"
        and any(item.kind == "direct" for item in edge.evidence)
        for edge in graph.edges
    )


def test_operational_graph_includes_consumer_relationships():
    graph = build_operational_graph()
    assert any(edge.type == "consumes" for edge in graph.edges)
    assert any(edge.target.startswith("surface:") for edge in graph.edges)


def test_operational_graph_empty_state_is_sane(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    graph = build_operational_graph(tmp_path)
    assert graph.nodes == ()
    assert graph.edges == ()
    assert graph.summary["nodes"] == 0
    assert graph.summary["edges"] == 0


def test_operational_graph_does_not_write_event_ledger_or_mutate_cluster():
    ledger = EventLedger()
    before = ledger.list_events()
    graph = build_operational_graph()
    after = ledger.list_events()
    assert before == after == []
    assert graph.metadata["writes_event_ledger"] is False
    assert graph.metadata["mutates_cluster"] is False


def test_operational_graph_confidence_renders(capsys):
    assert seed_local.main(["--operational-graph-confidence"]) == 0
    out = capsys.readouterr().out
    assert "Operational Graph Confidence" in out
    assert "High Confidence" in out
    assert "Medium Confidence" in out
    assert "Low Confidence" in out
    assert "Reason:" in out
    assert "Representative examples:" in out


def test_operational_graph_confidence_json_valid(capsys):
    assert seed_local.main(["--operational-graph-confidence", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "summary" in data
    assert "tiers" in data
    assert "important_low_confidence_edges" in data


def test_operational_graph_confidence_reports_all_tiers_and_reasoning():
    analysis = build_operational_graph_confidence()
    assert analysis["tiers"]["high"]["edge_count"] > 0
    assert analysis["tiers"]["medium"]["edge_count"] > 0
    assert analysis["tiers"]["low"]["edge_count"] > 0
    assert "direct emitter evidence" in analysis["tiers"]["high"]["reason"]
    assert "indirect helper evidence" in analysis["tiers"]["medium"]["reason"]
    assert "reference-only" in analysis["tiers"]["low"]["reason"]
    assert analysis["tiers"]["low"]["representative_examples"]


def test_operational_graph_confidence_filter_reports_selected_tier(capsys):
    assert seed_local.main(["--operational-graph-confidence", "low"]) == 0
    out = capsys.readouterr().out
    assert "Low Confidence" in out
    assert "High Confidence" not in out


def test_operational_graph_confidence_highlights_important_low_confidence_edges():
    analysis = build_operational_graph_confidence()
    important = analysis["important_low_confidence_edges"]
    assert important
    assert any(item["importance"] for item in important)


def test_operational_graph_confidence_empty_state_is_sane(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    analysis = build_operational_graph_confidence(tmp_path)
    assert analysis["summary"]["edges"] == 0
    assert analysis["tiers"]["high"]["edge_count"] == 0
    assert analysis["important_low_confidence_edges"] == []
    assert "No implementation-backed" in format_operational_graph_confidence(analysis)


def test_operational_graph_confidence_does_not_write_event_ledger_or_mutate_cluster():
    ledger = EventLedger()
    before = ledger.list_events()
    analysis = build_operational_graph_confidence()
    after = ledger.list_events()
    assert before == after == []
    assert analysis["summary"]["writes_event_ledger"] is False
    assert analysis["summary"]["mutates_cluster"] is False
