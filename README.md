# Corporate Valuation & M&A Lab

**Open-source Python valuation and transaction-modelling portfolio** covering enterprise valuation, private equity portfolio NAV, financial forecasting, acquisitions, leveraged buyouts, purchase accounting and investment committee reporting.

> **Scope:** A reproducible educational and research project. All bundled company examples are fictional. It is not an independent valuation opinion, investment advice, or a claim of IFRS 13 / IPEV / RICS compliance.

## Quick start

Requires Python 3.12 or later.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m examples.portfolio_demo
python -m examples.healthcare_investment_committee
python -m examples.integrated_lbo_case
python -m examples.exit_waterfall_ppa
python -m examples.acquisition_ic_report
```

The last example writes `investment_committee_example.md` in the working directory.

## Model catalogue

| Area | Python module | Main output |
| --- | --- | --- |
| EBITDA multiples and equity bridge | `valuation_lab/core.py` | EV, equity value |
| FCFF discounted cash flow | `valuation_lab/core.py` | DCF enterprise value |
| Private equity portfolio | `valuation_lab/core.py` | Holding fair-value proxy and NAV |
| Operating forecast | `valuation_lab/forecast.py` | Revenue, EBITDA, FCFF |
| Linked three statements | `valuation_lab/three_statement.py` | Income statement, balance sheet, cash flow, balance check |
| Trading comparables | `valuation_lab/comparables.py` | Median multiple and implied EV |
| M&A synergies | `valuation_lab/transactions.py` | Purchase price, synergy valuation |
| Debt schedule | `valuation_lab/transactions.py` | Interest, amortisation, cash sweep |
| Sponsor LBO | `valuation_lab/lbo.py` | Entry/exit equity, IRR, MOIC |
| Linked acquisition LBO | `valuation_lab/acquisition_model.py` | Operating cash flow to debt service to exit equity |
| Multiple sensitivity | `valuation_lab/sensitivity.py` | Scenario grid |
| Scenario-weighted equity | `valuation_lab/portfolio_scenarios.py` | Probability-weighted equity |
| Preferred equity waterfall | `valuation_lab/waterfall.py` | Preference vs conversion proceeds |
| Acquisition PPA | `valuation_lab/ppa.py` | Identifiable net assets, DTL, goodwill |
| Investment committee memo | `valuation_lab/memo.py` | Markdown IC report |

## Representative fictional healthcare transaction

- Entry EBITDA: £24m
- Entry EV/EBITDA: 8.0x
- Entry enterprise value: £192m
- Acquisition financing debt: £100m
- Transaction fees: £4m
- Sponsor equity contribution: **£96m**
- Five-year operating forecast with debt service and exit-value bridge

Run `python -m examples.acquisition_ic_report` to calculate actual projected results and generate the investment committee report. Figures are fictional, not observed market data.

## Quality controls

- Pytest tests under `tests/`
- GitHub Actions workflow at `.github/workflows/tests.yml`
- Input validation and explicit exceptions for funding shortfalls
- Three-statement balance checks and debt roll-forward assertions
- Written methodology, assumptions, and model limitations in `docs/`

## Important limitations

This is **not** a commercial-grade audited valuation system. In particular, the acquisition model does not produce a full post-deal consolidated balance sheet; the PPA is a simplified 100% acquisition bridge; the preferred equity waterfall models only one non-participating class; and the fund NAV model assumes pro-rata ordinary equity. No independent market data are bundled or silently fabricated.

Read `docs/METHODOLOGY.md`, `docs/THREE_STATEMENT_LBO.md`, `docs/ADVANCED_VALUATION.md`, and `docs/ACQUISITION_MODEL.md` before relying on results.

## Future professional extensions

Real-company cases using traceable filings and dates, robust multi-tranche capital structures, purchase accounting, IFRS 13 calibration, independent model review and valuation memos with cited market evidence.

## License

See `LICENSE` (MIT, if selected at repository creation).
