from factory.schemas.domain import Opportunity
from factory.validation.experiment import create_experiment, record_result
from factory.validation.decision import decide_validation

def test_validation_decision_is_evidence_backed():
    o=Opportunity(id="opp_d",title="Test",problem="Problem",target_customer="Users",evidence_ids=("ev_1",))
    e=create_experiment(opportunity=o,hypothesis="Users pay",method="offer",success_metric="1 paid",failure_threshold="0 paid",budget_limit=10)
    e=record_result(e,result="1 paid",result_evidence_ids=("ev_r",),status="passed")
    d=decide_validation(experiment=e,decided_by="NOVA")
    assert d.subject_id=="opp_d"
    assert d.outcome=="proceed_to_build_review"
    assert d.evidence_ids==("ev_r",)

def test_inconclusive_holds():
    o=Opportunity(id="opp_h",title="Test",problem="Problem",target_customer="Users",evidence_ids=("ev_1",))
    e=create_experiment(opportunity=o,hypothesis="Users pay",method="offer",success_metric="1 paid",failure_threshold="0 paid",budget_limit=10)
    e=record_result(e,result="No decisive signal",result_evidence_ids=("ev_r",),status="inconclusive")
    assert decide_validation(experiment=e,decided_by="NOVA").outcome=="hold_and_retest"
