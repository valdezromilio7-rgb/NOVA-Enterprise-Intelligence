# Simulation Engine — V0.1

## Simulation parameters

```text
seed: NOVA-V0-001
date_start: 2026-01-01
days: 90
branch_count: 1
employees: 30
customers: 100
suppliers: 20
products: 200
```

## Daily cycle

For each simulated day:

1. Generate external conditions.
2. Generate customer demand.
3. Generate sales subject to price, demand, credit and inventory.
4. Generate replenishment requirements.
5. Generate supplier deliveries and cost behavior.
6. Apply inventory movements.
7. Generate customer collections.
8. Generate supplier payments.
9. Generate operating expenses.
10. Update financial state.
11. Record all material events.
12. Run daily integrity checks.

## Demand model

A customer's baseline demand is modified by:

`Demand = BaseDemand × Seasonality × GrowthFactor × MarketFactor × RandomNoise`

Randomness must be deterministic for a given seed.

## Normal variability

The simulation must contain realistic variation in demand, payment timing, delivery timing, sales mix and operating costs. Variability must not automatically represent a problem.

## Hidden-event principle

Hidden events alter the underlying business behavior gradually. They must not be implemented as obviously malformed records. The resulting data should remain valid and internally consistent.

## Reproducibility

The same seed and configuration must generate the same dataset. Different seeds should produce different but plausible enterprises.

## Integrity rule

A simulation run is valid only when all accounting and inventory identities reconcile within the defined numerical tolerance.
