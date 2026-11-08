"""Integrated operating forecast and acquisition debt/cash waterfall.

Simplified annual model. Interest uses opening balances; principal repaid at
year-end. Tax is based on acquisition debt interest, not target legacy debt.
No NOLs, fees financing, revolver, deferred tax or circular interest.
"""
from dataclasses import dataclass
from .core import lbo_returns

@dataclass(frozen=True)
class AcquisitionInputs:
    opening_revenue: float
    revenue_growth: float
    ebitda_margin: float
    depreciation_pct_revenue: float
    capex_pct_revenue: float
    working_capital_pct_revenue: float
    tax_rate: float
    entry_ebitda: float
    entry_multiple: float
    acquisition_debt: float
    interest_rate: float
    annual_mandatory_amortisation: float
    transaction_fees: float
    exit_multiple: float
    years: int

def model_acquisition(a: AcquisitionInputs):
    if not isinstance(a.years, int) or a.years < 1:
        raise ValueError("years must be a positive integer")
    values = vars(a)
    if any(not isinstance(v, (int, float)) or not float("-inf") < v < float("inf") for v in values.values()):
        raise ValueError("inputs must be finite numbers")
    if a.opening_revenue <= 0 or a.entry_ebitda <= 0 or a.revenue_growth <= -1:
        raise ValueError("invalid revenue or growth")
    if any(not 0 <= r <= 1 for r in (a.ebitda_margin, a.depreciation_pct_revenue,
             a.capex_pct_revenue, a.working_capital_pct_revenue, a.tax_rate, a.interest_rate)):
        raise ValueError("rates must be in [0,1]")
    if min(a.entry_multiple, a.acquisition_debt, a.annual_mandatory_amortisation,
           a.transaction_fees, a.exit_multiple) < 0:
        raise ValueError("negative financing inputs")
    entry_ev = a.entry_ebitda * a.entry_multiple
    sponsor_equity = entry_ev + a.transaction_fees - a.acquisition_debt
    if sponsor_equity <= 0:
        raise ValueError("sponsor equity must be positive")
    revenue = a.opening_revenue
    nwc = revenue * a.working_capital_pct_revenue
    debt = a.acquisition_debt
    rows = []
    for year in range(1, a.years + 1):
        revenue *= 1 + a.revenue_growth
        ebitda = revenue * a.ebitda_margin
        depreciation = revenue * a.depreciation_pct_revenue
        ebit = ebitda - depreciation
        interest = debt * a.interest_rate
        taxes = max(0, ebit - interest) * a.tax_rate
        capex = revenue * a.capex_pct_revenue
        next_nwc = revenue * a.working_capital_pct_revenue
        delta_nwc = next_nwc - nwc
        nwc = next_nwc
        cash_before_debt_service = ebitda - taxes - capex - delta_nwc
        cash_after_interest = cash_before_debt_service - interest
        if cash_after_interest < -1e-9:
            raise ValueError(f"year {year}: insufficient cash to service interest")
        mandatory = min(debt, a.annual_mandatory_amortisation)
        if cash_after_interest + 1e-9 < mandatory:
            raise ValueError(f"year {year}: insufficient cash for mandatory amortisation")
        optional = min(debt-mandatory, max(0, cash_after_interest-mandatory))
        debt -= mandatory + optional
        retained_cash = max(0, cash_after_interest-mandatory-optional)
        rows.append({"year": year, "revenue": revenue, "ebitda": ebitda,
                     "ebit": ebit, "interest": interest, "taxes": taxes,
                     "capex": capex, "change_nwc": delta_nwc,
                     "cash_before_debt_service": cash_before_debt_service,
                     "mandatory_repayment": mandatory, "optional_repayment": optional,
                     "closing_debt": debt, "retained_cash": retained_cash})
    # Accumulate unused cash (once debt is repaid) at exit; no interest earned.
    exit_cash = sum(row["retained_cash"] for row in rows)
    exit_ev = rows[-1]["ebitda"] * a.exit_multiple
    exit_equity = max(0, exit_ev - debt + exit_cash)
    return {"entry_ev": entry_ev, "sponsor_equity": sponsor_equity,
            "exit_ev": exit_ev, "exit_debt": debt, "exit_cash": exit_cash,
            "exit_equity": exit_equity, "years": rows,
            **lbo_returns(sponsor_equity, exit_equity, a.years)}
