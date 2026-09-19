from factory.schemas.domain import Opportunity, Decision
from factory.product_specification import create_product_specification

def test_spec_requires_passed_validation_decision():
    o=Opportunity(id="opp_s",title="Test",problem="Problem",target_customer="Users",evidence_ids=("ev",))
    d=Decision(id="dec",subject_id="opp_s",gate="validation",outcome="proceed_to_build_review",rationale="validated",decided_by="NOVA",evidence_ids=("ev_r",),timestamp="now")
    s=create_product_specification(opportunity=o,decision=d,value_proposition="Value",scope=("MVP",),acceptance_criteria=("works",),analytics_requirements=("events",),architecture_requirements=("provider-neutral",))
    assert s.opportunity_id=="opp_s"
    assert s.provenance_decision_id=="dec"
