from dataclasses import dataclass


@dataclass
class LedgerState:
    cash: int
    accounts_receivable: int = 0
    accounts_payable: int = 0
    inventory_value: int = 0
    revenue: int = 0
    cogs: int = 0
    operating_expenses: int = 0

    @property
    def gross_profit(self) -> int:
        return self.revenue - self.cogs

    @property
    def operating_result(self) -> int:
        return self.gross_profit - self.operating_expenses


def sale_amount(quantity: int, unit_price: int, discount: int) -> int:
    gross = quantity * unit_price
    if discount < 0 or discount > gross:
        raise ValueError("discount must be between 0 and gross sale amount")
    return gross - discount


def inventory_balance(opening: int, purchases: int, returns: int, sales: int, damage: int, adjustments: int) -> int:
    return opening + purchases + returns - sales - damage + adjustments


def cash_balance(opening: int, collections: int, supplier_payments: int, expenses: int, capex: int = 0) -> int:
    return opening + collections - supplier_payments - expenses - capex
