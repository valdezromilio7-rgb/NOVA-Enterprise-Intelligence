"""Provider-neutral ingestion contracts with deterministic normalization."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class FreshnessStatus(str, Enum):
    FRESH = "fresh"
    STALE = "stale"
    UNKNOWN = "unknown"


class AcquisitionStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass(frozen=True)
class ProviderCapabilities:
    """Declared adapter capabilities; names are provider-neutral semantics."""

    supports_incremental: bool = False
    supports_pagination: bool = False
    supports_time_filter: bool = False
    supports_read_only: bool = True
    max_page_size: int | None = None

    def __post_init__(self) -> None:
        if self.max_page_size is not None and self.max_page_size <= 0:
            raise ValueError("max_page_size must be positive when provided")
        if not self.supports_read_only:
            raise ValueError("v0.1 adapters must support read-only acquisition")


@dataclass(frozen=True)
class RetrievalMetadata:
    retrieved_at: str
    request_id: str = ""
    duration_ms: int | None = None
    freshness: FreshnessStatus = FreshnessStatus.UNKNOWN
    error_code: str = ""
    error_message: str = ""

    def __post_init__(self) -> None:
        if not self.retrieved_at.strip():
            raise ValueError("retrieved_at must not be empty")
        if self.duration_ms is not None and self.duration_ms < 0:
            raise ValueError("duration_ms must not be negative")


@dataclass(frozen=True)
class NormalizedObservation:
    """Provider-neutral observation ready for canonical SourceObservation creation."""

    id: str
    source_id: str
    account_id: str | None = None
    observed_at: str
    reference: str
    content: str
    provenance: str
    confidence: float = 1.0
    retrieval: RetrievalMetadata | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("id", "source_id", "observed_at", "reference", "content", "provenance"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.account_id is not None and not self.account_id.strip():
            raise ValueError("account_id must be non-empty when provided")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class ObservationQueryResult:
    """Normalized observations exposed to downstream canonical domain consumers."""

    observations: Sequence[NormalizedObservation]
    retrieval: RetrievalMetadata

    def __post_init__(self) -> None:
        if self.retrieval is None:
            raise ValueError("retrieval metadata is required")


@dataclass(frozen=True)
class AcquisitionResult:
    """Auditable result of one adapter acquisition attempt."""

    provider: str
    status: AcquisitionStatus
    observations: Sequence[NormalizedObservation] = field(default_factory=tuple)
    retrieval: RetrievalMetadata | None = None

    def __post_init__(self) -> None:
        if not self.provider.strip():
            raise ValueError("provider must not be empty")
        if self.status is AcquisitionStatus.SUCCESS and self.retrieval is None:
            raise ValueError("successful acquisition requires retrieval metadata")
        if self.status is AcquisitionStatus.FAILED and self.observations:
            raise ValueError("failed acquisition must not expose observations")
