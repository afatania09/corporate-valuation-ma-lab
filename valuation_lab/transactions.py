"""Simplified M&A and LBO modelling; amounts in consistent currency units."""
from dataclasses import dataclass

def acquisition_case(target_ebitda, purchase_multiple, synergies,
                     synergy_multiple, net_debt, fees=0):
    if min(target_ebitda, purchase_multiple, synergies, synergy_multiple, fees) < 0:
        raise ValueError("non-negative operating assumptions required")
    purchase_ev = target_ebitda * purchase_multiple
    target_equity_price = purchase_ev - net_debt
    if target_equity_price < 0:
        raise ValueError("negative equity purchase price: review capital structure")
    synergy_value = synergies * synergy_multiple
    return {"purchase_ev": purchase_ev, "equity_purchase_price": target_equity_price,
            "synergy_value": synergy_value,
            "net_synergy_value_after_fees": synergy_value - fees,
            "effective_ev_after_synergies": purchase_ev - synergy_value + fees}

@dataclass(frozen=True)
class DebtTranche:
    name: str
    balance: float
    interest_rate: float
    annual_amortisation: float

def lbo_debt_schedule(tranches, annual_cash_available):
    """Interest on opening balance, then mandatory amortisation and optional sweep.
    Cash available is after operating expenses, tax and capex but before interest.
    No revolver, refinancing, covenants, or fees.
    """
    balances = [float(t.balance) for t in tranches]
    if any(t.balance < 0 or t.interest_rate < 0 or t.annual_amortisation < 0 for t in tranches):
        raise ValueError("debt inputs must be non-negative")
    rows = []
    for year, cash in enumerate(annual_cash_available, 1):
        interest = sum(b * t.interest_rate for b, t in zip(balances, tranches))
        if cash < interest:
            raise ValueError(f"year {year}: insufficient cash for interest; financing required")
        remaining = cash - interest
        mandatory = []
        for i, t in enumerate(tranches):
            payment = min(balances[i], t.annual_amortisation)
            mandatory.append(payment)
        if sum(mandatory) > remaining + 1e-9:
            raise ValueError(f"year {year}: insufficient cash for mandatory amortisation")
        for i, payment in enumerate(mandatory):
            balances[i] -= payment
        remaining -= sum(mandatory)
        sweep = 0.0
        for i in range(len(balances)):
            payment = min(balances[i], remaining)
            balances[i] -= payment
            remaining -= payment
            sweep += payment
        rows.append({"year": year, "interest": interest,
                     "mandatory_principal": sum(mandatory),
                     "optional_principal": sweep, "closing_debt": sum(balances),
                     "retained_cash": remaining})
    return rows
