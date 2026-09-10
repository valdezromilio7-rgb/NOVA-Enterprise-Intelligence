"""Provider-agnostic, deterministic graph primitives for Account Intelligence."""

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Mapping, Sequence


_ALLOWED_NODE_TYPES = frozenset(
    {
        "account",
        "source",
        "observation",
        "evidence",
        "signal",
        "context",
        "why_now",
        "business_problem",
        "opportunity",
    }
)

_ALLOWED_EDGES = frozenset(
    {
        ("account", "source"),
        ("source", "observation"),
        ("account", "observation"),
        ("observation", "evidence"),
        ("evidence", "signal"),
        ("observation", "signal"),
        ("signal", "context"),
        ("context", "why_now"),
        ("why_now", "business_problem"),
        ("business_problem", "opportunity"),
        ("evidence", "context"),
        ("evidence", "why_now"),
        ("evidence", "business_problem"),
        ("evidence", "opportunity"),
    }
)


def _stable_id(prefix: str, parts: Sequence[str]) -> str:
    payload = "|".join(part.strip() for part in parts)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}-{digest}"


@dataclass(frozen=True)
class GraphNode:
    """A canonical domain reference; payload is metadata, never hidden truth."""

    node_type: str
    node_id: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.node_type not in _ALLOWED_NODE_TYPES:
            raise ValueError(f"unsupported node_type: {self.node_type}")
        if not self.node_id.strip():
            raise ValueError("node_id must not be empty")


@dataclass(frozen=True)
class GraphEdge:
    """Typed directed relationship with explicit provenance."""

    source_type: str
    source_id: str
    target_type: str
    target_id: str
    relation: str
    provenance: str
    observed_at: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return _stable_id(
            "edge",
            (
                self.source_type,
                self.source_id,
                self.target_type,
                self.target_id,
                self.relation,
                self.observed_at,
                self.provenance,
            ),
        )

    def __post_init__(self) -> None:
        if (self.source_type, self.target_type) not in _ALLOWED_EDGES:
            raise ValueError(
                f"unsupported edge: {self.source_type} -> {self.target_type}"
            )
        if not self.source_id.strip() or not self.target_id.strip():
            raise ValueError("edge endpoints must not be empty")
        if not self.relation.strip():
            raise ValueError("relation must not be empty")
        if not self.provenance.strip():
            raise ValueError("edge provenance must not be empty")


@dataclass(frozen=True)
class SignalGraph:
    """Immutable graph snapshot with deterministic canonical serialization."""

    nodes: Sequence[GraphNode] = field(default_factory=tuple)
    edges: Sequence[GraphEdge] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        node_keys = [(node.node_type, node.node_id) for node in self.nodes]
        if len(node_keys) != len(set(node_keys)):
            raise ValueError("duplicate graph node")
        node_set = set(node_keys)
        for edge in self.edges:
            if (edge.source_type, edge.source_id) not in node_set:
                raise ValueError("edge source node is missing")
            if (edge.target_type, edge.target_id) not in node_set:
                raise ValueError("edge target node is missing")
        edge_ids = [edge.id for edge in self.edges]
        if len(edge_ids) != len(set(edge_ids)):
            raise ValueError("duplicate graph edge")

    def canonical_dict(self) -> dict[str, Any]:
        nodes = sorted(
            (
                {
                    "node_type": node.node_type,
                    "node_id": node.node_id,
                    "metadata": dict(sorted(node.metadata.items())),
                }
                for node in self.nodes
            ),
            key=lambda item: (item["node_type"], item["node_id"]),
        )
        edges = sorted(
            (
                {
                    "id": edge.id,
                    "source_type": edge.source_type,
                    "source_id": edge.source_id,
                    "target_type": edge.target_type,
                    "target_id": edge.target_id,
                    "relation": edge.relation,
                    "provenance": edge.provenance,
                    "observed_at": edge.observed_at,
                    "metadata": dict(sorted(edge.metadata.items())),
                }
                for edge in self.edges
            ),
            key=lambda item: item["id"],
        )
        return {"nodes": nodes, "edges": edges}

    def serialize(self) -> str:
        return json.dumps(self.canonical_dict(), sort_keys=True, separators=(",", ":"))


def build_graph(nodes: Sequence[GraphNode], edges: Sequence[GraphEdge]) -> SignalGraph:
    """Construct a validated graph and canonicalize collection ordering."""

    return SignalGraph(
        nodes=tuple(sorted(nodes, key=lambda n: (n.node_type, n.node_id))),
        edges=tuple(sorted(edges, key=lambda e: e.id)),
    )
