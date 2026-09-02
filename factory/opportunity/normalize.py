"""Deterministic normalization of market and operational signals."""

from __future__ import annotations

import hashlib
import re
from dataclasses import replace
from typing import Iterable

from factory.schemas.domain import Signal


def normalize_text(value: str) -> str:
    """Normalize text without changing its semantic content."""
    return re.sub(r"\s+", " ", value.strip().lower())


def stable_signal_id(signal: Signal) -> str:
    """Return a stable identifier derived from immutable signal content."""
    raw = "|".join(
        [
            signal.source,
            signal.observed_at,
            signal.subject,
            signal.content,
            signal.provenance,
        ]
    )
    return "sig_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def normalize_signal(signal: Signal) -> Signal:
    """Return a normalized copy while preserving provenance and metadata."""
    return replace(
        signal,
        id=stable_signal_id(signal),
        source=normalize_text(signal.source),
        subject=normalize_text(signal.subject),
        content=re.sub(r"\s+", " ", signal.content.strip()),
        provenance=signal.provenance.strip(),
    )


def normalize_signals(signals: Iterable[Signal]) -> list[Signal]:
    """Normalize, deduplicate, and deterministically order signals."""
    unique: dict[str, Signal] = {}
    for signal in signals:
        normalized = normalize_signal(signal)
        unique[normalized.id] = normalized
    return sorted(unique.values(), key=lambda item: item.id)
