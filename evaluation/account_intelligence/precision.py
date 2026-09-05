"""Deterministic Signal Precision evaluation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


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
    return SignalPrecisionResult(
        analyzed=len(predicted),
        correct=hits,
        precision=precision,
    )
