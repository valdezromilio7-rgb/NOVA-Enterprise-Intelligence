"""Governed task orchestration for Product Factory v0.1.

The orchestrator coordinates bounded execution. It does not grant authority,
select tools implicitly, or execute arbitrary code. Authorization remains the
responsibility of the Agent Registry and the resulting lifecycle is recorded
in the Audit Trail.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Sequence

from factory.execution.audit import AuditTrail
from factory.execution.contracts import (
    AuditEvent,
    ExecutionContract,
    ExecutionStatus,
    authorize_execution,
)
from factory.agents.registry import AgentRegistry


Executor = Callable[[ExecutionContract], Sequence[str]]


@dataclass(frozen=True)
class OrchestrationResult:
    """Deterministic summary of one orchestration attempt."""

    execution_id: str
    status: ExecutionStatus
    authorized: bool
    output_refs: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()


class GovernedOrchestrator:
    """Coordinate only executions that pass the canonical authorization boundary."""

    def __init__(
        self,
        registry: AgentRegistry,
        audit_trail: AuditTrail | None = None,
        executors: Mapping[str, Executor] | None = None,
    ) -> None:
        self.registry = registry
        self.audit_trail = audit_trail or AuditTrail()
        self.executors = dict(executors or {})

    def submit(self, contract: ExecutionContract) -> OrchestrationResult:
        """Authorize, execute a registered handler, and record lifecycle events.

        A missing handler is a controlled failure, not an authorization grant.
        No external side effect is performed by this orchestration layer itself.
        """
        authorization = authorize_execution(contract, self.registry)
        authorization_status = (
            ExecutionStatus.AUTHORIZED if authorization.authorized else ExecutionStatus.REJECTED
        )
        self.audit_trail.append(
            AuditEvent(
                event_type="execution.authorization",
                execution_id=contract.execution_id,
                agent_id=contract.agent_id,
                agent_version=contract.agent_version,
                status=authorization_status,
                timestamp="DETERMINISTIC",
                input_refs=contract.input_refs,
                metadata={"policy_version": contract.policy_version},
            )
        )

        if not authorization.authorized:
            return OrchestrationResult(
                execution_id=contract.execution_id,
                status=ExecutionStatus.REJECTED,
                authorized=False,
                reasons=authorization.reasons,
            )

        executor = self.executors.get(contract.task_type)
        if executor is None:
            reason = "executor_not_registered"
            self.audit_trail.append(
                AuditEvent(
                    event_type="execution.failure",
                    execution_id=contract.execution_id,
                    agent_id=contract.agent_id,
                    agent_version=contract.agent_version,
                    status=ExecutionStatus.FAILED,
                    timestamp="DETERMINISTIC",
                    input_refs=contract.input_refs,
                    error_code=reason,
                )
            )
            return OrchestrationResult(
                execution_id=contract.execution_id,
                status=ExecutionStatus.FAILED,
                authorized=True,
                reasons=(reason,),
            )

        self.audit_trail.append(
            AuditEvent(
                event_type="execution.started",
                execution_id=contract.execution_id,
                agent_id=contract.agent_id,
                agent_version=contract.agent_version,
                status=ExecutionStatus.STARTED,
                timestamp="DETERMINISTIC",
                input_refs=contract.input_refs,
            )
        )

        try:
            output_refs = tuple(executor(contract))
        except Exception as exc:
            error_code = f"executor_error:{type(exc).__name__}"
            self.audit_trail.append(
                AuditEvent(
                    event_type="execution.failure",
                    execution_id=contract.execution_id,
                    agent_id=contract.agent_id,
                    agent_version=contract.agent_version,
                    status=ExecutionStatus.FAILED,
                    timestamp="DETERMINISTIC",
                    input_refs=contract.input_refs,
                    error_code=error_code,
                )
            )
            return OrchestrationResult(
                execution_id=contract.execution_id,
                status=ExecutionStatus.FAILED,
                authorized=True,
                reasons=(error_code,),
            )

        self.audit_trail.append(
            AuditEvent(
                event_type="execution.succeeded",
                execution_id=contract.execution_id,
                agent_id=contract.agent_id,
                agent_version=contract.agent_version,
                status=ExecutionStatus.SUCCEEDED,
                timestamp="DETERMINISTIC",
                input_refs=contract.input_refs,
                output_refs=output_refs,
            )
        )
        return OrchestrationResult(
            execution_id=contract.execution_id,
            status=ExecutionStatus.SUCCEEDED,
            authorized=True,
            output_refs=output_refs,
        )
