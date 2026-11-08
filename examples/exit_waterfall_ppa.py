"""Synthetic preferred-equity exit and acquisition-accounting example."""
from valuation_lab.waterfall import Preferred, allocate_exit_proceeds
from valuation_lab.ppa import Intangible, purchase_price_allocation
from valuation_lab.portfolio_scenarios import Scenario, scenario_weighted_equity

for exit_equity in (50, 100, 300):
    print(f"Exit equity {exit_equity}:", allocate_exit_proceeds(
        exit_equity, Preferred(invested=40, liquidation_multiple=1.5,
                              as_converted_fraction=.3)))

print("PPA:", purchase_price_allocation(
    consideration=200, book_net_assets=100, asset_uplifts=10,
    intangibles=[Intangible("Brand", 30),
                 Intangible("Customer relationships", 20, 5)],
    tax_rate=.25))
print("Scenarios:", scenario_weighted_equity([
    Scenario("Downside", .25, 10, 6, 80),
    Scenario("Base", .5, 15, 8, 30),
    Scenario("Upside", .25, 20, 10, 20)]))
