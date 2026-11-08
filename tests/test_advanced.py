import pytest
from valuation_lab.forecast import ForecastAssumptions, operating_forecast
from valuation_lab.comparables import Comparable, comparable_summary
from valuation_lab.transactions import acquisition_case, DebtTranche, lbo_debt_schedule
from valuation_lab.sensitivity import multiple_sensitivity

def test_forecast_cash_flow_bridge():
    a = ForecastAssumptions(.1, .2, .25, .04, .03, .1)
    rows = operating_forecast(100, 10, 2, a)
    assert rows[0]["revenue"] == pytest.approx(110)
    assert rows[0]["change_nwc"] == pytest.approx(1)
    assert rows[0]["fcff"] == pytest.approx(110*.2 - (110*.2-110*.03)*.25 - 110*.04 - 1)
    assert rows[1]["nwc"] == pytest.approx(12.1)

def test_comparables():
    result = comparable_summary([Comparable("A", 100, 10), Comparable("B", 60, 10), Comparable("C", 80, 10)], 15)
    assert result["median_multiple"] == 8
    assert result["implied_ev"] == 120

def test_acquisition():
    r = acquisition_case(15, 7, 2, 6, 25, fees=3)
    assert r["purchase_ev"] == 105
    assert r["equity_purchase_price"] == 80
    assert r["net_synergy_value_after_fees"] == 9

def test_debt_schedule():
    tranches = [DebtTranche("Term loan", 100, .1, 10)]
    rows = lbo_debt_schedule(tranches, [30, 30])
    assert rows[0]["interest"] == pytest.approx(10)
    assert rows[0]["closing_debt"] == pytest.approx(80)
    assert rows[1]["interest"] == pytest.approx(8)
    assert rows[1]["closing_debt"] == pytest.approx(58)

def test_debt_shortfall():
    with pytest.raises(ValueError):
        lbo_debt_schedule([DebtTranche("Loan", 100, .1, 10)], [5])

def test_sensitivity():
    cells = multiple_sensitivity([14, 15], [7, 9], 25)
    assert len(cells) == 4
    assert cells[0]["equity_value"] == 73
    assert cells[-1]["equity_value"] == 110
