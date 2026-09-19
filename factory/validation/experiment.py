"""Validation experiment lifecycle helpers."""
from __future__ import annotations
from hashlib import sha256
from factory.schemas.domain import Opportunity, ValidationExperiment

def create_experiment(*, opportunity: Opportunity, hypothesis: str, method: str, success_metric: str, failure_threshold: str, budget_limit: float) -> ValidationExperiment:
    if not opportunity.evidence_ids: raise ValueError("validation experiment requires canonical evidence IDs")
    if budget_limit < 0: raise ValueError("budget_limit must be non-negative")
    key="|".join((opportunity.id,hypothesis,method,success_metric,failure_threshold))
    return ValidationExperiment(id="exp_"+sha256(key.encode()).hexdigest()[:24],opportunity_id=opportunity.id,hypothesis=hypothesis,method=method,success_metric=success_metric,failure_threshold=failure_threshold,budget_limit=budget_limit,status="planned",account_id=opportunity.account_id)

def record_result(experiment: ValidationExperiment, *, result: str, result_evidence_ids: tuple[str,...], status: str) -> ValidationExperiment:
    if status not in {"passed","failed","inconclusive"}: raise ValueError("invalid validation result status")
    refs=tuple(sorted(set(x.strip() for x in result_evidence_ids if x.strip())))
    if not refs: raise ValueError("validation result requires evidence IDs")
    return ValidationExperiment(**{**experiment.__dict__,"status":status,"result":result,"result_evidence_ids":refs})
