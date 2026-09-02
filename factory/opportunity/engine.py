"""End-to-end deterministic Opportunity Engine pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Mapping

from factory.opportunity.cluster import SignalCluster, cluster_signals
from factory.opportunity.normalize import normalize_signals
from factory.opportunity.score import score_opportunity
from factory.schemas.domain import Opportunity, OpportunityScore, OpportunityState, Signal


@dataclass(frozen=True)
class RankedOpportunity:
    opportunity: Opportunity
    score: OpportunityScore
    cluster: SignalCluster


@dataclass(frozen=True)
class OpportunityEngineResult:
    signals: tuple[Signal, ...]
    clusters: tuple[SignalCluster, ...]
    ranked_opportunities: tuple[RankedOpportunity, ...]


def _default_opportunity(cluster: SignalCluster) -> Opportunity:
    title = "Opportunity: " + (cluster.terms[0] if cluster.terms else cluster.key)
    return Opportunity(
        id="opp_" + cluster.key.removeprefix("cluster_"),
        title=title,
        problem="Signals indicate a recurring issue or unmet need; validation is required.",
        target_customer="Unknown — determine during validation.",
        state=OpportunityState.DISCOVERY,
        evidence_ids=cluster.signal_ids,
        assumptions=("The clustered signals represent the same underlying problem.",),
        metadata={"cluster_key": cluster.key, "terms": cluster.terms},
    )


def run_opportunity_engine(
    signals: Iterable[Signal],
    dimensions_by_opportunity: Mapping[str, Mapping[str, float]],
    *,
    opportunity_builder: Callable[[SignalCluster], Opportunity] | None = None,
    confidence_by_opportunity: Mapping[str, float] | None = None,
) -> OpportunityEngineResult:
    """Normalize, cluster, construct, score, and rank opportunities deterministically."""
    normalized = tuple(normalize_signals(signals))
    clusters = tuple(cluster_signals(normalized))
    builder = opportunity_builder or _default_opportunity
    confidence = confidence_by_opportunity or {}
    ranked: list[RankedOpportunity] = []

    for cluster in clusters:
        opportunity = builder(cluster)
        dimensions = dimensions_by_opportunity.get(opportunity.id)
        if dimensions is None:
            continue
        result = score_opportunity(
            opportunity,
            dimensions,
            confidence=confidence.get(opportunity.id, 0.0),
        )
        ranked.append(
            RankedOpportunity(opportunity=opportunity, score=result.score, cluster=cluster)
        )

    ranked.sort(key=lambda item: (-item.score.weighted_score, item.opportunity.id))
    return OpportunityEngineResult(
        signals=normalized,
        clusters=clusters,
        ranked_opportunities=tuple(ranked),
    )
