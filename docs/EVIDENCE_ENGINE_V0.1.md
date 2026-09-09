# NOVA Evidence Engine v0.1

## Purpose

The Evidence Engine creates the canonical layer between raw source observations and downstream Account Intelligence reasoning.

It enforces the distinction:

**Observation ≠ Evidence ≠ Signal ≠ Opportunity**

## Contract

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

Verification states are:

- `UNVERIFIED` — claim exists but has not been verified;
- `VERIFIED` — deterministic support checks pass;
- `CONFLICTING` — observations support incompatible interpretations and no silent resolution is performed;
- `UNVERIFIABLE` — claim cannot currently be verified and therefore cannot carry positive strength.

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

`SourceObservation → Evidence → Context → Why Now → Business Problem → Opportunity`

The current Context/Why Now/Business Problem contracts can carry canonical evidence references. The Opportunity bridge must place only canonical Evidence IDs in `Opportunity.evidence_ids`; raw observation references remain metadata until evidence records exist.

## v0.1 limitation

The deterministic engine validates structural support and explicit verification state. It does not establish semantic truth across independent external sources. Cross-source corroboration, contradiction detection, provider adapters, and model-assisted verification are later capabilities and must be evaluated before production autonomy.

## Acceptance evidence

Unit tests cover:

- deterministic identity;
- observation linkage;
- verified evidence;
- unsupported verification rejection;
- explicit conflict representation;
- unverifiable evidence constraints.
