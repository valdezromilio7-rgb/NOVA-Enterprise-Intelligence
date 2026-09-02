"""Deterministic lexical clustering for Product Factory v0.1."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from factory.schemas.domain import Signal

_STOPWORDS = {
    "a", "al", "con", "de", "del", "el", "en", "la", "las", "los",
    "para", "por", "que", "se", "un", "una", "y", "the", "and", "of", "to",
}


@dataclass(frozen=True)
class SignalCluster:
    """A deterministic group of related signals."""

    key: str
    signal_ids: tuple[str, ...]
    terms: tuple[str, ...]


def _tokens(signal: Signal) -> set[str]:
    text = f"{signal.subject} {signal.content}"
    return {
        token
        for token in re.findall(r"[a-z0-9áéíóúüñ]+", text.lower())
        if len(token) >= 3 and token not in _STOPWORDS
    }


def cluster_signals(signals: Iterable[Signal], min_overlap: int = 2) -> list[SignalCluster]:
    """Group signals when they share at least ``min_overlap`` meaningful tokens."""
    items = sorted(signals, key=lambda item: item.id)
    groups: list[dict[str, object]] = []

    for signal in items:
        tokens = _tokens(signal)
        matches: list[dict[str, object]] = []
        for group in groups:
            if len(tokens & group["tokens"]) >= min_overlap:  # type: ignore[operator]
                matches.append(group)
        if not matches:
            groups.append({"tokens": set(tokens), "ids": [signal.id]})
            continue
        target = matches[0]
        target["ids"].append(signal.id)  # type: ignore[union-attr]
        target["tokens"].update(tokens)  # type: ignore[union-attr]
        for other in matches[1:]:
            target["ids"].extend(other["ids"])  # type: ignore[union-attr]
            target["tokens"].update(other["tokens"])  # type: ignore[union-attr]
            groups.remove(other)

    clusters = []
    for group in groups:
        ids = tuple(sorted(set(group["ids"])))  # type: ignore[arg-type]
        terms = tuple(sorted(group["tokens"]))  # type: ignore[arg-type]
        key = "cluster_" + (terms[0] if terms else "empty")
        clusters.append(SignalCluster(key=key, signal_ids=ids, terms=terms))
    return sorted(clusters, key=lambda item: item.key)
