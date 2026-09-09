from evaluation.account_intelligence.end_to_end import run_end_to_end_evaluation


def test_end_to_end_evaluation_is_complete_and_deterministic() -> None:
    first = run_end_to_end_evaluation()
    second = run_end_to_end_evaluation()

    assert first.analyzed_accounts == 100
    assert first.extracted_signals == 32
    assert len(first.top_signals) == 20
    assert first.precision.analyzed == 20
    assert first.precision.correct == 20
    assert first.precision.precision == 1.0
    assert first.context.account_id == first.why_now.account_id == first.business_problem.account_id
    assert first.context.signal_id == first.why_now.signal_id == first.business_problem.signal_id
    assert first.business_problem.evidence_refs == ("obs-fixture-100",)
    assert first.opportunity.id == f"opp-{first.business_problem.id}"
    assert first.opportunity.evidence_ids == []
    assert first.opportunity.metadata["evidence_refs"] == "obs-fixture-100"

    assert first == second


def test_end_to_end_evaluation_rejects_invalid_top_n() -> None:
    try:
        run_end_to_end_evaluation(top_n=0)
    except ValueError as exc:
        assert str(exc) == "top_n must be positive"
    else:
        raise AssertionError("expected ValueError")
