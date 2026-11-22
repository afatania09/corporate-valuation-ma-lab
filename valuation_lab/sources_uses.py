"""Acquisition closing sources-and-uses bridge with explicit cash/debt treatment.

All figures are positive amounts in the same currency units. Target cash is
acquired and used to reduce the effective enterprise purchase cost only when
the agreed EV-to-equity bridge treats it as cash-like. This module assumes a
cash-free/debt-free enterprise valuation and refinancing of all target debt.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class ClosingInputs:
    offer_enterprise_value: float
    target_debt: float
    target_cash: float
    debt_like_items: float = 0.0
    cash_like_items: float = 0.0
    working_capital_adjustment: float = 0.0
    transaction_fees: float = 0.0
    financing_fees: float = 0.0
    new_acquisition_debt: float = 0.0
    rollover_equity: float = 0.0
    buyer_cash: float = 0.0


def closing_sources_uses(a: ClosingInputs):
    """Return reconciled funding bridge and seller equity consideration.

    Positive working_capital_adjustment increases seller consideration.
    Buyer cash is a funding source, NOT a reduction in the seller price.
    Target debt is refinanced and target cash is swept at closing; thus both
    enter the equity-price bridge and financing uses/sources respectively.
    """
    fields = vars(a)
    for name, v in fields.items():
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v):
            raise ValueError(f"{name} must be a finite number")
        if name != "working_capital_adjustment" and v < 0:
            raise ValueError(f"{name} must be non-negative")
    seller_equity = (a.offer_enterprise_value - a.target_debt
                     - a.debt_like_items + a.target_cash + a.cash_like_items
                     + a.working_capital_adjustment)
    if seller_equity < 0:
        raise ValueError("negative seller equity consideration: review EV bridge")
    if a.rollover_equity > seller_equity:
        raise ValueError("rollover equity exceeds seller equity consideration")
    # Target cash is assumed to be distributed/swept to the buyer at closing,
    # so it is included in equity consideration and separately funded by the sweep.
    uses = {
        "seller_cash_consideration": seller_equity - a.rollover_equity,
        "target_debt_refinancing": a.target_debt,
        "debt_like_settlement": a.debt_like_items,
        "transaction_fees": a.transaction_fees,
        "financing_fees": a.financing_fees,
    }
    sources_excluding_sponsor = {
        "new_acquisition_debt": a.new_acquisition_debt,
        "rollover_equity": a.rollover_equity,
        "buyer_cash": a.buyer_cash,
        "target_cash_sweep": a.target_cash,
        "other_cash_like_sweep": a.cash_like_items,
    }
    # Rollover equity is non-cash consideration: account for it in total uses
    # and sources consistently rather than subtracting it twice.
    uses["rollover_equity_consideration"] = a.rollover_equity
    total_uses = sum(uses.values())
    committed_sources = sum(sources_excluding_sponsor.values())
    sponsor_equity = total_uses - committed_sources
    if sponsor_equity < -1e-9:
        raise ValueError("sources exceed uses: reduce financing or review assumptions")
    sponsor_equity = max(0.0, sponsor_equity)
    sources = {**sources_excluding_sponsor, "new_sponsor_equity": sponsor_equity}
    residual = sum(sources.values()) - total_uses
    if abs(residual) > 1e-8:
        raise ArithmeticError("sources and uses do not reconcile")
    return {
        "seller_equity_value": seller_equity,
        "seller_cash_consideration": uses["seller_cash_consideration"],
        "sources": sources,
        "uses": uses,
        "total_sources": sum(sources.values()),
        "total_uses": total_uses,
        "funding_gap_before_new_sponsor_equity": total_uses - committed_sources,
        "new_sponsor_equity": sponsor_equity,
        "reconciliation_difference": residual,
        "effective_purchase_ev_before_fees": (
            seller_equity + a.target_debt + a.debt_like_items
            - a.target_cash - a.cash_like_items),
    }
