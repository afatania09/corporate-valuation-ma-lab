"""Probability-weighted scenario analysis for portfolio-company equity values."""
from dataclasses import dataclass
from .core import enterprise_value, equity_value

@dataclass(frozen=True)
class Scenario:
    name: str
    probability: float
    ebitda: float
    multiple: float
    net_debt: float

def scenario_weighted_equity(scenarios):
    items = list(scenarios)
    if not items:
        raise ValueError("at least one scenario required")
    if any(s.probability < 0 or s.probability > 1 for s in items):
        raise ValueError("scenario probabilities must be in [0,1]")
    if abs(sum(s.probability for s in items) - 1) > 1e-9:
        raise ValueError("probabilities must total one")
    rows = []
    for s in items:
        ev = enterprise_value(s.ebitda, s.multiple)
        # Limited liability: common equity cannot have negative proceeds.
        eq = max(0.0, equity_value(ev, s.net_debt))
        rows.append({"name": s.name, "probability": s.probability,
                     "enterprise_value": ev, "equity_value": eq,
                     "weighted_equity": s.probability*eq})
    return {"scenarios": rows,
            "expected_equity": sum(row["weighted_equity"] for row in rows)}
