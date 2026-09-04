"""Deterministic workflow state and failure policy primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class WorkflowState(str, Enum):
    PLANNED = "PLANNED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


class FailureAction(str, Enum):
    STOP = "STOP"
    BLOCK = "BLOCK"
    CANCEL = "CANCEL"


@dataclass(frozen=True)
class FailurePolicy:
    """Explicit fail-safe policy; retries are intentionally out of scope."""

    policy_version: str = "failure-policy-v0.1"
    on_step_failure: FailureAction = FailureAction.STOP
    on_authorization_failure: FailureAction = FailureAction.BLOCK


@dataclass
class WorkflowRunState:
    """Minimal mutable runtime state for one workflow execution."""

    workflow_id: str
    workflow_version: str
    state: WorkflowState = WorkflowState.PLANNED
    current_step_id: Optional[str] = None
    completed_step_ids: list[str] = field(default_factory=list)
    failure_step_id: Optional[str] = None
    failure_code: Optional[str] = None

    def start(self) -> None:
        if self.state is not WorkflowState.PLANNED:
            raise ValueError("workflow can only start from PLANNED")
        self.state = WorkflowState.RUNNING

    def mark_step_succeeded(self, step_id: str) -> None:
        if self.state is not WorkflowState.RUNNING:
            raise ValueError("step success requires RUNNING workflow")
        if step_id in self.completed_step_ids:
            raise ValueError("step already completed")
        self.completed_step_ids.append(step_id)
        self.current_step_id = None

    def mark_failed(self, step_id: str, failure_code: str, policy: FailurePolicy) -> None:
        if self.state is not WorkflowState.RUNNING:
            raise ValueError("failure requires RUNNING workflow")
        if not failure_code.strip():
            raise ValueError("failure_code must not be empty")
        self.failure_step_id = step_id
        self.failure_code = failure_code
        action = policy.on_step_failure
        self.state = {
            FailureAction.STOP: WorkflowState.FAILED,
            FailureAction.BLOCK: WorkflowState.BLOCKED,
            FailureAction.CANCEL: WorkflowState.CANCELLED,
        }[action]
        self.current_step_id = None

    def mark_authorization_blocked(self, step_id: str, policy: FailurePolicy) -> None:
        if self.state is not WorkflowState.RUNNING:
            raise ValueError("authorization block requires RUNNING workflow")
        self.failure_step_id = step_id
        self.failure_code = "AUTHORIZATION_DENIED"
        action = policy.on_authorization_failure
        self.state = {
            FailureAction.STOP: WorkflowState.FAILED,
            FailureAction.BLOCK: WorkflowState.BLOCKED,
            FailureAction.CANCEL: WorkflowState.CANCELLED,
        }[action]
        self.current_step_id = None

    def finish(self) -> None:
        if self.state is not WorkflowState.RUNNING:
            raise ValueError("workflow can only finish from RUNNING")
        self.state = WorkflowState.SUCCEEDED
