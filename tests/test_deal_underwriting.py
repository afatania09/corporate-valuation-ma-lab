import pytest
from valuation_lab.deal_underwriting import DealInputs, underwrite_deal, downside_scenarios


def example(**kwargs):
    d = dict(standalone_ev=100, offer_ev=110, annual_run_rate_synergy=10,
             synergy_realisation=(0.5, 1.0), integration_costs=(4, 0),
             discount_rate=.10, terminal_growth=.02, tax_rate=.25)
    d.update(kwargs)
    return DealInputs(**d)


def test_one_period_closed_form():
    a = example(standalone_ev=100, offer_ev=110, annual_run_rate_synergy=10,
                synergy_realisation=(1,), integration_costs=(0,), terminal_growth=0)
    result = underwrite_deal(a)
    assert result["net_synergy_npv"] == pytest.approx(75)
    assert result["maximum_offer_ev"] == pytest.approx(175)
    assert result["buyer_npv"] == pytest.approx(65)


def test_no_perpetuity_and_integration_costs():
    a = example(synergy_realisation=(1,), integration_costs=(4,),
                perpetual_synergies=False)
    r = underwrite_deal(a)
    assert r["pv_explicit_synergies"] == pytest.approx(7.5 / 1.1)
    assert r["pv_integration_costs"] == pytest.approx(3 / 1.1)
    assert r["net_synergy_npv"] == pytest.approx(4.5 / 1.1)
    assert r["value_creating"] is False


def test_purchase_price_npv_bridge():
    r = underwrite_deal(example())
    assert r["buyer_npv"] == pytest.approx(r["maximum_offer_ev"] - r["offer_ev"])
    assert r["buyer_npv"] == pytest.approx(r["net_synergy_npv"] - r["premium"])


def test_downside_monotonicity():
    results = downside_scenarios(example(synergy_realisation=(.4, .7, 1, 1),
                                          integration_costs=(4, 2, 0, 0)))
    assert results["base"]["buyer_npv"] > results["downside"]["buyer_npv"]
    assert results["downside"]["buyer_npv"] > results["severe"]["buyer_npv"]


@pytest.mark.parametrize("overrides", [
    {"discount_rate": .02, "terminal_growth": .02},
    {"synergy_realisation": (.5,), "integration_costs": (1, 2)},
    {"synergy_realisation": (1.2, 1)},
    {"integration_costs": (-1, 0)},
    {"offer_ev": float("nan")},
])
def test_invalid_inputs(overrides):
    with pytest.raises(ValueError):
        underwrite_deal(example(**overrides))


def test_scenario_delay_validation():
    with pytest.raises(ValueError):
        downside_scenarios(example(), {"invalid": {"synergy_factor": 1,
                           "cost_factor": 1, "delay_years": 2}})
