# NOVA Product Factory — Gate 1 Implementation v0.1

**Status:** Implemented
**Authority:** NOVA CORP

## Purpose

Gate 1 is the executable boundary between discovery and validation execution. It converts explicit opportunity evidence, score, validation plan, and risk/side-effect context into a deterministic `Decision` record.

It is governance code, not an LLM decision-maker.

## Inputs

- `Opportunity`
- `OpportunityScore`
- `ValidationExperiment`
- `Gate1Context`
- versioned `Gate1Policy`

## Policy

The default policy requires at least one evidence ID and permits automatic execution only when validation spend is zero and there is no elevated risk, sensitive-data processing, or external commitment.

The minimum score threshold is configurable and disabled by default so the factory does not invent a universal business cutoff before sufficient calibration data exists.

## Outcomes

- `APPROVE`: validation may proceed under the evaluated policy.
- `HOLD`: execution stops pending evidence, policy conditions, or explicit human approval.
- `REJECT`: explicit human rejection is recorded.

Silence is never interpreted as approval.

## Auditability

The resulting `Decision` records the opportunity, gate, outcome, rationale, actor, and evidence IDs. The evaluation also exposes machine-readable reasons and whether human approval is required.

## Next evolution

Gate 1 should later integrate with a persistent approval/audit event store and a versioned NOVA CORP delegation policy. Those are separate concerns and should not be hidden inside this gate implementation.
