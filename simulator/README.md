# Simulator

V0.1 generates a deterministic synthetic wholesale-distribution company.

## Design rules

- Use explicit assumptions rather than hidden formulas.
- Keep operational events traceable.
- Keep accounting flows separate from management KPIs.
- Never use ground-truth events as input to NOVA.
- Prefer established accounting/control concepts over invented business rules.

Implementation will proceed in small, testable modules:

1. master-data generation;
2. daily demand;
3. sales and revenue events;
4. inventory and weighted-average cost;
5. receivables and collections;
6. purchases and payables;
7. operating expenses;
8. daily control checks;
9. hidden-event scenarios;
10. dataset export.
