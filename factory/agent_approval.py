"""Auditable approval records for sensitive NOVA agent capabilities."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from factory.agent_permissions import Capability, AgentPolicy


@dataclass(frozen=True)
class CapabilityApproval:
    agent_id: str
    capability: Capability
    approver: str
    reason: str
    approved_at: str
    task_id: str | None = None


def create_capability_approval(*, policy: AgentPolicy, capability: Capability, approver: str, reason: str, task_id: str | None = None) -> CapabilityApproval:
    if capability not in policy.allowed:
        raise PermissionError(f"capability not allowed: {capability.value}")
    if not approver.strip():
        raise ValueError("approver must be non-empty")
    if not reason.strip():
        raise ValueError("reason must be non-empty")
    if task_id is not None and not task_id.strip():
        raise ValueError("task_id must be non-empty when provided")
    return CapabilityApproval(policy.agent_id, capability, approver, reason, datetime.now(timezone.utc).isoformat(), task_id)


def validate_capability_approval(approval: CapabilityApproval, *, policy: AgentPolicy, capability: Capability, task_id: str | None = None) -> None:
    if approval.agent_id != policy.agent_id:
        raise PermissionError("approval agent does not match policy")
    if approval.capability is not capability:
        raise PermissionError("approval capability does not match requested capability")
    if capability not in policy.allowed:
        raise PermissionError(f"capability not allowed: {capability.value}")
    if not approval.approver.strip() or not approval.reason.strip():
        raise ValueError("approval requires approver and reason")
    if task_id is not None and approval.task_id != task_id:
        raise PermissionError("approval task does not match requested task")
