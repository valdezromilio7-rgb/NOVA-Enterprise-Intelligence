# NOVA Opportunity Engine — Specification v0.1

**Status:** Proposed / Foundational
**Authority:** NOVA CORP

## 1. Purpose

Turn noisy market and operational signals into ranked, evidence-backed opportunities without confusing observations with assumptions.

## 2. Canonical entities

### Signal

A raw observation from a source.

Required fields:

- `signal_id`
- `source`
- `captured_at`
- `source_reference`
- `raw_claim`
- `source_type`
- `reliability_class`
- `region`
- `industry`
- `customer_segment`

### Evidence

A normalized claim supported by one or more signals.

Required fields:

- `evidence_id`
- `claim`
- `supporting_signal_ids`
- `evidence_type`
- `confidence`
- `observed_at`
- `provenance`

### Opportunity

A candidate problem/value-creation space derived from evidence.

Required fields:

- `opportunity_id`
- `title`
- `problem_statement`
- `target_segment`
- `geography`
- `evidence_ids`
- `assumptions`
- `score_version`
- `score`
- `status`
- `created_at`

## 3. Source classes

Initial source classes:

- direct customer evidence;
- public market data;
- competitor/product evidence;
- search/demand signals;
- community discussion;
- internal portfolio data;
- experimental/simulated data.

Source class must never be hidden. Simulated evidence must not be represented as real-market evidence.

## 4. Evidence discipline

Every material claim must be classified as one of:

- **Observed:** directly supported by a source.
- **Derived:** logically calculated from observed evidence.
- **Inferred:** plausible interpretation requiring uncertainty.
- **Assumed:** currently unverified.

The engine must preserve this distinction in all downstream artifacts.

## 5. Opportunity formation

```text
RAW SIGNALS
   -> NORMALIZE
   -> DEDUPLICATE
   -> CLUSTER
   -> EXTRACT PAINS
   -> ATTACH EVIDENCE
   -> IDENTIFY ASSUMPTIONS
   -> FORM OPPORTUNITY
```

An opportunity should represent a recurring or economically meaningful problem, not merely a product idea.

## 6. Initial scoring model

Score dimensions, each normalized to 0–10:

| Dimension | Initial weight |
|---|---:|
| Pain severity | 15% |
| Frequency/recurrence | 10% |
| Willingness to pay | 15% |
| Market potential | 10% |
| Distribution potential | 10% |
| AI leverage | 10% |
| Strategic fit | 10% |
| Competition intensity | 5% |
| Build complexity | 5% |
| Risk | 10% |

The weighted score is a decision aid, not a truth claim. Weights are versioned and may change after validation evidence.

## 7. Uncertainty adjustment

The raw score must be accompanied by evidence confidence and uncertainty.

A high score with weak evidence must not outrank a slightly lower score with materially stronger evidence without making the difference explicit.

The system must store:

- raw weighted score;
- evidence confidence;
- uncertainty flags;
- missing evidence;
- scoring version.

## 8. Ranking output

Each ranked opportunity must answer:

1. What painful problem appears to exist?
2. Who experiences it?
3. What evidence supports it?
4. What is still assumed?
5. Why could someone pay to solve it?
6. Why now?
7. What could make the opportunity fail?
8. What is the cheapest useful validation experiment?

## 9. Anti-bias rules

The engine must not:

- promote an opportunity solely because it is technically interesting;
- treat social engagement as equivalent to willingness to pay;
- treat AI novelty as customer demand;
- fabricate market size;
- convert an assumption into evidence through repetition;
- hide contradictory evidence.

## 10. Output artifacts

For each opportunity:

- normalized opportunity record;
- evidence ledger;
- assumption ledger;
- score breakdown;
- confidence/uncertainty report;
- validation recommendation;
- provenance manifest.

## 11. v0.1 evaluation

Use controlled synthetic opportunities and known ground truth to test whether the engine:

- ranks deliberately seeded high-value opportunities above distractors;
- preserves provenance;
- detects missing evidence;
- does not leak ground truth into discovery;
- produces reproducible rankings for the same input and configuration.
