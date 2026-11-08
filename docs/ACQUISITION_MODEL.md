# Linked acquisition / LBO operating model

This model links annual revenue and EBITDA forecasting to acquisition financing,
interest expense, tax, capex, changes in net working capital, mandatory amortisation,
an optional debt cash sweep and gross sponsor exit returns.

## Sources and uses
- Enterprise purchase price = entry EBITDA × entry multiple.
- New financing debt is an acquisition source.
- Sponsor equity = enterprise purchase price + transaction fees − new debt.
- Assumes target existing net debt is refinanced at close and the entry enterprise
  purchase price includes that repayment; no double counting of seller debt.

## Annual cash waterfall
1. Forecast revenue and EBITDA.
2. Calculate interest on opening acquisition debt.
3. Calculate taxes on EBIT less interest, with a zero tax floor.
4. Deduct capex and change in net working capital.
5. Pay interest, mandatory debt amortisation, then optional debt sweep.
6. Retain any excess cash after debt is fully repaid.

## Exit
Exit enterprise value is exit EBITDA × exit multiple. Exit equity adds accumulated
retained cash and subtracts closing acquisition debt. MOIC and IRR are gross sponsor
returns, assuming a single entry and exit with no interim sponsor distributions.

## Limitations
This is a *linked acquisition operating and debt model*, not a fully integrated
post-acquisition balance sheet. It excludes multiple debt tranches, covenant tests,
revolvers, refinancing, cash minimums, fees on exit, debt tax deductibility limits,
NOL carryforwards, management equity and preference waterfalls. Cash sweep is
year-end; interest is calculated on opening debt. No circularity solver is needed.
All sample inputs are fictional.
