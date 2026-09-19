"""Canonical product specification derived from an approved build review."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from typing import Sequence
from factory.schemas.domain import Decision, Opportunity

@dataclass(frozen=True)
class ProductSpecification:
    id: str
    opportunity_id: str
    problem: str
    target_customer: str
    value_proposition: str
    scope: Sequence[str]
    acceptance_criteria: Sequence[str]
    analytics_requirements: Sequence[str]
    architecture_requirements: Sequence[str]
    provenance_decision_id: str
    account_id: str | None = None

def create_product_specification(*, opportunity: Opportunity, decision: Decision, value_proposition: str, scope: Sequence[str], acceptance_criteria: Sequence[str], analytics_requirements: Sequence[str], architecture_requirements: Sequence[str]) -> ProductSpecification:
    if decision.subject_id != opportunity.id or decision.gate != "validation" or decision.outcome != "proceed_to_build_review":
        raise ValueError("product specification requires a passed validation decision")
    if not decision.evidence_ids:
        raise ValueError("build review requires decision evidence")
    values=(opportunity.id,value_proposition,*scope,*acceptance_criteria,*analytics_requirements,*architecture_requirements,decision.id)
    spec_id="spec_"+sha256("|".join(values).encode()).hexdigest()[:24]
    return ProductSpecification(id=spec_id,opportunity_id=opportunity.id,problem=opportunity.problem,target_customer=opportunity.target_customer,value_proposition=value_proposition,scope=tuple(scope),acceptance_criteria=tuple(acceptance_criteria),analytics_requirements=tuple(analytics_requirements),architecture_requirements=tuple(architecture_requirements),provenance_decision_id=decision.id,account_id=opportunity.account_id)
