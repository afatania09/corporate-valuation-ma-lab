"""Plain Markdown investment committee memo from a model result.

Generated report is an illustrative decision-support summary, not an opinion.
"""
from datetime import date

def investment_committee_memo(name, assumptions, result, valuation_date=None):
    if not name or not isinstance(name, str):
        raise ValueError("company name required")
    d = valuation_date or date.today().isoformat()
    lines = [
        f"# Investment committee | {name}",
        f"**Valuation date:** {d}",
        "**Status:** Illustrative model output; not an independent fair-value opinion.",
        "",
        "## Executive summary",
        f"- Entry enterprise value: {result['entry_ev']:,.2f}",
        f"- Initial sponsor equity: {result['sponsor_equity']:,.2f}",
        f"- Exit enterprise value: {result['exit_ev']:,.2f}",
        f"- Exit debt: {result['exit_debt']:,.2f}",
        f"- Exit equity proceeds: {result['exit_equity']:,.2f}",
        f"- Gross sponsor MOIC: {result['moic']:.2f}x",
        f"- Gross sponsor IRR: {result['irr']:.2%}",
        "",
        "## Assumptions",
    ]
    for key, value in vars(assumptions).items():
        lines.append(f"- {key.replace('_', ' ').title()}: {value}")
    lines.extend(["", "## Year-by-year operating and financing bridge",
                  "| Year | Revenue | EBITDA | Interest | Tax | Mandatory debt paydown | Optional debt paydown | Closing debt |",
                  "|---:|---:|---:|---:|---:|---:|---:|---:|"])
    for r in result["years"]:
        lines.append(f"| {r['year']} | {r['revenue']:.2f} | {r['ebitda']:.2f} | "
                     f"{r['interest']:.2f} | {r['taxes']:.2f} | "
                     f"{r['mandatory_repayment']:.2f} | {r['optional_repayment']:.2f} | "
                     f"{r['closing_debt']:.2f} |")
    lines.extend(["", "## Required diligence and limitations",
                  "- Verify earnings quality, sustainability of margin and working-capital assumptions.",
                  "- Support entry and exit multiples with dated comparable-company evidence.",
                  "- Confirm debt covenants, fees, amortisation and liquidity requirements.",
                  "- Analyse tax loss carryforwards, acquisition accounting and management incentives.",
                  "- Test downside cases and valuation sensitivities before any investment decision.",
                  "",
                  "This report uses simplified year-end cash sweeps and gross sponsor returns."])
    return "\n".join(lines) + "\n"
