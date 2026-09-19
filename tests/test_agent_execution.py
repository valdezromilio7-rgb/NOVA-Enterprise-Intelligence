from factory.agent_execution import BuildTask, create_build_plan
from factory.product_specification import ProductSpecification

def test_build_plan_is_bounded():
    s=ProductSpecification("spec_1","opp_1","problem","users","value",("mvp",),("works",),("events",),("provider-neutral",),"dec_1")
    p=create_build_plan(specification=s,tasks=(BuildTask("task_1","spec_1","engineering","Implement MVP","PR"),))
    assert p.approval_required is True
    assert p.tasks[0].specification_id=="spec_1"
