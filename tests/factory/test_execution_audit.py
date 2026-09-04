import unittest

from factory.execution.audit import AuditTrail
from factory.execution.contracts import AuditEvent, ExecutionStatus


class AuditTrailTests(unittest.TestCase):
    def _event(self, status=ExecutionStatus.STARTED, event_type="execution.started"):
        return AuditEvent(
            event_type=event_type,
            execution_id="exec-001",
            agent_id="research-001",
            agent_version="1.0.0",
            status=status,
            timestamp="2026-09-04T12:00:00Z",
        )

    def test_append_and_filter_by_execution(self):
        trail = AuditTrail()
        trail.append(self._event())
        self.assertEqual(len(trail.list()), 1)
        self.assertEqual(len(trail.for_execution("exec-001")), 1)
        self.assertEqual(trail.for_execution("exec-999"), ())

    def test_duplicate_event_is_rejected(self):
        event = self._event()
        trail = AuditTrail((event,))
        with self.assertRaises(ValueError):
            trail.append(event)

    def test_empty_execution_filter_is_rejected(self):
        with self.assertRaises(ValueError):
            AuditTrail().for_execution("")


if __name__ == "__main__":
    unittest.main()
