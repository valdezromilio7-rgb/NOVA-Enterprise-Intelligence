# NOVA Agent Approval Record v0.1

## Purpose

Sensitive agent capabilities require an explicit, auditable approval record rather than an unstructured boolean.

## Contract

`CapabilityApproval` records the agent, capability, approver, reason, UTC approval timestamp, and optional task identity.

The creation function refuses capabilities outside the agent policy and requires an approver and reason.

Validation verifies that the approval matches the agent policy, requested capability, and optional task boundary.

## Governance boundary

This artifact authorizes only the specific capability represented by the record. It does not grant new capabilities, credentials, budget, deployment access, or unrestricted autonomy.

It is an authorization artifact that can be attached to later tool-execution audit events.

## Next integration

The execution layer may consume this artifact when invoking a concrete tool while preserving least privilege and traceability.
