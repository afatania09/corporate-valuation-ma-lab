"""Traceable public financial-data input register and valuation quality gates."""
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from .comparables import Comparable, comparable_summary

@dataclass(frozen=True)
class FinancialEvidence:
    issuer: str
    period_end: str
    filing_date: str
    source_url: str
    currency: str
    enterprise_value: float
    ebitda: float
    data_status: str

    def validate(self):
        if not self.issuer.strip() or not self.currency.strip():
            raise ValueError("issuer and currency required")
        period, filing = date.fromisoformat(self.period_end), date.fromisoformat(self.filing_date)
        if filing < period:
            raise ValueError("filing date cannot precede period end")
        parsed = urlparse(self.source_url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("https source URL required")
        if self.data_status not in ("verified_public", "synthetic"):
            raise ValueError("data_status must be verified_public or synthetic")
        if self.enterprise_value <= 0 or self.ebitda <= 0:
            raise ValueError("positive EV and EBITDA required")
        return self

def load_evidence_csv(path):
    """Read rows with explicitly declared source and verification status."""
    columns = {"issuer", "period_end", "filing_date", "source_url",
               "currency", "enterprise_value", "ebitda", "data_status"}
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if not columns.issubset(reader.fieldnames or []):
            raise ValueError("missing required evidence columns")
        records = []
        for row in reader:
            item = FinancialEvidence(
                issuer=row["issuer"], period_end=row["period_end"],
                filing_date=row["filing_date"], source_url=row["source_url"],
                currency=row["currency"],
                enterprise_value=float(row["enterprise_value"]),
                ebitda=float(row["ebitda"]), data_status=row["data_status"])
            records.append(item.validate())
    if not records:
        raise ValueError("evidence register is empty")
    return records

def evidenced_comparables(records, target_ebitda, currency, as_of_date,
                          allow_synthetic=False):
    cutoff = date.fromisoformat(as_of_date)
    items = list(records)
    if not items:
        raise ValueError("evidence required")
    for r in items:
        r.validate()
        if r.currency != currency:
            raise ValueError("mixed currencies: normalise before comparison")
        if date.fromisoformat(r.filing_date) > cutoff:
            raise ValueError("look-ahead bias: filing date after valuation date")
        if r.data_status != "verified_public" and not allow_synthetic:
            raise ValueError("synthetic data excluded from evidenced valuation")
    result = comparable_summary(
        [Comparable(r.issuer, r.enterprise_value, r.ebitda) for r in items],
        target_ebitda)
    result["evidence_count"] = len(items)
    result["valuation_date"] = as_of_date
    result["currency"] = currency
    result["synthetic_included"] = any(r.data_status == "synthetic" for r in items)
    return result
