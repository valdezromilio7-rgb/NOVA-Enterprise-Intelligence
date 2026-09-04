# NOVA Workflow Engine v0.1

## Purpose

The Workflow Engine defines and runs ordered business processes composed of bounded agent executions. It is a coordination layer, not an authority layer.

## Architecture

```text
Workflow Definition
        |
        v
  Workflow Step
        |
        v
Execution Contract
        |
        v
Governed Orchestrator
        |
        +--> Agent Registry authorization
        |
        +--> Executor
        |
        +--> Audit Trail
```

## Invariants

1. Every step declares an agent, exact agent version, task type, output contract, and required permissions.
2. Every step is submitted through the Governed Orchestrator.
3. The Workflow Engine cannot grant permissions or bypass Agent Registry authorization.
4. Steps execute sequentially in declared order in v0.1.
5. A rejected or failed step stops the workflow; there is no implicit fallback.
6. Workflow and execution identifiers are deterministic for reproducible tests.
7. External side effects remain behind registered executors and existing governance boundaries.
8. Workflow state is observable through step results and the underlying Audit Trail.

## v0.1 Scope

Included:

- immutable workflow and step definitions;
- deterministic definition identifiers;
- sequential execution;
- fail-stop behavior;
- reuse of Execution Contract and Governed Orchestrator;
- unit-test coverage.

Explicitly deferred:

- parallel execution;
- retries;
- scheduling;
- persistent workflow state;
- distributed queues;
- automatic compensation/rollback;
- dynamic workflow mutation.

These capabilities require additional reliability and governance controls and must not be introduced implicitly.

## Authority Boundary

The Workflow Engine coordinates. The Agent Registry authorizes. The Governed Orchestrator enforces the execution boundary. NOVA CORP remains the ultimate governance authority.
