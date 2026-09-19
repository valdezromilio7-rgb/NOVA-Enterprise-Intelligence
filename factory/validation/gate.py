"""Deterministic pre-experiment validation gate."""

from __future__ import annotations
from factory.schemas.domain import Opportunity, OpportunityScore

def authorize_validation(*, opportunity: Opportunity, score: OpportunityScore, minimum_confidence: float = 0.5) -> None:
    """Authorize validation only; never product build, spend, deployment, or scaling."""
    if opportunity.state.value not in {"discovery", "validation"}:
        raise ValueError("opportunity must be in discovery or validation state")
    if not opportunity.evidence_ids:
        raise ValueError("validation requires canonical evidence IDs")
    if score.opportunity_id != opportunity.id:
        raise ValueError("score opportunity_id does not match opportunity")
    if not 0.0 <= minimum_confidence <= 1.0:
        raise ValueError("minimum_confidence must be between 0 and 1")
    if score.confidence < minimum_confidence:
        raise ValueError("validation requires sufficient scoring confidence")
