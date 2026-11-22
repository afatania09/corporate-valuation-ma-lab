"""Investment committee deal underwriting: buyer economics, synergies and downside.

All cash figures are in consistent currency units (e.g. GBP millions).
A deliberately transparent, unlevered acquisition evaluation; not an IFRS PPA,
accounting EPS accretion model, or a levered sponsor IRR calculation.
"""
from dataclasses import dataclass, replace
from math import isfinite


@dataclass(frozen=True)
class DealInputs:
    standalone_ev: float
    offer_ev: float
    annual_run_rate_synergy: float
    synergy_realisation: tuple[float, ...]
    discount_rate: float
    terminal_growth: float
    integration_costs: tuple[float, ...]
    tax_rate: float = 0.25
    perpetual_synergies: bool = True


def _validate(a: DealInputs):
    if not a.synergy_realisation or len(a.synergy_realisation) != len(a.integration_costs):
        raise ValueError("synergy realisation and integration cost schedules must be nonempty and equal length")
    scalar = (a.standalone_ev, a.offer_ev, a.annual_run_rate_synergy,
              a.discount_rate, a.terminal_growth, a.tax_rate)
    all_values = (*scalar, *a.synergy_realisation, *a.integration_costs)
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not isfinite(x)
           for x in all_values):
        raise ValueError("inputs must be finite numbers")
    if any(x < 0 for x in (a.standalone_ev, a.offer_ev, a.annual_run_rate_synergy)):
        raise ValueError("EV and run-rate synergy must be non-negative")
    if a.discount_rate <= a.terminal_growth or a.discount_rate <= -1 or a.terminal_growth <= -1:
        raise ValueError("discount rate must exceed terminal growth; both must exceed -100%")
    if not 0 <= a.tax_rate <= 1:
        raise ValueError("tax rate must be between zero and one")
    if any(not 0 <= x <= 1 for x in a.synergy_realisation):
        raise ValueError("realisation rates must be between zero and one")
    if any(x < 0 for x in a.integration_costs):
        raise ValueError("integration costs must be non-negative")
    if not isinstance(a.perpetual_synergies, bool):
        raise ValueError("perpetual_synergies must be boolean")


def underwrite_deal(a: DealInputs):
    """Discount after-tax synergy cash flows and after-tax integration costs.

    Terminal assumption (when enabled): year-N realised synergy continues,
    increasing at terminal_growth from N+1. No double counting of final-year cash.
    Returns a break-even offer EV and buyer NPV relative to standalone EV.
    """
    _validate(a)
    rows = []
    pv_synergies, pv_costs = 0.0, 0.0
    for year, (realisation, cost) in enumerate(
            zip(a.synergy_realisation, a.integration_costs), 1):
        factor = (1 + a.discount_rate) ** year
        synergy = a.annual_run_rate_synergy * realisation * (1 - a.tax_rate)
        # Simplifying assumption: integration costs are deductible in the year incurred.
        after_tax_cost = cost * (1 - a.tax_rate)
        pv_synergies += synergy / factor
        pv_costs += after_tax_cost / factor
        rows.append({"year": year, "realisation": realisation,
                     "after_tax_synergy": synergy,
                     "after_tax_integration_cost": after_tax_cost,
                     "net_cash_flow": synergy - after_tax_cost,
                     "discount_factor": 1 / factor})
    terminal = 0.0
    if a.perpetual_synergies:
        last_synergy = rows[-1]["after_tax_synergy"]
        terminal = (last_synergy * (1 + a.terminal_growth) /
                    (a.discount_rate - a.terminal_growth) /
                    (1 + a.discount_rate) ** len(rows))
    net_synergy_npv = pv_synergies + terminal - pv_costs
    premium = a.offer_ev - a.standalone_ev
    buyer_npv = net_synergy_npv - premium
    maximum_offer_ev = a.standalone_ev + net_synergy_npv
    return {"standalone_ev": a.standalone_ev, "offer_ev": a.offer_ev,
            "premium": premium, "pv_explicit_synergies": pv_synergies,
            "pv_terminal_synergies": terminal, "pv_integration_costs": pv_costs,
            "net_synergy_npv": net_synergy_npv, "buyer_npv": buyer_npv,
            "maximum_offer_ev": maximum_offer_ev,
            "headroom_to_maximum_offer": maximum_offer_ev - a.offer_ev,
            "premium_capture_pct": premium / net_synergy_npv if net_synergy_npv > 0 else None,
            "value_creating": buyer_npv >= 0, "annual_cash_flows": rows}


def downside_scenarios(base: DealInputs, cases=None):
    """Re-run valuation using explicit assumption shocks; no hidden probabilities."""
    if cases is None:
        cases = {
            "base": {"synergy_factor": 1, "cost_factor": 1, "delay_years": 0},
            "downside": {"synergy_factor": 0.7, "cost_factor": 1.3, "delay_years": 1},
            "severe": {"synergy_factor": 0.4, "cost_factor": 1.6, "delay_years": 2},
        }
    outcome = {}
    for name, shock in cases.items():
        synergy_factor = shock["synergy_factor"]
        cost_factor = shock["cost_factor"]
        delay_years = shock["delay_years"]
        if (isinstance(delay_years, bool) or not isinstance(delay_years, int)
                or delay_years < 0 or delay_years >= len(base.synergy_realisation)):
            raise ValueError("delay_years must be an integer in forecast range")
        if any(isinstance(x, bool) or not isinstance(x, (int, float)) or
               not isfinite(x) or x < 0 for x in (synergy_factor, cost_factor)):
            raise ValueError("scenario factors must be finite and non-negative")
        rates = (0.0,) * delay_years + tuple(base.synergy_realisation[:len(base.synergy_realisation) - delay_years])
        scenario = replace(base, annual_run_rate_synergy=base.annual_run_rate_synergy * synergy_factor,
                           synergy_realisation=rates,
                           integration_costs=tuple(c * cost_factor for c in base.integration_costs))
        outcome[name] = underwrite_deal(scenario)
    return outcome
