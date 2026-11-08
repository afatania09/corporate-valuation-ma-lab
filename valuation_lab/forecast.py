"""Simple linked operating forecast, with balance-sheet working-capital movements."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ForecastAssumptions:
    revenue_growth: float
    ebitda_margin: float
    tax_rate: float
    capex_pct_sales: float
    depreciation_pct_sales: float
    nwc_pct_sales: float

def operating_forecast(start_revenue, start_nwc, years, a: ForecastAssumptions):
    if years < 1 or start_revenue <= 0:
        raise ValueError("years and revenue must be positive")
    if not -1 < a.revenue_growth or not all(0 <= x <= 1 for x in (
        a.ebitda_margin, a.tax_rate, a.capex_pct_sales,
        a.depreciation_pct_sales, a.nwc_pct_sales
    )):
        raise ValueError("invalid forecast assumptions")
    result, revenue, prev_nwc = [], float(start_revenue), float(start_nwc)
    for year in range(1, years + 1):
        revenue *= 1 + a.revenue_growth
        ebitda = revenue * a.ebitda_margin
        depreciation = revenue * a.depreciation_pct_sales
        ebit = ebitda - depreciation
        cash_tax = max(0.0, ebit) * a.tax_rate
        capex = revenue * a.capex_pct_sales
        nwc = revenue * a.nwc_pct_sales
        change_nwc = nwc - prev_nwc
        fcff = ebit - cash_tax + depreciation - capex - change_nwc
        result.append(dict(year=year, revenue=revenue, ebitda=ebitda,
            depreciation=depreciation, ebit=ebit, cash_tax=cash_tax,
            capex=capex, nwc=nwc, change_nwc=change_nwc, fcff=fcff))
        prev_nwc = nwc
    return result
