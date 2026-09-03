"""Executable Gate 1: Validation Authorization.

Gate 1 is deterministic governance code. It does not make LLM decisions.
Agents may prepare inputs; NOVA CORP retains authority at configured risk gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from factory.schemas.domain import Decision, Opportunity, OpportunityScore, ValidationExperiment


@dataclass(frozen=True)
class Gate1Policy:
    """Explicit, versionable Gate 1 policy parameters."""

    policy_version: str = "gate1-v0.1"
    minimum_evidence_count: int = 1
    minimum_score: Optional[float] = None
    maximum_auto_budget: float = 0.0
    maximum_risk_score: float = 30.0
    require_human_for_external_commitment: bool = True
    require_human_for_sensitive_data: bool = True


@dataclass(frozen=True)
class Gate1Context:
    """Explicit risk/side-effect facts supplied to the gate."""

    risk_score: float = 0.0
    external_commitment: bool = False
    sensitive_data: bool = False
    human_approval: Optional[bool] = None


@dataclass(frozen=True)
class Gate1Evaluation:
    """Decision plus machine-readable governance state."""

    decision: Decision
    requires_human_approval: bool
    reasons: tuple[str, ...]
    policy_version: str


def evaluate_gate1(
    opportunity: Opportunity,
    score: OpportunityScore,
    experiment: ValidationExperiment,
    *,
    context: Gate1Context | None = None,
    policy: Gate1Policy | None = None,
) -> Gate1Evaluation:
    """Evaluate whether a validation experiment may proceed.

    Missing mandatory evidence or material risk/side effects stop autonomous
    execution. Human approval is explicit; silence never counts as approval.
    An explicit human rejection always records REJECT because it is an
    authoritative governance action, regardless of other gate conditions.
    """
    policy = policy or Gate1Policy()
    context = context or Gate1Context()

    if score.opportunity_id != opportunity.id:
        raise ValueError("score.opportunity_id must match opportunity.id")
    if experiment.opportunity_id != opportunity.id:
        raise ValueError("experiment.opportunity_id must match opportunity.id")
    if experiment.budget_limit < 0:
        raise ValueError("experiment budget must be non-negative")
    if context.risk_score < 0 or context.risk_score > 100:
        raise ValueError("risk_score must be between 0 and 100")
    if policy.minimum_evidence_count < 0:
        raise ValueError("minimum_evidence_count must be non-negative")
    if policy.maximum_auto_budget < 0:
        raise ValueError("maximum_auto_budget must be non-negative")
    if policy.minimum_score is not None and not 0 <= policy.minimum_score <= 100:
        raise ValueError("minimum_score must be between 0 and 100")

    reasons: list[str] = []
    evidence_count = len(opportunity.evidence_ids)
    if evidence_count < policy.minimum_evidence_count:
        reasons.append("insufficient_evidence")

    if policy.minimum_score is not None and score.weighted_score < policy.minimum_score:
        reasons.append("score_below_minimum")

    material_budget = experiment.budget_limit > policy.maximum_auto_budget
    elevated_risk = context.risk_score > policy.maximum_risk_score
    external_commitment = context.external_commitment and policy.require_human_for_external_commitment
    sensitive_data = context.sensitive_data and policy.require_human_for_sensitive_data

    if material_budget:
        reasons.append("material_spend_requires_approval")
    if elevated_risk:
        reasons.append("elevated_risk_requires_approval")
    if external_commitment:
        reasons.append("external_commitment_requires_approval")
    if sensitive_data:
        reasons.append("sensitive_data_requires_approval")

    approval_required = material_budget or elevated_risk or external_commitment or sensitive_data
    hard_block = "insufficient_evidence" in reasons or "score_below_minimum" in reasons

    if context.human_approval is False:
        outcome = "REJECT"
        decided_by = "NOVA_CORP"
        reasons.append("explicit_human_rejection")
    elif hard_block:
        outcome = "HOLD"
        decided_by = "NOVA_GATE1_POLICY"
    elif approval_required and context.human_approval is not True:
        outcome = "HOLD"
        decided_by = "NOVA_GATE1_POLICY"
    else:
        outcome = "APPROVE"
        decided_by = "NOVA_CORP" if approval_required else "NOVA_GATE1_POLICY"

    decision = Decision(
        id=f"gate1:{opportunity.id}:{experiment.id}:{policy.policy_version}",
        subject_id=opportunity.id,
        gate="GATE_1_VALIDATION_AUTHORIZATION",
        outcome=outcome,
        rationale=";".join(reasons) if reasons else "validation_meets_configured_gate1_policy",
        decided_by=decided_by,
        evidence_ids=tuple(opportunity.evidence_ids),
        timestamp="DETERMINISTIC",
    )

    return Gate1Evaluation(
        decision=decision,
        requires_human_approval=approval_required,
        reasons=tuple(reasons),
        policy_version=policy.policy_version,
    )
