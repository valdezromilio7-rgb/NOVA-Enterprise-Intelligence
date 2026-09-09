# NOVA Account Intelligence — E2E Evaluation v0.1

## Purpose

Prove that the Account Intelligence foundation can execute one reproducible chain from raw observations to a canonical Opportunity without bypassing evidence or governance boundaries.

## Evaluation chain

`RAW OBSERVATIONS → SIGNAL EXTRACTION → SIGNAL SCORING → TOP-N → PRECISION → CONTEXT → WHY NOW → BUSINESS PROBLEM → OPPORTUNITY`

## Baseline

- 100 deterministic synthetic accounts.
- 32 candidate signals extracted by the baseline rule set.
- Top 20 signals ranked deterministically.
- Precision evaluated against independently maintained synthetic labels.
- The factory domain does not import evaluation ground truth.
- The first ranked signal is transformed through Context, Why Now, Business Problem, and the canonical Opportunity contract.
- Repeated executions must produce identical result objects.

## Evidence boundary

v0.1 does not yet contain the canonical Evidence Engine. Therefore observation references are preserved as `evidence_refs` for traceability, but they are not copied into `Opportunity.evidence_ids`. Canonical Evidence IDs will be introduced by Issue #5.

The distinction is mandatory:

`Observation ≠ Evidence ≠ Signal ≠ Opportunity`

## Governance boundary

This harness is an evaluation artifact, not a production autonomous decision-maker. It does not call external providers, send outbound messages, spend money, alter production systems, or authorize execution.

The synthetic precision result is a regression benchmark only. It must not be represented as real-world market or signal performance.

## Acceptance criteria

1. 100 accounts are analyzed.
2. 32 candidate signals are extracted.
3. Top 20 are ranked and independently evaluated.
4. The baseline reaches 20/20 precision on this synthetic fixture.
5. At least one signal completes the Context → Why Now → Business Problem → Opportunity chain.
6. Provenance and observation references remain traceable.
7. Opportunity `evidence_ids` remains empty until canonical Evidence exists.
8. Repeated runs are identical.
9. Factory modules do not import evaluation ground truth.
10. Tests and CI remain green.

## Next dependency

Once this evaluation is green, implement **Issue #5 — Evidence Engine v0.1**. The Evidence Engine becomes the canonical boundary that allows validated evidence to flow into Context, Why Now, Business Problem, and eventually Opportunity without relabeling raw observations.
