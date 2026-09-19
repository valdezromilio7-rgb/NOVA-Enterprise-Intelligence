# NOVA Public Business Problem → Opportunity v0.1

## Canonical flow

`PROVIDER → NORMALIZED OBSERVATION → SIGNAL → EVIDENCE → CONTEXT → WHY NOW → BUSINESS PROBLEM → OPPORTUNITY`

This block completes the provider-neutral public intelligence path through the first discovery opportunity.

## Scope

- `account_id` is optional for canonical Business Problem and Opportunity.
- Public intelligence therefore remains global; no synthetic account is created.
- Business Problem explicitly references Signal, Context, Why Now, versions, evidence references, confidence, and provenance.
- Opportunity explicitly references the Business Problem and carries only canonical Evidence IDs in `evidence_ids`.
- The bridge does not infer demand, willingness to pay, scoring, validation, or execution authorization.

## Traceability

A valid public opportunity must be traceable backward:

`Opportunity → BusinessProblem → WhyNow + Context → Signal → Evidence → Observation → Provider`

The system preserves deterministic IDs where the consumer creates a new canonical object.

## Governance boundary

This stage is **discovery**, not approval to build. Validation, scoring, product specification, agent execution, and deployment remain downstream Product Factory stages and require their existing governance gates.

## Compatibility

Existing account-scoped Business Problem and Opportunity bridges remain intact. The canonical contracts add optional global scope rather than creating parallel public-domain types.
