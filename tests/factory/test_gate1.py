import unittest

from factory.governance.gate1 import Gate1Context, Gate1Policy, evaluate_gate1
from factory.schemas.domain import Opportunity, OpportunityScore, OpportunityState
from factory.validation.planner import plan_validation_experiment


class Gate1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.opportunity = Opportunity(
            id="opp_001",
            title="Customer support delivery visibility",
            problem="Customers cannot easily obtain reliable delivery status.",
            target_customer="Wholesale customers",
            state=OpportunityState.VALIDATION,
            evidence_ids=("ev_001", "ev_002"),
        )
        self.score = OpportunityScore(
            opportunity_id="opp_001",
            dimensions={"pain": 90.0},
            weighted_score=82.0,
            confidence=0.8,
            rationale="Strong observed pain.",
            scoring_version="score-v0.1",
        )

    def test_safe_low_cost_validation_can_auto_approve(self) -> None:
        experiment = plan_validation_experiment(self.opportunity, budget_limit=0.0)
        result = evaluate_gate1(self.opportunity, self.score, experiment)
        self.assertEqual(result.decision.outcome, "APPROVE")
        self.assertFalse(result.requires_human_approval)
        self.assertEqual(result.decision.decided_by, "NOVA_GATE1_POLICY")

    def test_insufficient_evidence_holds(self) -> None:
        opportunity = Opportunity(
            id=self.opportunity.id,
            title=self.opportunity.title,
            problem=self.opportunity.problem,
            target_customer=self.opportunity.target_customer,
        )
        experiment = plan_validation_experiment(opportunity)
        result = evaluate_gate1(opportunity, self.score, experiment)
        self.assertEqual(result.decision.outcome, "HOLD")
        self.assertIn("insufficient_evidence", result.reasons)

    def test_material_budget_requires_explicit_approval(self) -> None:
        experiment = plan_validation_experiment(self.opportunity, budget_limit=100.0)
        result = evaluate_gate1(self.opportunity, self.score, experiment)
        self.assertEqual(result.decision.outcome, "HOLD")
        self.assertTrue(result.requires_human_approval)
        self.assertIn("material_spend_requires_approval", result.reasons)

    def test_material_budget_can_be_approved_explicitly(self) -> None:
        experiment = plan_validation_experiment(self.opportunity, budget_limit=100.0)
        result = evaluate_gate1(
            self.opportunity,
            self.score,
            experiment,
            context=Gate1Context(human_approval=True),
        )
        self.assertEqual(result.decision.outcome, "APPROVE")
        self.assertEqual(result.decision.decided_by, "NOVA_CORP")

    def test_explicit_human_rejection_is_reject(self) -> None:
        experiment = plan_validation_experiment(self.opportunity, budget_limit=100.0)
        result = evaluate_gate1(
            self.opportunity,
            self.score,
            experiment,
            context=Gate1Context(human_approval=False),
        )
        self.assertEqual(result.decision.outcome, "REJECT")
        self.assertIn("explicit_human_rejection", result.reasons)

    def test_elevated_risk_holds_without_approval(self) -> None:
        experiment = plan_validation_experiment(self.opportunity)
        result = evaluate_gate1(
            self.opportunity,
            self.score,
            experiment,
            context=Gate1Context(risk_score=80.0),
        )
        self.assertEqual(result.decision.outcome, "HOLD")
        self.assertIn("elevated_risk_requires_approval", result.reasons)

    def test_sensitive_data_requires_approval(self) -> None:
        experiment = plan_validation_experiment(self.opportunity)
        result = evaluate_gate1(
            self.opportunity,
            self.score,
            experiment,
            context=Gate1Context(sensitive_data=True),
        )
        self.assertEqual(result.decision.outcome, "HOLD")
        self.assertIn("sensitive_data_requires_approval", result.reasons)

    def test_external_commitment_requires_approval(self) -> None:
        experiment = plan_validation_experiment(self.opportunity)
        result = evaluate_gate1(
            self.opportunity,
            self.score,
            experiment,
            context=Gate1Context(external_commitment=True),
        )
        self.assertEqual(result.decision.outcome, "HOLD")
        self.assertIn("external_commitment_requires_approval", result.reasons)

    def test_evidence_ids_are_preserved(self) -> None:
        experiment = plan_validation_experiment(self.opportunity)
        result = evaluate_gate1(self.opportunity, self.score, experiment)
        self.assertEqual(result.decision.evidence_ids, self.opportunity.evidence_ids)

    def test_evaluation_is_deterministic(self) -> None:
        experiment = plan_validation_experiment(self.opportunity, budget_limit=10.0)
        policy = Gate1Policy(maximum_auto_budget=0.0)
        first = evaluate_gate1(self.opportunity, self.score, experiment, policy=policy)
        second = evaluate_gate1(self.opportunity, self.score, experiment, policy=policy)
        self.assertEqual(first, second)

    def test_score_threshold_is_configurable(self) -> None:
        experiment = plan_validation_experiment(self.opportunity)
        policy = Gate1Policy(minimum_score=90.0)
        result = evaluate_gate1(self.opportunity, self.score, experiment, policy=policy)
        self.assertEqual(result.decision.outcome, "HOLD")
        self.assertIn("score_below_minimum", result.reasons)


if __name__ == "__main__":
    unittest.main()
