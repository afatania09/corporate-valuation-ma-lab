import pytest
from valuation_lab.waterfall import Preferred, allocate_exit_proceeds
from valuation_lab.ppa import Intangible, purchase_price_allocation
from valuation_lab.portfolio_scenarios import Scenario, scenario_weighted_equity

def test_preference_wins_in_low_exit():
    r = allocate_exit_proceeds(50, Preferred(40, 1.5, .3))
    assert r["preferred_proceeds"] == 50
    assert r["common_proceeds"] == 0
    assert r["method"] == "liquidation_preference"

def test_conversion_wins_at_high_exit():
    r = allocate_exit_proceeds(300, Preferred(40, 1.5, .3))
    assert r["preferred_proceeds"] == 90
    assert r["common_proceeds"] == 210
    assert r["method"] == "conversion"

def test_ppa_reconciles():
    r = purchase_price_allocation(200, 100, 10,
            [Intangible("Brand", 30), Intangible("Customer relationships", 20, 5)], .25)
    assert r["deferred_tax_liability"] == pytest.approx(11.25)
    assert r["identifiable_net_assets"] == pytest.approx(148.75)
    assert r["goodwill"] == pytest.approx(51.25)
    assert r["reconciliation"] == pytest.approx(0)

def test_scenario_weighting():
    r = scenario_weighted_equity([
        Scenario("Downside", .25, 10, 6, 80),
        Scenario("Base", .5, 15, 8, 30),
        Scenario("Upside", .25, 20, 10, 20)])
    assert r["expected_equity"] == pytest.approx(.25*0 + .5*90 + .25*180)

def test_probabilities_must_sum_to_one():
    with pytest.raises(ValueError):
        scenario_weighted_equity([Scenario("Only", .9, 10, 8, 10)])
