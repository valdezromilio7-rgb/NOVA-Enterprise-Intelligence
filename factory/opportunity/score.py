"""Transparent opportunity scoring.

Scores are intentionally deterministic and inspectable. The factory may later
replace individual dimensions with learned models, but the contract remains
stable and every score retains its version and rationale.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from factory.schemas.domain import Opportunity, OpportunityScore

DEFAULT_WEIGHTS: Mapping[str, float] = {
    "pain": 0.18,
    "frequency": 0.10,
    "willingness_to_pay": 0.15,
    "market_potential": 0.12,
    "competition": 0.07,
    "build_complexity": 0.10,
    "distribution": 0.08,
    "ai_leverage": 0.08,
    "strategic_fit": 0.07,
    "risk": 0.05,
}


@dataclass(frozen=True)
class ScoringResult:
    score: OpportunityScore


def score_opportunity(
    opportunity: Opportunity,
    dimensions: Mapping[str, float],
    *,
    weights: Mapping[str, float] = DEFAULT_WEIGHTS,
    confidence: float = 0.0,
    version: str = "v0.1",
) -> ScoringResult:
    """Return an auditable 0-100 weighted score.

    Inputs use a 0-100 scale. Missing dimensions are rejected rather than
    silently imputed because hidden assumptions would make rankings unsafe.
    """
    missing = [name for name in weights if name not in dimensions]
    if missing:
        raise ValueError(f"missing scoring dimensions: {', '.join(missing)}")
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("scoring weights must sum to 1.0")
    if any(not 0.0 <= value <= 100.0 for value in dimensions.values()):
        raise ValueError("all scoring dimensions must be between 0 and 100")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")

    weighted = sum(dimensions[k] * weights[k] for k in weights)
    rationale = "; ".join(
        f"{key}={dimensions[key]:.1f} x {weights[key]:.2f}" for key in weights
    )
    return ScoringResult(
        OpportunityScore(
            opportunity_id=opportunity.id,
            dimensions=dict(dimensions),
            weighted_score=round(weighted, 4),
            confidence=confidence,
            rationale=rationale,
            scoring_version=version,
        )
    )
