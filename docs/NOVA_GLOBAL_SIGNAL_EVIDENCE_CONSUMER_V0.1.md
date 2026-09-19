# NOVA Global Signal + Evidence Consumer v0.1

## Purpose

This layer consumes provider-neutral NormalizedObservation objects and emits the existing canonical Signal and Evidence contracts.

It exists so public and market data can enter NOVA Intelligence without being forced into an account identity.

## Rules

- One canonical Signal remains the only signal contract.
- One canonical Evidence remains the only evidence contract.
- Global observations keep account_id=None.
- Account-scoped observations retain their account identity.
- Mixed account scopes cannot produce one Evidence object.
- Adapters never create Signals or Evidence directly.
- Provider-specific SDK/API types do not cross into canonical domain contracts.
- IDs are deterministic and preserve observation lineage.
- Verification is explicit; consumers never silently upgrade evidence state.

## Flow

PROVIDER -> ADAPTER -> NORMALIZED OBSERVATION -> CANONICAL SIGNAL / CANONICAL EVIDENCE

For BCP:

BCP -> bcp adapter -> USD/PYG NormalizedObservation -> Signal + Evidence

This is the first real global-data path in NOVA Intelligence. Context, Why Now, Business Problem and Opportunity remain separate stages until their contracts are generalized without inventing account scope.

## Non-goals

- No fake account identities.
- No provider-specific domain models.
- No autonomous production actions.
- No broad scraping platform.
- No duplicate Signal/Evidence classes.
