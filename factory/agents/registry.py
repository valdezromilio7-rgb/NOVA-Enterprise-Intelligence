"""Canonical registry for bounded Product Factory agents.

The registry is an authorization boundary, not a prompt catalog. Agent
capabilities are explicit, least-privilege, and independently versioned.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class AgentStatus(str, Enum):
    DRAFT = "draft"
    EVALUATING = "evaluating"
    APPROVED = "approved"
    ACTIVE = "active"
    RESTRICTED = "restricted"
    RETIRED = "retired"


@dataclass(frozen=True)
class AgentDefinition:
    """Immutable declaration of an agent's authority and capabilities."""

    agent_id: str
    name: str
    version: str
    role: str
    description: str
    allowed_tasks: Sequence[str] = field(default_factory=tuple)
    forbidden_tasks: Sequence[str] = field(default_factory=tuple)
    input_contracts: Sequence[str] = field(default_factory=tuple)
    output_contracts: Sequence[str] = field(default_factory=tuple)
    tools: Sequence[str] = field(default_factory=tuple)
    data_access: Sequence[str] = field(default_factory=tuple)
    write_access: Sequence[str] = field(default_factory=tuple)
    financial_limit: float = 0.0
    execution_limit: int = 1
    escalation_rules: Sequence[str] = field(default_factory=tuple)
    evaluation_suite: Sequence[str] = field(default_factory=tuple)
    owner: str = "NOVA_CORP"
    status: AgentStatus = AgentStatus.DRAFT
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        required = {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "role": self.role,
            "description": self.description,
            "owner": self.owner,
        }
        for field_name, value in required.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.financial_limit < 0:
            raise ValueError("financial_limit must be non-negative")
        if self.execution_limit < 1:
            raise ValueError("execution_limit must be at least 1")
        if set(self.allowed_tasks) & set(self.forbidden_tasks):
            raise ValueError("a task cannot be both allowed and forbidden")
        if not self.evaluation_suite and self.status in {
            AgentStatus.APPROVED,
            AgentStatus.ACTIVE,
        }:
            raise ValueError("approved/active agents require an evaluation_suite")


@dataclass(frozen=True)
class TaskAuthorization:
    """Explicit task requirements presented to the registry for authorization."""

    task_type: str
    required_tools: Sequence[str] = field(default_factory=tuple)
    data_classification: str = "public"
    required_data_access: Sequence[str] = field(default_factory=tuple)
    required_write_access: Sequence[str] = field(default_factory=tuple)
    budget_exposure: float = 0.0

    def __post_init__(self) -> None:
        if not self.task_type.strip():
            raise ValueError("task_type must be non-empty")
        if self.budget_exposure < 0:
            raise ValueError("budget_exposure must be non-negative")


@dataclass(frozen=True)
class AuthorizationResult:
    authorized: bool
    reasons: tuple[str, ...]
    agent_id: str
    agent_version: str


class AgentRegistry:
    """In-memory canonical registry suitable for deterministic v0.1 workflows."""

    def __init__(self, agents: Sequence[AgentDefinition] = ()) -> None:
        self._agents: dict[str, AgentDefinition] = {}
        for agent in agents:
            self.register(agent)

    def register(self, agent: AgentDefinition) -> None:
        if agent.agent_id in self._agents:
            raise ValueError(f"agent already registered: {agent.agent_id}")
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> AgentDefinition:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise KeyError(f"unknown agent: {agent_id}") from exc

    def list(self, *, status: AgentStatus | None = None) -> tuple[AgentDefinition, ...]:
        agents = tuple(self._agents.values())
        if status is not None:
            agents = tuple(agent for agent in agents if agent.status == status)
        return tuple(sorted(agents, key=lambda agent: (agent.agent_id, agent.version)))

    def authorize(self, agent_id: str, task: TaskAuthorization) -> AuthorizationResult:
        """Check least-privilege constraints without executing the task."""
        agent = self.get(agent_id)
        reasons: list[str] = []

        if agent.status != AgentStatus.ACTIVE:
            reasons.append(f"agent_status_{agent.status.value}")
        if task.task_type in agent.forbidden_tasks:
            reasons.append("task_forbidden")
        if agent.allowed_tasks and task.task_type not in agent.allowed_tasks:
            reasons.append("task_not_allowed")
        if not set(task.required_tools).issubset(agent.tools):
            reasons.append("required_tool_not_granted")
        if not set(task.required_data_access).issubset(agent.data_access):
            reasons.append("required_data_access_not_granted")
        if not set(task.required_write_access).issubset(agent.write_access):
            reasons.append("required_write_access_not_granted")
        if task.budget_exposure > agent.financial_limit:
            reasons.append("financial_limit_exceeded")

        return AuthorizationResult(
            authorized=not reasons,
            reasons=tuple(reasons),
            agent_id=agent.agent_id,
            agent_version=agent.version,
        )
