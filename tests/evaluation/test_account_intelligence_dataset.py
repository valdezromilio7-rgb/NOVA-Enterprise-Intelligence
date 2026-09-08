from evaluation.account_intelligence.dataset import build_fixture


def test_fixture_has_100_accounts_and_observations() -> None:
    fixture = build_fixture()
    assert len(fixture.accounts) == 100
    assert len(fixture.observations) == 100


def test_fixture_is_deterministic() -> None:
    assert build_fixture() == build_fixture()


def test_fixture_rejects_non_positive_account_count() -> None:
    try:
        build_fixture(0)
    except ValueError as exc:
        assert str(exc) == "account_count must be positive"
    else:
        raise AssertionError("expected ValueError")
