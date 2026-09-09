"""Deterministic bridge from Account Intelligence business problems to Opportunity."""

from __future__ import annotations

from factory.account_intelligence.business_problem import BusinessProblem
from factory.schemas.domain import Opportunity


def business_problem_to_opportunity(
    problem: BusinessProblem,
    *,
    target_customer: str,
) -> Opportunity:
    """Translate a verified business problem into the canonical Opportunity contract.

    Observation references remain metadata until the Evidence Engine creates
    canonical Evidence records; this bridge never relabels observations as evidence.
    """
    if not target_customer.strip():
        raise ValueError("target_customer must not be empty")
    return Opportunity(
        id=f"opp-{problem.id}",
        title=problem.problem_statement,
        problem=problem.problem_statement,
        target_customer=target_customer,
        evidence_ids=[],
        assumptions=[
            "business problem translated from explicit account context and Why Now"
        ],
        metadata={
            "account_id": problem.account_id,
            "signal_id": problem.signal_id,
            "business_problem_id": problem.id,
            "context_version": problem.context_version,
            "why_now_version": problem.why_now_version,
            "evidence_refs": ",".join(problem.evidence_refs),
            "current_solution": problem.current_solution,
            "gap": problem.gap,
            "desired_outcome": problem.desired_outcome,
            "translation_version": "business-problem-opportunity-v0.1",
        },
    )
