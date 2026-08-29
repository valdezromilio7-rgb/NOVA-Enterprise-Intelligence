import random
from typing import List, Tuple

from .config import SimulationConfig
from .models import Company, Customer, Employee, Product, Supplier


INDUSTRIES = ["CONSTRUCTION", "MANUFACTURING", "RETAIL", "SERVICES", "AGRICULTURE"]
CATEGORIES = ["ELECTRICAL", "HARDWARE", "TOOLS", "SAFETY", "CONSTRUCTION", "CONSUMABLES"]
SEGMENTS = ["SMALL", "MEDIUM", "ENTERPRISE"]


def build_master_data(config: SimulationConfig) -> Tuple[Company, List[Employee], List[Customer], List[Supplier], List[Product]]:
    rng = random.Random(config.seed)

    company = Company(
        company_id="NID-001",
        name="NOVA Industrial Distribution S.A.",
        country="PY",
        currency=config.currency,
        start_date=config.start_date,
        simulation_seed=config.seed,
    )

    employees = []
    departments = ["SALES", "FINANCE", "OPERATIONS", "PURCHASING", "WAREHOUSE", "ADMINISTRATION"]
    for i in range(1, config.employees + 1):
        department = "SALES" if i <= 10 else departments[rng.randrange(len(departments))]
        employees.append(Employee(
            employee_id=f"EMP-{i:03d}",
            department=department,
            role="SALES_REP" if department == "SALES" else "SPECIALIST",
            salary=rng.randint(4_000_000, 10_000_000),
            performance_profile=rng.choice(["LOW", "NORMAL", "HIGH"]),
        ))

    suppliers = []
    for i in range(1, config.suppliers + 1):
        suppliers.append(Supplier(
            supplier_id=f"SUP-{i:03d}",
            category=CATEGORIES[(i - 1) % len(CATEGORIES)],
            payment_terms=rng.choice([15, 30, 45, 60]),
            lead_time=rng.randint(3, 14),
            reliability=round(rng.uniform(0.90, 0.99), 4),
            minimum_order_quantity=rng.randint(5, 50),
        ))

    customers = []
    for i in range(1, config.customers + 1):
        segment = rng.choices(SEGMENTS, weights=[70, 25, 5])[0]
        credit_limit = {"SMALL": 30_000_000, "MEDIUM": 100_000_000, "ENTERPRISE": 300_000_000}[segment]
        customers.append(Customer(
            customer_id=f"CUST-{i:03d}",
            segment=segment,
            industry=rng.choice(INDUSTRIES),
            credit_limit=credit_limit,
            payment_terms=rng.choice([0, 15, 30, 45, 60]),
            demand_profile=rng.choice(["RECURRING", "SEASONAL", "IRREGULAR", "GROWING"]),
            risk_profile=rng.choice(["LOW", "LOW", "NORMAL", "HIGH"]),
        ))

    products = []
    for i in range(1, config.products + 1):
        category = CATEGORIES[(i - 1) % len(CATEGORIES)]
        supplier = suppliers[(i - 1) % len(suppliers)]
        cost = rng.randint(50_000, 2_000_000)
        markup = rng.uniform(1.15, 1.55)
        price = max(cost + 1, int(cost * markup))
        stock_min = rng.randint(5, 30)
        stock_max = stock_min + rng.randint(20, 100)
        products.append(Product(
            product_id=f"SKU-{i:04d}",
            category=category,
            supplier_id=supplier.supplier_id,
            cost=cost,
            price=price,
            stock_min=stock_min,
            stock_max=stock_max,
            demand_profile=rng.choice(["FAST", "NORMAL", "SLOW", "DEAD"]),
        ))

    return company, employees, customers, suppliers, products
