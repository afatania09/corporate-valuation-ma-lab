import pytest
from valuation_lab.three_statement import OpeningBalanceSheet, Drivers, integrated_forecast
from valuation_lab.lbo import sponsor_lbo
from valuation_lab.transactions import DebtTranche

def opening():
    # 10 + 20 + 100 = 10 + 50 + 70
    return OpeningBalanceSheet(10, 20, 100, 10, 50, 70)

def drivers():
    return Drivers(.05, .25, .03, .05, .20, .10, .08, .25, 5)

def test_three_statement_balances_and_links():
    rows = integrated_forecast(100, opening(), drivers(), 5)
    assert len(rows) == 5
    assert all(abs(r["balance_check"]) < 1e-7 for r in rows)
    assert rows[0]["revenue"] == pytest.approx(105)
    assert rows[0]["interest"] == pytest.approx(4)
    assert rows[0]["debt"] == pytest.approx(45)
    assert rows[0]["equity"] == pytest.approx(70 + rows[0]["net_income"])
    assert rows[0]["cash"] == pytest.approx(10 + rows[0]["cash_change"])

def test_unbalanced_opening_rejected():
    bad = OpeningBalanceSheet(10, 20, 100, 10, 50, 71)
    with pytest.raises(ValueError, match="does not balance"):
        integrated_forecast(100, bad, drivers(), 2)

def test_funding_shortfall_rejected():
    a = Drivers(0, .01, .01, .5, .2, .1, .08, .25, 50)
    with pytest.raises(ValueError, match="funding shortfall"):
        integrated_forecast(100, opening(), a, 1)

def test_lbo_sources_uses_and_returns():
    tranches = [DebtTranche("Senior", 80, .08, 5),
                DebtTranche("Junior", 20, .12, 0)]
    result = sponsor_lbo(20, 8, 30, 100, 5, tranches,
                         [25, 27, 30, 32, 35], 25, 8)
    assert result["entry_ev"] == 160
    assert result["seller_equity"] == 130
    assert result["sponsor_equity"] == 65
    assert result["exit_ev"] == 200
    assert result["exit_debt"] >= 0
    assert result["moic"] == pytest.approx(result["exit_equity"]/65)

def test_lbo_debt_mismatch_rejected():
    with pytest.raises(ValueError, match="reconcile"):
        sponsor_lbo(20, 8, 30, 99, 5,
                    [DebtTranche("Senior", 100, .08, 5)],
                    [30], 25, 8)
