import unittest

from evaluation.product_factory.signals import BENCHMARK_SIGNALS
from factory.opportunity.cluster import cluster_signals
from factory.opportunity.engine import run_opportunity_engine
from factory.opportunity.normalize import normalize_signals
from factory.opportunity.score import DEFAULT_WEIGHTS
from factory.schemas.domain import Opportunity


class OpportunityEngineTests(unittest.TestCase):
    def test_normalization_is_deterministic(self):
        first = normalize_signals(BENCHMARK_SIGNALS)
        second = normalize_signals(BENCHMARK_SIGNALS)
        self.assertEqual(first, second)
        self.assertEqual(len(first), len(set(signal.id for signal in first)))

    def test_customer_support_signals_cluster(self):
        normalized = normalize_signals(BENCHMARK_SIGNALS)
        clusters = cluster_signals(normalized)
        support_cluster = next(
            cluster for cluster in clusters if "support" in cluster.terms
        )
        self.assertEqual(len(support_cluster.signal_ids), 3)

    def test_engine_ranks_highest_scored_opportunity_first(self):
        def builder(cluster):
            return Opportunity(
                id=cluster.key,
                title=cluster.key,
                problem="benchmark problem",
                target_customer="benchmark customer",
                evidence_ids=cluster.signal_ids,
                metadata={"terms": cluster.terms},
            )

        normalized = normalize_signals(BENCHMARK_SIGNALS)
        clusters = cluster_signals(normalized)
        dimensions = {}
        for cluster in clusters:
            score = {name: 40.0 for name in DEFAULT_WEIGHTS}
            if "support" in cluster.terms:
                score.update({
                    "pain": 95.0,
                    "frequency": 90.0,
                    "willingness_to_pay": 85.0,
                    "market_potential": 80.0,
                    "distribution": 85.0,
                })
            dimensions[cluster.key] = score

        result = run_opportunity_engine(
            BENCHMARK_SIGNALS,
            dimensions,
            opportunity_builder=builder,
            confidence_by_opportunity={cluster.key: 0.8 for cluster in clusters},
        )
        self.assertTrue(result.ranked_opportunities)
        self.assertIn(
            "support", result.ranked_opportunities[0].cluster.terms
        )


if __name__ == "__main__":
    unittest.main()
