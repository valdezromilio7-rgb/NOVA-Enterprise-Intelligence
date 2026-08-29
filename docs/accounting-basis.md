# Accounting & Control Basis — V0.1

This simulator does not invent accounting principles. Its baseline is aligned to established financial reporting and risk-management frameworks, adapted only where necessary for a synthetic enterprise experiment.

## Reference basis

- **IAS 2 Inventories:** inventory cost, cost formulas, recognition of inventory expense when sold, and write-down concepts. For interchangeable inventory V0.1 uses weighted-average cost. The simulator does not claim IFRS compliance; it implements a controlled subset for experimentation.
- **IFRS 15 Revenue:** revenue events are modeled around transfer of control of goods and consideration expected from the customer. V0.1 is a simple point-in-time wholesale-sale model; it does not model complex contracts or multiple performance obligations.
- **IFRS 9:** customer credit risk is represented separately from simple payment timing. Future versions can implement expected-credit-loss methodology. V0.1 must not label its simplified bad-debt estimate as an IFRS 9 ECL calculation.
- **COSO ERM:** risk discovery is organized around identifying, assessing, prioritizing, responding to, and reporting enterprise risks. The simulator is not a COSO implementation or certification.

## Control principles

1. Every material transaction has an identifiable source event.
2. Inventory movements reconcile to stock balances.
3. Credit sales create receivables; collections reduce receivables.
4. Purchases create supplier obligations; supplier payments reduce them.
5. Revenue, cost of sales, inventory and cash are modeled as separate economic flows.
6. Management metrics are derived from transaction data rather than independently fabricated.
7. Ground truth is isolated from NOVA's observation pipeline.
8. Any assumption not directly supported by a cited standard is explicitly marked as a simulation assumption.

## Scope boundary

V0.1 is a research simulator, not accounting software, tax software, audit software, or a regulatory reporting system. Paraguay-specific tax and statutory accounting rules will be added only after researching the applicable official Paraguayan sources.
