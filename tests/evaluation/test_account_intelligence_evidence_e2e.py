from evaluation.account_intelligence.end_to_end_with_evidence import run_end_to_end_evaluation_with_evidence


def test_e2e_propagates_canonical_evidence_id() -> None:
    first = run_end_to_end_evaluation_with_evidence()
    second = run_end_to_end_evaluation_with_evidence()

    assert first.analyzed_accounts == 100
    assert first.extracted_signals == 32
    assert len(first.top_signals) == 20
    assert first.precision.correct == 20
    assert first.precision.precision == 1.0
    assert first.evidence.id.startswith("ev-")
    assert first.evidence.observation_ids
    assert first.context.evidence_refs == (first.evidence.id,)
    assert first.why_now.evidence_refs == (first.evidence.id,)
    assert first.business_problem.evidence_refs == (first.evidence.id,)
    assert tuple(first.opportunity.evidence_ids) == (first.evidence.id,)
    assert first.opportunity.metadata["evidence_refs"] == first.evidence.id
    assert first == second


def test_e2e_with_evidence_rejects_invalid_top_n() -> None:
    try:
        run_end_to_end_evaluation_with_evidence(top_n=0)
    except ValueError as exc:
        assert str(exc) == "top_n must be positive"
    else:
        raise AssertionError("expected ValueError")
