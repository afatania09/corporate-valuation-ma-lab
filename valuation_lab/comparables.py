"""Transparent comparable-company multiple analysis."""
from dataclasses import dataclass
from statistics import median

@dataclass(frozen=True)
class Comparable:
    name: str
    enterprise_value: float
    ebitda: float

    @property
    def ev_ebitda(self):
        if self.enterprise_value <= 0 or self.ebitda <= 0:
            raise ValueError("positive EV and EBITDA required for EV/EBITDA")
        return self.enterprise_value / self.ebitda

def comparable_summary(comparables, target_ebitda, selected_multiple=None):
    comps = list(comparables)
    if not comps or target_ebitda <= 0:
        raise ValueError("comparables and positive target EBITDA required")
    multiples = [c.ev_ebitda for c in comps]
    selected = median(multiples) if selected_multiple is None else selected_multiple
    if selected <= 0:
        raise ValueError("selected multiple must be positive")
    return {"low_multiple": min(multiples), "median_multiple": median(multiples),
            "high_multiple": max(multiples), "selected_multiple": selected,
            "implied_ev": target_ebitda * selected,
            "observations": [(c.name, c.ev_ebitda) for c in comps]}
