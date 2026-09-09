"""Deterministic bridge from a business problem to an opportunity with canonical evidence."""

from __future__ import annotations

from factory.account_intelligence.business_problem import BusinessProblem
from factory.schemas.domain import Opportunity


def business_problem_to_opportunity_with_evidence(
    problem: BusinessProblem,
    *,
    target_customer: str,
    evidence_ids: tuple[str, ...],
) -> Opportunity:
    """Translate a business problem while preserving canonical Evidence IDs."""
    if not target_customer.strip():
        raise ValueError("target_customer must not be empty")
    normalized_evidence_ids = tuple(sorted(set(evidence_ids)))
    if not normalized_evidence_ids:
        raise ValueError("evidence_ids must not be empty")
    return Opportunity(
        id=f"opp-{problem.id}",
        title=problem.problem_statement,
        problem=problem.problem_statement,
        target_customer=target_customer,
        evidence_ids=normalized_evidence_ids,
        assumptions=(
            "business problem translated from explicit account context and Why Now",
        ),
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
            "translation_version": "business-problem-opportunity-evidence-v0.1",
        },
    )
