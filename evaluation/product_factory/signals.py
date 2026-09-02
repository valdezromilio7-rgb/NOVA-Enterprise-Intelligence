"""Public benchmark signals; hidden ground truth lives in a separate module."""

from factory.schemas.domain import Signal


BENCHMARK_SIGNALS = (
    Signal("raw-1", "CRM", "2026-01-03", "customer support", "Customers repeatedly wait days for answers about order status and delivery dates.", "synthetic:crm:001"),
    Signal("raw-2", "CRM", "2026-01-10", "delivery visibility", "Support staff manually check several systems before telling customers where an order is.", "synthetic:crm:002"),
    Signal("raw-3", "SALES", "2026-01-15", "inventory availability", "Sales representatives lose deals because current stock information is not available quickly.", "synthetic:sales:003"),
    Signal("raw-4", "OPS", "2026-01-18", "supplier delays", "Late supplier deliveries create recurring stockouts on high-demand products.", "synthetic:ops:004"),
    Signal("raw-5", "FINANCE", "2026-01-21", "invoice processing", "Employees spend substantial time reconciling invoices that arrive with inconsistent references.", "synthetic:finance:005"),
    Signal("raw-6", "CRM", "2026-01-25", "customer support", "Customers contact support again when delivery information is unavailable after purchase.", "synthetic:crm:006"),
)
