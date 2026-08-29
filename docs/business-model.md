# Business Model — V0.1

## Company

**NOVA Industrial Distribution S.A.** is a fictional Paraguayan B2B wholesale distributor used as a controlled enterprise laboratory.

## Operating model

The company purchases industrial products from suppliers, holds inventory, sells to business customers, delivers orders, invoices customers, collects receivables, pays suppliers and operating expenses, and manages working capital.

## Organizational scope

- 1 branch
- 30 employees
- 100 customers
- 20 suppliers
- 200 SKUs
- 90 simulated days

## Purpose of the simulation

The company must behave like a plausible operating business rather than a static dataset. Revenue, costs, inventory, receivables, cash, supplier behavior, customer behavior, and operating expenses must interact causally.

## Economic relationships

```text
Demand → Sales → Inventory → Receivables → Collections → Cash
Demand → Replenishment → Purchases → Inventory → Accounts Payable → Cash
Sales + COGS → Gross Profit
Gross Profit − Operating Expenses → Operating Result
``` 

## Management objective

Maximize sustainable economic value while maintaining adequate liquidity, service levels, inventory health, customer relationships, and supplier resilience.

## Simulation principle

Normal business variability must be distinguishable from meaningful deterioration, risk, leakage, and opportunity. Hidden events are introduced as changes in business behavior, not arbitrary corrupted records.
