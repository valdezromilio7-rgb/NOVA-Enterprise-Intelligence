"""Deterministic workflow execution over governed agent steps.

The workflow engine coordinates declared steps; it does not grant authority.
Each step is converted to an ExecutionContract and delegated to the governed
orchestrator, which remains the single execution boundary.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping, Sequence

from factory.execution.contracts import ExecutionContract, ExecutionStatus
from factory.orchestration.orchestrator import GovernedOrchestrator


class WorkflowStatus(str, Enum):
    PLANNED = "planned"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class WorkflowStep:
    """Immutable declaration of one ordered workflow step."""

    step_id: str
    agent_id: str
    agent_version: str
    task_type: str
    output_contract: str
    input_refs: Sequence[str] = field(default_factory=tuple)
    required_tools: Sequence[str] = field(default_factory=tuple)
    required_data_access: Sequence[str] = field(default_factory=tuple)
    required_write_access: Sequence[str] = field(default_factory=tuple)
    budget_exposure: float = 0.0
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("step_id", "agent_id", "agent_version", "task_type", "output_contract"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.budget_exposure < 0:
            raise ValueError("budget_exposure must be non-negative")


@dataclass(frozen=True)
class WorkflowDefinition:
    """Immutable ordered process definition."""

    workflow_id: str
    version: str
    steps: Sequence[WorkflowStep]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.workflow_id.strip() or not self.version.strip():
            raise ValueError("workflow_id and version must be non-empty")
        if not self.steps:
            raise ValueError("workflow must contain at least one step")
        ids = [step.step_id for step in self.steps]
        if len(ids) != len(set(ids)):
            raise ValueError("workflow step IDs must be unique")

    @property
    def definition_id(self) -> str:
        payload = {
            "workflow_id": self.workflow_id,
            "version": self.version,
            "steps": [
                {
                    "step_id": step.step_id,
                    "agent_id": step.agent_id,
                    "agent_version": step.agent_version,
                    "task_type": step.task_type,
                    "output_contract": step.output_contract,
                    "input_refs": tuple(step.input_refs),
                    "required_tools": tuple(step.required_tools),
                    "required_data_access": tuple(step.required_data_access),
                    "required_write_access": tuple(step.required_write_access),
                    "budget_exposure": step.budget_exposure,
                }
                for step in self.steps
            ],
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return f"workflow:{sha256(encoded).hexdigest()}"


@dataclass(frozen=True)
class WorkflowStepResult:
    step_id: str
    execution_id: str
    status: ExecutionStatus
    output_refs: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorkflowResult:
    workflow_id: str
    definition_id: str
    status: WorkflowStatus
    step_results: tuple[WorkflowStepResult, ...]


class WorkflowEngine:
    """Run declared workflows sequentially through the governed orchestrator."""

    def __init__(self, orchestrator: GovernedOrchestrator) -> None:
        self.orchestrator = orchestrator

    def run(self, workflow: WorkflowDefinition) -> WorkflowResult:
        results: list[WorkflowStepResult] = []
        for index, step in enumerate(workflow.steps, start=1):
            execution_id = f"{workflow.definition_id}:step:{index}:{step.step_id}"
            contract = ExecutionContract(
                execution_id=execution_id,
                agent_id=step.agent_id,
                agent_version=step.agent_version,
                task_type=step.task_type,
                input_refs=step.input_refs,
                output_contract=step.output_contract,
                required_tools=step.required_tools,
                required_data_access=step.required_data_access,
                required_write_access=step.required_write_access,
                budget_exposure=step.budget_exposure,
                policy_version="workflow-v0.1",
                metadata={"workflow_id": workflow.workflow_id, "step_id": step.step_id},
            )
            result = self.orchestrator.submit(contract)
            step_result = WorkflowStepResult(
                step_id=step.step_id,
                execution_id=execution_id,
                status=result.status,
                output_refs=result.output_refs,
                reasons=result.reasons,
            )
            results.append(step_result)
            if result.status != ExecutionStatus.SUCCEEDED:
                status = WorkflowStatus.CANCELLED if result.status == ExecutionStatus.CANCELLED else WorkflowStatus.FAILED
                return WorkflowResult(workflow.workflow_id, workflow.definition_id, status, tuple(results))

        return WorkflowResult(workflow.workflow_id, workflow.definition_id, WorkflowStatus.SUCCEEDED, tuple(results))
