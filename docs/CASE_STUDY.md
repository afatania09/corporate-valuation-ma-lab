# Case study: Fictional healthcare platform acquisition

**Purpose:** Demonstrate a complete traceable analysis workflow, not recommend an investment.

**Valuation date:** 30 September 2026 (illustrative date).

**Assumptions:** £24m entry EBITDA, 8.0x entry EV/EBITDA, £100m acquisition financing, £4m transaction fees, 6% annual revenue growth, 24% EBITDA margin, 8% debt interest, 25% tax rate, five-year exit at 8.0x EBITDA. The model is intentionally synthetic.

**Key questions for an investment committee:**
1. Is £24m maintainable EBITDA supported by recurring earnings, or are there one-offs?
2. What observable peer and transaction evidence supports 8.0x?
3. How does a 7.0x exit multiple affect sponsor returns?
4. How robust are debt service and working-capital forecasts?
5. Are refinancing risks, management equity and transaction taxes material?
6. Is the investment thesis driven by EBITDA growth, deleveraging or multiple expansion?

**Reproduce:** `python -m examples.full_deal_review`.

**Outputs:** An investment committee memo, 3×3 entry/exit multiple sensitivity, and a SHA-256 audit manifest. The hash verifies that the represented model inputs and results have not changed between runs; it does not verify their economic accuracy.

**Data provenance:** No real-company financial data are used. To convert this into a public-company case, add a source register recording document URL, issuer, filing date, reporting period, accounting currency, line item and reconciliation to the financial statements. Do not label synthetic assumptions as historical observations.
