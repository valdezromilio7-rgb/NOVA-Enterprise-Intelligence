import unittest

from factory.schemas.domain import Opportunity, OpportunityState
from factory.validation.planner import plan_validation_experiment


class ValidationPlannerTests(unittest.TestCase):
    def test_plan_is_bounded_and_reproducible(self):
        opportunity = Opportunity(
            id="opp_customer_support",
            title="Customer support delivery visibility",
            problem="Customers cannot quickly obtain order status.",
            target_customer="Customers and support teams",
            state=OpportunityState.DISCOVERY,
        )
        first = plan_validation_experiment(opportunity, budget_limit=0.0)
        second = plan_validation_experiment(opportunity, budget_limit=0.0)
        self.assertEqual(first, second)
        self.assertEqual(first.budget_limit, 0.0)
        self.assertEqual(first.status, "PLANNED")

    def test_negative_budget_is_rejected(self):
        opportunity = Opportunity(
            id="opp_test",
            title="Test",
            problem="Test",
            target_customer="Test",
        )
        with self.assertRaises(ValueError):
            plan_validation_experiment(opportunity, budget_limit=-1.0)


if __name__ == "__main__":
    unittest.main()
