# NOVA Workflow State + Failure Policy v0.1

## Purpose

Define the deterministic runtime state and fail-safe behavior for Product Factory workflows.

## States

`PLANNED → RUNNING → SUCCEEDED`

A running workflow may instead terminate as `FAILED`, `BLOCKED`, or `CANCELLED` according to an explicit policy.

## Rules

- Workflows start only from `PLANNED`.
- Steps can succeed only while the workflow is `RUNNING`.
- A step cannot be marked successful twice.
- Step failures default to `FAILED` (`STOP`).
- Authorization failures default to `BLOCKED`.
- Cancellation must be explicitly configured.
- Empty failure codes are invalid.
- No automatic retry is introduced in v0.1.
- No state transition bypasses governance or the Agent Registry.

## Design Principle

Failure is a controlled state, not an instruction to improvise. The factory must stop or block rather than silently change agent, permissions, tools, workflow, or policy.

## Future Extensions

Retries, resumable checkpoints, persistence backends, timeouts, compensation actions, and parallel execution require separate contracts and evaluation before adoption.
