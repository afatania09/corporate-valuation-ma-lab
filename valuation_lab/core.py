"""Core financial valuation methods. Cash flows are unlevered and year-end."""
from dataclasses import dataclass
from math import isfinite

def _number(value, label):
    if not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)

def enterprise_value(ebitda, multiple):
    """Trading-comparable enterprise value; EBITDA and EV share currency units."""
    e = _number(ebitda, "ebitda")
    m = _number(multiple, "multiple")
    if m < 0:
        raise ValueError("multiple must be non-negative")
    return e * m

def equity_value(ev, net_debt, other_adjustments=0):
    """Simplified EV-to-equity bridge; positive adjustments increase equity."""
    return _number(ev, "ev") - _number(net_debt, "net_debt") + _number(other_adjustments, "other_adjustments")

def dcf_enterprise_value(cash_flows, wacc, terminal_growth):
    """FCFF DCF using Gordon-growth terminal value; rates are decimals."""
    flows = [_number(v, "cash flow") for v in cash_flows]
    r = _number(wacc, "wacc")
    g = _number(terminal_growth, "terminal_growth")
    if not flows or r <= g or r <= -1 or g <= -1:
        raise ValueError("require nonempty cash flows, WACC > growth, and rates > -100%")
    explicit = sum(cf / (1 + r) ** t for t, cf in enumerate(flows, 1))
    terminal = flows[-1] * (1 + g) / (r - g)
    return explicit + terminal / (1 + r) ** len(flows)

@dataclass(frozen=True)
class Holding:
    name: str
    ebitda: float
    multiple: float
    net_debt: float
    ownership: float

    def fund_value(self):
        if not 0 <= self.ownership <= 1:
            raise ValueError("ownership must be between 0 and 1")
        return equity_value(enterprise_value(self.ebitda, self.multiple), self.net_debt) * self.ownership

def portfolio_nav(holdings, fund_cash=0, fund_liabilities=0):
    """Simplified ordinary-share NAV, excluding preferences and carry."""
    return sum(h.fund_value() for h in holdings) + _number(fund_cash, "fund_cash") - _number(fund_liabilities, "fund_liabilities")

def lbo_returns(entry_equity, exit_equity, years):
    """Gross equity MOIC and annualised IRR, with no interim distributions."""
    entry = _number(entry_equity, "entry_equity")
    exit_ = _number(exit_equity, "exit_equity")
    t = _number(years, "years")
    if entry <= 0 or exit_ < 0 or t <= 0:
        raise ValueError("entry equity and years must be positive; exit equity non-negative")
    moic = exit_ / entry
    return {"moic": moic, "irr": moic ** (1 / t) - 1}
