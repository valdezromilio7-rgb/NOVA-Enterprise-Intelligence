"""Deterministic account fixture for Account Intelligence evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from factory.account_intelligence.domain import Account, SourceObservation


@dataclass(frozen=True)
class AccountIntelligenceFixture:
    """A reproducible evaluation fixture with raw observations only."""

    accounts: tuple[Account, ...]
    observations: tuple[SourceObservation, ...]


def build_fixture(account_count: int = 100) -> AccountIntelligenceFixture:
    """Build deterministic synthetic accounts without embedding ground truth."""
    if account_count <= 0:
        raise ValueError("account_count must be positive")

    accounts: list[Account] = []
    observations: list[SourceObservation] = []

    for index in range(1, account_count + 1):
        account_id = f"acct-fixture-{index:03d}"
        accounts.append(
            Account(
                id=account_id,
                name=f"Fixture Company {index:03d}",
                country="PY",
                industry="wholesale_distribution",
                location="Paraguay",
                metadata={"fixture": "account-intelligence-v0.1", "index": str(index)},
            )
        )
        observations.append(
            SourceObservation(
                id=f"obs-fixture-{index:03d}",
                account_id=account_id,
                source_id="fixture",
                observed_at="2026-01-01T00:00:00Z",
                reference=f"fixture://observation/{index:03d}",
                content=(
                    "Customer support reports repeated delivery-status requests."
                    if index % 5 == 0
                    else "Routine company profile observation."
                ),
                provenance="synthetic-fixture",
                confidence=1.0,
                metadata={"fixture": "account-intelligence-v0.1"},
            )
        )

    return AccountIntelligenceFixture(accounts=tuple(accounts), observations=tuple(observations))
