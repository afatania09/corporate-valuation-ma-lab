# Delivery roadmap

## Implemented
- EV/EBITDA valuation and EV-to-equity bridge
- Unlevered FCFF DCF with Gordon terminal value
- Ordinary-share portfolio NAV and gross LBO return metrics
- Revenue-driven operating forecast with EBITDA, depreciation, tax, capex and net working capital
- Comparable-company multiple statistics
- M&A purchase price and synergy sensitivity
- Simplified debt amortisation / excess-cash sweep
- Automated unit tests and GitHub Actions

## Next engineering milestones
1. Fully integrated three-statement forecast: debt, interest, retained earnings, balance-sheet check.
2. LBO entry/exit cap table, financing fees, distributions, management incentive plan, preferred equity and waterfall.
3. Accretion/dilution using buyer share price, financing mix, incremental interest, purchase accounting and tax effects.
4. Instrument-level fair value, IFRS 3 PPA, impairment and scenario-weighted recoveries.
5. Public-data case studies with dated citations and reproducible data provenance.
6. Valuation memos, model audit logs, parameter governance and independent QA.

## Important scope
Current calculations are deliberately simplified educational prototypes, not professional valuation opinions. Do not claim the repository contains a full integrated three-statement model or a complete LBO until those are implemented.
