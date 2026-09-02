# NOVA Product Factory — Build Plan v0.1

**Status:** Proposed / Execution
**Authority:** NOVA CORP
**System:** NOVA Enterprise Intelligence

## 1. Objective

Implement the smallest end-to-end factory capable of receiving an opportunity, collecting evidence, scoring it, producing a validation plan, converting an approved opportunity into a product specification, and dispatching bounded agent tasks.

The first implementation must be deterministic, traceable, testable, and safe before external autonomy is expanded.

## 2. Build sequence

### Phase 1 — Foundation

- Establish canonical identifiers and artifact metadata.
- Define lifecycle state machine and governance gates.
- Define evidence provenance and confidence rules.
- Define agent registry and permission boundaries.
- Define execution/audit event model.

### Phase 2 — Opportunity Engine

- Ingest opportunity signals from structured/manual sources.
- Normalize signals.
- Deduplicate and cluster related signals.
- Separate evidence, inference, and assumptions.
- Generate opportunity records with provenance.

### Phase 3 — Scoring

- Implement transparent weighted scoring.
- Keep weights versioned and configurable.
- Store every component score and rationale.
- Penalize uncertainty and execution risk.
- Never present a score without its evidence basis.

### Phase 4 — Validation

- Generate validation hypotheses.
- Define target customer/persona.
- Define minimum evidence thresholds.
- Define experiment, metric, sample target, cost, and stop conditions.
- Record outcomes and update confidence.

### Phase 5 — Product Specification

For approved opportunities generate:

- problem statement;
- target user/customer;
- promise/value proposition;
- business model;
- MVP scope;
- non-goals;
- functional requirements;
- non-functional requirements;
- architecture constraints;
- data model requirements;
- AI/agent requirements where applicable;
- security/privacy requirements;
- analytics and telemetry;
- acceptance criteria;
- implementation backlog.

### Phase 6 — Bounded Agent Execution

- Register specialized agents.
- Create tasks with explicit scopes and permissions.
- Execute idempotently.
- Record inputs, outputs, artifacts, model/provider metadata where available, costs, and failures.
- Escalate when a task exceeds its authority.

### Phase 7 — Evaluation

Run the complete workflow against the existing simulation laboratory before connecting consequential external systems.

Measure:

- opportunity detection quality;
- ranking quality;
- evidence/assumption separation;
- validation recommendation quality;
- specification completeness;
- agent task success rate;
- traceability;
- cost and latency;
- false positives/false negatives.

## 3. Canonical workflow

```text
SIGNAL
  -> OPPORTUNITY
  -> SCORE
  -> VALIDATION PLAN
  -> HUMAN/DELEGATED GATE
  -> PRODUCT SPEC
  -> TASK GRAPH
  -> BOUNDED AGENT EXECUTION
  -> QA/EVALUATION
  -> ARTIFACTS + OUTCOMES
  -> LEARNING
```

## 4. Initial repository boundary

The existing simulation laboratory remains the controlled evaluation environment.

```text
simulator/       controlled reality generator
ground_truth/    hidden evaluation truth
nova/            intelligence experiments
evaluation/      experiment scoring

factory/         Product Factory execution layer (new)
docs/            canonical architecture and specifications
```

The factory must not contaminate ground truth during evaluation.

## 5. Technology policy

Do not lock the architecture to a large infrastructure stack prematurely. Technology choices must follow the workload and reliability requirements.

Initial implementation should favor:

- typed schemas;
- deterministic Python components where practical;
- versioned configuration;
- Git-native artifacts;
- explicit interfaces between modules;
- local/reproducible evaluation;
- provider abstraction for LLMs;
- replaceable workflow/orchestration layer.

## 6. Definition of Done for v0.1

A single opportunity can travel from intake to a decision-ready product specification through a reproducible workflow, with:

1. unique identifiers;
2. evidence provenance;
3. explainable score;
4. validation plan;
5. explicit gate status;
6. product specification;
7. bounded task graph;
8. audit trail;
9. deterministic replay where possible;
10. automated tests;
11. evaluation results;
12. no unauthorized production action.

## 7. Immediate implementation order

1. `OPPORTUNITY_ENGINE_SPEC_V0.1.md`
2. `AGENT_REGISTRY_SPEC_V0.1.md`
3. `DECISION_GATES_V0.1.md`
4. canonical schemas under `factory/schemas/`
5. deterministic Opportunity Engine prototype
6. scoring tests
7. validation workflow prototype
8. product-spec generation contract
9. bounded orchestration prototype
10. simulation-based end-to-end evaluation

## 8. Operating rule

We do not optimize for the number of agents. We optimize for validated outcomes per unit of capital, time, and human attention.
