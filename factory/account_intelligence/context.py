"""Provider-agnostic account context and Why Now assessment contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


@dataclass(frozen=True)
class AccountContext:
    """Auditable context assembled from observations and signals."""

    account_id: str
    signal_id: str
    context_type: str
    facts: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    current_state: str
    change_event: str
    confidence: float
    provenance: str
    context_version: str = "account-context-v0.1"

    def __post_init__(self) -> None:
        if not self.account_id.strip() or not self.signal_id.strip():
            raise ValueError("account_id and signal_id must be non-empty")
        if not self.context_type.strip() or not self.current_state.strip():
            raise ValueError("context_type and current_state must be non-empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.facts:
            raise ValueError("facts must not be empty")
        if not self.provenance.strip():
            raise ValueError("provenance must be non-empty")


@dataclass(frozen=True)
class WhyNowAssessment:
    """Explicit timing rationale; it does not claim urgency without evidence."""

    account_id: str
    signal_id: str
    trigger: str
    timing_factors: Tuple[str, ...]
    rationale: str
    evidence_refs: Tuple[str, ...]
    confidence: float
    verifiable: bool
    assessment_version: str = "why-now-v0.1"

    def __post_init__(self) -> None:
        if not self.account_id.strip() or not self.signal_id.strip():
            raise ValueError("account_id and signal_id must be non-empty")
        if not self.trigger.strip() or not self.rationale.strip():
            raise ValueError("trigger and rationale must be non-empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.verifiable and not self.evidence_refs:
            raise ValueError("verifiable Why Now assessments require evidence references")


def build_account_context(
    *,
    account_id: str,
    signal_id: str,
    context_type: str,
    facts: Tuple[str, ...],
    evidence_refs: Tuple[str, ...],
    current_state: str,
    change_event: str,
    confidence: float,
    provenance: str,
) -> AccountContext:
    """Construct context without inferring facts or fabricating evidence."""
    return AccountContext(
        account_id=account_id,
        signal_id=signal_id,
        context_type=context_type,
        facts=tuple(fact.strip() for fact in facts if fact.strip()),
        evidence_refs=tuple(sorted(set(evidence_refs))),
        current_state=current_state,
        change_event=change_event,
        confidence=confidence,
        provenance=provenance,
    )


def assess_why_now(
    *,
    context: AccountContext,
    trigger: str,
    timing_factors: Tuple[str, ...],
    rationale: str,
    evidence_refs: Tuple[str, ...],
    confidence: float,
    verifiable: bool,
) -> WhyNowAssessment:
    """Create a bounded Why Now assessment from explicit context."""
    if context.account_id == "" or context.signal_id == "":
        raise ValueError("context identity must be present")
    return WhyNowAssessment(
        account_id=context.account_id,
        signal_id=context.signal_id,
        trigger=trigger,
        timing_factors=tuple(factor.strip() for factor in timing_factors if factor.strip()),
        rationale=rationale,
        evidence_refs=tuple(sorted(set(evidence_refs))),
        confidence=confidence,
        verifiable=verifiable,
    )
