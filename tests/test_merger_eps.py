import pytest
from dataclasses import replace
from valuation_lab.merger_eps import MergerInputs, merger_eps

BASE = MergerInputs(100, 50, 20, 20, 200, .5, .25, .08, .04, .25, 10, 4, 2)

def test_mixed_funding():
    r = merger_eps(BASE)
    assert r["stock_funding"] == 100
    assert r["debt_funding"] == 50
    assert r["cash_funding"] == 50
    assert r["new_shares"] == 5
    assert r["combined_net_income"] == pytest.approx(118.5)
    assert r["combined_eps"] == pytest.approx(118.5/55)
    assert r["accretion_pct"] == pytest.approx(100*(118.5/110-1))

def test_invalid_funding():
    with pytest.raises(ValueError):
        merger_eps(replace(BASE, stock_fraction=.9))

def test_loss_making_buyer():
    assert merger_eps(replace(BASE, buyer_net_income=-10))["accretion_pct"] is None

def test_all_stock():
    r = merger_eps(replace(BASE, stock_fraction=1, debt_fraction=0))
    assert r["new_shares"] == 10
    assert r["cash_funding"] == 0
