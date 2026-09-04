import unittest

from factory.agents.registry import AgentDefinition, AgentRegistry, AgentStatus
from factory.execution.contracts import (
    AuditEvent,
    ExecutionContract,
    ExecutionStatus,
    authorize_execution,
)


class ExecutionContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = AgentDefinition(
            agent_id="research-001",
            name="Research Agent",
            version="1.0.0",
            role="research",
            description="Produces evidence-backed market research.",
            allowed_tasks=("market_research",),
            tools=("web_search",),
            data_access=("public",),
            evaluation_suite=("research-basic",),
            status=AgentStatus.ACTIVE,
        )
        self.registry = AgentRegistry((self.agent,))

    def _contract(self, **overrides):
        values = {
            "execution_id": "exec-001",
            "agent_id": "research-001",
            "agent_version": "1.0.0",
            "task_type": "market_research",
            "input_refs": ("opportunity:001",),
            "output_contract": "market-research-v0.1",
            "required_tools": ("web_search",),
            "required_data_access": ("public",),
        }
        values.update(overrides)
        return ExecutionContract(**values)

    def test_authorized_contract_passes_registry(self):
        result = authorize_execution(self._contract(), self.registry)
        self.assertTrue(result.authorized)
        self.assertEqual(result.reasons, ())

    def test_unknown_capability_is_rejected(self):
        result = authorize_execution(
            self._contract(task_type="deploy_to_production"), self.registry
        )
        self.assertFalse(result.authorized)
        self.assertIn("task_not_allowed", result.reasons)

    def test_agent_version_mismatch_is_rejected(self):
        result = authorize_execution(
            self._contract(agent_version="2.0.0"), self.registry
        )
        self.assertFalse(result.authorized)
        self.assertIn("agent_version_mismatch", result.reasons)

    def test_audit_event_id_is_deterministic(self):
        first = AuditEvent(
            event_type="execution.completed",
            execution_id="exec-001",
            agent_id="research-001",
            agent_version="1.0.0",
            status=ExecutionStatus.SUCCEEDED,
            timestamp="2026-09-04T12:00:00Z",
            input_refs=("opportunity:001",),
            output_refs=("artifact:001",),
        )
        second = AuditEvent(
            event_type="execution.completed",
            execution_id="exec-001",
            agent_id="research-001",
            agent_version="1.0.0",
            status=ExecutionStatus.SUCCEEDED,
            timestamp="2026-09-04T12:00:00Z",
            input_refs=("opportunity:001",),
            output_refs=("artifact:001",),
        )
        self.assertEqual(first.event_id, second.event_id)

    def test_failed_audit_event_requires_error_code(self):
        with self.assertRaises(ValueError):
            AuditEvent(
                event_type="execution.failed",
                execution_id="exec-001",
                agent_id="research-001",
                agent_version="1.0.0",
                status=ExecutionStatus.FAILED,
                timestamp="2026-09-04T12:00:00Z",
            )


if __name__ == "__main__":
    unittest.main()
