import pytest
from valuation_lab.consolidation import BalanceSheet, consolidate

def test_goodwill():
    r=consolidate(BalanceSheet(500,200,300),BalanceSheet(100,40,60),90,50,20,5,2)
    assert r["goodwill"]==15
    assert r["assets"]==593
    assert r["liabilities"]==295
    assert r["equity"]==298
    assert r["balance_check"]==0

def test_bargain():
    r=consolidate(BalanceSheet(500,200,300),BalanceSheet(100,40,60),50,0,0,0)
    assert r["bargain_gain"]==10
    assert r["balance_check"]==0

def test_unbalanced():
    with pytest.raises(ValueError):
        consolidate(BalanceSheet(500,200,200),BalanceSheet(100,40,60),50,0,0,0)
