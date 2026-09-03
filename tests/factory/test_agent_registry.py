import unittest

from factory.agents.registry import (
    AgentDefinition,
    AgentRegistry,
    AgentStatus,
    TaskAuthorization,
)


class AgentRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engineer = AgentDefinition(
            agent_id="engineering.001",
            name="NOVA Engineering Agent",
            version="0.1.0",
            role="engineering",
            description="Implements bounded approved technical tasks.",
            allowed_tasks=("implement", "refactor"),
            forbidden_tasks=("approve_spend", "release_production"),
            input_contracts=("product_spec.v1",),
            output_contracts=("code_change.v1",),
            tools=("github.read", "github.write"),
            data_access=("internal",),
            write_access=("repo:factory",),
            financial_limit=0.0,
            execution_limit=3,
            escalation_rules=("scope_exceeded", "repeated_failure"),
            evaluation_suite=("engineering.smoke.v1",),
            status=AgentStatus.ACTIVE,
        )

    def test_register_and_get(self) -> None:
        registry = AgentRegistry([self.engineer])
        self.assertEqual(registry.get("engineering.001"), self.engineer)

    def test_duplicate_agent_is_rejected(self) -> None:
        registry = AgentRegistry([self.engineer])
        with self.assertRaises(ValueError):
            registry.register(self.engineer)

    def test_active_agent_can_authorize_bounded_task(self) -> None:
        registry = AgentRegistry([self.engineer])
        result = registry.authorize(
            "engineering.001",
            TaskAuthorization(
                task_type="implement",
                required_tools=("github.write",),
                required_data_access=("internal",),
                required_write_access=("repo:factory",),
            ),
        )
        self.assertTrue(result.authorized)
        self.assertEqual(result.reasons, ())

    def test_forbidden_task_is_denied(self) -> None:
        registry = AgentRegistry([self.engineer])
        result = registry.authorize(
            "engineering.001",
            TaskAuthorization(task_type="approve_spend"),
        )
        self.assertFalse(result.authorized)
        self.assertIn("task_forbidden", result.reasons)

    def test_missing_tool_and_write_access_are_denied(self) -> None:
        registry = AgentRegistry([self.engineer])
        result = registry.authorize(
            "engineering.001",
            TaskAuthorization(
                task_type="implement",
                required_tools=("deploy.production",),
                required_write_access=("production",),
            ),
        )
        self.assertFalse(result.authorized)
        self.assertIn("required_tool_not_granted", result.reasons)
        self.assertIn("required_write_access_not_granted", result.reasons)

    def test_financial_limit_is_enforced(self) -> None:
        registry = AgentRegistry([self.engineer])
        result = registry.authorize(
            "engineering.001",
            TaskAuthorization(task_type="implement", budget_exposure=0.01),
        )
        self.assertFalse(result.authorized)
        self.assertIn("financial_limit_exceeded", result.reasons)

    def test_non_active_agent_cannot_execute(self) -> None:
        draft = AgentDefinition(
            agent_id="research.001",
            name="NOVA Research Agent",
            version="0.1.0",
            role="research",
            description="Researches bounded questions.",
            allowed_tasks=("research",),
            evaluation_suite=(),
            status=AgentStatus.DRAFT,
        )
        registry = AgentRegistry([draft])
        result = registry.authorize(
            "research.001", TaskAuthorization(task_type="research")
        )
        self.assertFalse(result.authorized)
        self.assertIn("agent_status_draft", result.reasons)

    def test_approved_agent_requires_evaluation_suite(self) -> None:
        with self.assertRaises(ValueError):
            AgentDefinition(
                agent_id="bad.001",
                name="Bad Agent",
                version="0.1.0",
                role="research",
                description="Invalid approved agent.",
                status=AgentStatus.APPROVED,
            )


if __name__ == "__main__":
    unittest.main()
