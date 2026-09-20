"""Auditable execution state for bounded agent tasks."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone
from factory.agent_execution import BuildTask

class TaskStatus(str, Enum):
    PLANNED="planned"; AUTHORIZED="authorized"; RUNNING="running"; SUCCEEDED="succeeded"; FAILED="failed"; BLOCKED="blocked"

@dataclass(frozen=True)
class TaskExecution:
    task_id: str
    status: TaskStatus
    actor: str
    started_at: str
    finished_at: str | None = None
    output_ref: str | None = None
    error: str | None = None

def authorize_task(task: BuildTask, *, actor: str) -> TaskExecution:
    if not actor.strip(): raise ValueError("actor must be non-empty")
    return TaskExecution(task_id=task.id,status=TaskStatus.AUTHORIZED,actor=actor,started_at=datetime.now(timezone.utc).isoformat())

def complete_task(execution: TaskExecution, *, output_ref: str) -> TaskExecution:
    if execution.status is not TaskStatus.AUTHORIZED and execution.status is not TaskStatus.RUNNING:
        raise ValueError("task must be authorized or running")
    if not output_ref.strip(): raise ValueError("output_ref must be non-empty")
    return TaskExecution(task_id=execution.task_id,status=TaskStatus.SUCCEEDED,actor=execution.actor,started_at=execution.started_at,finished_at=datetime.now(timezone.utc).isoformat(),output_ref=output_ref)
