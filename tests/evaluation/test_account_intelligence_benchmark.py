from evaluation.account_intelligence.benchmark import run_baseline_benchmark


def test_baseline_benchmark_runs_100_accounts_to_top_20() -> None:
    result = run_baseline_benchmark()
    assert result.analyzed_accounts == 100
    assert result.extracted_signals == 32
    assert len(result.ranked_top_signals) == 20
    assert result.precision.analyzed == 20
    assert result.precision.correct == 20
    assert result.precision.precision == 1.0


def test_benchmark_rejects_invalid_top_n() -> None:
    try:
        run_baseline_benchmark(top_n=0)
    except ValueError as exc:
        assert str(exc) == "top_n must be positive"
    else:
        raise AssertionError("expected ValueError")
