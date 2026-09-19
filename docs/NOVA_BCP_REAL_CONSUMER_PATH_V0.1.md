# NOVA BCP Real Consumer Path v0.1

The BCP adapter now has an explicit orchestration boundary that consumes its real provider-neutral acquisition result and emits the canonical Signal and Evidence contracts.

Flow:

BCP -> BcpDailyCurrencyAdapter -> NormalizedObservation -> canonical Signal + canonical Evidence

The pipeline does not create an account for public BCP data. The resulting Signal and Evidence retain account_id=None and preserve the observation ID as lineage.

Verification is explicit in this first controlled path because the BCP adapter is the authoritative read-only source for the observed reference-rate claim; downstream consumers must not infer additional facts from it.

This block intentionally stops before Context, Why Now, Business Problem and Opportunity. Those stages require a generic public-market contract rather than an account-shaped workaround.
