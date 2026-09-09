"""Canonical evidence contracts and deterministic validation for Account Intelligence."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Mapping, Sequence

from factory.account_intelligence.domain import SourceObservation


class EvidenceVerificationState(str, Enum):
    """Verification state for a claim supported by source observations."""

    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    CONFLICTING = "CONFLICTING"
    UNVERIFIABLE = "UNVERIFIABLE"


@dataclass(frozen=True)
class Evidence:
    """Validated representation of a claim supported by observations."""

    id: str
    account_id: str
    source_ids: Sequence[str]
    observation_ids: Sequence[str]
    observed_at: str
    claim: str
    strength: float
    provenance: str
    verification_state: EvidenceVerificationState = EvidenceVerificationState.UNVERIFIED
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("id", "account_id", "observed_at", "claim", "provenance"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not self.source_ids:
            raise ValueError("source_ids must not be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids must not be empty")
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("strength must be between 0 and 1")
        if self.verification_state is EvidenceVerificationState.VERIFIED and self.strength <= 0.0:
            raise ValueError("verified evidence must have positive strength")


def _stable_evidence_id(account_id: str, observation_ids: Sequence[str], claim: str) -> str:
    payload = "|".join((account_id, *sorted(set(observation_ids)), claim.strip()))
    return "ev-" + sha256(payload.encode("utf-8")).hexdigest()[:24]


def build_evidence(
    observations: Sequence[SourceObservation],
    *,
    claim: str,
    strength: float,
    verification_state: EvidenceVerificationState = EvidenceVerificationState.UNVERIFIED,
) -> Evidence:
    """Build canonical evidence from explicit observations without inventing provenance."""
    if not observations:
        raise ValueError("observations must not be empty")
    if not claim.strip():
        raise ValueError("claim must not be empty")
    account_ids = {observation.account_id for observation in observations}
    if len(account_ids) != 1:
        raise ValueError("all observations must belong to the same account")
    source_ids = tuple(sorted({observation.source_id for observation in observations}))
    observation_ids = tuple(sorted({observation.id for observation in observations}))
    provenance = ";".join(sorted({observation.provenance for observation in observations}))
    observed_at = max(observation.observed_at for observation in observations)
    evidence = Evidence(
        id=_stable_evidence_id(next(iter(account_ids)), observation_ids, claim),
        account_id=next(iter(account_ids)),
        source_ids=source_ids,
        observation_ids=observation_ids,
        observed_at=observed_at,
        claim=claim.strip(),
        strength=strength,
        provenance=provenance,
        verification_state=verification_state,
    )
    validate_evidence(evidence, observations)
    return evidence


def validate_evidence(evidence: Evidence, observations: Sequence[SourceObservation]) -> None:
    """Apply deterministic support rules before evidence may be treated as verified."""
    by_id = {observation.id: observation for observation in observations}
    missing = [observation_id for observation_id in evidence.observation_ids if observation_id not in by_id]
    if missing:
        raise ValueError("evidence references unknown observations")
    linked = [by_id[observation_id] for observation_id in evidence.observation_ids]
    if any(observation.account_id != evidence.account_id for observation in linked):
        raise ValueError("evidence account_id does not match observations")
    if any(observation.source_id not in evidence.source_ids for observation in linked):
        raise ValueError("evidence source linkage is incomplete")
    if evidence.verification_state is EvidenceVerificationState.VERIFIED:
        if evidence.strength <= 0.0 or any(observation.confidence <= 0.0 for observation in linked):
            raise ValueError("unsupported evidence cannot be marked verified")
    if evidence.verification_state is EvidenceVerificationState.UNVERIFIABLE and evidence.strength > 0.0:
        raise ValueError("unverifiable evidence cannot claim positive strength")
