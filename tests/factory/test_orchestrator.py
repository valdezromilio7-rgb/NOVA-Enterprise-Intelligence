import unittest

from factory.agents.registry import AgentDefinition, AgentRegistry, AgentStatus
from factory.execution.audit import AuditTrail
from factory.execution.contracts import ExecutionContract, ExecutionStatus
from factory.orchestration.orchestrator import GovernedOrchestrator


class GovernedOrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = AgentRegistry(
            [
                AgentDefinition(
                    agent_id="agent.research",
                    name="Research Agent",
                    version="1.0.0",
                    role="research",
                    description="Bounded research worker",
                    allowed_tasks=("research",),
                    tools=("search",),
                    evaluation_suite=("research-v1",),
                    status=AgentStatus.ACTIVE,
                )
            ]
        )
        self.audit = AuditTrail()

    def contract(self, **overrides):
        values = {
            "execution_id": "exec-001",
            "agent_id": "agent.research",
            "agent_version": "1.0.0",
            "task_type": "research",
            "input_refs": ("signal:001",),
            "output_contract": "research-result-v1",
            "required_tools": ("search",),
        }
        values.update(overrides)
        return ExecutionContract(**values)

    def test_authorized_execution_succeeds_and_is_audited(self):
        orchestrator = GovernedOrchestrator(
            self.registry,
            self.audit,
            {"research": lambda contract: ("artifact:001",)},
        )
        result = orchestrator.submit(self.contract())
        self.assertEqual(result.status, ExecutionStatus.SUCCEEDED)
        self.assertTrue(result.authorized)
        self.assertEqual(result.output_refs, ("artifact:001",))
        self.assertEqual(
            [event.status for event in self.audit.for_execution("exec-001")],
            [ExecutionStatus.AUTHORIZED, ExecutionStatus.STARTED, ExecutionStatus.SUCCEEDED],
        )

    def test_unauthorized_task_is_rejected_before_execution(self):
        called = False

        def executor(contract):
            nonlocal called
            called = True
            return ("artifact:should-not-exist",)

        orchestrator = GovernedOrchestrator(self.registry, self.audit, {"other": executor})
        result = orchestrator.submit(self.contract(task_type="other"))
        self.assertEqual(result.status, ExecutionStatus.REJECTED)
        self.assertFalse(called)
        self.assertEqual(result.reasons, ("task_not_allowed",))

    def test_missing_executor_is_controlled_failure(self):
        orchestrator = GovernedOrchestrator(self.registry, self.audit)
        result = orchestrator.submit(self.contract())
        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertEqual(result.reasons, ("executor_not_registered",))
        self.assertEqual(len(self.audit.for_execution("exec-001")), 2)

    def test_executor_failure_is_audited_without_exposing_exception_text(self):
        def executor(contract):
            raise RuntimeError("secret internal detail")

        orchestrator = GovernedOrchestrator(self.registry, self.audit, {"research": executor})
        result = orchestrator.submit(self.contract())
        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertEqual(result.reasons, ("executor_error:RuntimeError",))
        failure = self.audit.for_execution("exec-001")[-1]
        self.assertEqual(failure.error_code, "executor_error:RuntimeError")
        self.assertNotIn("secret internal detail", failure.error_code)


if __name__ == "__main__":
    unittest.main()
