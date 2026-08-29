# Data Model — V0.1

## Master entities

### company
- company_id
- name
- country
- currency
- start_date
- simulation_seed

### employees
- employee_id
- department
- role
- salary
- hire_date
- performance_profile

### customers
- customer_id
- segment
- location
- industry
- credit_limit
- payment_terms
- demand_profile
- risk_profile

### suppliers
- supplier_id
- category
- payment_terms
- lead_time
- reliability
- price_profile
- risk_profile
- minimum_order_quantity

### products
- product_id
- category
- supplier_id
- cost
- price
- target_margin
- stock_min
- stock_max
- demand_profile

## Transaction entities

### sales
- sale_id
- date
- customer_id
- employee_id
- product_id
- quantity
- unit_price
- discount
- gross_amount
- net_amount
- payment_terms

### purchases
- purchase_id
- date
- supplier_id
- product_id
- quantity
- unit_cost
- total_cost
- expected_delivery
- actual_delivery

### inventory
- inventory_id
- date
- product_id
- movement_type
- quantity
- reference_id

### payments
- payment_id
- date
- entity_type
- entity_id
- invoice_id
- amount
- payment_type

### expenses
- expense_id
- date
- category
- supplier
- amount
- department
- recurring

## Event log

Every material business action should be traceable through `event_log`:

- timestamp
- event_id
- event_type
- entity_type
- entity_id
- actor_id
- value
- metadata

## Accounting identities

### Inventory

`Opening Stock + Purchases + Returns − Sales − Damage ± Adjustments = Closing Stock`

### Cash

`Opening Cash + Collections − Supplier Payments − Expenses − CAPEX = Closing Cash`

### Sales

`Quantity × Unit Price − Discount = Net Sales`

### Accounts receivable

`Opening AR + Credit Sales − Collections − Credits = Closing AR`

These identities are invariant checks for the simulator.
