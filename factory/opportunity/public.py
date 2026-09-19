"""Canonical bridge from a Business Problem to an Opportunity."""

from __future__ import annotations

from hashlib import sha256

from factory.schemas.domain import BusinessProblem, Opportunity, OpportunityState


def build_opportunity(
    *,
    problem: BusinessProblem,
    title: str,
    target_customer: str,
    assumptions: tuple[str, ...] = (),
) -> Opportunity:
    """Translate an explicit Business Problem into a discovery Opportunity.

    This bridge does not infer demand, willingness to pay, score, or validation.
    Those remain downstream Product Factory responsibilities.
    """
    if not title.strip() or not target_customer.strip():
        raise ValueError("title and target_customer must be non-empty")
    opportunity_id = "opp_" + sha256(
        f"{problem.id}|{title.strip()}|{target_customer.strip()}".encode("utf-8")
    ).hexdigest()[:24]
    return Opportunity(
        id=opportunity_id,
        title=title.strip(),
        problem=problem.problem_statement,
        target_customer=target_customer.strip(),
        state=OpportunityState.DISCOVERY,
        account_id=problem.account_id,
        business_problem_id=problem.id,
        evidence_ids=tuple(problem.evidence_refs),
        assumptions=tuple(a.strip() for a in assumptions if a.strip()),
        metadata={
            "signal_id": problem.signal_id,
            "context_id": problem.context_id,
            "why_now_id": problem.why_now_id,
            "lineage_version": "public-business-problem-opportunity-v0.1",
        },
    )
