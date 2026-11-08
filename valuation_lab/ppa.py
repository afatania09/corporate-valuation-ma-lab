"""Simplified acquisition purchase price allocation and goodwill bridge.

Purchase consideration, acquired net assets and fair-value uplifts are in the
same currency. Assumes 100% acquisition, no NCI, no contingent consideration,
no pre-existing interests, no deferred tax on non-intangible asset uplifts.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Intangible:
    name: str
    fair_value: float
    tax_basis: float = 0.0

def purchase_price_allocation(consideration, book_net_assets, asset_uplifts,
                              intangibles, tax_rate):
    if consideration < 0 or not 0 <= tax_rate <= 1:
        raise ValueError("invalid consideration or tax rate")
    items = list(intangibles)
    if any(i.fair_value < 0 or i.tax_basis < 0 for i in items):
        raise ValueError("intangible values and tax bases must be nonnegative")
    if any(i.tax_basis > i.fair_value for i in items):
        raise ValueError("tax basis above fair value requires separate tax analysis")
    intangible_fv = sum(i.fair_value for i in items)
    deferred_tax_liability = sum((i.fair_value-i.tax_basis)*tax_rate for i in items)
    identifiable_net_assets = (book_net_assets + asset_uplifts
                               + intangible_fv - deferred_tax_liability)
    goodwill = consideration - identifiable_net_assets
    return {"consideration": consideration, "book_net_assets": book_net_assets,
            "asset_uplifts": asset_uplifts, "intangible_fair_value": intangible_fv,
            "deferred_tax_liability": deferred_tax_liability,
            "identifiable_net_assets": identifiable_net_assets,
            "goodwill": goodwill,
            "reconciliation": identifiable_net_assets + goodwill - consideration}
