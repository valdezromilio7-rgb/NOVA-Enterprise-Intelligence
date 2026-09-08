from factory.account_intelligence.domain import Account, AccountSignal
from factory.account_intelligence.opportunity import signal_to_opportunity


def make_account() -> Account:
    return Account(id="acct_1", name="Acme SA", country="PY")


def make_signal(account_id: str = "acct_1") -> AccountSignal:
    return AccountSignal(
        id="sig_1",
        account_id=account_id,
        signal_type="hiring",
        title="Acme is expanding its sales team",
        observed_at="2026-09-05T12:00:00Z",
        observation_ids=("obs_2", "obs_1"),
        confidence=0.9,
    )


def test_signal_to_opportunity_preserves_traceability() -> None:
    opportunity = signal_to_opportunity(make_account(), make_signal())

    assert opportunity.id == "opp-sig_1"
    assert opportunity.title == "Acme is expanding its sales team"
    assert opportunity.problem == "Acme is expanding its sales team"
    assert opportunity.target_customer == "Acme SA"
    assert opportunity.evidence_ids == []
    assert opportunity.metadata["account_id"] == "acct_1"
    assert opportunity.metadata["signal_id"] == "sig_1"
    assert opportunity.metadata["observation_ids"] == "obs_1,obs_2"
    assert opportunity.metadata["translation_version"] == "account-opportunity-v0.1"


def test_signal_to_opportunity_is_deterministic() -> None:
    first = signal_to_opportunity(make_account(), make_signal())
    second = signal_to_opportunity(make_account(), make_signal())

    assert first == second


def test_signal_to_opportunity_rejects_cross_account_signal() -> None:
    try:
        signal_to_opportunity(make_account(), make_signal("acct_2"))
        assert False, "cross-account signal must be rejected"
    except ValueError as exc:
        assert "account_id" in str(exc)


def test_signal_to_opportunity_allows_explicit_context_overrides() -> None:
    opportunity = signal_to_opportunity(
        make_account(),
        make_signal(),
        title="Sales expansion opportunity",
        problem="Growing sales capacity may require workflow support",
        target_customer="Acme commercial team",
    )

    assert opportunity.title == "Sales expansion opportunity"
    assert opportunity.problem == "Growing sales capacity may require workflow support"
    assert opportunity.target_customer == "Acme commercial team"
