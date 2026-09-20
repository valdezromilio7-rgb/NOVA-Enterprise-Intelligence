from factory.agent_execution import BuildTask
from factory.agent_task_execution import TaskStatus, authorize_task, complete_task

def test_task_execution_is_auditable():
    t=BuildTask("task_1","spec_1","engineering","Implement","PR")
    e=authorize_task(t,actor="agent-engineering")
    assert e.status is TaskStatus.AUTHORIZED
    done=complete_task(e,output_ref="pr:#1")
    assert done.status is TaskStatus.SUCCEEDED
    assert done.output_ref=="pr:#1"
