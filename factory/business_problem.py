"""Generic canonical Business Problem consumer for provider-neutral intelligence."""

from __future__ import annotations

from hashlib import sha256
from typing import Sequence

from factory.schemas.domain import BusinessProblem, Context, WhyNow


def _id(parts: Sequence[str]) -> str:
    payload = "|".join(part.strip() for part in parts)
    return "bp_" + sha256(payload.encode("utf-8")).hexdigest()[:24]


def build_business_problem(
    *,
    context: Context,
    why_now: WhyNow,
    problem_statement: str,
    current_solution: str,
    gap: str,
    desired_outcome: str,
    evidence_refs: Sequence[str],
    confidence: float,
    provenance: str,
) -> BusinessProblem:
    """Construct a canonical problem without inventing evidence or scope."""
    if context.signal_id != why_now.signal_id:
        raise ValueError("context and Why Now signal identity must match")
    refs = tuple(sorted(set(ref.strip() for ref in evidence_refs if ref.strip())))
    if not refs:
        raise ValueError("business problem requires evidence references")
    return BusinessProblem(
        id=_id((context.id, why_now.id, problem_statement)),
        signal_id=context.signal_id,
        context_id=context.id,
        why_now_id=why_now.id,
        context_version=context.context_version,
        why_now_version=why_now.assessment_version,
        problem_statement=problem_statement,
        current_solution=current_solution,
        gap=gap,
        desired_outcome=desired_outcome,
        evidence_refs=refs,
        confidence=confidence,
        provenance=provenance,
        account_id=context.account_id,
    )
