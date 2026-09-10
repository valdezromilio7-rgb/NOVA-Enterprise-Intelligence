# NOVA Account Intelligence — Evidence Integration v0.1

## Purpose

Close the evidence boundary in the Account Intelligence evaluation chain.

The verified architecture is:

`SourceObservation → Evidence → Signal → Context → Why Now → Business Problem → Opportunity`

The evaluation harness measures signal precision against independent benchmark labels, while downstream reasoning carries only canonical Evidence IDs.

## Contract boundary

- `SourceObservation` is raw source material.
- `Evidence` is a canonical claim supported by one or more observations.
- `AccountSignal` is an interpretation extracted from observations.
- `AccountContext`, `WhyNowAssessment`, and `BusinessProblem` reference canonical Evidence IDs.
- `Opportunity.evidence_ids` contains canonical Evidence IDs, never raw observation IDs.

## Evaluation

The synthetic v0.1 harness runs 100 deterministic accounts, extracts 32 candidate signals, ranks the top 20, and evaluates precision independently. The current fixture baseline reaches 20/20 precision because its distractor design is intentionally simple; this is a regression benchmark, not evidence of production market performance.

The selected top signal is converted into one canonical Evidence record and propagated through Context, Why Now, Business Problem, and Opportunity. Repeated runs must produce identical artifacts.

## Governance

This integration does not add provider connectors, scraping, CRM access, outbound messaging, LLM verification, autonomous spending, or production side effects. Evidence verification remains structurally bounded in v0.1; semantic truth and cross-source corroboration require a later evaluated capability.

## Architectural cleanup note

The repository currently contains an older `factory.schemas.domain.Evidence` contract and the richer Account Intelligence Evidence contract. They must not evolve independently. A later refactor should establish one canonical Evidence contract and migrate callers without breaking the Product Factory governance boundary.
