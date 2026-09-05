# NOVA Account Intelligence v0.1

**Status:** P0 foundation implemented  
**Authority:** NOVA CORP

## Objective

Establish the first executable vertical for:

`ACCOUNT → SIGNAL → OPPORTUNITY → VERIFIED ACTION`

v0.1 is a laboratory foundation. It does not claim commercial readiness.

## Architecture

```text
Approved Sources
      ↓
Source Registry
      ↓
Source Observations
      ↓
Normalization / Deterministic IDs
      ↓
Account + Account Signals
      ↓
Existing Opportunity Engine
      ↓
Validation / Governance
      ↓
Bounded Agent Execution
      ↓
Audit / Evaluation
```

## Domain contracts

### Account

Canonical business identity independent of provider identifiers.

### Source

Declaration of an information source. A source is not evidence by itself.

### SourceObservation

An observed fact tied to a source and account, including timestamp, reference, provenance, and confidence.

### AccountSignal

An interpreted account-scoped signal backed by one or more observations.

## Provider independence

Provider-specific identifiers must remain source references. The canonical account ID is deterministic from normalized identity attributes and is not derived from a vendor ID.

Future adapters may map DIRGE/INE, DNCP, web, news, jobs, technology, or customer data into the source/observation contracts without changing downstream business logic.

## Evaluation

`SignalPrecisionResult` measures exact-match precision against independently supplied truth. v0.1 intentionally does not hide a universal scoring formula or invent ground truth.

The existing Opportunity Engine remains the opportunity-ranking component. Account Intelligence supplies structured, traceable inputs to it.

## Security and governance

- No credentials or secrets in domain contracts.
- No external side effects in this foundation.
- No paid data-provider dependency.
- No autonomous outbound activity.
- Existing Agent Registry, Execution Contract, Governed Orchestrator, Workflow State, and Audit Trail remain the execution boundaries.

## Explicitly deferred

- Persistent storage.
- Real source connectors.
- Browser automation.
- Entity-resolution beyond deterministic identity primitives.
- Human verification UI.
- SaaS tenancy and billing.
- Automated outbound communication.

## Acceptance gate

This foundation is complete only when unit tests and CI pass. Commercial validation starts only after real-source adapters and human verification are implemented and evaluated.
