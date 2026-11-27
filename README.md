# Corporate Valuation & M&A Lab

**Open-source Python valuation and transaction-modelling portfolio** covering enterprise valuation, private equity portfolio NAV, financial forecasting, acquisitions, leveraged buyouts, purchase accounting and investment committee reporting.

> **Scope:** A reproducible educational and research project. Most bundled examples are fictional; historical cases explicitly identify their public sources. It is not an independent valuation opinion, investment advice, or a claim of IFRS 13 / IPEV / RICS compliance.

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
python -m examples.full_deal_review
python -m examples.evidence_quality_gate
python -m examples.strategic_acquisition_underwriting
python -m examples.acquisition_closing_bridge
```

The acquisition IC example writes `investment_committee_example.md`. The full deal review creates `outputs/investment_committee.md`, `outputs/sensitivity.json`, and `outputs/audit_manifest.json`.

## Interactive dashboard

```bash
python -m pip install -r requirements-dashboard.txt
python -m streamlit run dashboard.py
```

The dashboard exposes sponsor LBO and annualised merger EPS scenarios with editable assumptions and downloadable CSV results and a formula-linked editable LBO Excel workbook. It runs locally; no hosted deployment is claimed. Inputs are illustrative, not investment recommendations.

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
| Deal sensitivity | `valuation_lab/deal_sensitivity.py` | Entry/exit multiple return grid |
| Audit manifest | `valuation_lab/audit.py` | Deterministic input/result SHA-256 |
| Acquisition sources and uses | `valuation_lab/sources_uses.py` | EV-to-equity price bridge, closing financing and reconciliation | 
| Strategic acquisition bid underwriting | `valuation_lab/deal_underwriting.py` | After-tax synergy NPV, acquisition bid ceiling, buyer NPV and downside cases |
| Evidence quality gates | `valuation_lab/evidence.py` | Source register, date/currency checks, synthetic-data controls |

## Representative fictional healthcare transaction

- Entry EBITDA: £24m
- Entry EV/EBITDA: 8.0x
- Entry enterprise value: £192m
- Acquisition financing debt: £100m
- Transaction fees: £4m
- Sponsor equity contribution: **£96m**
- Five-year operating forecast with debt service and exit-value bridge

Run `python -m examples.acquisition_ic_report` to calculate actual projected results and generate the investment committee report. Figures are fictional, not observed market data.

## Strategic M&A underwriting example

Run `python -m examples.strategic_acquisition_underwriting` to compare base, downside and severe acquisition cases. The model calculates after-tax synergy cash flows, integration spending, a break-even maximum enterprise-value bid and buyer value creation or destruction. It is an **unlevered strategic acquisition screen**, not an EPS accretion or purchase accounting model. All example assumptions are fictional. See [deal underwriting methodology](docs/DEAL_UNDERWRITING.md).

## Acquisition financing and completion bridge

Run `python -m examples.acquisition_closing_bridge` for a fictional transaction showing seller equity consideration, refinancing, seller rollover, financing fees, buyer cash, target cash sweep and the residual sponsor equity requirement. The sources and uses are reconciled to zero. The module assumes freely sweepable target cash and full refinancing of target debt; see [completion bridge methodology](docs/SOURCES_AND_USES.md).

## Real transaction: Microsoft / Activision Blizzard

Run `python -m examples.microsoft_activision_case` to reconstruct the final $75.408bn purchase accounting disclosed in Microsoft's FY2025 Form 10-K, and calculate hypothetical perpetual FCFF hurdles across discount-rate and growth scenarios. The case is retrospective, not an independent valuation or measured deal return.

The `valuation_lab/merger_eps.py` module separately screens annualised EPS accretion/dilution under mixed acquisition funding.

## Historical context: Blackstone / Hilton

Run `python -m examples.hilton_lbo_case` for a stylised sponsor underwriting scenario anchored to the approximately $26bn 2007 buyout and six-year period to the 2013 IPO. Financing, exit EBITDA, multiples and debt are hypothetical; the IPO is not treated as an actual full sponsor exit. Annualised returns assume a single terminal distribution and omit fees and interim cash flows. See Hilton's 2013 Form S-1 via SEC EDGAR (CIK 1585689) for historical context.

## Quality controls

- Pytest tests under `tests/`
- GitHub Actions workflow at `.github/workflows/tests.yml`
- Input validation and explicit exceptions for funding shortfalls
- Three-statement balance checks and debt roll-forward assertions
- Written methodology, assumptions, and model limitations in `docs/`

## Important limitations

This is **not** a commercial-grade audited valuation system. In particular, the acquisition model does not produce a full post-deal consolidated forecast (a separate simplified acquisition-date balance sheet bridge is available in `valuation_lab/consolidation.py`); the PPA is a simplified 100% acquisition bridge; the preferred equity waterfall models only one non-participating class; and the fund NAV model assumes pro-rata ordinary equity. Historical accounting disclosures are separately sourced; no live market dataset is bundled.

Read `docs/SOURCES_AND_USES.md`, `docs/DEAL_UNDERWRITING.md`, `docs/METHODOLOGY.md`, `docs/THREE_STATEMENT_LBO.md`, `docs/ADVANCED_VALUATION.md`, `docs/ACQUISITION_MODEL.md`, and `docs/DATA_PROVENANCE.md` before relying on results.

## Release verification checklist

- Run `python -m pip install -r requirements-dev.txt -r requirements-dashboard.txt`.
- Run `python -m pytest -q` and inspect failures before release.
- Launch `python -m streamlit run dashboard.py` and exercise both tabs.
- Download the LBO workbook, open in Excel, and reconcile recalculated outputs against the dashboard.
- Verify historical accounting figures against original filings; hypothetical Hilton returns are not actual sponsor returns.
- Review acquisition-date consolidation assumptions: 100% cash purchase, no minority interests, no existing ownership, fees expensed.

## Future professional extensions

Real-company cases using traceable filings and dates, robust multi-tranche capital structures, purchase accounting, IFRS 13 calibration, independent model review and valuation memos with cited market evidence.

## License

See `LICENSE` (MIT, if selected at repository creation).
