import pytest
from factory.agent_permissions import AgentPolicy, Capability, authorize_capability

def test_agent_capability_is_explicit():
    p=AgentPolicy("agent-1",frozenset({Capability.READ_REPO,Capability.RUN_TESTS}),frozenset())
    authorize_capability(p,Capability.READ_REPO)
    with pytest.raises(PermissionError):
        authorize_capability(p,Capability.DEPLOY)

def test_sensitive_capability_requires_approval():
    p=AgentPolicy("agent-1",frozenset({Capability.DEPLOY}),frozenset({Capability.DEPLOY}))
    with pytest.raises(PermissionError):
        authorize_capability(p,Capability.DEPLOY)
    authorize_capability(p,Capability.DEPLOY,approved=True)
