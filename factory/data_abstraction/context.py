"""Generic context and Why Now consumers for provider-neutral intelligence."""

from __future__ import annotations

from hashlib import sha256
from typing import Sequence

from factory.schemas.domain import Context, Signal, WhyNow


def _id(prefix: str, parts: Sequence[str]) -> str:
    payload = "|".join(part.strip() for part in parts)
    return f'{prefix}_{sha256(payload.encode("utf-8")).hexdigest()[:24]}'


def build_context(*, signal: Signal, context_type: str, facts: Sequence[str], evidence_refs: Sequence[str], current_state: str, change_event: str, confidence: float, provenance: str) -> Context:
    clean_facts = tuple(f.strip() for f in facts if f.strip())
    if not clean_facts:
        raise ValueError("facts must not be empty")
    return Context(
        id=_id("ctx", (signal.id, context_type, *clean_facts)),
        signal_id=signal.id,
        context_type=context_type,
        facts=clean_facts,
        evidence_refs=tuple(sorted(set(evidence_refs))),
        current_state=current_state,
        change_event=change_event,
        confidence=confidence,
        provenance=provenance,
        account_id=signal.account_id,
    )


def build_why_now(*, context: Context, trigger: str, timing_factors: Sequence[str], rationale: str, evidence_refs: Sequence[str], confidence: float, verifiable: bool) -> WhyNow:
    refs = tuple(sorted(set(evidence_refs)))
    if verifiable and not refs:
        raise ValueError("verifiable Why Now assessments require evidence references")
    return WhyNow(
        id=_id("wn", (context.id, trigger, rationale)),
        signal_id=context.signal_id,
        trigger=trigger,
        timing_factors=tuple(f.strip() for f in timing_factors if f.strip()),
        rationale=rationale,
        evidence_refs=refs,
        confidence=confidence,
        verifiable=verifiable,
        account_id=context.account_id,
    )
