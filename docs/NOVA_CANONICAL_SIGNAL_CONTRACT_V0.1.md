# NOVA Canonical Signal Contract v0.1

**Status:** Foundational  
**Authority:** NOVA CORP  
**System:** NOVA Enterprise Intelligence

## Purpose

NOVA has one canonical **Signal** domain concept.

A Signal is an interpretation derived from observed information. It is not Evidence, and a Signal ID must never be stored as an Evidence ID.

## Canonical model

The canonical implementation is:

`factory.schemas.domain.Signal`

A Signal contains:

- identity: `id`
- source reference: `source`
- observation time: `observed_at`
- subject: `subject`
- interpreted content: `content`
- provenance: `provenance`
- extensible metadata: `metadata`
- optional account scope: `account_id`
- optional semantic type: `signal_type`
- supporting observations: `observation_ids`
- optional confidence: `confidence`
- optional rationale: `rationale`

Generic signals may omit account-scoped fields. Account-scoped signals must provide `account_id`, `signal_type`, and at least one `observation_id`.

## Boundary rules

```text
SOURCE -> OBSERVATION -> SIGNAL -> CONTEXT -> WHY NOW
                     |
                     +-> EVIDENCE -> OPPORTUNITY
```

- **Observation** records what was observed.
- **Signal** interprets observations.
- **Evidence** is a canonical claim supported by observations and verification state.
- **Opportunity** may reference canonical Evidence IDs only.
- Signal IDs belong in Signal references/metadata, never in `Opportunity.evidence_ids`.

## Account Intelligence migration

`AccountSignal` is no longer a second domain model. It is a compatibility constructor that returns the canonical `Signal` object.

New code must import:

```python
from factory.schemas.domain import Signal
```

The compatibility constructor exists only to avoid an abrupt break for existing callers. New modules must not introduce `AccountSignal`-style duplicate models.

## Governance rule

No new specialized Signal classes such as `IntentSignal`, `DemandSignal`, `SearchSignal`, or provider-specific Signal models may be added to the core domain.

Specialized semantics belong in `signal_type`, metadata, or higher-level engines while preserving the canonical Signal contract.

## Next architectural block

After this contract cleanup, NOVA proceeds to the provider-agnostic Data Abstraction Layer. Provider adapters must emit canonical Sources and Observations; they must not create provider-specific Signal domain models.
