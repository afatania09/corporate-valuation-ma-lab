import pytest
from valuation_lab.sources_uses import ClosingInputs, closing_sources_uses


def test_clean_acquisition():
    r = closing_sources_uses(ClosingInputs(
        offer_enterprise_value=200, target_debt=50, target_cash=10,
        transaction_fees=5, financing_fees=2, new_acquisition_debt=100))
    assert r["seller_equity_value"] == pytest.approx(160)
    assert r["total_uses"] == pytest.approx(217)
    assert r["new_sponsor_equity"] == pytest.approx(107)
    assert r["total_sources"] == pytest.approx(217)
    assert r["reconciliation_difference"] == pytest.approx(0)


def test_rollover_is_neutral_to_total_funding():
    base = dict(offer_enterprise_value=200, target_debt=20, target_cash=5,
                new_acquisition_debt=90)
    no_roll = closing_sources_uses(ClosingInputs(**base))
    with_roll = closing_sources_uses(ClosingInputs(**base, rollover_equity=30))
    assert with_roll["new_sponsor_equity"] == pytest.approx(no_roll["new_sponsor_equity"] - 30)
    assert with_roll["seller_cash_consideration"] == pytest.approx(no_roll["seller_cash_consideration"] - 30)
    assert with_roll["total_uses"] == pytest.approx(no_roll["total_uses"])


def test_debt_like_cash_like_and_working_capital():
    r = closing_sources_uses(ClosingInputs(
        offer_enterprise_value=200, target_debt=40, target_cash=10,
        debt_like_items=5, cash_like_items=3, working_capital_adjustment=-2))
    assert r["seller_equity_value"] == pytest.approx(166)
    assert r["effective_purchase_ev_before_fees"] == pytest.approx(198)
    assert r["new_sponsor_equity"] == pytest.approx(198)


@pytest.mark.parametrize("change", [
    {"offer_enterprise_value": float("nan")},
    {"target_cash": -1},
    {"rollover_equity": 300},
    {"new_acquisition_debt": 300},
    {"target_debt": 300},
])
def test_invalid_closing_inputs(change):
    fields = dict(offer_enterprise_value=200, target_debt=20, target_cash=5)
    fields.update(change)
    with pytest.raises(ValueError):
        closing_sources_uses(ClosingInputs(**fields))
