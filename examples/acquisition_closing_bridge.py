"""Fictional transaction: acquisition price versus financing at completion."""
from valuation_lab.sources_uses import ClosingInputs, closing_sources_uses


def main():
    case = ClosingInputs(
        offer_enterprise_value=215, target_debt=45, target_cash=8,
        debt_like_items=3, cash_like_items=0, working_capital_adjustment=-2,
        transaction_fees=5, financing_fees=3, new_acquisition_debt=110,
        rollover_equity=15, buyer_cash=10)
    r = closing_sources_uses(case)
    print("Fictional acquisition closing bridge (GBP m)")
    print(f"Seller equity value: {r['seller_equity_value']:.2f}")
    print("Uses:")
    for name, value in r["uses"].items():
        print(f"  {name:<31} {value:>10.2f}")
    print("Sources:")
    for name, value in r["sources"].items():
        print(f"  {name:<31} {value:>10.2f}")
    print(f"Sources less uses: {r['reconciliation_difference']:.8f}")


if __name__ == "__main__":
    main()
