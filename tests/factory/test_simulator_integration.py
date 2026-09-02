import unittest

from evaluation.product_factory.simulator_adapter import load_simulation_signals
from evaluation.product_factory.benchmark import run_benchmark
from simulator.config import SimulationConfig


class SimulatorIntegrationTests(unittest.TestCase):
    def test_adapter_is_deterministic_and_preserves_signal_count(self):
        config = SimulationConfig(seed=2026001)
        first = load_simulation_signals(config)
        second = load_simulation_signals(config)

        self.assertEqual(first, second)
        self.assertEqual(len(first), 6)
        self.assertTrue(all(signal.metadata["simulation_seed"] == 2026001 for signal in first))

    def test_benchmark_is_reproducible_and_finds_expected_top_cluster(self):
        metrics = run_benchmark(SimulationConfig(seed=2026001))

        self.assertTrue(metrics.reproducible)
        self.assertTrue(metrics.top1_hit)
        self.assertEqual(metrics.top1_signal_count, metrics.top1_expected_signal_count)
        self.assertGreaterEqual(metrics.cluster_count, 1)
        self.assertEqual(metrics.cluster_count, metrics.ranked_count)


if __name__ == "__main__":
    unittest.main()
