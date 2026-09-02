# NOVA Agent Registry — Specification v0.1

**Status:** Proposed / Foundational
**Authority:** NOVA CORP

## 1. Purpose

Provide a canonical registry for every agent allowed to execute work inside the NOVA Product Factory.

An agent is a bounded execution component, not an independent authority.

## 2. Required agent definition

Each registered agent must declare:

- `agent_id`
- `name`
- `version`
- `role`
- `description`
- `allowed_tasks`
- `forbidden_tasks`
- `input_contracts`
- `output_contracts`
- `tools`
- `data_access`
- `write_access`
- `financial_limit`
- `execution_limit`
- `escalation_rules`
- `evaluation_suite`
- `owner`
- `status`

## 3. Initial agent classes

### Research
Find and synthesize evidence within an explicitly defined research scope.

### Market Intelligence
Analyze demand, competition, pricing, distribution, and market structure.

### Validation
Design and interpret validation experiments. It may recommend actions but cannot independently commit material spend.

### Product
Transform validated opportunities into structured product specifications.

### Architecture
Check proposed systems against NOVA architecture and identify required decisions/ADRs.

### Engineering
Implement bounded technical tasks against an approved specification.

### QA
Test functionality, regressions, edge cases, and acceptance criteria.

### Security
Perform security analysis and release checks within approved scope.

### DevOps
Handle bounded build/deployment/observability tasks with explicit environment permissions.

### Growth
Generate and evaluate acquisition/retention experiments within approved limits.

### Finance
Model unit economics, budgets, and financial scenarios. It cannot approve its own spending.

### Documentation
Maintain canonical documentation and traceability artifacts.

### Supervisor / Orchestrator
Decompose approved workflows, dispatch tasks, collect outputs, detect failures, and escalate. It cannot override governance gates.

## 4. Permission model

Permissions are least-privilege and task-scoped.

A task must explicitly declare:

- required tools;
- data classification;
- read/write scope;
- external side effects;
- budget exposure;
- required approval level.

No agent receives production credentials merely because it is registered.

## 5. Execution contract

Every execution records:

```text
execution_id
agent_id + version
task_id
workflow_id
input_artifact_ids
output_artifact_ids
start/end timestamps
status
failure/retry information
model/provider metadata when applicable
cost metadata when available
human approvals/escalations
```

## 6. Idempotency and retries

Tasks that can create side effects must have an idempotency strategy.

Retries must not silently duplicate external actions.

Failed tasks are retried only within declared limits. Repeated failure triggers escalation rather than infinite autonomous retries.

## 7. Model/provider abstraction

Agent definitions must not hard-code a single LLM provider as part of the business contract.

The execution layer should support provider/model substitution while preserving:

- task contract;
- evaluation criteria;
- audit metadata;
- cost tracking;
- safety constraints.

## 8. Evaluation before autonomy

An agent may gain broader permissions only after measured evaluation demonstrates acceptable:

- task success;
- factual reliability;
- regression resistance;
- security behavior;
- cost efficiency;
- escalation behavior.

Autonomy is earned by evidence.

## 9. Agent lifecycle

`DRAFT -> EVALUATING -> APPROVED -> ACTIVE -> RESTRICTED -> RETIRED`

Any safety or reliability regression can move an agent to `RESTRICTED`.

## 10. Registry principle

The registry is the control point for agent capability. Prompts alone are not an authorization system.
