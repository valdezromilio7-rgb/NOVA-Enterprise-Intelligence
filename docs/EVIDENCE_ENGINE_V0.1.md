# NOVA Evidence Engine v0.1

## Purpose

The Evidence Engine creates the canonical layer between raw source observations and downstream Account Intelligence reasoning.

It enforces the distinction:

**Observation ≠ Evidence ≠ Signal ≠ Opportunity**

## Canonical contract

`Evidence` is defined once in `factory.schemas.domain.Evidence` and is the shared Product Factory contract. Account Intelligence provides deterministic construction and validation in `factory.account_intelligence.evidence`; it does not define a parallel Evidence type.

An `Evidence` record contains:

- deterministic identifier;
- account identity;
- source identifiers;
- supporting observation identifiers;
- observed time;
- explicit claim;
- strength from 0 to 1;
- non-empty provenance;
- explicit verification state.

Verification states are `UNVERIFIED`, `VERIFIED`, `CONFLICTING`, and `UNVERIFIABLE`.

## Rules

1. Evidence must reference at least one observation.
2. All linked observations must belong to the same account.
3. Source linkage must be preserved.
4. Provenance is inherited from linked observations and cannot be empty.
5. Verified evidence requires positive strength and positive source-observation confidence.
6. Conflicting observations remain explicitly conflicting.
7. Unverifiable evidence cannot claim positive strength.
8. Evidence IDs are deterministic from account, observations, and claim.
9. The engine does not call external providers, scrape the web, or use an LLM for autonomous verification.
10. Evaluation ground truth is never imported by factory modules.

## Integration boundary

Current Account Intelligence flow:

`SourceObservation → Evidence → Signal → Context → Why Now → Business Problem → Opportunity`

`Opportunity.evidence_ids` may contain only canonical Evidence IDs. Raw observation IDs remain inside observation linkage and must never be relabeled as evidence.

The business-problem opportunity bridge accepts explicit Evidence IDs and does not infer or manufacture them.

## v0.1 limitation

The deterministic engine validates structural support and explicit verification state. It does not establish semantic truth across independent external sources. Cross-source corroboration, contradiction detection, provider adapters, and model-assisted verification are later capabilities and must be evaluated before production autonomy.

## Acceptance evidence

Unit tests cover deterministic identity, observation linkage, verified evidence, unsupported verification rejection, explicit conflict representation, and unverifiable evidence constraints.

The E2E evaluation uses the same canonical Evidence contract and verifies deterministic propagation into Context, Why Now, Business Problem, and Opportunity.
