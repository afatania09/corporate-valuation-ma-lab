"""Integrated simplified income statement, balance sheet and cash flow forecast.

All values use consistent currency units. Annual periods, opening-balance interest,
no dividends, no acquisitions, no deferred tax and no equity issuance.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class OpeningBalanceSheet:
    cash: float
    receivables: float
    ppe: float
    payables: float
    debt: float
    equity: float

    def difference(self):
        return self.cash + self.receivables + self.ppe - self.payables - self.debt - self.equity

@dataclass(frozen=True)
class Drivers:
    growth: float
    ebitda_margin: float
    depreciation_pct_revenue: float
    capex_pct_revenue: float
    receivables_pct_revenue: float
    payables_pct_revenue: float
    interest_rate: float
    tax_rate: float
    annual_debt_repayment: float

def integrated_forecast(opening_revenue, opening, drivers, years):
    """Return annual linked statement rows with zero-balance residuals."""
    numbers = [opening_revenue, years, *vars(opening).values(), *vars(drivers).values()]
    if any(not isinstance(v, (int, float)) or not isfinite(v) for v in numbers):
        raise ValueError("all inputs must be finite numbers")
    if not isinstance(years, int) or years < 1 or opening_revenue <= 0:
        raise ValueError("positive revenue and integer years required")
    if abs(opening.difference()) > 1e-7:
        raise ValueError("opening balance sheet does not balance")
    if min(opening.cash, opening.receivables, opening.ppe, opening.payables, opening.debt) < 0:
        raise ValueError("opening assets and liabilities cannot be negative")
    if drivers.growth <= -1 or drivers.annual_debt_repayment < 0:
        raise ValueError("invalid growth or debt repayment")
    rates = (drivers.ebitda_margin, drivers.depreciation_pct_revenue,
             drivers.capex_pct_revenue, drivers.receivables_pct_revenue,
             drivers.payables_pct_revenue, drivers.interest_rate, drivers.tax_rate)
    if any(not 0 <= v <= 1 for v in rates):
        raise ValueError("rates must be in [0,1]")

    revenue = float(opening_revenue)
    cash, ar, ppe, ap, debt, equity = (
        float(opening.cash), float(opening.receivables), float(opening.ppe),
        float(opening.payables), float(opening.debt), float(opening.equity))
    result = []
    for year in range(1, years + 1):
        revenue *= 1 + drivers.growth
        ebitda = revenue * drivers.ebitda_margin
        depreciation = revenue * drivers.depreciation_pct_revenue
        capex = revenue * drivers.capex_pct_revenue
        if depreciation > ppe + capex + 1e-9:
            raise ValueError(f"year {year}: depreciation exceeds available PPE")
        ebit = ebitda - depreciation
        interest = debt * drivers.interest_rate
        pretax = ebit - interest
        taxes = max(0.0, pretax) * drivers.tax_rate
        net_income = pretax - taxes
        next_ar = revenue * drivers.receivables_pct_revenue
        next_ap = revenue * drivers.payables_pct_revenue
        change_ar = next_ar - ar
        change_ap = next_ap - ap
        operating_cash_flow = net_income + depreciation - change_ar + change_ap
        repayment = min(debt, drivers.annual_debt_repayment)
        closing_cash = cash + operating_cash_flow - capex - repayment
        if closing_cash < -1e-9:
            raise ValueError(f"year {year}: funding shortfall; financing required")
        cash = max(0.0, closing_cash)
        ar, ap = next_ar, next_ap
        ppe += capex - depreciation
        debt -= repayment
        equity += net_income
        assets = cash + ar + ppe
        liabilities_equity = ap + debt + equity
        residual = assets - liabilities_equity
        if abs(residual) > 1e-7:
            raise ArithmeticError(f"year {year}: balance sheet residual {residual}")
        result.append({
            "year": year, "revenue": revenue, "ebitda": ebitda,
            "depreciation": depreciation, "ebit": ebit, "interest": interest,
            "pretax_income": pretax, "taxes": taxes, "net_income": net_income,
            "operating_cash_flow": operating_cash_flow, "capex": capex,
            "debt_repayment": repayment, "cash_change": operating_cash_flow-capex-repayment,
            "cash": cash, "receivables": ar, "ppe": ppe, "assets": assets,
            "payables": ap, "debt": debt, "equity": equity,
            "liabilities_and_equity": liabilities_equity,
            "balance_check": residual,
            "unlevered_fcff": ebit - max(0.0, ebit)*drivers.tax_rate
                            + depreciation - capex - change_ar + change_ap,
        })
    return result
