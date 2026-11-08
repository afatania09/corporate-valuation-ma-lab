"""Simplified exit proceeds allocation with senior preference and common equity.

All amounts share currency units. The preferred security is NON-participating:
it receives the greater of its capped preference or as-converted common value.
Assumes one preferred class, no accrued interest, options or transaction costs.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Preferred:
    invested: float
    liquidation_multiple: float
    as_converted_fraction: float

def allocate_exit_proceeds(exit_equity, preferred: Preferred):
    if exit_equity < 0 or preferred.invested < 0 or preferred.liquidation_multiple < 0:
        raise ValueError("negative proceeds or preference inputs")
    if not 0 <= preferred.as_converted_fraction <= 1:
        raise ValueError("conversion fraction must be between zero and one")
    preference = min(exit_equity, preferred.invested * preferred.liquidation_multiple)
    conversion = exit_equity * preferred.as_converted_fraction
    if conversion > preference:
        preferred_proceeds = conversion
        method = "conversion"
    else:
        preferred_proceeds = preference
        method = "liquidation_preference"
    common_proceeds = exit_equity - preferred_proceeds
    return {"preferred_proceeds": preferred_proceeds,
            "common_proceeds": common_proceeds, "method": method,
            "total_allocated": preferred_proceeds + common_proceeds}
