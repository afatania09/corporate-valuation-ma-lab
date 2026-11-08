"""Illustrative entry/exit LBO with a debt schedule and gross sponsor returns."""
from .core import lbo_returns
from .transactions import DebtTranche, lbo_debt_schedule

def sponsor_lbo(entry_ebitda, entry_multiple, entry_net_debt, financing_debt,
                transaction_fees, tranches, annual_cash_available,
                exit_ebitda, exit_multiple, exit_cash=0):
    """Cash available is after tax/capex/working capital, before interest.
    Entry net debt affects seller equity value; sponsor funds full enterprise
    purchase price less new acquisition debt, plus transaction fees.
    Assumes seller debt refinanced at close and no other sources/uses.
    """
    if min(entry_ebitda, entry_multiple, financing_debt, transaction_fees,
           exit_ebitda, exit_multiple, exit_cash) < 0:
        raise ValueError("negative input not supported")
    if abs(sum(t.balance for t in tranches)-financing_debt) > 1e-7:
        raise ValueError("tranches must reconcile to financing debt")
    entry_ev = entry_ebitda * entry_multiple
    seller_equity = entry_ev - entry_net_debt
    if seller_equity < 0:
        raise ValueError("negative seller equity: review capital structure")
    sponsor_equity = entry_ev + transaction_fees - financing_debt
    if sponsor_equity <= 0:
        raise ValueError("sponsor entry equity must be positive")
    schedule = lbo_debt_schedule(tranches, annual_cash_available)
    exit_ev = exit_ebitda * exit_multiple
    exit_debt = schedule[-1]["closing_debt"]
    exit_equity = exit_ev - exit_debt + exit_cash
    if exit_equity < 0:
        raise ValueError("negative exit equity: sponsor equity would be wiped out")
    returns = lbo_returns(sponsor_equity, exit_equity, len(schedule))
    return {"entry_ev": entry_ev, "seller_equity": seller_equity,
            "sponsor_equity": sponsor_equity, "entry_financing_debt": financing_debt,
            "exit_ev": exit_ev, "exit_debt": exit_debt, "exit_equity": exit_equity,
            "debt_schedule": schedule, **returns}
