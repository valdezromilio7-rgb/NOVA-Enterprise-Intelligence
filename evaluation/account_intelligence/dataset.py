"""Deterministic account fixture for Account Intelligence evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from factory.account_intelligence.domain import Account, AccountSignal, SourceObservation


@dataclass(frozen=True)
class AccountIntelligenceFixture:
    """A reproducible evaluation fixture with explicit expected signals."""

    accounts: tuple[Account, ...]
    observations: tuple[SourceObservation, ...]
    signals: tuple[AccountSignal, ...]
    expected_signal_ids: frozenset[str]


def build_fixture(account_count: int = 100) -> AccountIntelligenceFixture:
    """Build deterministic synthetic accounts without external data access."""
    if account_count <= 0:
        raise ValueError("account_count must be positive")

    accounts: list[Account] = []
    observations: list[SourceObservation] = []
    signals: list[AccountSignal] = []
    expected: set[str] = set()

    for index in range(1, account_count + 1):
        account_id = f"acct-fixture-{index:03d}"
        account = Account(
            id=account_id,
            name=f"Fixture Company {index:03d}",
            industry="wholesale_distribution",
            location="Paraguay",
            metadata={"fixture": "account-intelligence-v0.1", "index": index},
        )
        accounts.append(account)

        observation = SourceObservation(
            id=f"obs-fixture-{index:03d}",
            account_id=account_id,
            source_id="fixture",
            observed_at="2026-01-01T00:00:00Z",
            content=(
                "Customer support reports repeated delivery-status requests."
                if index % 5 == 0
                else "Routine company profile observation."
            ),
            provenance="synthetic-fixture",
            confidence=1.0,
            metadata={"fixture": "account-intelligence-v0.1"},
        )
        observations.append(observation)

        if index % 5 == 0:
            signal = AccountSignal(
                id=f"sig-fixture-{index:03d}",
                account_id=account_id,
                source_id="fixture",
                observation_ids=[observation.id],
                title="Repeated delivery-status support demand",
                claim="Customers repeatedly request delivery status information",
                observed_at=observation.observed_at,
                confidence=0.95,
                metadata={"fixture": "account-intelligence-v0.1"},
            )
            signals.append(signal)
            expected.add(signal.id)

    return AccountIntelligenceFixture(
        accounts=tuple(accounts),
        observations=tuple(observations),
        signals=tuple(signals),
        expected_signal_ids=frozenset(expected),
    )
