import pytest

from factory.account_intelligence.graph import GraphEdge, GraphNode, build_graph


def _nodes():
    return [
        GraphNode("account", "acct-001"),
        GraphNode("source", "src-001"),
        GraphNode("observation", "obs-001"),
        GraphNode("evidence", "ev-001"),
        GraphNode("signal", "sig-001"),
        GraphNode("context", "ctx-001"),
        GraphNode("why_now", "why-001"),
        GraphNode("business_problem", "bp-001"),
        GraphNode("opportunity", "opp-001"),
    ]


def _edges():
    return [
        GraphEdge("account", "acct-001", "source", "src-001", "uses", "fixture", "2026-09-10T00:00:00Z"),
        GraphEdge("source", "src-001", "observation", "obs-001", "produced", "fixture", "2026-09-10T00:00:00Z"),
        GraphEdge("observation", "obs-001", "evidence", "ev-001", "supports", "fixture", "2026-09-10T00:00:00Z"),
        GraphEdge("evidence", "ev-001", "signal", "sig-001", "supports", "fixture", "2026-09-10T00:00:00Z"),
        GraphEdge("signal", "sig-001", "context", "ctx-001", "has_context", "fixture", "2026-09-10T00:00:00Z"),
        GraphEdge("context", "ctx-001", "why_now", "why-001", "explains_timing", "fixture", "2026-09-10T00:00:00Z"),
        GraphEdge("why_now", "why-001", "business_problem", "bp-001", "frames", "fixture", "2026-09-10T00:00:00Z"),
        GraphEdge("business_problem", "bp-001", "opportunity", "opp-001", "creates", "fixture", "2026-09-10T00:00:00Z"),
    ]


def test_graph_serialization_is_deterministic():
    first = build_graph(_nodes(), _edges())
    second = build_graph(list(reversed(_nodes())), list(reversed(_edges())))
    assert first.serialize() == second.serialize()
    assert first.edges[0].id == second.edges[0].id


def test_graph_requires_provenance_on_edges():
    with pytest.raises(ValueError, match="edge provenance"):
        GraphEdge("account", "acct-001", "source", "src-001", "uses", " ")


def test_graph_rejects_invalid_edge_direction():
    with pytest.raises(ValueError, match="unsupported edge"):
        GraphEdge("opportunity", "opp-001", "account", "acct-001", "reverses", "fixture")


def test_graph_rejects_missing_endpoint_node():
    with pytest.raises(ValueError, match="target node is missing"):
        build_graph(
            [GraphNode("account", "acct-001"), GraphNode("source", "src-001")],
            [GraphEdge("account", "acct-001", "source", "src-missing", "uses", "fixture")],
        )


def test_graph_has_no_evaluation_truth_contract():
    graph = build_graph(_nodes(), _edges())
    serialized = graph.serialize()
    assert "ground_truth" not in serialized
    assert "EXPECTED_SIGNAL" not in serialized
