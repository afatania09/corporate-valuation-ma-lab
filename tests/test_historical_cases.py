import pytest
from examples.hilton_lbo_case import scenario, analyse
from examples.microsoft_activision_case import analyse as microsoft

def test_hilton_base():
    r = scenario()
    assert r["entry_equity"] == 6
    assert r["exit_equity"] == 24
    assert r["moic"] == 4
    assert r["annualised_return"] == pytest.approx(4**(1/6)-1)

def test_hilton_downside():
    assert scenario(exit_ebitda=0)["moic"] == 0

def test_hilton_invalid():
    with pytest.raises(ValueError):
        scenario(entry_debt=26)

def test_hilton_scenarios_order():
    returns = [r["moic"] for r in analyse()["scenarios"]]
    assert returns == sorted(returns)

def test_microsoft_reconciliation():
    r = microsoft()
    assert r["identifiable_net_assets"] + r["reconstructed_goodwill"] == r["purchase_price"]
    assert r["ev_proxy"] == 65231
