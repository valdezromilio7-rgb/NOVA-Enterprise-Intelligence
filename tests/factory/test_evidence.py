from factory.account_intelligence.domain import SourceObservation
from factory.account_intelligence.evidence import build_evidence, validate_evidence
from factory.schemas.domain import EvidenceVerificationState


def observation(
    observation_id: str = "obs-001",
    *,
    account_id: str = "acct-001",
    source_id: str = "source-001",
    confidence: float = 1.0,
    content: str = "Customer support reports repeated delivery-status requests.",
) -> SourceObservation:
    return SourceObservation(
        id=observation_id,
        source_id=source_id,
        account_id=account_id,
        observed_at="2026-01-01T00:00:00Z",
        reference=f"fixture://{observation_id}",
        content=content,
        provenance="synthetic-fixture",
        confidence=confidence,
    )


def test_evidence_is_deterministic_and_preserves_observation_linkage() -> None:
    first = build_evidence(
        (observation(),),
        claim="Repeated delivery-status demand exists.",
        strength=0.8,
    )
    second = build_evidence(
        (observation(),),
        claim="Repeated delivery-status demand exists.",
        strength=0.8,
    )

    assert first == second
    assert first.observation_ids == ("obs-001",)
    assert first.source_ids == ("source-001",)
    assert first.verification_state is EvidenceVerificationState.UNVERIFIED


def test_verified_evidence_requires_positive_supported_strength() -> None:
    evidence = build_evidence(
        (observation(),),
        claim="Repeated delivery-status demand exists.",
        strength=0.8,
        verification_state=EvidenceVerificationState.VERIFIED,
    )
    validate_evidence(evidence, (observation(),))


def test_unsupported_verified_evidence_is_rejected() -> None:
    try:
        build_evidence(
            (observation(confidence=0.0),),
            claim="Unsupported claim.",
            strength=0.8,
            verification_state=EvidenceVerificationState.VERIFIED,
        )
    except ValueError as exc:
        assert str(exc) == "unsupported evidence cannot be marked verified"
    else:
        raise AssertionError("expected ValueError")


def test_conflicting_state_is_explicit_and_not_silently_resolved() -> None:
    evidence = build_evidence(
        (
            observation(),
            observation(
                "obs-002",
                content="Customer support reports no delivery-status issue.",
            ),
        ),
        claim="Delivery-status demand has conflicting observations.",
        strength=0.5,
        verification_state=EvidenceVerificationState.CONFLICTING,
    )
    assert evidence.verification_state is EvidenceVerificationState.CONFLICTING
    assert evidence.observation_ids == ("obs-001", "obs-002")


def test_unverifiable_evidence_cannot_claim_positive_strength() -> None:
    try:
        build_evidence(
            (observation(),),
            claim="Unverifiable claim.",
            strength=0.1,
            verification_state=EvidenceVerificationState.UNVERIFIABLE,
        )
    except ValueError as exc:
        assert str(exc) == "unverifiable evidence cannot claim positive strength"
    else:
        raise AssertionError("expected ValueError")
