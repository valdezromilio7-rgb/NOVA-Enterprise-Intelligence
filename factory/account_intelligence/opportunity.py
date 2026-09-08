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
    """Translate an observed account signal into the existing Opportunity contract.

    This bridge does not infer commercial value, assign a score, authorize
    execution, or manufacture evidence. Observation references are preserved
    in metadata until the Evidence Engine provides canonical evidence IDs.
    """
    if signal.account_id != account.id:
        raise ValueError("signal account_id does not match account")
    if not signal.title.strip():
        raise ValueError("signal title must not be empty")

    opportunity_id = f"opp-{signal.id}"
    return Opportunity(
        id=opportunity_id,
        title=title or signal.title,
        problem=problem or signal.title,
        target_customer=target_customer or account.name,
        evidence_ids=[],
        assumptions=["opportunity translated from observed account signal"],
        metadata={
            "account_id": account.id,
            "signal_id": signal.id,
            "observation_ids": ",".join(sorted(signal.observation_ids)),
            "translation_version": "account-opportunity-v0.1",
        },
    )
