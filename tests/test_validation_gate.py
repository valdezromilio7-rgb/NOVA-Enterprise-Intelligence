import pytest
from factory.schemas.domain import Opportunity, OpportunityScore
from factory.validation.gate import authorize_validation

def test_validation_gate_accepts_evidence_backed_opportunity():
    opportunity = Opportunity(id="opp_001", title="Evidence-backed opportunity", problem="Problem", target_customer="Users", evidence_ids=("ev_001",))
    score = OpportunityScore(opportunity_id="opp_001", dimensions={"evidence": 80.0}, weighted_score=80.0, confidence=0.8, rationale="explicit evidence", scoring_version="v0.1")
    authorize_validation(opportunity=opportunity, score=score)

def test_validation_gate_rejects_missing_evidence():
    opportunity = Opportunity(id="opp_002", title="No evidence", problem="Problem", target_customer="Users")
    score = OpportunityScore(opportunity_id="opp_002", dimensions={"evidence": 50.0}, weighted_score=50.0, confidence=0.8, rationale="", scoring_version="v0.1")
    with pytest.raises(ValueError, match="canonical evidence"):
        authorize_validation(opportunity=opportunity, score=score)

def test_validation_gate_rejects_low_confidence():
    opportunity = Opportunity(id="opp_003", title="Low confidence", problem="Problem", target_customer="Users", evidence_ids=("ev_003",))
    score = OpportunityScore(opportunity_id="opp_003", dimensions={"evidence": 50.0}, weighted_score=50.0, confidence=0.2, rationale="", scoring_version="v0.1")
    with pytest.raises(ValueError, match="sufficient scoring confidence"):
        authorize_validation(opportunity=opportunity, score=score)
