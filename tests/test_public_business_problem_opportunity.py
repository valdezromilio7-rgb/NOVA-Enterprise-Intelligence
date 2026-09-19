from factory.business_problem import build_business_problem
from factory.opportunity.public import build_opportunity
from factory.schemas.domain import Context, Signal, WhyNow


def test_public_business_problem_preserves_global_scope_and_lineage():
    signal = Signal(
        id="sig_public_001",
        source="bcp",
        observed_at="2026-09-19",
        subject="USD/PYG reference rate",
        content="USD: 7000",
        provenance="Banco Central del Paraguay",
        observation_ids=("obs_001",),
        signal_type="reference_rate",
        confidence=1.0,
    )
    context = Context(
        id="ctx_public_001",
        signal_id=signal.id,
        context_type="market",
        facts=("Reference rate changed.",),
        evidence_refs=("ev_001",),
        current_state="Current reference rate is published.",
        change_event="New daily observation.",
        confidence=1.0,
        provenance="BCP",
    )
    why_now = WhyNow(
        id="wn_public_001",
        signal_id=signal.id,
        trigger="New daily publication",
        timing_factors=("daily publication",),
        rationale="The latest official observation is available now.",
        evidence_refs=("ev_001",),
        confidence=1.0,
        verifiable=True,
    )
    problem = build_business_problem(
        context=context,
        why_now=why_now,
        problem_statement="Users need a current reference rate.",
        current_solution="Consult the official daily publication.",
        gap="The value is not yet packaged for the intended workflow.",
        desired_outcome="A traceable, current information asset.",
        evidence_refs=("ev_001",),
        confidence=1.0,
        provenance="NOVA public intelligence",
    )
    assert problem.account_id is None
    assert problem.context_id == context.id
    assert problem.why_now_id == why_now.id
    assert problem.evidence_refs == ("ev_001",)


def test_public_opportunity_keeps_business_problem_lineage():
    problem = build_business_problem(
        context=Context(
            id="ctx_002",
            signal_id="sig_002",
            context_type="market",
            facts=("A fact.",),
            evidence_refs=("ev_002",),
            current_state="State.",
            change_event="Change.",
            confidence=0.9,
            provenance="source",
        ),
        why_now=WhyNow(
            id="wn_002",
            signal_id="sig_002",
            trigger="Trigger",
            timing_factors=("factor",),
            rationale="Rationale",
            evidence_refs=("ev_002",),
            confidence=0.9,
            verifiable=True,
        ),
        problem_statement="Problem",
        current_solution="Current solution",
        gap="Gap",
        desired_outcome="Outcome",
        evidence_refs=("ev_002",),
        confidence=0.9,
        provenance="source",
    )
    opportunity = build_opportunity(
        problem=problem,
        title="Traceable information asset",
        target_customer="Public information users",
    )
    assert opportunity.account_id is None
    assert opportunity.business_problem_id == problem.id
    assert opportunity.evidence_ids == ("ev_002",)
    assert opportunity.metadata["signal_id"] == problem.signal_id
