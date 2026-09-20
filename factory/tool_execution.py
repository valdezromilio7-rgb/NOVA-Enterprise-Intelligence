"""Governed tool execution boundary for NOVA agents."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Any
from factory.agent_approval import CapabilityApproval, validate_capability_approval
from factory.agent_permissions import AgentPolicy, Capability


@dataclass(frozen=True)
class ToolExecutionResult:
    tool_name: str
    capability: Capability
    agent_id: str
    status: str
    executed_at: str
    output_ref: str


def execute_tool(
    *,
    policy: AgentPolicy,
    capability: Capability,
    tool_name: str,
    tool: Callable[[], Any],
    approval: CapabilityApproval | None = None,
    task_id: str | None = None,
    output_ref: str | None = None,
) -> ToolExecutionResult:
    if not tool_name.strip():
        raise ValueError("tool_name must be non-empty")
    if capability not in policy.allowed:
        raise PermissionError(f"capability not allowed: {capability.value}")
    if policy.requires_approval(capability):
        if approval is None:
            raise PermissionError(f"explicit approval required: {capability.value}")
        validate_capability_approval(approval, policy=policy, capability=capability, task_id=task_id)
    result = tool()
    ref = output_ref.strip() if output_ref is not None else str(result)
    if not ref:
        raise ValueError("tool execution requires output_ref")
    return ToolExecutionResult(tool_name, capability, policy.agent_id, "succeeded", datetime.now(timezone.utc).isoformat(), ref)
