"""Stable adapter interface for external information providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Mapping

from factory.data_abstraction.domain import AcquisitionResult, ProviderCapabilities


class DataProviderAdapter(ABC):
    """Read-only, provider-neutral acquisition boundary."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        raise NotImplementedError

    @abstractmethod
    def acquire(self, query: Mapping[str, str]) -> AcquisitionResult:
        """Acquire normalized observations without exposing provider payloads."""
        raise NotImplementedError
