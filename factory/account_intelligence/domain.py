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


def AccountSignal(
    *,
    id: str,
    account_id: str,
    signal_type: str,
    title: str,
    observed_at: str,
    observation_ids: Sequence[str],
    confidence: float,
    rationale: str = "",
    metadata: Mapping[str, str] | None = None,
):
    """Compatibility constructor for the canonical Signal.

    New code must import Signal from factory.schemas.domain directly.
    This adapter exists only to prevent an abrupt break for existing
    Account Intelligence callers while the duplicate AccountSignal contract is
    retired.
    """
    from factory.schemas.domain import Signal

    values = dict(metadata or {})
    provenance = str(values.pop("provenance", "account-intelligence"))
    return Signal(
        id=id,
        source=f"account:{account_id}",
        observed_at=observed_at,
        subject=title,
        content=title,
        provenance=provenance,
        metadata=values,
        account_id=account_id,
        signal_type=signal_type,
        observation_ids=tuple(observation_ids),
        confidence=confidence,
        rationale=rationale,
    )
