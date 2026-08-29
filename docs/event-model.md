# Hidden Event Model — V0.1

The first simulation contains five hidden events. Ground truth is maintained separately from the data exposed to NOVA.

## E01 — Cost Drift

A supplier progressively increases the cost of selected products. Expected signal: rising COGS and deteriorating product/customer margins.

## E02 — Discount Drift

A salesperson progressively increases discounts on selected sales. Expected signal: stable or growing revenue accompanied by declining realized margin.

## E03 — Inventory Accumulation

A product category experiences sustained overstock relative to demand. Expected signal: increasing days of inventory and capital immobilization.

## E04 — Collection Deterioration

A selected customer cohort progressively pays later. Expected signal: worsening receivables aging and cash conversion.

## E05 — Hidden Best Practice

A salesperson develops a repeatable product/customer mix that produces superior economics. Expected signal: a positive performance pattern that could potentially be replicated.

## Event requirements

Each event must:

- begin subtly;
- evolve over time;
- affect valid business transactions;
- have measurable economic impact;
- have identifiable affected entities;
- remain unknown to NOVA during discovery;
- be recorded in `ground_truth/events.json` for evaluation.

## Difficulty

V0 intentionally uses five events. Later versions will add compound events, interacting causes, external shocks, and multi-domain causal chains.
