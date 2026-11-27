"""Annualised merger EPS screen; monetary inputs and shares in consistent units."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class MergerInputs:
    buyer_net_income: float
    buyer_shares: float
    buyer_share_price: float
    target_net_income: float
    equity_purchase_price: float
    stock_fraction: float
    debt_fraction: float
    debt_rate: float
    cash_yield: float
    tax_rate: float
    pretax_synergies: float = 0.0
    pretax_integration_cost: float = 0.0
    pretax_incremental_amortisation: float = 0.0

def merger_eps(x: MergerInputs) -> dict[str, float | None]:
    """Assumes full-year ownership, fixed financing and usable tax shields.

    Target earnings are retained after existing interest; no target debt
    refinancing is assumed. Cash funding is the residual consideration.
    """
    if not all(isfinite(v) for v in vars(x).values()):
        raise ValueError("Inputs must be finite")
    if min(x.buyer_shares, x.buyer_share_price) <= 0 or x.equity_purchase_price < 0:
        raise ValueError("Invalid shares, price or consideration")
    if not all(0 <= v <= 1 for v in (x.stock_fraction, x.debt_fraction, x.tax_rate)):
        raise ValueError("Invalid fractions")
    if x.stock_fraction + x.debt_fraction > 1:
        raise ValueError("Funding fractions exceed consideration")
    if min(x.debt_rate, x.cash_yield, x.pretax_integration_cost, x.pretax_incremental_amortisation) < 0:
        raise ValueError("Negative financing rate or expense")
    stock = x.equity_purchase_price * x.stock_fraction
    debt = x.equity_purchase_price * x.debt_fraction
    cash = x.equity_purchase_price - stock - debt
    new_shares = stock / x.buyer_share_price
    adjustment = (x.pretax_synergies - x.pretax_integration_cost -
                  x.pretax_incremental_amortisation - debt*x.debt_rate -
                  cash*x.cash_yield) * (1-x.tax_rate)
    standalone = x.buyer_net_income / x.buyer_shares
    combined_income = x.buyer_net_income + x.target_net_income + adjustment
    combined_eps = combined_income / (x.buyer_shares + new_shares)
    return {"stock_funding": stock, "debt_funding": debt, "cash_funding": cash,
            "new_shares": new_shares, "combined_net_income": combined_income,
            "standalone_eps": standalone, "combined_eps": combined_eps,
            "eps_change": combined_eps-standalone,
            "accretion_pct": 100*(combined_eps/standalone-1) if standalone > 0 else None}
