"""Provider-agnostic deterministic signal extraction baseline."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable, Sequence

from factory.account_intelligence.domain import AccountSignal, SourceObservation


@dataclass(frozen=True)
class SignalRule:
    """Explicit rule used by the baseline extractor; rules are not truth labels."""

    rule_id: str
    signal_type: str
    title: str
    trigger_terms: tuple[str, ...]
    confidence: float = 0.8

    def __post_init__(self) -> None:
        if not self.rule_id.strip() or not self.signal_type.strip() or not self.title.strip():
            raise ValueError("rule_id, signal_type and title must be non-empty")
        if not self.trigger_terms:
            raise ValueError("trigger_terms must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


def _stable_signal_id(observation: SourceObservation, rule: SignalRule) -> str:
    payload = "|".join((observation.id, rule.rule_id))
    return "sig_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def extract_signals(
    observations: Iterable[SourceObservation],
    rules: Sequence[SignalRule],
) -> tuple[AccountSignal, ...]:
    """Extract signals without accessing evaluation ground truth."""
    normalized_rules = tuple(rules)
    if len({rule.rule_id for rule in normalized_rules}) != len(normalized_rules):
        raise ValueError("rule_id values must be unique")

    signals: list[AccountSignal] = []
    for observation in observations:
        content = observation.content.casefold()
        for rule in normalized_rules:
            if all(term.casefold() in content for term in rule.trigger_terms):
                signals.append(
                    AccountSignal(
                        id=_stable_signal_id(observation, rule),
                        account_id=observation.account_id,
                        signal_type=rule.signal_type,
                        title=rule.title,
                        observed_at=observation.observed_at,
                        observation_ids=(observation.id,),
                        confidence=min(observation.confidence, rule.confidence),
                        rationale=f"matched rule {rule.rule_id}",
                        metadata={"rule_id": rule.rule_id},
                    )
                )
    return tuple(sorted(signals, key=lambda signal: signal.id))
