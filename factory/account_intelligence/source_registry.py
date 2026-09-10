"""Explicit registry for approved Account Intelligence sources."""
from __future__ import annotations

from typing import Sequence

from factory.account_intelligence.domain import Source


class SourceRegistry:
    """In-memory source registry for deterministic v0.1 execution."""

    def __init__(self, sources: Sequence[Source] = ()) -> None:
        self._sources: dict[str, Source] = {}
        for source in sources:
            self.register(source)

    def register(self, source: Source) -> None:
        if source.id in self._sources:
            raise ValueError(f"source already registered: {source.id}")
        self._sources[source.id] = source

    def get(self, source_id: str) -> Source:
        try:
            return self._sources[source_id]
        except KeyError as exc:
            raise KeyError(f"unknown source: {source_id}") from exc

    def list(self) -> tuple[Source, ...]:
        return tuple(sorted(self._sources.values(), key=lambda source: source.id))
