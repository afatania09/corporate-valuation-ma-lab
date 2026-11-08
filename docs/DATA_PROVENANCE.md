# Evidence policy and public-market-data provenance

The repository deliberately does not invent public-company market prices, EBITDA
or transaction multiples. A public-company case should record each source and
the valuation date before any multiple is calculated.

## Register schema

Use a UTF-8 CSV with columns:

`issuer,period_end,filing_date,source_url,currency,enterprise_value,ebitda,data_status`

- `period_end`: fiscal period end (ISO YYYY-MM-DD).
- `filing_date`: date source became public; must not be after valuation date.
- `source_url`: original public filing or documented valuation evidence URL.
- `currency`: a consistent reporting currency; convert all amounts before analysis.
- `enterprise_value`: independently reconciled market capitalisation + net debt and adjustments at an appropriate measurement date.
- `ebitda`: reconciled historical/forward maintainable earnings, with accounting policy consistency.
- `data_status`: `verified_public` only after manual source reconciliation; otherwise `synthetic`.

## Quality gates

`evidenced_comparables` rejects look-ahead bias, mixed currencies, missing sources
and synthetic data unless the caller explicitly sets `allow_synthetic=True`.

**Caveat:** The software checks *metadata consistency*, not that a URL contains the
claimed figures. Marking a row `verified_public` is a human attestation, not
independent verification by the program. EV and EBITDA dates can differ and must
be reconciled separately. The register is a starting point, not a complete
market approach or fair-value compliance system.

For a real case study, attach documented source excerpts, valuation-date market
capitalisation, fully diluted shares, lease/debt adjustments, non-recurring
earnings adjustments, and a written comparable selection rationale.
