"""Bounded validation experiment planning."""

from __future__ import annotations

import hashlib

from factory.schemas.domain import Opportunity, ValidationExperiment


def _experiment_id(opportunity_id: str) -> str:
    return "exp_" + hashlib.sha256(opportunity_id.encode("utf-8")).hexdigest()[:16]


def plan_validation_experiment(
    opportunity: Opportunity,
    *,
    budget_limit: float = 0.0,
) -> ValidationExperiment:
    """Create a reversible, bounded validation plan with no external commitment."""
    if budget_limit < 0:
        raise ValueError("budget_limit must be non-negative")

    hypothesis = (
        f"The problem described by '{opportunity.title}' is sufficiently painful "
        "for the target customer to take a measurable validation action."
    )
    method = (
        "Run a low-cost customer/problem validation experiment using observable "
        "responses or behavior; do not infer willingness to pay without evidence."
    )
    return ValidationExperiment(
        id=_experiment_id(opportunity.id),
        opportunity_id=opportunity.id,
        hypothesis=hypothesis,
        method=method,
        success_metric="Predefined evidence threshold reached from target-customer responses or behavior.",
        failure_threshold="No meaningful signal after the agreed sample/timebox.",
        budget_limit=budget_limit,
        status="PLANNED",
    )
