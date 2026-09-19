"""Evidence-backed decision gate for validation outcomes."""
from __future__ import annotations
from factory.schemas.domain import Decision, ValidationExperiment

def decide_validation(*, experiment: ValidationExperiment, decided_by: str) -> Decision:
    if experiment.status not in {"passed", "failed", "inconclusive"}:
        raise ValueError("validation experiment must have a terminal result")
    if not experiment.result_evidence_ids:
        raise ValueError("decision requires validation result evidence")
    if not decided_by.strip():
        raise ValueError("decided_by must be non-empty")
    outcome = {"passed": "proceed_to_build_review", "failed": "kill_or_reframe", "inconclusive": "hold_and_retest"}[experiment.status]
    return Decision(
        id=f"dec_{experiment.id}",
        subject_id=experiment.opportunity_id,
        gate="validation",
        outcome=outcome,
        rationale=experiment.result,
        decided_by=decided_by,
        evidence_ids=experiment.result_evidence_ids,
        timestamp="",
    )
