"""Run: python -m examples.portfolio_demo"""
from valuation_lab.core import Holding, portfolio_nav, enterprise_value, equity_value, dcf_enterprise_value, lbo_returns

holdings = [
    Holding("Technology", 20, 10, 40, .8),
    Holding("Healthcare", 15, 9, 25, .65),
    Holding("Manufacturing", 12, 7, 30, 1),
    Holding("Retail", 8, 6, 20, .7),
    Holding("Logistics", 10, 8, 15, .9),
]
for h in holdings:
    ev = enterprise_value(h.ebitda, h.multiple)
    print(f"{h.name:15} EV £{ev:7.2f}m | equity £{equity_value(ev,h.net_debt):7.2f}m | fund £{h.fund_value():7.2f}m")
print(f"Fund NAV: £{portfolio_nav(holdings, 12, 7):.2f}m")
print(f"DCF EV: £{dcf_enterprise_value([12,14,16,18,20], .10, .025):.2f}m")
print(f"LBO: {lbo_returns(100, 200, 5)}")
