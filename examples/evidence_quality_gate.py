"""Run the synthetic example with an explicit non-market-data override."""
from valuation_lab.evidence import FinancialEvidence, evidenced_comparables

items = [
    FinancialEvidence("Synthetic Peer A", "2025-12-31", "2026-03-31",
                      "https://example.org/peer-a", "GBP", 120, 15, "synthetic"),
    FinancialEvidence("Synthetic Peer B", "2025-12-31", "2026-04-15",
                      "https://example.org/peer-b", "GBP", 160, 20, "synthetic"),
]
result = evidenced_comparables(items, target_ebitda=14, currency="GBP",
                              as_of_date="2026-09-30", allow_synthetic=True)
print("Synthetic illustrative valuation, not observed market data:")
print(result)
