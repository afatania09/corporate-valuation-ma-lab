import pytest
from valuation_lab.acquisition_model import AcquisitionInputs, model_acquisition
from valuation_lab.memo import investment_committee_memo

def assumptions(**overrides):
    base = dict(opening_revenue=100, revenue_growth=.06, ebitda_margin=.24,
        depreciation_pct_revenue=.03, capex_pct_revenue=.05,
        working_capital_pct_revenue=.10, tax_rate=.25,
        entry_ebitda=24, entry_multiple=8, acquisition_debt=100,
        interest_rate=.08, annual_mandatory_amortisation=5,
        transaction_fees=4, exit_multiple=8, years=5)
    base.update(overrides)
    return AcquisitionInputs(**base)

def test_entry_sources_and_uses():
    r = model_acquisition(assumptions())
    assert r["entry_ev"] == 192
    assert r["sponsor_equity"] == 96
    assert r["exit_equity"] == pytest.approx(r["exit_ev"]-r["exit_debt"]+r["exit_cash"])
    assert r["moic"] == pytest.approx(r["exit_equity"]/96)
    assert all(row["closing_debt"] >= 0 for row in r["years"])

def test_cash_bridge_and_debt_rollforward():
    r = model_acquisition(assumptions())
    prior = 100
    for row in r["years"]:
        assert row["cash_before_debt_service"] == pytest.approx(
            row["ebitda"]-row["taxes"]-row["capex"]-row["change_nwc"])
        assert row["closing_debt"] == pytest.approx(
            prior-row["mandatory_repayment"]-row["optional_repayment"])
        prior = row["closing_debt"]

def test_debt_service_failure():
    with pytest.raises(ValueError, match="insufficient cash"):
        model_acquisition(assumptions(ebitda_margin=.01, acquisition_debt=170,
                                      interest_rate=.5))

def test_memo_generation():
    a = assumptions()
    memo = investment_committee_memo("ExampleCo", a, model_acquisition(a),
                                     valuation_date="2026-09-30")
    assert "ExampleCo" in memo
    assert "2026-09-30" in memo
    assert "Gross sponsor IRR" in memo
    assert "| Year | Revenue |" in memo
