"""Hilton historical buyout context with explicitly hypothetical underwriting.

Historical context: Blackstone acquired Hilton in 2007 for approximately
$26 billion including debt. Hilton returned to public markets in 2013.
Reference: Hilton Worldwide Holdings 2013 Form S-1, SEC CIK 1585689.
All numerical underwriting assumptions below are illustrative, not actual
Blackstone cash flows, financing terms or realised investment returns.
"""
import json

def scenario(entry_ev=26.0, entry_debt=20.0, exit_ebitda=3.0,
             exit_multiple=12.0, exit_debt=12.0, years=6):
    if not 0 <= entry_debt < entry_ev or min(exit_ebitda, exit_multiple, exit_debt)<0 or years<=0:
        raise ValueError("Invalid underwriting assumptions")
    equity=entry_ev-entry_debt
    exit_equity=max(0,exit_ebitda*exit_multiple-exit_debt)
    moic=exit_equity/equity
    return dict(entry_equity=equity,exit_equity=exit_equity,moic=moic,
                annualised_return=moic**(1/years)-1,
                debt_reduction=entry_debt-exit_debt)

def analyse():
    return {"units":"USD billions","historical_context":"2007 buyout; 2013 IPO",
            "source_locator":"https://www.sec.gov/edgar/browse/?CIK=1585689",
            "assumptions":"Hypothetical financing, EBITDA, exit multiples and debt; no interim distributions or fees.",
            "scenarios":[dict(name=n,exit_ebitda=e,exit_multiple=m,exit_debt=d,
                              **scenario(exit_ebitda=e,exit_multiple=m,exit_debt=d))
                         for n,e,m,d in [("downside",2,9,16),("base",3,12,12),("upside",4,14,8)]]}

if __name__=="__main__":
    print(json.dumps(analyse(),indent=2))
