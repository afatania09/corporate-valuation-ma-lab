import csv
import pytest
from valuation_lab.evidence import FinancialEvidence, load_evidence_csv, evidenced_comparables

def item(**changes):
    args = dict(issuer="Example", period_end="2025-12-31",
                filing_date="2026-03-31",
                source_url="https://example.org/annual-report",
                currency="GBP", enterprise_value=120, ebitda=15,
                data_status="synthetic")
    args.update(changes)
    return FinancialEvidence(**args)

def test_lookahead_rejected():
    with pytest.raises(ValueError, match="look-ahead"):
        evidenced_comparables([item()], 10, "GBP", "2026-01-01", allow_synthetic=True)

def test_synthetic_cannot_pass_as_verified():
    with pytest.raises(ValueError, match="synthetic"):
        evidenced_comparables([item()], 10, "GBP", "2026-09-30")

def test_synthetic_demo_explicitly_permitted():
    r = evidenced_comparables([item()], 10, "GBP", "2026-09-30", allow_synthetic=True)
    assert r["implied_ev"] == pytest.approx(80)
    assert r["synthetic_included"] is True

def test_currency_mismatch():
    with pytest.raises(ValueError, match="mixed currencies"):
        evidenced_comparables([item(currency="USD")], 10, "GBP", "2026-09-30", True)

def test_bad_url():
    with pytest.raises(ValueError, match="https"):
        item(source_url="not-a-url").validate()

def test_csv_loader(tmp_path):
    file = tmp_path / "evidence.csv"
    with file.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(vars(item()).keys()))
        writer.writeheader()
        writer.writerow(vars(item()))
    assert load_evidence_csv(file)[0].issuer == "Example"
