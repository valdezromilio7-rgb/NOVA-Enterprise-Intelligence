from factory.account_intelligence.domain import Account, AccountSignal
from factory.account_intelligence.opportunity import signal_to_opportunity
from factory.schemas.domain import Signal


def test_canonical_signal_supports_account_scope():
    signal = Signal(
        id="sig-1",
        source="source-1",
        observed_at="2026-09-19T12:00:00Z",
        subject="Demand increased",
        content="Observed demand increase",
        provenance="source-1",
        account_id="account-1",
        signal_type="demand",
        observation_ids=("obs-1",),
        confidence=0.9,
        rationale="Repeated observation",
    )

    assert signal.account_id == "account-1"
    assert signal.signal_type == "demand"
    assert signal.observation_ids == ("obs-1",)
    assert signal.title == signal.subject


def test_account_signal_compatibility_constructor_returns_canonical_signal():
    signal = AccountSignal(
        id="sig-legacy",
        account_id="account-1",
        signal_type="demand",
        title="Demand increased",
        observed_at="2026-09-19T12:00:00Z",
        observation_ids=("obs-1",),
        confidence=0.8,
    )

    assert isinstance(signal, Signal)
    assert signal.account_id == "account-1"
    assert signal.title == "Demand increased"


def test_account_signal_bridge_accepts_canonical_signal():
    signal = Signal(
        id="sig-2",
        source="source-1",
        observed_at="2026-09-19T12:00:00Z",
        subject="Need identified",
        content="Observed need",
        provenance="source-1",
        account_id="account-1",
        signal_type="need",
        observation_ids=("obs-2",),
        confidence=0.95,
    )
    opportunity = signal_to_opportunity(
        Account(id="account-1", name="Example Account", country="PY"),
        signal,
    )

    assert opportunity.metadata["signal_id"] == "sig-2"
    assert opportunity.evidence_ids == []


def test_account_scoped_signal_requires_observations():
    try:
        Signal(
            id="sig-invalid",
            source="source-1",
            observed_at="2026-09-19T12:00:00Z",
            subject="Invalid",
            content="Invalid",
            provenance="source-1",
            account_id="account-1",
            signal_type="need",
        )
    except ValueError as exc:
        assert "observations" in str(exc)
    else:
        raise AssertionError("expected account-scoped signal validation to fail")
