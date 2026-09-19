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
    """Canonical interpretation of one or more observations.

    A Signal is the single domain concept used by Product Factory and Account
    Intelligence. Generic signals may omit account-scoped fields; account-scoped
    signals must identify their observations and signal type. Signal IDs must
    never be used as Evidence IDs.
    """

    id: str
    source: str
    observed_at: str
    subject: str
    content: str
    provenance: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
    account_id: str | None = None
    signal_type: str | None = None
    observation_ids: Sequence[str] = field(default_factory=tuple)
    confidence: float | None = None
    rationale: str = ""

    @property
    def title(self) -> str:
        """Compatibility/readability alias for account-scoped consumers."""
        return self.subject

    def __post_init__(self) -> None:
        for field_name in (
            "id",
            "source",
            "observed_at",
            "subject",
            "content",
            "provenance",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.account_id is not None and not self.account_id.strip():
            raise ValueError("account_id must be non-empty when provided")
        if self.signal_type is not None and not self.signal_type.strip():
            raise ValueError("signal_type must be non-empty when provided")

        if self.account_id is not None and not self.observation_ids:
            raise ValueError("account-scoped signals must reference observations")
        if self.account_id is not None and self.signal_type is None:
            raise ValueError("account-scoped signals must define signal_type")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("signal confidence must be between 0 and 1")


@dataclass(frozen=True)
class Evidence:
    """Canonical validated representation of a claim supported by observations."""

    id: str
    account_id: str | None
    source_ids: Sequence[str]
    observation_ids: Sequence[str]
    observed_at: str
    claim: str
    strength: float
    provenance: str
    verification_state: EvidenceVerificationState = EvidenceVerificationState.UNVERIFIED
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("id", "observed_at", "claim", "provenance"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.account_id is not None and not self.account_id.strip():
            raise ValueError("account_id must be non-empty when provided")
        if not self.source_ids:
            raise ValueError("source_ids must not be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids must not be empty")
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("evidence strength must be between 0 and 1")
        if self.verification_state is EvidenceVerificationState.VERIFIED and self.strength <= 0.0:
            raise ValueError("verified evidence must have positive strength")


@dataclass(frozen=True)
class Context:
    """Canonical context assembled from explicit signals and evidence."""
    id: str
    signal_id: str
    context_type: str
    facts: Sequence[str]
    evidence_refs: Sequence[str]
    current_state: str
    change_event: str
    confidence: float
    provenance: str
    account_id: str | None = None
    context_version: str = "context-v0.1"

    def __post_init__(self) -> None:
        for name in ("id", "signal_id", "context_type", "current_state", "provenance"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.account_id is not None and not self.account_id.strip():
            raise ValueError("account_id must be non-empty when provided")
        if not self.facts:
            raise ValueError("facts must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class WhyNow:
    """Canonical timing assessment; urgency is never inferred silently."""
    id: str
    signal_id: str
    trigger: str
    timing_factors: Sequence[str]
    rationale: str
    evidence_refs: Sequence[str]
    confidence: float
    verifiable: bool
    account_id: str | None = None
    assessment_version: str = "why-now-v0.1"

    def __post_init__(self) -> None:
        for name in ("id", "signal_id", "trigger", "rationale"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.account_id is not None and not self.account_id.strip():
            raise ValueError("account_id must be non-empty when provided")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.verifiable and not self.evidence_refs:
            raise ValueError("verifiable Why Now assessments require evidence references")


@dataclass(frozen=True)
class BusinessProblem:
    """Canonical problem statement derived from explicit context and Why Now."""

    id: str
    signal_id: str
    context_id: str
    why_now_id: str
    context_version: str
    why_now_version: str
    problem_statement: str
    current_solution: str
    gap: str
    desired_outcome: str
    evidence_refs: Sequence[str]
    confidence: float
    provenance: str
    account_id: str | None = None
    problem_version: str = "business-problem-v0.1"

    def __post_init__(self) -> None:
        for name in ("id", "signal_id", "context_id", "why_now_id", "context_version", "why_now_version", "problem_statement", "current_solution", "gap", "desired_outcome", "provenance"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.account_id is not None and not self.account_id.strip():
            raise ValueError("account_id must be non-empty when provided")
        if not self.evidence_refs:
            raise ValueError("business problem requires evidence references")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class Opportunity:
    id: str
    title: str
    problem: str
    target_customer: str
    state: OpportunityState = OpportunityState.DISCOVERY
    account_id: str | None = None
    business_problem_id: str | None = None
    # Only canonical Evidence IDs belong here. Observation, Signal, Source, or
    # arbitrary references must remain in their own contracts/metadata.
    evidence_ids: Sequence[str] = field(default_factory=tuple)
    assumptions: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("id", "title", "problem", "target_customer"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.account_id is not None and not self.account_id.strip():
            raise ValueError("account_id must be non-empty when provided")
        if self.business_problem_id is not None and not self.business_problem_id.strip():
            raise ValueError("business_problem_id must be non-empty when provided")


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
