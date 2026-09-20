"""Explicit capability boundary for NOVA agents."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet

class Capability(str, Enum):
    READ_REPO="read_repo"; WRITE_REPO="write_repo"; RUN_TESTS="run_tests"; CREATE_PR="create_pr"
    DEPLOY="deploy"; SPEND="spend"; ACCESS_SECRETS="access_secrets"

@dataclass(frozen=True)
class AgentPolicy:
    agent_id: str
    allowed: FrozenSet[Capability]
    approval_required: FrozenSet[Capability] = frozenset()

    def permits(self, capability: Capability) -> bool:
        return capability in self.allowed and capability not in self.approval_required

    def requires_approval(self, capability: Capability) -> bool:
        return capability in self.approval_required

def authorize_capability(policy: AgentPolicy, capability: Capability, *, approved: bool=False) -> None:
    if capability not in policy.allowed:
        raise PermissionError(f"capability not allowed: {capability.value}")
    if capability in policy.approval_required and not approved:
        raise PermissionError(f"explicit approval required: {capability.value}")
