from factory.account_intelligence.domain import Account, Source, SourceObservation
from factory.account_intelligence.normalize import (
    normalize_account,
    normalize_observations,
    stable_account_id,
)
from factory.account_intelligence.source_registry import SourceRegistry
from evaluation.account_intelligence.precision import evaluate_signal_precision


def test_account_id_is_deterministic_and_provider_independent() -> None:
    first = stable_account_id("Acme SA", "PY", "https://acme.example")
    second = stable_account_id(" acme sa ", "py", "https://acme.example")
    assert first == second
    assert first.startswith("acct_")


def test_account_normalization_preserves_identity_semantics() -> None:
    account = Account(id="ignored", name=" Acme   SA ", country="PY", industry="Transport")
    normalized = normalize_account(account)
    assert normalized.id == stable_account_id("Acme SA", "PY")
    assert normalized.name == "acme sa"
    assert normalized.industry == "transport"


def test_observation_normalization_deduplicates_deterministically() -> None:
    observation = SourceObservation(
        id="ignored",
        source_id="DIRGE",
        account_id="acct_1",
        observed_at="2026-09-05T12:00:00Z",
        reference=" record-1 ",
        content=" Company   expanded ",
        provenance="public-record",
    )
    result = normalize_observations((observation, observation))
    assert len(result) == 1
    assert result[0].id.startswith("obs_")
    assert result[0].content == "Company expanded"


def test_source_registry_rejects_duplicates() -> None:
    source = Source(id="dirge", name="DIRGE", kind="public_registry")
    registry = SourceRegistry((source,))
    assert registry.get("dirge") == source
    try:
        registry.register(source)
        assert False, "duplicate source must be rejected"
    except ValueError as exc:
        assert "already registered" in str(exc)


def test_invalid_observation_confidence_is_rejected() -> None:
    try:
        SourceObservation(
            id="obs",
            source_id="source",
            account_id="acct",
            observed_at="2026-09-05",
            reference="ref",
            content="content",
            provenance="public",
            confidence=1.1,
        )
        assert False, "confidence outside [0,1] must be rejected"
    except ValueError as exc:
        assert "confidence" in str(exc)


def test_signal_precision_matches_definition() -> None:
    result = evaluate_signal_precision(
        ("sig-1", "sig-2", "sig-2", "sig-3"),
        ("sig-1", "sig-3"),
    )
    assert result.analyzed == 3
    assert result.correct == 2
    assert result.precision == 2 / 3
