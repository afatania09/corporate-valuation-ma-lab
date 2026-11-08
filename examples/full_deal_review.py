"""End-to-end synthetic IC case with sensitivity, memo and audit manifest.

Run: python -m examples.full_deal_review
Writes files to outputs/ (excluded from Git via .gitignore if configured).
"""
from pathlib import Path
import json
from valuation_lab.acquisition_model import AcquisitionInputs, model_acquisition
from valuation_lab.deal_sensitivity import deal_sensitivity
from valuation_lab.audit import audit_manifest
from valuation_lab.memo import investment_committee_memo

a = AcquisitionInputs(
    opening_revenue=100, revenue_growth=.06, ebitda_margin=.24,
    depreciation_pct_revenue=.03, capex_pct_revenue=.05,
    working_capital_pct_revenue=.10, tax_rate=.25,
    entry_ebitda=24, entry_multiple=8, acquisition_debt=100,
    interest_rate=.08, annual_mandatory_amortisation=5,
    transaction_fees=4, exit_multiple=8, years=5)
results = model_acquisition(a)
sensitivity = deal_sensitivity(a, [7, 8, 9], [7, 8, 9])
manifest = audit_manifest("Fictional Healthcare Acquisition", a,
                          {"base": results, "sensitivity": sensitivity},
                          ["Synthetic assumptions only; no market sources"])
folder = Path("outputs")
folder.mkdir(exist_ok=True)
(folder/"investment_committee.md").write_text(
    investment_committee_memo("Fictional Healthcare Acquisition", a, results,
                              valuation_date="2026-09-30"), encoding="utf-8")
(folder/"audit_manifest.json").write_text(
    json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
(folder/"sensitivity.json").write_text(
    json.dumps(sensitivity, indent=2), encoding="utf-8")
print(f"Gross IRR: {results['irr']:.2%} | MOIC: {results['moic']:.2f}x")
print(f"Audit SHA-256: {manifest['sha256']}")
print("Generated outputs/investment_committee.md, audit_manifest.json, sensitivity.json")
