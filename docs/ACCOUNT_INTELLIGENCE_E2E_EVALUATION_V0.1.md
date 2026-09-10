# NOVA Account Intelligence — E2E Evaluation v0.1

## Purpose

Prove that the Account Intelligence foundation can execute one reproducible chain from raw observations to a canonical Opportunity without bypassing evidence or governance boundaries.

## Evaluation chain

`RAW OBSERVATIONS → SIGNAL EXTRACTION → SIGNAL SCORING → TOP-N → PRECISION → EVIDENCE → CONTEXT → WHY NOW → BUSINESS PROBLEM → OPPORTUNITY`

## Baseline

- 100 deterministic synthetic accounts.
- 32 candidate signals extracted by the baseline rule set.
- Top 20 signals ranked deterministically.
- Precision evaluated against independently maintained synthetic labels.
- The factory domain does not import evaluation ground truth.
- The first ranked signal is transformed through canonical Evidence, Context, Why Now, Business Problem, and Opportunity contracts.
- Repeated executions must produce identical result objects.

## Evidence boundary

`SourceObservation` is raw source material. The E2E harness creates one canonical `Evidence` record from the selected observation and propagates its Evidence ID downstream.

The distinction is mandatory:

`Observation ≠ Evidence ≠ Signal ≠ Opportunity`

`Opportunity.evidence_ids` contains canonical Evidence IDs only; raw observation IDs are never relabeled as evidence.

The selected evidence remains `UNVERIFIED` in v0.1. Consequently, the E2E `Why Now` assessment is explicitly non-verifiable until a later evaluated verification capability establishes stronger support.

## Governance boundary

This harness is an evaluation artifact, not a production autonomous decision-maker. It does not call external providers, send outbound messages, spend money, alter production systems, or authorize execution.

The synthetic precision result is a regression benchmark only. It must not be represented as real-world market or signal performance.

## Acceptance criteria

1. 100 accounts are analyzed.
2. 32 candidate signals are extracted.
3. Top 20 are ranked and independently evaluated.
4. The baseline reaches 20/20 precision on this synthetic fixture.
5. At least one signal completes the Evidence → Context → Why Now → Business Problem → Opportunity chain.
6. Provenance and canonical Evidence linkage remain traceable.
7. Opportunity `evidence_ids` contains canonical Evidence IDs only.
8. Repeated runs are identical.
9. Factory modules do not import evaluation ground truth.
10. Tests and CI remain green.

## Implementation status

The E2E path now uses the single canonical Evidence contract in `factory.schemas.domain` and the existing business-problem opportunity bridge with explicit Evidence ID propagation.
