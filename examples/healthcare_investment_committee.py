"""Fictional healthcare investment committee challenge case."""
from valuation_lab.comparables import Comparable, comparable_summary
from valuation_lab.core import equity_value
from valuation_lab.sensitivity import multiple_sensitivity
from valuation_lab.transactions import acquisition_case

reported_ebitda = 15
temporary_savings = 1
maintainable_ebitda = reported_ebitda - temporary_savings
net_debt = 25
comps = [Comparable("Peer A", 70, 10), Comparable("Peer B", 84, 12),
         Comparable("Peer C", 64, 8)]
valuation = comparable_summary(comps, maintainable_ebitda)
print("Fictional healthcare valuation challenge")
print(f"Reported EBITDA £{reported_ebitda}m; maintainable £{maintainable_ebitda}m")
print(f"Peer median: {valuation['median_multiple']:.1f}x")
print(f"Enterprise value: £{valuation['implied_ev']:.1f}m")
print(f"Equity value: £{equity_value(valuation['implied_ev'], net_debt):.1f}m")
print("Sensitivity (EBITDA / multiple / equity value)")
for cell in multiple_sensitivity([13, 14, 15], [7, 8, 9], net_debt):
    print(f"{cell['ebitda']:>2} / {cell['multiple']:>2}x / £{cell['equity_value']:.1f}m")
print("Illustrative purchase:", acquisition_case(14, 7, 2, 6, 25, 3))
