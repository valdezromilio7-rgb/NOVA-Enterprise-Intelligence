"""Thin orchestration boundary for real provider observation consumption."""

from __future__ import annotations

from factory.data_abstraction.adapter import DataProviderAdapter
from factory.data_abstraction.consumer import evidence_from_observations, signal_from_observation
from factory.data_abstraction.domain import AcquisitionStatus
from factory.schemas.domain import Evidence, EvidenceVerificationState, Signal


def acquire_bcp_signal_and_evidence(
    adapter: DataProviderAdapter,
    *,
    currency: str = "USD",
    claim: str | None = None,
) -> tuple[Signal, Evidence]:
    """Acquire one real provider observation and derive canonical Signal/Evidence."""
    result = adapter.acquire({"currency": currency})
    if result.status is not AcquisitionStatus.SUCCESS:
        raise RuntimeError(
            f"provider acquisition failed: {result.retrieval.error_code or 'UNKNOWN'}"
        )
    if len(result.observations) != 1:
        raise ValueError("expected exactly one observation")
    observation = result.observations[0]
    signal = signal_from_observation(
        observation,
        subject=f"{currency.upper()}/PYG reference rate",
        signal_type="reference_rate",
        rationale="Direct provider observation from BCP daily reference currency source.",
    )
    evidence_claim = claim or observation.content
    evidence = evidence_from_observations(
        (observation,),
        claim=evidence_claim,
        strength=observation.confidence,
        verification_state=EvidenceVerificationState.VERIFIED,
    )
    return signal, evidence
