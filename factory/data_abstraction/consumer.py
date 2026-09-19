"""Provider-neutral consumers that turn normalized observations into canonical domain facts."""

from __future__ import annotations

from hashlib import sha256
from typing import Sequence

from factory.data_abstraction.domain import NormalizedObservation
from factory.schemas.domain import Evidence, EvidenceVerificationState, Signal


def _stable_id(prefix: str, parts: Sequence[str]) -> str:
    payload = "|".join(part.strip() for part in parts)
    return f"{prefix}_{sha256(payload.encode("utf-8")).hexdigest()[:24]}"


def signal_from_observation(observation: NormalizedObservation, *, subject: str, content: str | None = None, signal_type: str | None = None, rationale: str = "") -> Signal:
    """Create the canonical Signal without inventing account scope."""
    if not subject.strip():
        raise ValueError("subject must not be empty")
    signal_content = observation.content if content is None else content
    if not signal_content.strip():
        raise ValueError("content must not be empty")
    return Signal(id=_stable_id("sig", (observation.id, subject, signal_content)), source=observation.source_id, observed_at=observation.observed_at, subject=subject.strip(), content=signal_content.strip(), provenance=observation.provenance, metadata=dict(observation.metadata), account_id=observation.account_id, signal_type=signal_type, observation_ids=(observation.id,), confidence=observation.confidence, rationale=rationale)


def evidence_from_observations(observations: Sequence[NormalizedObservation], *, claim: str, strength: float, verification_state: EvidenceVerificationState = EvidenceVerificationState.UNVERIFIED) -> Evidence:
    """Build canonical Evidence from provider-neutral observations."""
    if not observations:
        raise ValueError("observations must not be empty")
    if not claim.strip():
        raise ValueError("claim must not be empty")
    account_ids = {observation.account_id for observation in observations}
    if len(account_ids) != 1:
        raise ValueError("all observations must share the same account scope")
    source_ids = tuple(sorted({observation.source_id for observation in observations}))
    observation_ids = tuple(sorted({observation.id for observation in observations}))
    provenance = ";".join(sorted({observation.provenance for observation in observations}))
    observed_at = max(observation.observed_at for observation in observations)
    account_id = next(iter(account_ids))
    evidence = Evidence(id=_stable_id("ev", (account_id or "", *observation_ids, claim)), account_id=account_id, source_ids=source_ids, observation_ids=observation_ids, observed_at=observed_at, claim=claim.strip(), strength=strength, provenance=provenance, verification_state=verification_state)
    validate_normalized_evidence(evidence, observations)
    return evidence


def validate_normalized_evidence(evidence: Evidence, observations: Sequence[NormalizedObservation]) -> None:
    """Validate canonical evidence against its exact normalized observations."""
    by_id = {observation.id: observation for observation in observations}
    missing = [oid for oid in evidence.observation_ids if oid not in by_id]
    if missing:
        raise ValueError("evidence references unknown observations")
    linked = [by_id[oid] for oid in evidence.observation_ids]
    if any(observation.account_id != evidence.account_id for observation in linked):
        raise ValueError("evidence account_id does not match observations")
    if any(observation.source_id not in evidence.source_ids for observation in linked):
        raise ValueError("evidence source linkage is incomplete")
    if evidence.verification_state is EvidenceVerificationState.VERIFIED:
        if evidence.strength <= 0.0 or any(observation.confidence <= 0.0 for observation in linked):
            raise ValueError("unsupported evidence cannot be marked verified")
    if evidence.verification_state is EvidenceVerificationState.UNVERIFIABLE and evidence.strength > 0.0:
        raise ValueError("unverifiable evidence cannot claim positive strength")