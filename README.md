# NOVA Enterprise Intelligence

AI-powered enterprise intelligence platform and simulation laboratory for discovering hidden risks, inefficiencies, opportunities, and economic value across business operations.

## V0.1 — Enterprise Simulation Laboratory

The first milestone is a reproducible 90-day virtual enterprise designed to validate whether NOVA can discover economically meaningful signals without being told what to look for.

### Initial scope

- 1 company
- 1 branch
- 30 employees
- 100 customers
- 20 suppliers
- 200 products
- 90 simulated days
- 5 hidden business events
- deterministic, seed-based simulation
- automated financial and operational integrity checks

### Core principle

The simulator creates the **reality**. NOVA observes the reality. A separate **ground truth** layer records what actually happened and is never exposed to NOVA during discovery experiments.

```text
REALITY → DATA → NOVA DISCOVERY → EVALUATION
             ↑                         ↑
          Simulator              Ground Truth
```

## Repository structure

```text
nova-enterprise-intelligence/
├── docs/
├── simulator/
├── data/
├── ground_truth/
├── nova/
└── evaluation/
```

## Development principle

We validate the intelligence system experimentally before scaling the simulation or building a commercial product. Every experiment must be reproducible, measurable, and traceable.
