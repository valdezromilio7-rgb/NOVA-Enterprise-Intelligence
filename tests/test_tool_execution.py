import pytest

from factory.agent_approval import create_capability_approval
from factory.agent_permissions import AgentPolicy, Capability
from factory.tool_execution import execute_tool


def test_tool_execution_requires_approval_for_sensitive_capability():
    policy = AgentPolicy("agent-1", frozenset({Capability.DEPLOY}), frozenset({Capability.DEPLOY}))
    with pytest.raises(PermissionError):
        execute_tool(policy=policy, capability=Capability.DEPLOY, tool_name="deploy", tool=lambda: "deployment")


def test_tool_execution_consumes_matching_approval():
    policy = AgentPolicy("agent-1", frozenset({Capability.DEPLOY}), frozenset({Capability.DEPLOY}))
    approval = create_capability_approval(policy=policy, capability=Capability.DEPLOY, approver="human-1", reason="approved", task_id="task-1")
    result = execute_tool(policy=policy, capability=Capability.DEPLOY, tool_name="deploy", tool=lambda: "release-123", approval=approval, task_id="task-1")
    assert result.status == "succeeded"
    assert result.output_ref == "release-123"


def test_tool_execution_denies_unlisted_capability():
    policy = AgentPolicy("agent-1", frozenset({Capability.READ_REPO}), frozenset())
    with pytest.raises(PermissionError):
        execute_tool(policy=policy, capability=Capability.DEPLOY, tool_name="deploy", tool=lambda: "x")
