"""Deterministic append-only audit trail for Product Factory v0.1."""
from __future__ import annotations

from typing import Sequence

from factory.execution.contracts import AuditEvent


class AuditTrail:
    """In-memory append-only audit trail for deterministic v0.1 workflows."""

    def __init__(self, events: Sequence[AuditEvent] = ()) -> None:
        self._events: list[AuditEvent] = []
        self._event_ids: set[str] = set()
        for event in events:
            self.append(event)

    def append(self, event: AuditEvent) -> None:
        if event.event_id in self._event_ids:
            raise ValueError(f"duplicate audit event: {event.event_id}")
        self._events.append(event)
        self._event_ids.add(event.event_id)

    def list(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)

    def for_execution(self, execution_id: str) -> tuple[AuditEvent, ...]:
        if not execution_id.strip():
            raise ValueError("execution_id must be non-empty")
        return tuple(event for event in self._events if event.execution_id == execution_id)
