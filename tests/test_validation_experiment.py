from factory.schemas.domain import Opportunity
from factory.validation.experiment import create_experiment, record_result

def test_validation_experiment_is_traceable():
    o=Opportunity(id="opp_v",title="Test",problem="Problem",target_customer="Users",evidence_ids=("ev_1",))
    e=create_experiment(opportunity=o,hypothesis="Users will pay",method="landing-page test",success_metric="3 paid users",failure_threshold="0 paid users",budget_limit=10)
    assert e.account_id is None
    done=record_result(e,result="3 paid users",result_evidence_ids=("ev_result",),status="passed")
    assert done.status=="passed"
    assert done.result_evidence_ids==("ev_result",)
