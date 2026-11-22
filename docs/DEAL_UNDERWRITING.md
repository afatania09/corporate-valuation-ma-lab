# Strategic M&A underwriting and bid discipline

This workstream adds **buyer-side investment decision modelling** to the existing DCF, comparables, LBO, PPA and audit modules. Inputs in the example are entirely fictional and expressed in GBP millions.

## Questions answered

1. What is the target worth without the acquisition? `standalone_ev`.
2. How much are expected *incremental* cost or revenue synergies worth, after tax?
3. How much capital must be spent to achieve those synergies?
4. Does the purchase premium leave positive economic value for the acquirer?
5. What is the **maximum break-even enterprise-value offer**, and how does it change in downside scenarios?

## Formulae

For year t, after-tax synergy = run-rate synergy × realised fraction × (1 − tax rate).

Explicit synergy PV = sum(after-tax synergy / (1 + discount rate)^t).

Integration costs are discounted after tax using the simplifying assumption that costs are deductible in the year incurred.

Optional terminal PV = final-year after-tax synergy × (1 + g) / (r − g) / (1 + r)^N.

**Net synergy NPV = explicit synergy PV + terminal synergy PV − PV of integration costs.**

**Acquirer NPV = net synergy NPV − (offer EV − standalone EV).**

**Maximum break-even offer EV = standalone EV + net synergy NPV.**

A positive NPV is a necessary commercial screen, not a complete transaction recommendation. Headroom equals maximum EV less the proposed offer EV.

## Downside design

The sample runs base, downside (30% synergy haircut, 30% cost overrun, one-year delay), and severe (60% synergy haircut, 60% cost overrun, two-year delay) scenarios. Delays shift the synergy realisation schedule without shifting integration spending: a conservative implementation assumption. Scenario shocks are explicitly documented and not probabilities.

## Professional review points

- Reconcile EV to equity consideration, acquired debt, working-capital adjustments and sources/uses separately; this model does **not** perform that reconciliation.
- Validate incremental synergies against overlap with management's standalone plan, and assign owners, dependencies, costs and delivery dates.
- A perpetuity can overvalue synergies; review contract duration, churn, competition, one-off benefits and whether integration benefits remain defensible beyond the forecast.
- The example assumes a single discount rate, constant tax rate, immediate tax deductibility of integration expenses, no tax loss restrictions, and annual year-end cash flows.
- No probability-weighting or financing tax shield is applied; risks should be explicitly reviewed rather than double counted in both cash flows and discount rates.
- EV and cash-flow conventions must be consistent. The standalone value is an externally supplied assumption, not calculated by this module.
- This is **not** an EPS accretion/dilution analysis, financing model, fairness opinion, IFRS 3 purchase accounting, or an investment recommendation.

## Run

```bash
python -m examples.strategic_acquisition_underwriting
python -m pytest -q
```

To make this suitable for a real acquisition, next add public-company filings (with valuation dates and citations), explicit target operational diligence, separation of revenue/cost synergies, funding sources/uses, debt covenants, tax analysis, probability-weighted deal risks and an independently reviewed committee memo.
