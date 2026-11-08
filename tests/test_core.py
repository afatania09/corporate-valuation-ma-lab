import pytest
from valuation_lab.core import (
    Holding, enterprise_value, equity_value, dcf_enterprise_value,
    portfolio_nav, lbo_returns,
)

def test_ev_equity():
    assert enterprise_value(15, 7) == 105
    assert equity_value(105, 25) == 80

def test_portfolio():
    holdings = [
        Holding("Technology", 20, 10, 40, .8),
        Holding("Healthcare", 15, 9, 25, .65),
        Holding("Manufacturing", 12, 7, 30, 1),
        Holding("Retail", 8, 6, 20, .7),
        Holding("Logistics", 10, 8, 15, .9),
    ]
    assert portfolio_nav(holdings, 12, 7) == pytest.approx(336.60)

def test_dcf_manual():
    assert dcf_enterprise_value([10], .10, .02) == pytest.approx((10 + 10*1.02/.08)/1.10)

def test_invalid_wacc():
    with pytest.raises(ValueError):
        dcf_enterprise_value([10, 11], .02, .03)

def test_lbo():
    result = lbo_returns(100, 200, 5)
    assert result["moic"] == 2
    assert result["irr"] == pytest.approx(2**.2 - 1)

def test_ownership():
    with pytest.raises(ValueError):
        Holding("Bad", 10, 8, 0, 1.2).fund_value()
