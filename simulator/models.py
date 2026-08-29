from dataclasses import dataclass
from datetime import date


@dataclass
class Company:
    company_id: str
    name: str
    country: str
    currency: str
    start_date: date
    simulation_seed: int


@dataclass
class Employee:
    employee_id: str
    department: str
    role: str
    salary: int
    performance_profile: str


@dataclass
class Customer:
    customer_id: str
    segment: str
    industry: str
    credit_limit: int
    payment_terms: int
    demand_profile: str
    risk_profile: str


@dataclass
class Supplier:
    supplier_id: str
    category: str
    payment_terms: int
    lead_time: int
    reliability: float
    minimum_order_quantity: int


@dataclass
class Product:
    product_id: str
    category: str
    supplier_id: str
    cost: int
    price: int
    stock_min: int
    stock_max: int
    demand_profile: str
