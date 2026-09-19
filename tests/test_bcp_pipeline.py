from factory.data_abstraction.pipeline import acquire_bcp_signal_and_evidence
from factory.data_abstraction.providers.bcp import BcpDailyCurrencyAdapter


FIXTURE = """
<div>PLANILLA DE COTIZACIONES AL 19 DE SEPTIEMBRE DEL 2026</div>
<table>
<tr><th>Nombre</th><th>Código</th><th>Compra</th></tr>
<tr><td>Dólar</td><td>USD</td><td>7420</td></tr>
</table>
"""


def test_bcp_fixture_reaches_canonical_signal_and_evidence():
    adapter = BcpDailyCurrencyAdapter(fetcher=lambda url, timeout: (FIXTURE, 12))
    signal, evidence = acquire_bcp_signal_and_evidence(adapter, currency="USD")
    assert signal.account_id is None
    assert signal.source == "bcp:cotizacion-referencial-monedas-diaria"
    assert signal.observation_ids == (evidence.observation_ids[0],)
    assert evidence.account_id is None
    assert evidence.verification_state.value == "VERIFIED"
    assert evidence.source_ids == ("bcp:cotizacion-referencial-monedas-diaria",)
