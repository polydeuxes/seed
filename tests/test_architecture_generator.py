import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "docs" / "generated" / "architecture" / "architecture_graph.json"
MERMAID_PATH = ROOT / "docs" / "generated" / "architecture" / "runtime_ownership.mmd"
DOT_PATH = ROOT / "docs" / "generated" / "architecture" / "runtime_ownership.dot"


def test_architecture_generator_outputs_are_stable():
    before = {
        path: path.read_text()
        for path in (GRAPH_PATH, MERMAID_PATH, DOT_PATH)
    }

    subprocess.run(
        ["python", "scripts/generate_architecture.py"],
        cwd=ROOT,
        check=True,
    )

    after = {
        path: path.read_text()
        for path in (GRAPH_PATH, MERMAID_PATH, DOT_PATH)
    }
    assert after == before


def test_architecture_graph_records_runtime_owner_boundaries():
    graph = json.loads(GRAPH_PATH.read_text())
    assert graph["banner"] == "generated; do not edit"
    assert MERMAID_PATH.read_text().startswith("%% generated; do not edit")
    assert DOT_PATH.read_text().startswith("// generated; do not edit")

    node_ids = {node["id"] for node in graph["nodes"]}
    assert "RuntimeLoop" not in node_ids

    edges = graph["edges"]
    assert {
        "from": "Runtime",
        "to": "StateProjector",
        "label": "projects current state for deterministic callers",
    } in edges
    assert not any(
        edge["from"] == "Runtime"
        and edge["to"] == "ToolExecutor"
        and edge.get("path") == "request_tool"
        for edge in edges
    )
