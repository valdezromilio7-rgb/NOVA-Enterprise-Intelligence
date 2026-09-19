"""Deterministic normalization and identifiers for adapter output."""

from __future__ import annotations

import hashlib
import re
from dataclasses import replace

from factory.data_abstraction.domain import NormalizedObservation


def normalize_text(value: str) -> str:
    return re.sub(r"\\s+", " ", value.strip())


def stable_observation_id(observation: NormalizedObservation) -> str:
    raw = "|".join((observation.source_id, observation.account_id, observation.observed_at, observation.reference, observation.content, observation.provenance))
    return "obs_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def normalize_observation(observation: NormalizedObservation) -> NormalizedObservation:
    normalized = replace(
        observation,
        source_id=normalize_text(observation.source_id),
        account_id=normalize_text(observation.account_id),
        reference=normalize_text(observation.reference),
        content=normalize_text(observation.content),
        provenance=normalize_text(observation.provenance),
    )
    return replace(normalized, id=stable_observation_id(normalized))
