# NOVA AI SaaS — EXECUTION GAP REPORT v0.1

**Date:** 2026-09-05  
**Repository:** `valdezromilio7-rgb/NOVA-Enterprise-Intelligence`  
**Authority:** NOVA CORP  
**Mode:** EXECUTION

## 1. Executive assessment

The repository has a solid governance/execution foundation, but it is still a **Product Factory core**, not an Account Intelligence product. The correct move is not to replace the existing factory architecture; it is to add a provider-agnostic Account Intelligence domain on top of it.

Current maturity is sufficient to begin the vertical safely, but not sufficient to claim a commercial MVP.

## 2. Current state

### Implemented

- Product Factory architecture and lifecycle.
- Deterministic signal normalization, clustering, opportunity scoring, and ranking.
- Validation planning and Gate 1 authorization.
- Bounded Agent Registry with explicit permissions and financial limits.
- Execution Contracts and append-only Audit Trail.
- Governed Orchestrator enforcing registry authorization.
- Workflow definitions with sequential execution and fail-stop behavior.
- Workflow runtime state and explicit failure policy.
- Deterministic simulator/evaluation laboratory with separated ground truth.
- CI workflow for factory tests.

### Evidence in repository

The current README still describes the repository primarily as an enterprise simulation laboratory. The Product Factory architecture explicitly establishes discovery, validation, bounded agent execution, governance, traceability, and learning as the intended factory capabilities. Existing domain contracts already separate Signal, Evidence, Opportunity, scoring, validation, and decisions.

## 3. Correct architecture

The following foundations should be preserved and reused:

`Opportunity Engine → Agent Registry → Execution Contract → Governed Orchestrator → Workflow State → Audit Trail`

The Account Intelligence vertical should become a domain input/output layer around these primitives, not a second orchestration stack.

## 4. Gaps

### P0 — blocking for Account Intelligence v0.1

1. No canonical `Account` domain object.
2. No canonical source/provider registry abstraction.
3. No first-class source observation/provenance contract.
4. Signal is not yet explicitly account-scoped by contract.
5. No deterministic entity-resolution contract.
6. No Account → Signal → Opportunity integration test.
7. No Signal Precision evaluation contract for the new vertical.

### P1 — required after foundation

1. Persistent run store for workflow executions.
2. Versioned source adapters for DIRGE/INE, DNCP and other approved sources.
3. Evidence coverage and freshness evaluation.
4. Cost accounting per account/signal/verified opportunity.
5. Verification workflow and human review interface.
6. Market-memory persistence.
7. Browser/runtime abstraction for future public-web research.

### P2 — deliberately deferred

- CRM.
- Automated outbound/email sequencing.
- Full SaaS multi-tenancy.
- Broad scraping infrastructure.
- Autonomous commercial commitments.
- Complex CEO dashboard.
- Large agent catalog.

## 5. What is wrong or technically risky

### 5.1 Current Signal contract is too generic

The existing Signal contract is reusable, but its fields do not make account identity, source identity, observation time, and verification semantics explicit enough for Account Intelligence. Extend it compatibly or introduce a dedicated account-intelligence observation contract; do not fork the meaning of Signal.

### 5.2 Opportunity scoring is not intelligence inference

The existing Opportunity Engine requires dimensions to be supplied externally. This is correct for deterministic testing but means it does not yet discover or infer those dimensions itself. Account Intelligence must not pretend this is already solved.

### 5.3 In-memory execution is not production persistence

Agent Registry, workflow state, and audit components currently provide deterministic runtime primitives, but durable distributed operation is not implemented. This is acceptable for v0.1 laboratory execution.

### 5.4 No real data-source adapter exists yet

The architecture anticipates provider abstraction, but the repository does not yet contain a canonical Account Intelligence source adapter layer. This is the immediate build target.

## 6. What to reuse

- `factory.schemas.domain.Signal`
- `factory.schemas.domain.Evidence`
- `factory.opportunity.*`
- `factory.validation.*`
- `factory.governance.*`
- `factory.agents.registry`
- `factory.execution.*`
- `factory.orchestration.*`
- `factory.workflow.*`
- `evaluation/product_factory/*`
- existing CI and deterministic testing approach

## 7. What to eliminate

Nothing from the current factory core should be deleted at this stage.

Do not introduce parallel versions of:

- agent authorization;
- execution contracts;
- audit logging;
- workflow orchestration;
- opportunity scoring.

Account Intelligence must consume these capabilities.

## 8. Priority map

| Priority | Work | Reason |
|---|---|---|
| P0 | Account/source/signal/evidence contracts | Domain foundation |
| P0 | Deterministic normalization + IDs | Reproducibility and deduplication |
| P0 | Account → Signal integration | Core value chain |
| P0 | Signal Precision evaluation | Prevents false claims |
| P0 | Documentation + tests + CI | Engineering gate |
| P1 | Persistent Run Store | Durable operation |
| P1 | Real source adapters | Commercial validation |
| P1 | Human verification layer | Quality control |
| P1 | Cost/usage telemetry | Unit economics |
| P2 | Product UI / SaaS packaging | Only after paid validation |

## 9. First Issue

**Issue #2 — P0: Implement NOVA Account Intelligence v0.1 foundation**

The issue defines the first executable vertical and explicitly excludes CRM, outbound automation, multi-tenancy, and autonomous production actions.

## 10. First PR

`feat(account-intelligence): establish v0.1 domain foundation`

The first PR must implement only the P0 foundation. It must not introduce real external scraping, paid data providers, outbound messaging, or production side effects.

## 11. Acceptance criteria

- Account Intelligence contracts are dependency-light and provider-agnostic.
- Source observations retain provenance and timestamps.
- Signals can be deterministically attached to accounts.
- Entity identity can be represented without binding to one provider's ID.
- Existing Opportunity Engine consumes resulting signals without bypassing governance.
- Signal Precision can be evaluated against independent/hidden truth.
- Invalid states are rejected by tests.
- CI passes.
- Architecture decisions and boundaries are documented.

## 12. Decision

**Proceed.** The repository is architecturally ready for the first Account Intelligence vertical. The next engineering unit is the Account Intelligence domain foundation, not a UI, CRM, SDR, or broad scraping system.

## 13. Next executable step

Create the P0 Account Intelligence branch and implement the canonical domain contracts plus deterministic normalization/evaluation tests. Then run CI and open the first PR.
