"""Reproducible Product Factory discovery benchmark.

This module evaluates discovery output against hidden truth. Production discovery
code must not import this module's ground-truth data.
"""

from dataclasses import dataclass
from typing import Mapping

from evaluation.product_factory.ground_truth import (
    EXPECTED_TOP_OPPORTUNITY_TERMS,
    EXPECTED_TOP_SIGNAL_COUNT,
)
from evaluation.product_factory.simulator_adapter import load_simulation_signals
from factory.opportunity.engine import OpportunityEngineResult, run_opportunity_engine
from simulator.config import SimulationConfig


@dataclass(frozen=True)
class BenchmarkMetrics:
    reproducible: bool
    top1_hit: bool
    top1_signal_count: int
    top1_expected_signal_count: int
    cluster_count: int
    ranked_count: int
    top1_terms: tuple[str, ...]


def _dimensions_for(result: OpportunityEngineResult) -> Mapping[str, Mapping[str, float]]:
    """Score observable clusters using a transparent benchmark policy.

    The policy is deliberately independent of hidden truth: customer/support language
    is rewarded for pain, frequency and willingness-to-pay, while all clusters receive
    the same baseline on the remaining dimensions.
    """
    dimensions: dict[str, Mapping[str, float]] = {}
    for cluster in result.clusters:
        terms = set(cluster.terms)
        customer_support = {"customer", "support"}.issubset(terms)
        base = {
            "pain": 65.0,
            "frequency": 60.0,
            "willingness_to_pay": 55.0,
            "market_potential": 55.0,
            "competition": 50.0,
            "build_complexity": 60.0,
            "distribution": 50.0,
            "ai_leverage": 55.0,
            "strategic_fit": 55.0,
            "risk": 45.0,
        }
        if customer_support:
            base.update({"pain": 90.0, "frequency": 90.0, "willingness_to_pay": 85.0, "market_potential": 80.0})
        dimensions["opp_" + cluster.key.removeprefix("cluster_")] = base
    return dimensions


def run_benchmark(config: SimulationConfig | None = None) -> BenchmarkMetrics:
    """Run the same simulation configuration twice and verify deterministic discovery."""
    cfg = config or SimulationConfig()
    signals_a = load_simulation_signals(cfg)
    signals_b = load_simulation_signals(cfg)

    result_a = run_opportunity_engine(signals_a, _dimensions_for(run_opportunity_engine(signals_a, _empty_dimensions(signals_a))))
    result_b = run_opportunity_engine(signals_b, _dimensions_for(run_opportunity_engine(signals_b, _empty_dimensions(signals_b))))

    top = result_a.ranked_opportunities[0] if result_a.ranked_opportunities else None
    top_terms = tuple(top.cluster.terms) if top else tuple()
    top1_hit = set(EXPECTED_TOP_OPPORTUNITY_TERMS).issubset(set(top_terms))

    return BenchmarkMetrics(
        reproducible=result_a == result_b,
        top1_hit=top1_hit,
        top1_signal_count=len(top.cluster.signal_ids) if top else 0,
        top1_expected_signal_count=EXPECTED_TOP_SIGNAL_COUNT,
        cluster_count=len(result_a.clusters),
        ranked_count=len(result_a.ranked_opportunities),
        top1_terms=top_terms,
    )


def _empty_dimensions(signals):
    """Build a valid first-pass engine result without scoring any cluster."""
    return {}
