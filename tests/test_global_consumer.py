from factory.data_abstraction.consumer import evidence_from_observations, signal_from_observation
from factory.data_abstraction.domain import FreshnessStatus, NormalizedObservation, RetrievalMetadata
from factory.schemas.domain import EvidenceVerificationState


def observation(account_id=None, observation_id="obs-global-001"):
    return NormalizedObservation(
        id=observation_id,
        source_id="bcp:cotizacion-referencial-monedas-diaria",
        account_id=account_id,
        observed_at="2026-09-19",
        reference="https://www.bcp.gov.py/webapps/web/cotizacion/monedas",
        content="Dólar: USD; PYG per unit: 7420",
        provenance="Banco Central del Paraguay",
        confidence=1.0,
        retrieval=RetrievalMetadata(
            retrieved_at="2026-09-19T18:00:00Z",
            request_id="fixture-001",
            duration_ms=10,
            freshness=FreshnessStatus.FRESH,
        ),
        metadata={"currency": "USD", "rate_pyg": "7420"},
    )


def test_global_observation_becomes_canonical_signal_without_account_scope():
    signal = signal_from_observation(observation(), subject="USD/PYG reference rate")
    assert signal.account_id is None
    assert signal.observation_ids == ("obs-global-001",)
    assert signal.source == "bcp:cotizacion-referencial-monedas-diaria"


def test_global_observation_becomes_canonical_evidence_without_fake_account():
    evidence = evidence_from_observations(
        (observation(),),
        claim="BCP reported a USD/PYG reference rate of 7420.",
        strength=1.0,
        verification_state=EvidenceVerificationState.VERIFIED,
    )
    assert evidence.account_id is None
    assert evidence.observation_ids == ("obs-global-001",)


def test_global_evidence_is_deterministic():
    first = evidence_from_observations((observation(),), claim="USD/PYG rate is 7420.", strength=1.0)
    second = evidence_from_observations((observation(),), claim="USD/PYG rate is 7420.", strength=1.0)
    assert first == second


def test_mixed_account_scopes_are_rejected():
    try:
        evidence_from_observations(
            (observation(), observation(account_id="acct-001", observation_id="obs-account-001")),
            claim="Mixed scope.",
            strength=0.5,
        )
    except ValueError as exc:
        assert str(exc) == "all observations must share the same account scope"
    else:
        raise AssertionError("expected ValueError")
