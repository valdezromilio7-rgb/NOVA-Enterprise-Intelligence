# NOVA Account Context + Why Now v0.1

## Purpose

This layer converts an observed Account Signal into explicit business context without inventing facts, evidence, urgency, or commercial value.

## Contract

```text
ACCOUNT
  ↓
SIGNAL
  ↓
CONTEXT
  ├─ facts
  ├─ current state
  ├─ change event
  ├─ evidence references
  └─ provenance/confidence
  ↓
WHY NOW
  ├─ trigger
  ├─ timing factors
  ├─ rationale
  ├─ evidence references
  └─ verifiability
  ↓
BUSINESS PROBLEM
  ↓
OPPORTUNITY
```

## Governance rules

1. Context may only contain explicitly supplied facts.
2. Evidence references must point to observations/evidence already available; this layer does not manufacture evidence.
3. Why Now is an assessment, not a fact. It must distinguish verified timing from reported or inferred timing.
4. A verifiable Why Now assessment requires evidence references.
5. Confidence is bounded to `[0, 1]` and must not be treated as truth probability without a defined calibration study.
6. Provider-specific APIs, scraping runtimes, LLMs, CRM systems, outbound messaging, and production side effects are outside v0.1.
7. The existing Opportunity Engine remains the canonical opportunity-scoring path.

## Reuse

The layer is intentionally compatible with the existing `Account`, `AccountSignal`, `SourceObservation`, and shared `Evidence`/`Opportunity` contracts. It does not create a second execution or authorization system.

## Next layer

The next implementation step is a deterministic business-problem bridge that requires context and Why Now inputs, preserves evidence references, and emits the existing `Opportunity` contract. Commercial scoring and execution authorization remain separate concerns.
