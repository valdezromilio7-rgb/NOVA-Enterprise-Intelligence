# NOVA Product Factory — Execution Contract & Audit Trail v0.1

Status: Proposed / Implementation v0.1
Authority: NOVA CORP

## Purpose

The Execution Contract is the boundary between an authorized agent and an execution attempt. It makes the intended task, agent version, required capabilities, data access, write access, input references, output contract, and budget exposure explicit before execution.

The Audit Trail records lifecycle transitions and references to inputs, outputs, and evidence. It is append-oriented: execution code should emit events rather than silently mutate an execution history.

## Control flow

```text
Agent Registry
      ↓
Execution Contract
      ↓
Authorization
      ↓
Execution attempt
      ↓
Artifacts / Decisions
      ↓
Audit Event
      ↓
Evaluation
```

## Non-goals

- This layer does not execute arbitrary code.
- It does not choose an LLM provider.
- It does not replace NOVA governance gates.
- It does not grant permissions through prompts or natural-language instructions.
- It does not provide a production database in v0.1.

## Execution Contract requirements

Every contract must identify:

- execution ID;
- agent ID and exact agent version;
- task type;
- input references;
- output contract;
- required tools and data/write access;
- budget exposure;
- optional parent execution;
- policy version.

Authorization is delegated to the canonical Agent Registry. A contract is rejected when the agent is not authorized, the requested capability is outside its allow-list, a required tool/data/write permission is missing, the financial limit is exceeded, or the contract agent version differs from the registered version.

## Audit requirements

An audit event records:

- event type;
- execution ID;
- agent identity/version;
- lifecycle status;
- timestamp;
- input/output/evidence references;
- error code for failed execution;
- metadata;
- deterministic event ID.

The deterministic event ID is derived from the event's canonical content, making repeated identical events reproducible in v0.1 experiments.

## Security and governance

Authorization is deny-by-default. Agent identity and version are part of the execution contract. Financial exposure is checked before authorization. Sensitive actions remain subject to the separate NOVA governance gates.

Human approval is never inferred from the absence of a rejection. Governance authority remains with NOVA CORP.

## Future evolution

Production implementations may add durable storage, cryptographic integrity controls, correlation IDs, distributed tracing, idempotency keys, actor identity, environment, model/provider metadata, cost telemetry, and retention policies. Those additions must preserve the core separation between authorization, execution, and audit.
