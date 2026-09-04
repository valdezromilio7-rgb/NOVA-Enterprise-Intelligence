import unittest

from factory.agents.registry import AgentDefinition, AgentRegistry, AgentStatus
from factory.execution.audit import AuditTrail
from factory.execution.contracts import ExecutionStatus
from factory.orchestration.orchestrator import GovernedOrchestrator
from factory.workflow.engine import WorkflowDefinition, WorkflowEngine, WorkflowStatus, WorkflowStep


class WorkflowEngineTests(unittest.TestCase):
    def setUp(self):
        agent = AgentDefinition(
            agent_id="agent.research",
            name="Research Agent",
            version="1.0.0",
            role="research",
            description="Bounded research executor",
            allowed_tasks=("research",),
            evaluation_suite=("research-v0.1",),
            status=AgentStatus.ACTIVE,
        )
        self.audit = AuditTrail()
        self.registry = AgentRegistry([agent])
        self.orchestrator = GovernedOrchestrator(
            self.registry,
            self.audit,
            executors={"research": lambda contract: (f"artifact:{contract.execution_id}",)},
        )
        self.engine = WorkflowEngine(self.orchestrator)

    def test_workflow_runs_all_steps_in_order(self):
        workflow = WorkflowDefinition(
            workflow_id="wf.discovery",
            version="0.1.0",
            steps=(
                WorkflowStep("research-1", "agent.research", "1.0.0", "research", "research-output"),
                WorkflowStep("research-2", "agent.research", "1.0.0", "research", "research-output"),
            ),
        )
        result = self.engine.run(workflow)
        self.assertEqual(result.status, WorkflowStatus.SUCCEEDED)
        self.assertEqual([r.step_id for r in result.step_results], ["research-1", "research-2"])
        self.assertTrue(all(r.status == ExecutionStatus.SUCCEEDED for r in result.step_results))

    def test_workflow_stops_after_failed_step(self):
        workflow = WorkflowDefinition(
            workflow_id="wf.failure",
            version="0.1.0",
            steps=(
                WorkflowStep("allowed", "agent.research", "1.0.0", "research", "research-output"),
                WorkflowStep("blocked", "agent.research", "1.0.0", "forbidden", "research-output"),
                WorkflowStep("never", "agent.research", "1.0.0", "research", "research-output"),
            ),
        )
        result = self.engine.run(workflow)
        self.assertEqual(result.status, WorkflowStatus.FAILED)
        self.assertEqual(len(result.step_results), 2)
        self.assertEqual(result.step_results[1].status, ExecutionStatus.REJECTED)

    def test_definition_id_is_deterministic(self):
        step = WorkflowStep("research", "agent.research", "1.0.0", "research", "research-output")
        first = WorkflowDefinition("wf.same", "0.1.0", (step,))
        second = WorkflowDefinition("wf.same", "0.1.0", (step,))
        self.assertEqual(first.definition_id, second.definition_id)

    def test_duplicate_step_ids_are_rejected(self):
        step = WorkflowStep("same", "agent.research", "1.0.0", "research", "research-output")
        with self.assertRaises(ValueError):
            WorkflowDefinition("wf.duplicate", "0.1.0", (step, step))


if __name__ == "__main__":
    unittest.main()
