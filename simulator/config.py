from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SimulationConfig:
    seed: int = 2026001
    start_date: date = date(2026, 1, 1)
    days: int = 90
    employees: int = 30
    customers: int = 100
    suppliers: int = 20
    products: int = 200
    initial_cash: int = 2_000_000_000
    currency: str = "PYG"
