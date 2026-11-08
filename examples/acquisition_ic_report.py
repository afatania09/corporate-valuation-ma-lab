"""Generate a fictional acquisition memo: python -m examples.acquisition_ic_report"""
from pathlib import Path
from valuation_lab.acquisition_model import AcquisitionInputs, model_acquisition
from valuation_lab.memo import investment_committee_memo

a = AcquisitionInputs(
    opening_revenue=100, revenue_growth=.06, ebitda_margin=.24,
    depreciation_pct_revenue=.03, capex_pct_revenue=.05,
    working_capital_pct_revenue=.10, tax_rate=.25,
    entry_ebitda=24, entry_multiple=8, acquisition_debt=100,
    interest_rate=.08, annual_mandatory_amortisation=5,
    transaction_fees=4, exit_multiple=8, years=5)
result = model_acquisition(a)
memo = investment_committee_memo("Fictional Healthcare Platform", a, result,
                                 valuation_date="2026-09-30")
path = Path("investment_committee_example.md")
path.write_text(memo, encoding="utf-8")
print(f"Wrote {path}; MOIC={result['moic']:.2f}x IRR={result['irr']:.2%}")
