"""Reproducible Account Intelligence benchmark harness."""

from __future__ import annotations

from dataclasses import dataclass

from evaluation.account_intelligence.dataset import AccountIntelligenceFixture, build_fixture
from evaluation.account_intelligence.ground_truth import EXPECTED_SIGNAL_OBSERVATION_IDS
from evaluation.account_intelligence.precision import SignalPrecisionResult, evaluate_observation_precision
from factory.account_intelligence.domain import AccountSignal
from factory.account_intelligence.score import SignalScore, rank_signal_scores, score_signal
from factory.account_intelligence.signal_engine import SignalRule, extract_signals


BASELINE_RULES = (
    SignalRule(
        rule_id="delivery-demand-v0.1",
        signal_type="customer_pain",
        title="Repeated delivery-status support demand",
        trigger_terms=("customer support", "delivery-status"),
        confidence=0.8,
    ),
)


@dataclass(frozen=True)
class AccountIntelligenceBenchmarkResult:
    analyzed_accounts: int
    extracted_signals: int
    ranked_top_signals: tuple[SignalScore, ...]
    precision: SignalPrecisionResult


def _observable_dimensions(content: str) -> dict[str, float]:
    """Return baseline dimensions from observable wording, not hidden labels."""
    repeated = "repeated" in content.casefold()
    return {
        "relevance": 24 if repeated else 15,
        "recency": 18,
        "intensity": 17 if repeated else 7,
        "icp_fit": 18,
        "evidence": 8 if repeated else 5,
        "verifiability": 5,
    }


def run_baseline_benchmark(
    fixture: AccountIntelligenceFixture | None = None,
    top_n: int = 20,
) -> AccountIntelligenceBenchmarkResult:
    """Run the full synthetic baseline without exposing labels to factory code."""
    if top_n <= 0:
        raise ValueError("top_n must be positive")

    data = fixture or build_fixture()
    signals = extract_signals(data.observations, BASELINE_RULES)
    observation_by_id = {observation.id: observation for observation in data.observations}
    scores = rank_signal_scores(
        tuple(
            score_signal(signal, _observable_dimensions(observation_by_id[signal.observation_ids[0]].content))
            for signal in signals
        )
    )
    top_scores = scores[:top_n]
    signal_by_id = {signal.id: signal for signal in signals}
    top_signals: tuple[AccountSignal, ...] = tuple(
        signal_by_id[score.signal_id] for score in top_scores
    )
    precision = evaluate_observation_precision(top_signals, EXPECTED_SIGNAL_OBSERVATION_IDS)
    return AccountIntelligenceBenchmarkResult(
        analyzed_accounts=len(data.accounts),
        extracted_signals=len(signals),
        ranked_top_signals=top_scores,
        precision=precision,
    )
