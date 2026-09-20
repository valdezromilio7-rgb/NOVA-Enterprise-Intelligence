import pytest

from factory.agent_approval import create_capability_approval, validate_capability_approval
from factory.agent_permissions import AgentPolicy, Capability


def test_sensitive_capability_approval_is_auditable():
    policy = AgentPolicy("agent-1", frozenset({Capability.DEPLOY}), frozenset({Capability.DEPLOY}))
    approval = create_capability_approval(policy=policy, capability=Capability.DEPLOY, approver="human-1", reason="approved production release", task_id="task-1")
    assert approval.agent_id == "agent-1"
    assert approval.capability is Capability.DEPLOY
    assert approval.task_id == "task-1"
    validate_capability_approval(approval, policy=policy, capability=Capability.DEPLOY, task_id="task-1")


def test_approval_cannot_cross_agent_or_capability_boundaries():
    policy = AgentPolicy("agent-1", frozenset({Capability.DEPLOY}), frozenset({Capability.DEPLOY}))
    approval = create_capability_approval(policy=policy, capability=Capability.DEPLOY, approver="human-1", reason="approved")
    other_policy = AgentPolicy("agent-2", frozenset({Capability.DEPLOY}), frozenset({Capability.DEPLOY}))
    with pytest.raises(PermissionError):
        validate_capability_approval(approval, policy=other_policy, capability=Capability.DEPLOY)
    with pytest.raises(PermissionError):
        validate_capability_approval(approval, policy=policy, capability=Capability.SPEND)
