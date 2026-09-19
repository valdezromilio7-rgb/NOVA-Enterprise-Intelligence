from factory.data_abstraction.context import build_context, build_why_now
from factory.schemas.domain import Signal


def signal():
    return Signal(
        id="sig_global_001",
        source="bcp:cotizacion-referencial-monedas-diaria",
        observed_at="2026-09-19",
        subject="USD/PYG reference rate",
        content="USD reference rate observed.",
        provenance="Banco Central del Paraguay",
        account_id=None,
        signal_type="reference_rate",
        observation_ids=("obs-global-001",),
        confidence=1.0,
    )


def test_public_signal_builds_context_without_account_scope():
    context = build_context(
        signal=signal(),
        context_type="market_reference",
        facts=("USD/PYG reference rate observed.",),
        evidence_refs=("ev_global_001",),
        current_state="Reference rate available.",
        change_event="Daily observation.",
        confidence=1.0,
        provenance="BCP",
    )
    assert context.account_id is None
    assert context.signal_id == "sig_global_001"


def test_public_context_builds_why_now_without_fake_account():
    context = build_context(
        signal=signal(),
        context_type="market_reference",
        facts=("USD/PYG reference rate observed.",),
        evidence_refs=("ev_global_001",),
        current_state="Reference rate available.",
        change_event="Daily observation.",
        confidence=1.0,
        provenance="BCP",
    )
    why_now = build_why_now(
        context=context,
        trigger="Daily rate publication",
        timing_factors=("new daily observation",),
        rationale="The source published a new reference-rate observation.",
        evidence_refs=("ev_global_001",),
        confidence=1.0,
        verifiable=True,
    )
    assert why_now.account_id is None
    assert why_now.signal_id == context.signal_id
