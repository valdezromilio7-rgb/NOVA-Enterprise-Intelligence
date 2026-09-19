from factory.data_abstraction.adapter import DataProviderAdapter
from factory.data_abstraction.domain import (
    AcquisitionResult,
    AcquisitionStatus,
    NormalizedObservation,
    ProviderCapabilities,
    RetrievalMetadata,
)
from factory.data_abstraction.normalize import normalize_observation, stable_observation_id


def make_observation(**overrides):
    values = dict(
        id="raw",
        source_id="source-1",
        account_id="account-1",
        observed_at="2026-09-19T12:00:00Z",
        reference=" https://example.test/item ",
        content="  Demand   increased ",
        provenance=" example-provider ",
        confidence=0.9,
    )
    values.update(overrides)
    return NormalizedObservation(**values)


def test_observation_id_is_deterministic_and_normalized():
    first = normalize_observation(make_observation())
    second = normalize_observation(make_observation(id="different"))

    assert first.id == second.id == stable_observation_id(first)
    assert first.content == "Demand increased"
    assert first.reference == "https://example.test/item"


def test_successful_acquisition_requires_retrieval_metadata():
    retrieval = RetrievalMetadata(retrieved_at="2026-09-19T12:00:01Z")
    result = AcquisitionResult(
        provider="laboratory",
        status=AcquisitionStatus.SUCCESS,
        observations=(make_observation(),),
        retrieval=retrieval,
    )
    assert result.status is AcquisitionStatus.SUCCESS


def test_failed_acquisition_cannot_publish_observations():
    try:
        AcquisitionResult(
            provider="laboratory",
            status=AcquisitionStatus.FAILED,
            observations=(make_observation(),),
        )
    except ValueError as exc:
        assert "failed acquisition" in str(exc)
    else:
        raise AssertionError("expected failed acquisition validation")


def test_adapter_contract_is_read_only_and_provider_neutral():
    class LaboratoryAdapter(DataProviderAdapter):
        @property
        def provider_name(self):
            return "laboratory"

        @property
        def capabilities(self):
            return ProviderCapabilities(supports_pagination=True)

        def acquire(self, query):
            return AcquisitionResult(
                provider=self.provider_name,
                status=AcquisitionStatus.SUCCESS,
                observations=(make_observation(),),
                retrieval=RetrievalMetadata(retrieved_at="2026-09-19T12:00:01Z"),
            )

    adapter = LaboratoryAdapter()
    assert adapter.capabilities.supports_read_only is True
    assert adapter.acquire({}).observations[0].source_id == "source-1"


def test_observation_can_be_global_without_account_scope():
    observation = normalize_observation(make_observation(account_id=None))
    assert observation.account_id is None
    assert observation.id.startswith("obs_")


def test_bcp_adapter_normalizes_real_source_shape():
    from factory.data_abstraction.providers.bcp import BcpDailyCurrencyAdapter

    html = """
    <table>
      <tr><th>MONEDA</th><th>ME/USD</th><th>₲ / ME</th></tr>
      <tr><td>DÓLAR ESTADOUNIDENSE</td><td>USD</td><td>5.956,04</td></tr>
    </table>
    <div>PLANILLA DE COTIZACIONES AL VIERNES 18 DE SEPTIEMBRE DEL 2026</div>
    """
    adapter = BcpDailyCurrencyAdapter(fetcher=lambda url, timeout: (html, 12))
    result = adapter.acquire({"currency": "USD"})

    assert result.status is AcquisitionStatus.SUCCESS
    observation = result.observations[0]
    assert observation.account_id is None
    assert observation.observed_at == "2026-09-18"
    assert observation.metadata["currency"] == "USD"
    assert observation.metadata["rate_pyg"] == "5.956,04"
    assert observation.provenance == "Banco Central del Paraguay"
    assert result.retrieval is not None


def test_account_scoped_observation_bridges_without_changing_identity():
    from factory.data_abstraction.bridge import to_source_observation

    normalized = normalize_observation(make_observation())
    bridged = to_source_observation(normalized)

    assert bridged.id == normalized.id
    assert bridged.account_id == normalized.account_id
    assert bridged.source_id == normalized.source_id
    assert bridged.content == normalized.content


def test_global_observation_cannot_cross_account_boundary():
    from factory.data_abstraction.bridge import to_source_observation

    normalized = normalize_observation(make_observation(account_id=None))
    try:
        to_source_observation(normalized)
    except ValueError as exc:
        assert "global observations" in str(exc)
    else:
        raise AssertionError("expected global observation boundary")
