import json

from scripts import seed_local
from seed_runtime.events import EventLedger
from seed_runtime.operational_graph import (
    OperationalGraphEdge,
    OperationalGraphEvidence,
    OperationalGraphNode,
    _add_operational_graph_edge,
    _filter_aggregate_operational_graph_edges,
    _important_low_confidence_edge_examples,
    _operational_graph_node_id,
    build_operational_graph,
    build_operational_graph_confidence,
    build_operational_graph_taxonomy,
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


def test_operational_graph_classifies_aggregate_and_concrete_nodes():
    graph = build_operational_graph()
    nodes = {node.id: node for node in graph.nodes}
    assert nodes["surface:views"].classification == "aggregate_surface"
    assert nodes["surface:diagnostics"].classification == "aggregate_surface"
    assert nodes["diagnostic:capability_needs"].classification == "concrete_diagnostic"
    assert nodes["emitter:action_plan"].classification == "concrete_emitter"
    assert nodes["surface:views"].aggregate is True
    assert nodes["diagnostic:capability_needs"].aggregate is False
    node_json = nodes["surface:views"].to_json_dict()
    assert node_json["taxonomy"] == "aggregate"
    assert nodes["diagnostic:capability_needs"].to_json_dict()["taxonomy"] == "concrete"


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


def test_operational_graph_preserves_emitter_consumer_audit_composition_boundary():
    ledger = EventLedger()
    before = ledger.list_events()
    graph = build_operational_graph()
    after = ledger.list_events()
    data = graph.to_json_dict()
    edges = {(edge.source, edge.target, edge.type): edge for edge in graph.edges}

    assert before == after == []
    assert graph.metadata["read_only"] is True
    assert graph.metadata["writes_event_ledger"] is False
    assert graph.metadata["mutates_cluster"] is False
    assert {"summary", "nodes", "edges", "metadata"} <= data.keys()
    assert graph.nodes == tuple(sorted(graph.nodes, key=lambda item: item.id))
    assert graph.edges == tuple(
        sorted(graph.edges, key=lambda item: (item.source, item.type, item.target))
    )

    emits_edge = edges[("emitter:action_plan", "event:action_plan.created", "emits")]
    assert emits_edge.confidence == "high"
    assert any(item.kind == "direct" for item in emits_edge.evidence)
    assert any(item.detail == "event emission literal" for item in emits_edge.evidence)
    assert "emitter:action_plan" in {node.id for node in graph.nodes}
    assert "event:action_plan.created" in {node.id for node in graph.nodes}

    consumes_edges = [
        edge
        for edge in graph.edges
        if edge.source == "event:action_plan.created"
        and edge.type == "consumes"
        and edge.confidence == "medium"
    ]
    assert consumes_edges
    assert all(any(item.kind == "indirect" for item in edge.evidence) for edge in consumes_edges)
    assert all(
        any(item.source == "emitter_consumer_audit" for item in edge.evidence)
        for edge in consumes_edges
    )
    assert len(edges) == len(graph.edges)
    assert graph.summary["relationship_types"]["emits"] > 0
    assert graph.summary["relationship_types"]["consumes"] > 0
    assert graph.summary["confidence_counts"]["high"] > 0
    assert graph.summary["confidence_counts"]["medium"] > 0


def test_operational_graph_preserves_consumer_dependency_audit_composition_boundary():
    ledger = EventLedger()
    before = ledger.list_events()
    graph = build_operational_graph()
    after = ledger.list_events()
    data = graph.to_json_dict()
    edges = {(edge.source, edge.target, edge.type): edge for edge in graph.edges}

    assert before == after == []
    assert graph.metadata["read_only"] is True
    assert graph.metadata["writes_event_ledger"] is False
    assert graph.metadata["mutates_cluster"] is False
    assert {"summary", "nodes", "edges", "metadata"} <= data.keys()
    assert graph.nodes == tuple(sorted(graph.nodes, key=lambda item: item.id))
    assert graph.edges == tuple(
        sorted(graph.edges, key=lambda item: (item.source, item.type, item.target))
    )

    node_ids = {node.id for node in graph.nodes}
    assert "diagnostic:operational_graph" in node_ids
    assert "surface:state_build" in node_ids
    edge = edges[("diagnostic:operational_graph", "surface:state_build", "consumes")]
    assert edge.confidence == "low"
    assert any(item.kind == "reference" for item in edge.evidence)
    assert any(
        item.detail == "state_build source group references operational_graph"
        for item in edge.evidence
    )
    assert any(item.source.startswith("seed_runtime/") for item in edge.evidence)
    assert len(edges) == len(graph.edges)
    assert graph.summary["relationship_types"]["consumes"] > 0
    assert graph.summary["confidence_counts"]["low"] > 0


def test_operational_graph_node_registry_preserves_node_creation_boundary():
    ledger = EventLedger()
    before = ledger.list_events()
    nodes = {}

    first = _operational_graph_node_id(nodes, "surface", "views")
    second = _operational_graph_node_id(nodes, "surface", "views")
    diagnostic = _operational_graph_node_id(nodes, "diagnostic", "capability_needs")
    graph = build_operational_graph()
    after = ledger.list_events()
    data = graph.to_json_dict()

    assert first == second == "surface:views"
    assert diagnostic == "diagnostic:capability_needs"
    assert len(nodes) == 2
    assert nodes[first] == OperationalGraphNode(
        "surface:views", "surface", "views", "aggregate_surface"
    )
    assert nodes[diagnostic].classification == "concrete_diagnostic"
    assert nodes[first].aggregate is True
    assert before == after == []
    assert {"summary", "nodes", "edges", "metadata"} <= data.keys()
    assert graph.summary["nodes"] == len(graph.nodes)
    assert graph.nodes == tuple(sorted(graph.nodes, key=lambda item: item.id))
    assert graph.metadata["read_only"] is True
    assert graph.metadata["writes_event_ledger"] is False
    assert graph.metadata["mutates_cluster"] is False


def test_operational_graph_edge_registry_preserves_duplicate_merge_boundary():
    ledger = EventLedger()
    before = ledger.list_events()
    edges = {}
    direct = OperationalGraphEvidence("direct", "a.py", "event emission literal")
    reference = OperationalGraphEvidence("reference", "b.py", "source reference")

    _add_operational_graph_edge(edges, "source", "target", "uses", (), "high")
    assert edges == {}

    _add_operational_graph_edge(edges, "source", "target", "uses", (direct,), "low")
    _add_operational_graph_edge(
        edges, "source", "target", "uses", (direct, reference), "high"
    )
    graph = build_operational_graph()
    after = ledger.list_events()
    data = graph.to_json_dict()

    assert list(edges) == [("source", "target", "uses")]
    assert edges[("source", "target", "uses")] == OperationalGraphEdge(
        "source", "target", "uses", (direct, reference), "high"
    )
    assert before == after == []
    assert {"summary", "nodes", "edges", "metadata"} <= data.keys()
    assert graph.summary["edges"] == len(graph.edges)
    assert graph.summary["relationship_types"] == {
        key: graph.summary["relationship_types"][key]
        for key in graph.summary["relationship_types"]
    }
    assert graph.summary["confidence_counts"]
    assert graph.edges == tuple(
        sorted(graph.edges, key=lambda item: (item.source, item.type, item.target))
    )
    assert graph.metadata["read_only"] is True
    assert graph.metadata["writes_event_ledger"] is False
    assert graph.metadata["mutates_cluster"] is False


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
    assert "Uncertainty causes:" in out
    assert "Caused primarily by:" in out
    assert "Operational relationship uncertainty:" in out
    assert "Uncertainty categories:" in out
    assert "Representative examples:" in out


def test_operational_graph_confidence_json_valid(capsys):
    assert seed_local.main(["--operational-graph-confidence", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "summary" in data
    assert "tiers" in data
    assert "important_low_confidence_edges" in data
    assert "taxonomy" in data


def test_operational_graph_confidence_reports_all_tiers_and_reasoning():
    analysis = build_operational_graph_confidence()
    assert analysis["tiers"]["high"]["edge_count"] > 0
    assert analysis["tiers"]["medium"]["edge_count"] > 0
    assert analysis["tiers"]["low"]["edge_count"] > 0
    assert "direct emitter evidence" in analysis["tiers"]["high"]["reason"]
    assert "indirect helper evidence" in analysis["tiers"]["medium"]["reason"]
    assert "reference-only" in analysis["tiers"]["low"]["reason"]
    assert analysis["tiers"]["low"]["representative_examples"]
    low = analysis["tiers"]["low"]
    assert low["uncertainty_causes"]["aggregate_target"] > 0
    assert low["uncertainty_causes"]["reference_only_evidence"] > 0
    assert (
        low["uncertainty_categories"]["taxonomy_uncertainty"]
        == low["uncertainty_causes"]["aggregate_target"]
    )
    assert low["uncertainty_categories"]["reference_only_uncertainty"] > 0
    assert (
        low["confidence_interpretation"]["aggregate_target_edges"]
        == low["uncertainty_causes"]["aggregate_target"]
    )
    assert low["confidence_interpretation"]["operational_relationship_uncertainty_edges"] == 0


def test_operational_graph_confidence_preserves_tier_assembly_boundary():
    ledger = EventLedger()
    before = ledger.list_events()
    analysis = build_operational_graph_confidence()
    after = ledger.list_events()
    data = json.loads(json.dumps(analysis))

    assert before == after == []
    assert analysis["summary"]["read_only"] is True
    assert analysis["summary"]["writes_event_ledger"] is False
    assert analysis["summary"]["mutates_cluster"] is False
    assert {"summary", "tiers", "taxonomy", "important_low_confidence_edges", "metadata"} <= data.keys()

    tiers = analysis["tiers"]
    assert set(tiers) == {"high", "medium", "low"}
    assert tiers["high"]["edge_count"] == analysis["summary"]["confidence_counts"]["high"]
    assert tiers["medium"]["edge_count"] == analysis["summary"]["confidence_counts"]["medium"]
    assert tiers["low"]["edge_count"] == analysis["summary"]["confidence_counts"]["low"]
    assert tiers["high"]["relationship_types"]["emits"] > 0
    assert tiers["medium"]["relationship_types"]["consumes"] > 0
    assert tiers["low"]["relationship_types"]["consumes"] > 0
    assert tiers["high"]["evidence_categories"]["direct"] > 0
    assert tiers["medium"]["evidence_categories"]["indirect"] > 0
    assert tiers["low"]["evidence_categories"]["reference"] > 0
    assert tiers["low"]["uncertainty_causes"]["reference_only_evidence"] > 0
    assert tiers["low"]["uncertainty_categories"]["reference_only_uncertainty"] > 0
    assert "direct emitter evidence" in tiers["high"]["reason"]
    assert "indirect helper evidence" in tiers["medium"]["reason"]
    assert "reference-only" in tiers["low"]["reason"]
    assert "already directly supported" in tiers["high"]["potential_confidence_improvement"]
    assert tiers["high"]["representative_examples"]
    assert tiers["medium"]["representative_examples"]
    assert tiers["low"]["representative_examples"]
    assert analysis["important_low_confidence_edges"]


def test_operational_graph_confidence_exclude_aggregate_filters_taxonomy_noise(capsys):
    analysis = build_operational_graph_confidence(exclude_aggregate=True)
    full = build_operational_graph_confidence()
    assert analysis["summary"]["exclude_aggregate"] is True
    assert analysis["summary"]["excluded_aggregate_edges"] > 0
    assert analysis["summary"]["edges"] < full["summary"]["edges"]
    assert (
        analysis["tiers"]["low"]["uncertainty_causes"].get("aggregate_target", 0)
        == 0
    )

    assert (
        seed_local.main(
            ["--operational-graph-confidence", "--exclude-aggregate", "--json"]
        )
        == 0
    )
    data = json.loads(capsys.readouterr().out)
    assert data["summary"]["exclude_aggregate"] is True
    assert data["summary"]["excluded_aggregate_edges"] > 0


def test_operational_graph_confidence_aggregate_edge_filter_preserves_boundary():
    aggregate = OperationalGraphNode(
        "surface:views", "surface", "views", "aggregate_surface"
    )
    concrete = OperationalGraphNode(
        "diagnostic:capability_needs",
        "diagnostic",
        "capability_needs",
        "concrete_diagnostic",
    )
    aggregate_edge = OperationalGraphEdge(
        aggregate.id,
        concrete.id,
        "consumes",
        (OperationalGraphEvidence("reference", "seed_runtime/state.py", "reference"),),
        "low",
    )
    concrete_edge = OperationalGraphEdge(
        concrete.id,
        "event:action_plan.created",
        "emits",
        (OperationalGraphEvidence("direct", "seed_runtime/action_plans.py", "literal"),),
        "high",
    )
    nodes = {aggregate.id: aggregate, concrete.id: concrete}
    edges = (aggregate_edge, concrete_edge)

    assert (
        _filter_aggregate_operational_graph_edges(
            edges, nodes, exclude_aggregate=False
        )
        is edges
    )
    assert _filter_aggregate_operational_graph_edges(
        edges, nodes, exclude_aggregate=True
    ) == (concrete_edge,)

    ledger = EventLedger()
    before = ledger.list_events()
    filtered = build_operational_graph_confidence(exclude_aggregate=True)
    full = build_operational_graph_confidence(exclude_aggregate=False)
    after = ledger.list_events()
    data = json.loads(json.dumps(filtered))

    assert before == after == []
    assert filtered["summary"]["exclude_aggregate"] is True
    assert full["summary"]["exclude_aggregate"] is False
    assert filtered["summary"]["edges"] < full["summary"]["edges"]
    assert filtered["summary"]["excluded_aggregate_edges"] > 0
    assert filtered["summary"]["edges"] == sum(
        tier["edge_count"] for tier in filtered["tiers"].values()
    )
    assert filtered["tiers"]["low"]["edge_count"] == filtered["summary"][
        "confidence_counts"
    ].get("low", 0)
    assert filtered["important_low_confidence_edges"] == [
        edge
        for edge in full["important_low_confidence_edges"]
        if edge in filtered["important_low_confidence_edges"]
    ]
    assert filtered["taxonomy"] == full["taxonomy"]
    assert {"summary", "tiers", "taxonomy", "important_low_confidence_edges", "metadata"} <= data.keys()
    assert filtered["summary"]["read_only"] is True
    assert filtered["summary"]["writes_event_ledger"] is False
    assert filtered["summary"]["mutates_cluster"] is False


def test_operational_graph_confidence_important_low_selection_preserves_boundary(capsys):
    def edge(source, target, confidence="low"):
        return OperationalGraphEdge(
            source,
            target,
            "consumes",
            (
                OperationalGraphEvidence(
                    "reference", "seed_runtime/example.py:1", "reference"
                ),
            ),
            confidence,
        )

    already_filtered_edges = (
        edge("diagnostic:zeta", "surface:diagnostics"),
        edge("diagnostic:not_important", "surface:ordinary"),
        edge("diagnostic:alpha", "surface:diagnostics"),
        edge("diagnostic:medium", "surface:diagnostics", "medium"),
        *(
            edge(f"diagnostic:item_{index:02d}", "surface:pressure_audit")
            for index in range(12)
        ),
    )

    selected = _important_low_confidence_edge_examples(already_filtered_edges)

    assert len(selected) == 10
    assert [item["source"] for item in selected] == [
        "diagnostic:alpha",
        "diagnostic:item_00",
        "diagnostic:item_01",
        "diagnostic:item_02",
        "diagnostic:item_03",
        "diagnostic:item_04",
        "diagnostic:item_05",
        "diagnostic:item_06",
        "diagnostic:item_07",
        "diagnostic:item_08",
    ]
    assert all(item["confidence"] == "low" for item in selected)
    assert all(item["importance"] for item in selected)
    assert all("evidence" in item for item in selected)
    assert "diagnostic:not_important" not in {item["source"] for item in selected}
    assert "diagnostic:medium" not in {item["source"] for item in selected}

    ledger = EventLedger()
    before = ledger.list_events()
    analysis = build_operational_graph_confidence(exclude_aggregate=True)
    after = ledger.list_events()
    data = json.loads(json.dumps(analysis))

    assert before == after == []
    assert "important_low_confidence_edges" in data
    assert len(analysis["important_low_confidence_edges"]) <= 10
    assert analysis["summary"]["read_only"] is True
    assert analysis["summary"]["writes_event_ledger"] is False
    assert analysis["summary"]["mutates_cluster"] is False
    assert analysis["summary"]["edges"] == sum(
        tier["edge_count"] for tier in analysis["tiers"].values()
    )
    assert analysis["summary"]["excluded_aggregate_edges"] > 0
    assert analysis["taxonomy"]["summary"]["nodes"] > 0
    assert analysis["tiers"]["low"]["reason"]

    assert seed_local.main(["--operational-graph-confidence"]) == 0
    out = capsys.readouterr().out
    assert "Operationally relevant low-confidence edges:" in out
    assert "Low Confidence" in out

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


def test_operational_graph_taxonomy_renders_and_json_is_valid(capsys):
    assert seed_local.main(["--operational-graph-taxonomy"]) == 0
    out = capsys.readouterr().out
    assert "Operational Graph Taxonomy" in out
    assert "Aggregate nodes:" in out
    assert "aggregate_surface" in out

    assert seed_local.main(["--operational-graph-taxonomy", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["summary"]["aggregate_nodes"] > 0
    assert data["summary"]["concrete_nodes"] > 0
    assert data["classifications"]["aggregate_surface"] > 0
    assert data["aggregate_connectivity"]


def test_operational_graph_taxonomy_does_not_write_event_ledger_or_mutate_cluster():
    ledger = EventLedger()
    before = ledger.list_events()
    analysis = build_operational_graph_taxonomy()
    after = ledger.list_events()
    assert before == after == []
    assert analysis["summary"]["writes_event_ledger"] is False
    assert analysis["summary"]["mutates_cluster"] is False
