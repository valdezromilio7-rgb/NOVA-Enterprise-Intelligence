"""Read-only adapter for the Banco Central del Paraguay daily FX page."""

from __future__ import annotations

from datetime import datetime, timezone
from html.parser import HTMLParser
import re
from typing import Callable, Mapping
from urllib.request import Request, urlopen

from factory.data_abstraction.adapter import DataProviderAdapter
from factory.data_abstraction.domain import (
    AcquisitionResult,
    AcquisitionStatus,
    FreshnessStatus,
    NormalizedObservation,
    ProviderCapabilities,
    RetrievalMetadata,
)
from factory.data_abstraction.normalize import normalize_observation

SOURCE_ID = "bcp:cotizacion-referencial-monedas-diaria"
SOURCE_URL = "https://www.bcp.gov.py/webapps/web/cotizacion/monedas"

_MONTHS = {
    "ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5, "JUNIO": 6,
    "JULIO": 7, "AGOSTO": 8, "SEPTIEMBRE": 9, "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12,
}


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "tr":
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._row is not None and self._cell is not None:
            self._row.append(re.sub(r"\s+", " ", "".join(self._cell)).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None


def _fetch_html(url: str, timeout_seconds: float) -> tuple[str, int]:
    request = Request(url, headers={"User-Agent": "NOVA-DataAbstraction/0.1"})
    started = datetime.now(timezone.utc)
    with urlopen(request, timeout=timeout_seconds) as response:
        payload = response.read()
    elapsed = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
    return payload.decode("utf-8", errors="replace"), elapsed


def _extract_observed_date(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html.upper())
    text = re.sub(r"\s+", " ", text)
    match = re.search(
        r"PLANILLA DE COTIZACIONES AL\s+(?:\w+\s+)?(\d{1,2}) DE ([A-ZÁÉÍÓÚÑ]+) DEL (\d{4})",
        text,
    )
    if not match:
        raise ValueError("BCP observation date not found")
    day, month_name, year = match.groups()
    month = _MONTHS.get(month_name)
    if month is None:
        raise ValueError(f"unsupported BCP month: {month_name}")
    return f"{int(year):04d}-{month:02d}-{int(day):02d}"


def _extract_currency_row(html: str, currency: str) -> tuple[str, str, str]:
    parser = _TableParser()
    parser.feed(html)
    wanted = currency.strip().upper()
    for row in parser.rows:
        if len(row) >= 3 and row[1].strip().upper() == wanted:
            return row[0], row[1], row[2]
    raise ValueError(f"BCP currency not found: {wanted}")


class BcpDailyCurrencyAdapter(DataProviderAdapter):
    """Acquire the latest BCP reference currency observation without account scope."""

    def __init__(
        self,
        *,
        timeout_seconds: float = 15.0,
        fetcher: Callable[[str, float], tuple[str, int]] | None = None,
    ) -> None:
        self._timeout_seconds = timeout_seconds
        self._fetcher = fetcher or _fetch_html

    @property
    def provider_name(self) -> str:
        return "bcp"

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(supports_read_only=True)

    def acquire(self, query: Mapping[str, str]) -> AcquisitionResult:
        retrieved_at = datetime.now(timezone.utc).isoformat()
        started = datetime.now(timezone.utc)
        currency = query.get("currency", "USD").strip().upper() or "USD"
        try:
            html, duration_ms = self._fetcher(SOURCE_URL, self._timeout_seconds)
            observed_at = _extract_observed_date(html)
            name, code, rate = _extract_currency_row(html, currency)
            observation = normalize_observation(
                NormalizedObservation(
                    id="pending",
                    source_id=SOURCE_ID,
                    account_id=None,
                    observed_at=observed_at,
                    reference=SOURCE_URL,
                    content=f"{name}: {code}; PYG per unit: {rate}",
                    provenance="Banco Central del Paraguay",
                    confidence=1.0,
                    metadata={"currency": code, "rate_pyg": rate},
                )
            )
            return AcquisitionResult(
                provider=self.provider_name,
                status=AcquisitionStatus.SUCCESS,
                observations=(observation,),
                retrieval=RetrievalMetadata(
                    retrieved_at=retrieved_at,
                    duration_ms=duration_ms,
                    freshness=FreshnessStatus.UNKNOWN,
                ),
            )
        except Exception as exc:
            return AcquisitionResult(
                provider=self.provider_name,
                status=AcquisitionStatus.FAILED,
                observations=(),
                retrieval=RetrievalMetadata(
                    retrieved_at=retrieved_at,
                    duration_ms=int((datetime.now(timezone.utc) - started).total_seconds() * 1000),
                    freshness=FreshnessStatus.UNKNOWN,
                    error_code="BCP_ACQUISITION_ERROR",
                    error_message=str(exc),
                ),
            )
