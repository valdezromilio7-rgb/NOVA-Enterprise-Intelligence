import unittest

from factory.workflow.state import FailureAction, FailurePolicy, WorkflowRunState, WorkflowState


class WorkflowRunStateTests(unittest.TestCase):
    def test_lifecycle_is_deterministic(self):
        run = WorkflowRunState("wf-1", "v0.1")
        self.assertEqual(run.state, WorkflowState.PLANNED)
        run.start()
        run.mark_step_succeeded("step-1")
        run.finish()
        self.assertEqual(run.state, WorkflowState.SUCCEEDED)
        self.assertEqual(run.completed_step_ids, ["step-1"])

    def test_step_failure_stops_by_default(self):
        run = WorkflowRunState("wf-1", "v0.1")
        run.start()
        run.mark_failed("step-2", "EXECUTOR_ERROR", FailurePolicy())
        self.assertEqual(run.state, WorkflowState.FAILED)
        self.assertEqual(run.failure_code, "EXECUTOR_ERROR")

    def test_authorization_failure_blocks_by_default(self):
        run = WorkflowRunState("wf-1", "v0.1")
        run.start()
        run.mark_authorization_blocked("step-2", FailurePolicy())
        self.assertEqual(run.state, WorkflowState.BLOCKED)
        self.assertEqual(run.failure_code, "AUTHORIZATION_DENIED")

    def test_custom_cancel_policy_is_explicit(self):
        run = WorkflowRunState("wf-1", "v0.1")
        run.start()
        policy = FailurePolicy(on_step_failure=FailureAction.CANCEL)
        run.mark_failed("step-2", "TIMEOUT", policy)
        self.assertEqual(run.state, WorkflowState.CANCELLED)

    def test_invalid_transitions_are_rejected(self):
        run = WorkflowRunState("wf-1", "v0.1")
        with self.assertRaises(ValueError):
            run.finish()
        run.start()
        run.mark_step_succeeded("step-1")
        with self.assertRaises(ValueError):
            run.mark_step_succeeded("step-1")

    def test_empty_failure_code_is_rejected(self):
        run = WorkflowRunState("wf-1", "v0.1")
        run.start()
        with self.assertRaises(ValueError):
            run.mark_failed("step-1", " ", FailurePolicy())


if __name__ == "__main__":
    unittest.main()
