"""Two-factor EV and equity valuation sensitivity."""
from .core import equity_value

def multiple_sensitivity(ebitda_values, multiples, net_debt):
    if not ebitda_values or not multiples:
        raise ValueError("provide EBITDA values and multiples")
    return [{"ebitda": e, "multiple": m, "enterprise_value": e*m,
             "equity_value": equity_value(e*m, net_debt)}
            for e in ebitda_values for m in multiples]
