"""Reproducible end-to-end Account Intelligence evaluation harness."""

from __future__ import annotations

from dataclasses import dataclass

from evaluation.account_intelligence.benchmark import BASELINE_RULES, _observable_dimensions
from evaluation.account_intelligence.dataset import AccountIntelligenceFixture, build_fixture
from evaluation.account_intelligence.ground_truth import EXPECTED_SIGNAL_OBSERVATION_IDS
from evaluation.account_intelligence.precision import SignalPrecisionResult, evaluate_observation_precision
from factory.account_intelligence.business_problem import BusinessProblem, build_business_problem
from factory.account_intelligence.context import AccountContext, WhyNowAssessment, assess_why_now, build_account_context
from factory.account_intelligence.evidence import Evidence, build_evidence
from factory.account_intelligence.opportunity_bridge import business_problem_to_opportunity
from factory.account_intelligence.score import SignalScore, rank_signal_scores, score_signal
from factory.account_intelligence.signal_engine import extract_signals
from factory.schemas.domain import Opportunity, EvidenceVerificationState


@dataclass(frozen=True)
class AccountIntelligenceE2EResult:
    analyzed_accounts: int
    extracted_signals: int
    top_signals: tuple[SignalScore, ...]
    precision: SignalPrecisionResult
    evidence: Evidence
    context: AccountContext
    why_now: WhyNowAssessment
    business_problem: BusinessProblem
    opportunity: Opportunity


def run_end_to_end_evaluation(fixture: AccountIntelligenceFixture | None = None, top_n: int = 20) -> AccountIntelligenceE2EResult:
    """Execute the complete deterministic v0.1 chain without factory truth access."""
    if top_n <= 0:
        raise ValueError("top_n must be positive")
    data = fixture or build_fixture()
    signals = extract_signals(data.observations, BASELINE_RULES)
    observation_by_id = {observation.id: observation for observation in data.observations}
    account_by_id = {account.id: account for account in data.accounts}
    scores = rank_signal_scores(tuple(score_signal(signal, _observable_dimensions(observation_by_id[signal.observation_ids[0]].content)) for signal in signals))
    top_signals = scores[:top_n]
    precision = evaluate_observation_precision(top_signals, EXPECTED_SIGNAL_OBSERVATION_IDS)
    if not top_signals:
        raise ValueError("end-to-end evaluation requires at least one top signal")
    top_signal = next(signal for signal in signals if signal.id == top_signals[0].signal_id)
    observation = observation_by_id[top_signal.observation_ids[0]]
    account = account_by_id[top_signal.account_id]
    evidence = build_evidence(observations=(observation,), claim=observation.content, strength=observation.confidence, verification_state=EvidenceVerificationState.UNVERIFIED)
    evidence_refs = (evidence.id,)
    context = build_account_context(account_id=account.id, signal_id=top_signal.id, context_type="operational", facts=(observation.content,), evidence_refs=evidence_refs, current_state="Customer support receives delivery-status requests.", change_event="Repeated delivery-status demand is observed.", confidence=observation.confidence, provenance=observation.provenance)
    why_now = assess_why_now(context=context, trigger=top_signal.title, timing_factors=("repeated observed demand",), rationale="The observation contains explicit repeated demand and provides a current operational trigger.", evidence_refs=evidence_refs, confidence=0.8, verifiable=False)
    problem = build_business_problem(context=context, why_now=why_now, problem_statement="Customers cannot reliably obtain delivery status without support intervention.", current_solution="Support staff respond to delivery-status requests manually.", gap="The observed workflow lacks a single verified delivery-status path for customers.", desired_outcome="Provide verified delivery visibility while reducing repeated support demand.", evidence_refs=evidence_refs, confidence=0.85, provenance=observation.provenance)
    opportunity = business_problem_to_opportunity(problem, target_customer=account.name)
    opportunity = Opportunity(id=opportunity.id, title=opportunity.title, problem=opportunity.problem, target_customer=opportunity.target_customer, state=opportunity.state, evidence_ids=evidence_refs, assumptions=opportunity.assumptions, metadata=opportunity.metadata)
    return AccountIntelligenceE2EResult(analyzed_accounts=len(data.accounts), extracted_signals=len(signals), top_signals=top_signals, precision=precision, evidence=evidence, context=context, why_now=why_now, business_problem=problem, opportunity=opportunity)
