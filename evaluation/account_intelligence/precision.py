"""Deterministic Account Intelligence precision evaluation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from factory.account_intelligence.domain import AccountSignal


@dataclass(frozen=True)
class SignalPrecisionResult:
    analyzed: int
    correct: int
    precision: float


def evaluate_signal_precision(
    predicted_signal_ids: Iterable[str],
    correct_signal_ids: Iterable[str],
) -> SignalPrecisionResult:
    """Measure exact-match precision against independently supplied truth."""
    predicted = tuple(dict.fromkeys(predicted_signal_ids))
    correct = set(correct_signal_ids)
    hits = sum(signal_id in correct for signal_id in predicted)
    precision = hits / len(predicted) if predicted else 0.0
    return SignalPrecisionResult(len(predicted), hits, precision)


def evaluate_observation_precision(
    predicted_signals: Sequence[AccountSignal],
    correct_observation_ids: Iterable[str],
) -> SignalPrecisionResult:
    """Evaluate predicted signals against labels attached to raw observations."""
    predicted_observations = tuple(
        dict.fromkeys(
            observation_id
            for signal in predicted_signals
            for observation_id in signal.observation_ids
        )
    )
    return evaluate_signal_precision(predicted_observations, correct_observation_ids)
