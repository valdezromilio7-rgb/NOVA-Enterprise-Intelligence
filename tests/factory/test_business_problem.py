from factory.account_intelligence.business_problem import build_business_problem
from factory.account_intelligence.context import build_account_context, assess_why_now
from factory.account_intelligence.opportunity_bridge import business_problem_to_opportunity


def _context():
    return build_account_context(
        account_id="acct-001",
        signal_id="sig-001",
        context_type="operational",
        facts=("Repeated delivery-status requests are observed.",),
        evidence_refs=("ev-001",),
        current_state="Support staff respond manually.",
        change_event="Repeated requests increased.",
        confidence=0.9,
        provenance="fixture",
    )


def _why_now(context):
    return assess_why_now(
        context=context,
        trigger="Repeated delivery-status requests",
        timing_factors=("recent repeated demand",),
        rationale="The observed repetition indicates a current operational trigger.",
        evidence_refs=("ev-001",),
        confidence=0.8,
        verifiable=True,
    )


def test_business_problem_is_deterministic_and_auditable() -> None:
    context = _context()
    why_now = _why_now(context)
    first = build_business_problem(
        context=context,
        why_now=why_now,
        problem_statement="Customers cannot reliably obtain delivery status.",
        current_solution="Support staff check systems manually.",
        gap="No single workflow exposes current delivery status.",
        desired_outcome="Reduce repeated status requests with verified delivery visibility.",
        evidence_refs=("ev-001", "ev-001"),
        confidence=0.85,
        provenance="fixture",
    )
    second = build_business_problem(
        context=context,
        why_now=why_now,
        problem_statement="Customers cannot reliably obtain delivery status.",
        current_solution="Support staff check systems manually.",
        gap="No single workflow exposes current delivery status.",
        desired_outcome="Reduce repeated status requests with verified delivery visibility.",
        evidence_refs=("ev-001",),
        confidence=0.85,
        provenance="fixture",
    )
    assert first.id == second.id
    assert first.evidence_refs == ("ev-001",)


def test_business_problem_requires_matching_context_and_why_now() -> None:
    context = _context()
    mismatched = assess_why_now(
        context=build_account_context(
            account_id="acct-002",
            signal_id="sig-002",
            context_type="operational",
            facts=("fact",),
            evidence_refs=("ev-002",),
            current_state="state",
            change_event="change",
            confidence=0.8,
            provenance="fixture",
        ),
        trigger="trigger",
        timing_factors=("factor",),
        rationale="rationale",
        evidence_refs=("ev-002",),
        confidence=0.8,
        verifiable=True,
    )
    try:
        build_business_problem(
            context=context,
            why_now=mismatched,
            problem_statement="problem",
            current_solution="solution",
            gap="gap",
            desired_outcome="outcome",
            evidence_refs=("ev-001",),
            confidence=0.8,
            provenance="fixture",
        )
    except ValueError as exc:
        assert str(exc) == "context and Why Now identity must match"
    else:
        raise AssertionError("expected ValueError")


def test_business_problem_reuses_canonical_opportunity_contract() -> None:
    context = _context()
    problem = build_business_problem(
        context=context,
        why_now=_why_now(context),
        problem_statement="Customers cannot reliably obtain delivery status.",
        current_solution="Support staff check systems manually.",
        gap="No single workflow exposes current delivery status.",
        desired_outcome="Reduce repeated status requests.",
        evidence_refs=("ev-001",),
        confidence=0.85,
        provenance="fixture",
    )
    opportunity = business_problem_to_opportunity(
        problem,
        target_customer="Fixture Company",
        evidence_ids=("ev-001", "ev-001"),
    )
    assert opportunity.id == f"opp-{problem.id}"
    assert opportunity.evidence_ids == ("ev-001",)
    assert opportunity.metadata["business_problem_id"] == problem.id
    assert opportunity.metadata["why_now_version"] == problem.why_now_version
    assert opportunity.metadata["evidence_refs"] == "ev-001"


def test_opportunity_bridge_rejects_empty_target_customer() -> None:
    context = _context()
    problem = build_business_problem(
        context=context,
        why_now=_why_now(context),
        problem_statement="problem",
        current_solution="solution",
        gap="gap",
        desired_outcome="outcome",
        evidence_refs=("ev-001",),
        confidence=0.8,
        provenance="fixture",
    )
    try:
        business_problem_to_opportunity(problem, target_customer=" ")
    except ValueError as exc:
        assert str(exc) == "target_customer must not be empty"
    else:
        raise AssertionError("expected ValueError")
