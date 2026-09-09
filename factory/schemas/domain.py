"""Canonical, dependency-light domain objects for the Product Factory.

These models deliberately contain no provider-specific or infrastructure-specific
logic. They form the traceable contract between discovery, scoring, validation,
governance, and orchestration.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class EvidenceType(str, Enum):
    OBSERVED = "observed"
    REPORTED = "reported"
    EXPERIMENTAL = "experimental"
    INFERRED = "inferred"


class EvidenceVerificationState(str, Enum):
    """Verification state for a claim supported by source observations."""

    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    CONFLICTING = "CONFLICTING"
    UNVERIFIABLE = "UNVERIFIABLE"


class OpportunityState(str, Enum):
    IDEA = "idea"
    DISCOVERY = "discovery"
    VALIDATION = "validation"
    APPROVED = "approved"
    BUILDING = "building"
    QA = "qa"
    DEPLOYMENT = "deployment"
    LIVE = "live"
    GROWING = "growing"
    SCALE = "scale"
    HOLD = "hold"
    KILL = "kill"


@dataclass(frozen=True)
class Signal:
    id: str
    source: str
    observed_at: str
    subject: str
    content: str
    provenance: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Evidence:
    """Canonical validated representation of a claim supported by observations."""

    id: str
    account_id: str
    source_ids: Sequence[str]
    observation_ids: Sequence[str]
    observed_at: str
    claim: str
    strength: float
    provenance: str
    verification_state: EvidenceVerificationState = EvidenceVerificationState.UNVERIFIED
    metadata: Mapping[str, Any] = field(default_factory=dict)

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
            raise ValueError("evidence strength must be between 0 and 1")
        if self.verification_state is EvidenceVerificationState.VERIFIED and self.strength <= 0.0:
            raise ValueError("verified evidence must have positive strength")


@dataclass(frozen=True)
class Opportunity:
    id: str
    title: str
    problem: str
    target_customer: str
    state: OpportunityState = OpportunityState.DISCOVERY
    evidence_ids: Sequence[str] = field(default_factory=tuple)
    assumptions: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OpportunityScore:
    opportunity_id: str
    dimensions: Mapping[str, float]
    weighted_score: float
    confidence: float
    rationale: str
    scoring_version: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.weighted_score <= 100.0:
            raise ValueError("weighted score must be between 0 and 100")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class ValidationExperiment:
    id: str
    opportunity_id: str
    hypothesis: str
    method: str
    success_metric: str
    failure_threshold: str
    budget_limit: float
    status: str = "planned"


@dataclass(frozen=True)
class Decision:
    id: str
    subject_id: str
    gate: str
    outcome: str
    rationale: str
    decided_by: str
    evidence_ids: Sequence[str] = field(default_factory=tuple)
    timestamp: str = ""
