from .accounting import cash_balance, inventory_balance, sale_amount
from .config import SimulationConfig
from .controls import require_equal, require_non_negative
from .master_data import build_master_data


def run_smoke_test() -> None:
    """Validate the deterministic master-data and accounting primitives."""
    config = SimulationConfig()
    company, employees, customers, suppliers, products = build_master_data(config)

    assert company.simulation_seed == config.seed
    assert len(employees) == config.employees
    assert len(customers) == config.customers
    assert len(suppliers) == config.suppliers
    assert len(products) == config.products

    gross = 10 * products[0].price
    net = sale_amount(10, products[0].price, 0)
    require_equal(gross, net, "sale amount without discount")

    stock = inventory_balance(100, 50, 5, 30, 2, 0)
    require_equal(123, stock, "inventory invariant")
    require_non_negative(stock, "inventory")

    cash = cash_balance(1_000, 500, 200, 100)
    require_equal(1_200, cash, "cash invariant")

    print("NOVA Enterprise Intelligence V0.1 smoke test: PASS")
    print(f"company={company.company_id} seed={company.simulation_seed}")
    print(f"employees={len(employees)} customers={len(customers)} suppliers={len(suppliers)} products={len(products)}")


if __name__ == "__main__":
    run_smoke_test()
