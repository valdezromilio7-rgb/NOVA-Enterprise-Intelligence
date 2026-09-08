"""Deterministic, auditable Account Intelligence signal scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from factory.account_intelligence.domain import AccountSignal


SIGNAL_SCORE_MAX = {
    "relevance": 25,
    "recency": 20,
    "intensity": 20,
    "icp_fit": 20,
    "evidence": 10,
    "verifiability": 5,
}


@dataclass(frozen=True)
class SignalScore:
    signal_id: str
    dimensions: Mapping[str, float]
    total_score: float
    confidence: float
    rationale: str
    scoring_version: str = "signal-scoring-v0.1"

    def __post_init__(self) -> None:
        if not 0.0 <= self.total_score <= 100.0:
            raise ValueError("total_score must be between 0 and 100")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


def score_signal(
    signal: AccountSignal,
    dimensions: Mapping[str, float],
) -> SignalScore:
    """Score one signal from externally supplied, auditable dimensions.

    This v0.1 contract intentionally does not infer dimensions with an LLM.
    """
    expected = set(SIGNAL_SCORE_MAX)
    if set(dimensions) != expected:
        raise ValueError("dimensions must contain exactly the six signal score dimensions")

    for name, maximum in SIGNAL_SCORE_MAX.items():
        value = float(dimensions[name])
        if not 0.0 <= value <= maximum:
            raise ValueError(f"{name} must be between 0 and {maximum}")

    total = sum(float(dimensions[name]) for name in SIGNAL_SCORE_MAX)
    rationale = "; ".join(
        f"{name}={float(dimensions[name]):g}/{maximum:g}"
        for name, maximum in SIGNAL_SCORE_MAX.items()
    )
    return SignalScore(
        signal_id=signal.id,
        dimensions=dict(dimensions),
        total_score=total,
        confidence=signal.confidence,
        rationale=rationale,
    )


def rank_signal_scores(scores: Sequence[SignalScore]) -> tuple[SignalScore, ...]:
    """Return deterministic ranking: score descending, then signal ID."""
    return tuple(sorted(scores, key=lambda item: (-item.total_score, item.signal_id)))
