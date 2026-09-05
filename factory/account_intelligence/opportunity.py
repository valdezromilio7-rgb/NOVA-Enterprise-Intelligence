"""Deterministic bridge from account intelligence signals to opportunities."""

from __future__ import annotations

from dataclasses import dataclass

from factory.account_intelligence.domain import Account, AccountSignal
from factory.schemas.domain import Opportunity


@dataclass(frozen=True)
class AccountOpportunityLink:
    """Auditable mapping between an account signal and an opportunity."""

    account_id: str
    signal_id: str
    opportunity_id: str


def signal_to_opportunity(
    account: Account,
    signal: AccountSignal,
    *,
    title: str | None = None,
    problem: str | None = None,
    target_customer: str | None = None,
) -> Opportunity:
    """Create a factory Opportunity without bypassing existing governance.

    The function only translates an already-observed signal. It does not infer
    commercial value, authorize execution, or assign a score.
    """
    if signal.account_id != account.id:
        raise ValueError("signal account_id does not match account")
    if not signal.claim.strip():
        raise ValueError("signal claim must not be empty")

    opportunity_id = f"opp-{signal.id}"
    return Opportunity(
        id=opportunity_id,
        title=title or signal.claim,
        problem=problem or signal.claim,
        target_customer=target_customer or account.name,
        evidence_ids=list(signal.evidence_ids),
        assumptions=["opportunity translated from observed account signal"],
        metadata={
            "account_id": account.id,
            "signal_id": signal.id,
            "source_id": signal.source_id,
            "translation_version": "account-opportunity-v0.1",
        },
    )
