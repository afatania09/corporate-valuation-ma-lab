"""Fictional strategic acquisition: standalone value, integration risk and bid ceiling."""
from valuation_lab.deal_underwriting import DealInputs, downside_scenarios


def main():
    deal = DealInputs(
        standalone_ev=180.0, offer_ev=215.0, annual_run_rate_synergy=9.0,
        synergy_realisation=(0.25, 0.60, 0.85, 1.0, 1.0),
        integration_costs=(12.0, 7.0, 3.0, 0.0, 0.0),
        discount_rate=0.11, terminal_growth=0.02, tax_rate=0.25,
    )
    print("Fictional strategic acquisition | all figures GBP m")
    print("Scenario       Synergy NPV    Premium    Buyer NPV    Max EV    Decision")
    for name, r in downside_scenarios(deal).items():
        print(f"{name:<14} {r['net_synergy_npv']:>11.2f} "
              f"{r['premium']:>10.2f} {r['buyer_npv']:>12.2f} "
              f"{r['maximum_offer_ev']:>9.2f} "
              f"{'VALUE CREATING' if r['value_creating'] else 'DESTROYS VALUE'}")


if __name__ == "__main__":
    main()
