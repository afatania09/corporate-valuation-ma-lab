"""Fictional investment committee illustration; run as a Python module."""
from valuation_lab.three_statement import OpeningBalanceSheet, Drivers, integrated_forecast
from valuation_lab.transactions import DebtTranche
from valuation_lab.lbo import sponsor_lbo

opening = OpeningBalanceSheet(cash=10, receivables=20, ppe=100,
                              payables=10, debt=50, equity=70)
drivers = Drivers(growth=.05, ebitda_margin=.25, depreciation_pct_revenue=.03,
                  capex_pct_revenue=.05, receivables_pct_revenue=.20,
                  payables_pct_revenue=.10, interest_rate=.08, tax_rate=.25,
                  annual_debt_repayment=5)
rows = integrated_forecast(100, opening, drivers, 5)
print("Year | Revenue | EBITDA | Cash | Debt | Balance check")
for row in rows:
    print(f"{row['year']:4} | {row['revenue']:7.2f} | {row['ebitda']:6.2f} | "
          f"{row['cash']:5.2f} | {row['debt']:5.2f} | {row['balance_check']:.2e}")

deal = sponsor_lbo(entry_ebitda=20, entry_multiple=8, entry_net_debt=30,
                   financing_debt=100, transaction_fees=5,
                   tranches=[DebtTranche("Senior", 80, .08, 5),
                             DebtTranche("Junior", 20, .12, 0)],
                   annual_cash_available=[25, 27, 30, 32, 35],
                   exit_ebitda=25, exit_multiple=8)
print(f"Entry sponsor equity: {deal['sponsor_equity']:.2f}")
print(f"Exit sponsor equity: {deal['exit_equity']:.2f}")
print(f"Gross MOIC: {deal['moic']:.2f}x | gross IRR: {deal['irr']:.2%}")
