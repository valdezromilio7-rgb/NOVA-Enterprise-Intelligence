"""Deterministic bridge from Account Intelligence business problems to Opportunity."""

from __future__ import annotations

from typing import Sequence

from factory.account_intelligence.business_problem import BusinessProblem
from factory.schemas.domain import Opportunity


def business_problem_to_opportunity(
    problem: BusinessProblem,
    *,
    target_customer: str,
    evidence_ids: Sequence[str] = (),
) -> Opportunity:
    """Translate a business problem while preserving canonical Evidence IDs."""
    if not target_customer.strip():
        raise ValueError("target_customer must not be empty")

    normalized_evidence_ids = tuple(
        sorted(
            set(
                evidence_id.strip()
                for evidence_id in evidence_ids
                if evidence_id.strip()
            )
        )
    )

    return Opportunity(
        id=f"opp-{problem.id}",
        title=problem.problem_statement,
        problem=problem.problem_statement,
        target_customer=target_customer,
        evidence_ids=normalized_evidence_ids,
        assumptions=[
            "business problem translated from explicit account context and Why Now"
        ],
        metadata={
            "account_id": problem.account_id,
            "signal_id": problem.signal_id,
            "business_problem_id": problem.id,
            "context_version": problem.context_version,
            "why_now_version": problem.why_now_version,
            "evidence_refs": ",".join(normalized_evidence_ids),
            "current_solution": problem.current_solution,
            "gap": problem.gap,
            "desired_outcome": problem.desired_outcome,
            "translation_version": "business-problem-opportunity-v0.1",
        },
    )
