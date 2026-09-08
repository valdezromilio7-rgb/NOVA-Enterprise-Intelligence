from factory.account_intelligence.domain import AccountSignal
from factory.account_intelligence.score import rank_signal_scores, score_signal
from factory.account_intelligence.signal_engine import SignalRule, extract_signals
from evaluation.account_intelligence.dataset import build_fixture


def _signal() -> AccountSignal:
    return AccountSignal(
        id="sig-1",
        account_id="acct-1",
        signal_type="customer_pain",
        title="Delivery support demand",
        observed_at="2026-01-01T00:00:00Z",
        observation_ids=("obs-1",),
        confidence=0.9,
    )


def test_signal_score_is_sum_of_bounded_dimensions() -> None:
    score = score_signal(
        _signal(),
        {
            "relevance": 25,
            "recency": 20,
            "intensity": 15,
            "icp_fit": 18,
            "evidence": 9,
            "verifiability": 5,
        },
    )
    assert score.total_score == 92
    assert score.confidence == 0.9


def test_signal_ranking_is_deterministic() -> None:
    high = score_signal(_signal(), {"relevance": 25, "recency": 20, "intensity": 20, "icp_fit": 20, "evidence": 10, "verifiability": 5})
    low_signal = AccountSignal(
        id="sig-2",
        account_id="acct-2",
        signal_type="customer_pain",
        title="Other",
        observed_at="2026-01-01T00:00:00Z",
        observation_ids=("obs-2",),
        confidence=0.8,
    )
    low = score_signal(low_signal, {"relevance": 10, "recency": 10, "intensity": 10, "icp_fit": 10, "evidence": 5, "verifiability": 5})
    assert [item.signal_id for item in rank_signal_scores((low, high))] == ["sig-1", "sig-2"]


def test_signal_engine_does_not_need_ground_truth() -> None:
    fixture = build_fixture()
    rules = (SignalRule("delivery-demand-v0.1", "customer_pain", "Repeated delivery-status support demand", ("customer support", "delivery-status")),)
    signals = extract_signals(fixture.observations, rules)
    assert len(signals) == 20
    assert all(signal.account_id.startswith("acct-fixture-") for signal in signals)
