# NOVA Provider-Agnostic Data Abstraction Layer v0.1

**Status:** Foundational  
**Authority:** NOVA CORP

## Purpose

Create one stable boundary between external information providers and NOVA Intelligence.

```
PROVIDER -> ADAPTER -> NORMALIZED OBSERVATION -> SIGNAL -> EVIDENCE
```

Adapters are read-only in v0.1 and return provider-neutral contracts. Provider payloads, SDK types, API field names, authentication details, and vendor-specific semantics must not leak into the canonical domain.

## Contracts

- `DataProviderAdapter`: stable adapter interface.
- `ProviderCapabilities`: explicit declared capabilities.
- `RetrievalMetadata`: retrieval time, request identity, duration, freshness and error semantics.
- `NormalizedObservation`: provider-neutral observation.
- `AcquisitionResult`: auditable success/partial/failure boundary.
- `normalize_observation`: deterministic normalization and stable observation ID.

## Rules

1. Provider adapters never create Signals directly.
2. Provider adapters never create Evidence directly.
3. Every successful acquisition records retrieval metadata.
4. Failed acquisitions cannot expose observations.
5. Observation IDs are deterministic from normalized source/account/time/reference/content/provenance.
6. Provider-specific metadata may be retained only inside the adapter layer; canonical observations expose generic metadata.
7. Capabilities are declarations, not assumptions.
8. v0.1 acquisition is read-only.
9. Paid providers are not required for the contract.
10. The abstraction must be reusable by future NOVA products.

## Freshness and errors

Freshness is explicit: `fresh`, `stale`, or `unknown`.

Acquisition status is explicit: `success`, `partial`, or `failed`.

A failed acquisition cannot silently produce observations. Partial results remain auditable through the acquisition status and retrieval metadata.

## Non-goals

This block does not implement scraping, crawling, CRM, outbound automation, provider-specific Paraguay integrations, paid-data dependencies, or production write actions.

Those are later adapters/capabilities built behind this boundary.

## Next step

Implement the first real read-only provider adapter against a measurable public source. The adapter must feed canonical observations and preserve provenance, retrieval time, freshness, deterministic IDs, and errors.
