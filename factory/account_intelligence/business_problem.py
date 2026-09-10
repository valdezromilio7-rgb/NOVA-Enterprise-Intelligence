"""Provider-agnostic business problem contract for Account Intelligence."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Tuple

from factory.account_intelligence.context import AccountContext, WhyNowAssessment


@dataclass(frozen=True)
class BusinessProblem:
    """Auditable business problem derived from explicit context and timing."""

    id: str
    account_id: str
    signal_id: str
    context_version: str
    why_now_version: str
    problem_statement: str
    current_solution: str
    gap: str
    desired_outcome: str
    evidence_refs: Tuple[str, ...]
    confidence: float
    provenance: str
    problem_version: str = "business-problem-v0.1"

    def __post_init__(self) -> None:
        required = (
            self.id,
            self.account_id,
            self.signal_id,
            self.context_version,
            self.why_now_version,
            self.problem_statement,
            self.current_solution,
            self.gap,
            self.desired_outcome,
            self.provenance,
        )
        if any(not value.strip() for value in required):
            raise ValueError("business problem required fields must be non-empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.evidence_refs:
            raise ValueError("business problem requires evidence references")


def _stable_problem_id(
    account_id: str,
    signal_id: str,
    context_version: str,
    why_now_version: str,
) -> str:
    payload = "|".join((account_id, signal_id, context_version, why_now_version))
    return "bp-" + sha256(payload.encode("utf-8")).hexdigest()[:24]


def build_business_problem(
    *,
    context: AccountContext,
    why_now: WhyNowAssessment,
    problem_statement: str,
    current_solution: str,
    gap: str,
    desired_outcome: str,
    evidence_refs: Tuple[str, ...],
    confidence: float,
    provenance: str,
) -> BusinessProblem:
    """Construct a business problem without inventing facts or evidence."""
    if context.account_id != why_now.account_id or context.signal_id != why_now.signal_id:
        raise ValueError("context and Why Now identity must match")
    refs = tuple(sorted(set(ref.strip() for ref in evidence_refs if ref.strip())))
    if not refs:
        raise ValueError("business problem requires evidence references")
    return BusinessProblem(
        id=_stable_problem_id(
            context.account_id,
            context.signal_id,
            context.context_version,
            why_now.assessment_version,
        ),
        account_id=context.account_id,
        signal_id=context.signal_id,
        context_version=context.context_version,
        why_now_version=why_now.assessment_version,
        problem_statement=problem_statement,
        current_solution=current_solution,
        gap=gap,
        desired_outcome=desired_outcome,
        evidence_refs=refs,
        confidence=confidence,
        provenance=provenance,
    )
