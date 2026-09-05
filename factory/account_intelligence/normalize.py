"""Deterministic normalization and identifiers for Account Intelligence."""
from __future__ import annotations

import hashlib
import re
from dataclasses import replace
from typing import Iterable

from factory.account_intelligence.domain import Account, SourceObservation


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def stable_account_id(name: str, country: str, website: str = "") -> str:
    raw = "|".join((normalize_text(name), normalize_text(country), normalize_text(website)))
    return "acct_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def stable_observation_id(observation: SourceObservation) -> str:
    raw = "|".join(
        (
            observation.source_id,
            observation.account_id,
            observation.observed_at,
            observation.reference,
            observation.content,
        )
    )
    return "obs_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def normalize_account(account: Account) -> Account:
    account_id = stable_account_id(account.name, account.country, account.website)
    return replace(
        account,
        id=account_id,
        name=normalize_text(account.name),
        country=normalize_text(account.country),
        industry=normalize_text(account.industry),
        size=normalize_text(account.size),
        location=normalize_text(account.location),
        website=normalize_text(account.website),
    )


def normalize_observation(observation: SourceObservation) -> SourceObservation:
    return replace(
        observation,
        id=stable_observation_id(observation),
        source_id=normalize_text(observation.source_id),
        account_id=normalize_text(observation.account_id),
        observed_at=observation.observed_at.strip(),
        reference=observation.reference.strip(),
        content=re.sub(r"\s+", " ", observation.content.strip()),
        provenance=observation.provenance.strip(),
    )


def normalize_observations(observations: Iterable[SourceObservation]) -> list[SourceObservation]:
    unique: dict[str, SourceObservation] = {}
    for observation in observations:
        normalized = normalize_observation(observation)
        unique[normalized.id] = normalized
    return sorted(unique.values(), key=lambda item: item.id)
