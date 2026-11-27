"""100% cash acquisition, no existing ownership or non-controlling interests."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class BalanceSheet:
    assets: float
    liabilities: float
    equity: float

def consolidate(buyer: BalanceSheet, target: BalanceSheet, price: float,
                new_debt: float, asset_stepup: float, deferred_tax: float,
                expensed_fees: float=0.0):
    values=(*vars(buyer).values(),*vars(target).values(),price,new_debt,asset_stepup,deferred_tax,expensed_fees)
    if not all(isfinite(v) for v in values):
        raise ValueError("Nonfinite inputs")
    for b in (buyer,target):
        if min(b.assets,b.liabilities)<0 or abs(b.assets-b.liabilities-b.equity)>1e-7:
            raise ValueError("Unbalanced opening accounts")
    if min(price,new_debt,asset_stepup,deferred_tax,expensed_fees)<0:
        raise ValueError("Negative acquisition input")
    fair_net_assets=target.equity+asset_stepup-deferred_tax
    goodwill=max(0,price-fair_net_assets)
    bargain_gain=max(0,fair_net_assets-price)
    assets=buyer.assets+target.assets+asset_stepup+goodwill+new_debt-price-expensed_fees
    liabilities=buyer.liabilities+target.liabilities+new_debt+deferred_tax
    equity=buyer.equity-expensed_fees+bargain_gain
    if abs(assets-liabilities-equity)>1e-7:
        raise ArithmeticError("Consolidation failed to reconcile")
    return dict(assets=assets,liabilities=liabilities,equity=equity,
                goodwill=goodwill,bargain_gain=bargain_gain,
                balance_check=assets-liabilities-equity)
