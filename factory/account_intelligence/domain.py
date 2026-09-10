"""Provider-agnostic domain contracts for Account Intelligence v0.1."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Account:
    """Canonical business account identity independent of any provider."""

    id: str
    name: str
    country: str
    industry: str = ""
    size: str = ""
    location: str = ""
    website: str = ""
    source_refs: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("id", "name", "country"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True)
class Source:
    """A declared information source; it does not itself prove a claim."""

    id: str
    name: str
    kind: str
    authority: str = ""
    base_reference: str = ""
    version: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("id", "name", "kind"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True)
class SourceObservation:
    """An observed source fact before it is interpreted as a business signal."""

    id: str
    source_id: str
    account_id: str
    observed_at: str
    reference: str
    content: str
    provenance: str
    confidence: float = 1.0
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in (
            "id",
            "source_id",
            "account_id",
            "observed_at",
            "reference",
            "content",
            "provenance",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class AccountSignal:
    """Account-scoped interpretation backed by one or more observations."""

    id: str
    account_id: str
    signal_type: str
    title: str
    observed_at: str
    observation_ids: Sequence[str]
    confidence: float
    rationale: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("id", "account_id", "signal_type", "title", "observed_at"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not self.observation_ids:
            raise ValueError("observation_ids must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
