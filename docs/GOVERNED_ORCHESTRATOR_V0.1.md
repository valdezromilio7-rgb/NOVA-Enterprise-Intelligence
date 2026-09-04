# NOVA Governed Orchestrator v0.1

Status: Proposed / Implemented v0.1
Authority: NOVA CORP

## Purpose

The Governed Orchestrator coordinates bounded agent executions. It is not an authority layer and it does not execute arbitrary code.

## Execution sequence

1. Receive an immutable `ExecutionContract`.
2. Authorize the contract through the canonical `AgentRegistry`.
3. Record authorization as an `AuditEvent`.
4. Stop immediately when authorization fails.
5. Resolve an explicitly registered executor for the task type.
6. Record `STARTED` before invoking the executor.
7. Record `SUCCEEDED` with output references, or `FAILED` with a non-sensitive error code.

## Governance rules

- The Registry is the source of agent capability authority.
- The orchestrator cannot expand tools, data access, write access, financial limits, or task permissions.
- A missing executor is a controlled failure, never an implicit fallback.
- Executor exceptions are not copied into the audit trail; only a stable error class/code is recorded.
- Audit events are append-only through the v0.1 `AuditTrail`.
- External side effects belong to explicitly registered executors and remain subject to the contract and upstream governance gates.

## v0.1 limitations

This implementation is intentionally in-memory and synchronous. It does not yet provide distributed locking, persistent event storage, retries, queues, secrets management, human approval UI, or production tool adapters.

Those capabilities must be added without weakening the authorization boundary.

## Future state

The orchestrator will later coordinate multi-step workflows, but every child execution must receive its own bounded contract and remain independently auditable. No recursive delegation may bypass NOVA CORP governance.
