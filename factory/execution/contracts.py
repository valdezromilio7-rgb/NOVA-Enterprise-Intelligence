"""Canonical execution and audit contracts.

These contracts define what may be executed and what must be recorded. They
are intentionally provider-agnostic and do not execute arbitrary code.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping, Sequence

from factory.agents.registry import AgentRegistry, TaskAuthorization


class ExecutionStatus(str, Enum):
    AUTHORIZED = "authorized"
    REJECTED = "rejected"
    STARTED = "started"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class ExecutionContract:
    """Immutable declaration of one bounded agent execution."""

    execution_id: str
    agent_id: str
    agent_version: str
    task_type: str
    input_refs: Sequence[str] = field(default_factory=tuple)
    output_contract: str = ""
    required_tools: Sequence[str] = field(default_factory=tuple)
    required_data_access: Sequence[str] = field(default_factory=tuple)
    required_write_access: Sequence[str] = field(default_factory=tuple)
    budget_exposure: float = 0.0
    parent_execution_id: str | None = None
    policy_version: str = "execution-v0.1"
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("execution_id", "agent_id", "agent_version", "task_type", "output_contract", "policy_version"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.budget_exposure < 0:
            raise ValueError("budget_exposure must be non-negative")

    def to_task_authorization(self) -> TaskAuthorization:
        return TaskAuthorization(
            task_type=self.task_type,
            required_tools=self.required_tools,
            required_data_access=self.required_data_access,
            required_write_access=self.required_write_access,
            budget_exposure=self.budget_exposure,
        )


@dataclass(frozen=True)
class ExecutionAuthorization:
    execution_id: str
    authorized: bool
    reasons: tuple[str, ...]
    agent_id: str
    agent_version: str
    policy_version: str


@dataclass(frozen=True)
class AuditEvent:
    """Append-only event describing one execution lifecycle transition."""

    event_type: str
    execution_id: str
    agent_id: str
    agent_version: str
    status: ExecutionStatus
    timestamp: str
    input_refs: Sequence[str] = field(default_factory=tuple)
    output_refs: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    error_code: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)
    event_id: str = ""

    def __post_init__(self) -> None:
        if not self.event_type.strip():
            raise ValueError("event_type must be non-empty")
        if not self.execution_id.strip():
            raise ValueError("execution_id must be non-empty")
        if not self.agent_id.strip() or not self.agent_version.strip():
            raise ValueError("agent identity must be non-empty")
        if not self.timestamp.strip():
            raise ValueError("timestamp must be non-empty")
        if self.status == ExecutionStatus.FAILED and not self.error_code:
            raise ValueError("failed events require error_code")
        if not self.event_id:
            object.__setattr__(self, "event_id", self.deterministic_id())

    def deterministic_id(self) -> str:
        payload = {
            "event_type": self.event_type,
            "execution_id": self.execution_id,
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "input_refs": tuple(self.input_refs),
            "output_refs": tuple(self.output_refs),
            "evidence_refs": tuple(self.evidence_refs),
            "error_code": self.error_code,
            "metadata": dict(sorted(self.metadata.items())),
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return f"audit:{sha256(encoded).hexdigest()}"


def authorize_execution(
    contract: ExecutionContract,
    registry: AgentRegistry,
) -> ExecutionAuthorization:
    """Authorize a contract using the canonical Agent Registry only."""
    result = registry.authorize(contract.agent_id, contract.to_task_authorization())
    registered = registry.get(contract.agent_id)
    reasons = list(result.reasons)
    if registered.version != contract.agent_version:
        reasons.append("agent_version_mismatch")

    return ExecutionAuthorization(
        execution_id=contract.execution_id,
        authorized=not reasons,
        reasons=tuple(reasons),
        agent_id=contract.agent_id,
        agent_version=contract.agent_version,
        policy_version=contract.policy_version,
    )
