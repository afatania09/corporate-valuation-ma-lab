# Acquisition completion: sources and uses

The transaction underwriting module values an acquisition on an **enterprise-value** basis. This module separately models how the deal is paid for at completion.

## Conventions

All numbers are in one currency and non-negative except a signed working-capital adjustment. Seller equity value equals offer EV less target debt and debt-like items, plus target cash, cash-like items and the signed working-capital adjustment.

**Uses** include cash paid to sellers, rollover consideration, repayment of target debt and debt-like items, transaction costs and financing fees. **Sources** include new acquisition debt, seller rollover equity, buyer cash, target cash and other cash-like sweeps, and the required new sponsor equity.

Rollover is counted in **both** uses (non-cash seller consideration) and sources (seller reinvestment). Therefore rollover reduces cash paid to sellers and new sponsor equity, but does not reduce total uses.

Target cash and cash-like items are assumed freely available to be swept at closing. In practice, confirm restrictions, minimum cash, trapped cash, taxes and legal structure. Target debt is assumed refinanced in full; do not use this bridge unchanged for debt assumed rather than repaid.

**Working capital** is a closing purchase-price adjustment, not a forecast change in working capital.

## Limitations and controls

- An agreed enterprise-value definition, debt-like schedule, locked-box/completion-accounts mechanism and cash-free/debt-free agreement are prerequisites to a real deal.
- The model rejects negative seller consideration, excess rollover and sources exceeding uses.
- It does not calculate the debt service capacity or covenant headroom for new debt; use the existing acquisition/LBO models separately.
- Buyer cash and new sponsor equity are distinguished; sources must be demonstrably available.
- Rollover equity does not represent the same economic claim as ordinary sponsor cash equity in all structures.
- This is not an accounting purchase-price allocation, tax structuring opinion or legal completion statement.

Run `python -m examples.acquisition_closing_bridge` and `python -m pytest -q`.
