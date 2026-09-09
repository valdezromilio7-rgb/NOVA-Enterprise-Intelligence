from factory.account_intelligence.context import (
    assess_why_now,
    build_account_context,
)


def test_context_normalizes_facts_and_evidence() -> None:
    context = build_account_context(
        account_id="acct-1",
        signal_id="sig-1",
        context_type="customer_pain",
        facts=(" repeated requests ", "delivery delay"),
        evidence_refs=("obs-2", "obs-1", "obs-1"),
        current_state="support lacks delivery visibility",
        change_event="repeated requests observed",
        confidence=0.9,
        provenance="synthetic-fixture",
    )
    assert context.facts == ("repeated requests", "delivery delay")
    assert context.evidence_refs == ("obs-1", "obs-2")


def test_why_now_requires_evidence_when_marked_verifiable() -> None:
    context = build_account_context(
        account_id="acct-1",
        signal_id="sig-1",
        context_type="customer_pain",
        facts=("repeated requests",),
        evidence_refs=("obs-1",),
        current_state="support lacks visibility",
        change_event="repeat demand observed",
        confidence=0.9,
        provenance="synthetic-fixture",
    )
    try:
        assess_why_now(
            context=context,
            trigger="repeat support demand",
            timing_factors=("recent observation",),
            rationale="Recent repeat demand provides a concrete trigger.",
            evidence_refs=(),
            confidence=0.8,
            verifiable=True,
        )
    except ValueError as exc:
        assert str(exc) == "verifiable Why Now assessments require evidence references"
    else:
        raise AssertionError("expected ValueError")


def test_why_now_can_be_explicitly_unverified() -> None:
    context = build_account_context(
        account_id="acct-1",
        signal_id="sig-1",
        context_type="customer_pain",
        facts=("repeated requests",),
        evidence_refs=(),
        current_state="support lacks visibility",
        change_event="reported issue",
        confidence=0.5,
        provenance="reported",
    )
    assessment = assess_why_now(
        context=context,
        trigger="reported urgency",
        timing_factors=("reported",),
        rationale="Timing is reported but not independently verified.",
        evidence_refs=(),
        confidence=0.5,
        verifiable=False,
    )
    assert assessment.verifiable is False
    assert assessment.evidence_refs == ()
