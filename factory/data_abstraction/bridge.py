"""Bridge provider-neutral observations into canonical account-domain observations."""

from __future__ import annotations

from factory.account_intelligence.domain import SourceObservation
from factory.data_abstraction.domain import NormalizedObservation


def to_source_observation(observation: NormalizedObservation) -> SourceObservation:
    """Convert an account-scoped normalized observation without changing facts."""
    if observation.account_id is None:
        raise ValueError("global observations cannot be converted to account-scoped SourceObservation")
    return SourceObservation(
        id=observation.id,
        source_id=observation.source_id,
        account_id=observation.account_id,
        observed_at=observation.observed_at,
        reference=observation.reference,
        content=observation.content,
        provenance=observation.provenance,
        confidence=observation.confidence,
        metadata={str(k): str(v) for k, v in observation.metadata.items()},
    )
